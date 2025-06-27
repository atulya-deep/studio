import * as React from "react"

import { analyzeAndSummarizeArticle } from '@/ai/flows/analyze-and-summarize-article';
import { mockNewsData } from "@/lib/mock-data";
import type { NewsArticleWithAnalysis, Competitor } from "@/types";
import { MarketVerseDashboard } from "@/components/market-verse-dashboard";
import { PageClientWrapper } from "@/components/page-client-wrapper";
import { Skeleton } from "@/components/ui/skeleton";

export default async function Home() {
  const articlesWithAnalysis: NewsArticleWithAnalysis[] = [];
  for (const article of mockNewsData) {
    try {
      const result = await analyzeAndSummarizeArticle({ articleContent: article.content });
      articlesWithAnalysis.push({
        ...article,
        summary: result.summary,
        sentiment: {
          sentiment: result.sentiment,
          confidence: result.confidence,
        },
      });
    } catch (error) {
      console.error(`Failed to process article ${article.id}:`, error);
      // Fallback in case of AI error
      articlesWithAnalysis.push({
        ...article,
        summary: "Summary not available.",
        sentiment: { sentiment: "neutral", confidence: 0 },
      });
    }
  }

  const competitors: Competitor[] = ["BASF", "EMS", "Celanese"];

  return (
    <PageClientWrapper>
      <React.Suspense fallback={<DashboardSkeleton />}>
        <MarketVerseDashboard articles={articlesWithAnalysis} competitors={competitors} dateRange={undefined} />
      </React.Suspense>
    </PageClientWrapper>
  );
}

function DashboardSkeleton() {
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
