'use server';

/**
 * @fileOverview An AI agent that analyzes sentiment and summarizes a given text.
 *
 * - analyzeAndSummarizeArticle - A function that handles sentiment analysis and summarization.
 * - ArticleAnalysisInput - The input type for the analyzeAndSummarizeArticle function.
 * - ArticleAnalysisOutput - The return type for the analyzeAndSummarizeArticle function.
 */

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const ArticleAnalysisInputSchema = z.object({
  articleContent: z
    .string()
    .describe('The content of the news article to be analyzed and summarized.'),
});
export type ArticleAnalysisInput = z.infer<typeof ArticleAnalysisInputSchema>;

const ArticleAnalysisOutputSchema = z.object({
  summary: z.string().describe('A concise summary of the news article.'),
  sentiment: z
    .enum(['positive', 'negative', 'neutral'])
    .describe('The sentiment of the text.'),
  confidence: z
    .number()
    .min(0)
    .max(1)
    .describe('The confidence level of the sentiment analysis (0 to 1).'),
});
export type ArticleAnalysisOutput = z.infer<typeof ArticleAnalysisOutputSchema>;

export async function analyzeAndSummarizeArticle(input: ArticleAnalysisInput): Promise<ArticleAnalysisOutput> {
  return analyzeAndSummarizeArticleFlow(input);
}

const prompt = ai.definePrompt({
  name: 'analyzeAndSummarizeArticlePrompt',
  input: {schema: ArticleAnalysisInputSchema},
  output: {schema: ArticleAnalysisOutputSchema},
  prompt: `You are an expert news analyst. First, summarize the following news article concisely. Second, analyze the sentiment of the article. Return the sentiment as either "positive", "negative", or "neutral", along with a confidence score between 0 and 1.

Article: {{{articleContent}}}
`,
});

const analyzeAndSummarizeArticleFlow = ai.defineFlow(
  {
    name: 'analyzeAndSummarizeArticleFlow',
    inputSchema: ArticleAnalysisInputSchema,
    outputSchema: ArticleAnalysisOutputSchema,
  },
  async input => {
    const {output} = await prompt(input);
    return output!;
  }
);
