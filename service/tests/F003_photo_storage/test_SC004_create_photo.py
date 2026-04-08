"""
Test SC004 — Photo is stored in the database linked to the user.

## Traceability
Feature: F003 — Photo storage
Scenario: SC004 — Create photo

## BDD
Given: Empty database
When:  POST /api/v1/photos with user_id and file_id
Then:  Photo record created with correct user_id
"""
import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_data, expected",
    [
        (
            {"user_id": 123, "file_id": "AgACAgIAAxk", "file_path": "/photos/123/photo1.jpg"},
            {"status": 201, "user_id": 123},
        ),
        (
            {"user_id": 456, "file_id": "BgBCBgIBByL"},
            {"status": 201, "user_id": 456},
        ),
    ],
    ids=["with_file_path", "without_file_path"],
)
async def test_create_photo(client, input_data, expected):
    """
    Given: Empty database
    When:  POST /api/v1/photos with user_id and file_id
    Then:  Photo record created with correct user_id, status 201
    """
    # When
    response = await client.post("/api/v1/photos", json=input_data)

    # Then
    assert response.status_code == expected["status"]
    data = response.json()
    assert data["user_id"] == expected["user_id"]
    assert data["file_id"] == input_data["file_id"]
    assert "id" in data
    assert "created_at" in data
