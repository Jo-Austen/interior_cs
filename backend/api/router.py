from fastapi import APIRouter
from backend.api.v1.public import contacts as pub_contacts
from backend.api.v1.public import posts as pub_posts

api_router = APIRouter(prefix="/api")

# v1 public
api_router.include_router(pub_contacts.router, prefix="/v1/public", tags=["public:contacts"])
api_router.include_router(pub_posts.router,    prefix="/v1/public", tags=["public:posts"])
