```markdown
# **Library Management API Overview**

## **Endpoints**

---

### **Libraries**

#### **GET /libraries/**

Retrieve all libraries.

- **Optional Query Parameters**:
  - `city`: Filter libraries by city.
  - `latitude`: User's latitude.
  - `longitude`: User's longitude.
  - `book`: Filter libraries by book availability.

- **Response**:
  ```json
  [
      {
          "id": 1,
          "library_name": "Central Library",
          "city": "Sample City",
          "distance": 2.5
      },
      ...
  ]
  ```

- **Notes**:
  - If `latitude` and `longitude` are provided, libraries are sorted by proximity.
  - If `book` is provided, filters libraries where the specified book is available.

#### **POST /libraries/**

Create a new library.

- **Required Fields**:
  - `library_name`: Name of the library.
  - `city`: City where the library is located.
  - `latitude`: Latitude of the library.
  - `longitude`: Longitude of the library.

#### **PUT /libraries/{id}/**

Update an existing library.

---

### **Authors**

#### **GET /authors/**

Retrieve all authors.

#### **POST /authors/**

Create a new author.

- **Required Fields**:
  - `first_name`: Author's first name.
  - `second_name`: Author's last name.

#### **Response**:
  - If the author already exists:
    ```json
    {
        "message": "Author John Doe already exists.",
        "id": 1,
        "first_name": "John",
        "second_name": "Doe"
    }
    ```
  - If created successfully:
    ```json
    {
        "id": 2,
        "first_name": "Jane",
        "second_name": "Smith"
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

#### **POST /books/**

Create a new book.

- **Required Fields**:
  - `title`: Title of the book.
  - `author`: ID of the author.
  - `rating`: Rating of the book.

#### **POST /books/{id}/upload-cover/**

Upload a cover image for a book.

#### **POST /books/{id}/library/{library_id}/rent/**

Rent a book from a library.

---

### **Genres**

#### **GET /genres/**

Retrieve all genres.

- **Optional Query Parameters**:
  - `id`: Filter by genre ID.
  - `genre`: Filter by genre name.

#### **POST /genres/**

Create a new genre.

- **Required Field**:
  - `genre`: Name of the genre.

---

### **Library Books**

#### **POST /library-books/**

Add a new book to a library.

- **Required Fields**:
  - `book`: ID of the book.
  - `library`: ID of the library.
  - `book_count`: Number of copies available.

#### **PUT /library-books/{id}/**

Update the number of copies available for a book in a library.

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

#### **PUT /rental/{id}/**

Return a book.

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

---

## **Key Features**

1. **Libraries**:
   - Filter libraries by city, proximity, or book availability.
   - Manage library records via CRUD operations.

2. **Authors**:
   - Create or retrieve authors.
   - Handles duplicate authors gracefully.

3. **Books**:
   - Extensive filtering options by genre, author, rating, title, or search.
   - Rent books directly from libraries.

4. **Genres**:
   - Retrieve all genres or filter by ID or name.
   - Associate genres with books.

5. **Library Books**:
   - Manage the availability of books in libraries.

6. **Rentals**:
   - Track active and past rentals.
   - Ensure users cannot rent more than two copies of the same book.

7. **Best-Sellers**:
   - Retrieve the top-rated books across all libraries.

8. **Best Nearest Books**:
   - Retrieve highly-rated books from the nearest libraries based on location.

```