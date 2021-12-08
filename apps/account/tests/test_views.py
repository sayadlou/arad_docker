from django.test import TestCase
from django.urls import reverse

from ..models import UserProfile


class ViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        UserProfile.objects.create_user("saeid", email="aa@bb.cc", password="asdDFe43sefsedsd")

    def test_login(self):
        response = self.client.get(reverse('account:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')


    def test_logout(self):
        response = self.client.get(reverse('account:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/logged_out.html')

    def test_profile(self):
        response = self.client.get(reverse('account:profile'))
        self.assertEqual(response.status_code, 302)
        self.client.login(username='saeid', password='asdDFe43sefsedsd')
        response = self.client.get(reverse('account:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/profile.html')

    def test_password_change(self):
        response = self.client.get(reverse('account:password_change'))
        self.assertEqual(response.status_code, 302)
        self.client.login(username='saeid', password='asdDFe43sefsedsd')
        response = self.client.get(reverse('account:password_change'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/password_change_form.html')

    def test_password_change_done(self):
        # self.client.login(username='saeid', password='asdDFe43sefsedsd')
        response = self.client.get(reverse('account:password_change_done'))
        self.assertEqual(response.status_code, 302)
        self.client.login(username='saeid', password='asdDFe43sefsedsd')
        response = self.client.get(reverse('account:password_change_done'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/password_change_done.html')

    def test_password_reset(self):
        response = self.client.get(reverse('account:password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/password_reset_form.html')

    def test_password_reset_done(self):
        response = self.client.get(reverse('account:password_reset_done'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/password_reset_done.html')

    def test_password_reset_complete(self):
        response = self.client.get(reverse('account:password_reset_complete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/password_reset_complete.html')

    def test_signup(self):
        my_data = {'address': "some where",
                   'first_name': "saesrgrid",
                   'last_name': "saessefid",
                   'mobile': "saeid",
                   'phone': "saeid",
                   'username': "saeidsef",
                   'email': "saeid@sef.csdf",
                   'password1': "saeidDSE216.",
                   'password2': "saeidDSE216.",
                    'captcha_0': 'dummy-value',
                   'captcha_1': 'PASSED',
                   }

        response = self.client.post(
            reverse('account:signup'),
            data=my_data
            # data={
            #     "username": "sayadlou3",
            #     "first_name": "saeid",
            #     "last_name": "sayadlou",
            #     "mobile": "09124633829",
            #     "phone": "02166403092",
            #     "email": "saeid@jgcsdf.com",
            #     "address": "some where",
            #     "password1": "Dkasad123.",
            #     "password2": "Dkasad123.",
            #     'captcha_0': 'dummy-value',
            #     'captcha_1': 'PASSED',
            # }
        )
        print(UserProfile.objects.all().count())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(UserProfile.objects.all().count(), 2)
        # self.assertTemplateUsed(response, 'account/password_reset_complete.html')
