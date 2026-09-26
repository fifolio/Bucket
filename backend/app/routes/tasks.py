from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_current_user, get_user_supabase
from app.models.task import TaskCreate, TaskResponse, TaskUpdate


tasks = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@tasks.get("", response_model=list[TaskResponse])
def get_tasks(current_user=Depends(get_current_user)):
    try:
        client = get_user_supabase(current_user["token"])

        response = (
            client
            .table("tasks")
            .select("*")
            .execute()
        )

        return response.data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@tasks.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user=Depends(get_current_user),
):
    try:
        client = get_user_supabase(current_user["token"])

        response = (
            client
            .table("tasks")
            .select("*")
            .eq("id", task_id)
            .single()
            .execute()
        )

        return response.data

    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )


@tasks.post("", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    current_user=Depends(get_current_user),
):
    try:
        client = get_user_supabase(current_user["token"])

        task_data = {
            **task.model_dump(),
            "user_id": current_user["user"].id,
        }

        response = (
            client
            .table("tasks")
            .insert(task_data)
            .execute()
        )

        return response.data[0]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@tasks.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task: TaskUpdate,
    current_user=Depends(get_current_user),
):
    try:
        client = get_user_supabase(current_user["token"])

        response = (
            client
            .table("tasks")
            .update(task.model_dump(exclude_unset=True))
            .eq("id", task_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=404,
                detail="Task not found",
            )

        return response.data[0]

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@tasks.delete("/{task_id}")
def delete_task(
    task_id: int,
    current_user=Depends(get_current_user),
):
    try:
        client = get_user_supabase(current_user["token"])

        response = (
            client
            .table("tasks")
            .delete()
            .eq("id", task_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=404,
                detail="Task not found",
            )

        return {
            "message": "Task deleted successfully"
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )