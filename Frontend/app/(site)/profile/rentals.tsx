"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

import { Book, Library, Rental } from "@/interfaces";
import { Session } from "next-auth";
import { useEffect, useState } from "react";
import BookCard from "@/components/book-card-client";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { cn } from "@/lib/utils";
import CardSkeleton from "@/components/card-skeleton";

interface RentalData {
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
      const pendingAndRented = rentals_.filter((r) => r.rental_status === "Pending" || r.rental_status === "Rented");

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

      const activeRentals = allData.filter((d) => d.rental.rental_status === "Pending" || d.rental.rental_status === "Rented");

      // const books = await Promise.all(
      //   rentals_.map(async (r) => {
      //     const res_ = await fetch("http://localhost:8081/waz/books/" + r.book + "/");
      //     return await res_.json();
      // }));
      // const libraries = await Promise.all(
      //   rentals_.map(async (r) => {
      //     const res_ = await fetch("http://localhost:8081/waz/libraries/" + r.library + "/");
      //     return await res_.json();
      // }));

      // console.log(allData);

      // console.log(rentals_); // all rentals
      // console.log(pendingAndRented); // pending and rented rentals
      // console.log(books); // books for all rentals
      // console.log(libraries); // books for 
      // setRentals(rentals_);
      // const rentedBook1 = 1; 
      // const res2 = await fetch("http://localhost:8081/waz/books/1/");
    })();
  }, []);

  return (
    <>
      {rentals === undefined ? (
        <CardSkeleton />
      ) : (
        <CurrentlyRented rentals={rentals.filter((d) => d.rental.rental_status === "Pending" || d.rental.rental_status === "Rented")}/>
      )}
    </>
  );
}

function CurrentlyRented({rentals}: {rentals: RentalData[]}) {
  const [count, setCount] = useState(1); 
  return (
    <Card>
      <CardHeader className="flex-row items-center justify-between flex-wrap gap-4">
        <CardTitle className="grow">Obecnie wypożyczone</CardTitle>
        <div className="flex justify-end gap-2 grow">
          {Array.from(Array(rentals.length).keys()).map((key) => {
            key += 1;

            return (
              <Button 
                key={key} 
                variant="outline" 
                className={cn("aspect-square", key == count && "bg-accent text-accent-foreground")}
                onClick={() => setCount(key)}
              >
                {key}
              </Button>
            );
          })}
        </div>
      </CardHeader>
      <CardContent>
        <div className="flex">
          <div key={rentals[count-1].rental.id} className="flex justify-between gap-4 flex-wrap-reverse">
            <div className="flex w-1/2 flex-col gap-2 justify-between pb-2 grow">
              <div>
                <h3 className="font-semibold">{rentals[count-1].library.library_name}</h3>
                <span className="text-muted-foreground">{rentals[count-1].library.city}</span>
              </div>
              <div>
                <h4 className="text-center">Termin oddania</h4>
                <Progress value={
                  (new Date().getTime() - new Date(rentals[count-1].rental.rental_date).getTime())/
                  (new Date(rentals[count-1].rental.due_date).getTime() - new Date(rentals[count-1].rental.rental_date).getTime())*100
                }/>
                <div className="flex justify-between">
                  <span className="text-muted-foreground text-sm">{rentals[count-1].rental.rental_date}</span>
                  <span className="text-muted-foreground text-sm">{rentals[count-1].rental.due_date}</span>
                </div>
              </div>
              <div className="flex justify-between gap-2 flex-wrap">
                <Button className="grow max-w-[100px]" onClick={() => toast.info("Placeholder")} >Kontakt</Button>
                <Button className="grow max-w-[100px]" onClick={() => toast.info("Placeholder")}>Przedłóż</Button>
              </div>
            </div>
            <div className="flex grow">
              <div className="w-full"><BookCard bookData={rentals[count-1].book}/></div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

function RentalsGraph({rentals}: {rentals: RentalData[]}) {
  return (
    <div>
      {}
    </div>
  );
}

