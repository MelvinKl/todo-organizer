from sqlalchemy import Column, String, Float, Integer

from db.schema import Base


class TodoList(Base):
    __tablename__ = "todolist"

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String)
    priority_max = Column(Float, default=10.)
    priority_update_algorithm = Column(Integer, default=0)

    def __repr__(self):
        return self.name
