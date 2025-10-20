# backend/routers_contact.py
from fastapi import APIRouter, BackgroundTasks, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.core.db import get_db
from backend.models.contact import Contact
from backend.schemas.contacts import ContactCreate, ContactOut
from backend.services.mailer import send_appointment_emails

router = APIRouter(prefix="/contacts")

@router.post("/", response_model=ContactOut, name="Create contact")
def create_contact(payload: ContactCreate, request: Request, background: BackgroundTasks, db: Session = Depends(get_db)):
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
    # ⚡ 关键：后台异步发邮件（不阻塞请求）
    background.add_task(
        send_appointment_emails,
        {
            "id": c.id,
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
        },
    )
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
