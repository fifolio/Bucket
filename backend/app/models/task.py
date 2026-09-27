from pydantic import BaseModel, Field
from app.models.category import CategoryResponse

# input model
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, min_length=1, max_length=2000)
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
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, min_length=1, max_length=2000)
    completed: bool | None = None
    category_id: int | None = None