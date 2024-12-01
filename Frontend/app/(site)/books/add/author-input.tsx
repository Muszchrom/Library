"use client"

import { Button } from "@/components/ui/button";
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command";
import { FormControl, FormItem, FormLabel } from "@/components/ui/form";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import { Author } from "@/interfaces";
import { cn } from "@/lib/utils";
import { Check, ChevronsUpDown } from "lucide-react";
import { ControllerRenderProps, UseFormReturn } from "react-hook-form";

interface AuthorInputProps {
  children: React.ReactNode,
  field: ControllerRenderProps<{
    title: string;
    author: number;
    isbn: string;
    isbn13: string;
    description: string;
    publication_date: string;
    cover?: "";
  }, "author">,
  uploadBookForm: UseFormReturn<{
    author: number;
    title: string;
    isbn: string;
    isbn13: string;
    description: string;
    publication_date: string;
    cover?: "";
  }, undefined, undefined>,
  authors: Author[]
}

export default function AuthorInput({ children, field, uploadBookForm, authors }: AuthorInputProps) {

  return (
    <FormItem className="flex flex-col">
      <FormLabel>Autor</FormLabel>
      <Popover>
        <PopoverTrigger asChild>
          <FormControl>
            <Button
              variant="outline"
              role="combobox"
              className={cn(
                "w-[200px] justify-between",
                !field.value && "text-muted-foreground"
              )}
            >
              {field.value
                ? authors.find(
                    (author) => author.id == field.value
                  )?.first_name + " " + authors.find(
                    (author) => author.id == field.value
                  )?.second_name
                : "Wybierz autora"}
              <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
            </Button>
          </FormControl>
        </PopoverTrigger>
        <PopoverContent className="w-[200px] p-0">
          <Command>
            <CommandInput placeholder="Wyszukaj autora..." />
            <ScrollArea>
              <CommandList className="flex flex-col w-full space-x-2 py-2 px-1 max-h-[200px] " style={{overflowX: "unset", overflowY: "unset"}}>
                <CommandEmpty className="text-sm flex flex-col w-full gap-2 items-center">
                  <span>Nie znaleziono autora.</span>
                  {children}
                </CommandEmpty>
                <CommandGroup>
                  {authors.map((author) => (
                    <CommandItem 
                      value={author.first_name + " " + author.second_name}
                      key={author.id}
                      onSelect={() => {
                        uploadBookForm.setValue("author", author.id)
                      }}
                    >
                      <Check
                        className={cn(
                          "mr-2 h-4 w-4",
                          author.id == field.value
                            ? "opacity-100"
                            : "opacity-0"
                        )}
                      />

                      {author.first_name + " " + author.second_name}
                    </CommandItem>
                  ))}
                </CommandGroup>
              </CommandList>
              <ScrollBar orientation="vertical" />
            </ScrollArea>
          </Command>
        </PopoverContent>
      </Popover>
    </FormItem>
  );
}