"""
List all tickets for a user.
"""
from typing import List, Optional
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from create_ticket import TICKET_STORAGE


class TicketSummary(BaseModel):
    """Summary of a single ticket."""
    ticket_id: str = Field(..., description="The ticket ID")
    status: str = Field(..., description="Current ticket status")
    category: str = Field(..., description="Issue category")
    priority: str = Field(..., description="Ticket priority")
    issue_summary: str = Field(..., description="Description of the issue")
    eta: str = Field(..., description="Estimated time to resolution")
    assigned_queue: str = Field(..., description="Queue the ticket is assigned to")
    created_at: str = Field(..., description="When ticket was created")
    last_update: str = Field(..., description="Latest update message")


class TicketListResponse(BaseModel):
    """List of tickets for a user."""
    count: int = Field(..., description="Number of tickets found")
    tickets: List[TicketSummary] = Field(default_factory=list, description="List of tickets")
    message: Optional[str] = Field(None, description="Error or info message")


@tool()
def list_my_tickets(user_email: str) -> TicketListResponse:
    """
    List all support tickets for a given user.
    
    Args:
        user_email: Email address of the user
        
    Returns:
        List of tickets sorted by created date (newest first)
    """
    if not user_email:
        return TicketListResponse(
            count=0,
            tickets=[],
            message="Please provide a user email address"
        )
    
    # Find all tickets for this user
    user_tickets = []
    for ticket_id, ticket in TICKET_STORAGE.items():
        if ticket["user_email"].lower() == user_email.lower():
            user_tickets.append(TicketSummary(
                ticket_id=ticket["ticket_id"],
                status=ticket["status"],
                category=ticket["category"],
                priority=ticket["priority"],
                issue_summary=ticket["issue_summary"],
                eta=ticket["eta"],
                assigned_queue=ticket["assigned_queue"],
                created_at=ticket["created_at"],
                last_update=ticket["last_update"]
            ))
    
    # Sort by created_at descending (newest first)
    user_tickets.sort(key=lambda x: x.created_at, reverse=True)
    
    return TicketListResponse(
        count=len(user_tickets),
        tickets=user_tickets
    )

# Made with Bob
