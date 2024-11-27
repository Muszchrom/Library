"use client";
import { Book, Library, Rental } from "@/interfaces";
import { Session } from "next-auth";
import { useEffect, useState } from "react";
import CardSkeleton from "@/components/card-skeleton";
import RentalsChart from "./rental-chart";
import CurrentlyRented from "./currently-rented";

export interface RentalData {
  book: Book, 
  rental: Rental, 
  library: Library
}

export default function Rentals({session}: {session: Session}) {
  const [rentals, setRentals] = useState<RentalData[] | undefined>(undefined);

  useEffect(() => {
    (async () => {
      const res = await fetch("http://localhost:8081/waz/rentals/user/" + session.user.id + "/");
      const rentals_: Rental[] = await res.json();

      const allData = await Promise.all(rentals_.map(async (r) => {
        const resBook = await fetch("http://localhost:8081/waz/books/" + r.book + "/");
        const resLib = await fetch("http://localhost:8081/waz/libraries/" + r.library + "/");
        return {
          rental: r,
          book: await resBook.json(),
          library: await resLib.json()
        };
      }));
      setRentals(allData);
    })();
  }, []);

  return (
    <>
      {rentals === undefined ? (
        <>
          <CardSkeleton />
          <CardSkeleton />
        </>
      ) : (
        <>
          <CurrentlyRented rentals={rentals.slice().filter((d) => d.rental.rental_status === "Pending" || d.rental.rental_status === "Rented")}/>
          <RentalsChart rentals={rentals}/>
        </>
      )}
    </>
  );
}

