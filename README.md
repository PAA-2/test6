# PAA-P8

Ce projet étend PAA-P1 à PAA-P7 en introduisant des organisations multi-tenant
avec invitations et sélection d'organisation côté utilisateur. Toutes les
données (projets, fichiers, recherche, analytics) sont désormais rattachées à
une organisation.

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
- `POST /tasks/analytics/rebuild` (admin)
- `POST /tasks/files/{id}/thumbnail`
- `GET /tasks/{id}/status`
- `GET /tasks` (admin)
- `GET /search`
- `GET /search/facets`
- `GET /search/suggestions`
- `POST /search/saved`
- `GET /search/saved`
- `DELETE /search/saved/{id}`
- `POST /orgs`
- `GET /orgs`
- `GET /orgs/{id}`
- `GET /orgs/{id}/members`
- `POST /orgs/{id}/invites`
- `GET /invites/{token}`
- `POST /invites/{token}/accept`
- `POST /me/org`

Variables d'environnement clés dans `apps/api/.env.example` : `ALLOW_OWNER_DELETE`, `PROJECTS_PAGE_SIZE_DEFAULT`, `PROJECTS_PAGE_SIZE_MAX`, `MAX_FILE_SIZE_MB`, `ALLOWED_FILE_TYPES`, `EMAIL_NOTIFICATIONS_ENABLED`, `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `ANALYTICS_CACHE_TTL_SECONDS`, `REDIS_URL`, `JOBS_MAX_RETRIES`, `ANALYTICS_REFRESH_CRON`, `NOTIFICATIONS_CLEANUP_CRON`, `THUMBNAIL_MAX_SIZE`, `THUMBNAIL_QUALITY`, `SEARCH_PAGE_SIZE_MAX`, `SEARCH_LANGUAGE`, `INVITE_TOKEN_TTL_HOURS`, `APP_BASE_URL`.

## Structure

```
repo/
  apps/
    api/
    web/
  docker-compose.yml
```
