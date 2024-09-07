from fastapi import FastAPI
from router.url import url_router
from starlette.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Include Router
app.include_router(url_router, prefix="/rapid_linker")

app.mount("/img", StaticFiles(directory="img"), name="img")