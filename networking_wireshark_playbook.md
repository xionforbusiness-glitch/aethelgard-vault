---
aliases: [Wireshark, Networking, Packet Analysis, Troubleshooting]
tags: [networking, sysadmin, security, analysis]
created: 2026-09-19
up: "[[Technical/Skills_and_Stack]]"
related: ["[[Work/Experience_and_Roles]]"]
---

# 🌐 Networking & Wireshark Triage Playbook

A practical handbook for packet analysis, protocol diagnostics, and broadband infrastructure troubleshooting.

---

## 1. High-Efficiency Wireshark Display Filters

### General Troubleshooting Filters
| Objective | Filter Expression |
| :--- | :--- |
| Find all TCP Resets | `tcp.flags.reset == 1 && tcp.seq == 1` |
| Isolate Retransmissions | `tcp.analysis.retransmission || tcp.analysis.fast_retransmission` |
| Check High Latency / RTT | `tcp.analysis.ack_rtt > 0.15` (packets taking $> 150\text{ ms}$) |
| DNS Latency & Errors | `dns.flags.rcode != 0 || dns.time > 0.1` |
| HTTP Server Errors | `http.response.code >= 500` |
| Trace Target Client IP | `ip.addr == 192.168.1.100 && !(ip.addr == 192.168.1.1)` |

### Security & Protocol Hunting
- **Detect Cleartext Auth:** `http.request.method == "POST" && (frame contains "password" || frame contains "pwd")`
- **Detect SYN Scanning Activity:** `tcp.flags.syn == 1 && tcp.flags.ack == 0`
- **Isolate DHCP Handshake:** `bootp || dhcp`

---

## 2. TCP 3-Way Handshake & Teardown Analysis

```
Client                                      Server
  │                                           │
  │─── SYN (Seq=0) ──────────────────────────>│  1. Request Connection
  │<── SYN-ACK (Seq=0, Ack=1) ────────────────│  2. Acknowledge & Request
  │─── ACK (Seq=1, Ack=1) ───────────────────>│  3. Connection Established
  │                                           │
  │              DATA EXCHANGE                │
  │                                           │
  │─── FIN-ACK (Seq=x, Ack=y) ───────────────>│  4. Client Initiates Close
  │<── ACK (Seq=y, Ack=x+1) ──────────────────│  5. Server Acknowledges Close
  │<── FIN-ACK (Seq=y, Ack=x+1) ──────────────│  6. Server Initiates Close
  │─── ACK (Seq=x+1, Ack=y+1) ───────────────>│  7. Connection Terminated
```

---

## 3. ISP & Customer Broadband Triage Framework
*(Synthesized from enterprise ISP tech support operations at [[Work/Experience_and_Roles#3. Customer Service & Technical Support|Concentrix/Optimum]])*

### Physical Layer (L1) & Coaxial/Fiber Diagnostics
- **Downstream Power Levels (DOCSIS):** Optimal range is $-7\text{ dBmV}$ to $+7\text{ dBmV}$. Levels below $-10\text{ dBmV}$ cause packet loss.
- **Downstream SNR (Signal-to-Noise Ratio):** Should consistently measure $> 35\text{ dB}$.
- **Upstream Power Levels:** Ideal range is $38\text{ dBmV} - 48\text{ dBmV}$. If upstream exceeds $52\text{ dBmV}$, the modem is shouting to reach the CMTS and will drop offline.

### Data Link / Network Layer (L2/L3) Steps
1. **Check IP Allocation:** Run `ipconfig /all` or `ip a` to check for APIPA self-assigned address (`169.254.x.x`), indicating local DHCP failure.
2. **Gateway Hop Isolation:** Ping default gateway; if packet loss occurs, problem is internal LAN/WLAN.
3. **External Transit Isolation:** Ping public DNS resolvers (`8.8.8.8` or `1.1.1.1`); if gateway passes but external fails, problem is CMTS routing or upstream WAN outage.