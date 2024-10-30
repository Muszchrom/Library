Server:
~/dbfiles/
~/*

run: docker compose -f docker-compose.dev.yml up --build -d

### Backend
If after building the application, the backed container does not start, you need to remove the 'migrations' folders

URLS:
* `http://localhost:8000/libraries/`                  <= returns json with available libraries
* `http://localhost:8000/libraries/?city=<city>`      <= returns json with available libraries in the city
* `http://localhost:8000/libraries/id`                <= returns json with a specific library

* `http://localhost:8000/authors/`                    <= returns json with available authors
* `http://localhost:8000/authors/id`                  <= returns json with a specific author

* `http://localhost:8000/books/`                      <= returns json with available books
* `http://localhost:8000/books/id`                    <= returns json with a specific book

* `books/genres`                                       <= not implemented yet

* `http://localhost:8000/genres/`                       <= returns json with available genres
* `http://localhost:8000/genres/Fantastyka`             <= returns json with a specific genre by name in database

* `http://localhost:8000/book-genres/`                  <= returns json with available relation book - genres
* `http://localhost:8000/book-genres/id`                <= returns json with a specific relation book - genres

* `http://localhost:8000/library-books/`              <= not implemented yet
* `http://localhost:8000/rentals/`                    <= not implemented yet


### Connecting to PostgreSQL server
* On host go to `localhost:5420`
* Right click Servers, located on the left side of browser window, then select Register, server
* Fill in Name field with whatever name you like
* Go to Connection section
  * Host name/address: `host.docker.internal`
  * Port: `5432`
  * Maintenance database: `student`
  * Username: `student`
  * Password: `student`


# Frontend
create file Frontend/.env.local with these lines in it:
`NEXTAUTH_SECRET=[secret key]`
`NEXTAUTH_URL=http://localhost:3000/`
And to get secret key run this command in ubuntu: `openssl rand -base64 32`

### Gateway
* Role:
  * 1 - Admin
  * 2 - Employee
  * 3 - User

#### Config
/books  
role 1 - DELETE,PUT,PATCH
role 2 - POST
role 3 - GET

/genres  
role 1 - POST,DELETE,PUT,PATCH
role 3 - GET

/authors
role 1 - DELETE,PUT,PATCH
role 2 - POST
role 3 - GET

/books-genres  
role 1 - DELETE,PUT,PATCH
role 2 - POST
role 3 - GET