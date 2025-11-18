# DevSecOps Practice Project

This is a sample Python Flask application intentionally containing various security vulnerabilities and code quality issues for DevSecOps practice.

## Intentional Security Issues

1. **Hardcoded Secrets**: Secret keys and credentials in source code
2. **SQL Injection**: Unsanitized user input in SQL queries
3. **Command Injection**: Unsafe shell command execution
4. **SSTI**: Server-Side Template Injection vulnerability
5. **Insecure Deserialization**: Using pickle with untrusted data
6. **Weak Cryptography**: MD5 for password hashing
7. **Debug Mode**: Flask debug mode enabled in production
8. **Open Redirect**: Unvalidated URL redirects
9. **Unrestricted File Upload**: No file type validation
10. **Vulnerable Dependencies**: Outdated packages with known CVEs

## Code Quality Issues

- Unused variables and imports
- Poor function naming
- High cyclomatic complexity
- PEP 8 violations
- Missing docstrings
- Long parameter lists

## Tools to be Used

### A Level - Linting
- Flake8
- Pylint

### E Level - SCA
- pip-audit
- Safety

### O Level - Advanced
- Semgrep (SAST)
- Bandit (Security-focused linter)

## Setup

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

⚠️ **WARNING**: Do NOT run this application in production or on a public network. It contains intentional security vulnerabilities for educational purposes only.
