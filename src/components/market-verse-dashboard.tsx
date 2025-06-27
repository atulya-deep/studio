"use client"

import * as React from "react"
import { addDays, isWithinInterval } from 'date-fns'
import { DateRange } from "react-day-picker"

import type { NewsArticleWithAnalysis, Competitor, SentimentData } from "@/types"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { SentimentChart } from "./sentiment-chart"
import { NewsCard } from "./news-card"
import { Skeleton } from "@/components/ui/skeleton"

interface MarketVerseDashboardProps {
  articles: NewsArticleWithAnalysis[]
  competitors: Competitor[]
  dateRange: DateRange | undefined
}

export function MarketVerseDashboard({ articles, competitors, dateRange }: MarketVerseDashboardProps) {
  const [activeTab, setActiveTab] = React.useState<Competitor>(competitors[0])
  const [isClient, setIsClient] = React.useState(false)

  React.useEffect(() => {
    setIsClient(true)
  }, [])
  
  const filteredArticles = React.useMemo(() => {
    return articles.filter(article => {
      if (article.competitor !== activeTab) return false
      if (!dateRange?.from) return true
      const articleDate = new Date(article.date)
      const toDate = dateRange.to ?? dateRange.from
      return isWithinInterval(articleDate, { start: dateRange.from, end: addDays(toDate, 1) })
    })
  }, [articles, activeTab, dateRange])

  const sentimentCounts = React.useMemo(() => {
    return filteredArticles.reduce(
      (acc, article) => {
        if (article.sentiment.sentiment === 'positive') acc.positive += 1
        else if (article.sentiment.sentiment === 'negative') acc.negative += 1
        else acc.neutral += 1
        return acc
      },
      { positive: 0, negative: 0, neutral: 0 }
    )
  }, [filteredArticles])

  if (!isClient) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-1/3" />
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <Skeleton className="h-[340px] lg:col-span-1" />
          <div className="lg:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-6">
            {[...Array(4)].map((_, i) => <Skeleton key={i} className="h-[250px]" />)}
          </div>
        </div>
      </div>
    )
  }

  return (
    <Tabs value={activeTab} onValueChange={(value) => setActiveTab(value as Competitor)}>
      <TabsList className="mb-4">
        {competitors.map(c => (
          <TabsTrigger key={c} value={c}>{c}</TabsTrigger>
        ))}
      </TabsList>
      {competitors.map(c => (
        <TabsContent key={c} value={c} className="mt-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-1">
              <SentimentChart data={sentimentCounts} />
            </div>
            <div className="lg:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-6">
              {filteredArticles.length > 0 ? (
                filteredArticles.map(article => (
                  <NewsCard key={article.id} article={article} />
                ))
              ) : (
                <div className="md:col-span-2 text-center text-muted-foreground py-16">
                    <p>No news articles found for the selected criteria.</p>
                </div>
              )}
            </div>
          </div>
        </TabsContent>
      ))}
    </Tabs>
  )
}
