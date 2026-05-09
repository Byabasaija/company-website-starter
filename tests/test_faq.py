from django.test import TestCase, Client
from faq.models import FAQItem


class FAQItemTest(TestCase):

    def test_active_items_ordered(self):
        FAQItem.objects.create(question='Q2', answer='A2', order=2, is_active=True)
        FAQItem.objects.create(question='Q1', answer='A1', order=1, is_active=True)
        items = list(FAQItem.objects.filter(is_active=True))
        self.assertEqual(items[0].question, 'Q1')

    def test_inactive_excluded(self):
        FAQItem.objects.create(question='Q-active', answer='A', order=1, is_active=True)
        FAQItem.objects.create(question='Q-hidden', answer='A', order=2, is_active=False)
        self.assertEqual(FAQItem.objects.filter(is_active=True).count(), 1)


class FAQViewTest(TestCase):

    def test_faq_returns_200(self):
        response = self.client.get('/faq/')
        self.assertEqual(response.status_code, 200)

    def test_faq_context_has_items(self):
        FAQItem.objects.create(question='Q', answer='A', order=1, is_active=True)
        response = self.client.get('/faq/')
        self.assertIn('faq_items', response.context)
        self.assertEqual(len(response.context['faq_items']), 1)
