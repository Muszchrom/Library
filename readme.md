Server:
~/dbfiles/
~/*

run: docker compose -f docker-compose.dev.yml up --build -d

### Backend
If after building the application, the backed container does not start, you need to remove the 'migrations' folders

URLS:
* `http://localhost:8000/libraries/`                  <= returns json with available libraries
* `http://localhost:8000/libraries/?city=<city>`      <= returns json with available libraries in the city
* `http://localhost:8000/libraries/?latitude=<>&longitude=<>`   <= returns json with list of nearest libraries
* `http://localhost:8000/libraries/id`                <= returns json with a specific library

* `http://localhost:8000/authors/`                    <= returns json with available authors
* `http://localhost:8000/authors/id`                  <= returns json with a specific author

* `http://localhost:8000/books/`                      <= returns json with available books
* `http://localhost:8000/books/id`                    <= returns json with a specific book
* `http://localhost:8000/books/?author=<>`            <= returns json with books written by this author
* `http://localhost:8000/books/?genre=<>`             <= returns json with books of this genre
* `http://localhost:8000/books/?rating=<>`            <= return json with books with this rating
* `http://localhost:8000/books/?title=<>`           <= return json with books of this title
* `http://localhost:8000/books/?search=<>`          <= serching books by title and author


* `http://localhost:8000/genres/`                       <= returns json with available genres
* `http://localhost:8000/genres/Fantastyka`             <= returns json with a specific genre by name in database
* `http://localhost:8000/genres/?genre=<>`              <= return json with books of this genre 

* `http://localhost:8000/book-genres/`                  <= returns json with available relation book - genres
* `http://localhost:8000/book-genres/id`                <= returns json with a specific relation book - genres

* `http://localhost:8000/best-nearest/?latitude=<>&longitude=<>`                <= returns json with books which have best rating from nearest libraries

* `http://localhost:8000/bestseller`                <= returns json with books which have best rating

* `http://localhost:8000/library-books/`              <= not implemented yet
* `http://localhost:8000/rentals/`                    <= not implemented yet


# Connecting to PostgreSQL server
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
Create a file Frontend/.env.local with these lines in it:
```
NEXTAUTH_SECRET=[secret key]
NEXTAUTH_URL=http://localhost:3000/

GATEWAY_URL=http://gateway:8081/
GATEWAY_URL_CLIENT=http://localhost:8081/
BACKEND_URL=http://backend:8000/
BACKEND_URL_NO_PORT_NO_HTTP=backend
GATEWAY_URL_NO_PORT_NO_HTTP=gateway
```

And to get secret key run this command in ubuntu: `openssl rand -base64 32`

# Gateway
### Custom headers for user authentication on backend
<b>X-role-id</b> or in python <b>HTTP_X_ROLE_ID</b> consists of two values in the following format: "user_role user_id". Real world example would be "3 1"
Note that not every request would have this kind of header on itself. This type of data can only be retrieved when user is signed in. Because of that add appropriate null handlers or inform gateway maintainers about routes requiring user_role and user_id. Possible values: `"user_role user_id" | null`.

python code example to get this header: `self.request.META.get('HTTP_X_ROLE_ID')`

Roles:
* 1 - Admin
* 2 - Employee
* 3 - User

## Routes
### /auth/user
#### PATCH
Alters current record in database. User must be logged in and token must be provided. Please provide only one field that has to be changed at the time otherwise errors might occur since only one field changes per request in set order. 

<b>@Headers</b><br>
Authorization bearer with JWT. 

<b>@Body</b><br>
Takes current password and a field that has to be changed.
```
{
    "password": "student", 
    // plus one of the following
    "newPassword": "student2"
    "username": "student"
    "email": "student@student.student"
    "phone": 123123123
}
```
<b>@Response</b></br> 
```
{
    "id": 1,
    "username": "student",
    "email": "student@student.student",
    "phone": 123123123,
    "role": 3
}
``` 


#### Config
* /libraries  
  `role 1 - GET,POST,PUT,DELETE,PATCH`     
  `role 2 - GET`   
  `role 3 - GET`
* /authors  
  `role 1 - GET,POST,PUT,DELETE,PATCH`   
  `role 2 - GET,PATCH,POST`   
  `role 3 - GET`
* /books  
  `role 1 - GET,POST,PUT,DELETE,PATCH`   
  `role 2 - GET,PATCH,POST`   
  `role 3 - GET`
* /genres  
  `role 1 - GET,POST,PUT,DELETE,PATCH`   
  `role 2 - GET,PATCH,POST`   
  `role 3 - GET`
* /books-genres      
  `role 1 - GET,POST,PUT,DELETE,PATCH`   
  `role 2 - GET,PATCH,POST`   
  `role 3 - GET`