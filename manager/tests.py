from django.test import TestCase
from django.test.urlresolvers import reverse

from .models import *

# Create your tests here.

class test_index(TestCase):
    def test_index_works(self):
        '''index should return a found value'''
        response = self.client.get(reverse('manage:index'))
        self.assertEqual(response.status_code, 200)
