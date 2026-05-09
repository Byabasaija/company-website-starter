from django.test import TestCase, Client
from gallery.models import GalleryCategory, GalleryImage


def make_category(name, order=0):
    from django.utils.text import slugify
    return GalleryCategory.objects.create(name=name, slug=slugify(name), order=order)


class GalleryCategoryTest(TestCase):

    def test_categories_ordered_by_order(self):
        make_category('Chess Boards', order=2)
        make_category('Tournaments', order=1)
        cats = list(GalleryCategory.objects.values_list('name', flat=True))
        self.assertEqual(cats[0], 'Tournaments')

    def test_slug_stored(self):
        cat = make_category('Annual Cup')
        self.assertEqual(cat.slug, 'annual-cup')


class GalleryImageTest(TestCase):

    def setUp(self):
        self.cat = make_category('General')

    def test_active_images_filtered(self):
        GalleryImage.objects.create(category=self.cat, image='gallery/a.jpg', order=1, is_active=True)
        GalleryImage.objects.create(category=self.cat, image='gallery/b.jpg', order=2, is_active=False)
        self.assertEqual(GalleryImage.objects.filter(is_active=True).count(), 1)

    def test_images_ordered_by_order(self):
        GalleryImage.objects.create(category=self.cat, image='gallery/b.jpg', order=2, is_active=True)
        GalleryImage.objects.create(category=self.cat, image='gallery/a.jpg', order=1, is_active=True)
        imgs = list(GalleryImage.objects.all())
        self.assertEqual(imgs[0].order, 1)


class GalleryViewTest(TestCase):

    def test_gallery_returns_200(self):
        response = self.client.get('/gallery/')
        self.assertEqual(response.status_code, 200)

    def test_gallery_context_has_images_and_categories(self):
        response = self.client.get('/gallery/')
        self.assertIn('images', response.context)
        self.assertIn('categories', response.context)


class GalleryLightboxTest(TestCase):

    def setUp(self):
        cat = make_category('Test')
        GalleryImage.objects.create(
            category=cat, image='gallery/test.jpg', order=1, is_active=True
        )

    def test_gallery_page_has_lightbox_show_handler(self):
        response = self.client.get('/gallery/')
        self.assertContains(response, '@click="show(')

    def test_gallery_page_has_lightbox_overlay(self):
        response = self.client.get('/gallery/')
        self.assertContains(response, 'fixed inset-0')
        self.assertContains(response, ':src="src"')
