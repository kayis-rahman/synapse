# Security Policy

## Supported Versions
Security updates will be provided for the latest version.

## Reporting a Vulnerability

If you discover a security vulnerability in SYNAPSE, please report it responsibly.

### Disclosure
**Do NOT** open a public GitHub issue
- Email: kaisbk1@gmail.com
- Include details: version, reproduction steps, impact
- Allow 48 hours for response before public disclosure

### What to Include
- Description of the vulnerability
- Steps to reproduce
- Proof of concept (optional)
- Affected versions
- Impact assessment

## Security Best Practices

### Data Protection
- All databases use SQLite with appropriate permissions
- Sensitive data (API keys) use environment variables
- File uploads restricted to `/tmp/rag-uploads` directory

### Access Control
- MCP server runs with non-root user in container
- Unix permissions set to 0700 on upload directories

### Network Security
- HTTP MCP server supports CORS configuration
- Transport security settings configurable
- No default credentials included

## Known Vulnerabilities

None at this time.

## Dependencies

We regularly audit dependencies:
- llama-cpp-python
- fastapi
- pydantic
- mcp-server

## Compliance

- MIT License
- No GDPR/PII handling by design (local-only)
