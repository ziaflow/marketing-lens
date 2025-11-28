import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Search } from 'lucide-react';

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
      <Card className="flex items-center justify-center min-h-[400px]">
        <CardHeader className="text-center">
          <CardTitle>SEO Data Coming Soon</CardTitle>
          <CardContent className="text-muted-foreground">
            This section will contain detailed analytics for SEO performance.
          </CardContent>
        </CardHeader>
      </Card>
    </div>
  );
}
