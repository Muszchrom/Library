"use client";
import { SessionProvider } from "next-auth/react";
import React from "react";
import LogInOutButton from "./log-in-out-button";

export default function LogInOutThing() {
  return (
    <SessionProvider>
      <LogInOutButton />
    </SessionProvider>
  )
}