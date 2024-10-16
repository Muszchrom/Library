import Link from "next/link";
import React from "react";

export default function LoginLayout({children}: {children: React.ReactNode}) {
  return (
    <main className="flex-[1_1_0]">
      <div className="container px-4 md:px-8 mx-auto flex h-14 max-w-screen-2xl items-center text-sky-600 hover:underline">
        <Link href="/">Powrót</Link>
      </div>
      <div className="container mx-auto flex justify-center items-center h-full">
        <div className="max-w-xs w-full">
          {children}
        </div>
      </div>
    </main>
  )
}