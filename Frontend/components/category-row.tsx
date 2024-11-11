import { ScrollArea, ScrollBar } from "./ui/scroll-area";
import { Genre } from "@/interfaces";

export default async function CategoryRow() {
  const res = await fetch(process.env.GATEWAY_URL + "waz/genres/");
  const genres: Genre[] = await res.json();
  return (
    <ScrollArea>
      <div className="flex w-max space-x-2">
        {genres.map((genre) => {
          return (
            <div className="aspect-square h-36 border rounded-lg flex items-center justify-center p-4">
              <span className="text-center">{genre.genre}</span>
            </div>
          )
        })}
      </div>
      <ScrollBar orientation="horizontal" />
    </ScrollArea>
  );
}