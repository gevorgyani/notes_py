from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# Определение моделей данных с помощью Pydantic
# Pydantic - библиотека, которая позволяет создавать классы ,
# т.е схемы того, как мы должны принимать данные, в каком формате,
# мы это будем реализовывать с помощью классов.

class NoteBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Title of the note")
    content: str = Field(..., min_length=10, description="Content of the note")
    category: Optional[str] = Field(None, max_length=50, description="Category of the note")
    status: str = Field("active", description="Status of the note")


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    # нам позволяет описывать схемы , которые мы потом будем применять к эндпоинтам
    # указываем названия полей, которые будем принимать при создании заметок
    # этот класс используем в качестве схемы, чтобы мы потом могли работать с
    # моделями этого класса и доставать инфу из них, что то типо словаря
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    content: Optional[str] = Field(None, min_length=10)
    category: Optional[str] = Field(None, max_length=50)
    status: Optional[str] = Field("active", description="Status of the note")


class NoteInDB(NoteBase):
    # класс, который отвечает з сохранение данных в бд, указываем в каком формате хотим сохранить инфу в бд
    id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool = False

    class Config:
        orm_mode = True  #позволяет работать пайдантик моделям работать с sqlalchemy
