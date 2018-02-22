from django import forms
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.safestring import mark_safe


class InternalExternalTextBoxWidget(forms.Textarea):
    template_name = 'internal_external_comments/internal_external_textbox_widget.html'
    
    def __init__(self, *args, **kwargs):
        self.internal_external = kwargs.pop('internal_external', "internal")
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
            final_attrs['class'] = 'internal_external_editor form-control'
        else:
            if 'form-control' not in final_attrs.get('class'):
                # add in form control bootstrap tag if not there just to get some initial styling
                final_attrs['class'] = ' '.join(final_attrs['class'].split(' ') + ['form-control'])
            final_attrs['class'] = ' '.join(final_attrs['class'].split(' ') +
                                            ['internal_external_editor'])
        if self.internal_external == 'internal':
            final_attrs['class'] = ' '.join(final_attrs['class'].split(' ') +
                                            ['internal_external_editor_internal'])

        assert 'id' in final_attrs, "InternalExternal Text Box widget attributes must contain 'id'"

        html = [
            '<div class="col-sm-10">',
            '<span class="note_header btn{}"'.format(" active_note" if self.internal_external == "internal" else ""),
            ' id="internal_external_status_set_internal">Internal Note</span>',
            '<span class="note_header btn{}"'.format(" active_note" if self.internal_external != "internal" else ""),
            ' id="internal_external_status_set_external">External Note</span>',
            '<textarea{!s}>{!s}</textarea>'.format(flatatt(final_attrs), escape(value)),
            '</div>'
        ]
        return mark_safe('\n'.join(html))

    # def __init__(self, internal_external="internal", internal_allow=False, attrs=None):
    #     self.internal_external = internal_external
    #     self.internal_allow = internal_allow
    #     default_attrs = {'cols': '40', 'rows': '10',
    #                      'class': 'internal_external_editor form-control'}
    #     if attrs:
    #         default_attrs.update(attrs)
    #     super().__init__(default_attrs)

    # def get_context(self, name, value, attrs):
    #     context = super().get_context(name, value, attrs)
    #     context['widget']['internal_external_allow_internal'] = self.internal_allow
    #     return context

    # def build_attrs(self, base_attrs, extra_attrs=None, *args, **kwargs):
    #     attrs = super().build_attrs(base_attrs, extra_attrs, *args, **kwargs)
    #     if 'form-control' not in attrs.get('class'):
    #         # add in form control bootstrap tag if not there just to get some initial styling
    #         attrs['class'] = ' '.join(attrs['class'].split(' ') + ['form-control'])
    #     if 'internal_external_editor' not in attrs.get('class'):
    #         # make sure internal_external_editor class exists
    #         attrs['class'] = ' '.join(attrs['class'].split(' ') + ['internal_external_editor'])
    #     if self.internal_external is 'internal' and self.internal_allow:
    #         attrs['class'] = ' '.join(attrs['class'].split(
    #             ' ') + ['internal_external_editor_internal'])
    #     return attrs

    class Media:
        css = {
            'all': ('internal_external_comments/css/internalexternalwidget.css',)
        }
        js = ('internal_external_comments/js/internalexternalwidget.js',)
