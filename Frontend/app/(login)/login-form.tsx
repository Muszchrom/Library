"use client"

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { toast } from "sonner";
import { useRouter } from "next/navigation";
import { signIn } from "next-auth/react";

const loginSchema = z.object({
  username: z.string().min(3, {
    message: "Nazwa użytkownika musi zawierać przynajmniej 3 znaki"
  }).max(24, {
    message: "Nazwa użytkownika nie może mieć więcej niż 255 znaków"
  }),
  password: z.string().min(6, {
    message: "Hasło musi zawierać przynajmniej 6 znaków"
  }).max(255, {
    message: "Hasło nie może mieć więcej niż 255 znaków"
  })
})

const registerSchema = z.object({
    username: z.string().min(3, {
      message: "Nazwa użytkownika musi zawierać przynajmniej 3 znaki"
    }).max(24, {
      message: "Nazwa użytkownika nie może mieć więcej niż 255 znaków"
    }),
    password: z.string().min(6, {
      message: "Hasło musi zawierać przynajmniej 6 znaków"
    }).max(255, {
      message: "Hasło nie może mieć więcej niż 255 znaków"
    }),
    confirmPassword: z.string(),
  }).superRefine(({confirmPassword, password}, ctx) => {
    if (confirmPassword !== password) {
      ctx.addIssue({
        code: "custom",
        message: "Hasła się nie zgadzają",
        path: ["confirmPassword"]
      })
    }
  })

export function LoginForm({formType}: {formType: "login" | "register"}) {
  const router = useRouter();

  const loginForm = useForm<z.infer<typeof loginSchema>>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      username: "",
      password: ""
    }
  })

  const registerForm = useForm<z.infer<typeof registerSchema>>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      username: "",
      password: "",
      confirmPassword: ""
    }
  })

  async function onSubmitLogin(values: z.infer<typeof loginSchema>) {
    const res = await signIn("credentials", {
      username: values.username,
      password: values.password,
      redirect: false
    })

    if (!res?.error) {
      router.push("/");
      toast.success("Jesteś teraz zalogowany/a!");
    } else {
      toast.error("Logowanie nie powiodło się", {
        description: "Niepoprawna nazwa użytkownika i/lub hasło"
      })
    }
  }

  async function onSubmitRegister(values: z.infer<typeof registerSchema>) {
    const res = await fetch("http://localhost:8081/auth/login", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(values)
    })
    
    if (res.status === 200) {
      onSubmitLogin(values); // login directly after register
    } else if (res.status === 400) {
      toast.error("Rejestracja nie powiodła się", {
        description: "Niepoprawna dane rejestracji lub podana nazwa użytkownika już istnieje"
      })
    } else {
      toast.error("Rejestracja nie powiodła się", {
        description: "Kod błędu: " + res.status
      })
    }
  }

  return formType === "login" ? (
    <Form {...loginForm}>
      <form onSubmit={loginForm.handleSubmit(onSubmitLogin)} className="space-y-4">
        <FormField
          control={loginForm.control}
          name="username"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Login</FormLabel>
              <FormControl>
                <Input placeholder="Scaresca20" {...field} />
              </FormControl>
              <FormDescription>
                Pole na wprowadzenie loginu.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
          />

        <FormField
          control={loginForm.control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Hasło</FormLabel>
              <FormControl>
                <Input type="password" placeholder="Super silne hasło" {...field} />
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
  ) : (
    <Form {...registerForm}>
      <form onSubmit={registerForm.handleSubmit(onSubmitRegister)} className="space-y-4">
        <FormField
          control={registerForm.control}
          name="username"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Login</FormLabel>
              <FormControl>
                <Input placeholder="Scaresca20" {...field} />
              </FormControl>
              <FormDescription>
                Pole na wprowadzenie loginu.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
          />

        <FormField
          control={registerForm.control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Hasło</FormLabel>
              <FormControl>
                <Input type="password" placeholder="Super silne hasło" {...field} />
              </FormControl>
              <FormDescription>
                Pole na wprowadzenie hasła.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
          />
        <FormField
          control={registerForm.control}
          name="confirmPassword"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Powtórz hasło</FormLabel>
              <FormControl>
                <Input type="password" placeholder="Super silne hasło" {...field} />
              </FormControl>
              <FormDescription>
                Pole na ponowne wprowadzenie hasła.
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
  )
}
