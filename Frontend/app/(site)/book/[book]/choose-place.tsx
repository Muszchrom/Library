import { Button } from "@/components/ui/button";
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import { City } from "@/interfaces";
import { cities } from "@/lib/rawdata";
import { cn } from "@/lib/utils";
import { Check, ChevronsUpDown } from "lucide-react";
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

export default function ChoosePlace({changeListener}: {changeListener: (city: City) => void}) {
  const searchParams = useSearchParams();
  const [choosenCity, setChoosenCity] = useState<City | undefined>(undefined);
  
  useEffect(() => {
    const c = searchParams.get("city");
    if (!c) return;

    const foundCity = cities.find((ct) => ct.city == c);
    if (!foundCity) return;
    setChoosenCity(foundCity);
    changeListener(foundCity);
  }, [searchParams, changeListener])
  
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