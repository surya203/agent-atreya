from pydantic import BaseModel

class Task(BaseModel):
    id: int = None
    title: str
    completed: bool = False