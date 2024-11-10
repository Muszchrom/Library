import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import Image from "next/image";
import magglass from "@/components/svg/magglass.svg";
import BookCard from "@/components/book-card";
import { images } from "@/app/raw-dev-data";
import { Book } from "@/interfaces";

export default async function BrowseBooksPage() {
  const res2 = await fetch(process.env.GATEWAY_URL + "waz/books/");
  const books: Book[] = await res2.json();

  return (
    <>
      <div className="relative">
        <Image alt="" src={magglass} className="absolute w-5 left-2 top-1/2 transform -translate-y-1/2"/>
        <Input className="pl-8"/>
      </div>
      <div className="flex justify-between items-center">
        <span className="font-bold">420 Wynikow</span>
        <div className="flex gap-3">
          <Button variant={"outline"}>Filtry - 12</Button>
          <Button variant={"outline"}>Malejąco</Button>
        </div>
      </div>
      <div className="grid gap-2 grid-cols-[repeat(auto-fill,minmax(10rem,1fr))]"> {/*flex flex-wrap gap-2 */}
        {books.map((book) => (
          <BookCard bookData={book}/>
        ))}
      </div>
    </>
  );
}