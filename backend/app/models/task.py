from pydantic import BaseModel

# input model
class TaskCreate(BaseModel):
    title: str
    description: str | None = None

# output model
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: str

# input model for updating a task
class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None