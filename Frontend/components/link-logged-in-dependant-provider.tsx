"use client";
import { SessionProvider } from "next-auth/react";
import React from "react";
import LinkLoggedInDependant, { LinkLoggedInDependantProps } from "./link-logged-in-dependant";

export default function LinkLoggedInDependantProvider(props: LinkLoggedInDependantProps) {
  return (
    <SessionProvider>
      <LinkLoggedInDependant {...props}>
      
      </LinkLoggedInDependant>
    </SessionProvider>
  )
}