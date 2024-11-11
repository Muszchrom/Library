"use client"

import ImageInput from "@/components/image-input";
import { Button } from "@/components/ui/button";
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { cn } from "@/lib/utils";
import { zodResolver } from "@hookform/resolvers/zod";
import { Check, ChevronsUpDown } from "lucide-react";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";

const MAX_FILE_SIZE = 5000000;
const ACCEPTED_IMAGE_TYPES = ["image/jpeg", "image/jpg", "image/png", "image/webp"];

const uploadBookSchema = z.object({
  author: z.number(),
  isbn: z.string().length(10, "Niepoprawny isbn"),
  isbn13: z.string().length(13, "Niepoprawny isbn"),
  title: z.string().max(255, "Zbyt długi tytuł"),
  description: z.string().max(255, "Zbyt długi opis"),
  publication_date: z.string().date("Niepoprwna data"),
  cover: z.any()
          .refine((files) => files?.length == 1, "Zdjęcie jest wymagane")
          .refine((files) => files?.[0]?.size <= MAX_FILE_SIZE, "Maksymalny rozmiar pliku to 5 MB")
          .refine((files) => ACCEPTED_IMAGE_TYPES.includes(files?.[0]?.type), "Akceptowane typy zdjęć to .jpg, .jpeg, .png oraz .webp")
})

interface Author {
  first_name: string,
  second_name: string,
  id: number
}

const authors: Author[] = [
  {
    first_name: "Maciek",
    second_name: "Zbignieszewski",
    id: 1
  },
  {
    first_name: "Janusz",
    second_name: "Piechocinski",
    id: 2
  },
  {
    first_name: "Jurek",
    second_name: "Zdźburek",
    id: 3
  },
  {
    first_name: "Brajan",
    second_name: "Kaczek",
    id: 4
  }
]

export function BookForm() {
  /*
  To upload a book, library manager has to be logged in
  and after request is made, gateway has to set correct headers
  identifying the library. This identity data has to be stored
  somewhere too
  */
  const uploadBookForm = useForm<z.infer<typeof uploadBookSchema>>({
    resolver: zodResolver(uploadBookSchema),
    defaultValues: {
      author: undefined,
      cover: "",
      isbn: "",
      isbn13: "",
      title: "",
      description: "",
      publication_date: "",
    }
  })  
  const fileRef = uploadBookForm.register("cover");

  const onSubmit = (values: z.infer<typeof uploadBookSchema>) => {
    console.log(values)
  }

  return (
    <Form {...uploadBookForm}>
      <form onSubmit={uploadBookForm.handleSubmit(onSubmit)} className="w-full max-w-md flex flex-col gap-2">
        {/* <FormLabel>Zdjęcie okładki</FormLabel>
        <ImageInput /> */}
        <FormField 
          control={uploadBookForm.control}
          name="cover"
          render={({ field }) => {
            const [x, setX] = useState(" ");
            return (
              <FormItem>
              <FormLabel>Zdjęcie okładki</FormLabel>
              <FormControl>
                <>
                <Input 
                  type="file" 
                  accept="image/*" 
                  className="hidden"
                  { ...fileRef }
                  onChange={(e) => field.onChange(e.target?.files?.[0] ?? undefined)}
                  />
                <div 
                  className="w-full aspect-video border flex items-center justify-center"
                  onClick={() => fileRef.ref.current.}
                  >
                  {field.value ? (
                    <img src={URL.createObjectURL(field.value)} />
                  ) : (
                    <svg className="stroke-foreground" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" pointerEvents={"none"}>
                      <path d="M4 14V18H20V14M12 6L8 10M12 6L16 10M12 6V14" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  )}
                </div>
                </>
              </FormControl>
              <FormMessage />
            </FormItem>
            )
          }}
        />
        <FormField 
          control={uploadBookForm.control}
          name="title"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Tytuł</FormLabel>
              <FormControl>
                <Input placeholder="W pustyni i w puszczy" { ...field }/>
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField 
          control={uploadBookForm.control}
          name="description"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Opis</FormLabel>
              <FormControl>
                <Input placeholder="Lorem ipsum dolor" { ...field }/>
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField 
          control={uploadBookForm.control}
          name="isbn"
          render={({ field }) => (
            <FormItem>
              <FormLabel>ISBN</FormLabel>
              <FormControl>
                <Input placeholder="3161484100" { ...field }/>
              </FormControl>
            </FormItem>
          )}
        />
        <FormField 
          control={uploadBookForm.control}
          name="isbn13"
          render={({ field }) => (
            <FormItem>
              <FormLabel>ISBN 13</FormLabel>
              <FormControl>
                <Input placeholder="9783161484100" { ...field }/>
              </FormControl>
            </FormItem>
          )}
        />
        <FormField 
          control={uploadBookForm.control}
          name="publication_date"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Data publikacji</FormLabel>
              <FormControl>
                <Input type="date" placeholder="2002-09-11" { ...field }/>
              </FormControl>
            </FormItem>
          )}
        />
        <FormField 
          control={uploadBookForm.control}
          name="author"
          render={({ field }) => (
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
                    <CommandList>
                      <CommandEmpty>Nie znaleziono autora.</CommandEmpty>
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
                  </Command>
                </PopoverContent>
              </Popover>
            </FormItem>
          )}
        />
        <div className="flex justify-end mt-4">
          <Button type="submit">Dalej</Button>
        </div>
      </form>
    </Form>
  );
}