"use client"
import { useSearchParams } from "next/navigation";

export default function CartPage() {
  const searchParams = useSearchParams()
 
  const lib = searchParams.get('libraryid');
  const book = searchParams.get('bookid');
  return (
    <div className="flex flex-col">
      Cart
      <span>{lib}</span>
      <span>{book}</span>
    </div>
  );
}