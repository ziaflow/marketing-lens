import { Card, CardHeader, CardTitle, CardContent, CardDescription, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Settings } from 'lucide-react';
import { PlatformIcon } from '@/components/platform-icon';
import type { Platform } from '@/components/platform-icon';

const dataSources: { name: string; platform: Platform, connected?: boolean, projectId?: string }[] = [
    { name: 'Microsoft Clarity', platform: 'bing', connected: true, projectId: process.env.CLARITY_PROJECT_ID },
    { name: 'Google Analytics', platform: 'google' },
    { name: 'Facebook Ads', platform: 'facebook' },
    { name: 'LinkedIn Campaign Manager', platform: 'linkedin' },
    { name: 'TikTok for Business', platform: 'tiktok' },
    { name: 'Reddit Ads', platform: 'reddit' },
];

export default function SettingsPage() {
  return (
    <div className="p-4 md:p-8 space-y-8">
      <div className="flex items-center gap-4">
        <Settings className="size-8 text-primary" />
        <div>
          <h1 className="text-3xl md:text-4xl font-headline font-bold">
            Settings
          </h1>
          <p className="text-muted-foreground">
            Manage your account and data source connections.
          </p>
        </div>
      </div>
      
      <Card>
        <CardHeader>
          <CardTitle>Data Sources</CardTitle>
          <CardDescription>Connect and manage your marketing data platforms. Represents API authentication.</CardDescription>
        </CardHeader>
        <CardContent className="grid gap-6">
          {dataSources.map(source => (
            <div key={source.name} className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <PlatformIcon platform={source.platform} className="size-6" />
                <div>
                  <span className="font-medium">{source.name}</span>
                  {source.projectId && (
                    <p className="text-xs text-muted-foreground">Project ID: {source.projectId}</p>
                  )}
                </div>
              </div>
              {source.connected ? (
                <Button variant="outline" disabled>Connected</Button>
              ) : (
                <Button variant="outline">Connect</Button>
              )}
            </div>
          ))}
        </CardContent>
        <CardFooter className="border-t pt-6">
          <Button>Add Custom Source</Button>
        </CardFooter>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Ad-hoc Analysis</CardTitle>
          <CardDescription>Connect to external tools for deeper analysis.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
            <p>Your PostgreSQL database connection string is available here for integration with tools like Power BI, Excel, and Microsoft Copilot Notebooks.</p>
            <div className="space-y-2">
                <Label htmlFor="db-string">Connection String</Label>
                <Input id="db-string" readOnly defaultValue="postgresql://user:password@host:port/database" />
            </div>
        </CardContent>
        <CardFooter>
            <Button variant="secondary">Copy Connection String</Button>
        </CardFooter>
      </Card>
    </div>
  );
}
