"""
Test SC005 — List user's saved photos.

## Traceability
Feature: F004 — Saved photo selection
Scenario: SC005 — User has saved photos

## BDD
Given: User has saved photos in backend
When:  GET /api/v1/photos?user_id=123
Then:  Returns list of photos
"""
import pytest


@pytest.mark.asyncio
async def test_list_user_photos(client):
    """
    Given: User has 2 saved photos
    When:  GET /api/v1/photos?user_id=123
    Then:  Returns list of 2 photos
    """
    # Given
    await client.post("/api/v1/photos", json={"user_id": 123, "file_id": "photo1"})
    await client.post("/api/v1/photos", json={"user_id": 123, "file_id": "photo2"})

    # When
    response = await client.get("/api/v1/photos", params={"user_id": 123})

    # Then
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_list_user_photos_empty(client):
    """
    Given: User has no saved photos
    When:  GET /api/v1/photos?user_id=456
    Then:  Returns empty list
    """
    # When
    response = await client.get("/api/v1/photos", params={"user_id": 456})

    # Then
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0
