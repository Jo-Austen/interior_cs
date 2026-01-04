import sys
from backend.scripts import create_tables, seed_posts

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    if cmd == "create":
        create_tables.main()
    elif cmd == "seed":
        seed_posts.main()
    else:
        print("Usage: python -m backend.scripts.manage [create|seed]")
