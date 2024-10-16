import { SiteFooter } from "@/components/site-footer"
import { SiteHeader } from "@/components/site-header"

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <>
      <SiteHeader />
        <main className="flex-1">
          <div className="border-b">
            <div className="container flex-1 items-start mx-auto px-4 md:px-8 max-w-screen-2xl">
              {children}
            </div>
          </div>
        </main>
      <SiteFooter />
    </>
  )
}
