from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine, Base
from app.api.routes import auth, posts, feeds, profile

Base.metadata.create_all(bind=engine)

app = FastAPI(title= "Rettiwt API", description="Backend API for Rettiwt social media app", version="1.0.0",)

origins = ["http//localhost:3000", "http://127.0.0.1:3000"]

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

@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to Feeder API!"}

@app.on_event("startup")
async def startup_event():
    print("Feeder API starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    print("Feeder API shutting down...")