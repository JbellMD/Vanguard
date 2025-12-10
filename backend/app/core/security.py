from __future__ import annotations

from typing import Optional

from fastapi import Depends, Header, HTTPException, status

from .config import get_settings


async def verify_api_key(x_api_key: Optional[str] = Header(default=None, alias="x-api-key")) -> None:
    """Simple API key verification using the x-api-key header.

    - If settings.api_key is None, auth is disabled (useful for local dev).
    - If settings.api_key is set, the header must be present and match.
    """
    settings = get_settings()
    if settings.api_key is None:
        # Auth disabled; do nothing.
        return

    if not x_api_key or x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
        )


async def get_project_id(x_project_id: Optional[str] = Header(default=None, alias="X-Project-Id")) -> Optional[str]:
    """Extract optional project identifier from X-Project-Id header.

    This is currently not persisted; handlers can accept it as a dependency
    to scope behavior or logging. Later we can map this to a Project/Tenant
    model in the database.
    """
    return x_project_id
