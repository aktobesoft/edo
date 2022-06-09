from fastapi import APIRouter, Depends
from common_module.urls_module import query_parameters_list
from sqlalchemy import select, tuple_
from core.db import database
from typing import List
from catalogs.notes.models import Notes, NotesOut
from auth.user_auth import get_current_active_user, UserModel

notesRouter = APIRouter()

@notesRouter.get("/", response_model=List[NotesOut])
async def read_notes(parameters: dict = Depends(query_parameters_list), current_user: UserModel = Depends(get_current_active_user)):
    list1 = [tuple_(50, True),tuple_(51, True)]
    query = select(Notes.id, Notes.text, Notes.completed).where(tuple_(Notes.id, Notes.completed).in_(list1))
    listValue = await database.fetch_all(query)
    return listValue