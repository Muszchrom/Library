import ButtonLink from "@/components/button-link";
import { Separator } from "@/components/ui/separator";
import { authOptions } from "@/lib/auth";
import { getServerSession } from "next-auth";
import React from "react";

export default async function BookLayout({children}: {children: React.ReactNode}) {
  const session = await getServerSession(authOptions);

  if (session?.user.role == "2" || session?.user.role == "1") {
    return (
      <div className="flex flex-col gap-3">
        <div className="flex w-full justify-between gap-2 sm:gap-4">
          <ButtonLink to="/books/browse" emoji="🔎">Przeglądaj</ButtonLink>
          <ButtonLink to="/books/add" emoji="➕">Dodaj</ButtonLink>
          <ButtonLink to="/books/stats" emoji="📈">Statystyki</ButtonLink>
        </div>
        <Separator orientation="horizontal"/>
        {children}
      </div>
    )
  } else {
    return (
      <div className="flex flex-col gap-3">
        {children}
      </div>
    )
  }
}

