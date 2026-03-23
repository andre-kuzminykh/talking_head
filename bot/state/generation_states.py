"""
FSM states for the generation flow.

## Traceability
Feature: F002 — Photo upload
Feature: F004 — Saved photo selection
Feature: F005 — Speech text input
Feature: F006 — Audio generation
Feature: F007 — Video generation
"""
from aiogram.fsm.state import State, StatesGroup


class GenerationStates(StatesGroup):
    waiting_for_photo = State()
    waiting_for_text = State()
    generating = State()
