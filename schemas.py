from pydantic import BaseModel
class TaskCreate(BaseModel):
    title: str
class TaskUpdate(BaseModel):
    title: str
    completed: bool
class GoalRequest(BaseModel):
    goal: str
class Task(BaseModel):
    task_id: int
    title: str
    completed: bool
class Config:
    from_attributes = True