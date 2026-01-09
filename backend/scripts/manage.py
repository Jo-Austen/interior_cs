import sys
from backend.scripts import init_db, seed_posts

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    if cmd == "create":
        init_db.main()
    elif cmd == "seed":
        seed_posts.main()
    else:
        print("Usage: python -m backend.scripts.manage [create|seed]")
