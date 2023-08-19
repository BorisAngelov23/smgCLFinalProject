from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from smgCLFinalProject.auth_app.models import CaptainUser
from smgCLFinalProject.team.models import Team
from smgCLFinalProject.team.forms import TeamRegistrationForm


class AuthAppViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.team = Team.objects.create(captain=self.user)

    def test_captain_register_view(self):
        response = self.client.post(
            reverse("captain_register"),
            data={
                "username": "newuser",
                "password1": "newpassword",
                "password2": "newpassword",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CaptainUser.objects.filter(
            username="newuser").exists())

    def test_captain_login_view(self):
        response = self.client.post(
            reverse("captain_login"),
            data={"username": "testuser", "password": "testpassword"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.login(
            username="testuser", password="testpassword"))

    def test_captain_logout_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("captain_logout"))
        self.assertEqual(response.status_code, 302)

    def test_captain_details_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("captain_details"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to your profile")


class ViewsIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CaptainUser.objects.create_user(
            username="testuser",
            password="testpassword",
            grade="10",
            paralelka="A",
            phone_number="1234567890",
            facebook_link="https://facebook.com/testuser",
            position="MF",
        )

    def test_captain_register_view(self):
        response = self.client.get(reverse("captain_register"))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("captain_register"),
            data={
                "username": "newuser",
                "password1": "newpassword",
                "password2": "newpassword",
                "grade": "8",
                "paralelka": "A",
                "phone_number": "9876543210",
                "facebook_link": "https://facebook.com/newuser",
                "position": "GK",
            },
        )
        self.assertEqual(response.status_code, 302)

        new_user = CaptainUser.objects.get(username="newuser")
        self.assertEqual(new_user.grade, "8")


class AuthAppIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_captain_register_view(self):
        response = self.client.get(reverse("captain_register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth_app/register.html")

    def test_captain_register_submit_valid_form(self):
        response = self.client.post(
            reverse("captain_register"),
            data={
                "username": "testuser",
                "password1": "testpassword",
                "password2": "testpassword",
                "grade": "9",
                "paralelka": "A",
                "phone_number": "1234567890",
                "facebook_link": "https://facebook.com/testuser",
                "position": "MF",
            },
        )
        self.assertEqual(response.status_code, 302)

        new_user = CaptainUser.objects.get(username="testuser")
        self.assertEqual(new_user.grade, "9")

    def test_captain_register_submit_invalid_form(self):
        response = self.client.post(
            reverse("captain_register"),
            data={
                "username": "testuser",
                "password1": "testpassword",
                "password2": "wrongpassword",
                "grade": "13",
                "paralelka": "A",
                "phone_number": "1234567890",
                "facebook_link": "https://facebook.com/testuser",
                "position": "MF",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_captain_login_view(self):
        response = self.client.get(reverse("captain_login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth_app/login.html")
