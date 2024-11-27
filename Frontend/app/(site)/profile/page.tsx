import SignOut from "@/components/signout";
import { authOptions } from "@/lib/auth";
import { getServerSession } from "next-auth";
import EditProfile from "./edit-profile";
import { User } from "@/interfaces";
import Rentals from "./rentals";
import CardSkeleton from "@/components/card-skeleton";

export default async function Page() {
  const session = await getServerSession(authOptions);
  const res = await fetch("http://gateway:8081/auth/user/" + session?.user.id);
  if (res.status !== 200 || !session) return <SignOut />
  const user: User = await res.json();
  
  return (
    <>
      <div className="flex flex-col gap-4">
        <h1 className="text-2xl font-bold tracking-tight">Profil</h1>
        <Rentals session={session}/>

        <CardSkeleton />

        <EditProfile session={session} apiToken={session.user.APIToken}/>

      </div>
    </>
  );
}