"""
Uvicorn entry point for the Talking Head backend service.
"""
import uvicorn

from core.loader import app  # noqa: F401
import api.v1.include_router  # noqa: F401

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
