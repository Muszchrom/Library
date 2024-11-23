"use client"
import { Button } from "@/components/ui/button";
import { Author } from "@/interfaces";
import React, { useState } from "react";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Command, CommandEmpty, CommandInput, CommandItem, CommandList } from "@/components/ui/command";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import { Check, ChevronsUpDown, Trash2 } from "lucide-react";
import { CommandGroup } from "cmdk";
import { cn } from "@/lib/utils";

interface AuthorSelectProps {
  authors: Author[]
  value: number | undefined
  onValueChange: (value: number | undefined) => void
}

export default function AuthorSelect({authors, value, onValueChange}: AuthorSelectProps) {

  const [open, setOpen] = useState(false);

  return (
    <Popover modal={true} open={open} onOpenChange={() => setOpen(!open)}>
      <div className="flex flex-row gap-2">
        <PopoverTrigger asChild>
          <Button variant="outline" role="combobox" className={cn("justify-between grow", !value && "text-muted-foreground")} onClick={() => setOpen(!open)}>
            {value 
              ? (() => {
                const x = authors.find((author) => author.id == value);
                return `${x?.first_name} ${x?.second_name}`;
              })()
              : "Wybierz autora"}
            <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50"/>
          </Button>
        </PopoverTrigger>
        <Button variant="destructive" disabled={!value} onClick={() => onValueChange(undefined)}>
          <Trash2 className="h-4 w-4"/>
        </Button>
      </div>
      <PopoverContent className="w-[--radix-popover-trigger-width] max-h-[--radix-popover-content-available-height] p-0">
        <Command>
          <CommandInput placeholder="Wyszukaj autora..." />
          <ScrollArea>
            <CommandList className="flex flex-col w-full space-x-2 py-2 px-1 max-h-[200px] " style={{overflowX: "unset", overflowY: "unset"}}>
              <CommandEmpty className="text-sm flex flex-col w-full gap-2 items-center">
                Nie znaleziono autora
              </CommandEmpty>
              <CommandGroup>
                {authors.map((author) => (
                  <CommandItem
                    value={author.first_name + " " + author.second_name}
                    key={author.id}
                    onSelect={() => {
                      onValueChange(author.id)
                      setOpen(!open)
                    }}
                  >
                    <Check 
                      className={cn(
                        "mr-2 h-4 w-4",
                        author.id === value
                          ? "opacity-100"
                          : "opacity-0"
                      )}
                    />
                    {author.first_name + " " + author.second_name}
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