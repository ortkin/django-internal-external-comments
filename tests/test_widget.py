from django.test import SimpleTestCase

from internal_external_comments.widgets import InternalExternalTextBoxWidget


class InternalExternalWidgetTests(SimpleTestCase):
    """
    initial widget attributes as defined hard coded:
        {cols': '40', 'rows': '10', 'class': 'internal_external_editor form-control'}
    """
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
        self.assertIn('rows="10"', html)
        self.assertIn('form-control', html)

    def test_InternalExternalTextBoxWidget_class_widget(self):
        html = self.widget.render(
            'thename', 'some test value', attrs={'id': 'id_thename', 'class': 'blah'}
        )
        self.assertIn('id="id_thename"', html)
        self.assertIn('name="thename"', html)
        self.assertIn('some test value', html)
        self.assertIn('class="blah', html)

    def test_InternalExternalTextBoxWidget_with_widget_attributes(self):
        # should only have default attributes set
        widget = InternalExternalTextBoxWidget(
            attrs={'cols': 30, 'rows': 13, 'class': 'crappyclass'})
        html = widget.render(
            'thename', 'some test value'
            )
        self.assertIn('cols="30"', html)
        self.assertIn('rows="13"', html)
        self.assertIn('crappyclass', html)

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
        widget = InternalExternalTextBoxWidget(internal_allow=True)
        html = widget.render(
            'thename', None, attrs={'id': 'id_thename', 'class': 'form-control', 'rows': '5'}
        )
        self.assertIn('internal_external_editor_internal', html)

    def test_InternalExternalTextBoxWidget_initial(self):
        widget = InternalExternalTextBoxWidget(internal_external="external")
        html = widget.render(
            'thename', None, attrs={'id': 'id_thename'}
        )
        self.assertNotIn('internal_external_editor_internal', html)
