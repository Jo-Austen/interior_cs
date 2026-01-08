from __future__ import annotations
from sqlalchemy.orm import Session
from sqlalchemy import select

from backend.models.contact import Contact

def create(db: Session, contact: Contact) -> Contact:
    """
    Persist a Contact ORM entity and return the refreshed entity.
    """
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

def list_recent(db: Session, limit: int = 50) -> list[Contact]:
    """
    Fetch recent contacts.
    """
    stmt = select(Contact).order_by(Contact.submitted_at.desc()).limit(limit)
    return db.execute(stmt).scalars().all()
