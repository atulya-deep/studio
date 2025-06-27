"use client"

import { Pie, PieChart, ResponsiveContainer } from "recharts"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  ChartTooltipContent,
  ChartTooltip,
  ChartContainer,
  ChartLegend,
  ChartLegendContent,
} from "@/components/ui/chart"
import type { ChartConfig } from "@/components/ui/chart"
import { TrendingUp, TrendingDown, Minus } from "lucide-react"

interface SentimentChartProps {
  data: {
    positive: number
    negative: number
    neutral: number
  }
}

const chartConfig = {
  positive: {
    label: "Positive",
    color: "hsl(var(--chart-2))",
    icon: TrendingUp,
  },
  negative: {
    label: "Negative",
    color: "hsl(var(--destructive))",
    icon: TrendingDown,
  },
  neutral: {
    label: "Neutral",
    color: "hsl(var(--chart-4))",
    icon: Minus,
  },
} satisfies ChartConfig

export function SentimentChart({ data }: SentimentChartProps) {
  const chartData = [
    { name: "positive", value: data.positive, fill: "var(--color-positive)" },
    { name: "negative", value: data.negative, fill: "var(--color-negative)" },
    { name: "neutral", value: data.neutral, fill: "var(--color-neutral)" },
  ]
  const total = data.positive + data.negative + data.neutral

  return (
    <Card>
      <CardHeader>
        <CardTitle>Sentiment Overview</CardTitle>
        <CardDescription>Analysis of news articles sentiment</CardDescription>
      </CardHeader>
      <CardContent className="flex items-center justify-center">
        {total > 0 ? (
          <ChartContainer
            config={chartConfig}
            className="h-[250px] w-full max-w-[250px]"
          >
            <PieChart>
              <ChartTooltip
                cursor={false}
                content={<ChartTooltipContent hideLabel />}
              />
              <Pie
                data={chartData}
                dataKey="value"
                nameKey="name"
                innerRadius={60}
                strokeWidth={5}
              >
              </Pie>
              <ChartLegend
                content={<ChartLegendContent nameKey="name" />}
                className="-mt-4"
              />
            </PieChart>
          </ChartContainer>
        ) : (
          <div className="h-[250px] flex items-center justify-center text-muted-foreground">
            No data to display
          </div>
        )}
      </CardContent>
    </Card>
  )
}
