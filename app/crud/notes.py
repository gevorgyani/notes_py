from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.notes import Note
from sqlalchemy import update, delete, or_
from datetime import datetime
from typing import Optional


async def get_notes(db: AsyncSession, show_deleted: bool = False, category: Optional[str] = None):
    query = select(
        Note)  #вызываем фукцию селет и указываем объект Note из модели, селект и название табл к которой хотим обратиться
    if not show_deleted:
        query = query.where(Note.is_deleted == False)
    if category:
        query = query.where(Note.category == category)
    result = await db.execute(query)  #чтобы выполнить query нужно вызвать execute
    return result.scalars().all()  #с помощью scalars мы получаем наши данные в формате класса Note(получаем список наших обектов этого класса)


async def get_note_by_id(db: AsyncSession, note_id: int):
    query = select(Note).where(Note.id == note_id, Note.is_deleted == False)
    result = await db.execute(query)
    return result.scalar_one_or_none()  #получаем один объект класса


async def create_note_in_db(db: AsyncSession, note_data: dict):
    db_note = Note(**note_data)  #создаем объект класса Note (передаем словарь)
    db.add(db_note)
    await db.commit()  #подтверждение операции
    return db_note  #у db ноут автоматически будет проставлен id


async def update_note_in_db(db: AsyncSession, db_note: Note, update_data: dict):
    for key, value in update_data.items():
        setattr(db_note, key, value)  #
    db_note.updated_at = datetime.utcnow()
    await db.commit()
    return db_note


async def delete_note_in_db(db: AsyncSession, db_note: Note):
    db_note.is_deleted = True
    await db.commit()
    return db_note


async def archive_note_in_db(db: AsyncSession, db_note: Note):
    db_note.status = "archived"
    await db.commit()
    return db_note


async def restore_note_in_db(db: AsyncSession, db_note: Note):
    db_note.is_deleted = False
    db_note.updated_at = datetime.utcnow()
    await db.commit()
    return db_note


async def search_note_in_db(db: AsyncSession, query: str):
    search_query = select(Note).where(
        Note.is_deleted == False,
        or_(
            Note.title.ilike(f"%{query}%"),
            Note.content.ilike(f"%{query}%")
        ))
    result = await db.execute(search_query)
    return result.scalars().all()  #с помощью scalars мы получаем наши данные в формате класса Note(получаем список наших обектов этого класса)
