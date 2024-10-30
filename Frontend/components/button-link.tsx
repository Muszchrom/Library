import Link from "next/link";
import { Button } from "./ui/button";

export default function ButtonLink({emoji, to, children}: {emoji: string, to: string, children: React.ReactNode}) {
  return (
    <Button variant={"outline"} className="flex-grow p-0">
      <Link href={to} className="py-2 px-2 sm:px-4 w-full text-center">
        <span className="flex w-full items-center justify-center">
          <span className="mr-1 sm:mr-2 block">{emoji}</span>
          <span>{children}</span>
        </span>
      </Link>
    </Button>
  )
}