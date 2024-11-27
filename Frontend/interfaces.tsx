export interface Book {
  id: number,
  isbn: string,
  isbn13: string,
  title: string,
  description: string,
  publication_date: string,
  rating: null | number,
  cover_book: string,
  author: number
}

export interface Rental {
  id: number,
  user_id: number,
  rental_status: "Pending" | "Rented" | "Returned",
  rental_date: string,
  due_date: string,
  return_date: string,
  book: number,
  library: number
}

export interface User {
  id: number,
  username: string,
  email: string,
  phone: number,
  role: number
}

export interface Library {
  id: number,
  library_name: string,
  city: string,
  latitude: string,
  longitude: string
}

export interface LibraryDistance {
  id: number,
  library_name: string,
  city: string,
  distance: number
}

export interface Genre {
  id: number,
  genre: string
}

export interface Author {
  first_name: string,
  second_name: string,
  id: number
}

export interface BookData {
  id: number,
  title: string,
  available: boolean,
  user_score: number,
  coverURL: string
}

export interface CommonBookGenres {
  id: number,
  name: string
}
