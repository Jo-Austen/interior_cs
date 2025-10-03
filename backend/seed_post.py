from backend.db import SessionLocal
from backend.models_post import Post
from datetime import datetime

db = SessionLocal()
if not db.query(Post).count():
    db.add(Post(slug="hello-world", title="第一篇文章", summary="摘要",
                body="正文内容", published=True, published_at=datetime.now()))
    db.commit()
    print("Seeded one post.")
else:
    print("Posts already exist.")
db.close()
