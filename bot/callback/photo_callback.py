"""
Callback data for photo selection.

## Traceability
Feature: F004 — Saved photo selection
Scenarios: SC005
"""
from aiogram.filters.callback_data import CallbackData


class PhotoCallback(CallbackData, prefix="photo"):
    action: str
    photo_id: int = 0
