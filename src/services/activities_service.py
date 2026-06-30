from fastapi import HTTPException

from src.config import REQUIRED_EMAIL_DOMAIN
from src.data.activities_store import add_participant, get_activities, get_activity


def list_activities():
    """Return all activities with metadata and current participants."""
    return get_activities()


def get_activity_participants(activity_name: str):
    """Return the registered participant emails for one activity."""
    activity = get_activity(activity_name)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found, sorry")

    return {
        "activity": activity_name,
        "participants": activity["participants"]
    }


def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity."""
    normalized_email = email.strip().lower()

    if not normalized_email.endswith(REQUIRED_EMAIL_DOMAIN):
        raise HTTPException(
            status_code=400,
            detail=f"Email must use the {REQUIRED_EMAIL_DOMAIN} domain"
        )

    activity = get_activity(activity_name)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    if normalized_email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    add_participant(activity_name, normalized_email)
    return {"message": f"Signed up {normalized_email} for {activity_name}"}
