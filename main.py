if __name__ == '__main__':
    conn = database.get_connection()
    database.create_table(conn)