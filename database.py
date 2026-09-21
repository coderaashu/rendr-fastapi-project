from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker ,declarative_base

DATABASE_URL = "postgresql://postgres:bhendi@localhost:5434/blog_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
