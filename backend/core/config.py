# backend/core/config.py
from __future__ import annotations
import os
from dotenv import load_dotenv

load_dotenv()

def _get_bool(name: str, default: bool = False) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return v.strip().lower() in {"1", "true", "yes", "y", "on"}

def _get_list(name: str, default: str = "") -> list[str]:
    raw = os.getenv(name, default)
    return [x.strip() for x in raw.split(",") if x.strip()]

class Settings:
    def __init__(self) -> None:
        self.SMTP_HOST: str | None = os.getenv("SMTP_HOST")
        self.SMTP_PORT: int = int(os.getenv("SMTP_PORT", "465"))
        self.SMTP_USER: str | None = os.getenv("SMTP_USER")
        self.SMTP_PASS: str | None = os.getenv("SMTP_PASS")
        self.SMTP_TLS: bool = _get_bool("SMTP_TLS", False)
        self.SMTP_SSL: bool = _get_bool("SMTP_SSL", True)

        self.MAIL_FROM: str = os.getenv("MAIL_FROM", "no-reply@example.com")
        self.MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME", "Interior Co.")

        self.COMPANY_NAME: str = os.getenv("COMPANY_NAME", "Interior Co.")
        self.COMPANY_ADDR: str = os.getenv("COMPANY_ADDR", "")
        self.COMPANY_PHONE: str = os.getenv("COMPANY_PHONE", "")
        self.COMPANY_EMAIL: str = os.getenv("COMPANY_EMAIL", "")
        self.COMPANY_SITE: str = os.getenv("COMPANY_SITE", "")

        self.APPOINTMENT_NOTIFY_TO: list[str] = _get_list("APPOINTMENT_NOTIFY_TO", "")

        # CORS
        self.CORS_ALLOW_ORIGINS: list[str] = _get_list(
            "CORS_ALLOW_ORIGINS",
            "http://localhost:3000,http://127.0.0.1:3000",
        )
        self.CORS_ALLOW_CREDENTIALS: bool = _get_bool("CORS_ALLOW_CREDENTIALS", True)

        if self.CORS_ALLOW_CREDENTIALS and "*" in self.CORS_ALLOW_ORIGINS:
            raise ValueError("CORS_ALLOW_ORIGINS cannot contain '*' when CORS_ALLOW_CREDENTIALS is true")

settings = Settings()

