from fastapi import APIRouter, Depends, HTTPException
from app.db_errors import translate_db_error
from app.exceptions import NotFoundError
from postgrest.exceptions import APIError
from app.dependencies import get_current_user, get_user_supabase
from app.models.task import TaskCreate, TaskResponse, TaskUpdate


tasks = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@tasks.get("", response_model=list[TaskResponse])
def get_tasks(current_user=Depends(get_current_user)):
    client = get_user_supabase(current_user["token"])
    try:
        response = client.table("tasks").select("*, category:categories(*)").execute()
    except APIError as e:
        raise translate_db_error(e)
    return response.data


@tasks.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, current_user=Depends(get_current_user)):
    client = get_user_supabase(current_user["token"])
    try:
        response = (
            client.table("tasks")
            .select("*, category:categories(*)")
            .eq("id", task_id)
            .single()
            .execute()
        )
    except APIError as e:
        raise translate_db_error(e)
    if not response.data:
        raise NotFoundError("Task not found")
    return response.data


@tasks.post("", response_model=TaskResponse)
def create_task(task: TaskCreate, current_user=Depends(get_current_user)):
    client = get_user_supabase(current_user["token"])
    task_data = {**task.model_dump(), "user_id": current_user["user"].id}
    try:
        response = client.table("tasks").insert(task_data).execute()
    except APIError as e:
        raise translate_db_error(e)
    return response.data[0]

@tasks.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, current_user=Depends(get_current_user)):
    client = get_user_supabase(current_user["token"])
    try:
        response = (
            client.table("tasks")
            .update(task.model_dump(exclude_unset=True))
            .eq("id", task_id)
            .execute()
        )
    except APIError as e:
        raise translate_db_error(e)
    if not response.data:
        raise NotFoundError("Task not found")
    return response.data[0]

@tasks.delete("/{task_id}")
def delete_task(task_id: int, current_user=Depends(get_current_user)):
    client = get_user_supabase(current_user["token"])
    try:
        response = client.table("tasks").delete().eq("id", task_id).execute()
    except APIError as e:
        raise translate_db_error(e)
    if not response.data:
        raise NotFoundError("Task not found")
    return {"message": "Task deleted successfully"}