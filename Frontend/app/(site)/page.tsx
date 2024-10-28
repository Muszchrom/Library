import BooksRow from "@/components/books-row";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";
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

export default function Home() {
  return (
    <div className="flex flex-col gap-2">
      <BooksRow bookDataArray={images} title="Zawsze najlepsze"/>

      <HomepageRowV2 genres={commonBookGenres}></HomepageRowV2>

      <BooksRow bookDataArray={images} title="Najlepsze w okolicy"/>

      <BooksRow bookDataArray={images} title="Najlepsze w ostatnim czasie"/>
    </div>
  );
}

function HomepageRowV2({genres}: {genres: CommonBookGenres[]}) {
  return (
    <div className="flex gap-2 overflow-auto py-2">
      {genres.map((genre) => (
        <Card key={genre.id} className="h-36 aspect-square">
          <CardHeader className="flex items-center justify-center h-full w-30">
            <CardTitle>
              {genre.name}
            </CardTitle>
          </CardHeader>
        </Card>
      ))}
    </div>
  )
}

