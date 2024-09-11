from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# Определение моделей данных с помощью Pydantic

class NoteBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Title of the note")
    content: str = Field(..., min_length=10, description="Content of the note")
    category: Optional[str] = Field(None, max_length=50, description="Category of the note")


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    content: Optional[str] = Field(None, min_length=10)
    category: Optional[str] = Field(None, max_length=50)


class NoteInDB(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool = False

    class Config:
        orm_mode = True
