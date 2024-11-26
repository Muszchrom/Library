"use client";
import { Button } from "@/components/ui/button";
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

export type psswdValues = z.infer<typeof psswdSchema>

const psswdSchema = z.object({
  newPassword: z.string().min(6, {
    message: "Hasło musi zawierać przynajmniej 6 znaków"
  }).max(255, {
    message: "Hasło nie może mieć więcej niż 255 znaków"
  }),
  newPasswordRepeat: z.string().min(6, {
    message: "Hasło musi zawierać przynajmniej 6 znaków"
  }).max(255, {
    message: "Hasło nie może mieć więcej niż 255 znaków"
  }),
  password: z.string()
}).superRefine(({newPassword, newPasswordRepeat}, ctx) => {
  if (newPassword !== newPasswordRepeat) {
    ctx.addIssue({
      code: "custom",
      message: "Hasła się nie zgadzają",
      path: ["newPasswordRepeat"]
    })
  }
});

interface PsswdFormProps {
  onSubmit: (values: z.infer<typeof psswdSchema>) => Promise<void>
}

export default function PsswdForm({onSubmit}: PsswdFormProps) {
  const form = useForm<z.infer<typeof psswdSchema>>({
    resolver: zodResolver(psswdSchema),
    defaultValues: {
      newPassword: "",
      newPasswordRepeat: "",
      password: ""
    }
  });

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <FormField 
          control={form.control}
          name="newPassword"
          render={({field}) => (
            <FormItem>
              <FormLabel>Nowe hasło</FormLabel>
              <FormControl>
                <Input type="password" placeholder="Scaresca20" {...field}/>
              </FormControl>
              <FormDescription>
                Pole na wprowadzenie nowego hasła.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField 
          control={form.control}
          name="newPasswordRepeat"
          render={({field}) => (
            <FormItem>
              <FormLabel>Powtórz nowe hasło</FormLabel>
              <FormControl>
                <Input type="password" placeholder="Scaresca20" {...field}/>
              </FormControl>
              <FormDescription>
                Pole na powtórzenie hasła.
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