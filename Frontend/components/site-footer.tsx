export function SiteFooter() {
  return (
    <footer className="py-6 md:py-0 container md:px-8 mx-auto max-w-screen-2xl">
      <div className="flex flex-col items-center justify-between gap-4 md:h-24 md:flex-row mx-auto">
        <p className="text-balance text-center text-sm leading-loose text-muted-foreground md:text-left">
          Stolen by Muszchrom.
          From <a href="https://twitter.com/shadcn" target="_blank" rel="no_referrer" className="font-medium underline underline-offset-4">shadcn</a>.
          Code available on <a href="https://github.com/Muszchrom/Library" target="_blank" rel="no_referrer" className="font-medium underline underline-offset-4">GitHub</a>
        </p>
      </div>
    </footer>
  )
}