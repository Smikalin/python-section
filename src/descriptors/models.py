from typing import Any, TypeAlias

JSON: TypeAlias = dict[str, Any]


class Model:
    def __init__(self, payload: JSON):
        self.payload = payload


class Field:
    def __init__(self, path: str):
        self.path = path

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        # Разбиваем путь на части
        parts = self.path.split(".")
        current = obj.payload

        # Проходим по пути
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None

        return current

    def __set__(self, obj, value):
        if obj is None:
            return

        # Разбиваем путь на части
        parts = self.path.split(".")
        current = obj.payload

        # Проходим по пути, создавая промежуточные словари если нужно
        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {}
            current = current[part]

        # Устанавливаем значение в последней части пути
        current[parts[-1]] = value
