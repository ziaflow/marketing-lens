import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { DollarSign } from 'lucide-react';

export default function PaidMediaPage() {
  return (
    <div className="p-4 md:p-8 space-y-8">
      <div className="flex items-center gap-4">
        <DollarSign className="size-8 text-primary" />
        <div>
          <h1 className="text-3xl md:text-4xl font-headline font-bold">
            Paid Media Performance
          </h1>
          <p className="text-muted-foreground">
            Analyze the performance of your paid advertising campaigns.
          </p>
        </div>
      </div>
      <Card className="flex items-center justify-center min-h-[400px]">
        <CardHeader className="text-center">
          <CardTitle>Paid Media Data Coming Soon</CardTitle>
          <CardContent className="text-muted-foreground">
            This section will contain detailed analytics for your ad spend and ROI.
          </CardContent>
        </CardHeader>
      </Card>
    </div>
  );
}
