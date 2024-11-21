import Link from "next/link";
import { ScrollArea, ScrollBar } from "./ui/scroll-area";
import { Genre } from "@/interfaces";

export default async function CategoryRow() {
  const res = await fetch(process.env.GATEWAY_URL + "waz/genres/");
  const genres: Genre[] = await res.json();
  return (
    <ScrollArea>
      <div className="flex w-max space-x-2 pb-3">
        {genres.map((genre) => {
          return (
            <Link 
              className="aspect-square h-36 border rounded-lg flex items-center justify-center p-4 cursor-pointer text-center"
              key={genre.id}
              href={"/books/browse?genre=" + genre.genre}>
                {genre.genre}
            </Link>
          )
        })}
      </div>
      <ScrollBar orientation="horizontal"/>
    </ScrollArea>
  );
}