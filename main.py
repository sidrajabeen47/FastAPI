from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, get_db
import models
import schemas
from langchain_openai import ChatOpenAI
import os
# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def sanity():
    return {"message": "API is up and running"}
@app.post("/create-tasks")
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)): 
    db_task = models.TaskModel(title=task.title)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
@app.get("/tasks")
def get_all_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.TaskModel).all()
    return tasks
@app.get("/tasks/{task_id}")
def get_single_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.TaskModel).filter(models.TaskModel.task_id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail=f"Task not found with ID {task_id}")
    return db_task
@app.put("/update-task/{task_id}")
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(models.TaskModel).filter(models.TaskModel.task_id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail=f"Task not found with ID {task_id}")
    db_task.title = task.title
    db_task.completed = task.completed
    db.commit()
    db.refresh(db_task)
    return db_task
@app.delete("/delete/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.TaskModel).filter(models.TaskModel.task_id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail=f"Task not found with ID {task_id}")
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully", "task": db_task}

llm = ChatOpenAI(
base_url="https://router.huggingface.co/v1",
api_key=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
model="mistralai/Mistral-7B-Instruct-v0.2:featherless-ai",
temperature=0.7,
max_tokens=200
)
def generate_tasks(goal: str):
    prompt = f"""
    Goal: {goal}
    Break this goal into 5 actionable tasks.
    Return ONLY the tasks, one per line.
    """
    
    response = llm.invoke(prompt) 
    tasks = [line.strip() for line in response.content.split("\n") if line.strip()]
    
    return tasks
@app.post("/tasks/generate", response_model=list[schemas.Task])
def generate_task(goal: schemas.GoalRequest, db: Session = Depends(get_db)):
    tasks = generate_tasks(goal.goal)
    created_tasks = []
    for task in tasks:
        cleaned_title = task.lstrip("1234567890.- ").strip()
        if not cleaned_title or len(cleaned_title) < 3:
            continue
        db_task = models.TaskModel(title=cleaned_title)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        created_tasks.append(db_task)
    return created_tasks
