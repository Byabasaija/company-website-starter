from django import forms


class TrixWidget(forms.Textarea):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        field_id = attrs.get('id', f'id_{name}')
        attrs['hidden'] = True
        textarea = super().render(name, value, attrs, renderer)
        return (
            f'{textarea}'
            f'<trix-editor input="{field_id}" '
            f'class="trix-content border border-gray-300 rounded-lg min-h-[200px] p-2">'
            f'</trix-editor>'
        )

    class Media:
        css = {'all': ('https://unpkg.com/trix@2/dist/trix.css',)}
        js = ('https://unpkg.com/trix@2/dist/trix.umd.min.js',)
