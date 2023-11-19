from typing import List

from db.schema.todo_item import TodoItem


class UpdateAlgorithms:
    @staticmethod
    def increment(list_items: List[TodoItem], max_priority: float) -> List[TodoItem]:
        for item in list_items:
            item.priority = max(item.priority + item.priority_update_increment_weight, max_priority)
        return list_items
