import { Separator } from "@radix-ui/react-separator";
import BookCard from "./book-card";
import { Book } from "@/interfaces";
import { ScrollArea, ScrollBar } from "./ui/scroll-area";


export default function BooksRow({bookDataArray, title}: {bookDataArray: Book[], title: string}) {
  return (
    <div className="flex flex-col gap-2">
      <h2 className="text-2xl pt-2 leading-none">{title}</h2>
      <Separator orientation="horizontal" className="mb-1"/>
      <ScrollArea className="">
        <div className="flex w-max space-x-2">
          {bookDataArray.map((bookData) => 
            <div className="w-40">
              <BookCard key={bookData.id} bookData={bookData}></BookCard>
            </div>
          )}
        </div>
        <ScrollBar orientation="horizontal" />
      </ScrollArea>
      {/* <div className="flex gap-2 overflow-x-auto w-full">
      </div> */}
    </div>
  )
}
