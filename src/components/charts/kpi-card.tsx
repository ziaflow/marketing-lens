import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { ArrowUp, ArrowDown } from 'lucide-react';

type KpiCardProps = {
  label: string;
  value: string;
  change: string;
  isPositive: boolean;
};

export function KpiCard({ label, value, change, isPositive }: KpiCardProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{label}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        <p className="text-xs text-muted-foreground flex items-center gap-1">
          <span
            className={cn(
              'flex items-center gap-1',
              isPositive ? 'text-green-600' : 'text-destructive'
            )}
          >
            {isPositive ? (
              <ArrowUp className="h-4 w-4" />
            ) : (
              <ArrowDown className="h-4 w-4" />
            )}
            {change}
          </span>
          vs. last month
        </p>
      </CardContent>
    </Card>
  );
}
