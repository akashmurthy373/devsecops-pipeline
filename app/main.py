# app/main.py
# ─────────────────────────────────────────────────────────────────
# DevSecOps Pipeline — Flask API
#
# A small REST API that acts as a "security scan results dashboard".
# Five routes return JSON data about the pipeline's scan results.
# This gives Bandit, pip-audit, and Gitleaks something real to scan.
#
# Routes:
#   GET  /              → API info and version
#   GET  /health        → health check for all scanners
#   GET  /results       → all scan results
#   GET  /results/<id>  → one result by ID
#   POST /scan          → simulate triggering a scan
# ─────────────────────────────────────────────────────────────────

from flask import Flask, jsonify, request
from datetime import datetime, timezone

app = Flask(__name__)

# In-memory store of scan results (no database needed for this demo)
SCAN_RESULTS = [
    {"id": 1, "tool": "Gitleaks",  "category": "Secret Scanning",   "status": "passed", "findings": 0},
    {"id": 2, "tool": "pip-audit", "category": "Dependency Audit",   "status": "passed", "findings": 0},
    {"id": 3, "tool": "Bandit",    "category": "Static Analysis",    "status": "passed", "findings": 0},
    {"id": 4, "tool": "Trivy",     "category": "Container Scanning", "status": "passed", "findings": 0},
]


@app.route("/")
def index():
    """Return basic API info."""
    return jsonify({
        "name": "DevSecOps Pipeline API",
        "version": "1.0.0",
        "description": "Security scan results dashboard",
        "status": "running",
        "endpoints": ["/health", "/results", "/results/<id>", "/scan"]
    })


@app.route("/health")
def health():
    """Return health status of all pipeline scanners."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "scanners": {
            "secret_scanning": "gitleaks",
            "dependency_audit": "pip-audit",
            "static_analysis":  "bandit",
            "container_scan":   "trivy"
        }
    })


@app.route("/results")
def get_results():
    """Return all scan results."""
    return jsonify({
        "total": len(SCAN_RESULTS),
        "results": SCAN_RESULTS
    })


@app.route("/results/<int:result_id>")
def get_result(result_id):
    """Return a single scan result by its ID."""
    result = next((r for r in SCAN_RESULTS if r["id"] == result_id), None)
    if result is None:
        return jsonify({"error": f"No result found with id {result_id}"}), 404
    return jsonify(result)


@app.route("/scan", methods=["POST"])
def trigger_scan():
    """Simulate triggering a new security scan for a given repo."""
    data = request.get_json(silent=True) or {}
    repo = data.get("repo", "unknown")
    branch = data.get("branch", "main")

    return jsonify({
        "message": "Scan queued successfully",
        "repo": repo,
        "branch": branch,
        "status": "queued",
        "queued_at": datetime.now(timezone.utc).isoformat()
    }), 202   # 202 Accepted = request received, processing later


if __name__ == "__main__":
    # debug=False is important in production — debug=True exposes an
    # interactive shell that lets attackers run code on your server.
    app.run(host="0.0.0.0", port=5000, debug=False)
