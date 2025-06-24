from django.test import TestCase, Client
from django.urls import reverse
import json
import random
from django.contrib.auth.models import User
from services.models import VehicleCategory, AllowedVehicles, AccessArea

class VehiclesBulkEntryTest(TestCase):
    def setUp(self):
        # Create some VehicleCategory and Zone instances for test DB
        VehicleCategory.objects.create(title="Autoturism")
        VehicleCategory.objects.create(title="Motocicleta")

        AccessArea.objects.create(name="ZONA A")
        AccessArea.objects.create(name="ZONA B")

        self.client = Client()
        # create user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_bulk_entry_save(self):
        category_obj = VehicleCategory.objects.get(title="Autoturism")
        zone_obj = AccessArea.objects.get(name="ZONA A")

        data = AllowedVehicles.objects.create(
            owner="John Doe",
            identification_nr="B-123-XYZ",
            permit_nr="AV123",
            start_date="2025-06-23",
            end_date="2025-06-30",
            description="Note"
        )

        # Now assign the M2M relation
        data.area.set([zone_obj])
        data.categ.set([category_obj])

        # Use client.post with content_type and json.dumps data
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        # Optionally verify the AllowedVehicles entry was created correctly
        av = AllowedVehicles.objects.filter(owner="John Doe").first()
        self.assertIsNotNone(av)
        self.assertEqual(av.categ, category_obj)
        self.assertIn(zone_obj, av.area.all())  # because area is ManyToMany
