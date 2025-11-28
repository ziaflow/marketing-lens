import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const data = [
  { date: 'Mon', spend: 1200, conversions: 45 },
  { date: 'Tue', spend: 1500, conversions: 52 },
  { date: 'Wed', spend: 1100, conversions: 38 },
  { date: 'Thu', spend: 1700, conversions: 65 },
  { date: 'Fri', spend: 2100, conversions: 89 },
  { date: 'Sat', spend: 2400, conversions: 110 },
  { date: 'Sun', spend: 1900, conversions: 75 },
];

export default function PerformanceChart() {
  return (
    <div className="h-96 w-full bg-white p-4 rounded-lg shadow">
      <h3 className="text-lg font-medium leading-6 text-gray-900 mb-4">Weekly Performance</h3>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart
          data={data}
          margin={{
            top: 10,
            right: 30,
            left: 0,
            bottom: 0,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
          <XAxis dataKey="date" axisLine={false} tickLine={false} tick={{fill: '#6B7280', fontSize: 12}} dy={10} />
          <YAxis yAxisId="left" axisLine={false} tickLine={false} tick={{fill: '#6B7280', fontSize: 12}} />
          <YAxis yAxisId="right" orientation="right" axisLine={false} tickLine={false} tick={{fill: '#6B7280', fontSize: 12}} />
          <Tooltip
            contentStyle={{ backgroundColor: '#fff', borderRadius: '8px', border: '1px solid #e5e7eb', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}
            itemStyle={{ color: '#374151', fontSize: '14px' }}
          />
          <Legend wrapperStyle={{ paddingTop: '20px' }} />
          <Area yAxisId="left" type="monotone" dataKey="spend" name="Spend ($)" stroke="#4285F4" fill="url(#colorSpend)" strokeWidth={2} />
          <Area yAxisId="right" type="monotone" dataKey="conversions" name="Conversions" stroke="#10B981" fill="url(#colorConv)" strokeWidth={2} />

          <defs>
            <linearGradient id="colorSpend" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#4285F4" stopOpacity={0.1}/>
              <stop offset="95%" stopColor="#4285F4" stopOpacity={0}/>
            </linearGradient>
            <linearGradient id="colorConv" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#10B981" stopOpacity={0.1}/>
              <stop offset="95%" stopColor="#10B981" stopOpacity={0}/>
            </linearGradient>
          </defs>
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
