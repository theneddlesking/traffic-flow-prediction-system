import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.fix_dist import fix_dist
from api.routes.site import router as site_router
from api.routes.route import router as routing_router


sys.stdout.reconfigure(encoding="utf-8")

app = FastAPI()

# use site router
app.include_router(site_router, prefix="/site")

# use routing router
app.include_router(routing_router, prefix="/routing")

DEV_URL = "http://localhost:5173"
BUILD_URL = "http://localhost:8000"

# allow CORS for frontend's origin
origins = [
    DEV_URL,
    BUILD_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

APP_DIR = "/app"

# fix dist
fix_dist(APP_DIR)

# serve static files from the build directory
app.mount(APP_DIR, StaticFiles(directory="./frontend/dist", html=True), name="static")


# to run this api from the main directory:
# uvicorn app:app --reload
