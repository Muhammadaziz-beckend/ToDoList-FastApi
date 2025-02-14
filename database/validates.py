import json
from fastapi.responses import JSONResponse


def write_file(filename, many=False):
    """
    Для создания JSON файла, если его нет
    :param filename: Название файла
    :param many: Данные будут в list[] или dict{}
    """
    res = [] if many else {}
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(res, file, ensure_ascii=False, indent=4)
    return res


def decorator_validate_file(fun):
    """
    Декоратор для обработки исключений при работе с файлом:
    если файл поврежден или не найден, создается новый файл.
    """

    def wrapper(*args, **kwargs):
        from database.data_control import TasksConfig

        filename = TasksConfig.filename

        try:
            return fun(*args, **kwargs)  # Вызов функции, которую декорируем
        except (json.JSONDecodeError, FileNotFoundError) as e:
            # Если произошла ошибка с файлом, восстанавливаем файл
            print(f"Ошибка с файлом {filename}: {str(e)}")
            return write_file(filename, many=True)
        except Exception as e:
            # Ловим все другие исключения
            return JSONResponse({f"Произошла непредвиденная ошибка: {str(e)}"},500)

    return wrapper
