from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from spy_agency.models import SpyCat, Mission, Target


class SpyCatValidationTests(TestCase):
    def setUp(self):
        self.valid_breed = "Persian"
        self.invalid_breed = "UnknownBreed"

    def test_valid_breed(self):
        spy_cat = SpyCat(
            name="Agent Whiskers",
            years_of_experience=3,
            breed=self.valid_breed,
            salary=50000.00
        )
        try:
            spy_cat.full_clean()
            spy_cat.save()
        except ValidationError:
            self.fail(
                "SpyCat with a valid breed "
                "should not raise ValidationError."
            )

    def test_invalid_breed(self):
        spy_cat = SpyCat(
            name="Agent Unknown",
            years_of_experience=2,
            breed=self.invalid_breed,
            salary=40000.00
        )
        with self.assertRaises(ValidationError):
            spy_cat.full_clean()

    def test_breed_validation_on_update(self):
        spy_cat = SpyCat.objects.create(
            name="Agent Paws",
            years_of_experience=5,
            breed=self.valid_breed,
            salary=60000.00
        )
        spy_cat.breed = self.invalid_breed
        with self.assertRaises(ValidationError):
            spy_cat.full_clean()


class MissionActionsTests(APITestCase):
    def setUp(self):
        self.cat = SpyCat.objects.create(
            name="Agent Meow",
            years_of_experience=5,
            breed="Persian",
            salary=5000.00
        )
        self.mission_url = reverse("spy_agency:mission-list")
        self.assign_cat_url = lambda pk: reverse(
            "spy_agency:mission-assign-cat", args=[pk]
        )
        self.update_targets_url = lambda pk: reverse(
            "spy_agency:mission-update-targets", args=[pk]
        )

    def test_create_mission(self):
        data = {
            "cat": None,
            "is_complete": False,
            "targets": [
                {"name": "Target Alpha", "country": "USA", "notes": ""},
                {"name": "Target Beta", "country": "UK", "notes": ""}
            ]
        }
        response = self.client.post(self.mission_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Mission.objects.count(), 1)
        self.assertEqual(Target.objects.count(), 2)

    def test_assign_cat_to_mission(self):
        mission = Mission.objects.create(is_complete=False)
        data = {"cat_id": self.cat.id}
        response = self.client.post(
            self.assign_cat_url(mission.id),
            data=data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mission.refresh_from_db()
        self.assertEqual(mission.cat, self.cat)

    def test_update_targets(self):
        mission = Mission.objects.create(is_complete=False)
        target1 = Target.objects.create(
            name="Target Alpha",
            country="USA",
            mission=mission
        )
        target2 = Target.objects.create(
            name="Target Beta",
            country="UK",
            mission=mission
        )

        data = {
            "targets": [
                {
                    "id": target1.id,
                    "notes": "Observation complete",
                    "is_complete": False
                },
                {
                    "id": target2.id,
                    "notes": "Target neutralized",
                    "is_complete": True
                }
            ]
        }
        response = self.client.patch(
            self.update_targets_url(mission.id),
            data=data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        target1.refresh_from_db()
        target2.refresh_from_db()

        self.assertEqual(target1.notes, "Observation complete")
        self.assertFalse(target1.is_complete)
        self.assertEqual(target2.notes, "Target neutralized")
        self.assertTrue(target2.is_complete)

    def test_cannot_delete_assigned_mission(self):
        mission = Mission.objects.create(is_complete=False, cat=self.cat)
        delete_url = reverse("spy_agency:mission-detail", args=[mission.id])

        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Cannot delete a mission assigned to a cat",
            response.data["detail"]
        )
        self.assertTrue(Mission.objects.filter(id=mission.id).exists())

    def test_delete_unassigned_mission(self):
        mission = Mission.objects.create(is_complete=False)
        delete_url = reverse("spy_agency:mission-detail", args=[mission.id])

        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Mission.objects.filter(id=mission.id).exists())
