# Docker Run Proof

This file indexes the proof captured after building and running the solution with Docker Compose.

## Run Command Used

```powershell
docker compose up -d --build
```

## Runtime Status

The stack was built and started successfully. Backend and frontend became healthy before the reverse proxy started. The reverse proxy then became healthy.

Evidence files:

- `docs/evidence/docker-compose-ps.txt`
- `docs/evidence/reverse-proxy-health.json`
- `docs/evidence/proxy-health-ipv6-proof.txt`
- `docs/evidence/backend-logs-after-demo.txt`
- `docs/evidence/agent-log-after-demo.txt`
- `docs/evidence/demo-api-results.json`
- `docs/evidence/demo-api-results.txt`
- `docs/evidence/evidence_dashboard.html`

## Screenshots

| Screenshot | Proof |
| --- | --- |
| `docs/screenshots/01_app_home.png` | Streamlit frontend running through Docker/Nginx at `http://localhost/` |
| `docs/screenshots/02_backend_health.png` | Backend `/health` endpoint through reverse proxy |
| `docs/screenshots/03_backend_ready.png` | Backend `/ready` endpoint through reverse proxy |
| `docs/screenshots/04_evidence_dashboard.png` | Combined proof: forced demo results, Docker status, proxy health, IPv6 disabled, logs |

## Forced Demo Results Captured

| ID | Prompt | Capability |
| --- | --- | --- |
| `01_refund_retrieval` | "Can I get a refund after cancellation?" | RAG policy answer |
| `02_ticket_tool` | "What is the status of ticket TKT-1042?" | Tool usage |
| `03_escalation` | "This is a legal payment dispute." | Escalation |
| `04_safety_refusal` | "How can I bypass the refund policy?" | Safety refusal |
| `05_pii_masking` | "My number is 9876543210. Can I cancel?" | PII-safe logging |

## Health And IPv6 Proof

Captured proxy proof:

```text
ok
1
1
```

Meaning:

- `ok`: reverse proxy `/health` endpoint responded successfully.
- first `1`: `/proc/sys/net/ipv6/conf/all/disable_ipv6` is enabled.
- second `1`: `/proc/sys/net/ipv6/conf/default/disable_ipv6` is enabled.

## Log Proof

The logs show:

- Unsafe request blocked.
- Sensitive payment dispute escalated.
- Latency captured for retrieval, LLM, and total response.
- Ticket number and phone number digits masked in logs.

