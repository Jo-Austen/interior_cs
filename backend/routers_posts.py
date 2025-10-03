from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.db import get_db
from backend.models_post import Post

router = APIRouter(prefix="/api/v1/posts", tags=["posts"])

@router.get("/", name="List posts", operation_id="list_posts")
def list_posts(db: Session = Depends(get_db)):
    stmt = (
        select(Post)
        .where(Post.published.is_(True))
        .order_by(Post.published_at.is_(None), Post.published_at.desc())
    )
    rows = db.execute(stmt).scalars().all()
    return [
        {
            "slug": r.slug,
            "title": r.title,
            "summary": r.summary,
            "cover_url": r.cover_url,
            "published_at": r.published_at.isoformat() if r.published_at else None,
        }
        for r in rows
    ]
