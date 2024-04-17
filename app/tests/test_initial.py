from django.test import TestCase, Client
from django.urls import reverse

from operators.services import initial_creation


class InitialTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.operator = initial_creation().get()

    def auth(self):
        from django.contrib.auth.models import User
        user = User.objects.get(username="Aneta Demová")
        self.client.force_login(user=user)

    def test_homepage(self):
        response = self.client.get(reverse('welcome-page'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_navbar_items(self):
        self.auth()
        response = self.client.get(reverse("clients"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("proposals"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("contracts"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("reports"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("create-proposal"))
        self.assertEqual(response.status_code, 200)
