import ButtonLink from "@/components/button-link";
import React from "react";

export default function BookLayout({children}: {children: React.ReactNode}) {
  return (
    <div className="flex flex-col gap-3">
      <div className="flex w-full justify-between gap-2 sm:gap-4">
        <ButtonLink to="/books/browse" emoji="🔎">Przeglądaj</ButtonLink>
        <ButtonLink to="/books/add" emoji="➕">Dodaj</ButtonLink>
        <ButtonLink to="/books/stats" emoji="📈">Statystyki</ButtonLink>
      </div>
      {children}
    </div>
  )
}

