"use client"
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import Image from "next/image";
import magglass from "@/components/svg/magglass.svg";
import { Book } from "@/interfaces";
import { useEffect, useState } from "react";
import BookCard from "./book-card-client";
import BookCardSkeleton from "./book-card-skeleton";



export default function BrowseBooksPage() {
  const [books, setBooks] = useState<Book[]>([]);

  useEffect(() => {
    (async () => {
      const res = await fetch("http://localhost:8081/" + "waz/books/");
      const bks: Book[] = await res.json();
      setBooks(bks.slice(0, 30));
    })();
  }, []);

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
        
        {books.length ? books.map((book) => (
          <BookCard key={book.id} bookData={book}/>
        )) : Array.from(Array(10).keys()).map((i) => (
          <BookCardSkeleton key={i}/>
        ))}
      </div>
    </>
  );
}