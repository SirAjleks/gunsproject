from django.test import TestCase, Client
from django.urls import reverse
from .models import Rank, Person, Gun, Assignment

class ArsenalSystemTests(TestCase):
    def setUp(self):
        # Create some initial data for tests
        self.rank = Rank.objects.create(name="Lieutenant")
        self.person = Person.objects.create(name="Test Person", rank=self.rank)
        self.gun = Gun.objects.create(name="Test Gun")
        # Client for simulating web requests
        self.client = Client()

    def test_add_gun_view(self):
        # Simulate adding a new gun via POST request
        response = self.client.post(reverse('gun_add'), {'name': 'New Gun'})
        # After adding, it should redirect (status 302) to guns list
        self.assertEqual(response.status_code, 302)
        # The new gun should exist in the database:
        self.assertTrue(Gun.objects.filter(name="New Gun").exists())

    def test_assign_and_return_flow(self):
        # Issue the gun to the person
        response = self.client.post(reverse('assign_gun'), {'person': self.person.id, 'gun': self.gun.id})
        # After assignment, check that gun is marked assigned in DB
        self.gun.refresh_from_db()
        self.assertTrue(self.gun.is_assigned)
        # There should be an Assignment record now
        assignment = Assignment.objects.get(gun=self.gun, person=self.person, date_returned__isnull=True)
        # Now simulate returning the gun
        response = self.client.get(reverse('return_gun', args=[self.gun.id]))
        # Reload from DB and check is_assigned is False and assignment got a return date
        self.gun.refresh_from_db()
        self.assertFalse(self.gun.is_assigned)
        assignment.refresh_from_db()
        self.assertIsNotNone(assignment.date_returned)
