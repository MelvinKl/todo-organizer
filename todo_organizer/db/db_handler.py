import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from todo_organizer.db.schema.todo_item import TodoItem
from todo_organizer.db.schema.todo_list import TodoList

logger = logging.getLogger(__name__)


class DBHandler:
    def __init__(self, connection_string: str):
        self._engine = create_engine(connection_string, echo=False)

    def get_list_items(self, todo_list: TodoList):
        with Session(self._engine) as session:
            result = session.query(TodoItem).filter_by(list_id=todo_list.id).order_by(-TodoItem.priority).all()
            return result

    def get_all_lists(self):
        with Session(self._engine) as session:
            result = session.query(TodoList).order_by(TodoList.name).all()
            return result

    def upsert(self, db_items):
        try:
            with Session(self._engine) as session:
                data = [session.merge(x) for x in db_items]  # upsert
                session.add_all(data)
                session.commit()
        except Exception as e:
            logger.error(f"Could not upsert data. {e}")
            raise e

    def delete(self, db_item):
        with Session(self._engine) as session:
            session.delete(db_item)
            session.commit()
