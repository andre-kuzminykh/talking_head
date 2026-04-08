"""
Widget: Text input for speech.

## Traceability
Feature: F005 — Speech text input
Scenarios: SC007, SC008
SC007 — valid text → answer: text_accepted → start generation
SC008 — empty text → answer: text_empty
"""
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from node.text.trigger.text_input_trigger import TextInputTrigger
from node.text.code.text_input_code import TextInputCode
from node.text.answer.text_empty_answer import TextEmptyAnswer
from node.text.answer.text_accepted_answer import TextAcceptedAnswer
from node.generation.trigger.generate_trigger import GenerateTrigger
from node.generation.code.generate_code import GenerateCode
from node.generation.answer.video_ready_answer import VideoReadyAnswer
from node.generation.answer.generation_error_answer import GenerationErrorAnswer
from state.generation_states import GenerationStates

text_input_router = Router(name="text_input")

TEXT_ANSWER_REGISTRY = {
    "text_empty": TextEmptyAnswer(),
    "text_accepted": TextAcceptedAnswer(),
}

GENERATION_ANSWER_REGISTRY = {
    "video_ready": VideoReadyAnswer(),
    "generation_error": GenerationErrorAnswer(),
}


@text_input_router.message(GenerationStates.waiting_for_text)
async def handle_text_input(message: Message, state: FSMContext):
    # Phase 1: Text validation
    trigger = TextInputTrigger()
    trigger_data = await trigger.run(message, state)

    code = TextInputCode()
    code_result = await code.run(trigger_data, state)

    answer = TEXT_ANSWER_REGISTRY[code_result["answer_name"]]
    await answer.run(event=message, user_lang="en", data=code_result["data"])

    if code_result["answer_name"] != "text_accepted":
        return

    # Phase 2: Generation pipeline
    gen_trigger = GenerateTrigger()
    gen_trigger_data = await gen_trigger.run(message, state)

    gen_code = GenerateCode()
    gen_result = await gen_code.run(gen_trigger_data, state)

    gen_answer = GENERATION_ANSWER_REGISTRY[gen_result["answer_name"]]
    await gen_answer.run(event=message, user_lang="en", data=gen_result["data"])
