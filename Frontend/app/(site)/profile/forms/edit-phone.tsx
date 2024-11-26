"use client";
import { Button } from "@/components/ui/button";
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

export type phoneValues = z.infer<typeof phoneSchema>

const phoneSchema = z.object({
  phone: z.string().regex(
    new RegExp(/^([0-9]{3}) ?([0-9]{3}) ?([0-9]{3})$/),
    "Niepoprawny numer telefonu"
  ),
  password: z.string()
});

interface PhoneFormProps {
  onSubmit: (values: z.infer<typeof phoneSchema>) => Promise<void>
}

export default function PhoneForm({onSubmit}: PhoneFormProps) {
  const form = useForm<z.infer<typeof phoneSchema>>({
    resolver: zodResolver(phoneSchema),
    defaultValues: {
      phone: "",
      password: ""
    }
  });

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <FormField 
          control={form.control}
          name="phone"
          render={({field}) => (
            <FormItem>
              <FormLabel>Nowy email</FormLabel>
              <FormControl>
                <Input type="tel" placeholder="123456789" {...field}/>
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