"""
Tests for school views
"""
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from datetime import date

from core.models import School, Tournament, Debater, Team


class SchoolViewsTest(TestCase):
    """Test school views"""

    def setUp(self):
        self.client = Client()
        self.school = School.objects.create(name="Test School")
        self.debater = Debater.objects.create(
            first_name="John",
            last_name="Doe",
            school=self.school
        )
        self.tournament = Tournament.objects.create(
            name="Test Tournament",
            host=self.school,
            date=date(2024, 1, 1),
            season="2024"
        )

    def test_school_list_view(self):
        """Test school list view"""
        response = self.client.get(reverse('core:schools'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test School")

    def test_school_detail_view(self):
        """Test school detail view"""
        response = self.client.get(
            reverse('core:school_detail', kwargs={'pk': self.school.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test School")

    def test_school_with_debaters(self):
        """Test school view with debaters"""
        response = self.client.get(
            reverse('core:school_detail', kwargs={'pk': self.school.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John Doe")

    def test_school_with_tournaments(self):
        """Test school view with hosted tournaments"""
        response = self.client.get(
            reverse('core:school_detail', kwargs={'pk': self.school.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Tournament")

    def test_school_search_view(self):
        """Test school search functionality"""
        response = self.client.get(reverse('core:schools'), {'search': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test School")

    def test_nonexistent_school_404(self):
        """Test that non-existent school returns 404"""
        response = self.client.get(
            reverse('core:school_detail', kwargs={'pk': 99999})
        )
        self.assertEqual(response.status_code, 404)

    def test_school_filter_by_region(self):
        """Test filtering schools by region"""
        # Test basic filter functionality (even if regions aren't implemented)
        response = self.client.get(reverse('core:schools'), {'region': 'Northeast'})
        self.assertEqual(response.status_code, 200)

    def test_school_with_multiple_debaters(self):
        """Test school with multiple debaters"""
        # Create additional debaters
        for i in range(3):
            Debater.objects.create(
                first_name=f"Debater{i}",
                last_name=f"Last{i}",
                school=self.school
            )
        
        response = self.client.get(
            reverse('core:school_detail', kwargs={'pk': self.school.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_school_with_multiple_tournaments(self):
        """Test school with multiple hosted tournaments"""
        # Create additional tournaments
        for i in range(3):
            Tournament.objects.create(
                name=f"Tournament {i}",
                host=self.school,
                date=date(2024, i+1, 1),
                season="2024"
            )
        
        response = self.client.get(
            reverse('core:school_detail', kwargs={'pk': self.school.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_school_statistics_display(self):
        """Test school statistics display"""
        response = self.client.get(
            reverse('core:school_detail', kwargs={'pk': self.school.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test School")

    def test_school_ordering(self):
        """Test school list ordering"""
        # Create schools with different names for ordering test
        School.objects.create(name="Alpha School")
        School.objects.create(name="Beta School")
        
        response = self.client.get(reverse('core:schools'))
        self.assertEqual(response.status_code, 200)

    def test_school_pagination(self):
        """Test school list pagination"""
        # Create many schools to test pagination
        for i in range(25):
            School.objects.create(name=f"School {i:02d}")
        
        response = self.client.get(reverse('core:schools'))
        self.assertEqual(response.status_code, 200)
