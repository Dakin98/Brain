# AGENTS.md - Your Workspace

## Every Session

1. Read `SOUL.md` — this is who you are
2. Read `USER.md` — this is who you're helping
3. Read `skills-install-queue.md` — what needs to be installed
4. Check `installation-log.md` — what's already done
5. Continue installation from last position

## Installation Process

```
1. Read queue
2. Check if already installed
3. Set delay (start with 30s)
4. Attempt installation
5. Log result
6. If success: mark as done
7. If rate limit: increase delay, retry
8. If error: log and continue
9. Repeat until queue empty
```

## Delay Strategy

- First attempt: 30 seconds
- After rate limit: 60 seconds
- Second rate limit: 120 seconds
- Third rate limit: 240 seconds
- Max delay: 300 seconds (5 minutes)

## Logging

Every attempt must be logged with:
- Timestamp
- Skill name
- Status (success/rate_limit/error)
- Delay used
- Error message (if any)

## Files

- `skills-install-queue.md` — Source of truth (read-only)
- `installation-log.md` — Progress tracking (write)
- `installation-status.json` — Machine-readable state (write)