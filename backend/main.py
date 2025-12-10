from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="UrbanFlow Backend", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

from auth_routes import auth_router
from estacao_routes import estacao_router

app.include_router(auth_router)
app.include_router(estacao_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
