# Aurora Financial — Integrations

Aurora is built API-first so it plugs into a bank's existing landscape.

## Integration methods
- **REST APIs** for synchronous request/response operations.
- **Webhooks** for push notifications on events (payment settled, account opened).
- **Kafka event streams** for high-throughput, real-time event consumption.

## Pre-built connectors
Aurora ships connectors for common systems:
- Core banking: Temenos, Finacle
- CRM: Salesforce Financial Services Cloud
- Data warehouse: Snowflake, BigQuery
- Identity: Okta, Azure AD (SSO via SAML and OIDC)

## Sandbox
Every customer gets a free sandbox environment with synthetic data for building and
testing integrations before going live. Sandbox API keys are separate from production
and rate-limited to 100 requests per second.

## Rate limits
Production APIs are rate-limited per customer tier: Standard 200 rps, Priority 500 rps,
Enterprise negotiable.
