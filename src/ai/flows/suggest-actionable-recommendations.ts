'use server';
/**
 * @fileOverview An AI agent that suggests actionable recommendations based on marketing data analysis.
 *
 * - suggestActionableRecommendations - A function that handles the generation of actionable recommendations.
 * - SuggestActionableRecommendationsInput - The input type for the suggestActionableRecommendations function.
 * - SuggestActionableRecommendationsOutput - The return type for the suggestActionableRecommendations function.
 */

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const SuggestActionableRecommendationsInputSchema = z.object({
  clientData: z
    .string()
    .describe('The marketing data for a specific client, including metrics across various channels.'),
  insights: z
    .string()
    .describe('Insights derived from the client data, highlighting anomalies and trends.'),
});
export type SuggestActionableRecommendationsInput = z.infer<
  typeof SuggestActionableRecommendationsInputSchema
>;

const SuggestActionableRecommendationsOutputSchema = z.object({
  recommendations: z
    .string()
    .describe('A list of actionable recommendations based on the data and insights.'),
});
export type SuggestActionableRecommendationsOutput = z.infer<
  typeof SuggestActionableRecommendationsOutputSchema
>;

export async function suggestActionableRecommendations(
  input: SuggestActionableRecommendationsInput
): Promise<SuggestActionableRecommendationsOutput> {
  return suggestActionableRecommendationsFlow(input);
}

const prompt = ai.definePrompt({
  name: 'suggestActionableRecommendationsPrompt',
  input: {schema: SuggestActionableRecommendationsInputSchema},
  output: {schema: SuggestActionableRecommendationsOutputSchema},
  prompt: `You are an AI marketing assistant specializing in generating actionable recommendations based on data analysis.

  Based on the client's marketing data and identified insights, provide a list of concrete and actionable recommendations to improve marketing outcomes. These recommendations should address any issues or capitalize on opportunities.

  Client Data: {{{clientData}}}
  Insights: {{{insights}}}
  Recommendations:
  `,
});

const suggestActionableRecommendationsFlow = ai.defineFlow(
  {
    name: 'suggestActionableRecommendationsFlow',
    inputSchema: SuggestActionableRecommendationsInputSchema,
    outputSchema: SuggestActionableRecommendationsOutputSchema,
  },
  async input => {
    const {output} = await prompt(input);
    return output!;
  }
);
