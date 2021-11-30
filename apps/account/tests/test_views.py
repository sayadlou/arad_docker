from django.test import TestCase
from django.urls import reverse


class ViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def test_home(self):
        response = self.client.get('/profile/login')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('profile:login'))
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'core/home.html')

    def test_home(self):
        pass
