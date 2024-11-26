"use client";
import { Button } from "@/components/ui/button";
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

export type unameValues = z.infer<typeof unameSchema>

const unameSchema = z.object({
  username: z.string().min(3, {
    message: "Nazwa użytkownika musi zawierać przynajmniej 3 znaki"
  }).max(24, {
    message: "Nazwa użytkownika nie może mieć więcej niż 255 znaków"
  }),
  password: z.string()
});

interface UnameFormProps {
  onSubmit: (values: z.infer<typeof unameSchema>) => Promise<void>
}

export default function UnameForm({onSubmit}: UnameFormProps) {
  const form = useForm<z.infer<typeof unameSchema>>({
    resolver: zodResolver(unameSchema),
    defaultValues: {
      username: "",
      password: ""
    }
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <FormField 
          control={form.control}
          name="username"
          render={({field}) => (
            <FormItem>
              <FormLabel>Nowa nazwa użytkownika</FormLabel>
              <FormControl>
                <Input type="text" placeholder="Scaresca20" {...field}/>
              </FormControl>
              <FormDescription>
                Pole na wprowadzenie nazwy użytkownika.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField 
          control={form.control}
          name="password"
          render={({field}) => (
            <FormItem>
              <FormLabel>Hasło</FormLabel>
              <FormControl>
                <Input type="password" placeholder="*********" {...field}/>
              </FormControl>
              <FormDescription>
                Pole na wprowadzenie hasła.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <div className="flex justify-end">
          <Button type="submit">Dalej</Button>
        </div>
      </form>
    </Form>
  );
}