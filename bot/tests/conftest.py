"""
Global test fixtures for bot.
"""
from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def mock_message():
    msg = AsyncMock()
    msg.from_user = MagicMock(id=123, username="testuser", first_name="Test")
    msg.text = "Hello"
    msg.photo = None
    msg.answer = AsyncMock()
    msg.answer_video = AsyncMock()
    return msg


@pytest.fixture
def mock_message_with_photo():
    msg = AsyncMock()
    msg.from_user = MagicMock(id=123, username="testuser", first_name="Test")
    msg.text = None
    photo = MagicMock()
    photo.file_id = "AgACAgIAAxk"
    photo.file_unique_id = "unique123"
    msg.photo = [photo]
    msg.answer = AsyncMock()
    return msg


@pytest.fixture
def mock_callback():
    cb = AsyncMock()
    cb.from_user = MagicMock(id=123, username="testuser")
    cb.answer = AsyncMock()
    cb.message = AsyncMock()
    cb.message.edit_text = AsyncMock()
    return cb


@pytest.fixture
def mock_state():
    state = AsyncMock()
    state.get_data = AsyncMock(return_value={})
    state.set_data = AsyncMock()
    state.update_data = AsyncMock()
    state.set_state = AsyncMock()
    state.clear = AsyncMock()
    return state
