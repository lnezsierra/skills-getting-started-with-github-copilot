"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Merg High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Merg High School API",
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
        "participants": ["michael@merghigh.edu", "daniel@merghigh.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@merghigh.edu", "sophia@merghigh.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@merghigh.edu", "olivia@merghigh.edu"]
    },
    "Soccer Team": {
        "description": "Practice soccer skills and compete in interschool matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["lucas@merghigh.edu", "mia@merghigh.edu"]
    },
    "Basketball Team": {
        "description": "Develop basketball fundamentals and play competitive games",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["ethan@merghigh.edu", "ava@merghigh.edu"]
    },
    "Art Club": {
        "description": "Explore drawing, painting, and mixed-media techniques",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["isabella@merghigh.edu", "noah@merghigh.edu"]
    },
    "Drama Club": {
        "description": "Practice acting, stagecraft, and theatrical performance",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["amelia@merghigh.edu", "liam@merghigh.edu"]
    },
    "Debate Team": {
        "description": "Build critical thinking and public speaking through structured debates",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["harper@merghigh.edu", "james@merghigh.edu"]
    },
    "Science Olympiad": {
        "description": "Solve scientific challenges and prepare for academic competitions",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["evelyn@merghigh.edu", "henry@merghigh.edu"]
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

    # Retrieve activity and append the student email.
    activity = activities[activity_name]

    # Validate that the email is @merghigh.edu
    if not email.endswith("@merghigh.edu"):
        raise HTTPException(
            status_code=400,
            detail="Invalid email domain. Must be @merghigh.edu",
        )
    if email in activity["participants"]:
        raise HTTPException(
            status_code=409,
            detail="Student is already registered for this activity",
        )

    activity["participants"].append(email)

    # Return a human-readable confirmation for the frontend.
    return {"message": f"Signed up {email} for {activity_name}"}
