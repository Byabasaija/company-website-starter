from django import forms
from django.utils.html import format_html


class _TrixJS:
    def __html__(self):
        return '<script src="https://cdn.jsdelivr.net/npm/trix@2.1.1/dist/trix.umd.min.js"></script>'


class _TrixCSS:
    def __html__(self):
        return '<link href="https://cdn.jsdelivr.net/npm/trix@2.1.1/dist/trix.min.css" rel="stylesheet">'


class _TrixNoUploadJS:
    """Disables file attachment in Trix and hides the attach button."""
    def __html__(self):
        return (
            '<script>'
            'window.addEventListener("trix-file-accept",function(e){e.preventDefault();});'
            'window.addEventListener("trix-initialize",function(e){'
            'var b=e.target.toolbarElement.querySelector("[data-trix-action=\'attachFiles\']");'
            'if(b)b.style.display="none";'
            '});'
            '</script>'
        )


class TrixWidget(forms.Widget):
    class Media:
        css = {'all': (_TrixCSS(),)}
        js = (_TrixJS(), _TrixNoUploadJS())

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
