# AI Support Resolution Agent

Production-ready setup for a FastAPI backend and Streamlit frontend. The recommended run path uses separate Docker images, Docker Compose, and an Nginx reverse proxy. An optional local Windows run path is also available through scripts.

## Architecture

- `backend`: FastAPI service running the support agent on port `8000`.
- `frontend`: Streamlit UI running on port `8501`.
- `reverse-proxy`: Nginx entrypoint exposed on host IPv4 port `80`.
- `/`: routed to the Streamlit frontend.
- `/api/*`: routed to the FastAPI backend after stripping `/api`.
- `/health`: reverse proxy health endpoint.

## Prerequisites

### Docker Mode

- Docker Desktop installed and running.
- Docker Compose v2 available through `docker compose`.
- A `.env` file in the project root with API credentials:

```env
OPENAI_API_KEY=your_key_here
OPENAI_API_BASE=https://your-openai-compatible-endpoint/v1
```

Do not commit real secrets to source control.

### Local Script Mode

- Python installed locally.
- A virtual environment named `venv` in the project root.
- Dependencies installed from `requirements.txt`.
- A `.env` file in the project root with the same API credentials shown above.

Create and prepare the local virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Option 1: Run With Docker Compose

From the project root:

```powershell
docker compose build
```

This builds two application images:

- Backend image from `app/Dockerfile` using `app/requirements.txt`
- Frontend image from `ui/Dockerfile` using `ui/requirements.txt`

Nginx uses the official `nginx:1.27-alpine` image.

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

Stop Docker services:

```powershell
docker compose down
```

Rebuild after code changes:

```powershell
docker compose up -d --build
```

## Option 2: Run Locally With Windows Scripts

Use this mode when Docker is not required and you want to run the backend and frontend directly on Windows.

Start both services:

```powershell
.\scripts\start_service.bat
```

This script:

- Activates `venv`
- Starts FastAPI with Uvicorn
- Starts the Streamlit frontend

Open the app:

```text
http://localhost:8501/
```

Backend health check:

```text
http://localhost:8000/health
```

Stop both local services:

```powershell
.\scripts\stop_service.bat
```

Local script mode is useful for development, but Docker Compose is recommended for production-style evaluation because it includes separated services, reverse proxy routing, container health checks, and restart policies.

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
- `scripts/start_service.bat`: optional local Windows startup script.
- `scripts/stop_service.bat`: optional local Windows stop script.
- `CAPSTONE_PHASE_DELIVERABLES.md`: single consolidated phase-by-phase capstone document.
- `docs/01_PROBLEM_FRAMING.md`: 1-2 page problem framing document.
- `docs/02_DEMO_SCRIPT_AND_EVIDENCE.md`: forced demo script and evidence checklist.
- `docs/03_PROMPT_COMPARISON.md`: prompt comparison table using the same test set.
- `docs/04_EVALUATION_REPORT.md`: evaluation report with debugged failure cases.
- `docs/05_ENGINEERING_PRODUCT_JUSTIFICATION.md`: engineering and product justification.
- `docs/DOCKER_RUN_PROOF.md`: index of Docker run evidence and screenshots.
- `docs/screenshots/`: captured proof screenshots.
- `docs/evidence/`: captured proof logs, API results, and health output.
- `.dockerignore`: excludes local virtualenvs, logs, caches, and secrets from build context.
- `.env`: runtime API credentials loaded into the backend container.
