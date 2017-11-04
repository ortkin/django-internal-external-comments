from django.test import SimpleTestCase
from django.forms.renderers import DjangoTemplates, Jinja2

from internal_external_comments.widgets import InternalExternalTextBoxWidget


try:
    import jinja2
except ImportError:
    jinja2 = None


class InternalExternalWidgetTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        cls.django_renderer = DjangoTemplates()
        cls.jinja2_renderer = Jinja2() if jinja2 else None
        cls.renderers = [cls.django_renderer] + ([cls.jinja2_renderer] if cls.jinja2_renderer else [])
        super().setUpClass()

    def check_html(self, widget, name, value, html='', attrs=None, strict=False, **kwargs):
        assertEqual = self.assertEqual if strict else self.assertHTMLEqual
        if self.jinja2_renderer:
            output = widget.render(name, value, attrs=attrs, renderer=self.jinja2_renderer, **kwargs)
            # Django escapes quotes with '&quot;' while Jinja2 uses '&#34;'.
            assertEqual(output.replace('&#34;', '&quot;'), html)

        output = widget.render(name, value, attrs=attrs, renderer=self.django_renderer, **kwargs)
        assertEqual(output, html)

    def test_InternalExternalTextBoxWidget_widget(self):
        widget = InternalExternalTextBoxWidget()
        html = widget.render(
            'thename', 'some test value', attrs={'id': 'id_thename'}
        )
        self.assertIn('id="id_thename"', html)
        self.assertIn('name="thename"', html)
        self.assertIn('some test value', html)

    def test_InternalExternalTextBoxWidget_None_Value_widget(self):
        widget = InternalExternalTextBoxWidget()
        html = widget.render(
            'thename', None, attrs={'id': 'id_thename'}
        )
        self.assertIn('id="id_thename"', html)
        self.assertIn('name="thename"', html)
        self.assertIn('', html)

    def test_InternalExternalTextBoxWidget_class_widget(self):
        widget = InternalExternalTextBoxWidget()
        html = widget.render(
            'thename', 'some test value', attrs={'id': 'id_thename', 'class': 'blah'}
        )
        self.assertIn('id="id_thename"', html)
        self.assertIn('name="thename"', html)
        self.assertIn('some test value', html)
        self.assertIn('class="blah', html)

    def test_InternalExternalTextBoxWidget_no_id(self):
        widget = InternalExternalTextBoxWidget()
        try:
            widget.render(
                'thename', 'some test value', attrs={}
            )
            self.fail("expecting widget to fail without an id")
        except Exception as e:
            self.assertEqual("InternalExternal Text Box widget attributes must contain 'id'", e.args[0])
