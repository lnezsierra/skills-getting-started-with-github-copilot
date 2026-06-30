from fastapi import HTTPException

from src.config import REQUIRED_EMAIL_DOMAIN
from src.data.activities_store import add_participant, get_activities


def list_activities():
    """Return all activities with metadata and current participants."""
    # Retrieve and return all activities from the data store
    return get_activities()


def get_activity(activity_name: str):
    """Return a single activity by name, or None if not found."""
    # Fetch all activities and retrieve the specific one
    activities = get_activities()
    return activities.get(activity_name)


def get_activity_participants(activity_name: str):
    """Return the registered participant emails for one activity."""
    # Get the activity details
    activity = get_activity(activity_name)
    # Return 404 if activity does not exist
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found, sorry")

    # Return activity name and list of participants
    return {
        "activity": activity_name,
        "participants": activity["participants"]
    }


def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity."""
    # Normalize email by stripping whitespace and converting to lowercase
    normalized_email = email.strip().lower()

    # Validate that email uses the required domain
    if not normalized_email.endswith(REQUIRED_EMAIL_DOMAIN):
        raise HTTPException(
            status_code=400,
            detail=f"Email must use the {REQUIRED_EMAIL_DOMAIN} domain"
        )

    # Fetch the activity to verify it exists
    activity = get_activity(activity_name)
    # Return 404 if activity does not exist
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Check if student is already signed up
    if normalized_email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Add the participant to the activity
    add_participant(activity_name, normalized_email)
    # Return success message
    return {"message": f"Signed up {normalized_email} for {activity_name}"}
