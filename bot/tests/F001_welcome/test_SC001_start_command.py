"""
Test SC001 — Bot replies with welcome message on /start.

## Traceability
Feature: F001 — User greeting
Scenario: SC001 — Start command

## BDD
Given: User opens the Telegram bot
When:  User sends /start command
Then:  Bot replies with a welcome message and action buttons
"""
import pytest

from node.welcome.trigger.start_trigger import StartTrigger
from node.welcome.code.start_code import StartCode
from node.welcome.answer.welcome_answer import WelcomeAnswer


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
async def test_start_code(mock_state):
    """
    Given: Trigger data with user info
    When:  Code processes it
    Then:  Returns welcome answer_name
    """
    code = StartCode()
    result = await code.run({"first_name": "Test"}, mock_state)

    assert result["answer_name"] == "welcome"


@pytest.mark.asyncio
async def test_welcome_answer(mock_message):
    """
    Given: Welcome answer
    When:  Answer renders
    Then:  Bot sends welcome message with keyboard
    """
    answer = WelcomeAnswer()
    await answer.run(event=mock_message, user_lang="en", data={})

    mock_message.answer.assert_called_once()
    call_args = mock_message.answer.call_args
    assert "Welcome" in call_args[0][0] or "Welcome" in call_args.kwargs.get("text", call_args[0][0])
