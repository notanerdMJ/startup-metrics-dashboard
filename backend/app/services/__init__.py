# backend/app/services/__init__.py
"""
Services registry.
"""

from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    get_user_by_email,
    get_user_by_id,
    create_user,
)
from app.services.metrics_engine import MetricsEngine