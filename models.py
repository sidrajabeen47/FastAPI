from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class TaskModel(Base):
    __tablename__ = "tasks"

    # Indent these lines so they belong to the class:
    task_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)