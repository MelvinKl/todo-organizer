from sqlalchemy import Column, Float, String, ForeignKey, Integer

from db.schema import Base
from db.schema.todo_list import TodoList


class TodoItem(Base):
    __tablename__ = "todoitem"

    id = Column(Integer, primary_key=True)
    list_id = Column(String, ForeignKey(f"{TodoList.__tablename__}.id"))
    priority = Column(Float)
    title = Column(String)
    description = Column(String, default="")
    priority_update_increment_weight = Column(Float, default=0.25)
