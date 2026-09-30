---
source_url: https://n8n.io/
ingested: 2026-09-20
sha256: a3b7c9d1e5f8a2b4c6d9e7f3a1b5c8d2e6f4a9b7c1d3e5f8a2b4c6d9e7f3a1b5
---

# n8n — AI Workflow Automation Platform

**Website:** https://n8n.io/
**GitHub:** https://github.com/n8n-io/n8n
**Stars:** 205.4K | **Forks:** 60.8K

## What is n8n?

n8n (pronounced "n-eight-n") is a **fair-code workflow automation platform** with native AI capabilities. It combines visual building with custom code, allowing users to self-host or use cloud, with 400+ integrations.

The name "n8n" comes from "nodemation" — combining "node" (Node.js, node-based view) and "automation."

## Key Statistics

- **GitHub Stars:** 205.4K (Top 50 repos)
- **G2 Rating:** 4.7/5 stars
- **Community:** 200k+ members
- **Commits:** 24,543+
- **Releases:** 2,166 tags

## Core Features

### 1. Visual + Code Workflow Building
- **No-code visual builder** — Drag-and-drop node-based interface
- **Custom code** — Write JavaScript or Python anywhere in workflows
- **Best of both worlds** — Visual building when you want it, code when you need it

### 2. AI-Native Platform
- **Agent Builder** — Build AI agents with natural language
- **LLM integrations** — Native support for major language models
- **Human-in-the-loop** — AI governance with guardrails and evaluations
- **AI workflow testing** — Test with real data to improve accuracy

### 3. 400+ Integrations
- Cloud services: Google, Microsoft, Salesforce, Slack, Discord
- Databases: PostgreSQL, MySQL, MongoDB, Redis
- Communication: Email, SMS, WhatsApp, Telegram
- DevOps: GitHub, GitLab, AWS, Docker, Kubernetes
- AI/ML: OpenAI, Anthropic, Hugging Face, custom APIs

### 4. Enterprise Features
- **Security:** Fully on-prem option, SSO SAML, LDAP, encrypted secret stores
- **Access Control:** RBAC permissions, version control
- **Observability:** Audit logs, log streaming to SIEM, workflow history
- **Developer Experience:** Git-based control, isolated environments, multi-user workflows

### 5. Deployment Options
- **Self-hosted:** Docker, Kubernetes, any cloud provider
- **Cloud:** Managed n8n.io service
- **Hybrid:** Mix of both

## Use Cases

### IT Operations
- On-board new employees (provision accounts, setup access)
- Automated ticket workflows

### Security Operations
- Enrich security incident tickets
- Threat intelligence automation
- **Case Study:** Vodafone saved £2.2 Million with n8n SOAR capabilities

### DevOps
- Convert natural language into API calls
- Automated deployment pipelines
- Monitoring and alerting workflows

### Sales & Marketing
- Generate customer insights from reviews
- CRM automation (Salesforce, HubSpot)
- Lead scoring and nurturing

### AI Workflows
- RAG (Retrieval-Augmented Generation) pipelines
- Document processing and summarization
- Multi-agent orchestration

## Code Example (JavaScript in Workflow)

```javascript
// Get data from previous node
const items = $input.all();

// Process each item
const results = items.map(item => {
  return {
    json: {
      original: item.json,
      processed: item.json.data.toUpperCase(),
      timestamp: new Date().toISOString()
    }
  };
});

return results;
```

## Enterprise Customers

- Microsoft
- Fender
- Amadeus
- Meta
- Deutsche Telekom
- Novo Nordisk
- NVIDIA
- Dell
- Cummins
- Vodafone
- Mercedes-Benz
- Mistral AI

## Case Studies

### Huel — AI First Company Culture
- Saved 1,000 hours of manual work
- "n8n was the big unlock. It allows you to integrate AI into your work in a safe and controlled way"
- Ollie Scheers, CTO

### Vodafone — Threat Intelligence
- Saved £2.2 Million
- "n8n provides SOAR capability and workflows in a low-code model, as well as the ability to code for more complex workflows and integrations"
- Claire Van Hinsbergh, Cyber Operations Engineering Manager

## Technical Stack

- **Language:** TypeScript (primary)
- **Runtime:** Node.js
- **Database:** PostgreSQL
- **License:** Sustainable Use License (fair-code)
- **Container:** Docker, Kubernetes

## Related Tools

- **Zapier** — Cloud-only alternative
- **Make (Integromat)** — Visual automation
- **Apache Airflow** — Data pipeline automation
- **Temporal** — Microservice orchestration
- **AutoGPT / LangChain** — AI agent frameworks

## Getting Started

### Docker (Self-Hosted)
```bash
docker run -d --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n n8nio/n8n
```

### Cloud
Sign up at https://n8n.io/

### Development
```bash
git clone https://github.com/n8n-io/n8n.git
cd n8n
npm install
npm run start
```

## Topics

ai, apis, automation, cli, data-flow, development, integration-framework, integrations, ipaas, low-code, low-code-platform, mcp, mcp-client, mcp-server, n8n, no-code, self-hosted, typescript, workflow, workflow-automation

---

*Ingested: 2026-09-20*
*Related: [[technical_skills_knowledge_base]], [[01 Technical Skills]]*