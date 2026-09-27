from pydantic import BaseModel, Field

class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)

class CategoryResponse(BaseModel):
    id: int
    name: str
    created_at: str

class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)

