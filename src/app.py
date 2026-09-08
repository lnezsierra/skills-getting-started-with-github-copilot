"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

# Configure the API metadata displayed in the generated documentation.
app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Resolve and mount the frontend assets under the /static URL path.
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database. Data resets whenever the server restarts.
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Checkers Club": {
        "description": "Practice checkers tactics and play friendly matches",
        "schedule": "Mondays, 3:30 PM - 4:30 PM",
        "max_participants": 14,
        "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
    },
    "Tabletop Games Club": {
        "description": "Explore strategy board games and cooperative challenges",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["noah@mergington.edu", "ava@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Math Tutoring": {
        "description": "Strengthen algebra, geometry, and problem-solving skills",
        "schedule": "Tuesdays, 4:00 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["liam@mergington.edu", "isabella@mergington.edu"]
    },
    "Science Workshop": {
        "description": "Hands-on experiments in physics, chemistry, and biology",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["ethan@mergington.edu", "amelia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Practice soccer skills and compete in interschool matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Develop basketball fundamentals and play competitive games",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["ethan@mergington.edu", "ava@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore drawing, painting, and mixed-media techniques",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu", "noah@mergington.edu"]
    },
    "Drama Club": {
        "description": "Practice acting, stagecraft, and theatrical performance",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["amelia@mergington.edu", "liam@mergington.edu"]
    },
    "Debate Team": {
        "description": "Build critical thinking and public speaking through structured debates",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["harper@mergington.edu", "james@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Solve scientific challenges and prepare for academic competitions",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["evelyn@mergington.edu", "henry@mergington.edu"]
    },
    "Volleyball Club": {
        "description": "Learn volleyball fundamentals and play weekly scrimmages",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["henry@mergington.edu", "evelyn@mergington.edu"]
    }
}


@app.get("/")
def root():
    """Redirect root path to the static web application."""
    # Send visitors directly to the frontend entry page.
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    """Return all activities with metadata and current participants."""
    # FastAPI serializes the activity dictionary as JSON.
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Reject requests for activities that are not in the database.
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Only school emails are allowed for new registrations.
    normalized_email = email.strip().lower()
    if not normalized_email.endswith("@mergington.edu"):
        raise HTTPException(
            status_code=400,
            detail="Invalid email domain. Must be @mergington.edu",
        )

    # Retrieve the selected activity for the remaining validation checks.
    activity = activities[activity_name]

    # Prevent the same student from registering more than once.
    if normalized_email in activity["participants"]:
        raise HTTPException(
            status_code=409,
            detail="Student is already registered for this activity",
        )

    # Store the registration in the in-memory participant list.
    activity["participants"].append(normalized_email)

    # Return a confirmation message for the frontend notification.
    return {"message": f"Signed up {normalized_email} for {activity_name}"}
