"""
Test SC009 — Audio file is generated with Andre AIT eng voice.

## Traceability
Feature: F006 — Audio generation
Scenario: SC009 — Generate audio from text

## BDD
Given: Valid text is provided
When:  POST /api/v1/generation/audio with text
Then:  Audio URL is returned
"""
import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_data, expected",
    [
        (
            {"text": "Hello world"},
            {"status": 200, "has_audio_url": True},
        ),
    ],
    ids=["valid_text"],
)
async def test_generate_audio(client, input_data, expected):
    """
    Given: Valid text is provided
    When:  Audio generation is requested
    Then:  Audio URL is returned
    """
    # Given
    mock_result = {"audio_url": "https://example.com/audio.mp3"}

    with patch(
        "api.v1.endpoints.generation.audio.service.generate_audio",
        new_callable=AsyncMock,
        return_value=mock_result,
    ):
        # When
        response = await client.post("/api/v1/generation/audio", json=input_data)

        # Then
        assert response.status_code == expected["status"]
        data = response.json()
        assert "audio_url" in data
        assert len(data["audio_url"]) > 0


@pytest.mark.asyncio
async def test_generate_audio_empty_text(client):
    """
    Given: Empty text
    When:  Audio generation is requested
    Then:  Validation error returned
    """
    response = await client.post("/api/v1/generation/audio", json={"text": ""})
    assert response.status_code == 422
