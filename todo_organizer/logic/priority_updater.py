from datetime import datetime
from typing import List

from todo_organizer.db.schema.todo_item import TodoItem
from todo_organizer.logic.update_algorithms import UpdateAlgorithms


class PriorityUpdater:
    def update_priority(self, list_items: List[TodoItem], max_priority: float, load: bool = False) -> List[TodoItem]:
        for item in list_items:
            if item.priority_update_algorithm == UpdateAlgorithms.Increment.value and not load:
                item.priority = self._increment(item, max_priority)
            elif item.priority_update_algorithm == UpdateAlgorithms.Date:
                item.priority = self._update_date_priority(item, max_priority)
            item.last_priority_update = datetime.now()
        return list_items

    @staticmethod
    def _update_date_priority(list_item: TodoItem, max_priority: float) -> TodoItem:
        if list_item.priority_update_deadline_max_priority < list_item.priority:
            # priority is above the allowed regulation by datetime. Do nothing
            return list_item

        current_time = datetime.now()
        seconds_since_last_update = (current_time - list_item.last_priority_update).total_seconds()
        seconds_left = (list_item.priority_update_deadline - current_time).total_seconds()
        priority_left = list_item.priority_update_deadline_max_priority - list_item.priority
        priority_per_second = float(priority_left) / float(seconds_left)
        if priority_per_second < 0:
            # we are over the deadline
            list_item.priority = min(max_priority,
                                     max(list_item.priority, list_item.priority_update_deadline_max_priority))
            return list_item

        list_item.priority = priority_per_second * seconds_since_last_update + list_item.priority
        return list_item

    @staticmethod
    def _increment(list_item: TodoItem, max_priority: float) -> TodoItem:
        new_priority = max(list_item.priority + list_item.priority_update_increment_weight, max_priority)
        return new_priority
