from fastapi import FastAPI
from server.app.routers import llm

app = FastAPI()

app.include_router(llm.router)
