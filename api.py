import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
import re

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    dbname="library", user="postgres", password="password", host="localhost", port="5050"
)
cursor = conn.cursor()

# Создание таблицы, если её нет (char, varchar)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        published_year INT NOT NULL,
        isbn TEXT UNIQUE NOT NULL,
        available BOOLEAN DEFAULT TRUE
    )
''')
conn.commit()

# Проверка на то что ровно 13 цифр
def is_valid_isbn(isbn: str) -> bool:
    return bool(re.match(r"^\d{13}$", isbn))

# Валидация в JSON
class Book(BaseModel):
    id: int
    title: str = Field(..., example="War and Peace")
    author: str = Field(..., example="Leo Tolstoy")
    published_year: int = Field(..., ge=1450, le=datetime.now().year)
    isbn: str = Field(..., example="9781234567897")
    available: bool = True


# Routes
app = FastAPI()

@app.post("/books/", response_model=Book)
def create_book(book: Book):
    cursor.execute("SELECT * FROM books WHERE isbn = %s", (book.isbn,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Book with this ISBN already exists")
    cursor.execute("INSERT INTO books (title, author, published_year, isbn, available) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                   (book.title, book.author, book.published_year, book.isbn, book.available))
    conn.commit()
    return book



@app.get("/books/", response_model=list(Book))
def get_books():
    cursor.execute("SELECT title, author, published_year, isbn, available FROM books")
    books = cursor.fetchall()
    return [Book(title=b[0], author=b[1], published_year=b[2], isbn=b[3], available=b[4]) for b in books]



@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    cursor.execute("SELECT title, author, published_year, isbn, available FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return Book(title=book[0], author=book[1], published_year=book[2], isbn=book[3], available=book[4])



@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: Book):
    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Book not found")
    cursor.execute("UPDATE books SET title=%s, author=%s, published_year=%s, isbn=%s, available=%s WHERE id=%s",
                   (book.title, book.author, book.published_year, book.isbn, book.available, book_id))
    conn.commit()
    return book



@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Book not found")
    cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
    conn.commit()
    return {"message": "Book deleted successfully"}
