"use client"
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import Image from "next/image";
import magglass from "@/components/svg/magglass.svg";
import { Author, Book, Genre } from "@/interfaces";
import React, { useEffect, useRef, useState } from "react";
import BookCard from "./book-card-client";
import BookCardSkeleton from "./book-card-skeleton";
import { Label } from "@/components/ui/label";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogOverlay, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Command, CommandEmpty, CommandInput, CommandItem, CommandList } from "@/components/ui/command";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import { Check, ChevronsUpDown } from "lucide-react";
import { CommandGroup } from "cmdk";
import { cn } from "@/lib/utils";
import AuthorSelect from "./author-select";
import GenreSelect from "./genre-select";
import RatingSelect from "./rating-select";



export default function BrowseBooksPage() {
  const [loading, setLoading] = useState(true);
  const [books, setBooks] = useState<Book[]>([]);
  const [inputValue, setInputValue] = useState("");

  const [search, setSearch] = useState("");
  const [filters, setFilters] = useState("");

  useEffect(() => {
    (async () => {
      const url = "http://localhost:8081/waz/books/?" + (search.length ? search : "") + "&" + filters;
      const res = await fetch(url);
      setLoading(false);
      if (res.status !== 200) return setBooks([]);
      const bks: Book[] = await res.json();
      setBooks(bks.slice(0, 30));
    })();
  }, [search, filters]);

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
          <Filters onSubmit={setFilters}/>
          {/* <Button variant={"outline"}>Filtry - 12</Button> */}
          {/* <Button variant={"outline"}>Malejąco</Button> */}
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

function Filters({onSubmit}: {onSubmit: (filter: string) => void}) {
  const [open, setOpen] = useState(false);
  const [authors, setAuthors] = useState<Author[]>([]);
  const [genres, setGenres] = useState<Genre[]>([]);
  const [ratings, setRatings] = useState<number[]>([]);

  const [selectedAuthor, setSelectedAuthor] = useState<number | undefined>(undefined);
  const [selectedGenre, setSelectedGenre] = useState<string | undefined>(undefined);
  const [selectedRating, setSelectedRating] = useState<number | undefined>(undefined);

  useEffect(() => {
    (async () => {
      const res = await fetch("http://localhost:8081/waz/authors/")
      const res1 = await fetch("http://localhost:8081/waz/genres/")
      const authors_ = await res.json();
      const genres_ = await res1.json();
      setAuthors(authors_);
      setGenres(genres_);
      const temp = [];
      for (let i=5; i>=0; i-=0.5) {
        temp.push(i);
      }
      setRatings(temp);
    })();
  }, []);

  const resetFilters = () => {
    setSelectedAuthor(undefined);
    setSelectedGenre(undefined);
    setSelectedRating(undefined);
  }

  const handleClick = () => {
    const f = (selectedAuthor ? "author=" + encodeURIComponent(selectedAuthor) + "&" : "") +
              (selectedGenre ? "genre=" + encodeURIComponent(selectedGenre) + "&" : "") +
              (selectedRating ? "rating=" + encodeURIComponent(selectedRating) : "");
    onSubmit(f);
    setOpen(!open);
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline">Filtry {(selectedAuthor ? 1 : 0) + (!!selectedGenre ? 1 : 0) + (selectedRating !== undefined ? 1 : 0)}</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Wybierz filtry</DialogTitle>
          <DialogDescription>
            Make changes to your profile here. Click save when you're done.
          </DialogDescription>
        </DialogHeader>
        <div className="flex flex-col">
          <span className="ml-2 mb-1">Autor</span>
          <AuthorSelect authors={authors} value={selectedAuthor} onValueChange={setSelectedAuthor}/>
          <span className="ml-2 mb-1">Gatunek</span>
          <GenreSelect genres={genres} value={selectedGenre} onValueChange={setSelectedGenre} />
          <span className="ml-2 mb-1">Ocena</span>
          <RatingSelect ratings={ratings} value={selectedRating} onValueChange={setSelectedRating}/>
          {/* <AuthorSelect authors={authors}/> */}
        </div>
        <div className="flex justify-between">
          <Button variant="secondary" onClick={resetFilters}>Wyczyść filtry</Button>
          <Button variant="default" className="min-w-[100px]" onClick={handleClick}>Ok</Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}

