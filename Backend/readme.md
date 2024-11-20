
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

**Retrieve all books** with optional filters.

- **Optional Query Parameters**:
  - `genre`: Filter by genre name.
  - `author`: Filter by author name (format: `First Last`) or author ID.
  - `rating`: Filter by book rating.
  - `title`: Search for books by title using fuzzy matching.
  - `search`: Search for books by title or author (fuzzy matching).

- **Example**:
  ```bash
  GET /books/?genre=Fantasy&rating=4.5&search=John Smith
  ```

- **Response**:
  ```json
  [
      {
          "id": 1,
          "author": 2,
          "isbn": "1234567890",
          "isbn13": "1234567890123",
          "title": "Fantasy World",
          "description": "A magical journey.",
          "publication_date": "2023-01-01",
          "rating": 4.5,
          "cover_book": "/media/covers/fantasy_world.jpg"
      }
  ]
  ```

#### **POST /books/**

**Create a new book** in the database.

- **Required Fields**:
  - `title`: Title of the book.
  - `author`: ID of the author.
  - `rating`: Rating of the book.

- **Example**:
  ```bash
  POST /books/
  {
      "title": "Mystery Novel",
      "author": 1,
      "isbn": "0987654321",
      "isbn13": "0987654321098",
      "description": "An intriguing mystery story.",
      "publication_date": "2024-01-01",
      "rating": 4.0
  }
  ```

- **Validation**:
  - `isbn` must be 10 characters.
  - `isbn13` must be 13 characters.
  - `rating` must be between 1.0 and 5.0 in 0.5 steps.
  - A book with the same `isbn` and `author` cannot already exist.

#### **POST /books/{id}/upload-cover/**

**Upload a cover image** for a specific book.

- **Example**:
  ```bash
  POST /books/1/upload-cover/
  Content-Type: multipart/form-data
  File: cover.jpg
  ```

- **Response**:
  ```json
  {
      "id": 1,
      "title": "Fantasy World",
      "cover_book": "/media/covers/cover.jpg"
  }
  ```

#### **POST /books/{id}/library/{library_id}/rent/**

**Rent a book from a specific library**.

- **Path Parameters**:
  - `id`: ID of the book to rent.
  - `library_id`: ID of the library.

- **Headers**:
  - `X-role-id`: User role and ID in the format `"role user_id"`. Example: `"3 1"`.

- **Example**:
  ```bash
  POST /books/1/library/2/rent/
  X-role-id: "3 10"
  ```

- **Response**:
  ```json
  {
      "message": "Book 'Fantasy World' successfully rented from 'Central Library'.",
      "rental_status": "Rented",
      "rental_date": "2024-11-20",
      "due_date": "2024-12-04"
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