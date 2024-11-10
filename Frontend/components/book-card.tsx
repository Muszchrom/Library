import Link from "next/link";
import Image from "next/image";
import Score from "./score";
import { Book } from "@/interfaces";

export default function BookCard({bookData}: {bookData: Book}) {
  const baseUrl = "/book";
  const temp_cover = "https://static01.helion.com.pl/global/okladki/vbig/arcapi.jpg"
  {/*bookData.coverURL  */} 
  // 176 - 240
  return (
    <div className="w-full h-full flex flex-col">
      <Link href={baseUrl + "/" + bookData.id}>
        <Image className="rounded-md w-full" alt="" height={100} width={176} src={temp_cover} />
      </Link>
      <h3 className="font-medium leading-none tracking-tight px-1 pt-2">
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
