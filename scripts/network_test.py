#!/usr/bin/env python3
"""Network connectivity test."""
import socket
import sys

domains = ["api.xiaomi.com", "token-plan-ams.xiaomimimo.com", "google.com"]

print("=== DNS RESOLUTION TEST ===")
for domain in domains:
    try:
        result = socket.gethostbyname(domain)
        print(f"✅ {domain} -> {result}")
    except Exception as e:
        print(f"❌ {domain} -> {e}")

print("\n=== DNS CONFIGURATION ===")
with open('/etc/resolv.conf', 'r') as f:
    print(f.read())
