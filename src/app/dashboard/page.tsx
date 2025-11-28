import { getClients, getClientData } from '@/lib/data';
import Link from 'next/link';
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  CardDescription,
} from '@/components/ui/card';
import Image from 'next/image';
import { ArrowUp } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { PlatformIcon } from '@/components/platform-icon';

export default function AgencyDashboardPage() {
  const clients = getClients();

  return (
    <div className="p-4 md:p-8 space-y-8">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-3xl md:text-4xl font-headline font-bold">
            Agency Overview
          </h1>
          <p className="text-muted-foreground">
            A high-level view of all client accounts.
          </p>
        </div>
        <div className="flex items-center gap-2">
            <PlatformIcon platform="google" className="size-6" />
            <PlatformIcon platform="facebook" className="size-6" />
            <PlatformIcon platform="linkedin" className="size-6" />
            <PlatformIcon platform="instagram" className="size-6" />
            <PlatformIcon platform="tiktok" className="size-6" />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {clients.map((client) => {
          const data = getClientData(client.id);
          const revenue = data.kpis.find(k => k.label === 'Total Revenue');
          return (
            <Link href={`/dashboard/clients/${client.id}`} key={client.id}>
              <Card className="h-full hover:shadow-lg transition-shadow duration-300 hover:-translate-y-1">
                <CardHeader className="flex flex-row items-center gap-4 space-y-0">
                  <Image
                    src={client.logo.imageUrl}
                    alt={`${client.name} logo`}
                    width={48}
                    height={48}
                    className="rounded-full border"
                    data-ai-hint={client.logo.imageHint}
                  />
                  <div className="flex-1">
                    <CardTitle className="font-headline text-lg">
                      {client.name}
                    </CardTitle>
                    <CardDescription>View Dashboard</CardDescription>
                  </div>
                </CardHeader>
                <CardContent className="space-y-2">
                  <p className="text-xs text-muted-foreground">Monthly Revenue</p>
                  <div className="text-2xl font-bold">{revenue?.value}</div>
                  <div className="flex items-center gap-1 text-xs text-green-600">
                    <ArrowUp className="size-4" />
                    <span>{revenue?.change}</span>
                  </div>
                </CardContent>
              </Card>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
