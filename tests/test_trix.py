from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.utils.safestring import SafeData
from core.widgets import TrixWidget
from events.admin import EventAdmin
from events.models import Event
from core.admin import AboutSectionAdmin, ServiceAdmin
from core.models import AboutSection, Service


class TrixWidgetTest(TestCase):
    def setUp(self):
        self.widget = TrixWidget()
        self.html = self.widget.render('body', 'existing text', attrs={'id': 'id_body'})

    def test_renders_trix_editor_element(self):
        self.assertIn('<trix-editor', self.html)

    def test_trix_editor_input_attribute_matches_id(self):
        self.assertIn('input="id_body"', self.html)

    def test_hidden_input_carries_existing_value(self):
        self.assertIn('value="existing text"', self.html)

    def test_hidden_input_has_correct_name(self):
        self.assertIn('name="body"', self.html)

    def test_returns_safe_string(self):
        self.assertIsInstance(self.html, SafeData)


class EventAdminTrixTest(TestCase):
    def test_event_admin_uses_trix_widget_for_description(self):
        site = AdminSite()
        admin_instance = EventAdmin(Event, site)
        form_class = admin_instance.get_form(request=None)
        widget = form_class().fields['description'].widget
        self.assertIsInstance(widget, TrixWidget)


class CoreAdminTrixTest(TestCase):
    def test_about_section_admin_uses_trix_widget_for_body(self):
        site = AdminSite()
        admin_instance = AboutSectionAdmin(AboutSection, site)
        form_class = admin_instance.get_form(request=None)
        widget = form_class().fields['body'].widget
        self.assertIsInstance(widget, TrixWidget)

    def test_service_admin_uses_trix_widget_for_description(self):
        site = AdminSite()
        admin_instance = ServiceAdmin(Service, site)
        form_class = admin_instance.get_form(request=None)
        widget = form_class().fields['description'].widget
        self.assertIsInstance(widget, TrixWidget)
