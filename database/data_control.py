import json
from fastapi.responses import JSONResponse
from typing import Tuple
from apps.tasks.models import TaskCrete
from pydantic import BaseModel

from database.validates import decorator_validate_file


class TasksConfig:
    filename = "database/data_tasks.json"

    @classmethod
    def reade_file_tasks(cls):
        """
        Возволщяет данные задач
        """
        with open(cls.filename, "r", encoding="utf-8") as file:
            return json.load(file)

    @classmethod
    @decorator_validate_file
    def search_id(cls, task_id: int) -> Tuple[int, dict] | None:
        """
        Находит задачу по task_id
        """
        data = cls.reade_file_tasks()

        # Ищем задачу с нужным task_id
        task = next(
            ((index, task) for index, task in enumerate(data) if task["id"] == task_id),
            None,
        )

        if task:
            return task
        else:
            return (-1, f"Task with id {task_id} not found")


def load_validate(data, many=False):
    """
    Проверяет и приводит JSON к нужному формату.
    :param data: Загруженные данные
    :param many: True — если ожидаем список, False — если объект
    :return: Валидированные данные
    """
    if not data:  # Если пустой JSON
        return [] if many else {}

    if many and isinstance(data, list):
        return data
    elif not many and isinstance(data, dict):
        return data
    else:
        return list(data) if many else dict(data)


@decorator_validate_file
def data_get_tasks(many=False):
    """
    Загружает JSON из файла и валидирует.
    :param many: True — список задач, False — одиночный объект
    :return: Данные из JSON
    """
    filename = TasksConfig.filename

    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
        return load_validate(data, many=many)


@decorator_validate_file
def data_post_tasks(data: dict):
    """
    Добавляет новую задачу в список и сохраняет её в файл.
    :param data: Словарь с данными задачи
    :return: Обновленный объект задачи
    """
    filename = TasksConfig.filename

    # Загружаем текущие данные из файла
    with open(filename, "r", encoding="utf-8") as file:
        data_ = json.load(file)
    max_id = max([task["id"] for task in data_], default=0)

    # Присваиваем уникальный ID задаче
    task_id = max_id + 1
    data["id"] = task_id

    # Добавляем новую задачу в список
    data_.append(data)

    # Сохраняем обновленный список в файл
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data_, file, ensure_ascii=False, indent=4)

    # Возвращаем добавленную задачу с ID
    return data


@decorator_validate_file
def data_delete_tasks(task_id: int):

    filename = TasksConfig.filename

    with open(filename, "r", encoding="utf-8") as file:
        data: list[dict] = json.load(file)

    index, obj = TasksConfig.search_id(task_id)

    if index == -1:
        return JSONResponse({"Error": obj}, 404)

    data.pop(index)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    return JSONResponse("", 204)


@decorator_validate_file
def data_update_tasks(task_id: int, data: dict, pritel=False):
    # Поиск задачи по task_id
    index, res = TasksConfig.search_id(task_id)

    # Если задача не найдена, возвращаем ошибку 404
    if index == -1:
        return JSONResponse({"error": res}, status_code=404)
    res_id = res["id"]
    del res["id"]

    if not pritel:
        data_keys = set(dict(data).keys())
        res_keys = set(res.keys())

        if not (data_keys == res_keys):
            missing_keys = list(res_keys.difference(data_keys))
            if missing_keys:
                return JSONResponse(
                    {"error": f"Вы не передали: {', '.join(missing_keys)}"},
                    status_code=404,
                )


    for i in res:
        res[i] = data[i]

    res["id"] = res_id
    data_: list = TasksConfig.reade_file_tasks()
    filename = TasksConfig.filename

    data_.pop(index)
    data_.append(res)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data_, file, ensure_ascii=False, indent=4)

    return res
