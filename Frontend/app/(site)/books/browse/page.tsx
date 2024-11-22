"use client"
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import Image from "next/image";
import magglass from "@/components/svg/magglass.svg";
import { Book } from "@/interfaces";
import React, { useEffect, useState } from "react";
import BookCard from "./book-card-client";
import BookCardSkeleton from "./book-card-skeleton";
import { Label } from "@/components/ui/label";



export default function BrowseBooksPage() {
  const [loading, setLoading] = useState(true);
  const [books, setBooks] = useState<Book[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [search, setSearch] = useState("");

  useEffect(() => {
    (async () => {
      const url = "http://localhost:8081/waz/books/?" + (search.length ? search : "") + "&"
      const res = await fetch(url);
      setLoading(false);
      if (res.status !== 200) return setBooks([]);
      const bks: Book[] = await res.json();
      console.log(bks);
      setBooks(bks.slice(0, 30));
    })();
  }, [search]);

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.length === 0) return setSearch("");
    setSearch("title=" + encodeURIComponent(inputValue));
  }

  return (
    <>
      <form onSubmit={handleFormSubmit} className="flex flex-col gap-2">
        <Label>Wyszukaj tytuł</Label>
        <div className="flex gap-2 relative" >
          <Image alt="" src={magglass} className="absolute w-5 left-2 top-1/2 transform -translate-y-1/2"/>
          <Input className="pl-8" type="text" value={inputValue} onChange={(e) => setInputValue(e.target.value)}/>
          <Button type="submit">Szukaj</Button>
        </div>
      </form>
      <div className="flex justify-between items-center">
        <span className="">{books.length} Wyników</span>
        <div className="flex gap-3">
          <Button variant={"outline"}>Filtry - 12</Button>
          <Button variant={"outline"}>Malejąco</Button>
        </div>
      </div>
      <div className="grid gap-2 grid-cols-[repeat(auto-fill,minmax(10rem,1fr))]"> {/*flex flex-wrap gap-2 */}
        
        {!loading ? (
            books.length ? books.map((book) => (
              <BookCard key={book.id} bookData={book}/>
            )) : <span>Brak wyników</span>
          ) : (
            Array.from(Array(10).keys()).map((i) => (
              <BookCardSkeleton key={-i}/>
            ))
          )}
      </div>
    </>
  );
}