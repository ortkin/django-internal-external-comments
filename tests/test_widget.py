from django.test import SimpleTestCase
from django import forms
from django_comments.forms import CommentForm

from internal_external_comments.widgets import InternalExternalTextBoxWidget


class InternalExternalWidgetTests(SimpleTestCase):
    widget = InternalExternalTextBoxWidget()

    def test_InternalExternalTextBoxWidget_widget(self):
        html = self.widget.render(
            'thename', 'some test value', attrs={'id': 'id_thename'}
        )
        self.assertIn('id="id_thename"', html)
        self.assertIn('name="thename"', html)
        self.assertIn('some test value', html)

    def test_InternalExternalTextBoxWidget_None_Value_widget(self):
        html = self.widget.render(
            'thename', None, attrs={'id': 'id_thename'}
        )
        self.assertIn('id="id_thename"', html)
        self.assertIn('name="thename"', html)
        self.assertIn('rows="3"', html)
        self.assertIn('form-control', html)

    def test_InternalExternalTextBoxWidget_class_widget(self):
        html = self.widget.render(
            'thename', 'some test value', attrs={'id': 'id_thename', 'class': 'blah'}
        )
        self.assertIn('id="id_thename"', html)
        self.assertIn('name="thename"', html)
        self.assertIn('some test value', html)
        self.assertIn('class="blah', html)

    def test_InternalExternalTextBoxWidget_no_id(self):
        try:
            self.widget.render(
                'thename', 'some test value', attrs={}
            )
            self.fail("expecting widget to fail without an id")
        except Exception as e:
            self.assertEqual("InternalExternal Text Box widget attributes must contain 'id'", e.args[0])

    def test_InternalExternalTextBoxWidget_with_attributes(self):
        html = self.widget.render(
            'thename', None, attrs={'id': 'id_thename', 'class': 'form-control', 'rows': '5'}
        )
        self.assertIn('id="id_thename"', html)
        self.assertIn('name="thename"', html)
        self.assertIn('rows="5"', html)
        self.assertIn('form-control', html)
        self.assertIn('internal_external_editor', html)

    def test_InternalExternalTextBoxWidget_internal_classes(self):
        html = self.widget.render(
            'thename', None, attrs={'id': 'id_thename', 'class': 'form-control', 'rows': '5'}
        )
        self.assertIn('internal_external_editor_internal', html)

    def test_InternalExternalTextBoxWidget_initial(self):
        widget = InternalExternalTextBoxWidget(internal_external="external")
        html = widget.render(
            'thename', None, attrs={'id': 'id_thename'}
        )
        self.assertNotIn('internal_external_editor_internal', html)
