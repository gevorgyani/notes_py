from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Annotated

from app.crud.notes import get_note_by_id
from app.schemas.notes import NoteCreate, NoteUpdate, NoteInDB
from app.core.init_db import get_db
from app.services.notes import (
    fetch_notes,
    create_note_service,
    update_note_service,
    delete_note_service,
    restore_note_service,
    search_note_service, archive_note_service
)

router = APIRouter()  #маршрут, который включает все эндпоинты


#эндпоинты, на которых делаются запросы
@router.get("/", response_model=List[NoteInDB])
async def read_notes(
        category: Optional[str] = None,
        show_deleted: bool = False,
        db: AsyncSession = Depends(get_db)
):
    notes = await fetch_notes(db, show_deleted=show_deleted, category=category)
    return notes


@router.get("/search", response_model=List[NoteInDB])
async def search_note_endpoint(
        query: str,
        db: AsyncSession = Depends(get_db)

):
    notes = await search_note_service(db, query=query)
    return notes



@router.post("/", response_model=NoteInDB)
async def create_note_endpoint(note: NoteCreate, db: AsyncSession = Depends(get_db)):
    return await create_note_service(db, note)


@router.get("/{note_id}", response_model=NoteInDB)
async def read_note_endpoint(note_id: int, db: AsyncSession = Depends(get_db)):
    note = await get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/{note_id}", response_model=NoteInDB)
async def update_note_endpoint(note_id: int, note: NoteUpdate, db: AsyncSession = Depends(get_db)):
    db_note = await update_note_service(db, note_id, note)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note


@router.delete("/{note_id}", response_model=dict)
async def delete_note_endpoint(note_id: int, db: AsyncSession = Depends(get_db)):
    db_note = await delete_note_service(db, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note marked as deleted successfully"}


@router.put("/{note_id}/archive", response_model=NoteInDB)
async def archive_note_endpoint(note_id: int, db: AsyncSession = Depends(get_db)):
    db_note = await archive_note_service(db, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note


@router.post("/{note_id}/restore", response_model=NoteInDB)
async def restore_note_endpoint(note_id: int, db: AsyncSession = Depends(get_db)):
    db_note = await restore_note_service(db, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Deleted note not found")
    return db_note
