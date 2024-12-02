import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useState } from "react";
import BookCard from "@/components/book-card-client";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { cn } from "@/lib/utils";
import { RentalData } from "./rentals";
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from "@/components/ui/alert-dialog";
import { gatewayServer } from "@/lib/urls";

export default function CurrentlyRented({token, rentalsProp}: {token: string, rentalsProp: RentalData[]}) {
  const [rentals, setRentals] = useState(rentalsProp);
  const [count, setCount] = useState(1); 

  const handleClick = async (rentalId: number) => {
    const res = await fetch(gatewayServer + "waz/rentals/" + rentalId + "/", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
      }
    }); 
    setRentals(rentals.filter((rental) => rental.rental.id !== rentalId));
    setCount(count-1);
    if (res.status === 200) {
      toast.success("Usunięto rezerwację na książkę")
    } else {
      toast.error("Wystąpił błąd", {
        description: "Kod błędu: " + res.status
      })
    }
  }

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
        {rentals[count-1] ? (
          <div className="flex justify-between gap-4 flex-wrap-reverse">
          <div className="flex w-1/2 flex-col gap-2 justify-between pb-2 grow">
            <div>
              <h3 className="font-semibold">{rentals[count-1].library.library_name}</h3>
              <span className="text-muted-foreground">{rentals[count-1].library.city}</span>
            </div>
            <div>
              <h4 className="text-center">Termin oddania</h4>
              <Progress value={
                (new Date().getTime() - new Date(rentals[count-1].rental.rental_date).getTime())/
                (new Date(rentals[count-1].rental.due_date).getTime() - new Date(rentals[count-1].rental.rental_date).getTime())*100 | 0
              }/>
              <div className="flex justify-between">
                <span className="text-muted-foreground text-sm">{rentals[count-1].rental.rental_date}</span>
                <span className="text-muted-foreground text-sm">{rentals[count-1].rental.due_date}</span>
              </div>
            </div>
            <div className="flex justify-between gap-2 flex-wrap">
              <Button className="grow max-w-[100px]" onClick={() => toast.info("Placeholder")}>Kontakt</Button>
              {rentals[count-1].rental.rental_status === "Rented" 
                ? <Button className="grow max-w-[100px]" onClick={() => toast.info("Placeholder")}>Przedłuż</Button>
                : (
                  <AlertDialog>
                    <AlertDialogTrigger className="grow max-w-[100px] bg-destructive py-2 px-4 text-destructive-foreground shadow-sm hover:bg-destructive/90 rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50">
                      Anuluj
                    </AlertDialogTrigger>
                    <AlertDialogContent>
                      <AlertDialogHeader>
                        <AlertDialogTitle>Usunąć rezerwację?</AlertDialogTitle>
                        <AlertDialogDescription>
                          Ta akcja jest nieodwracalna i ponowne dodanie książki będzie wymagać jej ponownego odnalezienia. 
                        </AlertDialogDescription>
                      </AlertDialogHeader>
                      <AlertDialogFooter>
                        <AlertDialogCancel>Anuluj</AlertDialogCancel>
                        <AlertDialogAction onClick={() => handleClick(rentals[count-1].rental.id)} className="grow bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90 rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50">
                          Usuń rezerwację
                        </AlertDialogAction>
                      </AlertDialogFooter>
                    </AlertDialogContent>
                  </AlertDialog>
                )}
            </div>
          </div>
          <div className="flex grow">
            <div className="w-full">
              <BookCard bookData={rentals[count-1].book}/>
            </div>
          </div>
        </div>
        ) : (
          <div className="aspect-video flex items-center justify-center">
            <span>Brak wypożyczonych książek 😔</span>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

