from django import forms
from django.utils.html import format_html


class TrixWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        field_id = attrs.get('id', f'id_{name}')
        return format_html(
            '<input type="hidden" id="{}" name="{}" value="{}">'
            '<trix-editor input="{}" '
            'class="trix-content border border-gray-300 rounded-lg min-h-[200px] p-2">'
            '</trix-editor>',
            field_id,
            name,
            value or '',
            field_id,
        )

    def value_from_datadict(self, data, files, name):
        return data.get(name)

    class Media:
        css = {'all': ('https://unpkg.com/trix@2/dist/trix.css',)}
        js = ('https://unpkg.com/trix@2/dist/trix.umd.min.js',)
