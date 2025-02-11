






@app.get("/books/", response_model=list[Book])
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
