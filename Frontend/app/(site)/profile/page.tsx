import SignOut from "@/components/signout";
import { authOptions } from "@/lib/auth";
import { getServerSession } from "next-auth";
import EditProfile from "./edit-profile";
import Rentals from "./rentals";

export default async function Page() {
  const session = await getServerSession(authOptions);
  if (!session) return <SignOut />
  
  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-2xl font-bold tracking-tight">Profil</h1>
      <Rentals session={session}/>
      <EditProfile session={session} apiToken={session.user.APIToken}/>
    </div>
  );
}