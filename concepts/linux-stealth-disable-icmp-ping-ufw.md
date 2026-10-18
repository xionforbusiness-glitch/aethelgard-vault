---
title: "Linux Stealth Hardening: Disabling ICMP Ping Discovery in UFW"
created: 2026-10-18
updated: 2026-10-18
type: concept
tags: [security, linux, networking, ufw, iptables, firewall, hardening, networkchuck, sysadmin]
sources: [NetworkChuck (Facebook Reel 1275181257662822)]
confidence: high
contested: false
contradictions: []
---

# 🥷 Linux Server Stealth Hardening: Disabling ICMP Ping Discovery (NetworkChuck Guide)

> **"No replies, no discovery. Make your server completely invisible to automated internet-wide port sweeps and ping scans."**  
> Operational security guide based on **NetworkChuck's UFW ICMP stealth hardening tutorial**, explaining how automated scanning bots discover cloud servers and how to configure UFW to drop `echo-request` packets silently.

---

## 🔍 How Automated Scanners Find Your Server

When internet scanning engines (Shodan, Censys, masscan, zmap, or script-kiddie botnets) hunt for vulnerable cloud instances, their first step is usually an **ICMP Echo Sweep** (`ping` sweep across entire IP subnets):

```
Scanner (Attacker)                 Your Cloud Server
       │                                  │
       │ ─── ICMP Echo Request (Ping) ──> │
       │                                  │
       │ <── ICMP Echo Reply (Default) ── │  🚨 "Server is ALIVE! Proceed to port scan."
```

If your server replies, the attacker confirms an active host and immediately proceeds to aggressive TCP/UDP port scanning (SSH brute-force, web vulnerability fuzzing).

By configuring your firewall to **DROP** ICMP echo requests silently without sending an ICMP unreachable error:
```
Scanner (Attacker)                 Your Cloud Server
       │                                  │
       │ ─── ICMP Echo Request (Ping) ──> │  [DROP silently]
       │                                  │
       │ ─── (Timeout... No reply) ─────> │  🥷 "Host appears down or dead IP. Moving on."
```

---

## 🛠️ Step-by-Step Implementation with UFW

By default on Ubuntu/Debian, `ufw` permits ICMP traffic via rules inside `/etc/ufw/before.rules`. Standard `ufw deny` commands do not block ICMP because `before.rules` executes first.

### Step 1: Open UFW Before Rules
```bash
sudo nano /etc/ufw/before.rules
```

### Step 2: Locate the ICMP Section
Find the block labeled `-A ufw-before-input -p icmp ...`:
```text
# ok icmp codes for INPUT
-A ufw-before-input -p icmp --icmp-type destination-unreachable -j ACCEPT
-A ufw-before-input -p icmp --icmp-type time-exceeded -j ACCEPT
-A ufw-before-input -p icmp --icmp-type parameter-problem -j ACCEPT
-A ufw-before-input -p icmp --icmp-type echo-request -j ACCEPT
```

### Step 3: Change `echo-request` to `DROP`
Modify the `echo-request` rule from `ACCEPT` to `DROP`:
```text
-A ufw-before-input -p icmp --icmp-type echo-request -j DROP
```
*(Or in IPv6 `/etc/ufw/before6.rules`, change `--icmpv6-type echo-request` to `DROP`)*.

### Step 4: Reload UFW
```bash
sudo ufw reload
```

---

## ⚖️ Trade-offs & Operational Considerations

| Dimension | Default (Ping Enabled) | Stealth Mode (`DROP` Echo Request) |
| :--- | :--- | :--- |
| **Security Posture** | Exposed to automated sweeps | Invisible to casual subnet ping sweeps |
| **Network Troubleshooting** | Easy (`ping your-server.ip`) | Requires TCP/port checking (`nc`, `curl`, `hping3`) |
| **Path MTU Discovery** | Handled by ICMP type 3 | Unaffected (we only drop type 8 `echo-request`, keeping `destination-unreachable` open!) |

> 💡 **Key Invariant:** Never drop ALL ICMP types blindly. Dropping `destination-unreachable` breaks Path MTU Discovery (PMTUD), causing packet fragmentation issues and stalling TCP handshakes. Drop **only** `echo-request`.

---

## 🔗 Related Notes & Vault Assets

* [[concepts/ai-red-teaming-and-llm-hacking-playbook|AI Red Teaming Playbook]]
* [[concepts/vibe-coder-security-fix-kit|Vibe Coder Security Fix Kit]]
* [[01 Technical Skills|Technical Skills Knowledge Base]]
* [[log|Operational Log]]
