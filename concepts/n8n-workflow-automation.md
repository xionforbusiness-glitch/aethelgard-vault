---
title: n8n Workflow Automation Platform
created: 2026-09-20
updated: 2026-09-20
type: concept
tags: [automation, workflow, ai-integration, low-code, n8n, self-hosted]
sources: [raw/articles/n8n-workflow-automation.md]
confidence: high
contested: false
contradictions: []
---

# n8n Workflow Automation Platform

**n8n** (pronounced "n-eight-n") is a fair-code workflow automation platform with native AI capabilities. It combines visual node-based building with custom JavaScript/Python code, supporting both self-hosted and cloud deployments with 400+ integrations.

## Overview

| Attribute | Value |
|-----------|-------|
| GitHub Stars | 205.4K |
| Forks | 60.8K |
| Community | 200k+ members |
| G2 Rating | 4.7/5 |
| Language | TypeScript/Node.js |

## Core Philosophy

**"Code when you need it, UI when you don't"** — Unlike tools limited to either visual building OR code, n8n provides both:
- Drag-and-drop node-based visual workflow builder
- Write JavaScript or Python anywhere in workflows
- See inputs/outputs next to every step settings

## Key Features

### AI-Native Platform
- **Agent Builder** — Build AI agents with natural language
- **Native LLM integrations** — OpenAI, Anthropic, Mistral, and more
- **Human-in-the-loop** — AI governance with guardrails and evaluations
- **RAG pipelines** — Retrieval-augmented generation workflows

### 400+ Integrations
- **Cloud:** Google, Microsoft, Salesforce, Slack, Discord
- **Databases:** PostgreSQL, MySQL, MongoDB, Redis
- **Communication:** Email, SMS, WhatsApp, Telegram
- **DevOps:** GitHub, GitLab, AWS, Docker, Kubernetes

### Enterprise Ready
- **Self-hosted:** Docker, Kubernetes, any cloud
- **Security:** SSO SAML, LDAP, encrypted secrets, RBAC
- **Observability:** Audit logs, SIEM integration, workflow history

## Use Cases

### IT Operations
- Employee on-boarding automation
- Account provisioning workflows
- Ticket management

### Security (SecOps)
- Security incident enrichment
- **Vodafone Case Study:** Saved £2.2M with SOAR workflows

### DevOps
- Natural language to API calls
- Deployment automation
- Monitoring & alerting pipelines

### AI Workflows
- Document processing & summarization
- Multi-agent orchestration
- RAG-based Q&A systems

## Notable Deployments

- Microsoft, Meta, NVIDIA, Dell
- Deutsche Telekom, Mercedes-Benz
- Vodafone, Mistral AI

## vs. Alternatives

| Tool | Type | Self-Hosted | Code Support |
|------|------|-------------|--------------|
| **n8n** | Fair-code | ✅ | JS/Python |
| Zapier | SaaS | ❌ | Limited |
| Make (Integromat) | SaaS | ❌ | Limited |
| Apache Airflow | Open-source | ✅ | Python only |

## Cross-References

- [[01 Technical Skills]] — Python, JavaScript, Node.js
- [[technical_skills_knowledge_base]] — Web stack and automation
- [[02 Projects]] — Can be used for project automation
- [[ai_evaluation_annotation_handbook]] — AI integration patterns
- [[openvpn_network_tunneling_architecture]] — Self-hosted infrastructure

## Getting Started

### Docker (Self-Hosted)
```bash
docker run -d --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n n8nio/n8n
```

### Key Links
- Website: https://n8n.io/
- GitHub: https://github.com/n8n-io/n8n
- Community: https://community.n8n.io/
- Docs: https://docs.n8n.io/