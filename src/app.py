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

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Serve frontend files (HTML/CSS/JS) from /static
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
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


@app.get("/")
def root():
    """Redirect root path to the static web application."""
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    """Return all activities with metadata and current participants."""
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Ensure the requested activity exists.
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Only school emails are allowed for new registrations.
    normalized_email = email.strip().lower()
    if not normalized_email.endswith("@mergington.edu"):
        raise HTTPException(
            status_code=400,
            detail="Email must end with @mergington.edu"
        )

    # Retrieve activity and append the student email.
    activity = activities[activity_name]
    if normalized_email in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is already registered for this activity"
        )

    activity["participants"].append(normalized_email)

    # Return a human-readable confirmation for the frontend.
    return {"message": f"Signed up {normalized_email} for {activity_name}"}
