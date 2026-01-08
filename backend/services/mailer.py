from __future__ import annotations
import smtplib
import logging
from email.message import EmailMessage
from typing import Mapping
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from backend.core.config import settings

logger = logging.getLogger(__name__)

_tpl_env = Environment(
    loader=FileSystemLoader(str(Path(__file__).resolve().parents[1] / "templates" / "email")),
    autoescape=select_autoescape(["html", "xml"])
)

def _render(tpl_name: str, **ctx) -> str:
    return _tpl_env.get_template(tpl_name).render(**ctx)

def _send(msg: EmailMessage) -> None:
    host, port = settings.SMTP_HOST, settings.SMTP_PORT
    if not host:
        logger.warning("SMTP_HOST not configured; skip sending email.")
        return

    if settings.SMTP_SSL:
        with smtplib.SMTP_SSL(host, port) as s:
            if settings.SMTP_USER:
                s.login(settings.SMTP_USER, settings.SMTP_PASS or "")
            s.send_message(msg)
    else:
        with smtplib.SMTP(host, port) as s:
            if settings.SMTP_TLS:
                s.starttls()
            if settings.SMTP_USER:
                s.login(settings.SMTP_USER, settings.SMTP_PASS or "")
            s.send_message(msg)

def _base_msg(to_addrs: list[str], subject: str) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = f"{settings.MAIL_FROM_NAME} <{settings.MAIL_FROM}>"
    msg["To"] = ", ".join(to_addrs)
    msg["Subject"] = subject
    return msg

def send_appointment_emails(contact: Mapping[str, object]) -> None:
    try:
        # 1) 发给公司（internal）
        if settings.APPOINTMENT_NOTIFY_TO:
            html = _render("appointment_internal.html", contact=contact, company=settings)
            msg = _base_msg(settings.APPOINTMENT_NOTIFY_TO, subject="【预约通知】新的预约提交")
            msg.set_content("Your email client does not support HTML.")
            msg.add_alternative(html, subtype="html")
            _send(msg)

        # 2) 发给预约方（customer）
        email = (contact.get("email") or "").strip() if isinstance(contact.get("email"), str) else None
        if email:
            html = _render("appointment_customer.html", contact=contact, company=settings)
            msg = _base_msg([email], subject="预约已收到（Interior Co.）")
            msg.set_content("Your email client does not support HTML.")
            msg.add_alternative(html, subtype="html")
            _send(msg)

    except Exception:
        logger.exception(
            "send_appointment_emails failed: id=%s email=%s",
            contact.get("id"),
            contact.get("email"),
        )
