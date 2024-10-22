CREATE DATABASE books_database;

\c books_database;

CREATE TABLE IF NOT EXISTS public.authors_db (
  id                      BIGINT NOT NULL
                            GENERATED ALWAYS AS IDENTITY, 
  first_name              VARCHAR(255),
  second_name             VARCHAR(255),

  PRIMARY KEY(id)
)

CREATE TABLE IF NOT EXISTS public.genres_db (
  id                      BIGINT NOT NULL
                            GENERATED ALWAYS AS IDENTITY, 
  genre                   VARCHAR(50) NOT NULL,

  PRIMARY KEY(id)
)

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
)

CREATE INDEX book_index ON public.book_genres_db(book_id);
CREATE INDEX genre_index ON public.book_genres_db(genre_id);

