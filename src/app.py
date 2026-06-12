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

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
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
    "Debate Club": {
        "description": "Develop public speaking and critical thinking skills through competitive debate",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["lucas@mergington.edu"]
    },
    "Robotics Team": {
        "description": "Design and build robots to compete in STEM competitions",
        "schedule": "Mondays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["alex@mergington.edu", "jordan@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball training and intramural games",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["marcus@mergington.edu", "tyler@mergington.edu"]
    },
    "Volleyball Club": {
        "description": "Learn volleyball skills and participate in friendly matches",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["isabella@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore painting, drawing, and sculpture techniques",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 15,
        "participants": ["sarah@mergington.edu", "rachel@mergington.edu"]
    },
    "Drama Club": {
        "description": "Perform in theatrical productions and develop acting skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["david@mergington.edu"]
    },
    "Music Ensemble": {
        "description": "Join our band or orchestra and perform in school concerts",
        "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 22,
        "participants": ["grace@mergington.edu", "benjamin@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Normalize email for consistent deduplication
    email_norm = email.strip().lower()

    # Check if student is already signed up (case-insensitive)
    if any(p.strip().lower() == email_norm for p in activity["participants"]):
        raise HTTPException(status_code=400, detail="Student already signed up")

    # Add student (store normalized email)
    activity["participants"].append(email_norm)
    return {"message": f"Signed up {email_norm} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def remove_participant(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    # Normalize incoming email and find matching participant (case-insensitive)
    email_norm = email.strip().lower()
    match_index = next((i for i, p in enumerate(activity["participants"]) if p.strip().lower() == email_norm), None)

    if match_index is None:
        raise HTTPException(status_code=404, detail="Participant not found")

    removed = activity["participants"].pop(match_index)
    return {"message": f"Removed {removed} from {activity_name}"}
