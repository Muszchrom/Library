"use client";
import { Book, Library, Rental } from "@/interfaces";
import { Session } from "next-auth";
import { useEffect, useState } from "react";
import CardSkeleton from "@/components/card-skeleton";
import RentalsChart from "./rental-chart";
import CurrentlyRented from "./currently-rented";
import { gatewayClient } from "@/lib/urls";

export interface RentalData {
  book: Book, 
  rental: Rental, 
  library: Library
}

export default function Rentals({session}: {session: Session}) {
  const [rentals, setRentals] = useState<RentalData[] | undefined>(undefined);

  useEffect(() => {
    (async () => {
      const res = await fetch(gatewayClient + "waz/rentals/user/" + session.user.id + "/");
      if (!res.ok) return;
      const rentals_: Rental[] = await res.json();

      const allData = await Promise.all(rentals_.map(async (r) => {
        const resBook = await fetch(gatewayClient + "waz/books/" + r.book + "/");
        const resLib = await fetch(gatewayClient + "waz/libraries/" + r.library + "/");
        return {
          rental: r,
          book: await resBook.json(),
          library: await resLib.json()
        };
      }));
      setRentals(allData);
    })();
  }, [session.user.id]);

  return (
    <>
      {rentals === undefined ? (
        <>
          <CardSkeleton />
          <CardSkeleton />
        </>
      ) : (
        <>
          <CurrentlyRented token={session.user.APIToken} rentalsProp={rentals.slice().filter((d) => d.rental.rental_status === "Pending" || d.rental.rental_status === "Rented")}/>
          <RentalsChart rentals={rentals}/>
        </>
      )}
    </>
  );
}

