export type Competitor = "BASF" | "EMS" | "Celanese";

export interface NewsArticle {
  id: string;
  competitor: Competitor;
  title: string;
  content: string;
  source: string;
  url: string;
  date: string; // ISO 8601 format
  imageUrl?: string;
  imageHint?: string;
}

export type NewsArticleWithAnalysis = NewsArticle & {
  summary: string;
  sentiment: {
    sentiment: "positive" | "negative" | "neutral";
    confidence: number;
  };
};

export type SentimentData = {
  name: 'Sentiments';
  positive: number;
  negative: number;
  neutral: number;
};
