# DevSecOps Pipeline — Automated Security Testing

A GitHub Actions CI/CD pipeline that runs three automated security scans
on every push and pull request.

| Scan | Tool | Checks |
|------|------|--------|
| 🔑 Secret Scanning | Gitleaks | Hardcoded credentials |
| 📦 Dependency Audit | pip-audit | Known CVEs in packages |
| 🔍 Static Analysis | Bandit | Insecure code patterns |

## Pipeline Status
![Security Pipeline](https://github.com/akashmurthy373/devsecops-pipeline/actions/workflows/security.yml/badge.svg)

## Project Structure
```
devsecops-pipeline/
├── .github/workflows/security.yml   ← the pipeline definition
├── app/
│   ├── main.py                      ← demo application fixture
│   └── requirements.txt             ← Python dependencies
├── .gitleaks.toml                   ← Gitleaks allowlist config
└── README.md
```

## How It Works
On every `git push` or pull request, GitHub Actions automatically:
1. Spins up a fresh Ubuntu virtual machine
2. Runs **Gitleaks** to detect accidentally committed secrets
3. Runs **pip-audit** to check dependencies for known CVEs
4. Runs **Bandit** to scan Python code for insecure patterns

If any scan finds a problem, the pipeline fails and blocks the merge.
