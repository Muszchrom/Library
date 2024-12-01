"use client"

import ImageInput from "./image-input";
import { Button } from "@/components/ui/button";
import { Dialog, DialogTrigger } from "@/components/ui/dialog";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Author } from "@/interfaces";
import AuthorForm from "./author-form";
import AuthorInput from "./author-input";
import { SessionProvider } from "next-auth/react";

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

export function BookForm() {
  /*
  To upload a book, library manager has to be logged in
  and after request is made, gateway has to set correct headers
  identifying the library. This identity data has to be stored
  somewhere too
  */
  const [authors, setAuthors] = useState<Author[]>([]);
  useEffect(() => {
    (async () => {
      const res = await fetch("http://localhost:8081/waz/authors/");

      const ath = await res.json();
      setAuthors(ath)
    })()
  }, [])


  // undefined because typescript doesnt like any. It has to do with useFormContext stuff
  const uploadBookForm = useForm<z.infer<typeof uploadBookSchema>, undefined>({
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
    <Dialog>
      <Form {...uploadBookForm}>
        <form onSubmit={uploadBookForm.handleSubmit(onSubmit)} className="w-full max-w-md flex flex-col gap-2">
          {/* <FormLabel>Zdjęcie okładki</FormLabel>
          <ImageInput /> */}
          <FormField 
            control={uploadBookForm.control}
            name="cover"
            render={({ field }) => <ImageInput field={field} fileRef={fileRef} />}
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
                  <Input className="dark:[color-scheme:dark] block" type="date" placeholder="2002-09-11" { ...field }/>
                </FormControl>
              </FormItem>
            )}
          />
          <FormField 
            control={uploadBookForm.control}
            name="author"
            render={({ field }) => (
              <AuthorInput authors={authors} field={field} uploadBookForm={uploadBookForm}>
                <DialogTrigger asChild>
                  <Button type="button">Dodaj</Button>
                </DialogTrigger>
              </AuthorInput>
            )
          }
          />
          <div className="flex justify-end mt-4">
            <Button type="submit">Dalej</Button>
          </div>
        </form>
      </Form>
      <div>
        <SessionProvider>
          <AuthorForm xdd={(a) => {setAuthors(authors.concat(a))}}/>
        </SessionProvider>
      </div>
    </Dialog>
  );
}