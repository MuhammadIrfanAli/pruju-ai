from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_FOLDER = "./database"
DATABASE_FILE = "pruju.db"
DATABASE_URL = f"sqlite:///{DATABASE_FOLDER}/{DATABASE_FILE}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()