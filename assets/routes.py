from fastapi import FastAPI, HTTPException
import assets.database as db
from assets.models.book import Book, is_valid_published_year, is_valid_isbn

conn = db.get_connection()
db.create_table(conn)

# Routes
app = FastAPI()


@app.post("/books/", response_model=Book)
def create_book(book: Book):
    if db.is_book_created_isbn(conn, book.isbn):
        raise HTTPException(status_code=400, detail="Book with this ISBN already exists")

    if not is_valid_isbn(book.isbn):
        raise HTTPException(status_code=400, detail="Invalid isbn")

    if not is_valid_published_year(book.published_year):
        raise HTTPException(status_code=400, detail="Invalid published year")

    db.create_book(conn, book)
    return book


@app.get("/books/", response_model=list[Book])
def get_books():
    return db.fetch_all_books(conn)


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    if not db.is_book_created_id(conn, book_id):
        raise HTTPException(status_code=404, detail="Book not found")

    book = db.fetch_one_book_id(conn, book_id)
    return Book(title=book[0], author=book[1], published_year=book[2], isbn=book[3], available=book[4])


@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: Book):
    if not db.is_book_created_id(conn, book_id):
        raise HTTPException(status_code=404, detail="Book not found")

    if db.is_book_created_isbn(conn, book.isbn):
        if db.fetch_one_book_id(conn, book_id)[3] != book.isbn:
            raise HTTPException(status_code=400, detail="Book with this ISBN already exists")

    if not is_valid_isbn(book.isbn):
        raise HTTPException(status_code=400, detail="Invalid isbn")

    if not is_valid_published_year(book.published_year):
        raise HTTPException(status_code=400, detail="Invalid published year")

    db.update_book(conn, book_id, book)
    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    if not db.is_book_created_id(conn, book_id):
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete_book(conn, book_id)
    return {"message": "Book deleted successfully"}
