import { defineMiddleware } from "astro:middleware";

export const onRequest = defineMiddleware((context, next) => {
  // Mock Tenant Resolution Logic
  // In production, this would parse context.url.host
  const subdomain = context.url.host.split('.')[0];
  context.locals.tenantId = subdomain === 'localhost' ? 'demo-tenant' : subdomain;

  return next();
});
