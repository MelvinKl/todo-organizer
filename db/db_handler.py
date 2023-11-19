from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db.schema import Base
from db.schema.todo_item import TodoItem
from db.schema.todo_list import TodoList


class DBHandler:
    def __init__(self):
        self._engine = create_engine("sqlite+pysqlite:///test", echo=True)
        Base.metadata.create_all(self._engine)

    def get_list_items(self, todo_list: TodoList):
        with Session(self._engine) as session:
            result = session.query(TodoItem).filter_by(list_id=todo_list.id).order_by(
                -TodoItem.priority).all()
            return result

    def get_all_lists(self):
        with Session(self._engine) as session:
            result = session.query(TodoList).order_by(TodoList.name).all()
            return result

    def upsert(self, db_items):
        with Session(self._engine) as session:
            for i in range(len(db_items)):
                try:
                    db_items[i] = session.merge(db_items[i])
                except IntegrityError:
                    pass
                    # session.add(item)
            session.add_all(db_items)
            session.commit()

    def delete(self, db_item):
        with Session(self._engine) as session:
            session.delete(db_item)
            session.commit()
