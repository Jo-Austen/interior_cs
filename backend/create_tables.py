from backend.db import engine, Base
import backend.models_post  # noqa

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tables created.")
