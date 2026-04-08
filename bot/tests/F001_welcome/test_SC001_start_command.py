"""
Test SC001 — Bot replies with welcome message on /start and sets waiting_for_photo.

## Traceability
Feature: F001 — User greeting
Scenario: SC001 — Start command

## BDD
Given: User opens the Telegram bot
When:  User sends /start command
Then:  Bot replies with a welcome message, sets waiting_for_photo state,
       and shows a "Select saved photo" button (photo upload is immediate)
"""
import pytest

from node.welcome.trigger.start_trigger import StartTrigger
from node.welcome.code.start_code import StartCode
from node.welcome.answer.welcome_answer import WelcomeAnswer
from state.generation_states import GenerationStates


@pytest.mark.asyncio
async def test_start_trigger(mock_message, mock_state):
    """
    Given: User sends /start
    When:  Trigger processes the message
    Then:  Returns user data
    """
    trigger = StartTrigger()
    result = await trigger.run(mock_message, mock_state)

    assert result["user_id"] == 123
    assert result["first_name"] == "Test"
    mock_state.clear.assert_called_once()


@pytest.mark.asyncio
async def test_start_code_sets_waiting_for_photo(mock_state):
    """
    Given: Trigger data with user info
    When:  Code processes it
    Then:  Returns welcome answer_name and sets state to waiting_for_photo
    """
    code = StartCode()
    result = await code.run({"first_name": "Test"}, mock_state)

    assert result["answer_name"] == "welcome"
    mock_state.set_state.assert_called_once_with(GenerationStates.waiting_for_photo)


@pytest.mark.asyncio
async def test_welcome_answer_shows_select_button(mock_message):
    """
    Given: Welcome answer
    When:  Answer renders
    Then:  Bot sends welcome message with "Select saved photo" button
           (no "Upload" button — user sends photo directly)
    """
    answer = WelcomeAnswer()
    await answer.run(event=mock_message, user_lang="en", data={})

    mock_message.answer.assert_called_once()
    call_args = mock_message.answer.call_args
    text = call_args[0][0] if call_args[0] else call_args.kwargs.get("text", "")
    assert "Welcome" in text

    keyboard = call_args.kwargs.get("reply_markup") or call_args[1].get("reply_markup")
    buttons = [btn.text for row in keyboard.inline_keyboard for btn in row]
    assert "Select saved photo" in buttons
    assert "Upload new photo" not in buttons
