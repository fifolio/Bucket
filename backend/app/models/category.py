from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    id: int
    name: str
    created_at: str

class CategoryUpdate(BaseModel):
    name: str | None = None

