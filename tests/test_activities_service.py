import pytest
from fastapi import HTTPException

from src.services.activities_service import (
    get_activity,
    get_activity_participants,
    list_activities,
    signup_for_activity,
)


def test_list_activities_includes_known_activity():
    activities = list_activities()

    assert "Chess Club" in activities


def test_get_activity_returns_none_for_unknown_activity():
    assert get_activity("Unknown Club") is None


def test_get_activity_participants_raises_not_found_for_unknown_activity():
    with pytest.raises(HTTPException) as exc_info:
        get_activity_participants("Unknown Club")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Activity not found, sorry"


def test_signup_for_activity_raises_invalid_domain_error():
    with pytest.raises(HTTPException) as exc_info:
        signup_for_activity("Chess Club", "invalid@example.com")

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Email must use the @merginton.edu domain"


def test_signup_for_activity_raises_not_found_for_unknown_activity():
    with pytest.raises(HTTPException) as exc_info:
        signup_for_activity("Unknown Club", "student@merginton.edu")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Activity not found"
