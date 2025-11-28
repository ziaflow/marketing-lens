import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Search, Gauge } from 'lucide-react';

export default function SeoPage() {
  return (
    <div className="p-4 md:p-8 space-y-8">
      <div className="flex items-center gap-4">
        <Search className="size-8 text-primary" />
        <div>
          <h1 className="text-3xl md:text-4xl font-headline font-bold">
            SEO Analysis
          </h1>
          <p className="text-muted-foreground">
            Track and improve your search engine optimization efforts.
          </p>
        </div>
      </div>
      <div className="grid md:grid-cols-2 gap-8">
        <Card className="flex items-center justify-center min-h-[300px]">
          <CardHeader className="text-center">
            <CardTitle>Search Console Data Coming Soon</CardTitle>
            <CardContent className="text-muted-foreground pt-2">
              This section will show keyword and query performance.
            </CardContent>
          </CardHeader>
        </Card>
        <Card className="flex flex-col justify-center min-h-[300px]">
           <CardHeader>
            <div className="flex items-center gap-2">
                <Gauge className="size-6 text-primary" />
                <CardTitle>PageSpeed Insights</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="text-center text-muted-foreground">
            PageSpeed data will be displayed here soon.
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
