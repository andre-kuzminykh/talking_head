"""
Router registration for the FastAPI application.
"""
from core.loader import app
from core.exceptions import AppException
from api.v1.exception_handlers import app_exception_handler
from api.v1.endpoints import photos_router, generation_router

API_V1_PREFIX = "/api/v1"

app.include_router(photos_router, prefix=API_V1_PREFIX)
app.include_router(generation_router, prefix=API_V1_PREFIX)
app.add_exception_handler(AppException, app_exception_handler)
