"""
Photos API router.

## Traceability
Feature: F003 — Photo storage
Feature: F004 — Saved photo selection
"""
from fastapi import APIRouter

from api.v1.endpoints.photos.get import router as get_router
from api.v1.endpoints.photos.post import router as post_router
from api.v1.endpoints.photos.delete import router as delete_router

router = APIRouter(prefix="/photos", tags=["photos"])
router.include_router(get_router)
router.include_router(post_router)
router.include_router(delete_router)
