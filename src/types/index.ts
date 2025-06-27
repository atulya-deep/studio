import type { AnalyzeSentimentOutput } from "@/ai/flows/analyze-sentiment";
import type { SummarizeArticleOutput } from "@/ai/flows/summarize-article";

export type Competitor = "BASF" | "EMS" | "Celanese";

export interface NewsArticle {
  id: string;
  competitor: Competitor;
  title: string;
  content: string;
  source: string;
  url: string;
  date: string; // ISO 8601 format
}

export type NewsArticleWithAnalysis = NewsArticle & {
  summary: SummarizeArticleOutput['summary'];
  sentiment: AnalyzeSentimentOutput;
};

export type SentimentData = {
  name: 'Sentiments';
  positive: number;
  negative: number;
  neutral: number;
};
