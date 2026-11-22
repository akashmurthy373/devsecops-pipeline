# DevSecOps Pipeline — Automated Security Testing

[![Security Pipeline](https://github.com/akashmurthy373/devsecops-pipeline/actions/workflows/security.yml/badge.svg)](https://github.com/akashmurthy373/devsecops-pipeline/actions/workflows/security.yml)

> A production-style CI/CD security pipeline built with GitHub Actions.  
> Three automated security scans run in parallel on every push and pull request.

---

## 🔍 What It Does

| Scan | Tool | Checks For | Report |
|------|------|-----------|--------|
| 🔑 Secret Scanning | [Gitleaks](https://github.com/gitleaks/gitleaks) | Hardcoded API keys, tokens, passwords | GitHub Security tab |
| 📦 Dependency Audit | [pip-audit](https://github.com/pypa/pip-audit) | CVEs in Python packages (via PyPI Advisory DB) | Action log |
| 🔍 Static Analysis (SAST) | [Bandit](https://bandit.readthedocs.io/) | Insecure code patterns (shell injection, eval, weak crypto) | GitHub Security tab |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Developer pushes code              │
└──────────────────────────┬──────────────────────────┘
                           │  triggers
                           ▼
           ┌───────────────────────────────┐
           │     GitHub Actions Runner     │
           │        (ubuntu-latest)        │
           └───────┬───────────┬───────────┘
                   │           │           │
        ┌──────────▼──┐  ┌─────▼──────┐  ┌▼────────────┐
        │  Gitleaks   │  │  pip-audit │  │   Bandit    │
        │  (secrets)  │  │  (CVEs)    │  │   (SAST)    │
        └──────┬──────┘  └─────┬──────┘  └─────┬───────┘
               │               │               │
               └───────────────┼───────────────┘
                               │  SARIF upload
                               ▼
                 ┌─────────────────────────┐
                 │  GitHub Security Tab    │
                 │  Code Scanning Results  │
                 └─────────────────────────┘
```

---

## 🔒 Security Gates

Branch protection rules are configured on `main` so that **pull requests cannot be merged** unless all three security checks pass. This prevents vulnerable or insecure code from ever reaching the main branch.

---

## 📂 Project Structure

```
devsecops-pipeline/
├── .github/
│   └── workflows/
│       └── security.yml     ← pipeline definition (3 parallel jobs)
├── app/
│   ├── main.py              ← Python application fixture (scanned by Bandit)
│   └── requirements.txt     ← dependencies (scanned by pip-audit)
├── .gitleaks.toml           ← Gitleaks allowlist configuration
└── README.md
```

---

## 🛠️ Tools & Why They Were Chosen

### Gitleaks
- **Why:** The #1 cause of security breaches in startups is accidentally committed secrets (AWS keys, database passwords). Gitleaks scans every file and every commit in git history.
- **How it fails:** Exit code 1 if any pattern matching a known secret format is found.

### pip-audit
- **Why:** 78% of applications use at least one open-source package with a known vulnerability (Snyk State of Open Source 2023). pip-audit queries the PyPI Advisory Database and OSV.
- **How it fails:** Exit code 1 if any installed package has an unpatched CVE.

### Bandit
- **Why:** SAST catches entire categories of bugs before they reach production: SQL injection, shell injection, hardcoded credentials, use of `eval()`, insecure deserialization.
- **How it fails:** Exit code 1 on Medium or High severity findings. Results are uploaded as SARIF to GitHub's Code Scanning dashboard.

---

## ⚡ Running the Pipeline

The pipeline runs automatically. To trigger it manually:
1. Make any change to a file
2. `git add . && git commit -m "trigger scan" && git push`
3. Go to the **Actions** tab to watch it run

To view security findings:
- Go to **Security → Code scanning** in this repository

---

## 🧪 Demo Findings (Documented)

| Finding | Tool | File | Status |
|---------|------|------|--------|
| `requests==2.31.0` — 6 CVEs (PYSEC-2026-1873, 1872, 2275) | pip-audit | `app/requirements.txt` | ✅ Fixed → upgraded to `2.33.0` |
| `subprocess.run(shell=True)` — B602 HIGH severity | Bandit | `app/main.py` | ✅ Fixed → removed `shell=True` |

---

## 📚 Learning Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Gitleaks Rules](https://github.com/gitleaks/gitleaks/blob/master/config/gitleaks.toml)
- [pip-audit CVE Database](https://osv.dev/)
- [Bandit Test Plugins](https://bandit.readthedocs.io/en/latest/plugins/index.html)
- [SARIF Format Overview](https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/sarif-support-for-code-scanning)
