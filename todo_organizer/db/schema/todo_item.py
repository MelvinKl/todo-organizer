from sqlalchemy import Column, Float, String, ForeignKey, Integer, DateTime

from todo_organizer.db.schema import Base
from todo_organizer.db.schema.todo_list import TodoList


class TodoItem(Base):
    __tablename__ = "todoitem"

    id = Column(Integer, primary_key=True)
    list_id = Column(String, ForeignKey(f"{TodoList.__tablename__}.id"))
    priority = Column(Float)
    title = Column(String)
    description = Column(String, default="")

    priority_update_algorithm = Column(Integer, default=0)
    priority_update_increment_weight = Column(Float, default=0.25)
    priority_update_deadline = Column(DateTime)
    priority_update_deadline_max_priority = Column(Float, default=0)
    last_priority_update = Column(DateTime)
