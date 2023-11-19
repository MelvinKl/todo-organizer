from sqlalchemy import Column, String, Float

from db.schema import Base


class TodoList(Base):
    __tablename__ = "todolist"

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String)
    priority_max = Column(Float, default=10.)

    def __repr__(self):
        return self.name
