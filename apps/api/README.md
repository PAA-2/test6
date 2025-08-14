# API

API FastAPI avec authentification JWT.

## Commandes

```bash
pytest
ruff check .
black --check .
```

## Endpoints fichiers

- `POST /files/upload`
- `GET /files`
- `GET /files/{id}/download`
- `DELETE /files/{id}`

## Endpoints notifications

- `GET /notifications`
- `PATCH /notifications/{id}/read`
- `PATCH /notifications/read-all`
- WebSocket `/notifications/ws?token=...`

## Endpoints analytics

- `GET /analytics/summary`
- `GET /analytics/projects-per-day?days=30`
- `GET /analytics/top-users` (admin)

## Endpoints tâches

- `POST /tasks/analytics/rebuild` (admin)
- `POST /tasks/files/{id}/thumbnail`
- `GET /tasks/{id}/status`
- `GET /tasks` (admin)
