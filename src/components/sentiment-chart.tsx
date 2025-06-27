"use client"

import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from "recharts"

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { ChartTooltipContent, ChartTooltip, ChartContainer } from "@/components/ui/chart"

interface SentimentChartProps {
  data: {
    positive: number
    negative: number
    neutral: number
  }
}

export function SentimentChart({ data }: SentimentChartProps) {
    const chartData = [
    { name: "Positive", value: data.positive, fill: "hsl(var(--chart-2))" },
    { name: "Negative", value: data.negative, fill: "hsl(var(--destructive))" },
    { name: "Neutral", value: data.neutral, fill: "hsl(var(--chart-4))" },
  ]
  
  const chartConfig = {
    value: {
      label: "Count",
    },
    Positive: {
      label: "Positive",
      color: "hsl(var(--chart-2))",
    },
    Negative: {
      label: "Negative",
      color: "hsl(var(--destructive))",
    },
    Neutral: {
      label: "Neutral",
      color: "hsl(var(--chart-4))",
    },
  }


  return (
    <Card>
      <CardHeader>
        <CardTitle>Sentiment Overview</CardTitle>
        <CardDescription>Analysis of news articles sentiment</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig} className="h-[250px] w-full">
            <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} layout="vertical" margin={{ left: 10 }}>
                    <XAxis type="number" hide />
                    <YAxis dataKey="name" type="category" tickLine={false} axisLine={false} tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 12 }} width={80} />
                    <Tooltip
                        cursor={{ fill: "hsl(var(--muted))" }}
                        content={<ChartTooltipContent indicator="dot" />}
                    />
                    <Bar dataKey="value" radius={4} />
                </BarChart>
            </ResponsiveContainer>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
