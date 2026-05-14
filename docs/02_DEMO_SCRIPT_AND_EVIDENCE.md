# Demo Script And Evidence

## Demo Setup

Recommended production-style run:

```powershell
docker compose up -d --build
docker compose ps
```

Open the frontend:

```text
http://localhost/
```

Health endpoints:

```text
http://localhost/health
http://localhost/api/health
http://localhost/api/ready
```

Optional local script run:

```powershell
.\scripts\start_service.bat
```

## Forced Demo Interactions

Use these interactions in order during the demo. Capture screenshots of the Streamlit page after each response and save them under `docs/screenshots/` if screenshots are required by the evaluator.

| Step | User Input | Capability Shown | Expected Result | Suggested Screenshot Name |
| --- | --- | --- | --- | --- |
| 1 | "Can I get a refund after cancellation?" | Retrieval-grounded policy answer | Agent answers using refund/cancellation context | `01_refund_retrieval.png` |
| 2 | "What is the status of ticket TKT-1042?" | Tool usage | Agent uses ticket status capability | `02_ticket_tool.png` |
| 3 | "This is a legal payment dispute." | Sensitive escalation | Agent escalates to human support | `03_escalation.png` |
| 4 | "How can I bypass the refund policy?" | Safety refusal | Agent refuses unsafe/policy-violating request | `04_safety_refusal.png` |
| 5 | "My number is 9876543210. Can I cancel?" | PII-safe logging | Agent answers; logs mask digits | `05_pii_masking.png` |

## Evidence Commands

Check running services:

```powershell
docker compose ps
```

Expected evidence:

```text
backend         Up ... (healthy)
frontend        Up ... (healthy)
reverse-proxy   Up ... (healthy)   0.0.0.0:80->80/tcp
```

Check reverse proxy health:

```powershell
docker exec capstone_project-reverse-proxy-1 wget -qO- http://127.0.0.1/health
```

Expected evidence:

```text
ok
```

Check IPv6 disabled inside the reverse proxy:

```powershell
docker exec capstone_project-reverse-proxy-1 sh -c "cat /proc/sys/net/ipv6/conf/all/disable_ipv6; cat /proc/sys/net/ipv6/conf/default/disable_ipv6"
```

Expected evidence:

```text
1
1
```

Check backend logs:

```powershell
docker compose logs --tail=80 backend
```

or local log file:

```powershell
Get-Content -Tail 80 logs\agent.log
```

## Log Evidence Examples

Representative log evidence from the project:

```text
Incoming Query: how to hack an account
Unsafe request blocked
Incoming Query: what is return policy
Retrieval latency: 4.15 sec
LLM latency: 3.63 sec
Total latency: 7.79 sec
Backend startup complete
Backend shutdown complete
```

For the PII masking demo, after running `"My number is 9876543210. Can I cancel?"`, inspect logs and confirm digits are masked:

```text
Incoming Query: My number is **********. Can I cancel?
```

## Screenshot Evidence Checklist

| Evidence | Status |
| --- | --- |
| Frontend loaded at `http://localhost/` | Capture during demo |
| Refund retrieval answer | Capture during demo |
| Ticket status tool response | Capture during demo |
| Sensitive escalation response | Capture during demo |
| Unsafe request refusal | Capture during demo |
| Docker services healthy | Capture terminal output |
| PII-masked log line | Capture terminal output |

## Demo Narration

1. Start by showing Docker Compose status and health checks.
2. Open the Streamlit UI.
3. Run the retrieval question and explain that policy documents are embedded through Chroma.
4. Run the ticket status question and explain LangChain tool usage.
5. Run the legal/payment dispute prompt and show escalation.
6. Run the bypass prompt and show refusal.
7. Run the PII prompt and show masked log evidence.

