```markdown
# **Library Management API**

## **Overview**

This API allows users to interact with libraries, books, authors, genres, and rentals. It provides filtering, searching, and operations like renting and returning books.

---

## **Endpoints**

### **Libraries**

#### **GET /libraries/**

Retrieve all libraries.

- **Optional Query Parameters**:
  - `city`: Filter libraries by city.
  - `latitude`: User's latitude.
  - `longitude`: User's longitude.
  - `book`: Filter libraries by book availability.

- **Example**:
  ```bash
  GET /libraries/?city=SampleCity&latitude=51.246452&longitude=22.568446
  ```

- **Response**:
  ```json
  [
      {
          "id": 1,
          "library_name": "Central Library",
          "city": "Sample City",
          "distance": 2.5
      }
  ]
  ```

#### **POST /libraries/**

Create a new library.

- **Required Fields**:
  - `library_name`: Name of the library.
  - `city`: City where the library is located.
  - `latitude`: Latitude of the library.
  - `longitude`: Longitude of the library.

- **Example**:
  ```bash
  POST /libraries/
  {
      "library_name": "Central Library",
      "city": "Sample City",
      "latitude": 51.246452,
      "longitude": 22.568446
  }
  ```

---

### **Authors**

#### **GET /authors/**

Retrieve all authors.

#### **POST /authors/**

Create a new author.

- **Required Fields**:
  - `first_name`: Author's first name.
  - `second_name`: Author's last name.

- **Example**:
  ```bash
  POST /authors/
  {
      "first_name": "John",
      "second_name": "Doe"
  }
  ```

- **Response**:
  ```json
  {
      "id": 1,
      "first_name": "John",
      "second_name": "Doe"
  }
  ```

---

### **Books**

#### **GET /books/**

Retrieve all books.

- **Optional Query Parameters**:
  - `genre`: Filter books by genre.
  - `author`: Filter books by author name or ID.
  - `rating`: Filter books by rating.
  - `title`: Search for books by title (fuzzy matching).
  - `search`: Search for books by title or author (fuzzy matching).

- **Example**:
  ```bash
  GET /books/?genre=Fantasy&rating=4.5
  ```

#### **POST /books/**

Create a new book.

- **Required Fields**:
  - `title`: Title of the book.
  - `author`: ID of the author.
  - `rating`: Rating of the book.

- **Example**:
  ```bash
  POST /books/
  {
      "title": "Fantasy World",
      "author": 1,
      "rating": 4.5
  }
  ```

---

### **Genres**

#### **GET /genres/**

Retrieve all genres.

- **Optional Query Parameters**:
  - `id`: Filter by genre ID.
  - `genre`: Filter by genre name.

#### **POST /genres/**

Create a new genre.

- **Required Fields**:
  - `genre`: Name of the genre.

- **Example**:
  ```bash
  POST /genres/
  {
      "genre": "Fantasy"
  }
  ```

---

### **Library Books**

#### **POST /library-books/**

Add a book to a library.

- **Required Fields**:
  - `book`: ID of the book.
  - `library`: ID of the library.
  - `book_count`: Number of available copies.

- **Example**:
  ```bash
  POST /library-books/
  {
      "book": 1,
      "library": 2,
      "book_count": 10
  }
  ```

---

### **Rentals**

#### **GET /rental/**

Retrieve all rentals.

#### **GET /rental/{id}/**

Retrieve a specific rental.

#### **GET /rental/user/{user_id}/**

Retrieve rentals for a specific user.

#### **POST /rental/**

Rent a book.

- **Required Fields**:
  - `book_id`: ID of the book.
  - `library_id`: ID of the library.

- **Example**:
  ```bash
  POST /rental/
  {
      "book_id": 1,
      "library_id": 2
  }
  ```

#### **PUT /rental/{id}/**

Return a book.

- **Example**:
  ```bash
  PUT /rental/1/
  ```

---

### **Best-Seller Books**

#### **GET /best-sellers/**

Retrieve the top 15 highest-rated books.

---

### **Best Nearest Books**

#### **GET /best-nearest/**

Retrieve the top 25 books from the nearest 5 libraries.

- **Optional Query Parameters**:
  - `latitude`: User's latitude.
  - `longitude`: User's longitude.

- **Example**:
  ```bash
  GET /best-nearest/?latitude=51.246452&longitude=22.568446
  ```

- **Response**:
  ```json
  [
      {
          "id": 1,
          "title": "Fantasy World",
          "rating": 4.5
      }
  ]
  ```

---