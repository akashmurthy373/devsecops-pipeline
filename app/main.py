# app/main.py
# DevSecOps Pipeline — Application Fixture
# This file is scanned by Bandit (SAST) on every push.

import subprocess   # ← imported for the DEMO function below


def greet(name: str) -> str:
    """Return a greeting message."""
    return f"Hello, {name}! Welcome to the DevSecOps demo."


def add(a: int, b: int) -> int:
    """Return the sum of two numbers."""
    return a + b


# ─────────────────────────────────────────────────────────────────
# ⚠️  DEMO FUNCTION — intentionally insecure for Stage A demo
#
# subprocess.run() with shell=True is a HIGH-severity finding.
# It allows shell injection: if `cmd` comes from user input,
# an attacker could pass: "ls; rm -rf /" and destroy the server.
#
# Bandit rule: B602 — subprocess_popen_with_shell_equals_true
# Severity:    HIGH
# Fix:         Pass a list of arguments instead: ["ls", "-la"]
#              and remove shell=True entirely.
# ─────────────────────────────────────────────────────────────────
def run_system_command(cmd):
    """Run a system command — INSECURE (demo only)."""
    return subprocess.run(cmd, shell=True)   # noqa: B602  ← Bandit WILL flag this


if __name__ == "__main__":
    print(greet("World"))
    print(f"2 + 3 = {add(2, 3)}")
