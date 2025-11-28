import { notFound } from 'next/navigation';
import { getClientById, getClientData } from '@/lib/data';
import Image from 'next/image';
import { KpiCard } from '@/components/charts/kpi-card';
import { PerformanceChart } from '@/components/charts/performance-chart';
import { AiInsights } from '@/components/ai-insights';

export default function ClientPage({ params }: { params: { clientId: string } }) {
  const client = getClientById(params.clientId);
  if (!client) {
    notFound();
  }
  const data = getClientData(params.clientId);

  return (
    <div className="p-4 md:p-8 space-y-8">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div className="flex items-center gap-4">
          <Image
            src={client.logo.imageUrl}
            alt={`${client.name} logo`}
            width={64}
            height={64}
            className="rounded-full border-2"
            data-ai-hint={client.logo.imageHint}
          />
          <div>
            <h1 className="text-3xl md:text-4xl font-headline font-bold">
              {client.name}
            </h1>
            <p className="text-muted-foreground">
              Detailed performance dashboard.
            </p>
          </div>
        </div>
        <AiInsights clientDataString={JSON.stringify(data)} clientName={client.name} />
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {data.kpis.map((kpi) => (
          <KpiCard key={kpi.label} {...kpi} />
        ))}
      </div>
      
      <div>
        <PerformanceChart data={data.performance} />
      </div>

    </div>
  );
}

export function generateStaticParams() {
  const { getClients } = require('@/lib/data');
  const clients = getClients();
  return clients.map((client: { id: string }) => ({
    clientId: client.id,
  }));
}
