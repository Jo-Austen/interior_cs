# backend/routers_contact.py
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.core.db import get_db
from backend.models.contact import Contact
from backend.schemas.contacts import ContactCreate, ContactOut

router = APIRouter(prefix="/contacts")

@router.post("/", response_model=ContactOut, name="Create contact")
def create_contact(payload: ContactCreate, request: Request, db: Session = Depends(get_db)):
    # 轻度去重/限流（示例：同邮箱一分钟内重复提交可拦截，生产可接入更完善的限流）
    # 这里先省略限流实现，专注核心功能

    ip = request.client.host if request.client else None

    c = Contact(
        name=payload.name.strip(),
        email=str(payload.email).lower(),
        phone=payload.phone.strip() if payload.phone else None,
        contact_type=payload.contact_type,
        message=payload.message.strip(),

        preferred_contact=payload.preferred_contact,
        preferred_time=payload.preferred_time,

        visit_date=payload.visit_date,
        visit_time=payload.visit_time,
        visit_purpose=payload.visit_purpose,

        consent=payload.consent,
        ip_address=ip
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.get("/", name="List contacts (brief)")
def list_contacts(db: Session = Depends(get_db)):
    stmt = select(Contact).order_by(Contact.submitted_at.desc()).limit(50)
    rows = db.execute(stmt).scalars().all()
    return [
        {
            "id": r.id,
            "contact_type": r.contact_type,
            "name": r.name,
            "email": r.email,
            "submitted_at": r.submitted_at.isoformat()
        } for r in rows
    ]
