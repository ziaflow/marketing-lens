import React from 'react';

const campaigns = [
  { id: 1, name: 'Summer Sale 2024', platform: 'Meta', status: 'Active', spend: 4500.00, conversions: 120, roas: 3.2 },
  { id: 2, name: 'Brand Awareness', platform: 'TikTok', status: 'Active', spend: 2100.50, conversions: 45, roas: 1.8 },
  { id: 3, name: 'Retargeting - Cart', platform: 'Google', status: 'Paused', spend: 890.00, conversions: 32, roas: 4.1 },
  { id: 4, name: 'Influencer Collab', platform: 'TikTok', status: 'Active', spend: 1200.00, conversions: 88, roas: 2.9 },
  { id: 5, name: 'Winter Prep', platform: 'Meta', status: 'Draft', spend: 0.00, conversions: 0, roas: 0.0 },
];

export default function CampaignTable() {
  return (
    <div className="flex flex-col mt-8">
      <div className="-my-2 -mx-4 overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div className="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
          <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
            <table className="min-w-full divide-y divide-gray-300">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">Campaign Name</th>
                  <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Platform</th>
                  <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Status</th>
                  <th scope="col" className="px-3 py-3.5 text-right text-sm font-semibold text-gray-900">Spend</th>
                  <th scope="col" className="px-3 py-3.5 text-right text-sm font-semibold text-gray-900">Conversions</th>
                  <th scope="col" className="px-3 py-3.5 text-right text-sm font-semibold text-gray-900">ROAS</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 bg-white">
                {campaigns.map((campaign) => (
                  <tr key={campaign.id}>
                    <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6">{campaign.name}</td>
                    <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                        <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                            campaign.platform === 'Meta' ? 'bg-blue-100 text-blue-800' :
                            campaign.platform === 'TikTok' ? 'bg-pink-100 text-pink-800' : 'bg-green-100 text-green-800'
                        }`}>
                            {campaign.platform}
                        </span>
                    </td>
                    <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                        <span className={`inline-flex rounded-full h-2 w-2 mr-2 ${
                            campaign.status === 'Active' ? 'bg-green-400' :
                            campaign.status === 'Paused' ? 'bg-yellow-400' : 'bg-gray-400'
                        }`}></span>
                        {campaign.status}
                    </td>
                    <td className="whitespace-nowrap px-3 py-4 text-sm text-right text-gray-500">${campaign.spend.toFixed(2)}</td>
                    <td className="whitespace-nowrap px-3 py-4 text-sm text-right text-gray-500">{campaign.conversions}</td>
                    <td className="whitespace-nowrap px-3 py-4 text-sm text-right text-gray-900 font-medium">{campaign.roas.toFixed(2)}x</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
