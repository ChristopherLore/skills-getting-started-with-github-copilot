import pytest


@pytest.mark.asyncio
async def test_get_activities_returns_expected_activity_list(async_client):
    # Arrange
    expected_activities = {"Chess Club", "Programming Class"}

    # Act
    response = await async_client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert expected_activities.issubset(set(data))


@pytest.mark.asyncio
async def test_signup_creates_new_participant(async_client):
    # Arrange
    email = "newstudent@mergington.edu"
    signup_url = "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"

    # Act
    response = await async_client.post(signup_url)
    activities_response = await async_client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in participants


@pytest.mark.asyncio
async def test_signup_duplicate_email_returns_bad_request(async_client):
    # Arrange
    email = "duplicate@mergington.edu"
    signup_url = f"/activities/Programming%20Class/signup?email={email}"
    await async_client.post(signup_url)

    # Act
    response = await async_client.post(signup_url)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


@pytest.mark.asyncio
async def test_delete_participant_removes_registration(async_client):
    # Arrange
    email = "removeme@mergington.edu"
    signup_url = f"/activities/Gym%20Class/signup?email={email}"
    delete_url = f"/activities/Gym%20Class/participants?email={email}"
    await async_client.post(signup_url)

    # Act
    response = await async_client.delete(delete_url)
    activities_response = await async_client.get("/activities")
    participants = activities_response.json()["Gym Class"]["participants"]

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Gym Class"
    assert email not in participants


@pytest.mark.asyncio
async def test_delete_nonexistent_participant_returns_not_found(async_client):
    # Arrange
    delete_url = "/activities/Chess%20Club/participants?email=doesnotexist@mergington.edu"

    # Act
    response = await async_client.delete(delete_url)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
