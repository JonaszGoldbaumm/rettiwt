# app/tests/conftest.py
import os
import pytest
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import get_db
from app.api.routes import auth, posts, feeds, profile

# --- Test DB file ---
TEST_DB_FILE = "./test.db"
if os.path.exists(TEST_DB_FILE):
    os.remove(TEST_DB_FILE)

# --- SQLite for tests, but same schema as MySQL ---
SQLALCHEMY_TEST_DB_URL = f"sqlite:///{TEST_DB_FILE}"
engine = create_engine(
    SQLALCHEMY_TEST_DB_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# --- Ensure foreign key constraints ---
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, conn_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# --- Override get_db dependency ---
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
        db.commit()
    finally:
        db.close()

# --- Function to create tables using your MySQL schema ---
def create_mysql_like_schema():
    ddl = """
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        profile_pic BLOB,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        media BLOB,
        id_user INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE
    );

    CREATE TABLE likes (
        id_post INTEGER NOT NULL,
        id_user INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id_post, id_user),
        FOREIGN KEY (id_post) REFERENCES posts(id) ON DELETE CASCADE,
        FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE
    );

    CREATE TABLE comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_post INTEGER NOT NULL,
        id_user INTEGER NOT NULL,
        text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_post) REFERENCES posts(id) ON DELETE CASCADE,
        FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE
    );

    CREATE TABLE followed (
        id_user INTEGER NOT NULL,
        by_user INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id_user, by_user),
        FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (by_user) REFERENCES users(id) ON DELETE CASCADE,
        CHECK (id_user <> by_user)
    );
    """
    with engine.connect() as conn:
        for stmt in ddl.strip().split(";"):
            if stmt.strip():
                conn.execute(text(stmt))
        conn.commit()

# --- Create test app ---
def create_test_app():
    app = FastAPI(title="Test Rettiwt API")
    origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(auth.router)
    app.include_router(posts.router)
    app.include_router(feeds.router)
    app.include_router(profile.router)
    return app

# --- Fixture ---
@pytest.fixture(scope="session")
def client():
    create_mysql_like_schema()  # <-- Use exact MySQL-like tables

    app = create_test_app()
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    from app.db.base import Base
    Base.metadata.drop_all(bind=engine)
