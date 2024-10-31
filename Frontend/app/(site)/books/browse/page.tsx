import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";
import Image from "next/image";
import magglass from "@/components/svg/magglass.svg";
import { BookCardExperimental } from "@/components/book-card";
import { images } from "@/app/raw-dev-data";

export default function BrowseBooksPage() {
  return (
    <>
      <Separator orientation="horizontal"/>
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
      <div className="flex flex-wrap gap-2">
        <BookCardExperimental bookData={images[1]}/>
        <BookCardExperimental bookData={images[1]}/>
        <BookCardExperimental bookData={images[1]}/>
        <BookCardExperimental bookData={images[1]}/>
        <BookCardExperimental bookData={images[1]}/>
        <BookCardExperimental bookData={images[1]}/>
        <BookCardExperimental bookData={images[1]}/>
        <BookCardExperimental bookData={images[1]}/>
        <BookCardExperimental bookData={images[1]}/>
        <BookCardExperimental bookData={images[1]}/>
        <BookCardExperimental bookData={images[1]}/>
      </div>
    </>
  );
}