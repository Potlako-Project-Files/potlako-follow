from django.test.testcases import TestCase

from edc_call_manager.models import Call
from ..models import WorkList


class TestCallManager(TestCase):

    def setUp(self):
        pass
 
    def test_create_call(self):
        """Testt if a start model created a call instance.
        """
        WorkList.objects.create(subject_identifier='035-123456')
        self.assertEqual(Call.objects.filter(subject_identifier='035-123456').count(), 1)  
