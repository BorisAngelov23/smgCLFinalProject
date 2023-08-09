from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from smgCLFinalProject.auth_app.models import CaptainUser
from smgCLFinalProject.team.models import Team, Player
from smgCLFinalProject.team.forms import TeamRegistrationForm, PlayerForm


class TeamViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='captainuser', password='testpassword'
        )
        self.team = Team.objects.create(captain=self.user)

    def test_team_register_view(self):
        response = self.client.get(reverse('team_register'))
        self.assertEqual(response.status_code, 200)

    def test_team_register_view_with_existing_team(self):
        self.user.team = self.team
        self.user.save()
        response = self.client.get(reverse('team_register'))
        self.assertEqual(response.status_code, 302)

    def test_team_register_view_post(self):
        self.client.login(username='captainuser', password='testpassword')
        response = self.client.post(
            reverse('team_register'),
            data={'paralelki': ['A', 'B', 'C']}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user.team)

    def test_create_multiple_players_view(self):
        self.client.login(username='captainuser', password='testpassword')
        response = self.client.get(reverse('create_multiple_players'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add Players')


class TeamRegistrationFormTest(TestCase):

    def test_valid_form(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        form_data = {'paralelki': ['A', 'B']}
        form = TeamRegistrationForm(data=form_data, user=user)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        form_data = {'paralelki': ['A', 'B', 'C']}
        form = TeamRegistrationForm(data=form_data, user=user)
        self.assertFalse(form.is_valid())
        self.assertIn('You can\'t choose more than 2 classes', form.errors['__all__'][0])


class PlayerFormTest(TestCase):

    def test_valid_form(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'grade': '10',
            'paralelka': 'A',
            'position': 'MF',
        }
        form = PlayerForm(data=form_data, user=user)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        form_data = {
            'first_name': '123',  # Invalid name
            'last_name': 'Doe',
            'grade': '10',
            'paralelka': 'A',
            'position': 'MF',
        }
        form = PlayerForm(data=form_data, user=user)
        self.assertFalse(form.is_valid())
        self.assertIn('Name should only contain letters.', form.errors['__all__'][0])


class PlayerModelTest(TestCase):

    def setUp(self):
        captain_user = CaptainUser.objects.create_user(username='captain', password='testpassword')
        team = Team.objects.create(captain=captain_user, name='Team A', grade='10')
        self.player = Player.objects.create(
            first_name='John',
            last_name='Doe',
            grade='10',
            paralelka='A',
            team=team,
            position='MF'
        )

    def test_player_creation(self):
        player = self.player
        self.assertTrue(isinstance(player, Player))
        self.assertEqual(str(player), f'{player.first_name} {player.last_name}')

    def test_player_default_values(self):
        player = self.player
        self.assertEqual(player.goals, 0)
        self.assertEqual(player.assists, 0)
        self.assertEqual(player.yellow_cards, 0)
        self.assertEqual(player.red_cards, 0)
        self.assertEqual(player.games_played, 0)
        self.assertEqual(player.clean_sheets, 0)
        self.assertFalse(player.is_captain)


class TeamModelTest(TestCase):

    def setUp(self):
        captain_user = CaptainUser.objects.create_user(username='captain', password='testpassword')
        self.team = Team.objects.create(
            captain=captain_user,
            name='Team A',
            grade='10',
            paralelki=['A', 'B', 'C']
        )

    def test_team_creation(self):
        team = self.team
        self.assertTrue(isinstance(team, Team))
        self.assertEqual(str(team), team.name)

    def test_team_default_values(self):
        team = self.team
        self.assertEqual(team.paralelki, ['A', 'B', 'C'])
