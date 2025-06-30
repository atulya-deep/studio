'use server';

/**
 * @fileOverview An AI agent that analyzes sentiment, summarizes a given text, and generates a relevant image.
 *
 * - analyzeAndSummarizeArticle - A function that handles sentiment analysis, summarization, and image generation.
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

const TextAnalysisSchema = z.object({
  summary: z
    .string()
    .describe(
      'A detailed and descriptive summary of the news article, about 3-4 sentences long.'
    ),
  sentiment: z
    .enum(['positive', 'negative', 'neutral'])
    .describe('The sentiment of the text.'),
  confidence: z
    .number()
    .min(0)
    .max(1)
    .describe('The confidence level of the sentiment analysis (0 to 1).'),
  imageHint: z
    .string()
    .describe(
      "A one or two-word hint representing the main subject of the article for image generation purposes. Max two words."
    ),
});

const ArticleAnalysisOutputSchema = TextAnalysisSchema.extend({
  imageUrl: z
    .string()
    .url()
    .describe('A data URI for a generated image relevant to the article.'),
});
export type ArticleAnalysisOutput = z.infer<typeof ArticleAnalysisOutputSchema>;

export async function analyzeAndSummarizeArticle(
  input: ArticleAnalysisInput
): Promise<ArticleAnalysisOutput> {
  return analyzeAndSummarizeArticleFlow(input);
}

const textPrompt = ai.definePrompt({
  name: 'analyzeAndSummarizeArticlePrompt',
  input: {schema: ArticleAnalysisInputSchema},
  output: {schema: TextAnalysisSchema},
  prompt: `You are an expert news analyst. First, provide a detailed and descriptive summary of the following news article (3-4 sentences). Second, analyze the sentiment of the article. Return the sentiment as either "positive", "negative", or "neutral", along with a confidence score between 0 and 1. Finally, provide a one or two-word hint for generating an image that represents the article's main subject.

Article: {{{articleContent}}}
`,
});

const analyzeAndSummarizeArticleFlow = ai.defineFlow(
  {
    name: 'analyzeAndSummarizeArticleFlow',
    inputSchema: ArticleAnalysisInputSchema,
    outputSchema: ArticleAnalysisOutputSchema,
  },
  async (input) => {
    const { output: textOutput } = await textPrompt(input);
    if (!textOutput) {
        throw new Error("Failed to get text analysis from AI.");
    }

    const { media } = await ai.generate({
        model: 'googleai/gemini-2.0-flash-preview-image-generation',
        prompt: `Generate a photorealistic image of: ${textOutput.imageHint}`,
        config: {
            responseModalities: ['TEXT', 'IMAGE'],
        },
    });
    
    const imageUrl = media?.url || 'https://placehold.co/600x400.png';

    return {
        ...textOutput,
        imageUrl,
    };
  }
);
