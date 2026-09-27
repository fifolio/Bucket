from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_current_user, get_user_supabase
from app.models.category import CategoryCreate, CategoryResponse, CategoryUpdate

categories = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)

@categories.get("", response_model=list[CategoryResponse])
def get_categories(current_user=Depends(get_current_user)):
    try:
        client = get_user_supabase(current_user["token"])
        response = client.table("categories").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@categories.post("", response_model=CategoryResponse)
def create_category(category: CategoryCreate, current_user=Depends(get_current_user)):
    try:
        client = get_user_supabase(current_user["token"])
        data = {
            **category.model_dump(),
            "user_id": current_user["user"].id,
        }
        response = client.table("categories").insert(data).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@categories.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, category: CategoryUpdate, current_user=Depends(get_current_user)):
    try:
        client = get_user_supabase(current_user["token"])
        response = (
            client.table("categories")
            .update(category.model_dump(exclude_unset=True))
            .eq("id", category_id)
            .execute()
            )
        if not response.data:
            raise HTTPException(status_code=404, detail="Category not found")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@categories.delete("/{category_id}")
def delete_category(category_id: int, current_user=Depends(get_current_user)):
    try:
        client = get_user_supabase(current_user["token"])
        response = (
            client.table("categories")
            .delete()
            .eq("id", category_id)
            .execute()
        )
        if not response.data:
            raise HTTPException(status_code=404, detail="Category not found")
        return {"message": "Category deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

