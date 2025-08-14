# PAA-P1

Ce projet fournit une application d'exemple avec une API FastAPI et une interface React.

## Démarrer

```bash
docker compose up --build
```

## Backend

```bash
cd apps/api
pytest
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

## Structure

```
repo/
  apps/
    api/
    web/
  docker-compose.yml
```
