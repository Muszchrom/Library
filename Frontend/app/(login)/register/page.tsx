"use client"
import Link from "next/link";
import { LoginForm } from "../login-form";
import { useSearchParams } from "next/navigation";
import { Suspense } from "react";

function Register() {
  const searchParams = useSearchParams();
  const redirectBackTo: string | null = searchParams.get("redirectBackTo");
  const city: string | null = redirectBackTo && searchParams.get("city");
  const appendTo = "" + 
                   (redirectBackTo ? `?redirectBackTo=${encodeURIComponent(redirectBackTo as string)}` : "") + 
                   (city ? `&city=${encodeURIComponent(city as string)}` : "");

  return (
    <>
      <LoginForm formType="register" />
      <div className="flex justify-center mt-12">
        <span className="text-center text-muted-foreground">
          Masz już konto? 
          <Link className="text-sky-600 hover:underline" href={"/login" + appendTo}>
              &nbsp;Zaloguj się
          </Link>
        </span>
      </div>
    </>
  );
}

export default function RegisterSuspense() {
  return (
    <Suspense>
      <Register />
    </Suspense>
  )
}
