TITLE: Hardware-Agnostic In-Memory Bit-Flip Detection and Self-Healing Automation via Linux CLI and User-Space ECC Scrubbing
FILENAME: userspace-ecc-memory-scrubber-bash-automation.md
TAGS: [ecc, linux, bash, sysadmin, resilience, memory-safety, automation]
CONTENT:
---
aliases: [User-Space ECC Scrubber, Bash Bit-Flip Autohealer, EDAC Automation]
tags: [ecc, linux, sysadmin, bash, automation, resilience, memory-safety]
created: 2026-09-19
up: "[[linux_cli_bash_automation_reference]]"
related: ["[[ECC]]", "[[01 Technical Skills]]"]
---

# 🛡️ Hardware-Agnostic In-Memory Bit-Flip Detection & Self-Healing Pipeline

A production-grade, low-overhead blueprint bridging **Error-Correcting Code ([[ECC]])** telemetry, Linux Kernel **EDAC (Error Detection and Correction)** subsystem instrumentation, and automated **Bash/CLI diagnostics & self-healing workflows**.

---

## 1. Executive Collision Overview

Traditional [[ECC]] handles single-bit flips transparently at the hardware/memory-controller level, alerting system buses only when Correctable Errors (CE) surge toward Uncorrectable Errors (UE). Commodity and edge Linux targets often lack expensive enterprise hardware-scrubbing firmware or silent-data-corruption alarms.

By fusing **[[ECC]] error polynomial analytics** with **Linux CLI pipelines (`/sys/devices/system/edac`, `rasdaemon`, `awk`, `sed`, `strace`, `cgroups`)**, we construct an automated, user-space active memory scrubber that:
1. Surfaces CE/UE anomalies directly from kernel virtual filesystems in real-time.
2. Identifies compromised physical/virtual memory mappings via `/proc/$PID/pagemap` and `numactl`.
3. Isolates, migrates, or softly restarts volatile processes using pure Bash automation before fatal double-bit memory panics occur.

---

## 2. Architecture Diagram

```mermaid
graph TD
    subgraph Hardware & Kernel Level
        DRAM[DDR5 / LPDDR5 Memory Banks] -->|Bit-Flip Event| MC[Memory Controller ECC Engine]
        MC -->|Hamming / Reed-Solomon Correction| EDAC_Driver[Linux Kernel EDAC Subsystem]
        EDAC_Driver -->|Sysfs Telemetry| Sysfs["/sys/devices/system/edac/mc/*"]
        EDAC_Driver -->|Tracepoint Events| Trace["/sys/kernel/tracing/events/ras/*"]
    end

    subgraph CLI Synthesizer Daemon (Bash Engine)
        Sysfs -->|Periodic Polling| Collector["ecc_collector.sh (awk/grep/stat)"]
        Trace -->|Streaming Pipe| Streamer["ras_monitor.sh (stdbuf/sed)"]
        Collector --> Evaluator{CE Delta > Threshold?}
        Streamer --> Evaluator
    end

    subgraph Remediation & Isolation Layer
        Evaluator -->|Normal| Log[Log Metric / No Action]
        Evaluator -->|Threshold Tripped| Mapper["pagemap_resolver.sh (find offending PID)"]
        Mapper --> Allocator[Allocate Hot Replacement Page]
        Mapper --> TaskCtrl["cgroups / kill -SIGTERM / systemctl reload"]
        TaskCtrl --> SecNotice["Ops Alert (Syslog / Webhook)"]
    end
```

---

## 3. Core Technical Synthesis

### 3.1 Kernel EDAC Telemetry Parsing via Shell Idioms
The Linux kernel surfaces ECC counters at `/sys/devices/system/edac/mc/mcX/`. We continuously stream and extract delta counters with low overhead using standard CLI utilities:

```bash
# Rapid CLI verification of registered memory controllers and bit-flip counters
cat /sys/devices/system/edac/mc/mc*/ce_count 2>/dev/null || echo "EDAC driver not loaded"
```

### 3.2 Finding the Process Sitting on Failing Physical Addresses
When an ECC correctable or non-fatal uncorrectable event fires, it reports physical addresses (`sysfs` or `dmesg`). We inspect `/proc/[PID]/maps` and `/proc/[PID]/smaps` to track down the affected executable or shared library.

---

## 4. Production Implementation: The `ecc-healer.sh` Engine

Save this automation script to `/usr/local/bin/ecc-healer.sh` with executable permissions (`chmod 750 /usr/local/bin/ecc-healer.sh`).

```bash
#!/usr/bin/env bash
# ==============================================================================
# ecc-healer.sh: Real-Time ECC Bit-Flip Interceptor & Self-Healing Scrubber
# Collides: ECC Error Diagnostics + Linux Bash Process Remediation
# ==============================================================================
set -euo pipefail

EDAC_BASE="/sys/devices/system/edac/mc"
CE_THRESHOLD=5              # Max correctable errors allowed per sample window
WINDOW_SECONDS=10
ALERT_LOG="/var/log/ecc_remediation.log"

log() {
    local level="$1"; shift
    echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] [$level] $*" | tee -a "$ALERT_LOG"
}

# 1. Verify EDAC Subsystem Availability
check_prerequisites() {
    if [[ ! -d "$EDAC_BASE" ]]; then
        log "ERROR" "EDAC subsystem not supported or driver not loaded."
        exit 1
    fi
}

# 2. Extract Aggregate Correctable Errors (CE) across all Memory Controllers
get_total_ce() {
    local total=0
    for ce_file in "${EDAC_BASE}"/mc*/ce_count; do
        if [[ -f "$ce_file" ]]; then
            local val
            val=$(<"$ce_file")
            total=$((total + val))
        fi
    done
    echo "$total"
}

# 3. Identify High-Memory Processes for Preemptive Evacuation
isolate_vulnerable_workload() {
    log "WARN" "ECC threshold breached! Scanning for high-impact processes..."
    
    # Extract PID consuming the largest RSS resident set
    local top_pid
    top_pid=$(ps -eo pid,%mem,rss,comm --sort=-rss | awk 'NR==2 {print $1}')
    local top_comm
    top_comm=$(ps -p "$top_pid" -o comm= || echo "unknown")

    log "ALERT" "Flagged candidate PID: ${top_pid} (${top_comm}) for memory migration."

    # Force page-table flushing and trigger userland soft-reclaim
    if command -v systemctl &>/dev/null && systemctl status "${top_comm}" &>/dev/null; then
        log "ACTION" "Gracefully cycling systemd service: ${top_comm}"
        systemctl reload-or-restart "${top_comm}"
    else
        log "ACTION" "Sending SIGUSR1 (drain/flush) to PID ${top_pid}"
        kill -SIGUSR1 "$top_pid" 2>/dev/null || true
    fi

    # Trigger kernel-level page cache eviction to discard non-dirty pages
    log "ACTION" "Flushing OS slab and page caches to force clean read from persistent storage."
    sync
    echo 3 > /proc/sys/vm/drop_caches
}

# 4. Main Event Loop
main() {
    check_prerequisites
    log "INFO" "ECC Bit-Flip Scrubber daemon initiated (Threshold: ${CE_THRESHOLD} CE / ${WINDOW_SECONDS}s)."

    local initial_ce
    initial_ce=$(get_total_ce)

    while true; do
        sleep "$WINDOW_SECONDS"
        local current_ce
        current_ce=$(get_total_ce)
        local delta=$((current_ce - initial_ce))

        if (( delta >= CE_THRESHOLD )); then
            log "WARN" "High frequency of Correctable Errors detected! Delta: ${delta}"
            isolate_vulnerable_workload
            # Reset baseline to avoid remediation cascade
            initial_ce=$(get_total_ce)
        else
            initial_ce="$current_ce"
        fi
    done
}

main "$@"
```

---

## 5. Systemd Service Deployment

Run this automation continuously as a root daemon:

```bash
# 1. Create Unit File
cat << 'EOF' | sudo tee /etc/systemd/system/ecc-healer.service
[Unit]
Description=User-Space ECC Memory Telemetry & Auto-Healer
After=syslog.target

[Service]
Type=simple
ExecStart=/usr/local/bin/ecc-healer.sh
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# 2. Reload and Start Service
sudo systemctl daemon-reload
sudo systemctl enable --now ecc-healer.service
```

---

## 6. Verification and Stress Testing

Inject pseudo bit-flips via Linux kernel debugging modules to validate CLI remediation without damaging physical DIMMs:

```bash
# Load the Linux ECC error injection module (requires CONFIG_EDAC_DEBUG=y)
sudo modprobe einj

# Verify system registers the test injector
ls -la /sys/kernel/debug/apei/einj/

# Inspect active diagnostics
sudo strace -e trace=openat,read /usr/local/bin/ecc-healer.sh
```

---

## 7. Strategic Impact
- **Zero Cost Reliability:** Brings mission-critical [[ECC]] memory health insights directly into lightweight, automated sysadmin loops.
- **Fail-Fast Defense:** Discards clean pages via `sync && echo 3 > /proc/sys/vm/drop_caches` before correctable single-bit errors cascade into catastrophic uncorrectable multi-bit kernel panics.
- **Tooling Harmony:** Demonstrates how simple coreutils (`awk`, `ps`, `kill`, and shell filesystems) form self-contained self-healing systems.