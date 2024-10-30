import { BookData, CommonBookGenres } from "@/interfaces";

const images: BookData[] = [
  {
    id: 1,
    title: "Architektura API",
    available: true,
    user_score: 4.5,
    coverURL: "https://static01.helion.com.pl/global/okladki/vbig/arcapi.jpg"
  },
  {
    id: 2,
    title: "Architektura API",
    available: false,
    user_score: 4.5,
    coverURL: "https://static01.helion.com.pl/global/okladki/vbig/arcapi.jpg"
  },
  {
    id: 3,
    title: "Architektura API",
    available: true,
    user_score: 4.5,
    coverURL: "https://static01.helion.com.pl/global/okladki/vbig/arcapi.jpg"
  },
  {
    id: 4,
    title: "Architektura API",
    available: true,
    user_score: 4.5,
    coverURL: "https://static01.helion.com.pl/global/okladki/vbig/arcapi.jpg"
  },
  {
    id: 5,
    title: "Architektura API",
    available: true,
    user_score: 4.5,
    coverURL: "https://static01.helion.com.pl/global/okladki/vbig/arcapi.jpg"
  },
]

const commonBookGenres: CommonBookGenres[] = [
  { id: 1, name: "Fiction" },
  { id: 2, name: "Non-fiction" },
  { id: 3, name: "Mystery" },
  { id: 4, name: "Romance" },
  { id: 5, name: "Fantasy" },
];

export { images, commonBookGenres };