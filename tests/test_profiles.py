from django.test import TestCase, Client
from django.urls import reverse


def make_category(name, order=0):
    from django.utils.text import slugify
    from profiles.models import ProfileCategory
    return ProfileCategory.objects.create(name=name, slug=slugify(name), order=order)


def make_profile(name, category, order=0, is_active=True):
    from django.utils.text import slugify
    from profiles.models import Profile
    return Profile.objects.create(
        name=name, slug=slugify(name), role='Manager',
        category=category, order=order, is_active=is_active,
    )


class ProfileCategoryTest(TestCase):
    def test_categories_ordered_by_order(self):
        make_category('Board', order=2)
        make_category('Executives', order=1)
        from profiles.models import ProfileCategory
        names = list(ProfileCategory.objects.values_list('name', flat=True))
        self.assertEqual(names[0], 'Executives')

    def test_str_returns_name(self):
        cat = make_category('Executives')
        self.assertEqual(str(cat), 'Executives')


class ProfileModelTest(TestCase):
    def setUp(self):
        self.cat = make_category('Executives')

    def test_slug_stored(self):
        p = make_profile('Jane Doe', self.cat)
        self.assertEqual(p.slug, 'jane-doe')

    def test_slug_auto_generated_if_blank(self):
        from profiles.models import Profile
        p = Profile.objects.create(name='Auto Slug', role='CEO', category=self.cat)
        self.assertEqual(p.slug, 'auto-slug')

    def test_slug_unique_on_conflict(self):
        from profiles.models import Profile
        Profile.objects.create(name='Same Name', role='A', category=self.cat)
        p2 = Profile.objects.create(name='Same Name', role='B', category=self.cat)
        self.assertNotEqual(p2.slug, 'same-name')

    def test_inactive_profiles_exist_in_db(self):
        make_profile('Hidden', self.cat, is_active=False)
        from profiles.models import Profile
        self.assertEqual(Profile.objects.filter(is_active=False).count(), 1)

    def test_str_returns_name(self):
        p = make_profile('Jane Doe', self.cat)
        self.assertEqual(str(p), 'Jane Doe')


class ProfileListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.cat = make_category('Executives')
        make_profile('Alice', self.cat)
        make_profile('Bob', self.cat, is_active=False)

    def test_list_returns_200(self):
        response = self.client.get(reverse('profile-list'))
        self.assertEqual(response.status_code, 200)

    def test_list_context_has_profiles(self):
        response = self.client.get(reverse('profile-list'))
        self.assertIn('profiles', response.context)

    def test_list_context_has_categories(self):
        response = self.client.get(reverse('profile-list'))
        self.assertIn('categories', response.context)

    def test_list_only_shows_active_profiles(self):
        response = self.client.get(reverse('profile-list'))
        self.assertEqual(len(response.context['profiles']), 1)

    def test_list_page_has_category_filter(self):
        response = self.client.get(reverse('profile-list'))
        self.assertContains(response, 'executives')


class ProfileDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.cat = make_category('Board')

    def test_detail_returns_200(self):
        p = make_profile('John Smith', self.cat)
        response = self.client.get(reverse('profile-detail', args=[p.slug]))
        self.assertEqual(response.status_code, 200)

    def test_detail_404_for_inactive(self):
        p = make_profile('Hidden Person', self.cat, is_active=False)
        response = self.client.get(reverse('profile-detail', args=[p.slug]))
        self.assertEqual(response.status_code, 404)

    def test_detail_context_has_profile(self):
        p = make_profile('John Smith', self.cat)
        response = self.client.get(reverse('profile-detail', args=[p.slug]))
        self.assertEqual(response.context['profile'].name, 'John Smith')
