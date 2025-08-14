# PAA-P5

Ce projet étend PAA-P1 à PAA-P4 avec un tableau de bord analytique.

## Démarrer

```bash
docker compose up --build
```

## Backend

```bash
cd apps/api
pytest -q
ruff check .
black --check .
```

## Frontend

```bash
cd apps/web
npm install
npm run lint
npm run test
npm run dev
```

## API Principale

- `POST /projects` (admin, editor)
- `GET /projects`
- `GET /projects/{id}`
- `PUT /projects/{id}` (admin ou propriétaire/editor)
- `DELETE /projects/{id}` (admin ou propriétaire si autorisé)
- `PATCH /users/{id}/role` (admin)
- `POST /files/upload`
- `GET /files`
- `GET /files/{id}/download`
- `DELETE /files/{id}`
- `GET /notifications`
- `PATCH /notifications/{id}/read`
- `PATCH /notifications/read-all`
- WebSocket `ws://.../notifications/ws` (token en query)
- `GET /analytics/summary`
- `GET /analytics/projects-per-day`
- `GET /analytics/top-users` (admin)

Variables d'environnement clés dans `apps/api/.env.example` : `ALLOW_OWNER_DELETE`, `PROJECTS_PAGE_SIZE_DEFAULT`, `PROJECTS_PAGE_SIZE_MAX`, `MAX_FILE_SIZE_MB`, `ALLOWED_FILE_TYPES`, `EMAIL_NOTIFICATIONS_ENABLED`, `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `ANALYTICS_CACHE_TTL_SECONDS`.

## Structure

```
repo/
  apps/
    api/
    web/
  docker-compose.yml
```
