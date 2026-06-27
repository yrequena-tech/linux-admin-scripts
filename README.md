# Linux Admin Scripts

A collection of Bash shell scripts for Linux system administration.
Built on Fedora as part of MAC 232 - Unix/Linux coursework at LaGuardia Community College.

## Scripts

| Script | Description |
|--------|-------------|
| user_admin.sh | Add, delete, and manage user accounts |
| backup_all_homes.sh | Backup all home directories with timestamps |
| cleanup_with_confirm | Delete old files with user confirmation |
| add_users.sh | Add multiple users from a text file |
| check_service.sh | Check if a system service is running |
| system_update.sh | System update and upgrade with confirmation |
| network_scan.sh | Ping sweep to discover live hosts on subnet |
| user_menu.sh | Menu-driven user management tool |
| ip_monitor.sh | Monitor public IP and detect changes |
| ssh_checker.sh | Check SSH availability across a server list |# linux-admin-scripts

## Security Compliance Checker
**File:** `security_compliance_checker.py`  
**Language:** Python 3  
**Author:** Yesenia Requena 

### Overview
A Python-based security audit tool that evaluates a Fedora Linux system against 
industry security best practices. Outputs color-coded PASS/WARN/FAIL results with 
a compliance score, letter grade, and timestamped report saved to file.

### Controls Framework
All checks are mapped to **NIST SP 800-53** security controls.

### Checks Performed
| Check | NIST Control | Description |
|-------|-------------|-------------|
| SSH Root Login | AC-6 | Verifies root login is disabled in sshd_config |
| Firewall Status | SC-7 | Confirms firewalld is active |
| Password Policy | IA-5 | Checks password aging in /etc/login.defs |
| Failed Logins (24h) | AU-2 | Detects brute force attempts via journalctl |
| Pending Updates | SI-2 | Identifies unpatched packages via dnf |
| World-Writable Files | AC-3 | Scans /etc for insecure file permissions |
| Unused Accounts (90d) | AC-2 | Flags stale user accounts |

### Usage
```bash
sudo python3 security_compliance_checker.py
```

### Sample Output
```
Security Compliance Checker — Fedora Linux
Mapped to NIST SP 800-53 | 2026-06-27 04:56:06
==================================================
[WARN] SSH Root Login — PermitRootLogin not explicitly set | NIST: AC-6
[PASS] Firewall Status — firewalld is running | NIST: SC-7
[WARN] Password Policy — Issues: max age not set | NIST: IA-5
[PASS] Failed Logins (24h) — No failed SSH logins | NIST: AU-2
[WARN] Pending Updates — Updates are available | NIST: SI-2
[PASS] World-Writable Files (/etc) — No world-writable files found | NIST: AC-3
[WARN] Unused Accounts (90d) — Could not check account activity | NIST: AC-2
==================================================
COMPLIANCE SCORE: 3/7 (42%) — Grade: F
==================================================
Report saved to: compliance_report_2026-06-27_04-56-07.txt
```

