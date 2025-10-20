# backend/core/config.py
from __future__ import annotations
import os
from dotenv import load_dotenv

load_dotenv()

def _get_bool(name: str, default: bool = False) -> bool:
    v = os.getenv(name)
    if v is None: 
        return default
    return v.strip().lower() in {"1","true","yes","y","on"}

class Settings:
    SMTP_HOST: str | None = os.getenv("SMTP_HOST")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "465"))
    SMTP_USER: str | None = os.getenv("SMTP_USER")
    SMTP_PASS: str | None = os.getenv("SMTP_PASS")
    SMTP_TLS: bool = _get_bool("SMTP_TLS", False)
    SMTP_SSL: bool = _get_bool("SMTP_SSL", True)

    MAIL_FROM: str = os.getenv("MAIL_FROM", "no-reply@example.com")
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME", "Interior Co.")

    COMPANY_NAME: str = os.getenv("COMPANY_NAME", "Interior Co.")
    COMPANY_ADDR: str = os.getenv("COMPANY_ADDR", "")
    COMPANY_PHONE: str = os.getenv("COMPANY_PHONE", "")
    COMPANY_EMAIL: str = os.getenv("COMPANY_EMAIL", "")
    COMPANY_SITE: str = os.getenv("COMPANY_SITE", "")

    APPOINTMENT_NOTIFY_TO: list[str] = [
        e.strip() for e in os.getenv("APPOINTMENT_NOTIFY_TO", "").split(",") if e.strip()
    ]

settings = Settings()
