"use client"

import { Button } from "@/components/ui/button";
import { Book, LibraryDistance } from "@/interfaces";
import { useEffect, useState } from "react";
import ChoosePlace, { City } from "./choose-place";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { gatewayClient } from "@/lib/urls";
import { signOut } from "next-auth/react";

export default function LibrariesList({bookId, token}: {bookId: Book["id"], token: string | undefined}) {
  const [libraries, setLibraries] = useState<LibraryDistance[] | undefined>(undefined);

  const [city, setCity] = useState<City>();
  const [latLong, setLatLong] = useState<string>("") // ex "51.246500 22.568400" | "lat long"

  const router = useRouter();

  useEffect(() => {
    if (!(latLong.length > 0)) return;
    const [lat, long] = latLong.split(" ");
    (async () => {
      const url = gatewayClient + "waz/libraries/?" + 
                  "latitude=" + lat + "&" + 
                  "longitude=" + long + "&" + 
                  "book=" + bookId;
      const res = await fetch(url);
      const lbrs: LibraryDistance[] = await res.json();
      setLibraries(lbrs);
    })()
  }, [latLong, bookId]);


  const locationListener = (city: City) => {
    setLatLong(`${city.lat} ${city.long}`);
    setCity(city);
  }

  const libraryChosenEvent = async (libraryId: number) => {
    if (!token) return;
    const res = await fetch(gatewayClient + "waz/rentals/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
      },
      body: JSON.stringify({
        book_id: bookId,
        library_id: libraryId
      })
    })
    const data = await res.json()
    if (res.status === 400) {
      console.log(data.error)
      let clientError = "Książka jest obecnie niedostępna"
      if (data.error === "User role and ID not provided in the headers.") {
        (async () => {
          await signOut({redirect: false});
          return router.push('/login');
        })();
      } else if (data.error === "You cannot rent more than 2 books.") {
        clientError = "Nie możesz wypożyczyć więcej niż 2 książki"
      } 
      return toast.warning(clientError);
    }
    if (res.status !== 201) return toast.error("Coś poszło nie tak", {
      description: "Kod błędu" + res.status
    });

    // router.push(`/cart?libraryid=${libraryId}&bookid=${bookId}`);
    router.push(`/profile`);
  }

  return (
    <div className="flex flex-col gap-4 mt-4">
      <div className="flex justify-between items-start">
      </div>
      <span className="text-center">
        {libraries 
          ? `Biblioteki w pobliżu miasta ${city?.city}`
          : "Wybierz lokalizację aby zobaczyć najbliższe biblioteki"}
      </span>
      <div className="w-full flex justify-center">
        <ChoosePlace changeListener={locationListener}/>
      </div>
      {libraries?.slice(0, 7).map((library) => (
        <LibraryCard key={library.id} library={library} handleClick={libraryChosenEvent}/>
      ))}
    </div>
  );
}

function LibraryCard({library, handleClick}: {library: LibraryDistance, handleClick: (libId: number) => void}) {
  return (
    <div className="rounded-xl border bg-card text-card-foreground shadow">
      <div className="flex p-4 justify-between">
        <div className="flex flex-col justify-between gap-2">
          <h3 className="font-semibold leading-none tracking-tight">{library.library_name}</h3>
          <p className="text-sm text-muted-foreground">{library.city}{/**Sympatyczna 16, 20-530 Lublin */}</p>
        </div>
        <div className="flex flex-col justify-between gap-2">
          <span className="text-right text-sm text-muted-foreground leading-none">
          {Math.round(library.distance)} km
          </span>
          <Button onClick={() => handleClick(library.id)}>Wybierz</Button>
        </div>
      </div>
    </div>
  );
}