import pytest
from httpx import AsyncClient, ASGITransport
from src import app as app_module


@pytest.fixture
async def async_client() -> AsyncClient:
    transport = ASGITransport(app=app_module.app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture(autouse=True)
def reset_activities():
    # Recreate the in-memory activity state before each test to ensure isolation
    app_module.activities.clear()
    app_module.activities.update({
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
    })
