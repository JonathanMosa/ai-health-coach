import pytest
from django.core.exceptions import ValidationError
from core.models import CheckIn
from django.contrib.auth import get_user_model
from datetime import date
from django.utils import timezone
from core.serializers import CheckInSerializer
from types import SimpleNamespace
from rest_framework.test import APIClient
from django.urls import reverse

# Does not hit real data in DB
pytestmark = pytest.mark.django_db

def test_soreness_level_rejects_out_of_range():
    """Rejects a sorenesss_level above the valid 1-5 range"""
    User = get_user_model()
    user = User.objects.create_user(username = "testuser", password = "testpass123")
    checkin = CheckIn(soreness_level=8, sleep_hours=1, energy_level=5, notes="good", date=date(2026, 8, 1), user=user)
    with pytest.raises(ValidationError):
        checkin.full_clean()


def test_energy_level_rejects_out_of_range():
    """Rejects a energy_level above the valid 1-5 range"""
    User = get_user_model()
    user = User.objects.create_user(username = "testuser", password = "testpass123")
    checkin = CheckIn(soreness_level=5, sleep_hours=1, energy_level=0, notes="good", date=date(2026, 8, 1), user=user)
    with pytest.raises(ValidationError):
        checkin.full_clean()

def test_rejects_a_second_checkin_same_day():
    """Rejects two checkins in the same day"""
    User = get_user_model()
    user = User.objects.create_user(username = "testuser", password = "testpass123")
    checkin = CheckIn(soreness_level=5, sleep_hours=1, energy_level=2, notes="good", date=date(2026, 8, 1), user=user)
    checkin.save()
    checkin2 = CheckIn(soreness_level=5, sleep_hours=1, energy_level=2, notes="good", date=date(2026, 8, 1), user=user)
    with pytest.raises(ValidationError):
        checkin2.full_clean()

def test_user_rejects_spoof():
    """Rejects one user from entering another user's checkin data from requests"""
    User = get_user_model()
    user = User.objects.create_user(username = "testuser", password = "testpass123")
    user2 = User.objects.create_user(username = "testuser1", password = "testpass123")
    s = CheckInSerializer(data={"soreness_level":"5", "sleep_hours":"1", "energy_level":"2", "notes":"good", "date":"2026-08-14", "user": user2.id}, context={"request": SimpleNamespace(user=user)})
    s.is_valid()
    assert s.is_valid(), s.errors
    assert s.validated_data["user"] == user

def test_endpoint_auth_user():
    """Authorized user succeeds"""
    client = APIClient()
    User = get_user_model()
    user = User.objects.create_user(username = "testuser", password = "testpass123")
    client.force_authenticate(user=user)
    url = reverse("checkin-list")
    response = client.post(url, data={"soreness_level":"5", "sleep_hours":"1", "energy_level":"2", "notes":"good"})

    assert response.status_code == 201

def test_rejects_endpoint_unauth_user():
    """Rejects unauthorized user"""
    client = APIClient()
    url = reverse("checkin-list")
    response = client.post(url, data={"soreness_level":"5", "sleep_hours":"1", "energy_level":"2", "notes":"good", "user":"testuser", "date":"2026-06-20"})

    assert response.status_code == 401

def test_rejects_invalid_payload():
    """Rejects invalid payload"""
    client = APIClient()
    User = get_user_model()
    user = User.objects.create_user(username = "testuser", password = "testpass123")
    client.force_authenticate(user=user)
    url = reverse("checkin-list")
    response = client.post(url, data={"soreness_level":"10", "sleep_hours":"1", "energy_level":"2", "notes":"good"})

    assert response.status_code == 400

def test_rejects_user_from_tickering_user2_checkin():
    """Rejects user from list/retrieve/update/delete user2's checkin"""
    client = APIClient()
    User = get_user_model()
    user = User.objects.create_user(username = "testuser", password = "testpass123")
    user2 = User.objects.create_user(username = "testuser1", password = "testpass123")
    client.force_authenticate(user=user)
    checkin = CheckIn.objects.create(user=user2, date=date(2026, 8, 1), sleep_hours=5, soreness_level=3, energy_level=3)

    list_response = client.get(reverse("checkin-list"))
    assert list_response.data == []

    url = reverse("checkin-detail", args=[checkin.id])
    response = client.get(url)
    patch_response = client.patch(url, data={"user":"user2", "date":"2026-08-01", "sleep_hours":"5", "soreness_level": "3", "energy_level": "3"})
    delete_response = client.delete(url)

    assert response.status_code == 404
    assert patch_response.status_code == 404
    assert delete_response.status_code == 404

def test_rejects_duplicate_checkins():
    """Rejects duplicate checkins from same user in one day"""
    client = APIClient()
    User = get_user_model()
    user = User.objects.create_user(username = "testuser", password = "testpass123")
    client.force_authenticate(user=user)
    checkin = CheckIn.objects.create(user=user, date=timezone.localdate(), sleep_hours=5, soreness_level=3, energy_level=3)

    response = client.post(reverse("checkin-list"), data={"soreness_level": "3", "sleep_hours": "5", "energy_level": "3"})

    assert response.status_code == 400
    assert "non_field_errors" in response.data