"use client"

import { Button } from "@/components/ui/button"
import { DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog"
import { Form, FormControl, FormField, FormItem, FormLabel } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Author } from "@/interfaces"
import { zodResolver } from "@hookform/resolvers/zod"
import { useSession } from "next-auth/react"
import { useForm } from "react-hook-form"
import { toast } from "sonner"
import { z } from "zod"

const uploadAuthorSchema = z.object({
  first_name: z.string(),
  second_name: z.string()
})

export default function AuthorForm({xdd}: {xdd: (author: Author) => void}) {
  const { data } = useSession();
  
  const uploadAuthorForm = useForm<z.infer<typeof uploadAuthorSchema>>({
    resolver: zodResolver(uploadAuthorSchema),
    defaultValues: {
      first_name: "",
      second_name: "",
    }
  })  
  const onSubmit = async (values: z.infer<typeof uploadAuthorSchema>) => {
    const res = await fetch("http://localhost:8081/waz/authors/", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${data?.user.APIToken}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        first_name: values.first_name,
        second_name: values.second_name
      })
    });
    const author = await res.json();
    console.log(author);

    // const data = await res.json();
    if (author.message) {
      toast.error("Wysyłanie nie powiodło się", {
        description: author.message
      });
    } else {
      toast.success("Dodano nowego autora");
      xdd(author);
    }
  }

  return (
      <DialogContent className="sm:max-w-[425px] rounded-lg" >
        <DialogHeader>
          <DialogTitle>Dodaj autora</DialogTitle>
          <DialogDescription>Dodaj nowego autora do bazy danych</DialogDescription>
        </DialogHeader>

        {/* <form onSubmit={(e) => {e.preventDefault();e.stopPropagation()}} className="w-full flex flex-col gap-2">
          <label>Imię</label>
          <Input type="text" placeholder="Jan" />
          <label>Nazwisko</label>
          <Input type="text" placeholder="Kowlaski" />
          <div className="flex justify-end mt-3">
            <Button type="submit">Dalej</Button>
          </div>
        </form> */}
        <Form {...uploadAuthorForm}>
          <form onSubmit={uploadAuthorForm.handleSubmit(onSubmit)} className="w-full flex flex-col gap-2">
            <FormField 
              control={uploadAuthorForm.control} 
              name="first_name" 
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Imię</FormLabel>
                  <FormControl>
                    <Input type="text" placeholder="Jan" {...field} />
                  </FormControl>
                </FormItem>
              )} />

            <FormField 
              control={uploadAuthorForm.control} 
              name="second_name" 
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Nazwisko</FormLabel>
                  <FormControl>
                    <Input type="text" placeholder="Jan" {...field} />
                  </FormControl>
                </FormItem>
              )} />
            <div className="flex justify-end mt-3">
              <Button>
                Dodaj
              </Button>
            </div>
          </form>
        </Form>
      </DialogContent>
  )
}