import React from "react";

export default function SeparatorWithText({children}: {children: React.ReactNode}) {
  return (
    <div className="relative">
      <div className="mt-6">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t bg-border h-[1px]"></div>
        </div>
        <div className="relative flex justify-center text-sm">
          <span className="bg-background px-2 text-muted-foreground">
            {children}
          </span>
        </div>
      </div>
    </div>
  )
}