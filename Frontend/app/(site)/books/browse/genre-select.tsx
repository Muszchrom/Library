"use client"
import { Button } from "@/components/ui/button";
import { Genre } from "@/interfaces";
import React, { useState } from "react";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Command, CommandEmpty, CommandInput, CommandItem, CommandList } from "@/components/ui/command";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import { Check, ChevronsUpDown, Trash2 } from "lucide-react";
import { CommandGroup } from "cmdk";
import { cn } from "@/lib/utils";


interface GenreSelectProps {
  genres: Genre[]
  value: string | undefined
  onValueChange: (value: string | undefined) => void
}

export default function GenreSelect({genres, value, onValueChange}: GenreSelectProps) {
  const [open, setOpen] = useState(false);
  // const [selectedValue, setSelectedValue] = useState<string | undefined>(undefined);

  return (
    <Popover modal={true} open={open} onOpenChange={() => setOpen(!open)}>
      <div className="flex flex-row gap-2">
        <PopoverTrigger asChild>
          <Button variant="outline" role="combobox" className={cn("justify-between grow", !value && "text-muted-foreground")} onClick={() => setOpen(!open)}>
            {value 
              ? genres.find((genre) => genre.genre == value)?.genre
              : "Wybierz gatunek"}
            <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50"/>
          </Button>
        </PopoverTrigger>
        <Button variant="destructive" disabled={!value} onClick={() => onValueChange(undefined)}>
          <Trash2 className="h-4 w-4"/>
        </Button>
      </div>
      <PopoverContent className="w-[--radix-popover-trigger-width] max-h-[--radix-popover-content-available-height] p-0">
        <Command>
          <CommandInput placeholder="Wyszukaj gatunek..." />
          <ScrollArea>
            <CommandList className="flex flex-col w-full space-x-2 py-2 px-1 max-h-[200px] " style={{overflowX: "unset", overflowY: "unset"}}>
              <CommandEmpty className="text-sm flex flex-col w-full gap-2 items-center">
                Nie znaleziono gatunku
              </CommandEmpty>
              <CommandGroup>
                {genres.map((genre) => (
                  <CommandItem
                    value={genre.genre}
                    key={genre.id}
                    onSelect={() => {
                      onValueChange(genre.genre)
                      setOpen(!open)
                    }}
                  >
                    <Check 
                      className={cn(
                        "mr-2 h-4 w-4",
                        genre.genre === value
                          ? "opacity-100"
                          : "opacity-0"
                      )}
                    />
                    {genre.genre}
                  </CommandItem>
                ))}
              </CommandGroup>
            </CommandList>
            <ScrollBar orientation="vertical"/>
          </ScrollArea>
        </Command>
      </PopoverContent>
    </Popover>
  )
}