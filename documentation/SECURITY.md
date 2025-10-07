# Security Guidelines

## Overview

This document outlines security best practices and guidelines for the Financial Advisor UI project.

## Environment Configuration Security

### Secret Management

#### ❌ Never Do This
```python
# Don't hardcode secrets in source code
SECRET_KEY = "my-secret-key-123"
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
```

#### ✅ Do This Instead
```python
# Use environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
```

### Production Environment Variables

Required environment variables for production:

```bash
# Security - REQUIRED
SECRET_KEY=<generate-strong-32+-character-key>

# AWS Credentials - Use IAM roles when possible
AWS_ACCESS_KEY_ID=<your-aws-access-key>
AWS_SECRET_ACCESS_KEY=<your-aws-secret-key>
AWS_REGION=us-east-1

# API Configuration
ENVIRONMENT=production
DEBUG=false
API_HOST=127.0.0.1  # Don't use 0.0.0.0 in production
ALLOWED_ORIGINS=https://yourdomain.com

# Database
DATABASE_URL=<secure-database-connection-string>
```

## API Security

### Authentication & Authorization

- **Session Management**: UUID-based session IDs with configurable expiration
- **Rate Limiting**: Implemented to prevent abuse (60 requests/minute default)
- **CORS**: Configured with explicit allowed origins
- **Input Validation**: All inputs validated using Pydantic models

### Security Headers

The application implements security headers:

```python
# Trusted Host Middleware (production only)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["yourdomain.com"])

# CORS with explicit origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,  # Never use ["*"] in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
```

## Data Protection

### Session Data

- Sessions expire after 2 hours by default
- No persistent storage of sensitive user data
- Session cleanup runs every 30 minutes
- User preferences stored temporarily during advisory process

### Logging Security

- No sensitive data logged in production
- IP addresses and user agents logged for security monitoring
- Error messages sanitized to prevent information disclosure

## Deployment Security

### Docker Security

```dockerfile
# Use non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
USER nextjs

# Health checks
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

### Network Security

- API bound to localhost (127.0.0.1) in production
- Use reverse proxy (nginx) for external access
- Enable HTTPS/TLS in production
- Implement proper firewall rules

## Security Checklist

### Before Deployment

- [ ] Change default secret key
- [ ] Set strong AWS credentials or use IAM roles
- [ ] Configure proper CORS origins
- [ ] Set API host to 127.0.0.1 for production
- [ ] Enable HTTPS/TLS
- [ ] Configure proper logging levels
- [ ] Test rate limiting
- [ ] Verify session timeout settings
- [ ] Review error message sanitization

### Regular Security Tasks

- [ ] Rotate AWS credentials regularly
- [ ] Monitor session activity logs
- [ ] Review and update dependencies
- [ ] Check for security vulnerabilities
- [ ] Audit CORS configuration
- [ ] Monitor rate limiting effectiveness

## Incident Response

### Security Incident Checklist

1. **Immediate Response**
   - Identify and isolate affected systems
   - Preserve logs and evidence
   - Notify stakeholders

2. **Investigation**
   - Analyze logs for suspicious activity
   - Determine scope of incident
   - Identify root cause

3. **Recovery**
   - Rotate compromised credentials
   - Apply security patches
   - Update configurations

4. **Post-Incident**
   - Document lessons learned
   - Update security procedures
   - Implement additional controls

## Security Contacts

For security issues or questions:
- Create a private GitHub issue
- Email: security@yourdomain.com
- Follow responsible disclosure practices

## Compliance

This application handles financial data for educational purposes:
- No real financial transactions
- Educational disclaimers required
- User data minimization
- Session-based temporary storage only

## Security Tools

### Recommended Security Scanning

```bash
# Python security scanning
pip install safety bandit
safety check
bandit -r backend/

# Dependency vulnerability scanning
pip install pip-audit
pip-audit

# Docker security scanning
docker scan your-image:tag
```

### Code Quality

```bash
# Type checking
mypy backend/

# Linting
black backend/
isort backend/
flake8 backend/
```

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [AWS Security Best Practices](https://aws.amazon.com/architecture/security-identity-compliance/)
- [Python Security Guidelines](https://python.org/dev/security/)