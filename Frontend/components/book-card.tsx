import Link from "next/link";
import Image from "next/image";
import Score from "./score";
import { Book } from "@/interfaces";

export default async function BookCard({bookData}: {bookData: Book}) {
  const baseUrl = "/book";
  const coverUrl = await (async () => {
    const coverNotFound = process.env.GATEWAY_URL + "waz/media/covers/default_cover.jpg"

    if (!bookData.cover_book) return coverNotFound;
    const x = bookData.cover_book.split(":")[2]; // split into 3 parts, http, domain, path
    const url = process.env.GATEWAY_URL + "waz"  + x.substring(x.indexOf("/")); // remove port
    const y = await fetch(url, {method: "HEAD"})
    return y.status == 200 ? url : coverNotFound
  })()
  {/*bookData.coverURL  */} 
  // 176 - 240
  return (
    <div className="w-full h-full flex flex-col">
      <div className="w-40 h-56 overflow-hidden border-md">
        <Link href={baseUrl + "/" + bookData.id} className="w-full h-full flex items-center justify-center relative ">
          <Image 
            className="rounded-md w-full h-full object-contain relative z-10" 
            alt="" 
            height={224} 
            width={160} 
            src={coverUrl} />
          <div className="w-full h-full object-cover absolute top-0 bottom-0 z-0 rounded-md overflow-hidden">
            <Image className="w-auto h-auto object-cover blur-md" alt="" fill={true} quality={1} sizes="1vw" src={coverUrl} />
          </div>
        </Link>
      </div>
      <h3 className="font-medium leading-none tracking-tight px-1 pt-2 break-words">
        {bookData.title}
      </h3>
      <div className="flex justify-between mt-auto px-1 pb-2">
        <Score score={bookData.rating || 4.5} />
        {/* Or maybe genre? Since avaliability is dependent on library */}
        {/* Availablitity in current library */}
        <div className="overflow-auto">
          <span className="px-2 py-0.5 bg-primary text-secondary rounded-full text-sm">
            +99 km
          </span>
        </div>
      </div>
    </div>
  )
}
