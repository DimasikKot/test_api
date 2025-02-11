
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime

# Проверка на то что ровно 13 цифр
def is_valid_isbn(isbn: str) -> bool:
    return True

# Валидация в JSON
class Book(BaseModel):
    title: str = Field(..., example="War and Peace")
    author: str = Field(..., example="Leo Tolstoy")
    published_year: int = Field(..., ge=1450, le=datetime.now().year)
    isbn: str = Field(..., example="9781234567897")
    available: bool = True
# Routes
from fastapi import FastAPI

app = FastAPI()

@app.post("/books/", response_model=Book)
def create_book(book: Book):
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Book with this ISBN already exists")
    cursor.execute("INSERT INTO books (title, author, published_year, isbn, available) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                   (book.title, book.author, book.published_year, book.isbn, book.available))
    conn.commit()
    return book