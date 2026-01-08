from __future__ import annotations
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from backend.schemas.contacts import ContactCreate
from backend.models.contact import Contact
from backend.repositories import contacts_repo
from backend.mappers.contacts_mapper import to_contact_model, build_appointment_email_context
from backend.services.mailer import send_appointment_emails

def create_contact(
    *,
    db: Session,
    payload: ContactCreate,
    ip: str | None,
    background: BackgroundTasks,
) -> Contact:
    """
    Orchestrate contact creation:
    1) map schema -> ORM
    2) persist via repository
    3) schedule email notification
    """
    contact = to_contact_model(payload, ip=ip)
    contact = contacts_repo.create(db, contact)

    background.add_task(
        send_appointment_emails,
        build_appointment_email_context(contact),
    )
    return contact

def list_contacts_brief(db: Session, limit: int = 50) -> list[dict]:
    """
    Return a brief list (keeps current API behavior).
    """
    rows = contacts_repo.list_recent(db, limit=limit)
    return [
        {
            "id": int(r.id),
            "contact_type": r.contact_type,
            "name": r.name,
            "email": r.email,
            "submitted_at": r.submitted_at.isoformat(),
        }
        for r in rows
    ]
