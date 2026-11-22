# DevSecOps Pipeline — Automated Security Testing

[![Security Pipeline](https://github.com/akashmurthy373/devsecops-pipeline/actions/workflows/security.yml/badge.svg)](https://github.com/akashmurthy373/devsecops-pipeline/actions/workflows/security.yml)

> A production-style CI/CD security pipeline built with GitHub Actions.
> Four automated security scans run in parallel on every push, pull request,
> and on a weekly schedule — protecting a Flask REST API.

---

## 🔍 What It Scans

| # | Scan | Tool | Checks For | Report |
|---|------|------|-----------|--------|
| 1 | 🔑 Secret Scanning | [Gitleaks](https://github.com/gitleaks/gitleaks) | Hardcoded API keys, tokens, passwords in code or git history | GitHub Security tab |
| 2 | 📦 Dependency Audit | [pip-audit](https://github.com/pypa/pip-audit) | Known CVEs in Python packages (via PyPI Advisory DB) | Action log |
| 3 | 🔍 Static Analysis (SAST) | [Bandit](https://bandit.readthedocs.io/) | Insecure code patterns: shell injection, eval(), weak crypto | GitHub Security tab + Artifact |
| 4 | 🐳 Container Scanning | [Trivy](https://trivy.dev/) | CVEs in the Docker image: OS libraries, base image, packages | GitHub Security tab + Artifact |

---

## 🏗️ Architecture

```
Developer pushes code
        │
        ▼
GitHub Actions triggers pipeline
        │
   ┌────┴─────────────────────────────────┐
   │                                      │
   ▼         ▼           ▼               ▼
Gitleaks  pip-audit    Bandit           Trivy
(secrets) (CVEs in    (insecure    (CVEs in Docker
          packages)    code)         container)
   │         │           │               │
   └────┬────┘           └───────┬───────┘
        │                        │
        ▼                        ▼
   Action log             GitHub Security tab
                          + Downloadable SARIF artifacts
                                 │
        ┌────────────────────────┘
        ▼
   Branch Protection: PR merge BLOCKED until all 4 pass
```

---

## 📂 Project Structure

```
devsecops-pipeline/
├── .github/
│   └── workflows/
│       └── security.yml    ← pipeline: 4 parallel jobs + 4 extra features
├── app/
│   ├── main.py             ← Flask REST API (5 routes, scanned by Bandit)
│   └── requirements.txt    ← Python deps (scanned by pip-audit)
├── Dockerfile              ← container definition (scanned by Trivy)
├── .dockerignore           ← excludes secrets/.git from the image
├── .gitleaks.toml          ← Gitleaks allowlist config
└── README.md
```

---

## ⚙️ Pipeline Features

| Feature | How It Works |
|---------|-------------|
| ▶️ **Manual trigger** | "Run workflow" button in the Actions tab |
| ⏰ **Weekly schedule** | Runs every Monday 2 AM UTC — catches new CVEs automatically |
| 📋 **Job summaries** | Each job writes a formatted markdown report to the Actions UI |
| 💾 **Artifact download** | Bandit & Trivy SARIF reports downloadable for 30 days |
| 🔒 **Branch protection** | PRs to `main` blocked until all 4 checks pass |
| 🛡️ **Security tab** | Findings shown file-by-file with severity and line numbers |

---

## 🔒 Security Gates

Branch protection rules are configured on `main` so that **pull requests cannot be merged** unless all four security checks pass. This prevents vulnerable or insecure code from ever reaching the production branch.

---

## 🧪 Real Findings Caught & Fixed

| Finding | Tool | Severity | Fix Applied |
|---------|------|----------|-------------|
| `requests==2.31.0` — PYSEC-2026-1873, 1872, 2275 | pip-audit | High | Upgraded to `2.33.0` |
| `subprocess.run(shell=True)` — B602 | Bandit | High | Changed to `shell=False` with arg list |

---

## 🌐 The Flask API (What Gets Protected)

A REST API serving security scan results. Five endpoints:

| Method | Route | Returns |
|--------|-------|---------|
| `GET` | `/` | API name, version, status |
| `GET` | `/health` | Health check + list of scanners |
| `GET` | `/results` | All scan results |
| `GET` | `/results/<id>` | One scan result by ID |
| `POST` | `/scan` | Simulate queuing a new scan |

---

## 📚 Learning Resources

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Gitleaks Rules Reference](https://github.com/gitleaks/gitleaks/blob/master/config/gitleaks.toml)
- [pip-audit / OSV Database](https://osv.dev/)
- [Bandit Plugin Index](https://bandit.readthedocs.io/en/latest/plugins/index.html)
- [Trivy Documentation](https://trivy.dev/latest/docs/)
- [SARIF in GitHub Code Scanning](https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/sarif-support-for-code-scanning)
