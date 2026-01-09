from backend.core.db import engine, Base

import backend.models.post
import backend.models.contact

def main():
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

if __name__ == "__main__":
    main()

    