"""
Widget: Start / Welcome.

## Traceability
Feature: F001 — User greeting
Scenarios: SC001
SC001 — /start → answer: welcome
"""
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from node.welcome.trigger.start_trigger import StartTrigger
from node.welcome.code.start_code import StartCode
from node.welcome.answer.welcome_answer import WelcomeAnswer

welcome_router = Router(name="welcome")

ANSWER_REGISTRY = {
    "welcome": WelcomeAnswer(),
}


@welcome_router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext):
    trigger = StartTrigger()
    trigger_data = await trigger.run(message, state)

    code = StartCode()
    code_result = await code.run(trigger_data, state)

    answer = ANSWER_REGISTRY[code_result["answer_name"]]
    await answer.run(event=message, user_lang="en", data=code_result["data"])
