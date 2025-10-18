# backend/models_contact.py
from typing import Optional
from datetime import date, datetime
from sqlalchemy import (
    BigInteger, String, Text, Date, DateTime, Boolean, CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from backend.db import Base

class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(40))

    contact_type: Mapped[str] = mapped_column(String(16), nullable=False)  # 'online' | 'in_person'
    message: Mapped[str] = mapped_column(Text, nullable=False)

    preferred_contact: Mapped[Optional[str]] = mapped_column(String(16))
    preferred_time: Mapped[Optional[str]] = mapped_column(String(16))

    # ✅ 注解使用 Python 的 date 类型；列定义仍用 SQLAlchemy 的 Date
    visit_date: Mapped[Optional[date]] = mapped_column(Date)
    visit_time: Mapped[Optional[str]] = mapped_column(String(16))
    visit_purpose: Mapped[Optional[str]] = mapped_column(String(32))

    consent: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    ip_address: Mapped[Optional[str]] = mapped_column(String(45))

    # ✅ 注解使用 Python 的 datetime；列定义仍用 DateTime
    submitted_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("contact_type in ('online','in_person')", name="ck_contact_type"),
        CheckConstraint("(preferred_contact is null) or (preferred_contact in ('phone','email','video'))", name="ck_pref_contact"),
        CheckConstraint("(preferred_time is null) or (preferred_time in ('morning','afternoon','evening'))", name="ck_pref_time"),
        CheckConstraint("(visit_time is null) or (visit_time in ('morning','afternoon'))", name="ck_visit_time"),
        CheckConstraint("(visit_purpose is null) or (visit_purpose in ('product','project','support'))", name="ck_visit_purpose"),
    )
