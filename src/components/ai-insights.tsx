'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
  SheetDescription,
  SheetFooter,
} from '@/components/ui/sheet';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion';
import { Skeleton } from '@/components/ui/skeleton';
import { AlertCircle, Lightbulb, CheckCircle } from 'lucide-react';

import { identifyDataAnomalies } from '@/ai/flows/identify-data-anomalies';
import { generateInsights } from '@/ai/flows/generate-insights-from-data';
import { suggestActionableRecommendations } from '@/ai/flows/suggest-actionable-recommendations';

type AIResults = {
  anomalies: string[];
  insights: { summary: string; keyTrends: string };
  recommendations: string;
};

export function AiInsights({ clientDataString, clientName }: { clientDataString: string, clientName: string }) {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<AIResults | null>(null);
  const [isOpen, setIsOpen] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    setResults(null);
    try {
      const [anomaliesResult, insightsResult, recommendationsResult] = await Promise.all([
        identifyDataAnomalies({
          clientName: clientName,
          dataDescription: 'Monthly marketing performance data.',
          data: clientDataString,
        }),
        generateInsights({
          clientData: clientDataString,
        }),
        suggestActionableRecommendations({
          clientData: clientDataString,
          insights: `Generated from data for ${clientName}`,
        }),
      ]);

      setResults({
        anomalies: anomaliesResult.anomalies,
        insights: { summary: insightsResult.summary, keyTrends: insightsResult.keyTrends },
        recommendations: recommendationsResult.recommendations,
      });
    } catch (error) {
      console.error('Error generating AI insights:', error);
      // Here you could use the toast to show an error
    } finally {
      setLoading(false);
    }
  };

  return (
    <Sheet open={isOpen} onOpenChange={setIsOpen}>
      <SheetTrigger asChild>
        <Button className="font-bold bg-gradient-to-r from-primary to-teal-500 text-white hover:opacity-90 transition-opacity">
          ✨ Generate Insights
        </Button>
      </SheetTrigger>
      <SheetContent className="w-[400px] sm:w-[540px] sm:max-w-xl">
        <SheetHeader>
          <SheetTitle className="font-headline text-2xl">Intelligent Insights</SheetTitle>
          <SheetDescription>
            AI-powered analysis of your marketing data.
          </SheetDescription>
        </SheetHeader>
        <div className="py-4">
          {loading && (
            <div className="space-y-4">
              <Skeleton className="h-12 w-full" />
              <Skeleton className="h-20 w-full" />
              <Skeleton className="h-12 w-full" />
              <Skeleton className="h-20 w-full" />
              <Skeleton className="h-12 w-full" />
              <Skeleton className="h-20 w-full" />
            </div>
          )}
          {results && !loading && (
            <Accordion type="single" collapsible defaultValue="item-1" className="w-full">
              <AccordionItem value="item-1">
                <AccordionTrigger>
                  <div className="flex items-center gap-2">
                    <AlertCircle className="size-5 text-destructive" />
                    Anomalies Detected
                  </div>
                </AccordionTrigger>
                <AccordionContent>
                  <ul className="list-disc space-y-2 pl-6 text-sm text-muted-foreground">
                    {results.anomalies.map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                </AccordionContent>
              </AccordionItem>
              <AccordionItem value="item-2">
                <AccordionTrigger>
                  <div className="flex items-center gap-2">
                    <Lightbulb className="size-5 text-yellow-500" />
                    Key Insights
                  </div>
                </AccordionTrigger>
                <AccordionContent className="space-y-4 text-sm">
                  <div>
                    <h4 className="font-semibold">Summary</h4>
                    <p className="text-muted-foreground">{results.insights.summary}</p>
                  </div>
                   <div>
                    <h4 className="font-semibold">Key Trends</h4>
                    <p className="text-muted-foreground">{results.insights.keyTrends}</p>
                  </div>
                </AccordionContent>
              </AccordionItem>
              <AccordionItem value="item-3">
                <AccordionTrigger>
                  <div className="flex items-center gap-2">
                    <CheckCircle className="size-5 text-green-500" />
                    Recommendations
                  </div>
                </AccordionTrigger>
                <AccordionContent>
                   <p className="text-sm text-muted-foreground">{results.recommendations}</p>
                </AccordionContent>
              </AccordionItem>
            </Accordion>
          )}
        </div>
        <SheetFooter>
          <Button onClick={handleGenerate} disabled={loading} className="w-full">
            {loading ? 'Analyzing...' : 'Re-generate Insights'}
          </Button>
        </SheetFooter>
      </SheetContent>
    </Sheet>
  );
}
