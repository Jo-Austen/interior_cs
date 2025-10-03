import datetime
from typing import Optional
from sqlalchemy import BigInteger, String, Text, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from backend.db import Base

class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(160), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(String(300))
    body: Mapped[str] = mapped_column(Text, nullable=False)
    cover_url: Mapped[Optional[str]] = mapped_column(String(500))
    published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    published_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime) # type: ignore
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
