# AI Support Resolution Agent

Production-ready setup for a FastAPI backend and Streamlit frontend, packaged as separate Docker images and served through an Nginx reverse proxy.

## Architecture

- `backend`: FastAPI service running the support agent on port `8000`.
- `frontend`: Streamlit UI running on port `8501`.
- `reverse-proxy`: Nginx entrypoint exposed on host IPv4 port `80`.
- `/`: routed to the Streamlit frontend.
- `/api/*`: routed to the FastAPI backend after stripping `/api`.
- `/health`: reverse proxy health endpoint.

## Prerequisites

- Docker Desktop installed and running.
- Docker Compose v2 available through `docker compose`.
- A `.env` file in the project root with API credentials:

```env
OPENAI_API_KEY=your_key_here
OPENAI_API_BASE=https://your-openai-compatible-endpoint/v1
```

Do not commit real secrets to source control.

## Build Docker Images

From the project root:

```powershell
docker compose build
```

This builds two application images:

- Backend image from `app/Dockerfile` using `app/requirements.txt`
- Frontend image from `ui/Dockerfile` using `ui/requirements.txt`

Nginx uses the official `nginx:1.27-alpine` image.

## Run In Production Mode

Start all services:

```powershell
docker compose up -d
```

Open the application:

```text
http://localhost/
```

The backend is available through the reverse proxy:

```text
http://localhost/api/health
http://localhost/api/ready
```

## Check Service Status

View running containers:

```powershell
docker compose ps
```

Check logs:

```powershell
docker compose logs -f
```

Check only the backend logs:

```powershell
docker compose logs -f backend
```

## Health Checks

The production setup includes health checks at three layers:

- Backend container: `GET http://localhost:8000/health`
- Frontend container: `GET http://localhost:8501/_stcore/health`
- Reverse proxy container: `GET http://127.0.0.1/health`

The containers disable IPv6 through Docker `sysctls`. The reverse proxy is intentionally bound to IPv4 with `0.0.0.0:80:80`, listens on `0.0.0.0:80`, and its internal health check uses `127.0.0.1` instead of `localhost` to avoid IPv6 loopback resolution issues.

Docker Compose waits for backend and frontend health before starting the reverse proxy.

## Graceful Failure Handling

- Backend exceptions are logged in `logs/agent.log`.
- API users receive a generic service error instead of internal exception details.
- Frontend requests use a timeout and display user-friendly messages for timeout, connection, and backend errors.
- Containers use `restart: unless-stopped`.
- Backend and frontend define `stop_grace_period` so Docker has time to shut them down cleanly.

## Stop Services

```powershell
docker compose down
```

## Rebuild After Code Changes

```powershell
docker compose up -d --build
```

## Direct Image Build Commands

If you want to build images without Compose:

```powershell
docker build -f app/Dockerfile -t ai-support-backend:latest .
docker build -f ui/Dockerfile -t ai-support-frontend:latest .
```

Running manually is possible, but Compose is recommended because it wires service discovery, environment variables, health checks, persistence, and the reverse proxy together.

## Important Files

- `docker-compose.yml`: production orchestration.
- `app/Dockerfile`: backend image definition.
- `app/requirements.txt`: backend-only Python dependencies.
- `ui/Dockerfile`: frontend image definition.
- `ui/requirements.txt`: frontend-only Python dependencies.
- `nginx/nginx.conf`: reverse proxy routing.
- `.dockerignore`: excludes local virtualenvs, logs, caches, and secrets from build context.
- `.env`: runtime API credentials loaded into the backend container.
