import { Skeleton } from "@/components/ui/skeleton";

export default function BookCardSkeleton() {
  return (
    <div className="flex flex-col h-full">
      <div className="w-full h-56">
        <Skeleton className="w-full h-full"/>
      </div>
      <div className="w-36 h-5 mt-2">
        <Skeleton className="w-full h-full rounded-md"/>
      </div>
      <div className="flex h-5 mt-2 justify-between gap-2">
        <Skeleton className="w-28 h-full rounded-md"/>
        <Skeleton className="w-16 h-full rounded-md"/>
      </div>
    </div>
  );
}
