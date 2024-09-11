from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.notes import Note
from sqlalchemy import update, delete
from datetime import datetime
from typing import Optional


async def get_notes(db: AsyncSession, show_deleted: bool = False, category: Optional[str] = None):
    query = select(Note)
    if not show_deleted:
        query = query.where(Note.is_deleted == False)
    if category:
        query = query.where(Note.category == category)
    result = await db.execute(query)
    return result.scalars().all()

async def get_note_by_id(db: AsyncSession, note_id: int):
    query = select(Note).where(Note.id == note_id, Note.is_deleted == False)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def create_note_in_db(db: AsyncSession, note_data: dict):
    db_note = Note(**note_data)
    db.add(db_note)
    await db.commit()
    return db_note

async def update_note_in_db(db: AsyncSession, db_note: Note, update_data: dict):
    for key, value in update_data.items():
        setattr(db_note, key, value)
    db_note.updated_at = datetime.utcnow()
    await db.commit()
    return db_note

async def delete_note_in_db(db: AsyncSession, db_note: Note):
    db_note.is_deleted = True
    await db.commit()
    return db_note

async def restore_note_in_db(db: AsyncSession, db_note: Note):
    db_note.is_deleted = False
    db_note.updated_at = datetime.utcnow()
    await db.commit()
    return db_note
