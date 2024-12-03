"use client"
import Link from "next/link";
import { LoginForm } from "../login-form";
import { useSearchParams } from "next/navigation";
import { Suspense } from "react";


function LogIn() {
  const searchParams = useSearchParams();
  const redirectBackTo: string | null = searchParams.get("redirectBackTo");
  const city: string | null = redirectBackTo && searchParams.get("city");
  const appendTo = "" + 
                   (redirectBackTo ? `?redirectBackTo=${encodeURIComponent(redirectBackTo as string)}` : "") + 
                   (city ? `&city=${encodeURIComponent(city as string)}` : "");

  return (
    <>
      <LoginForm formType="login" />
      <div className="flex justify-center mt-12">
        <span className="text-center text-muted-foreground">
          Nie masz konta?
          <Link className="text-sky-600 hover:underline" href={"/register" + appendTo}>
            &nbsp;Zarejestruj się
          </Link>
        </span>
      </div>
    </>
  );
}

export default function LogInSuspense() {
  return (
    <Suspense>
      <LogIn />
    </Suspense>
  );
}
