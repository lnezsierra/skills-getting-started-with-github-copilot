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
    },
    "Painting Studio": {
        "description": "Learn painting techniques and create artwork",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alice@mergington.edu"]
    },
    "Digital Art": {
        "description": "Create digital illustrations and graphic designs",
        "schedule": "Saturdays, 1:00 PM - 3:00 PM",
        "max_participants": 18,
        "participants": ["james@mergington.edu", "lucy@mergington.edu"]
    },
    "Debate Society": {
        "description": "Develop critical thinking and public speaking skills through debate",
        "schedule": "Thursdays, 5:00 PM - 6:30 PM",
        "max_participants": 25,
        "participants": ["robert@mergington.edu", "claire@mergington.edu"]
    },
    "Math Olympiad": {
        "description": "Prepare for mathematical competitions and solve challenging problems",
        "schedule": "Tuesdays, 6:00 PM - 7:30 PM",
        "max_participants": 16,
        "participants": ["adam@mergington.edu"]
    },
    "Web Development": {
        "description": "Build modern web applications using HTML, CSS, and JavaScript",
        "schedule": "Wednesdays and Fridays, 5:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": ["noah@mergington.edu", "grace@mergington.edu"]
    },
    "Robotics Club": {
        "description": "Design and build robots for competitions",
        "schedule": "Mondays and Thursdays, 6:00 PM - 7:30 PM",
        "max_participants": 14,
        "participants": ["isaac@mergington.edu", "zoe@mergington.edu"]
    }
}


def get_activities():
    """Return all activities from the in-memory store."""
    return activities


def get_activity(activity_name: str):
    """Return one activity by name, or None if it doesn't exist."""
    return activities.get(activity_name)


def add_participant(activity_name: str, normalized_email: str):
    """Add a participant email to an activity."""
    activities[activity_name]["participants"].append(normalized_email)
