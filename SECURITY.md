# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly:

1. **Do not** open a public GitHub issue for security vulnerabilities.
2. Email the maintainer at the contact address listed in the README.
3. Include a description of the vulnerability, steps to reproduce, and potential impact.

We will acknowledge receipt within 48 hours and aim to provide a fix or mitigation plan within 7 days.

## Scope

This repository is a static GitHub profile page. The primary security concerns are:

- Accidental exposure of secrets or credentials via commits
- PII (personally identifiable information) exposure in public-facing content

## Best Practices for Contributors

- Never commit secrets, API keys, or credentials to this repository.
- Use the `.gitignore` file to prevent accidental commits of sensitive files.
- Review all changes for PII before pushing.
