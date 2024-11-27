"use client";
import { User } from "@/interfaces";
import EditProfilePopoverForm from "./forms/edit-profile-popover-form";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useEffect, useState } from "react";
import { Session } from "next-auth";
import SignOut from "@/components/signout";
import CardSkeleton from "@/components/card-skeleton";

export interface ChangeProfile {
  variant: "email" | "phone" | "psswd" | "uname"
}

interface Data extends ChangeProfile {
  title: string,
  content: string | number
}

const rawData: Data[] = [
  {
    variant: "email",
    title: "Email: ",
    content: ""
  },
  {
    variant: "phone",
    title: "Telefon: ",
    content: ""
  },
  {
    variant: "uname",
    title: "Nazwa użytkownika: ",
    content: ""
  },
  {
    variant: "psswd",
    title: "Hasło: ",
    content: "***********"
  }
]

export default function EditProfile({session, apiToken}: {session: Session, apiToken: string}) {
  const [udata, setUdata] = useState<Data[]>([]);

  useEffect(() => {
    (async () => {
      const res = await fetch("http://localhost:8081/auth/user/" + session.user.id);
      if (res.status !== 200 || !session) return <SignOut />
      const user: User = await res.json();
      updateData(user);
    })();
  }, [])

  const updateData = (user: User) => {
    rawData[0].content = user.email
    rawData[1].content = user.phone
    rawData[2].content = user.username
    setUdata([...rawData])
  }

  return (
    <>
    {udata.length ? (
      <Card>
        <CardHeader>
          <CardTitle>Ustawienia konta</CardTitle>
          <CardDescription>Zmień ustawienia konta klikając na przycisk "edytuj"</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col gap-4">
            {udata.map((d) => (
              <div key={d.variant} className="flex items-center justify-between">
                <div className="flex flex-col">
                  <span className="font-semibold leading-none tracking-tight">{d.title}</span>
                  <span className="text-muted-foreground">{d.content}</span>
                </div>
                <EditProfilePopoverForm variant={d.variant} token={apiToken} onUpdateSuccess={updateData}/>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    ) : (
      <CardSkeleton />
    )}
    </>
  );
}
