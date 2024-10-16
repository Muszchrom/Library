import Link from "next/link";
import { LoginForm } from "../login-form";


export default function LogIn() {
  return (
    <>
      <LoginForm formType="login" />
      <div className="flex justify-center mt-12">
        <span className="text-center text-muted-foreground">
          Nie masz konta?
          <Link className="text-sky-600 hover:underline" href={"/register"}>
            &nbsp;Zarejestruj się
          </Link>
        </span>
      </div>
    </>
  );
}
