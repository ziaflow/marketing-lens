import type { ImagePlaceholder } from './placeholder-images';
import { PlaceHolderImages } from './placeholder-images';

type Client = {
  id: string;
  name: string;
  logo: ImagePlaceholder;
};

export const clients: Client[] = [
  {
    id: 'acme-inc',
    name: 'Acme Inc.',
    logo: PlaceHolderImages.find((img) => img.id === 'client-logo-1')!,
  },
  {
    id: 'summit-co',
    name: 'Summit Co.',
    logo: PlaceHolderImages.find((img) => img.id === 'client-logo-2')!,
  },
  {
    id: 'quantum-solutions',
    name: 'Quantum Solutions',
    logo: PlaceHolderImages.find((img) => img.id === 'client-logo-3')!,
  },
  {
    id: 'stellar-corp',
    name: 'Stellar Corp',
    logo: PlaceHolderImages.find((img) => img.id === 'client-logo-4')!,
  },
];

const generatePerformanceData = (seed: number) => {
  const data = [];
  for (let i = 29; i >= 0; i--) {
    const date = new Date();
    date.setDate(date.getDate() - i);
    const dateString = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    data.push({
      date: dateString,
      sessions: Math.floor(Math.random() * (seed * 100) + 500),
      conversions: Math.floor(Math.random() * (seed * 5) + 20),
    });
  }
  return data;
};

const generateKpi = (label: string, value: number, change: number, unit: '' | '%' | '$' = '') => ({
  label,
  value: `${unit === '$' ? '$' : ''}${value.toLocaleString()}${unit !== '$' ? unit : ''}`,
  change: `${change >= 0 ? '+' : ''}${change.toFixed(1)}%`,
  isPositive: change >= 0,
});

export const clientData = {
  'acme-inc': {
    kpis: [
      generateKpi('Total Revenue', 45231, 12.2, '$'),
      generateKpi('Sessions', 87320, 8.1),
      generateKpi('Conversion Rate', 2.1, -0.5, '%'),
      generateKpi('Avg. CPC', 1.85, 5.3, '$'),
    ],
    performance: generatePerformanceData(1.2),
  },
  'summit-co': {
    kpis: [
      generateKpi('Total Revenue', 89542, 15.8, '$'),
      generateKpi('Sessions', 120430, 11.2),
      generateKpi('Conversion Rate', 3.5, 2.1, '%'),
      generateKpi('Avg. CPC', 0.95, -2.1, '$'),
    ],
    performance: generatePerformanceData(1.8),
  },
  'quantum-solutions': {
    kpis: [
      generateKpi('Total Revenue', 12083, -5.1, '$'),
      generateKpi('Sessions', 45010, -10.4),
      generateKpi('Conversion Rate', 1.5, -3.2, '%'),
      generateKpi('Avg. CPC', 2.50, 1.5, '$'),
    ],
    performance: generatePerformanceData(0.8),
  },
  'stellar-corp': {
    kpis: [
      generateKpi('Total Revenue', 150299, 22.5, '$'),
      generateKpi('Sessions', 250900, 18.9),
      generateKpi('Conversion Rate', 4.2, 5.6, '%'),
      generateKpi('Avg. CPC', 1.20, 0.5, '$'),
    ],
    performance: generatePerformanceData(2.5),
  },
};

export const getClients = () => clients;
export const getClientById = (id: string) => clients.find((c) => c.id === id);
export const getClientData = (id: string) => clientData[id as keyof typeof clientData];
