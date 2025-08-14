# Runbook

## Start
```
docker compose -f docker-compose.prod.yml up -d --build
```

## Logs
Logs are JSON on stdout. Use `docker logs`.

## Metrics
Prometheus scrapes `api:8000/metrics`.

## Backups
Run `scripts/backup.sh` nightly. Restore with `scripts/restore.sh <timestamp>`.
