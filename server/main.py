import sys
import os
from fastapi import FastAPI
from pydantic_settings import BaseSettings
from configs import NGROK_AUTHTOKEN
from server.app.routers import llm

class Settings(BaseSettings):
    # ... The rest of our FastAPI settings

    base_url: str = "http://localhost:8000"
    use_ngrok: bool = os.environ.get("USE_NGROK", "False") == "True"

settings = Settings()

def init_webhooks(base_url):
    # Update inbound traffic via APIs to use the public-facing ngrok URL
    pass

# Initialize the FastAPI app for a simple web server
app = FastAPI()

if settings.use_ngrok is True and NGROK_AUTHTOKEN is not None:
    # pyngrok should only ever be installed or initialized in a dev environment when this flag is set
    from pyngrok import ngrok

    # Get the dev server port (defaults to 8000 for Uvicorn, can be overridden with `--port`
    # when starting the server
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else "8000"

    # Open a ngrok tunnel to the dev server
    public_url = ngrok.connect(port).public_url
    print(f"ngrok tunnel \"{public_url}/docs\" -> \"http://127.0.0.1:{port}\"")

    # Update any base URLs or webhooks to use the public ngrok URL
    settings.base_url = public_url
    init_webhooks(public_url)

# ... Initialize routers and the rest of our app

app.include_router(llm.router)
