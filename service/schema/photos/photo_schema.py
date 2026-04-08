"""
Pydantic schemas for photo operations.

## Traceability
Feature: F003 — Photo storage
Scenarios: SC004, SC005
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PhotoCreateSchema(BaseModel):
    user_id: int
    file_id: str = Field(..., min_length=1, max_length=255)
    file_path: Optional[str] = Field(None, max_length=1024)


class PhotoResponseSchema(BaseModel):
    id: int
    user_id: int
    file_id: str
    file_path: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
