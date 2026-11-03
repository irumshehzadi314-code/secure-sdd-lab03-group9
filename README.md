# Secure SDD Lab 03 — Group 9

**Scenario 1: MediCare Hospital Patient Record Portal**

## Group Members
- Amina Rashid — UW-24-CY-BS-044 (Lead / Fix Developer)
- Iram Shehzadi — UW-24-CY-BS-015 (Scan Engineer)
- Salika Bibi — UW-24-CY-BS-008 (Code Reviewer / GitHub Maintainer)

## Scenario Description
A hospital patient portal written in Flask is being reviewed before launch. Missing role checks let any user read other patients' records. We scanned the code, fixed the vulnerabilities, proved the fixes, and added a custom rule.

## Findings Before and After
- **Baseline:** 6 findings (4 ERROR, 2 WARNING) 
- **After Fixes:** 0 findings

## Top 3 Findings and Fixes
1. **SQL Injection (rules.sql-string-formatting):** Fixed by using parameterised queries and adding ownership checks.
2. **Hardcoded Secret (rules.hardcoded-secret):** Fixed by reading `SECRET_KEY` from environment variables.
3. **Weak Hash (rules.weak-hash-md5):** Fixed by using Werkzeug's `check_password_hash`.

## Repository Files
- `app/app.py` — The vulnerable Flask application and the secure fixes.
- `app/make_db.py` — Script to build the test database.
- `rules/owasp-local.yml` — The baseline Semgrep rules used for scanning.
- `rules/no-md5.yml` — Custom Semgrep rule to prevent MD5 usage.
- `reports/` — Baseline and after-fix scan reports (JSON and SARIF).
- `tests/test_login.py` — Contains the false positive test fixture.
- `screenshots/` — Evidence of scans, GitHub workflow, and manual tests.

## Exact Scan Commands
```bash
semgrep --config rules/owasp-local.yml --metrics=off app/
semgrep --config rules/owasp-local.yml --metrics=off --json -o reports/baseline.json app/
semgrep --config rules/owasp-local.yml --metrics=off --json -o reports/after.json app/
