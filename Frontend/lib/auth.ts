import { DefaultSession, NextAuthOptions, User } from "next-auth";
import { JWT } from "next-auth/jwt"

import Credentials from "next-auth/providers/credentials"
import { gatewayServer } from "./urls";


declare module "next-auth" {
  interface User {
    id: string,
    token: string,
    username: string,
    email: string,
    phone: string,
    role: string
  }

  interface Session {
    user: {
      id: string,
      username: string,
      role: string,
      APIToken: string
    } & DefaultSession["user"]
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    id: string,
    username: string,
    role: string,
    APIToken: string
  }
}

export const authOptions: NextAuthOptions = {
  session: {
    strategy: "jwt"
  },
  providers: [
    Credentials({
      name: "credentials",
      credentials: {
        username: { label: "username", type: "text" },
        password: { label: "password", type: "password" }
      },
      async authorize(credentials) {
        try {
          const res = await fetch(gatewayServer + "auth/login", {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(credentials)
          });

          if (res.status === 403) {
            return null
          }

          const user: User = await res.json();
          if (res.ok && user) {
            return user;
          }
        } catch (e) {
          console.log(e);
        }
        return null;
      }
    })
  ], 
  callbacks: {
    jwt({ token, user }: { token: JWT, user: User }) {
      if (user) {
        token.id = user.id
        token.username = user.username
        token.role = user.role
        token.APIToken = user.token
      }
      return token;
    },
    session({ session, token }) {
      session.user.APIToken = token.APIToken;
      session.user.id = token.id;
      session.user.username = token.username;
      session.user.role = token.role;
      
      return session;
    }
  }
}