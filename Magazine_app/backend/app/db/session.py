import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Ensure we use an absolute path for SQLite if not provided, to avoid CWD issues
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Default to a local.db in the backend root directory (parent of app)
    # backend/app/db/session.py -> ../../../local.db
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    db_path = os.path.join(base_dir, "local.db")
    DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    # connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

if "sqlite" in DATABASE_URL:
     # Special args for SQLite
     engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        connect_args={"check_same_thread": False} 
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
