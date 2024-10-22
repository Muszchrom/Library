CREATE DATABASE books_database;

\c books_database;

CREATE TABLE IF NOT EXISTS public.authors_db (
  id                      BIGINT NOT NULL
                            GENERATED ALWAYS AS IDENTITY, 
  first_name              VARCHAR(255),
  second_name             VARCHAR(255),

  PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS public.genres_db (
  id                      BIGINT NOT NULL
                            GENERATED ALWAYS AS IDENTITY, 
  genre                   VARCHAR(50) NOT NULL,

  PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS public.books_db (
  id                      BIGINT NOT NULL 
                            GENERATED ALWAYS AS IDENTITY, 
  author_id               BIGINT NOT NULL,
  isbn                    VARCHAR(10) NOT NULL,
  isbn13                    VARCHAR(13) NOT NULL,
  title                   VARCHAR(255) NOT NULL,
  description             VARCHAR(255),
  publication_date        DATE NOT NULL,

  FOREIGN KEY(author_id) REFERENCES public.authors_db(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS public.book_genres_db (
  book_id                 BIGINT NOT NULL,
  genre_id                BIGINT NOT NULL,

  FOREIGN KEY(book_id) REFERENCES public.books_db(id)
    ON DELETE CASCADE,
  FOREIGN KEY(genre_id) REFERENCES public.genres_db(id)
    ON DELETE CASCADE,
  PRIMARY KEY(book_id, genre_id)
);

CREATE INDEX book_index ON public.book_genres_db(book_id);
CREATE INDEX genre_index ON public.book_genres_db(genre_id);


CREATE TABLE IF NOT EXISTS public.libraries_db (
  id                      INTEGER NOT NULL 
                            GENERATED ALWAYS AS IDENTITY, 
  library_name            VARCHAR(255),

  PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS public.library_books_db (
  book_id                 BIGINT NOT NULL,
  library_id              INTEGER NOT NULL,
  book_count              INTEGER NOT NULL,

  FOREIGN KEY(book_id) REFERENCES public.books_db(id),
  FOREIGN KEY(library_id) REFERENCES public.libraries_db(id),
  PRIMARY KEY(book_id, library_id)
);

CREATE TABLE IF NOT EXISTS public.rentals_db (
  id                      BIGINT NOT NULL 
                            GENERATED ALWAYS AS IDENTITY, 
  user_id                 BIGINT NOT NULL,
  book_id                 BIGINT NOT NULL,
  library_id              INTEGER NOT NULL, 
  rental_status           VARCHAR(25) NOT NULL, 
  rental_date             DATE NOT NULL,
  due_date                DATE NOT NULL,
  return_date             DATE,

  FOREIGN KEY(book_id) REFERENCES public.books_db(id),
  FOREIGN KEY(library_id) REFERENCES public.libraries_db(id),
  PRIMARY KEY(id)
);