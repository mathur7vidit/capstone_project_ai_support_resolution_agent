# Problem Framing Document

## Project Context

The selected industry scenario is Customer Support. The company wants an AI agent that helps users resolve support questions in a realistic workflow while behaving safely in production. The project uses the required Track A framework: LangChain.

The agent is named AI Support Resolution Agent. It supports refund, cancellation, escalation, and ticket-status workflows by combining policy retrieval, LLM reasoning, tool usage, safety rules, logging, and a production-style Docker deployment.

## Primary User Persona

| Field | Description |
| --- | --- |
| Persona | Customer support representative or customer using a self-service support portal |
| Main goal | Get accurate answers to support questions quickly |
| Workflow | Ask a support question, receive a policy-grounded answer, check ticket status if needed, escalate sensitive or unresolved cases |
| Pain points | Slow policy lookup, inconsistent answers, hallucinated policy details, missed escalation cases, privacy risks in logs |
| Success need | The agent must be useful, safe, explainable, and production-ready enough for real workflow evaluation |

## Exact Problem To Solve

Customer support users need fast and reliable help with policy questions and support status checks. A generic chatbot is risky because it may invent policy, mishandle sensitive cases, or expose private user information in logs.

This project solves that by building an AI support agent that:

- Uses approved policy documents as the source of truth.
- Refuses unsafe or policy-violating requests.
- Escalates legal, fraud, payment dispute, and unresolved cases.
- Uses tools for structured support actions.
- Captures latency and error logs for engineering review.
- Runs through Docker Compose behind an Nginx reverse proxy.

## Inputs, Outputs, Constraints, Assumptions

| Category | Details |
| --- | --- |
| Inputs | Natural-language support questions submitted through Streamlit or FastAPI |
| Outputs | JSON response with `response` and `latency`; frontend displays the answer and latency |
| Source documents | `data/refund_policy.txt`, `data/cancellation_policy.txt`, `data/escalation_policy.txt` |
| Constraints | Must not fabricate policies; must refuse unsafe requests; must escalate sensitive cases; must not store personal data in logs |
| Assumptions | Policy files are authoritative; `.env` contains valid API credentials; the LLM endpoint is reachable; unresolved cases should go to a human |

## Example User Questions

| Type | Example Question | Expected Behaviour |
| --- | --- | --- |
| Refund | "Can I get a refund after cancellation?" | Retrieve refund/cancellation policy and answer only from context |
| Cancellation | "How do I cancel my subscription?" | Retrieve cancellation policy |
| Ticket status | "What is the status of ticket TKT-1042?" | Use `ticket_status` tool |
| Sensitive case | "This is a legal payment dispute." | Escalate to human support |
| Unsafe request | "How can I bypass the refund policy?" | Refuse unsafe or policy-violating request |

## Success Criteria

| Success Criterion | Measurement |
| --- | --- |
| Grounded answers | Policy answers match retrieved context and do not invent missing policy |
| Safety enforcement | Unsafe requests are refused |
| Escalation | Sensitive cases trigger escalation |
| Tool usage | Ticket and escalation tools are selected appropriately |
| Privacy | Logs mask personal data before storage |
| Reliability | Backend, frontend, and reverse proxy health checks pass |
| Graceful failures | API/timeout failures show user-friendly messages |

## Known Failure Cases And Edge Scenarios

| Failure Case | Risk | Handling Strategy |
| --- | --- | --- |
| Missing policy information | Hallucinated policy answer | Prompt says to state information is missing |
| Unsafe request | Harmful or policy-violating guidance | `is_unsafe()` blocks before retrieval/LLM |
| Legal/fraud/payment dispute | Agent gives advice it should not give | `requires_escalation()` routes to `escalate_case` |
| LLM or embedding API outage | Request crashes | Backend catches exceptions and returns generic retry message |
| Backend unavailable | Frontend error leaks internals | Streamlit catches connection errors and shows friendly message |
| PII in query | Personal data stored in logs | `mask_pii()` masks digits before logging/feedback storage |

## Scope Boundary

In scope:

- Customer support workflow.
- Retrieval over policy text files.
- Two tools: ticket status and case escalation.
- Local production-style deployment with Docker Compose and Nginx.

Out of scope for this submission:

- Real CRM/ticketing integration.
- Cloud TLS setup.
- Enterprise identity and access management.
- Centralized observability stack.

