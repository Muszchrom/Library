import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart";
import { CartesianGrid, LabelList, Line, LineChart } from "recharts";
import { RentalData } from "./rentals";

export default function RentalsChart({rentals}: {rentals: RentalData[]}) {
  const months = ["sty", "lut", "mar", "kwi", "maj", "cze", "lip", "sie", "wrz", "paź", "lis", "gru"];
  const monthsFullName = ["Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień"];
  const chartConfig: any = {
    rentedTotal: {
      label: "Wypożyczenia",
    }
  }
  
  const chartData = (() => {
    const now = new Date();
    const x = [];
    for (let i=1; i<7; i++) {
      x.push({
        month: months[now.getMonth()],
        // ! O(n^2)!!!!!!!!!
        rentedTotal: rentals.filter((rental) => (
          rental.rental.return_date != null && new Date(rental.rental.return_date).getMonth() === now.getMonth()
        )).length
      });
      chartConfig[months[now.getMonth()]] = {
        label: months[now.getMonth()],
        color: "hsl(var(--chart-5))"
      };
      now.setMonth(now.getMonth() - 1);
    }
    return x;
  })().reverse();

  const str = (() => {
    const now = new Date();
    const nowStr = `${monthsFullName[now.getMonth()]} ${now.getFullYear()}`;
    now.setMonth(now.getMonth() - 6);
    return `${monthsFullName[now.getMonth()]} ${now.getFullYear()} - ${nowStr}`
  })();

  return (
    <Card>
      <CardHeader>
        <CardTitle>Twoja historia wypożyczeń</CardTitle>
        <CardDescription>{str}</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig}>
          <LineChart
            accessibilityLayer
            data={chartData}
            margin={{
              top: 24,
              left: 24,
              bottom: 24,
              right: 24,
            }}
          >
            <CartesianGrid vertical={false} />
            <ChartTooltip
              cursor={false}
              content={
                <ChartTooltipContent
                  indicator="line"
                  nameKey="rentedTotal"
                  hideLabel
                />
              }
            />
            <Line
              dataKey="rentedTotal"
              type="natural"
              stroke="hsl(var(--chart-5))"
              strokeWidth={2}
              dot={{
                fill: "hsl(var(--chart-5))",
              }}
              activeDot={{
                r: 6,
              }}
            >
              <LabelList
                position="top"
                offset={12}
                className="fill-foreground capitalize"
                fontSize={12}
                dataKey="month"
                formatter={(value: keyof typeof chartConfig) =>
                  chartConfig[value]?.label
                }
              />
            </Line>
          </LineChart>
        </ChartContainer>
      </CardContent>
      <CardFooter className="flex-col items-start gap-2 text-sm">
        <div className="leading-none text-muted-foreground">
          Pokazuję całkowitą liczbę zwrotów z ostatnich 6-ciu miesięcy
        </div>
      </CardFooter>
    </Card>
  );
}

