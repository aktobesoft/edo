from fastapi import APIRouter, Depends
from common_module.urls_module import common_parameters
from sqlalchemy import select, tuple_
from core.db import database
from typing import List
from references.notes.models import Notes, NotesOut

notesRouter = APIRouter()

@notesRouter.get("/", response_model=List[NotesOut])
async def read_notes(commons: dict = Depends(common_parameters)):
    list1 = [tuple_(50, True),tuple_(51, True)]
    query = select(Notes.id, Notes.text, Notes.completed).where(tuple_(Notes.id, Notes.completed).in_(list1))
    listValue = await database.fetch_all(query)
    return listValue