# backend/scripts/seed_posts.py
from __future__ import annotations

from datetime import datetime
from typing import Iterable

from sqlalchemy.orm import Session
from sqlalchemy import select

from backend.core.db import SessionLocal, Base, engine
from backend.models.post import Post


def _seed_data() -> Iterable[dict]:
    """返回种子文章数据（可按需修改/扩展）"""
    now = datetime.utcnow()
    return [
        {
            "slug": "welcome",
            "title": "Welcome to Interior Co.",
            "body": "This is the first post. 🎉",
            "cover_url": None,
            "published_at": now,
        },
        {
            "slug": "about-team",
            "title": "About Our Team",
            "body": "We design, we build, we care.",
            "cover_url": None,
            "published_at": now,
        },
    ]


def upsert_posts(db: Session) -> int:
    """
    幂等写入：按 slug 判断是否已存在，存在则跳过，不存在则插入
    返回新增数量
    """
    added = 0
    for data in _seed_data():
        slug = data["slug"]
        exists = db.execute(select(Post).where(Post.slug == slug)).scalar_one_or_none()
        if exists:
            # 已存在则跳过（保持幂等）
            continue
        row = Post(**data)
        db.add(row)
        added += 1
    if added:
        db.commit()
    return added


def main() -> None:
    """脚本入口：确保表存在 → 写入种子数据"""
    # 可选：保证表存在（适合本地环境；生产请用迁移工具）
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        added = upsert_posts(db)
        if added == 0:
            print("Posts already exist. (nothing inserted)")
        else:
            print(f"Inserted {added} seed posts.")


if __name__ == "__main__":
    main()

