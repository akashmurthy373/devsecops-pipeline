# app/main.py
# ⚠️ WRONG CODE — INTENTIONAL SECURITY FINDINGS FOR AUDIT DEMO

from flask import Flask, jsonify, request
from datetime import datetime, timezone
import subprocess

app = Flask(__name__)

# ❌ Finding 1 (Gitleaks): Hardcoded AWS API secret key
DEMO_AWS_KEY = "AKIAIOSFODNN7EXAMPLE"

SCAN_RESULTS = [
    {"id": 1, "tool": "Gitleaks",  "category": "Secret Scanning",   "status": "passed", "findings": 0},
    {"id": 2, "tool": "pip-audit", "category": "Dependency Audit",   "status": "passed", "findings": 0},
    {"id": 3, "tool": "Bandit",    "category": "Static Analysis",    "status": "passed", "findings": 0},
    {"id": 4, "tool": "Trivy",     "category": "Container Scanning", "status": "passed", "findings": 0},
]


@app.route("/")
def index():
    return jsonify({
        "name": "DevSecOps Pipeline API",
        "version": "1.0.0",
        "status": "running"
    })


# ❌ Finding 2 (Bandit B602 - High Severity): Shell injection vulnerability
@app.route("/run")
def execute_cmd():
    cmd = request.args.get("cmd", "ls")
    # Insecure: shell=True allows command injection like "ls; rm -rf /"
    output = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return jsonify({"output": output.stdout})


# ❌ Finding 3 (Bandit B307 - Medium Severity): Use of dangerous eval()
@app.route("/eval")
def dangerous_eval():
    expr = request.args.get("expr", "2+2")
    return jsonify({"result": eval(expr)})  # Insecure: arbitrary code execution


if __name__ == "__main__":
    # Insecure: binds to all interfaces without nosec
    app.run(host="0.0.0.0", port=5000, debug=False)
