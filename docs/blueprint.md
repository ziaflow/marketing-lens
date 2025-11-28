# **App Name**: Marketing Lens

## Core Features:

- Data Ingestion Pipeline: Automated data ingestion from Google Analytics (GA4), Search Console, Ads; Bing Webmaster Tools, LinkedIn Insight Tag, LinkedIn Page; Facebook Pixel, Instagram Page, TikTok Pixel, and Reddit Profile via APIs and file uploads (CSV/Excel) to Azure Blob Storage.
- Data Transformation & Normalization: Azure Data Factory (ADF) transforms raw data from Azure Blob Storage, mapping platform-specific metrics to a unified schema in PostgreSQL.
- Multi-Tenant Dashboard: AstroJS/React-based dashboard with Agency (Super Admin) and Client views, displaying aggregate performance across all clients or a single client, respectively.
- Hierarchical UI Navigation: Drill-down UI organized into General Overview (KPIs), Social Media, SEO, and Paid Media sections.
- Secure API Authentication: Use Azure Key Vault for securely storing and managing OAuth tokens for multiple platforms (20+).
- Ad-hoc Analysis Integration: Enable integration with Microsoft Copilot Notebooks, Excel, and Power BI by connecting them directly to the PostgreSQL database.
- Intelligent Insights: Use generative AI to create an AI 'tool' that identifies anomalies, insights, and suggests actions based on marketing data, configurable per client. The tool uses client data and insights.

## Style Guidelines:

- Primary color: 3f9b93, echoing the brand and reflecting data depth.
- Background color: ffffff, providing a clean, analytical backdrop.
- Accent color: a22a36, drawing the user's eye to key performance metrics and calls to action.
- Text color: 313131.
- Body font: 'Inter', sans-serif, chosen for a machined, neutral, readable look in reports.
- Headline font: 'Space Grotesk', sans-serif, chosen for a techy feel.
- Use clean, minimalist icons to represent data sources (Google, Facebook, etc.) and metrics (impressions, clicks).
- Dashboard layout is structured, with clear sections for each data category (Social, SEO, Paid Media) and key metrics highlighted.
- Subtle transitions and animations to enhance user engagement, such as data loading and metric updates.