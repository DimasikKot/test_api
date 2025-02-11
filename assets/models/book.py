from pydantic import BaseModel, Field
from datetime import datetime


# Валидация в JSON
class Book(BaseModel):
    title: str = Field(..., example="War and Peace")
    author: str = Field(..., example="Leo Tolstoy")
    published_year: int = Field(..., ge=1450, le=datetime.now().year)
    isbn: str = Field(..., example="9781234567897")
    available: bool = True


# Проверка на то что ровно 13 цифр
def is_valid_isbn(isbn: str) -> bool:
    return len(isbn) == 13


# Проверка на то что ровно 13 цифр
def is_valid_published_year(published_year: int) -> bool:
    return 1450 <= published_year <= datetime.now().year
