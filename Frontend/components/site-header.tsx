import {
  Sheet,
  SheetContent,
  SheetClose,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet"
import { BookCheckIcon } from "lucide-react";
import Link from "next/link";
import React from "react";
import LinkLoggedInDependantProvider from "./link-logged-in-dependant-provider";


export async function SiteHeader() {
  return (
    <header className="">
      <div className="container px-4 md:px-8 mx-auto flex h-14 max-w-screen-2xl items-center justify-between ">
        <Link href="/">
          <span className="scroll-m-20 text-xl font-bold tracking-tight inline-flex gap-1 items-center">
            <BookCheckIcon className="h-5 w-5"/>  
            library
          </span>
        </Link>
        <Sheet>
          <SheetTrigger className="h-9 py-2 ml-2 px-0 bg-transparent hover:bg-transparent focus-visible:bg-transparent focus-visible:ring-0 focus-visible:ring-offset-0 ">
            <svg strokeWidth="1.5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 [transform:rotateZ(180deg)]">
              <path d="M3 5H11" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"></path>
              <path d="M3 12H16" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"></path>
              <path d="M3 19H21" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"></path>
            </svg>
          </SheetTrigger>
          <SheetContent side={"left"} className="flex flex-col">
            <SheetTitle aria-describedby="" className="inline-flex gap-1 items-center">
              <BookCheckIcon className="h-5 w-5"/>  
              library
            </SheetTitle>
            <div className="my-4 pb-10 pr-6 flex-[1_1_0] flex flex-col">
              <div className="flex flex-col space-y-3">
                <LinkLoggedInDependantProvider 
                  type="sheet-link"
                  linkHref="/profile"
                  loggedInText="Profil"
                />
                <NavLink to="/books/browse">Książki</NavLink>
              </div>

              <div className="mt-auto">
              <SheetClose asChild>
                <LinkLoggedInDependantProvider 
                  type="log-in-out"
                  loggedInText="Wyloguj się"
                  notLoggedInText="Zaloguj się"
                />
              </SheetClose>
              </div>
            </div>
          </SheetContent>
        </Sheet>
      </div>
    </header>
  );
}

function NavLink({to, children}: {to: string, children: React.ReactNode}) {
  return (
    <SheetClose asChild>
      <Link href={to}>
        {children}
      </Link>
    </SheetClose>
  )
}