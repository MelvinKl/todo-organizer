from typing import List

from todo_organizer.db.schema.todo_item import TodoItem
from todo_organizer.logic.priority_update_algorithms import PriorityUpdateAlgorithms


class UpdateAlgorithms:
    def update_priority(self, list_items: List[TodoItem], max_priority: float) -> List[TodoItem]:
        for item in list_items:
            if item.priority_update_algorithm == PriorityUpdateAlgorithms.Increment.value:
                item.priority = self._increment(item, max_priority)
        return list_items

    @staticmethod
    def _increment(list_item: TodoItem, max_priority: float) -> TodoItem:
        new_priority = max(list_item.priority + list_item.priority_update_increment_weight, max_priority)
        return new_priority
