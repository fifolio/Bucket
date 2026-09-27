from pydantic import BaseModel
from app.models.category import CategoryResponse

# input model
class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    category_id: int | None = None


# output model
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: str
    category_id: int | None = None
    category: CategoryResponse | None = None  # populated when joined

# input model for updating a task
class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    category_id: int | None = None