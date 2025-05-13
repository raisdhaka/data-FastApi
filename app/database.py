from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Admin%40123@localhost/wvictim"
SQLALCHEMY_DATABASE_URL = "postgresql://dbuser:dbuser123@178.128.219.6/victimbd"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://psql:Admin%40123@localhost:5432/wvictim"

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()