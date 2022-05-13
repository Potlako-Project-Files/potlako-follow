from django.test import TestCase, tag
from django.core.exceptions import ValidationError
from edc_constants.constants import NO
from edc_call_manager.models import Call
from ..models import WorkList
from ..forms import LogEntryFormValidator


class TestCallManager(TestCase):

    def setUp(self):
        self.data={
            'patient_reached':'Yes',
            'comment': 'blah',         
        }
 
    def test_create_call(self):
        """Testt if a start model created a call instance.
        """
        WorkList.objects.create(subject_identifier='035-123456')
        self.assertEqual(Call.objects.filter(subject_identifier='035-123456').count(), 1)  
    
    @tag('cm')
    def test_comment_required(self):
        
        field_name = 'comment'
        self.data[field_name] = None
        self.data['patient_reached'] = NO

        form_validator = LogEntryFormValidator(cleaned_data=self.data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn(field_name, form_validator._errors)
     
