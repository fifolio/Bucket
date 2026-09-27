from pydantic import BaseModel, ConfigDict, Field
from app.models.category import CategoryResponse

# input model
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200, description="Short title for the task.")
    description: str | None = Field(default=None, min_length=1, max_length=2000, description="Optional longer description of the task.")
    category_id: int | None = Field(default=None, description="ID of an existing category to file this task under. Omit for uncategorized.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Finish step 15",
                "description": "Add OpenAPI descriptions and examples to all routes.",
                "category_id": 1,
            }
        }
    )


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