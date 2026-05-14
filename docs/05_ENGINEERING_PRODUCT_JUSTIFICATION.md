# Engineering And Product Justification

## Product Rationale

The AI Support Resolution Agent is designed for customer support workflows where accuracy, safety, escalation, and operational reliability matter more than open-ended conversation. Users need help with refund, cancellation, ticket status, and sensitive support issues. The agent is valuable because it reduces manual policy lookup while preserving human escalation for risky cases.

## Key Design Decisions

| Decision | Justification | Tradeoff |
| --- | --- | --- |
| Use LangChain | Required by Track A and supports LLM calls, tools, messages, and retrieval patterns | Adds framework dependency |
| Use FastAPI backend | Clean API boundary for `/chat`, `/health`, and `/ready` | Requires separate frontend/backend orchestration |
| Use Streamlit frontend | Fast demo UI for support workflow | Less customizable than a full web app |
| Use Chroma for retrieval | Lightweight local vector store suitable for capstone RAG | Not a managed production vector database |
| Use Nginx reverse proxy | Provides one entrypoint and routes `/` to frontend, `/api/*` to backend | Additional service to configure and health-check |
| Use Docker Compose | Reproducible local production-like environment | Not a replacement for Kubernetes/cloud deployment |
| Use code-level safety checks before LLM | Blocks unsafe/sensitive cases before expensive reasoning | Keyword logic can be too simple |
| Mask PII in logs | Directly supports safety requirement | Current implementation masks digits, not every PII type |

## Architecture

```text
User
  |
  v
Nginx reverse proxy :80
  |------------------------|
  v                        v
Streamlit frontend :8501   FastAPI backend :8000
                           |
                           v
                 LangChain agent workflow
                           |
        |------------------|------------------|
        v                  v                  v
   Safety checks        Chroma RAG        Tools
   refusal/escalation   policy context    ticket/escalate
```

## Safety Approach

Safety is handled as a first-class product requirement, not an afterthought.

| Safety Need | Implementation |
| --- | --- |
| Unsafe request refusal | `is_unsafe()` checks for unsafe/policy-violating keywords |
| Sensitive escalation | `requires_escalation()` checks legal, fraud, payment dispute cases |
| No policy fabrication | System prompt requires retrieved context only |
| PII-safe logging | `mask_pii()` masks digits before logging and feedback storage |
| Graceful failure | Generic user-facing errors, detailed internal logs |

## Deployment Assumptions

| Area | Assumption |
| --- | --- |
| Runtime | Docker Desktop or Docker-compatible environment is available |
| Secrets | `.env` is provided locally and not committed |
| Network | Local HTTP is acceptable for capstone demo |
| Model endpoint | OpenAI-compatible API endpoint is reachable |
| Data | Policy text files in `data/` are approved source of truth |
| Persistence | `logs/` and `chroma_db/` can be mounted locally |

## Production Readiness Decisions

| Requirement | Implementation |
| --- | --- |
| Separate frontend and backend | Separate `ui` and `app` directories and Dockerfiles |
| Docker images | `app/Dockerfile`, `ui/Dockerfile` |
| Compose orchestration | `docker-compose.yml` |
| Reverse proxy | `nginx/nginx.conf` |
| Health checks | Backend, frontend, and reverse-proxy health checks |
| Graceful shutdown | `stop_grace_period` and Uvicorn graceful timeout |
| Restart behaviour | `restart: unless-stopped` |
| IPv4-only runtime | IPv6 disabled through `sysctls`; proxy uses `0.0.0.0` and `127.0.0.1` health check |

## Why This Design Is Practical

The design is intentionally simple but production-aware. It does not overbuild infrastructure, but it shows the important industry behaviours:

- Clear service boundaries.
- Reproducible deployment.
- Health checks.
- Latency/error logging.
- Guardrails before LLM reasoning.
- Retrieval grounding.
- Human escalation path.
- Documented failure analysis and fixes.

## Product Tradeoffs

| Tradeoff | Reasonable For Capstone? | Future Improvement |
| --- | --- | --- |
| Keyword safety instead of full classifier | Yes, transparent and testable | Add LLM-based or policy classifier |
| Local Chroma instead of managed vector DB | Yes, reproducible locally | Move to managed vector store for scale |
| Streamlit instead of production React frontend | Yes, fast demo and clear UX | Build full frontend for real deployment |
| File logs instead of centralized tracing | Yes, enough for evidence | Add OpenTelemetry or cloud logging |
| Single backend worker | Yes, simpler local deployment | Scale workers after load testing |

## Submission Positioning

This project should be presented as an industry-style prototype moving toward production, not a one-off notebook demo. The strongest evidence is:

- The agent uses LangChain and RAG.
- Safety is enforced before retrieval and generation.
- Sensitive cases escalate.
- Deployment uses Docker, Compose, and reverse proxy.
- A real failure was debugged and fixed.
- Logs and health checks provide operational evidence.

