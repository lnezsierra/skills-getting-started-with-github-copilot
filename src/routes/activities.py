from fastapi import APIRouter

from src.services.activities_service import (
    get_activity_participants,
    list_activities,
    signup_for_activity,
)

router = APIRouter()


@router.get("/activities")
def get_activities():
    """Return all activities with metadata and current participants."""
    return list_activities()


@router.get("/activities/{activity_name}/participants")
def get_participants(activity_name: str):
    """Return the registered participant emails for one activity."""
    return get_activity_participants(activity_name)


@router.post("/activities/{activity_name}/signup")
def signup(activity_name: str, email: str):
    """Sign up a student for an activity."""
    return signup_for_activity(activity_name, email)
