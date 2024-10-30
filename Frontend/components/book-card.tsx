import Link from "next/link";
import Image from "next/image";
import Score from "./score";
import { BookData } from "@/interfaces";

export default function BookCard({bookData}: {bookData: BookData}) {
  const baseUrl = "/book";
  return (
    <div className="min-w-44">
      <Link href={baseUrl + "/" + bookData.id}>
        <Image className="rounded-md" alt="" height={100} width={176} src={bookData.coverURL} />
        {/* if i comment this line below everything works just fine */}
      </Link>
      <div className="px-1 py-2">
        <h3 className="font-medium leading-none tracking-tight">
          {bookData.title}
        </h3>
        <div className="flex justify-between">
          <Score score={bookData.user_score} />
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

export function BookCardExperimental({bookData}: {bookData: BookData}) {
  const baseUrl = "/book";
  return (
    <div className="flex flex-col flex-grow max-w-60">
      <Link href={baseUrl + "/" + bookData.id}>
        <Image className="rounded-md w-full" alt="" height={100} width={176} src={bookData.coverURL} />
        {/* if i comment this line below everything works just fine */}
      </Link>
      <div className="px-1 py-2">
        <h3 className="font-medium leading-none tracking-tight">
          {bookData.title}
        </h3>
        <div className="flex justify-between">
          <Score score={bookData.user_score} />
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