"use client"

import { Button } from "@/components/ui/button";
import { Book, LibraryDistance } from "@/interfaces";
import { useEffect, useState } from "react";
import ChoosePlace, { City } from "./choose-place";
import { useRouter } from "next/navigation";

export default function LibrariesList({bookId}: {bookId: Book["id"]}) {
  const [libraries, setLibraries] = useState<LibraryDistance[] | undefined>(undefined);
  const [sortDistanceAscending, setSortDistanceAscending] = useState<boolean>(true);

  const [city, setCity] = useState<City>();
  const [latLong, setLatLong] = useState<string>("") // ex "51.246500 22.568400" | "lat long"

  const router = useRouter();

  useEffect(() => {
    if (!(latLong.length > 0)) return;
    let [lat, long] = latLong.split(" ");
    (async () => {
      const url = "http://localhost:8081/waz/libraries/?" + 
                  "latitude=" + lat + "&" + 
                  "longitude=" + long + "&" + 
                  "book=" + bookId;
      const res = await fetch(url);
      const lbrs: LibraryDistance[] = await res.json();
      setLibraries(lbrs);
    })()
  }, [latLong]);

  // http://localhost:8000/libraries/?latitude=51.246500&longitude=22.568400&book=1

  const locationListener = (city: City) => {
    setLatLong(`${city.lat} ${city.long}`);
    setCity(city);
  }

  const libraryChosenEvent = (libraryId: number) => {
    console.log(libraryId, bookId);
    router.push(`/cart?libraryid=${libraryId}&bookid=${bookId}`);
  }

  return (
    <div className="flex flex-col gap-4 mt-4">
      <div className="flex justify-between items-start">
        {/* <Button variant={"outline"}>Odległość 👇</Button> */}
        {/* <Button variant={"outline"}>Domyślnie 👇</Button> */}
        {/* <Button variant="outline" disabled={true}>Dostawa ✅</Button> */}
        {/* <ChoosePlace changeListener={locationListener}/> */}
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