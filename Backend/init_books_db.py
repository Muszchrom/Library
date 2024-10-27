import psycopg2
from psycopg2 import sql
from datetime import datetime
import random
from faker import Faker
import logging

fake = Faker()

db_config = {
    'dbname': 'host.docker.internal',
    'user': 'student',
    'password': 'student',
    'host': 'localhost',
    'port': '5432'
}

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def is_table_empty(table_name):
    conn = None
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(table_name)))
        count = cursor.fetchone()[0]
        return count == 0
    except Exception as e:
        logging.error("Database error when checking table: %s", e)
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_data(table_name, columns, data):
    if is_table_empty(table_name):
        query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(columns))
        )
        conn = None
        try:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()
        except Exception as e:
            logging.error("Database error during data insertion: %s", e)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

def populate_authors_db(n):
    if is_table_empty('authors_db'):
        for _ in range(n):
            data = (None, fake.first_name(), fake.last_name())
            insert_data('authors_db', ['id', 'first_name', 'second_name'], data)

def populate_genres_db(genres):
    if is_table_empty('genres_db'):
        for genre in genres:
            data = (None, genre)
            insert_data('genres_db', ['id', 'genre'], data)

def populate_book_genres_db(n):
    if is_table_empty('book_genres_db'):
        for _ in range(n):
            book_id = random.randint(1, 10) 
            genre_id = random.randint(1, 5)  
            data = (book_id, genre_id)
            insert_data('book_genres_db', ['book_id', 'genre_id'], data)

def populate_rentals_db(n):
    if is_table_empty('rentals_db'):
        for _ in range(n):
            user_id = random.randint(1, 100)  
            book_id = random.randint(1, 10)  
            library_id = random.randint(1, 5) 
            rental_status = fake.random_element(elements=('rented', 'returned', 'reserved'))
            rental_date = fake.date_between(start_date='-2y', end_date='today')
            due_date = fake.date_between(start_date='today', end_date='+1y')
            return_date = fake.date_between(start_date=rental_date, end_date=due_date) if rental_status == 'returned' else None
            data = (None, user_id, book_id, library_id, rental_status, rental_date, due_date, return_date)
            insert_data('rentals_db', ['id', 'user_id', 'book_id', 'library_id', 'rental_status', 'rental_date', 'due_date', 'return_date'], data)

def populate_libraries_db(libraries):
    if is_table_empty('libraries_db'):
        for library in libraries:
            data = (None, library)
            insert_data('libraries_db', ['id', 'library_name'], data)

def populate_library_books_db(n):
    if is_table_empty('library_books_db'):
        for _ in range(n):
            book_id = random.randint(1, 10) 
            library_id = random.randint(1, 5)  
            book_count = random.randint(1, 100)
            data = (book_id, library_id, book_count)
            insert_data('library_books_db', ['book_id', 'library_id', 'book_count'], data)


populate_authors_db(10)
populate_genres_db(['Fantasy', 'Science Fiction', 'Mystery', 'Horror', 'Romance'])
populate_book_genres_db(10)
populate_rentals_db(10)
populate_libraries_db(['Main Branch', 'Downtown', 'East Side', 'West End', 'Suburban'])
populate_library_books_db(10)
