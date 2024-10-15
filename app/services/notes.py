from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.notes import NoteCreate, NoteUpdate, NoteInDB
from ..crud.notes import (
    get_notes,
    get_note_by_id,
    create_note_in_db,
    update_note_in_db,
    delete_note_in_db,
    restore_note_in_db,
    search_note_in_db, archive_note_in_db
)


async def fetch_notes(db: AsyncSession, show_deleted: bool = False, category: Optional[str] = None):  #параметры функции
    return await get_notes(db, show_deleted=show_deleted,
                           category=category)  #ожидание выполнения других асинхронных операций


async def create_note_service(db: AsyncSession, note: NoteCreate):
    note_data = note.dict()
    return await create_note_in_db(db, note_data)


async def update_note_service(db: AsyncSession, note_id: int, note_update: NoteUpdate):
    db_note = await get_note_by_id(db, note_id)  #по id получаем заметку
    if not db_note:
        return None
    update_data = note_update.dict(exclude_unset=True)  #exclude_unset позволяет все сделать как ключ к значению
    return await update_note_in_db(db, db_note, update_data)


async def archive_note_service(db: AsyncSession, note_id: int):
    db_note = await get_note_by_id(db, note_id)
    if not db_note:
        return None
    return await archive_note_in_db(db, db_note)


async def delete_note_service(db: AsyncSession, note_id: int):
    db_note = await get_note_by_id(db, note_id)
    if not db_note:
        return None
    return await delete_note_in_db(db, db_note)


async def restore_note_service(db: AsyncSession, note_id: int):
    db_note = await get_note_by_id(db, note_id)
    if not db_note:
        return None
    return await restore_note_in_db(db, db_note)


async def search_note_service(db: AsyncSession, query: str):
    return await search_note_in_db(db, query=query)
