CREATE DATABASE user_database;

\c user_database;

CREATE TABLE IF NOT EXISTS public.user_db (
  id                      BIGINT NOT NULL 
                            GENERATED ALWAYS AS IDENTITY, 
  username                VARCHAR(255) NOT NULL, 
  password                VARCHAR(255) NOT NULL,
  is_admin                BOOLEAN NOT NULL DEFAULT FALSE,

  UNIQUE(username),
  PRIMARY KEY(id)
);