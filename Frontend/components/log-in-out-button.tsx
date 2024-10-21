"use client";

import { signOut, useSession } from "next-auth/react";
import { Button } from "./ui/button";
import { toast } from "sonner";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function LogInOutButton() {
  const { data: session } = useSession();
  const router = useRouter();

  useEffect(() => {
    console.log(session)
  }, [session])

  const handleClick = () => {
    signOut({redirect: false});
    toast.info("Nastąpiło wylogowanie");
  }
  return (
    <>
      {session ? (
        <Button type="button" variant={"link"} onClick={() => handleClick()}>Wyloguj się</Button>
      ) : (
        <Button type="button" variant={"link"} onClick={() => router.push("/login")}>Zaloguj się</Button>
      )}
    </>
  )
}