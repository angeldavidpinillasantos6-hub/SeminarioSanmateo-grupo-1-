#!/usr/bin/env python3
import re
from collections import Counter
from datetime import datetime

LOG_FILE = 'Server.log'
BLACKLIST_FILE = 'ip_blacklist.txt'

# Patrones que indican posibles SQLi
PATTERNS = [
    r"\bOR\s+1=1\b",
    r"\bUNION\s+SELECT\b",
    r"\bDROP\s+TABLE\b",
    r"--|/\*|\*/",
    r"EXEC\s*\(",
]

IP_REGEX = re.compile(r"(\d{1,3}(?:\.\d{1,3}){3})")

def analyze_log():
    try:
        with open(LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Log file {LOG_FILE} not found.")
        return

    hits = []
    for pat in PATTERNS:
        for m in re.finditer(pat, text, flags=re.IGNORECASE):
            # obtener IP en un radio de 200 caracteres alrededor
            start = max(0, m.start()-200)
            segment = text[start:m.end()+200]
            ips = IP_REGEX.findall(segment)
            for ip in ips:
                hits.append((ip, pat))

    counts = Counter([ip for ip, _ in hits])

    if not hits:
        print("No attack patterns detected.")
        return

    # cargar lista existente
    existing = set()
    try:
        with open(BLACKLIST_FILE, 'r') as f:
            for line in f:
                existing.add(line.strip().split()[0])
    except FileNotFoundError:
        pass

    new_entries = []
    for ip, cnt in counts.items():
        if ip not in existing:
            new_entries.append(ip)

    if new_entries:
        with open(BLACKLIST_FILE, 'a') as f:
            for ip in new_entries:
                f.write(f"{ip} # detected {datetime.utcnow().isoformat()}\n")
        print(f"Added to blacklist: {new_entries}")
    else:
        print("No new IPs to add to blacklist.")

    # Estadísticas
    print("Attack counts by IP:")
    for ip, c in counts.items():
        print(f"{ip}: {c}")

if __name__ == '__main__':
    analyze_log()
