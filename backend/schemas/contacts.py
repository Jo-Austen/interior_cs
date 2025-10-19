# backend/schemas_contact.py
from typing import Optional, Literal
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field, model_validator, field_validator

ContactType = Literal["online", "in_person"]

class ContactCreate(BaseModel):
    # 共通
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    phone: Optional[str] = Field(default=None, max_length=40)

    contact_type: ContactType
    message: str = Field(min_length=1, max_length=5000)

    # 线上
    preferred_contact: Optional[Literal["phone", "email", "video"]] = None
    preferred_time: Optional[Literal["morning", "afternoon", "evening"]] = None

    # 到店
    visit_date: Optional[date] = None
    visit_time: Optional[Literal["morning", "afternoon"]] = None
    visit_purpose: Optional[Literal["product", "project", "support"]] = None

    consent: bool

    # ✅ 新增：前置校验器，把空字符串 "" 视为 None，避免字段层报错
    @field_validator(
        'preferred_contact', 'preferred_time',
        'visit_date', 'visit_time', 'visit_purpose',
        mode='before'
    )
    def empty_str_to_none(cls, v):
        return None if v == '' else v

    @model_validator(mode="after")
    def check_branch_requirements(self):
        if not self.consent:
            raise ValueError("必须勾选同意隐私政策（consent=true）")

        if self.contact_type == "online":
            if not (self.preferred_contact and self.preferred_time):
                raise ValueError("线上咨询需提供 preferred_contact 与 preferred_time")
        elif self.contact_type == "in_person":
            missing = [k for k, val in {
                "visit_date": self.visit_date,
                "visit_time": self.visit_time,
                "visit_purpose": self.visit_purpose
            }.items() if val is None]
            if missing:
                raise ValueError(f"到店咨询缺少必填字段: {', '.join(missing)}")
        return self


class ContactOut(BaseModel):
    id: int
    contact_type: ContactType
    name: str
    email: EmailStr
    phone: Optional[str]
    message: str
    preferred_contact: Optional[str]
    preferred_time: Optional[str]
    visit_date: Optional[date]
    visit_time: Optional[str]
    visit_purpose: Optional[str]
    submitted_at: datetime

    class Config:
        from_attributes = True
