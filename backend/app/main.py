from fastapi import FastAPI, Request
from app.exceptions import AppError
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.routes.tasks import tasks as tasks_router
from app.routes.auth import auth as auth_router
from app.routes.categories import categories as categories_router

tags_metadata = [
    {
        "name": "Authentication",
        "description": "Login and session handling via Supabase Auth.",
    },
    {
        "name": "Tasks",
        "description": "CRUD operations on tasks. Each task belongs to the "
                        "authenticated user and may optionally be linked to a category.",
    },
    {
        "name": "Categories",
        "description": "CRUD operations on categories. Tasks can be grouped "
                        "under a category via `category_id`.",
    },
]

app = FastAPI(
    title="Bucket API",
    description=(
        "A task-management API built with FastAPI and Supabase, used as a "
        "learning project to practice authentication, row-level security, "
        "relational data modeling, and production-grade error handling.\n\n"
        "All endpoints except `/auth/login` require a Bearer token obtained "
        "from that endpoint."
    ),
    version="1.0.0",
    openapi_tags=tags_metadata,
    contact={"name": "Firas Dabbabi"},
)

app.include_router(tasks_router)
app.include_router(auth_router)
app.include_router(categories_router)

@app.exception_handler(AppError)
def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"type": exc.__class__.__name__, "message": exc.detail}},
    )

@app.exception_handler(RequestValidationError)
def validation_error_handler(request: Request, exc: RequestValidationError):
    # Flatten Pydantic's nested error format into something a frontend can render directly
    errors = [
        {"field": ".".join(str(p) for p in err["loc"][1:]), "message": err["msg"]}
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={"error": {"type": "ValidationError", "message": "Invalid request data", "fields": errors}},
    )

    
@app.get("/", summary="Health check", description="Simple liveness check — returns a static message.")
def root():
    return {"message": "Hello, FastAPI!"}