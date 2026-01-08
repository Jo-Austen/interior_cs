from fastapi import APIRouter, BackgroundTasks, Depends, Request
from sqlalchemy.orm import Session

from backend.core.db import get_db
from backend.schemas.contacts import ContactCreate, ContactOut
from backend.services.contacts_service import create_contact, list_contacts_brief

router = APIRouter(prefix="/contacts")

@router.post("/", response_model=ContactOut, name="Create contact")
def create_contact_endpoint(
    payload: ContactCreate,
    request: Request,
    background: BackgroundTasks,
    db: Session = Depends(get_db),
):
    ip = request.client.host if request.client else None
    return create_contact(db=db, payload=payload, ip=ip, background=background)

@router.get("/", name="List contacts (brief)")
def list_contacts_endpoint(db: Session = Depends(get_db)):
    return list_contacts_brief(db=db, limit=50)
