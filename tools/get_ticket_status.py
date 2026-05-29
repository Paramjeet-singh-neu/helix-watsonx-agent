"""
Get status of an IT support ticket.
"""
from typing import Optional
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from create_ticket import TICKET_STORAGE


class TicketStatusResponse(BaseModel):
    """Ticket status response."""
    found: bool = Field(..., description="Whether the ticket was found")
    ticket_id: Optional[str] = Field(None, description="The ticket ID")
    status: Optional[str] = Field(None, description="Current ticket status")
    category: Optional[str] = Field(None, description="Issue category")
    priority: Optional[str] = Field(None, description="Ticket priority")
    issue_summary: Optional[str] = Field(None, description="Description of the issue")
    user_email: Optional[str] = Field(None, description="User's email address")
    eta: Optional[str] = Field(None, description="Estimated time to resolution")
    assigned_queue: Optional[str] = Field(None, description="Queue the ticket is assigned to")
    created_at: Optional[str] = Field(None, description="When ticket was created")
    last_update: Optional[str] = Field(None, description="Latest update message")
    message: Optional[str] = Field(None, description="Error message if ticket not found")


@tool()
def get_ticket_status(ticket_id: str) -> TicketStatusResponse:
    """
    Retrieve the status and details of a support ticket.
    
    Args:
        ticket_id: The ticket ID to look up (e.g., "TKT-1001")
        
    Returns:
        Ticket details if found, or error message if not found
    """
    if not ticket_id:
        return TicketStatusResponse(
            found=False,
            message="Please provide a ticket ID"
        )
    
    # Look up ticket in storage
    ticket = TICKET_STORAGE.get(ticket_id)
    
    if not ticket:
        return TicketStatusResponse(
            found=False,
            message=f"Ticket {ticket_id} not found"
        )
    
    # Return full ticket details
    return TicketStatusResponse(
        found=True,
        ticket_id=ticket["ticket_id"],
        status=ticket["status"],
        category=ticket["category"],
        priority=ticket["priority"],
        issue_summary=ticket["issue_summary"],
        user_email=ticket["user_email"],
        eta=ticket["eta"],
        assigned_queue=ticket["assigned_queue"],
        created_at=ticket["created_at"],
        last_update=ticket["last_update"]
    )

# Made with Bob
