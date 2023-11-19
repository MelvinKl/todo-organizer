import logging

from db.db_handler import DBHandler
from logic.update_algorithms import UpdateAlgorithms

logger = logging.getLogger(__name__)


class Logic:

    def __init__(self):
        self._db_handler = DBHandler()
        self._priority_updater = UpdateAlgorithms()

    def get_all_lists(self):
        return self._db_handler.get_all_lists()

    def get_list_items(self, todo_list):
        return self._db_handler.get_list_items(todo_list)

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
