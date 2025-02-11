# Создание таблицы, если её нет (char, varchar)
def create_table(connection):
    cursor = connection.cursor()
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
    connection.commit()


def book_is_created(connection, isbn: int):
    cursor = connection.cursor()
    cursor.execute("SELECT isbn FROM books WHERE isbn = %s", isbn)
    cursor.fetchone()