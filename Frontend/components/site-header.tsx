import {
  Sheet,
  SheetContent,
  SheetClose,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet"
import { BookCheckIcon } from "lucide-react";
import Link from "next/link";
import LogInOutThing from "./log-in-out-provider";


export async function SiteHeader() {
  const links = [
    { id: 1, title: "Lorem", path: "lorem" },
    { id: 2, title: "Ipsum", path: "ipsum" },
    { id: 3, title: "Dolor", path: "dolor" },
    { id: 4, title: "Sit", path: "sit" },
    { id: 5, title: "Amet", path: "amet" }
  ];

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
                {links.map((lnk) => 
                  <SheetClose asChild key={lnk.id}>
                    <Link href={lnk.path}>
                      {lnk.title}
                    </Link>
                  </SheetClose>
                )}
              </div>
              <div className="pt-6">
                <div className="flex flex-col space-y-3 pt-4">
                  <h4 className="font-medium">Miejsca</h4>
                  {links.map((lnk) => 
                    <SheetClose asChild key={lnk.id}>
                      <Link className="text-muted-foreground" href={lnk.path}>
                        {lnk.title}
                      </Link>
                    </SheetClose>
                  )}
                </div>
                
              </div>

              <div className="mt-auto">
              <SheetClose asChild>
                <LogInOutThing />
              </SheetClose>
              </div>
            </div>
          </SheetContent>
        </Sheet>
      </div>
    </header>
  );
}