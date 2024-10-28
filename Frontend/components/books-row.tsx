import { Separator } from "@radix-ui/react-separator";
import BookCard from "./book-card";
import { BookData } from "@/interfaces";


export default function BooksRow({bookDataArray, title}: {bookDataArray: BookData[], title: string}) {
  return (
    <div className="flex flex-col gap-2">
      <h2 className="text-2xl pt-2 leading-none">{title}</h2>
      <Separator orientation="horizontal" className="mb-1"/>
      <div className="flex gap-2 overflow-auto">
        {bookDataArray.map((bookData) => 
            <BookCard key={bookData.id} bookData={bookData}></BookCard>
        )}
      </div>
    </div>
  )
}
