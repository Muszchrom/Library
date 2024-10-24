"use client"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import clsx from "clsx";
import Image from "next/image";

interface ImageData {
  id: number,
  title: string,
  available: boolean,
  user_score: number,
  coverURL: string
}

const images: ImageData[] = [
  {
    id: 1,
    title: "Architektura API",
    available: true,
    user_score: 4.5,
    coverURL: "https://static01.helion.com.pl/global/okladki/vbig/arcapi.jpg"
  },
  {
    id: 2,
    title: "Architektura API",
    available: false,
    user_score: 4.5,
    coverURL: "https://static01.helion.com.pl/global/okladki/vbig/arcapi.jpg"
  },
  {
    id: 3,
    title: "Architektura API",
    available: true,
    user_score: 4.5,
    coverURL: "https://static01.helion.com.pl/global/okladki/vbig/arcapi.jpg"
  },
  {
    id: 4,
    title: "Architektura API",
    available: true,
    user_score: 4.5,
    coverURL: "https://static01.helion.com.pl/global/okladki/vbig/arcapi.jpg"
  },
  {
    id: 5,
    title: "Architektura API",
    available: true,
    user_score: 4.5,
    coverURL: "https://static01.helion.com.pl/global/okladki/vbig/arcapi.jpg"
  },
]

const commonBookGenres = [
  "Fiction",
  "Non-fiction",
  "Mystery",
  "Romance",
  "Fantasy",
];

export default function Home() {
  return (
    <div className="flex flex-col gap-2">
      <HomepageRow images={images} title="Zawsze najlepsze"/>

      <HomepageRowV2 genres={commonBookGenres}></HomepageRowV2>

      <HomepageRow images={images} title="Zawsze najlepsze"/>

      <HomepageRow images={images} title="Zawsze najlepsz"/>
    </div>
  );
}

function HomepageRowV2({genres}: {genres: string[]}) {
  return (
    <div className="flex gap-2 overflow-auto">
      {genres.map((genre) => (
        <Card className="h-36 aspect-square">
          <CardHeader className="flex items-center justify-center h-full w-30">
            <CardTitle>
              {genre}
            </CardTitle>
          </CardHeader>
        </Card>
      ))}
    </div>
  )
}

function HomepageRow({images, title}: {images: ImageData[], title: string}) {
  return (
    <div>
      <h2 className="text-2xl py-2">{title}</h2>
      <div className="flex gap-2 overflow-auto">
        {images.map((image) => {
            return <BookCard key={image.id} image={image}></BookCard>
          })}
      </div>
    </div>
  )
}


function BookCard({image}: {image: ImageData}) {
  return (
    <div className="min-w-40">
      <Image className="rounded-md" alt="" height={100} width={160} src={image.coverURL} />
      <div className="px-1 py-2">
        <h3 className="font-medium leading-none tracking-tight">
          {image.title}
        </h3> 
        <Score score={image.user_score} />
        <span className={clsx(
          "px-2 py-0.5 bg-primary text-secondary rounded-full text-sm",
          // image.available && bg-
        )}>
          {image.available ? "Dostępna" : "Niedostępna"}
        </span>
      </div>
    </div>
  )
}

function Score({score}: {score: number}) {
  return (
    <div>
      {Array.from(Array(Math.floor(score)).keys()).map((sc) => 
        <span className="text-sm">⭐</span>
      )}
      {!!(score - Math.floor(score)) && (
        <span className="relative text-sm">
          ⭐
          <div className="absolute top-0 bottom-0 right-0 left-1/2 bg-background"></div>
        </span>
      )}
    </div>
  )
}