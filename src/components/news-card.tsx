"use client"

import Image from "next/image"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Separator } from "@/components/ui/separator"
import type { NewsArticleWithAnalysis } from "@/types"
import { TrendingUp, TrendingDown, Minus, ExternalLink } from "lucide-react"
import { format } from 'date-fns'

interface NewsCardProps {
  article: NewsArticleWithAnalysis
}

const SentimentIndicator = ({ sentiment }: { sentiment: 'positive' | 'negative' | 'neutral' }) => {
  if (sentiment === 'positive') {
    return (
      <Badge variant="outline" className="border-green-500/50 text-green-600 dark:text-green-400 bg-green-500/10">
        <TrendingUp className="mr-1 h-4 w-4" />
        Positive
      </Badge>
    )
  }
  if (sentiment === 'negative') {
    return (
      <Badge variant="destructive">
        <TrendingDown className="mr-1 h-4 w-4" />
        Negative
      </Badge>
    )
  }
  return (
    <Badge variant="secondary">
      <Minus className="mr-1 h-4 w-4" />
      Neutral
    </Badge>
  )
}

export function NewsCard({ article }: NewsCardProps) {
  return (
    <Card className="flex flex-col overflow-hidden group transition-all duration-300 hover:shadow-md">
       {article.imageUrl && (
        <div className="relative aspect-video overflow-hidden">
          <Image
            src={article.imageUrl}
            alt={article.title}
            fill
            className="object-cover group-hover:scale-105 transition-transform duration-300"
            data-ai-hint={article.imageHint}
          />
        </div>
      )}
      <CardHeader>
        <div className="flex justify-between items-start gap-2">
          <CardTitle className="text-lg leading-tight group-hover:text-primary transition-colors">{article.title}</CardTitle>
          <div className="flex-shrink-0">
             <SentimentIndicator sentiment={article.sentiment.sentiment} />
          </div>
        </div>
        <CardDescription>
          {format(new Date(article.date), "PPP")} &middot; {article.source}
        </CardDescription>
      </CardHeader>
      <CardContent className="flex-grow">
        <p className="text-sm text-muted-foreground line-clamp-3">{article.summary}</p>
      </CardContent>
      <CardFooter>
        <Dialog>
          <DialogTrigger asChild>
            <Button variant="secondary" size="sm">Read More</Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-3xl">
            <DialogHeader>
              <DialogTitle>{article.title}</DialogTitle>
              <DialogDescription className="flex items-center gap-4 pt-2">
                <span>{format(new Date(article.date), "PPPP")}</span>
                <Separator orientation="vertical" className="h-4" />
                <span>{article.source}</span>
                <Separator orientation="vertical" className="h-4" />
                <SentimentIndicator sentiment={article.sentiment.sentiment} />
              </DialogDescription>
            </DialogHeader>
            <ScrollArea className="h-[50vh] pr-4">
              <div className="prose prose-sm dark:prose-invert max-w-none">
                 <p className="font-semibold text-foreground">Summary:</p>
                 <p>{article.summary}</p>
                 <Separator className="my-4"/>
                 <p className="font-semibold text-foreground">Full Article:</p>
                <p>{article.content}</p>
              </div>
            </ScrollArea>
            <div className="flex justify-end">
              <Button asChild variant="link" className="text-accent-foreground">
                <a href={article.url} target="_blank" rel="noopener noreferrer">
                  View Original Source <ExternalLink className="ml-2 h-4 w-4" />
                </a>
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </CardFooter>
    </Card>
  )
}
