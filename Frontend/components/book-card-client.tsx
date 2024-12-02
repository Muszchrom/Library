"use client";
import Score from "@/components/score";
import { Skeleton } from "@/components/ui/skeleton";
import { Book, Genre } from "@/interfaces";
import { gatewayClient } from "@/lib/urls";
import Link from "next/link";
import { useEffect, useState } from "react";

export default function BookCard({bookData}: {bookData: Book}) {
  const [coverUrl, setCoverUrl] = useState("");
  const [genre, setGenre] = useState("Ładuję ...");
  
  useEffect(() => {
    (async () => {
      const coverNotFound = gatewayClient + "waz/media/covers/default_cover.jpg";
      if (!bookData.cover_book) return setCoverUrl(coverNotFound);

      const x = bookData.cover_book.split(":")[2]; // split into 3 parts, http, domain, path
      const url = gatewayClient + "waz"  + x.substring(x.indexOf("/")); // remove port
      const y = await fetch(url, {method: "HEAD"});
      if (y.status == 200) return setCoverUrl(url);
      else setCoverUrl(coverNotFound);
    })();
  }, [bookData]);

  useEffect(() => {
    (async () => {
      const res = await fetch(gatewayClient + "waz/book-genres/?bookId=" + bookData.id);
      if (res.status !== 200) return;
      const genres = await res.json();
      if (!genres.length || genres[0].genre === undefined) return;
      const res2 = await fetch(gatewayClient + "waz/genres/" + genres[0].genre + "/");
      if (res2.status !== 200) return;
      const genre_: Genre = await res2.json();
      setGenre(genre_.genre)
    })();
  }, [bookData]);

  const baseUrl = "/book";

  {/*bookData.coverURL  */} 
  // 176 - 240
  return (
    <div className="flex flex-col h-full">
      <div className=" border-md">
        <Link href={baseUrl + "/" + bookData.id} className="w-full h-56 flex items-center justify-center relative ">
          {coverUrl.length !== 0 && (
            <>
              <div className="w-full h-full object-cover absolute top-0 bottom-0 rounded-md overflow-hidden z-[1]">
                {/* alt empty since its purely decorative thing */}
                <picture>
                  <img className="min-w-full min-h-full object-cover blur-md" alt="" src={coverUrl} />
                </picture>
              </div>
              <div className="w-40 h-56">
                <picture>
                  <img 
                    className="rounded-md w-full h-full object-contain relative z-[1]" 
                    alt={"Zdjęcie okładki książki pt. " + bookData.title} 
                    height={224} 
                    width={160} 
                    src={coverUrl} />
                </picture>
              </div>
            </>
           )}
           <div className="w-full h-56 absolute">
            <Skeleton className="w-full h-full"/>
          </div>
        </Link>
      </div>
      <h3 className="font-medium max-w-[164px] leading-none tracking-tight px-1 pt-2 break-words line-clamp-2">
        {bookData.title}
      </h3>
      <div className="flex justify-between gap-2 items-center mt-auto px-1 pb-2">
        <Score score={bookData.rating || 4.5} />
        {/* Or maybe genre? Since avaliability is dependent on library */}
        {/* Availablitity in current library */}
        <div className="px-2 py-0.5 bg-primary text-secondary rounded-full text-sm w-fit"> {/**max-w-16 */}
          <span className="line-clamp-1 break-all max-w-[64px]">
            {genre}
          </span>
        </div>
      </div>
    </div>
  )
}
