import { Separator } from "@radix-ui/react-separator";
import BookCard from "./book-card";
import { Book } from "@/interfaces";
import { ScrollArea, ScrollBar } from "./ui/scroll-area";


export default async function BooksRow({ title }: {title: string}) {
  const res = await fetch(process.env.GATEWAY_URL + "waz/books/");
  const books: Book[] = await res.json();

  return (
    <div className="flex flex-col gap-2">
      <h2 className="text-2xl pt-2 leading-none">{title}</h2>
      <Separator orientation="horizontal" className="mb-1"/>
      <ScrollArea className="">
        <div className="flex w-max space-x-2">
          {books.map((bookData) => 
            <div className="w-40">
              <BookCard key={bookData.id} bookData={bookData}></BookCard>
            </div>
          )}
        </div>
        <ScrollBar orientation="horizontal" />
      </ScrollArea>
    </div>
  )
}
