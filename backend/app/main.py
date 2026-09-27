from fastapi import FastAPI
from app.routes.tasks import tasks as tasks_router
from app.routes.auth import auth as auth_router
from app.routes.categories import categories as categories_router


app = FastAPI(
    title="Bucket Backend API Documentation",
    description="A simple FastAPI application that uses Supabase for authentication and data storage.",
    version="1.0.0",
)

app.include_router(tasks_router)
app.include_router(auth_router)
app.include_router(categories_router)

@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}