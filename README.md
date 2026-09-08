# Extracurricular Activities System (FastAPI)

A simple web application for managing extracurricular activities at Mergington High School. It includes a FastAPI backend, a static HTML/CSS/JavaScript frontend, and an API for viewing activities and registering students.

## Features

- View each activity's description, schedule, enrollment, and remaining capacity.
- Register for an activity directly from its activity card.
- Accept only student email addresses in the `@mergington.edu` domain.
- Prevent a student from registering for the same activity more than once.
- Disable registration buttons in the web interface when an activity is full.

Activity and registration data is stored in memory in [src/app.py](src/app.py). All changes are reset when the server restarts.

## Project Structure

```text
.
├── README.md
├── requirements.txt
└── src
    ├── app.py
    └── static
        ├── app.js
        ├── index.html
        └── styles.css
```

Key files:

- [src/app.py](src/app.py): FastAPI application, API endpoints, validation, and initial activity data.
- [src/static/index.html](src/static/index.html): web interface markup.
- [src/static/app.js](src/static/app.js): client-side activity rendering and registration logic.
- [src/static/styles.css](src/static/styles.css): interface styles.

## Requirements

- Python 3.10 or later
- pip

Project dependencies are listed in [requirements.txt](requirements.txt):

- `fastapi`
- `uvicorn`

## Installation

1. Clone the repository.
2. Optionally, create and activate a virtual environment.
3. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run Locally

From the project root, run:

```bash
uvicorn src.app:app --reload
```

Then open:

- Web application: http://127.0.0.1:8000/
- Swagger API documentation: http://127.0.0.1:8000/docs

The root URL redirects to the static application at `/static/index.html`.

## API Usage

### List Activities

`GET /activities`

Returns all activities, including their descriptions, schedules, capacities, and current participants.

Example:

```bash
curl http://127.0.0.1:8000/activities
```

### Register for an Activity

`POST /activities/{activity_name}/signup?email=correo@dominio.com`

The email must end in `@mergington.edu`. The endpoint returns an error if the activity does not exist or the student is already registered for it.

Example:

```bash
curl -X POST "http://127.0.0.1:8000/activities/Chess%20Club/signup?email=ana@mergington.edu"
```

Example success response:

```json
{
    "message": "Signed up ana@mergington.edu for Chess Club"
}
```

## Application Flow

1. The browser opens [src/static/index.html](src/static/index.html).
2. [src/static/app.js](src/static/app.js) requests the current activity data from `GET /activities`.
3. The page renders an activity card with capacity information and a registration button for each activity.
4. The student enters an email address and selects an activity's **Join activity** button.
5. The frontend sends a request to `POST /activities/{activity_name}/signup` and displays the result.
6. After a successful registration, the frontend reloads the activities to update their enrollment and availability.

## Current Limitations

- There is no database, so registrations are not persistent.
- There is no authentication or authorization.
- The frontend prevents registration when an activity is full, but the API does not enforce `max_participants` for direct requests.

## Possible Improvements

- Add persistence with SQLite or PostgreSQL.
- Enforce activity capacity in the API.
- Add authentication for administrators and students.
- Add automated endpoint and frontend tests.

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE) for details.

