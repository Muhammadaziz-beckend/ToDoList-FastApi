from fastapi import APIRouter

from apps.tasks.models import TaskCrete, TaskUpdate
from database.data_control import (
    data_delete_tasks,
    data_get_tasks,
    data_post_tasks,
    data_update_tasks,
)


router = APIRouter()


@router.get("/tasks/")
def get_tasks():
    """
    Получения задач.
    """
    return data_get_tasks(many=True)


@router.post("/tasks/", response_model=TaskCrete)
def post_tasks(data: TaskCrete):
    """
    Создаёт новую задачу.
    """
    task_data = data.dict()
    data_post_tasks(task_data)
    return data


@router.delete("/tasks/{id}")
def delete_tasks(id: int):
    """
    Удоление задачу по id
    """

    return data_delete_tasks(id)


@router.put("/tasks/{id}")
def put_tasks(id: int, data:dict):

    return data_update_tasks(id, data)
