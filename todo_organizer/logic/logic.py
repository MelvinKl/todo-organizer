import logging
from typing import List

from todo_organizer.db.db_handler import DBHandler
from todo_organizer.db.schema.todo_item import TodoItem
from todo_organizer.db.schema.todo_list import TodoList
from todo_organizer.logic.priority_updater import PriorityUpdater

logger = logging.getLogger(__name__)


class Logic:
    def __init__(self, db_handler: DBHandler, priority_updater: PriorityUpdater):
        self._db_handler = db_handler
        self._priority_updater = priority_updater

    def get_all_lists(self):
        return self._db_handler.get_all_lists()

    def get_list_items(self, todo_list: TodoList) -> List[TodoItem]:
        list_items = self._db_handler.get_list_items(todo_list)
        # update of timed priority
        list_items = self._priority_updater.update_priority(list_items, todo_list.priority_max, True)
        return list_items

    def upsert_list(self, todo_list, list_items):
        self._db_handler.upsert([todo_list])
        self._db_handler.upsert(list_items)

    def delete_item(self, list_item):
        self._db_handler.delete(list_item)

    def finish_item(self, todo_list, list_item):
        self.delete_item(list_item)
        remaining_items = self.get_list_items(todo_list)
        remaining_items = self._priority_updater.update_priority(remaining_items, todo_list.priority_max)
        self.upsert_list(todo_list, remaining_items)
