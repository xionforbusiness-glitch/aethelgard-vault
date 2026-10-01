---
title: "Wazuh SIEM & XDR Open-Source Security Operations Playbook"
created: 2026-10-01
updated: 2026-10-01
type: concept
tags: [security, cybersecurity, siem, xdr, wazuh, linux, networking, homelab, devops, blue-team]
sources: [raw/articles/2026-10-01-networkchuck-wazuh-siem-xdr-guide.md]
confidence: high
contested: false
contradictions: []
---

# 🛡️ Wazuh SIEM & XDR Security Operations Playbook

**Wazuh** is a free, open-source enterprise-grade **SIEM (Security Information and Event Management)** and **XDR (Extended Detection and Response)** platform. It provides unified endpoint protection, threat intelligence, file integrity monitoring, and automated incident response across Linux, Windows, macOS, and container clusters.

---

## 🏗️ 1. Core Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    WAZUH DASHBOARD                          │
│     (Web UI / OpenSearch Visualizations / Alert Triage)     │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                      WAZUH MANAGER                          │
│  (Analysis Engine / Decoders / Rulesets / Active Response)  │
└───────────────▲─────────────────────────────▲───────────────┘
                │                             │
    ┌───────────┴───────────┐     ┌───────────┴───────────┐
    │  WAZUH INDEXER        │     │  WAZUH AGENTS         │
    │  (OpenSearch Engine / │     │  (Windows, Linux,     │
    │   Log Storage & FTS)  │     │   macOS, Containers)  │
    └───────────────────────┘     └───────────────────────┘
```

---

## ⚡ 2. Core Capabilities & Blue Team Superpowers

| Module | Technical Functionality | Practical Security Value |
| :--- | :--- | :--- |
| **FIM (File Integrity Monitoring)** | Real-time monitoring of critical file hashes (SHA256), attributes, permissions, and Windows Registry keys. | Detects ransomware encryption, unauthorized web-shell drops, and privilege escalation configs. |
| **Vulnerability Detection** | Continuously cross-references installed OS packages against NVD/CVE security feeds. | Identifies unpatched software and outdated libraries before exploitation. |
| **SCA (Security Configuration Assessment)** | Evaluates system configuration against CIS (Center for Internet Security) benchmarks. | Highlights weak SSH ciphers, disabled UFW/firewalls, and insecure default permissions. |
| **Active Response** | Executes automated scripts/remediations upon specific rule triggers. | Blocks attacking IPs via `iptables` / `nftables` immediately upon brute-force detection. |
| **Log Analysis & Decoders** | Ingests `syslog`, auth logs, Apache/Nginx access logs, and Windows Event logs (Sysmon). | Correlates multi-stage attack vectors into single actionable incident alerts. |

---

## 🚀 3. Quick-Start Deployment (Docker Single-Node)

### Step 1: Clone the Official Docker Deployment
```bash
git clone https://github.com/wazuh/wazuh-docker.git -b v4.9.0 --depth=1
cd wazuh-docker/single-node
```

### Step 2: Generate TLS Certificates & Start Cluster
```bash
# Generate self-signed TLS certificates for internal manager/indexer communication
docker compose -f generate-indexing-certs.yml run --rm generator

# Launch Wazuh Manager, Indexer, and Dashboard in the background
docker compose up -d
```

### Step 3: Access Web UI
- **Dashboard URL:** `https://<SERVER_IP>`
- **Default Credentials:**
  - **Username:** `admin`
  - **Password:** `SecretPassword` *(generated during cert init)*

---

## 💻 4. Endpoint Agent Enrollment

### Linux (Ubuntu / Debian)
```bash
wget https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.9.0-1_amd64.deb
sudo WAZUH_MANAGER='<SERVER_IP>' WAZUH_AGENT_GROUP='default' dpkg -i ./wazuh-agent_4.9.0-1_amd64.deb
sudo systemctl daemon-reload
sudo systemctl enable --now wazuh-agent
```

### Windows (PowerShell Run as Administrator)
```powershell
Invoke-WebRequest -Uri https://packages.wazuh.com/4.x/windows/wazuh-agent-4.9.0-1.msi -OutFile ${env:tmp}\wazuh-agent.msi; `
msiexec.exe /i ${env:tmp}\wazuh-agent.msi /q WAZUH_MANAGER='<SERVER_IP>' WAZUH_REGISTRATION_SERVER='<SERVER_IP>'
NET START WazuhSvc
```

---

## ⚔️ 5. Setting Up Active Response (Automated IP Blocking)

Edit `/var/ossec/etc/ossec.conf` on the Wazuh Manager:

```xml
<!-- Active response: Block SSH brute-force attackers for 10 minutes -->
<active-response>
  <command>firewall-drop</command>
  <location>local</location>
  <rules_id>5712, 5710, 5716</rules_id>
  <timeout>600</timeout>
</active-response>
```

---

## 🔗 Related Notes & Skills
- [[01 Technical Skills]] — Systems, security, and networking competencies.
- [[networking_wireshark_playbook]] — Deep packet inspection and traffic diagnostics.
- [[linux_cli_bash_automation_reference]] — Shell automation, cron, and service management.
- `raw/articles/2026-10-01-networkchuck-wazuh-siem-xdr-guide.md` — Original video source.
