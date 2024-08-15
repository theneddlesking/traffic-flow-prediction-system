from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# allow CORS for frontend's origin
origins = [
    # dev
    "http://localhost:5173",
    # build
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# serve static files from the build directory
app.mount("/app", StaticFiles(directory="../frontend/dist", html=True), name="static")


@app.get("/api/hello")
async def read_root():
    return {"message": "Hello from FastAPI"}


@app.get("/api/add")
async def add_numbers(a: int, b: int):
    result = a + b
    return {"result": result}


# to run this api from the main directory:
# uvicorn test_api:app --reload