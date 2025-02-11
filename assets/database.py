from psycopg2._psycopg import connection
from assets.models.book import Book
import psycopg2


# Подключение к базе данных PostgreSQL
def get_connection() -> connection:
    return psycopg2.connect(
        dbname="library", user="postgres", password="password", host="localhost", port="5050"
    )


# Создание таблицы, если её нет (char, varchar)
def create_table(conn: connection) -> None:
    cursor = conn.cursor()
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


# Проверка, есть ли в БД книга
def is_book_created_isbn(conn: connection, isbn: str) -> bool:
    cursor = conn.cursor()
    cursor.execute("SELECT isbn FROM books WHERE isbn = %s", (isbn,))
    return cursor.fetchone() is not None


# Проверка, есть ли в БД книга
def is_book_created_id(conn: connection, book_id: int) -> bool:
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM books WHERE id = %s", (book_id,))
    return cursor.fetchone() is not None


def create_book(conn: connection, book: Book) -> None:
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO books (title, author, published_year, isbn, available) VALUES (%s, %s, %s, %s, %s) RETURNING id",
        (book.title, book.author, book.published_year, book.isbn, book.available))
    conn.commit()


def update_book(conn: connection, book_id: int, book: Book) -> None:
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET title=%s, author=%s, published_year=%s, isbn=%s, available=%s WHERE id=%s",
                   (book.title, book.author, book.published_year, book.isbn, book.available, book_id))
    conn.commit()


def delete_book(conn: connection, book_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
    conn.commit()


def fetch_all_books(conn: connection) -> list[Book]:
    cursor = conn.cursor()
    cursor.execute("SELECT title, author, published_year, isbn, available FROM books")
    books = cursor.fetchall()
    return [Book(title=b[0], author=b[1], published_year=b[2], isbn=b[3], available=b[4]) for b in books]


def fetch_one_book_isbn(conn: connection, isbn: str) -> Book | None:
    cursor = conn.cursor()
    cursor.execute("SELECT title, author, published_year, isbn, available FROM books WHERE isbn = %s", (isbn,))
    return cursor.fetchone()


def fetch_one_book_id(conn: connection, book_id: int) -> Book | None:
    cursor = conn.cursor()
    cursor.execute("SELECT title, author, published_year, isbn, available FROM books WHERE id = %s", (book_id,))
    return cursor.fetchone()
