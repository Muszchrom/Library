import Image from "next/image";
import Score from "@/components/score";
import { Button } from "@/components/ui/button";
import BooksRow from "@/components/books-row";
import { Book, BookData } from "@/interfaces";
import LibrariesList from "./libraries-list";

export default async function Page({ params }: { params: { book: number }}) {
  const res = await fetch(process.env.GATEWAY_URL + "waz/books/" + params.book + "/");
  const image: Book = await res.json();

  const res2 = await fetch(process.env.GATEWAY_URL + "waz/books/");
  const books: Book[] = await res2.json();

  return (
    <>
      <div className="flex gap-4">
        <div className="flex-shrink-0 flex-grow-0 basis-40">
          <Image className="rounded-md" alt="" height={252} width={160} src={image.cover_book} />
        </div>
        <div>
          <h2 className="text-xl font-semibold tracking-tight">{image.title}</h2>
          <Score score={image.rating || 0}/>
          <p className="text-muted-foreground text-sm leading-tight">
            {image.description}
          </p>
        </div>
      </div>
      <LibrariesList bookId={params.book}/>
      <div className="my-4"></div>
      <BooksRow books={books} title="Podobne książki" />
      <div className="my-4"></div>
    </>
  );
}

// function LibrariesList() {
//   return (
//     <div className="flex flex-col gap-4 mt-4">
//       <div className="flex gap-4">
//         <Button variant={"outline"}>Odległość 👇</Button>
//         <Button variant={"outline"}>Domyślnie 👇</Button>
//         <Button variant={"outline"}>Dostawa ✅</Button>
//       </div>
//       <LibraryCard />
//       <LibraryCard />
//       <LibraryCard />
//       <LibraryCard />
//       <LibraryCard />
//     </div>
//   )
// }

// function LibraryCard() {
//   return (
//     <div className="rounded-xl border bg-card text-card-foreground shadow">
//       <div className="flex p-4 justify-between">
//         <div className="flex flex-col justify-between gap-2">
//           <h3 className="font-semibold leading-none tracking-tight">Miejska Biblioteka Publiczna im. H. Łopacińskiego Filia nr 25</h3>
//           <p className="text-sm text-muted-foreground">Sympatyczna 16, 20-530 Lublin</p>
//         </div>
//         <div className="flex flex-col justify-between gap-2">
//           <span className="text-right text-sm text-muted-foreground leading-none">
//             +99 km
//           </span>
//           <Button>Wybierz</Button>
//         </div>
//       </div>
//     </div>
//   );
// }