import Score from "@/components/score";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import Image from "next/image";
import Link from "next/link";

export interface ImageData {
  id: number,
  title: string,
  available: boolean,
  user_score: number,
  coverURL: string
}

export interface CommonBookGenres {
  id: number,
  name: string
}

export const images: ImageData[] = [
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

export const commonBookGenres: CommonBookGenres[] = [
  { id: 1, name: "Fiction" },
  { id: 2, name: "Non-fiction" },
  { id: 3, name: "Mystery" },
  { id: 4, name: "Romance" },
  { id: 5, name: "Fantasy" },
];

export default function Home() {
  return (
    <div className="flex flex-col gap-2">
      <HomepageRow images={images} title="Zawsze najlepsze"/>

      <HomepageRowV2 genres={commonBookGenres}></HomepageRowV2>

      <HomepageRow images={images} title="Najlepsze w okolicy"/>

      <HomepageRow images={images} title="Najlepsze w ostatnim czasie"/>
    </div>
  );
}

function HomepageRowV2({genres}: {genres: CommonBookGenres[]}) {
  return (
    <div className="flex gap-2 overflow-auto py-2">
      {genres.map((genre) => (
        <Card key={genre.id} className="h-36 aspect-square">
          <CardHeader className="flex items-center justify-center h-full w-30">
            <CardTitle>
              {genre.name}
            </CardTitle>
          </CardHeader>
        </Card>
      ))}
    </div>
  )
}

export function HomepageRow({images, title}: {images: ImageData[], title: string}) {
  return (
    <div className="flex flex-col gap-2">
      <h2 className="text-2xl pt-2 leading-none">{title}</h2>
      <Separator orientation="horizontal" className="mb-1"/>
      <div className="flex gap-2 overflow-auto">
        {images.map((image) => 
            <BookCard key={image.id} image={image}></BookCard>
        )}
      </div>
    </div>
  )
}


function BookCard({image}: {image: ImageData}) {
  const baseUrl = "/books";
  return (
    <div className="min-w-44">
      <Link href={baseUrl + "/" + image.id}>
        <Image className="rounded-md" alt="" height={100} width={176} src={image.coverURL} />
      </Link>
      <div className="px-1 py-2">
        <h3 className="font-medium leading-none tracking-tight">
          {image.title}
        </h3>
        <div className="flex justify-between">
          <Score score={image.user_score} />
          {/* Or maybe genre? Since avaliability is dependent on library */}
          {/* Availablitity in current library */}
          <div className="overflow-auto">
            <span className="px-2 py-0.5 bg-primary text-secondary rounded-full text-sm">
              +99 km
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}