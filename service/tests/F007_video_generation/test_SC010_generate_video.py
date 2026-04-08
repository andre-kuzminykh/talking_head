"""
Test SC010 — Video is generated with correct parameters.

## Traceability
Feature: F007 — Video generation
Scenario: SC010 — Generate video from photo and audio

## BDD
Given: Photo and audio are available
When:  POST /api/v1/generation/video with photo_url and audio_url
Then:  Video URL is returned
"""
import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_data, expected",
    [
        (
            {
                "photo_url": "https://example.com/photo.jpg",
                "audio_url": "https://example.com/audio.mp3",
            },
            {"status": 200, "has_video_url": True},
        ),
    ],
    ids=["valid_inputs"],
)
async def test_generate_video(client, input_data, expected):
    """
    Given: Photo and audio are available
    When:  Video generation is requested
    Then:  Video URL is returned
    """
    # Given
    mock_result = {"video_url": "https://example.com/video.mp4"}

    with patch(
        "api.v1.endpoints.generation.video.service.generate_video",
        new_callable=AsyncMock,
        return_value=mock_result,
    ):
        # When
        response = await client.post("/api/v1/generation/video", json=input_data)

        # Then
        assert response.status_code == expected["status"]
        data = response.json()
        assert "video_url" in data
        assert len(data["video_url"]) > 0


@pytest.mark.asyncio
async def test_generate_video_missing_photo(client):
    """
    Given: Missing photo_url
    When:  Video generation is requested
    Then:  Validation error returned
    """
    response = await client.post(
        "/api/v1/generation/video",
        json={"photo_url": "", "audio_url": "https://example.com/audio.mp3"},
    )
    assert response.status_code == 422
