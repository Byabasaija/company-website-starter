from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from core.widgets import TrixWidget
from events.admin import EventAdmin
from events.models import Event
from core.admin import AboutSectionAdmin, ServiceAdmin
from core.models import AboutSection, Service


class TrixWidgetTest(TestCase):
    def test_renders_trix_editor_element(self):
        widget = TrixWidget()
        html = widget.render('description', '', attrs={'id': 'id_description'})
        self.assertIn('<trix-editor', html)

    def test_trix_editor_input_attribute_matches_textarea_id(self):
        widget = TrixWidget()
        html = widget.render('description', '', attrs={'id': 'id_description'})
        self.assertIn('input="id_description"', html)

    def test_textarea_is_hidden(self):
        widget = TrixWidget()
        html = widget.render('description', '', attrs={'id': 'id_description'})
        self.assertIn('hidden', html)


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
