"use client";

import { signOut, useSession } from "next-auth/react";
import { Button } from "./ui/button";
import { toast } from "sonner";
import { useRouter } from "next/navigation";
import { SheetClose } from "./ui/sheet";
import Link from "next/link";

export interface LinkLoggedInDependantProps {
  loggedInText?: string,
  notLoggedInText?: string,
  linkHref?: string,
  type?: 'log-in-out' | 'sheet-link'
}

export default function LinkLoggedInDependant({ loggedInText, notLoggedInText, linkHref, type }: LinkLoggedInDependantProps) {
  const { data: session } = useSession();
  const router = useRouter();

  const handleClick = () => {
    signOut({redirect: false});
    toast.info("Nastąpiło wylogowanie");
  }

  if (type === "sheet-link") {
    return (
      <>
        {session && (
          <SheetClose asChild>
            <Link href={linkHref ? linkHref : "/"}>
              {loggedInText}
            </Link>
          </SheetClose>
        )}
      </>
    )
  }

  return (
    <>
      <SheetClose asChild>
        {session ? (
          <Button type="button" variant={"link"} onClick={() => handleClick()}>{loggedInText}</Button>
        ) : (
          <Button type="button" variant={"link"} onClick={() => router.push("/login")}>{notLoggedInText}</Button>
        )}
      </SheetClose>
    </>
  )
}