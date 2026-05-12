from langchain_core.tools import tool


@tool
def ticket_status(ticket_id: str) -> str:
    """
    Get ticket status.
    """

    return f"Ticket {ticket_id} is currently in progress."


@tool
def escalate_case(issue: str) -> str:
    """
    Escalate issue to human support.
    """

    return f"Issue escalated to human support: {issue}"