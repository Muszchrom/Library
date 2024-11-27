import Image from "next/image";
import Score from "@/components/score";
import BooksRow from "@/components/books-row";
import { Book } from "@/interfaces";
import LibrariesList from "./libraries-list";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";

export default async function Page({ params }: { params: { book: string }}) {
  const session = await getServerSession(authOptions);

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
      <LibrariesList bookId={parseInt(params.book)} token={session?.user.APIToken}/>
      <div className="my-4"></div>
      <BooksRow books={books} title="Podobne książki" />
      <div className="my-4"></div>
    </>
  );
}