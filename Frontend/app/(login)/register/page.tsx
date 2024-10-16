import Link from "next/link";
import { LoginForm } from "../login-form";

export default function LogIn() {
  return (
    <>
      <LoginForm formType="register" />
      <div className="flex justify-center mt-12">
        <span className="text-center text-muted-foreground">
          Masz już konto? 
          <Link className="text-sky-600 hover:underline" href={"/login"}>
              &nbsp;Zaloguj się
          </Link>
        </span>
      </div>
    </>
  );
}
