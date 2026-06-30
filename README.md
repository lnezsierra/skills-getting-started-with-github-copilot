# Mergington High School Activities

This project is a small FastAPI app with a static frontend for browsing extracurricular activities and signing up students by email.

The app serves two pieces:

- a JSON API for listing activities and registering participants
- a browser UI in `src/static/` that consumes the API

## Features

- View a catalog of school activities with descriptions, schedules, and remaining spots
- Select an activity and see the registered students
- Sign up with a school email address
- Store activity data in memory for the current server session

## Requirements

- Python 3.10 or newer
- `pip`

## Setup

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run the app

Start the FastAPI app with Uvicorn:

```bash
uvicorn src.main:app --reload --port 8000
```

Open `http://127.0.0.1:8000` in your browser.

## API

The backend exposes these routes:

- `GET /activities` - list all activities and their current participants
- `GET /activities/{activity_name}/participants` - get the registered participants for one activity
- `POST /activities/{activity_name}/signup?email=user@merginton.edu` - sign up a student for an activity

The application expects emails to end with `@merginton.edu`.

## Project structure

- `src/main.py` - FastAPI application setup and root route
- `src/routes/` - API route definitions
- `src/services/` - business logic and validation
- `src/data/` - in-memory activity store
- `src/static/` - frontend HTML, CSS, and JavaScript

## Notes

- Activity data is stored in memory, so it resets when the server restarts.
- The root path redirects to the static UI at `/static/index.html`.