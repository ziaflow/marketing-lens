/// <reference path="../.astro/types.d.ts" />

type Runtime = import("@astrojs/node").Runtime;

declare namespace App {
  interface Locals extends Runtime {
    tenantId: string;
    platformConfig: {
        enableGSC: boolean;
        enableGA4: boolean;
        enableLinkedIn: boolean;
    }
  }
}
