from pydantic import BaseModel

class NotesOut(BaseModel):
    id: int
    text: str
    completed: bool