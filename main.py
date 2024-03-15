from fastapi import FastAPI
from router.url import url_router
from starlette.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Include Router
app.include_router(url_router)