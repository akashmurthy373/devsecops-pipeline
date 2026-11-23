# app/main.py
# ─────────────────────────────────────────────────────────────────
# DevSecOps Pipeline — Flask REST API (Clean & Secured)
# ─────────────────────────────────────────────────────────────────

from flask import Flask, jsonify, request
from datetime import datetime, timezone

app = Flask(__name__)

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
        "description": "Security scan results dashboard",
        "status": "running",
        "endpoints": ["/health", "/results", "/results/<id>", "/scan"]
    })


@app.route("/health")
def health():
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
    return jsonify({
        "total": len(SCAN_RESULTS),
        "results": SCAN_RESULTS
    })


@app.route("/results/<int:result_id>")
def get_result(result_id):
    result = next((r for r in SCAN_RESULTS if r["id"] == result_id), None)
    if result is None:
        return jsonify({"error": f"No result found with id {result_id}"}), 404
    return jsonify(result)


@app.route("/scan", methods=["POST"])
def trigger_scan():
    data = request.get_json(silent=True) or {}
    repo = data.get("repo", "unknown")
    branch = data.get("branch", "main")

    return jsonify({
        "message": "Scan queued successfully",
        "repo": repo,
        "branch": branch,
        "status": "queued",
        "queued_at": datetime.now(timezone.utc).isoformat()
    }), 202


if __name__ == "__main__":
    # nosec B104 — binding to 0.0.0.0 is intentional inside Docker container
    app.run(host="0.0.0.0", port=5000, debug=False)  # nosec B104
