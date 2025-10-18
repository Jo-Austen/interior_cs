from backend.core.db import engine, Base
import backend.models.post  # noqa
import backend.models.contact      # noqa

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tables created.")
