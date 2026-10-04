---
aliases: [Linux CLI, Bash Scripting, Sysadmin, Shell Commands]
tags: [linux, sysadmin, bash, automation]
created: 2026-09-19
up: "[[01 Technical Skills]]"
---

# 🐧 Linux CLI Administration & Bash Automation

A reference guide for command-line system operations, permissions architectures, and automated shell scripting.

---

## 1. Everyday Power-User Commands

### Process & Resource Diagnostics
```bash
# Display live interactive process table sorted by memory usage
top -o %MEM

# Locate process holding a specific network port (e.g., 8080)
ss -tulpn | grep :8080

# Trace system calls of an active process
strace -p <PID>
```

### Text Processing with Sed & Awk
```bash
# Print only IP addresses from an Apache/Nginx access log (field 1)
awk '{print $1}' access.log | sort | uniq -c | sort -nr

# Replace all instances of 'dev_db' with 'prod_db' in config files
sed -i 's/dev_db/prod_db/g' config/*.json
```

---

## 2. Linux Permissions Architecture

```
   File Type     User (Owner)       Group            Others
       │          r   w   x        r   w   x        r   w   x
       ▼         ─── ─── ───      ─── ─── ───      ─── ─── ───
      [-]         4 + 2 + 1        4 + 2 + 1        4 + 2 + 1
                   = 7              = 5              = 5
```

- **Read ($r=4$):** View file contents / list directory.
- **Write ($w=2$):** Modify file / create or delete files inside directory.
- **Execute ($x=1$):** Run file as program / traverse into directory.

---

## 3. Production Automated Backup Script

A robust Bash script template incorporating error trapping, timestamping, tarball compression, and log output:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Configuration
BACKUP_SRC="/var/www/html"
BACKUP_DEST="/opt/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
ARCHIVE_NAME="site_backup_${TIMESTAMP}.tar.gz"
LOG_FILE="/var/log/backup_operations.log"

# Log execution
log_msg() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_msg "Starting backup of ${BACKUP_SRC}..."

mkdir -p "${BACKUP_DEST}"

# Execute compressed archive
tar -czf "${BACKUP_DEST}/${ARCHIVE_NAME}" -C "${BACKUP_SRC}" .

# Compute checksum
CHECKSUM=$(sha256sum "${BACKUP_DEST}/${ARCHIVE_NAME}" | awk '{print $1}')
log_msg "Archive created successfully: ${ARCHIVE_NAME}"
log_msg "SHA256: ${CHECKSUM}"

# Retention: Delete archives older than 14 days
find "${BACKUP_DEST}" -type f -name "*.tar.gz" -mtime +14 -exec rm {} \;
log_msg "Backup cleanup cycle completed."
```