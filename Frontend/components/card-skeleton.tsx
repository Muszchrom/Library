import { Skeleton } from "@/components/ui/skeleton";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function CardSkeleton() {
  return (
    <Card>
      <CardHeader>
        <CardTitle><Skeleton className="w-1/2 h-5"/></CardTitle>
      </CardHeader>
      <CardContent>
        <Skeleton className="aspect-video w-full h-full"/>
      </CardContent>
    </Card>
  );
}