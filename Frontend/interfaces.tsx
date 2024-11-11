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
