import { Button } from "@/components/ui/button";
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import { cn } from "@/lib/utils";
import { Check, ChevronsUpDown } from "lucide-react";
import { useState } from "react";

export interface City {
  city: string, 
  long: string, 
  lat: string, 
  id: number
}

const cities: City[] = [
  { city: "Warszawa", long: "21.0122", lat: "52.2297", id: 1 },
  { city: "Kraków", long: "19.9366", lat: "50.0614", id: 2 },
  { city: "Łódź", long: "19.4560", lat: "51.7592", id: 3 },
  { city: "Wrocław", long: "17.0385", lat: "51.1079", id: 4 },
  { city: "Poznań", long: "16.9252", lat: "52.4064", id: 5 },
  { city: "Gdańsk", long: "18.6466", lat: "54.3521", id: 6 },
  { city: "Szczecin", long: "14.5530", lat: "53.4289", id: 7 },
  { city: "Bydgoszcz", long: "18.0066", lat: "53.1235", id: 8 },
  { city: "Lublin", long: "22.5674", lat: "51.2465", id: 9 },
  { city: "Białystok", long: "23.1688", lat: "53.1325", id: 10 },
  { city: "Katowice", long: "19.0238", lat: "50.2599", id: 11 },
  { city: "Gdynia", long: "18.5361", lat: "54.5189", id: 12 },
  { city: "Częstochowa", long: "19.1255", lat: "50.8118", id: 13 },
  { city: "Radom", long: "21.1562", lat: "51.4020", id: 14 },
  { city: "Toruń", long: "18.5984", lat: "53.0138", id: 15 },
  { city: "Sosnowiec", long: "19.2045", lat: "50.2863", id: 16 },
  { city: "Rzeszów", long: "22.0027", lat: "50.0412", id: 17 },
  { city: "Kielce", long: "20.6320", lat: "50.8661", id: 18 },
  { city: "Gliwice", long: "18.6766", lat: "50.2945", id: 19 },
  { city: "Zabrze", long: "18.7857", lat: "50.3249", id: 20 },
  { city: "Olsztyn", long: "20.4927", lat: "53.7784", id: 21 },
  { city: "Bielsko-Biała", long: "19.0347", lat: "49.8224", id: 22 },
  { city: "Bytom", long: "18.9233", lat: "50.3484", id: 23 },
  { city: "Zielona Góra", long: "15.5050", lat: "51.9356", id: 24 },
  { city: "Rybnik", long: "18.5463", lat: "50.0975", id: 25 },
  { city: "Ruda Śląska", long: "18.8557", lat: "50.2558", id: 26 },
  { city: "Opole", long: "17.9269", lat: "50.6751", id: 27 },
  { city: "Tychy", long: "19.0014", lat: "50.1206", id: 28 },
  { city: "Gorzów Wielkopolski", long: "15.2288", lat: "52.7325", id: 29 },
  { city: "Elbląg", long: "19.4088", lat: "54.1561", id: 30 }
];

export default function ChoosePlace({changeListener}: {changeListener: (city: City) => void}) {
  const [choosenCity, setChoosenCity] = useState<City | undefined>(undefined);
  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          className={cn(
            "w-[200px] justify-between",
            !choosenCity && "text-muted-foreground"
          )}
        >
          {choosenCity
            ? cities.find((city) => city.id === choosenCity.id)?.city
            : "Wybierz miasto"}
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[200px] p-0">
        <Command>
          <CommandInput placeholder="Wyszukaj miejscowość..."/>
          <ScrollArea>
            <CommandList className="flex flex-col w-full space-x-2 py-2 px-1 max-h-[200px] " style={{overflowX: "unset", overflowY: "unset"}}>
              <CommandEmpty>
                Nie znaleziono miejsca
              </CommandEmpty>
              <CommandGroup>
                {cities.map((city) => (
                  <CommandItem
                    value={city.city}
                    key={city.id}
                    onSelect={() => {
                      setChoosenCity(city);
                      changeListener(city);
                    }}
                  >
                    <Check 
                      className={cn(
                        "mr-2 h-4 w-4",
                        choosenCity?.id == city.id
                          ? "opacity-100"
                          : "opacity-0" 
                      )}
                    />
                    {city.city}
                  </CommandItem>
                ))}
              </CommandGroup>
            </CommandList>
            <ScrollBar orientation="vertical"/>
          </ScrollArea>
        </Command>
      </PopoverContent>
    </Popover>
  );
}