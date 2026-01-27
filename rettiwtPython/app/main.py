from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine, Base
from app.api.routes import auth, posts, feeds, profile
import asyncio
import datetime
import platform
import psutil

Base.metadata.create_all(bind=engine)

app = FastAPI(title= "Rettiwt API", description="Backend API for Rettiwt social media app", version="1.0.0",)

origins = ["http//localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://127.0.0.1:5173"]

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
    """
    Base endpoint, returning 'hello world' message
    """
    return {"message": "Welcome to Feeder API!"}

clients: list[WebSocket] = []

@app.websocket("/ws/info")
async def websocket_info(ws: WebSocket):
    """
    Server info websocket
    
    :param ws: Websocket instance
    :type ws: WebSocket
    """
    await ws.accept()
    clients.append(ws)
    try:
        while True:
            info = {
                "time": datetime.datetime.utcnow().isoformat() + "Z",
                "uptime_seconds": int((datetime.datetime.utcnow() - datetime.datetime.fromtimestamp(psutil.boot_time())).total_seconds()),
                "cpu_percent": psutil.cpu_percent(interval=None),
                "memory_percent": psutil.virtual_memory().percent,
                "platform": platform.system(),
                "python_version": platform.python_version(),
                "connected_clients": len(clients),
            }

            await ws.send_json(info)
            await asyncio.sleep(5)  # repeat every 5s

    except WebSocketDisconnect:
        clients.remove(ws)


@app.on_event("startup")
async def startup_event():
    """
    Console debug tool
    """
    print("Feeder API starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Console debug tool
    """
    print("Feeder API shutting down...")