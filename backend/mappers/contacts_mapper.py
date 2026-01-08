from __future__ import annotations
from typing import Any

from backend.models.contact import Contact
from backend.schemas.contacts import ContactCreate

def normalize_contact_create(payload: ContactCreate) -> dict[str, Any]:
    """
    Normalize schema input into primitives suitable for ORM.
    NOTE: No DB access here.
    """
    return {
        "name": payload.name.strip(),
        "email": str(payload.email).lower(),
        "phone": payload.phone.strip() if payload.phone else None,

        "contact_type": payload.contact_type,
        "message": payload.message.strip(),

        "preferred_contact": payload.preferred_contact,
        "preferred_time": payload.preferred_time,

        "visit_date": payload.visit_date,
        "visit_time": payload.visit_time,
        "visit_purpose": payload.visit_purpose,

        "consent": payload.consent,
    }

def to_contact_model(payload: ContactCreate, ip: str | None) -> Contact:
    """
    Build ORM instance from schema + request metadata.
    """
    data = normalize_contact_create(payload)
    return Contact(**data, ip_address=ip)

def build_appointment_email_context(c: Contact) -> dict[str, Any]:
    """
    Build email payload dict. Called after DB commit+refresh so submitted_at exists.
    """
    return {
        "id": int(c.id),
        "contact_type": c.contact_type,
        "name": c.name,
        "email": c.email,
        "phone": c.phone,
        "message": c.message,

        "preferred_contact": c.preferred_contact,
        "preferred_time": c.preferred_time,

        "visit_date": c.visit_date.isoformat() if c.visit_date else None,
        "visit_time": c.visit_time,
        "visit_purpose": c.visit_purpose,

        "submitted_at": c.submitted_at.isoformat(),
    }
