from django import forms
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.safestring import mark_safe


class InternalExternalTextBoxWidget(forms.Textarea):

    def __init__(self, *args, **kwargs):
        super(InternalExternalTextBoxWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        value = force_text(value)
        final_attrs = self.build_attrs(attrs)
        final_attrs['name'] = name
        if final_attrs.get('rows', None) is None:
            final_attrs['rows'] = 3
        if final_attrs.get('class', None) is None:
            final_attrs['class'] = 'internal_external_editor internal_active form-control'
        else:
            if 'form-control' not in final_attrs.get('class'):
                # add in form control bootstrap tag if not there just to get some initial styling
                final_attrs['class'] = ' '.join(final_attrs['class'].split(' ') + ['form-control'])
            final_attrs['class'] = ' '.join(final_attrs['class'].split(' ') +
                                            ['internal_external_editor internal_external_editor_active'])
        assert 'id' in final_attrs, "InternalExternal Text Box widget attributes must contain 'id'"
        html = [
            '<div class="col-sm-10">',
            '<span class="note_header active_note" id="internal_external_status_set_internal">Internal Note</span>',
            '<span class="note_header" id="internal_external_status_set_external">External Note</span>',
            '<textarea{!s}>{!s}</textarea>'.format(flatatt(final_attrs), escape(value)),
            '</div>'
        ]
        return mark_safe('\n'.join(html))

    class Media:
        css = {
            'all': ('internal_external_comments/css/internalexternalwidget.css',)
        }
        js = ('internal_external_comments/js/internalexternalwidget.js',)
