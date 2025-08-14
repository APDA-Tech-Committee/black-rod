"""
Tests for team views
"""
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from datetime import date

from core.models import School, Tournament, Debater, Team
from core.models.results.team import TeamResult


class TeamViewsTest(TestCase):
    """Test team views"""

    def setUp(self):
        self.client = Client()
        self.school = School.objects.create(name="Test School")
        self.debater1 = Debater.objects.create(
            first_name="John",
            last_name="Doe",
            school=self.school
        )
        self.debater2 = Debater.objects.create(
            first_name="Jane",
            last_name="Smith",
            school=self.school
        )
        self.team = Team.objects.create(name="Test Team")
        self.team.debaters.add(self.debater1, self.debater2)
        
        self.tournament = Tournament.objects.create(
            name="Test Tournament",
            host=self.school,
            date=date(2024, 1, 1),
            season="2024"
        )

    def test_team_list_view(self):
        """Test team list view"""
        response = self.client.get(reverse('core:teams'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Team")

    def test_team_detail_view(self):
        """Test team detail view"""
        response = self.client.get(
            reverse('core:team_detail', kwargs={'pk': self.team.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Team")

    def test_team_with_results(self):
        """Test team view with results"""
        # Create team result
        team_result = TeamResult.objects.create(
            team=self.team,
            tournament=self.tournament,
            wins=3,
            total_speaks=150
        )
        
        response = self.client.get(
            reverse('core:team_detail', kwargs={'pk': self.team.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Team")

    def test_team_search_view(self):
        """Test team search functionality"""
        response = self.client.get(reverse('core:teams'), {'search': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Team")

    def test_team_filter_by_school(self):
        """Test filtering teams by school"""
        # Create another school and team
        school2 = School.objects.create(name="Other School")
        debater3 = Debater.objects.create(
            first_name="Bob",
            last_name="Johnson",
            school=school2
        )
        team2 = Team.objects.create(name="Other Team")
        team2.debaters.add(debater3)
        
        response = self.client.get(reverse('core:teams'), {'school': self.school.pk})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Team")

    def test_nonexistent_team_404(self):
        """Test that non-existent team returns 404"""
        response = self.client.get(
            reverse('core:team_detail', kwargs={'pk': 99999})
        )
        self.assertEqual(response.status_code, 404)

    def test_team_with_multiple_results(self):
        """Test team with multiple tournament results"""
        # Create multiple results
        for i in range(3):
            tournament = Tournament.objects.create(
                name=f"Tournament {i}",
                host=self.school,
                date=date(2024, i+1, 1),
                season="2024"
            )
            TeamResult.objects.create(
                team=self.team,
                tournament=tournament,
                wins=i+1,
                total_speaks=100 + i*10
            )
        
        response = self.client.get(
            reverse('core:team_detail', kwargs={'pk': self.team.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_hybrid_team_display(self):
        """Test hybrid team display"""
        # Make one debater independent (hybrid team)
        self.debater2.is_independent = True
        self.debater2.save()
        
        response = self.client.get(
            reverse('core:team_detail', kwargs={'pk': self.team.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Team")

    def test_team_statistics_view(self):
        """Test team statistics display"""
        # Create results for statistics
        TeamResult.objects.create(
            team=self.team,
            tournament=self.tournament,
            wins=4,
            total_speaks=180
        )
        
        response = self.client.get(
            reverse('core:team_detail', kwargs={'pk': self.team.pk})
        )
        self.assertEqual(response.status_code, 200)
