from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import (
    books,
    users,
    reverses
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"]
)

app.include_router(users.router)
app.include_router(books.router)
app.include_router(reverses.router)

@app.get("/")
def home():
    return {
        "page": "home page"
    }