from django.test import TestCase
from django.urls import reverse

class SimpleTestCase(TestCase):
    def test_homepage_status_code(self):
        # Suppose the homepage is at '/'
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
