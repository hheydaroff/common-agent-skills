# Security Checklist

Quick reference for web application security. Treat every external input as hostile, every secret as sacred, and every authorization check as mandatory.

## Pre-Commit Checks

- [ ] No secrets in code (`git diff --cached | grep -i "password\|secret\|api_key\|token"`)
- [ ] `.gitignore` covers: `.env`, `.env.local`, `*.pem`, `*.key`
- [ ] `.env.example` uses placeholder values (not real secrets)

## OWASP Top 10 Prevention

| # | Vulnerability | Prevention |
|---|---|---|
| 1 | Broken Access Control | Auth checks on every endpoint, ownership verification |
| 2 | Cryptographic Failures | HTTPS, strong hashing, no secrets in code |
| 3 | Injection | Parameterized queries, input validation |
| 4 | Insecure Design | Threat modeling, spec-driven development |
| 5 | Security Misconfiguration | Security headers, minimal permissions, audit deps |
| 6 | Vulnerable Components | `npm audit`, keep deps updated, minimal deps |
| 7 | Auth Failures | Strong passwords, rate limiting, session management |
| 8 | Data Integrity Failures | Verify updates/dependencies, signed artifacts |
| 9 | Logging Failures | Log security events, don't log secrets |
| 10 | SSRF | Validate/allowlist URLs, restrict outbound requests |

## Input Validation

- [ ] All user input validated at system boundaries (API routes, form handlers)
- [ ] Validation uses allowlists (not denylists)
- [ ] String lengths constrained (min/max)
- [ ] Numeric ranges validated
- [ ] File uploads: type restricted, size limited, content verified
- [ ] SQL queries parameterized (no string concatenation)
- [ ] HTML output encoded (use framework auto-escaping)
- [ ] URLs validated before redirect (prevent open redirect)

```typescript
// Zod schema at boundary
const CreateTaskSchema = z.object({
  title: z.string().min(1).max(200).trim(),
  description: z.string().max(2000).optional(),
  priority: z.enum(['low', 'medium', 'high']).default('medium'),
});

app.post('/api/tasks', async (req, res) => {
  const result = CreateTaskSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(422).json({
      error: { code: 'VALIDATION_ERROR', details: result.error.flatten() },
    });
  }
  const task = await taskService.create(result.data);
  return res.status(201).json(task);
});
```

## Authentication

- [ ] Passwords hashed with bcrypt (≥12 rounds), scrypt, or argon2
- [ ] Session cookies: `httpOnly`, `secure`, `sameSite: 'lax'`
- [ ] Session expiration configured
- [ ] Rate limiting on login endpoint (≤10 attempts per 15 minutes)
- [ ] Password reset tokens: time-limited (≤1 hour), single-use
- [ ] JWT tokens validated (signature, expiration, issuer)
- [ ] Never store tokens in localStorage (XSS risk)

## Authorization

- [ ] Every protected endpoint checks authentication
- [ ] Every resource access checks ownership/role (prevents IDOR)
- [ ] Admin endpoints require admin role verification
- [ ] API keys scoped to minimum necessary permissions

```typescript
// Always check the authenticated user owns the resource
app.patch('/api/tasks/:id', authenticate, async (req, res) => {
  const task = await taskService.findById(req.params.id);
  if (task.ownerId !== req.user.id) {
    return res.status(403).json({ error: { code: 'FORBIDDEN' } });
  }
  // proceed
});
```

## Security Headers

```typescript
import helmet from 'helmet';
app.use(helmet());

// Content Security Policy
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'"],
    styleSrc: ["'self'", "'unsafe-inline'"],
    imgSrc: ["'self'", 'data:', 'https:'],
    connectSrc: ["'self'"],
  },
}));
```

Required headers:
```
Content-Security-Policy: default-src 'self'; script-src 'self'
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

## CORS Configuration

```typescript
// Restrictive (production)
cors({
  origin: ['https://yourdomain.com'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
})

// NEVER in production:
cors({ origin: '*' })
```

## Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

// General API
app.use('/api/', rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,
}));

// Stricter for auth
app.use('/api/auth/', rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 10,
}));
```

## Triaging npm audit Results

```
npm audit reports a vulnerability
├── Severity: critical or high
│   ├── Reachable in production code path?
│   │   ├── YES → Fix immediately (update, patch, or replace)
│   │   └── NO (dev-only dep, unused path) → Fix soon, not a blocker
│   └── Fix available?
│       ├── YES → Update to patched version
│       └── NO → Check workarounds, consider replacing, add to allowlist with review date
├── Severity: moderate
│   ├── Reachable in production? → Fix in next release cycle
│   └── Dev-only? → Fix when convenient
└── Severity: low
    └── Track and fix during regular dependency updates
```

Key questions:
- Is the vulnerable function actually called in your code path?
- Is the dependency runtime or dev-only?
- Is the vulnerability exploitable given your deployment context?

When deferring a fix, **document the reason and set a review date**.

## Data Protection

- [ ] Sensitive fields excluded from API responses (`passwordHash`, `resetToken`, etc.)
- [ ] Sensitive data not logged (passwords, tokens, full CC numbers)
- [ ] PII encrypted at rest (if required by regulation)
- [ ] HTTPS for all external communication
- [ ] Third-party API responses validated before use (treat as untrusted data)

## File Upload Safety

```typescript
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
const MAX_SIZE = 5 * 1024 * 1024; // 5MB

function validateUpload(file: UploadedFile) {
  if (!ALLOWED_TYPES.includes(file.mimetype)) {
    throw new ValidationError('File type not allowed');
  }
  if (file.size > MAX_SIZE) {
    throw new ValidationError('File too large (max 5MB)');
  }
}
```

## Error Handling (Security Perspective)

```typescript
// Production: generic error, no internals
res.status(500).json({
  error: { code: 'INTERNAL_ERROR', message: 'Something went wrong' }
});

// NEVER in production:
res.status(500).json({
  error: err.message,
  stack: err.stack,      // Exposes internals
  query: err.sql,        // Exposes database details
});
```
