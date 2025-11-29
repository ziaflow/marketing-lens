import { defineMiddleware } from "astro:middleware";

export const onRequest = defineMiddleware((context, next) => {
  const hostname = context.url.host;
  // Simple mock tenant resolution
  // In prod this would lookup tenant from DB based on subdomain
  const subdomain = hostname.split('.')[0];

  // Mock Tenant ID
  context.locals.tenantId = subdomain === 'localhost:3000' ? 'default-tenant-id' : `tenant-${subdomain}`;
  context.locals.platformConfig = {
      // Mock feature flags
      enableGSC: true,
      enableGA4: true,
      enableLinkedIn: true
  };

  return next();
});
