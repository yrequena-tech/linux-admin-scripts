# ============================================================
# Security Compliance Checker — Fedora Linux
# Author: Yesenia Requena | GitHub: yrequena-tech
# Program: AAS Cybersecurity, LaGuardia Community College
#          NSA-Designated CAE-CD Program
# Date: June 2026
#
# Purpose:
#   Audits a Fedora Linux system against security best
#   practices and outputs color-coded PASS/WARN/FAIL results
#   with a compliance score, letter grade, and timestamped
#   report saved to file.
#
# Controls mapped to NIST SP 800-53 and CIS Benchmarks.
#
# Checks performed:
#   1. SSH root login configuration       (AC-6)
#   2. Firewall status                    (SC-7)
#   3. Password policy                    (IA-5)
#   4. Failed login attempts (24h)        (AU-2)
#   5. Pending system updates             (SI-2)
#   6. World-writable files in /etc       (AC-3)
#   7. Unused/stale user accounts (90d)   (AC-2)
# ============================================================

import subprocess
import os
import datetime

RED = '\033[91m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
RESET = '\033[0m'
BOLD = '\033[1m'

results = []
score = 0
total = 0

def print_result(label, status, detail, nist):
    global score, total
    total += 1
    if status == 'PASS':
        color = GREEN
        score += 1
    elif status == 'WARN':
        color = YELLOW
    else:
        color = RED
    line = f"{color}[{status}]{RESET} {BOLD}{label}{RESET} — {detail} | NIST: {nist}"
    print(line)
    results.append(f"[{status}] {label} — {detail} | NIST: {nist}")

def check_ssh():
    try:
        with open('/etc/ssh/sshd_config', 'r') as f:
            content = f.read()
        if 'PermitRootLogin no' in content:
            print_result("SSH Root Login", "PASS", "Root login disabled", "AC-6")
        elif 'PermitRootLogin yes' in content:
            print_result("SSH Root Login", "FAIL", "Root login enabled — disable it", "AC-6")
        else:
            print_result("SSH Root Login", "WARN", "PermitRootLogin not explicitly set", "AC-6")
    except:
        print_result("SSH Root Login", "WARN", "Could not read sshd_config", "AC-6")

def check_firewall():
    try:
        result = subprocess.run(['firewall-cmd', '--state'], capture_output=True, text=True)
        if 'running' in result.stdout:
            print_result("Firewall Status", "PASS", "firewalld is running", "SC-7")
        else:
            print_result("Firewall Status", "FAIL", "firewalld is not running", "SC-7")
    except:
        print_result("Firewall Status", "FAIL", "Could not check firewall", "SC-7")

def check_password_policy():
    try:
        with open('/etc/login.defs', 'r') as f:
            content = f.read()
        issues = []
        if 'PASS_MAX_DAYS\t99999' in content or 'PASS_MAX_DAYS   99999' in content:
            issues.append("max age not set")
        if issues:
            print_result("Password Policy", "WARN", "Issues: " + ", ".join(issues), "IA-5")
        else:
            print_result("Password Policy", "PASS", "Password policy configured", "IA-5")
    except:
        print_result("Password Policy", "WARN", "Could not read login.defs", "IA-5")

def check_failed_logins():
    try:
        result = subprocess.run(
            ['journalctl', '-u', 'sshd', '--since', '24 hours ago', '--no-pager'],
            capture_output=True, text=True
        )
        failures = result.stdout.count('Failed password')
        if failures == 0:
            print_result("Failed Logins (24h)", "PASS", "No failed SSH logins", "AU-2")
        elif failures < 10:
            print_result("Failed Logins (24h)", "WARN", f"{failures} failed attempts", "AU-2")
        else:
            print_result("Failed Logins (24h)", "FAIL", f"{failures} failed attempts — possible brute force", "AU-2")
    except:
        print_result("Failed Logins (24h)", "WARN", "Could not read journal", "AU-2")

def check_updates():
    try:
        result = subprocess.run(['dnf', 'check-update', '--quiet'], capture_output=True, text=True)
        if result.returncode == 0:
            print_result("Pending Updates", "PASS", "System is up to date", "SI-2")
        else:
            print_result("Pending Updates", "WARN", "Updates are available — apply them", "SI-2")
    except:
        print_result("Pending Updates", "WARN", "Could not check updates", "SI-2")

def check_world_writable():
    try:
        result = subprocess.run(
            ['find', '/etc', '-maxdepth', '1', '-perm', '-o+w', '-type', 'f'],
            capture_output=True, text=True
        )
        files = result.stdout.strip().split('\n')
        files = [f for f in files if f]
        if not files:
            print_result("World-Writable Files (/etc)", "PASS", "No world-writable files found", "AC-3")
        else:
            print_result("World-Writable Files (/etc)", "FAIL", f"{len(files)} world-writable file(s) found", "AC-3")
    except:
        print_result("World-Writable Files (/etc)", "WARN", "Could not check file permissions", "AC-3")

def check_unused_accounts():
    try:
        result = subprocess.run(['lastlog', '--before', '90'], capture_output=True, text=True)
        lines = [l for l in result.stdout.split('\n') if '**Never logged in**' not in l and l.strip() and 'Username' not in l]
        if not lines:
            print_result("Unused Accounts (90d)", "PASS", "No stale accounts detected", "AC-2")
        else:
            print_result("Unused Accounts (90d)", "WARN", f"{len(lines)} account(s) inactive 90+ days", "AC-2")
    except:
        print_result("Unused Accounts (90d)", "WARN", "Could not check account activity", "AC-2")

def print_report():
    global score, total
    percent = int((score / total) * 100) if total > 0 else 0
    if percent >= 90:
        grade = 'A'
    elif percent >= 80:
        grade = 'B'
    elif percent >= 70:
        grade = 'C'
    elif percent >= 60:
        grade = 'D'
    else:
        grade = 'F'
    summary = f"\n{'='*50}\nCOMPLIANCE SCORE: {score}/{total} ({percent}%) — Grade: {grade}\n{'='*50}"
    print(BOLD + summary + RESET)
    results.append(summary)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"compliance_report_{timestamp}.txt"
    with open(filename, 'w') as f:
        f.write(f"Security Compliance Report — {timestamp}\n")
        f.write("="*50 + "\n")
        for line in results:
            f.write(line + "\n")
    print(f"\n{GREEN}Report saved to: {filename}{RESET}")

def main():
    print(BOLD + "\nSecurity Compliance Checker — Fedora Linux" + RESET)
    print("Mapped to NIST SP 800-53 | " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("="*50)
    check_ssh()
    check_firewall()
    check_password_policy()
    check_failed_logins()
    check_updates()
    check_world_writable()
    check_unused_accounts()
    print_report()

if __name__ == "__main__":
    main()
