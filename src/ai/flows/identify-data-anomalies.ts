'use server';
/**
 * @fileOverview This file defines a Genkit flow for identifying anomalies in marketing data.
 *
 * The flow takes marketing data as input and uses a GenAI model to detect anomalies,
 * providing insights and suggesting actions.
 *
 * @interface IdentifyDataAnomaliesInput - The input type for the identifyDataAnomalies function.
 * @interface IdentifyDataAnomaliesOutput - The output type for the identifyDataAnomalies function.
 * @function identifyDataAnomalies - A function that handles the anomaly detection process.
 */

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const IdentifyDataAnomaliesInputSchema = z.object({
  clientName: z.string().describe('The name of the client.'),
  dataDescription: z.string().describe('A description of the data being analyzed, including the source and metrics.'),
  data: z.string().describe('The marketing data in a suitable format for analysis, such as JSON or CSV.'),
});
export type IdentifyDataAnomaliesInput = z.infer<typeof IdentifyDataAnomaliesInputSchema>;

const IdentifyDataAnomaliesOutputSchema = z.object({
  anomalies: z.array(z.string()).describe('A list of identified anomalies in the data.'),
  insights: z.array(z.string()).describe('Insights derived from the identified anomalies.'),
  suggestedActions: z.array(z.string()).describe('Suggested actions based on the anomalies and insights.'),
});
export type IdentifyDataAnomaliesOutput = z.infer<typeof IdentifyDataAnomaliesOutputSchema>;

export async function identifyDataAnomalies(input: IdentifyDataAnomaliesInput): Promise<IdentifyDataAnomaliesOutput> {
  return identifyDataAnomaliesFlow(input);
}

const prompt = ai.definePrompt({
  name: 'identifyDataAnomaliesPrompt',
  input: {schema: IdentifyDataAnomaliesInputSchema},
  output: {schema: IdentifyDataAnomaliesOutputSchema},
  prompt: `You are an AI assistant specialized in identifying anomalies in marketing data.

  Analyze the provided data for the client "{{{clientName}}}", described as follows: {{{dataDescription}}}.
  The data is:
  {{{data}}}

  Identify any anomalies, derive insights from these anomalies, and suggest actions to address them.

  Format your output as a JSON object with the following keys:
  - anomalies: A list of identified anomalies in the data.
  - insights: Insights derived from the identified anomalies.
  - suggestedActions: Suggested actions based on the anomalies and insights.`,
});

const identifyDataAnomaliesFlow = ai.defineFlow(
  {
    name: 'identifyDataAnomaliesFlow',
    inputSchema: IdentifyDataAnomaliesInputSchema,
    outputSchema: IdentifyDataAnomaliesOutputSchema,
  },
  async input => {
    const {output} = await prompt(input);
    return output!;
  }
);
