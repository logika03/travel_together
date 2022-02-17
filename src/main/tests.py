from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from factory.django import DjangoModelFactory
import factory

from main.models import Trip

User = get_user_model()


# class UserFactory(DjangoModelFactory):
#     class Meta:
#         model = User
#
#     email = factory.Faker('email')
#     first_name = factory.Faker('first_name')
#     last_name = factory.Faker('last_name')


class MainTests(TestCase):
    def setUp(self):
        User.objects.create(
            email='sd@sd.ru'
        )
        user = User.objects.first()
        self.user = user
        Trip.objects.create(
            author=self.user,
            description='Trip',
            country='Russia',
            city='Kazan',
            city_information='https://yandex.ru',
            date=datetime.now().date(),
        )
        Trip.objects.create(
            author=self.user,
            description='Trip2',
            country='Russia',
            city='Kazan',
            city_information='https://yandex.ru',
            date=datetime.now().date(),
        )

    def test_signup(self):
        c = Client()
        signup_user(c)
        user = User.objects.get(email='test2@test.ru')
        self.assertEqual(user.is_authenticated, True)
        url = reverse('logout')
        response = c.get(url)
        self.assertEqual(response.status_code, 302)

    def test_find_trip(self):  # fail
        c = Client()
        url = reverse('find')
        response = c.post(url, {
            'country': 'Russia',
            'city': 'Kazan',
        })
        self.assertIsNot(response.status_code, 500)

    def test_get_account(self):
        c = Client()
        url = reverse('account', args=[self.user.id])
        response = c.get(url)
        self.assertEqual(response.status_code, 302)
        response = c.get(f'account/{self.user.email}/')
        self.assertEqual(response.status_code, 404)

    def test_reset_password_auth_user(self):
        c = Client()
        signup_user(c)
        url = reverse('change_password', args=['1'])
        response = c.get(url)
        self.assertEqual(response.status_code, 302)

    def test_change_password(self):
        c = Client()
        url = reverse('reset')
        c.post(url, {
            'email': self.user.email
        })
        cur_password = self.user.password
        url = reverse('change_password', args=[self.user.id])
        c.post(url, {
            'password': '123qaZ'
        })
        new_password = User.objects.first().password
        self.assertIsNot(cur_password, new_password)

    def test_non_existent_page(self):
        c = Client()
        response = c.get('/dfkvsfn/')
        self.assertEqual(response.status_code, 404)


def signup_user(c: Client):
    url = reverse('signup')
    return c.post(url, {
        'id': '105',
        'first_name': 'Test',
        'last_name': 'Test',
        'phone_number': '89999999999',
        'email': 'test2@test.ru',
        'password1': '123qaZ',
        'password2': '123qaZ',
    })
