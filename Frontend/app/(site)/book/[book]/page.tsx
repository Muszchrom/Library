import Score from "@/components/score";
import BooksRow from "@/components/books-row";
import { Book } from "@/interfaces";
import LibrariesList from "./libraries-list";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { gatewayClient, gatewayServer } from "@/lib/urls";

export default async function Page({ params }: { params: { book: string }}) {
  const session = await getServerSession(authOptions);

  const res = await fetch(gatewayServer + "waz/books/" + params.book + "/");
  const book: Book = await res.json();
  const x = book.cover_book.split(":")[2]; // split into 3 parts, http, domain, path
  const tempUrl = gatewayServer + "waz" + x.substring(x.indexOf("/")); // remove port
  const imageAvailable = await fetch(tempUrl, {method: "HEAD"});
  const url = imageAvailable.ok
    ? gatewayClient + "waz" + x.substring(x.indexOf("/"))
    : gatewayClient + "waz/media/covers/default_cover.jpg";

  const res2 = await fetch(gatewayServer + "waz/books/");
  const books: Book[] = await res2.json();

  return (
    <>
      <div className="flex gap-4">
        <div className="flex-shrink-0 flex-grow-0 basis-40">
          {/* <Image className="rounded-md" alt="" height={252} width={160} src={book.cover_book} /> */}
          <picture>
            <img className="rounded-md" alt={"Okładka książki " + book.title} src={url} />
          </picture>
        </div>
        <div>
          <h2 className="text-xl font-semibold tracking-tight">{book.title}</h2>
          <Score score={book.rating || 0}/>
          <p className="text-muted-foreground text-sm leading-tight">
            {book.description}
          </p>
        </div>
      </div>
      <LibrariesList bookId={parseInt(params.book)} token={session?.user.APIToken}/>
      <div className="my-4"></div>
      <BooksRow books={books.slice(0, 15)} title="Podobne książki" />
      <div className="my-4"></div>
    </>
  );
}