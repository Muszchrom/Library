import { authOptions } from "@/lib/auth";
import { getServerSession } from "next-auth";

export default async function Page() {
  const session = await getServerSession(authOptions);
  const res = await fetch("http://gateway:8081/auth/user/" + session?.user.id);
  const user = await res.json();

  return (
    <>
      <h1 className="text-2xl font-bold tracking-tight">Profil</h1>
      <div>
        <div className="flex justify-between">
          <span>id</span>
          <span>{user.id}</span>
        </div>
        <div className="flex justify-between">
          <span>username</span>
          <span>{user.username}</span>
        </div>
        <div className="flex justify-between">
          <span>email</span>
          <span>{user.email}</span>
        </div>
        <div className="flex justify-between">
          <span>phone</span>
          <span>{user.phone}</span>
        </div>
        <div className="flex justify-between">
          <span>role</span>
          <span>{user.role}</span>
        </div>
      </div>
    </>
  );
}