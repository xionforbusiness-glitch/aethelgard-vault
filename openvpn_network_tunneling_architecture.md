---
aliases: [OpenVPN Guide, Tunneling, VPN Architecture, Network Security]
tags: [networking, security, sysadmin, vpn]
created: 2026-09-19
up: "[[Technical/Skills_and_Stack]]"
related: ["[[Technical/Networking_Wireshark_Playbook]]"]
---

# 🔒 OpenVPN Architecture & Network Tunneling Protocols

An in-depth technical analysis of virtual network interfaces, cryptographic encapsulation, and gateway packet routing.

---

## 1. TUN vs. TAP Interface Comparison

OpenVPN creates a virtual software network interface managed by the operating system kernel.

```
                  ┌───────────────────────────────┐
                  │       User Space (OpenVPN)    │
                  └──────────────┬────────────────┘
                                 │
                         read()  │  write()
                                 ▼
                  ┌───────────────────────────────┐
                  │      Kernel Space (TUN/TAP)   │
                  └──────────────┬────────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 ▼                               ▼
       [ TUN (Layer 3: IP) ]           [ TAP (Layer 2: Ethernet) ]
    - Operates with IP Packets      - Operates with Ethernet Frames
    - No MAC headers transmitted    - Preserves MAC addresses & ARP
    - Lower protocol overhead       - Supports non-IP broadcast (LAN games)
    - Recommended for Site-to-Client- Used for full bridged networks
```

---

## 2. Cryptographic Security Architecture

OpenVPN establishes two distinct communication channels multiplexed over a single UDP/TCP port (default: UDP 1194):

### 1. Control Channel (TLS Secured)
- Performs mutual authentication via X.509 Public Key Infrastructure (PKI) certificates.
- Negotiates ephemeral session keys via Diffie-Hellman (DH) or Elliptic Curve Diffie-Hellman Ephemeral (ECDHE), ensuring **Forward Secrecy**.
- Generates rolling symmetric keys for the data channel.

### 2. Data Channel (Symmetric Cipher)
- Encapsulates and encrypts raw client network packets.
- Employs Authenticated Encryption with Associated Data (AEAD) ciphers (e.g., `AES-256-GCM` or `CHACHA20-POLY1305`).
- Eliminates HMAC integrity overhead by calculating payload authentication directly within the cipher block.

---

## 3. Production Server Configuration Blueprint (`server.conf`)

```ini
# Network Port & Virtual Interface
port 1194
proto udp
dev tun

# Cryptographic Certificates & Keys
ca /etc/openvpn/server/ca.crt
cert /etc/openvpn/server/server.crt
key /etc/openvpn/server/server.key
dh /etc/openvpn/server/dh.pem
tls-auth /etc/openvpn/server/ta.key 0 # Directional HMAC signature against DoS

# Subnet Pool Allocation
server 10.8.0.0 255.255.255.0

# Route all outbound Internet traffic through the tunnel
push "redirect-gateway def1 bypass-dhcp"
push "dhcp-option DNS 1.1.1.1"
push "dhcp-option DNS 8.8.8.8"

# Performance Tuning & Privilege Drop
cipher AES-256-GCM
auth SHA256
keepalive 10 120
persist-key
persist-tun
user nobody
group nogroup

# Status Logging
status /var/log/openvpn/openvpn-status.log
verb 3
```

---

## 4. Linux Kernel Forwarding & NAT Masquerade

For the VPN server to act as the default gateway for remote clients, the Linux kernel must permit packet routing between the virtual `tun0` interface and the physical egress interface (e.g., `eth0`):

```bash
# 1. Enable IPv4 packet forwarding in real-time
sudo sysctl -w net.ipv4.ip_forward=1

# Persist across reboots: Ensure /etc/sysctl.conf contains:
# net.ipv4.ip_forward = 1

# 2. Add NAT Masquerade rule via iptables
sudo iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE

# 3. Allow traffic forwarding between interfaces
sudo iptables -A FORWARD -i tun0 -o eth0 -j ACCEPT
sudo iptables -A FORWARD -i eth0 -o tun0 -m state --state RELATED,ESTABLISHED -j ACCEPT
```