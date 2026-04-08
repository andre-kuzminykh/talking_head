"""
Test SC011 — Bot sends video to user.

## Traceability
Feature: F008 — Result delivery
Scenario: SC011 — Video sent successfully

## BDD
Given: Video has been successfully generated
When:  Generation pipeline completes
Then:  Bot sends the video to the user
"""
import pytest
from unittest.mock import AsyncMock, patch

from node.generation.code.generate_code import GenerateCode
from node.generation.answer.generation_error_answer import GenerationErrorAnswer


@pytest.mark.asyncio
async def test_generate_code_success(mock_state):
    """
    Given: Valid photo and text in state
    When:  Generation pipeline runs
    Then:  Returns video_ready with video_url
    """
    code = GenerateCode()

    with patch.object(
        code._generation_api,
        "generate_audio",
        new_callable=AsyncMock,
        return_value={"audio_url": "https://example.com/audio.mp3"},
    ), patch.object(
        code._generation_api,
        "generate_video",
        new_callable=AsyncMock,
        return_value={"video_url": "https://example.com/video.mp4"},
    ):
        result = await code.run(
            {"file_id": "photo123", "speech_text": "Hello"},
            mock_state,
        )

    assert result["answer_name"] == "video_ready"
    assert result["data"]["video_url"] == "https://example.com/video.mp4"


@pytest.mark.asyncio
async def test_generate_code_error(mock_state):
    """
    Given: Generation API fails
    When:  Generation pipeline runs
    Then:  Returns generation_error
    """
    code = GenerateCode()

    with patch.object(
        code._generation_api,
        "generate_audio",
        new_callable=AsyncMock,
        side_effect=Exception("TTS service down"),
    ):
        result = await code.run(
            {"file_id": "photo123", "speech_text": "Hello"},
            mock_state,
        )

    assert result["answer_name"] == "generation_error"


@pytest.mark.asyncio
async def test_generation_error_answer(mock_message):
    """
    Given: Generation error
    When:  Error answer renders
    Then:  Bot sends error message
    """
    answer = GenerationErrorAnswer()
    await answer.run(event=mock_message, data={"error": "API timeout"})

    mock_message.answer.assert_called_once()
