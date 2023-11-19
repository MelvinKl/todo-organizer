from sqlalchemy import Column, String, Float

from todo_organizer.db.schema import Base


class TodoList(Base):
    __tablename__ = "todolist"

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String)
    priority_max = Column(Float, default=10.0)

    def __repr__(self):
        return self.name
