export interface Book {
  id: number,
  isbn: string,
  isbn13: string,
  title: string,
  description: string,
  publication_date: string,
  rating: null | number,
  author: number
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
