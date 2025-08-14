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
