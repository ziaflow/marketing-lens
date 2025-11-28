'use server';

/**
 * @fileOverview Generates insightful summaries and identifies key trends from marketing data.
 *
 * - generateInsights - A function that generates marketing insights.
 * - GenerateInsightsInput - The input type for the generateInsights function.
 * - GenerateInsightsOutput - The return type for the generateInsights function.
 */

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const GenerateInsightsInputSchema = z.object({
  clientData: z
    .string()
    .describe(
      'Marketing data for a specific client, including metrics from various platforms like Google Analytics, social media, and ad campaigns.'
    ),
  insightsRequest: z
    .string()
    .describe(
      'Optional string that can be used to ask for specific insight requests, such as focusing on a specific type of marketing data or platform.'
    )
    .optional(),
});
export type GenerateInsightsInput = z.infer<typeof GenerateInsightsInputSchema>;

const GenerateInsightsOutputSchema = z.object({
  summary: z.string().describe('A concise summary of the marketing data.'),
  keyTrends: z.string().describe('Identified key trends and patterns in the data.'),
  suggestedActions: z
    .string()
    .describe('Suggested actions based on the insights and trends.'),
});
export type GenerateInsightsOutput = z.infer<typeof GenerateInsightsOutputSchema>;

export async function generateInsights(input: GenerateInsightsInput): Promise<GenerateInsightsOutput> {
  return generateInsightsFlow(input);
}

const prompt = ai.definePrompt({
  name: 'generateInsightsPrompt',
  input: {schema: GenerateInsightsInputSchema},
  output: {schema: GenerateInsightsOutputSchema},
  prompt: `You are an AI marketing analyst. Analyze the following marketing data and generate a summary, identify key trends, and suggest actions.

Marketing Data: {{{clientData}}}

{% if insightsRequest %}Specific Insight Request: {{{insightsRequest}}}{% endif %}

Summary: 
Key Trends:
Suggested Actions: `,
});

const generateInsightsFlow = ai.defineFlow(
  {
    name: 'generateInsightsFlow',
    inputSchema: GenerateInsightsInputSchema,
    outputSchema: GenerateInsightsOutputSchema,
  },
  async input => {
    const {output} = await prompt(input);
    return output!;
  }
);
