CREATE DATABASE user_database;

\c user_database;

CREATE TABLE IF NOT EXISTS public.user_db (
  id                      BIGINT NOT NULL 
                            GENERATED ALWAYS AS IDENTITY, 
  username                VARCHAR(255) NOT NULL, 
  password                VARCHAR(255) NOT NULL,
  email                   VARCHAR(255) NOT NULL,
  phone                   INTEGER NOT NULL,
  role                    INTEGER NOT NULL DEFAULT 3,
  
  -- Optional
  age                     INTEGER,
  sex                     BOOLEAN,

  -- constraints
  UNIQUE(username),
  UNIQUE(email),
  UNIQUE(phone),
  PRIMARY KEY(id)
);