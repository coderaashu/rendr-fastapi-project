import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# 1. Try to get the URL from environment variables. Fallback to local for testing.
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:bhendi@localhost:5432/blog_db")

# 2. Render gives "postgres://", but SQLAlchemy needs "postgresql://"
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. Create the engine using the final URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()