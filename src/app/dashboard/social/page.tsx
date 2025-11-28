import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Share2 } from 'lucide-react';

export default function SocialPage() {
  return (
    <div className="p-4 md:p-8 space-y-8">
      <div className="flex items-center gap-4">
        <Share2 className="size-8 text-primary" />
        <div>
          <h1 className="text-3xl md:text-4xl font-headline font-bold">
            Social Media Analytics
          </h1>
          <p className="text-muted-foreground">
            Monitor engagement and growth across your social channels.
          </p>
        </div>
      </div>
      <Card className="flex items-center justify-center min-h-[400px]">
        <CardHeader className="text-center">
          <CardTitle>Social Media Data Coming Soon</CardTitle>
          <CardContent className="text-muted-foreground">
            This section will contain detailed analytics for social media performance.
          </CardContent>
        </CardHeader>
      </Card>
    </div>
  );
}
