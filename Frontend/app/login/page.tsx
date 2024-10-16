import { LoginForm } from "./login-form";

export default function LogIn() {
  return (
    <main className="flex-[1_1_0]">
      <div className="border-b container flex justify-center items-center h-full">
        <div className="max-w-xs w-full">
          <LoginForm />
        </div>
      </div>
    </main>
  );
}
