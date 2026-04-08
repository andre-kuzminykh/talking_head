"""
Test SC007 — Bot accepts valid text and starts generation.

## Traceability
Feature: F005 — Speech text input
Scenario: SC007 — Valid text input

## BDD
Given: Photo is selected for current generation
When:  User sends a text message
Then:  Bot accepts the text and starts generation pipeline
"""
import pytest

from node.text.trigger.text_input_trigger import TextInputTrigger
from node.text.code.text_input_code import TextInputCode


@pytest.mark.asyncio
async def test_text_input_trigger(mock_message, mock_state):
    """
    Given: User sends text
    When:  Trigger processes it
    Then:  Returns text data
    """
    mock_message.text = "Hello world, this is a test"
    trigger = TextInputTrigger()
    result = await trigger.run(mock_message, mock_state)

    assert result["text"] == "Hello world, this is a test"
    assert result["user_id"] == 123


@pytest.mark.asyncio
async def test_text_input_code_valid(mock_state):
    """
    Given: Valid text provided
    When:  Code processes it
    Then:  Returns text_accepted
    """
    code = TextInputCode()
    result = await code.run({"text": "Hello world"}, mock_state)

    assert result["answer_name"] == "text_accepted"
    assert result["data"]["text"] == "Hello world"


@pytest.mark.asyncio
async def test_text_input_code_empty(mock_state):
    """
    Given: Empty text provided
    When:  Code processes it
    Then:  Returns text_empty
    """
    code = TextInputCode()
    result = await code.run({"text": "   "}, mock_state)

    assert result["answer_name"] == "text_empty"
