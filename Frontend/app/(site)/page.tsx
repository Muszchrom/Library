import BooksRow from "@/components/books-row";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { commonBookGenres } from "../raw-dev-data";
import { Book, CommonBookGenres } from "@/interfaces";


export default async function Home() {
  const res = await fetch(process.env.GATEWAY_URL + "waz/books/");
  const images: Book[] = await res.json();
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

