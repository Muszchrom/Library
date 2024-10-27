import Image from "next/image";
import Score from "@/components/score";
import { Button } from "@/components/ui/button";
import BooksRow from "@/components/books-row";
import { BookData } from "@/interfaces";


// const libraries = [
//   {
//     name: "",
//     localization: {
//       city: "",
//       street: ""
//     }
//   }
// ]

const images: BookData[] = [
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

export default function Page({ params }: { params: { book: number }}) {
  const image = images[params.book];
  return (
    <>
      <div className="flex gap-4">
        <div className="flex-shrink-0 flex-grow-0 basis-40">
          <Image className="rounded-md" alt="" height={252} width={160} src={image.coverURL} />
        </div>
        <div>
          <h2 className="text-xl font-semibold tracking-tight">{image.title}</h2>
          <Score score={image.user_score}/>
          <p className="text-muted-foreground text-sm leading-tight">
            Jeśli dopiero zaczynasz swoją przygodę z tworzeniem API, książka &quot;Architektura API&quot;
            to doskonałe miejsce do rozpoczęcia nauki. Autorzy w przystępny sposób tłumaczą 
            złożone zagadnienia związane z projektowaniem i implementacją interfejsów API. 
            Znajdziesz tu wiele praktycznych przykładów i wskazówek, które pomogą Ci szybko 
            opanować podstawy i stworzyć swoje pierwsze API.
          </p>
        </div>
      </div>
      <LibrariesList />
      <div className="my-4"></div>
      <BooksRow bookDataArray={images} title="Podobne książki" />
      <div className="my-4"></div>
    </>
  );
}

function LibrariesList() {
  return (
    <div className="flex flex-col gap-4 mt-4">
      <div className="flex gap-4">
        <Button variant={"outline"}>Odległość 👇</Button>
        <Button variant={"outline"}>Domyślnie 👇</Button>
        <Button variant={"outline"}>Dostawa ✅</Button>
      </div>
      <LibraryCard />
      <LibraryCard />
      <LibraryCard />
      <LibraryCard />
      <LibraryCard />
    </div>
  )
}

function LibraryCard() {
  return (
    <div className="rounded-xl border bg-card text-card-foreground shadow">
      <div className="flex p-4 justify-between">
        <div className="flex flex-col justify-between gap-2">
          <h3 className="font-semibold leading-none tracking-tight">Miejska Biblioteka Publiczna im. H. Łopacińskiego Filia nr 25</h3>
          <p className="text-sm text-muted-foreground">Sympatyczna 16, 20-530 Lublin</p>
        </div>
        <div className="flex flex-col justify-between gap-2">
          <span className="text-right text-sm text-muted-foreground leading-none">
            +99 km
          </span>
          <Button>Wybierz</Button>
        </div>
      </div>
    </div>
  );
}