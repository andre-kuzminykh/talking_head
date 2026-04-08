"""
Test SC002 — Bot accepts photo and confirms upload.

## Traceability
Feature: F002 — Photo upload
Scenario: SC002 — Photo uploaded successfully

## BDD
Given: Bot is awaiting photo upload
When:  User sends a photo
Then:  Bot accepts the photo and confirms upload
"""
import pytest
from unittest.mock import AsyncMock, patch

from node.photo.trigger.upload_trigger import UploadTrigger
from node.photo.code.upload_code import UploadCode


@pytest.mark.asyncio
async def test_upload_trigger_with_photo(mock_message_with_photo, mock_state):
    """
    Given: User sends a photo message
    When:  Trigger processes it
    Then:  Returns photo data with has_photo=True
    """
    trigger = UploadTrigger()
    result = await trigger.run(mock_message_with_photo, mock_state)

    assert result["has_photo"] is True
    assert result["file_id"] == "AgACAgIAAxk"
    assert result["user_id"] == 123


@pytest.mark.asyncio
async def test_upload_trigger_without_photo(mock_message, mock_state):
    """
    Given: User sends a text message
    When:  Trigger processes it
    Then:  Returns has_photo=False
    """
    trigger = UploadTrigger()
    result = await trigger.run(mock_message, mock_state)

    assert result["has_photo"] is False


@pytest.mark.asyncio
async def test_upload_code_with_photo(mock_state):
    """
    Given: Trigger returned photo data
    When:  Code processes it
    Then:  Calls API and returns photo_saved
    """
    code = UploadCode()

    with patch.object(
        code._photos_api,
        "create_photo",
        new_callable=AsyncMock,
        return_value={"id": 1, "file_id": "AgACAgIAAxk"},
    ):
        result = await code.run(
            {"has_photo": True, "user_id": 123, "file_id": "AgACAgIAAxk"},
            mock_state,
        )

    assert result["answer_name"] == "photo_saved"


@pytest.mark.asyncio
async def test_upload_code_without_photo(mock_state):
    """
    Given: Trigger returned no photo
    When:  Code processes it
    Then:  Returns no_photo_error
    """
    code = UploadCode()
    result = await code.run({"has_photo": False}, mock_state)

    assert result["answer_name"] == "no_photo_error"
