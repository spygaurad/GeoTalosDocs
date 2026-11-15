# Local setup and deployment

GeoTALOS runs as a Docker Compose stack (backend) plus a Next.js app (frontend).

## Requirements

- Docker with Docker Compose
- Node.js and npm, for the frontend
- A [Clerk](https://clerk.com) application for sign-in (free tier is enough for development)
- Optional: an NVIDIA GPU with the NVIDIA Container Toolkit, for `geoops-service` (model training). Without one, it falls back to CPU.

## 1. Start the backend

```bash
git clone https://github.com/spygaurad/GeoTalosProd.git
cd GeoTalosProd
cp .env.docker .env
```

Edit `.env` and fill in at least:

| Variable | Where it comes from |
|---|---|
| `CLERK_SECRET_KEY` | Clerk Dashboard → API Keys |
| `CLERK_FRONTEND_API` | Clerk Dashboard, for example `happy-fox-42.clerk.accounts.dev` |
| `CLERK_WEBHOOK_SECRET` | Clerk Dashboard → Webhooks → signing secret |
| `GEOOPS_SERVICE_API_TOKEN` | Any random string. Compose refuses to start without it. |
| `BACKEND_CORS_ORIGINS`, `MINIO_CORS_ALLOW_ORIGIN` | The frontend origin, for example `http://localhost:3000` |

Then start everything:

```bash
docker compose up --build
```

Database migrations run automatically before the API, workers and Martin start (the `app-db-migrate` and `stac-db-migrate` services).

## 2. Start the frontend

```bash
git clone https://github.com/spygaurad/GeoTalosUI.git
cd GeoTalosUI
cp .env.example .env.local
npm install
npm run dev
```

In `.env.local`, set:

| Variable | Value |
|---|---|
| `NEXT_PUBLIC_API_URL` | The API, `http://localhost:8000` by default |
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | Clerk Dashboard → API Keys |
| `CLERK_SECRET_KEY` | Clerk Dashboard → API Keys (same as the backend) |

The two Clerk keys are not in `.env.example`, so add them yourself. The app runs on <http://localhost:3000>.

## Services and ports

| Service | Default port | Purpose |
|---|---|---|
| `api` | 8000 | FastAPI application (interactive docs at `/docs`) |
| `app-db` | 5432 | PostgreSQL + PostGIS application database |
| `stac-db` | 5433 | pgSTAC imagery catalog |
| `stac-api` | 8081 | STAC API |
| `titiler` | 8082 | Raster tiles from COGs |
| `redis` | 6379 | Celery broker |
| `redis-tiles` | internal | Vector tile cache, kept separate so tiles cannot evict Celery data |
| `minio` | 9000 / 9001 | Object storage API / web console |
| `martin` | internal | Vector tiles from PostGIS and PMTiles. Not exposed on the host; reached only through the API. |
| `flower` | 5555 | Celery monitoring |
| `geoops-service` | 8020 | Model training and serving (GPU) |

Every port can be changed in `.env` (for example `API_PORT`, `APP_DB_PORT`).

## Reference layers

Public reference layers (Ramsar sites, protected areas, concessions, rivers) are not in the repository because the files are large. Build or download them with the scripts in `scripts/reference_layers/`; the README there has the steps. See [Tiles, caching and reference layers](tiles.md).

!!! note "Existing databases"
    If you upgrade an existing database rather than starting fresh, run `GRANT CREATE ON DATABASE geoplat TO app_user;` once before migrating. New databases get this from the init script.
