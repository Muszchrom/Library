"use client";
import { Button } from "@/components/ui/button";
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

export type emailValues = z.infer<typeof emailSchema>

const emailSchema = z.object({
  email: z.string().email("Podaj poprawny adres email"),
  password: z.string()
});

interface EmailFormProps {
  onSubmit: (values: z.infer<typeof emailSchema>) => Promise<void>
}

export default function EmailForm({onSubmit}: EmailFormProps) {
  const form = useForm<z.infer<typeof emailSchema>>({
    resolver: zodResolver(emailSchema),
    defaultValues: {
      email: "",
      password: ""
    }
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <FormField 
          control={form.control}
          name="email"
          render={({field}) => (
            <FormItem>
              <FormLabel>Nowy email</FormLabel>
              <FormControl>
                <Input type="email" placeholder="marek.c@gmail.com" {...field}/>
              </FormControl>
              <FormDescription>
                Pole na wprowadzenie email.
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