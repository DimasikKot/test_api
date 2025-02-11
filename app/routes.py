from fastapi import APIRouter
from schemas import Book
from database import get_db_connection
from crud import create_book

router = APIRouter()

@router.post("/books/")
def add_book(book: Book):
    conn = get_db_connection()
    create_book(conn, book)
    return book
