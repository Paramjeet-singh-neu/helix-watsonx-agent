"""
Create IT support tickets.
"""
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.agent_builder.tools import tool

# In-memory ticket storage (persists across calls in same process)
TICKET_STORAGE = {}
TICKET_COUNTER = 1000


class TicketResponse(BaseModel):
    """Ticket creation response."""
    ticket_id: str = Field(..., description="Unique ticket identifier")
    status: str = Field(..., description="Current ticket status")
    category: str = Field(..., description="Issue category")
    priority: str = Field(..., description="Ticket priority")
    eta: str = Field(..., description="Estimated time to resolution")
    assigned_queue: str = Field(..., description="Queue the ticket is assigned to")
    created_at: str = Field(..., description="Timestamp when ticket was created")


@tool()
def create_ticket(user_email: str, issue_summary: str, category: str, priority: str) -> TicketResponse:
    """
    Create a new IT support ticket.
    
    Args:
        user_email: Email address of the user reporting the issue
        issue_summary: Brief description of the issue
        category: Issue category (Network, Hardware, Access, Software, Other)
        priority: Ticket priority (LOW, MEDIUM, HIGH)
        
    Returns:
        Ticket details including ticket ID, status, and ETA
    """
    global TICKET_COUNTER
    
    # Validate category
    valid_categories = ["Network", "Hardware", "Access", "Software", "Other"]
    if category not in valid_categories:
        category = "Other"
    
    # Validate priority
    valid_priorities = ["LOW", "MEDIUM", "HIGH"]
    if priority not in valid_priorities:
        priority = "MEDIUM"
    
    # Generate ticket ID
    TICKET_COUNTER += 1
    ticket_id = f"TKT-{TICKET_COUNTER}"
    
    # Calculate ETA based on priority
    if priority == "HIGH":
        eta = "4 hours"
        eta_datetime = datetime.now() + timedelta(hours=4)
    elif priority == "MEDIUM":
        eta = "1 business day"
        eta_datetime = datetime.now() + timedelta(days=1)
    else:  # LOW
        eta = "3 business days"
        eta_datetime = datetime.now() + timedelta(days=3)
    
    # Determine assigned queue
    assigned_queue = f"{category} Support Team"
    
    # Create ticket
    created_at = datetime.now().isoformat()
    
    ticket = {
        "ticket_id": ticket_id,
        "user_email": user_email,
        "issue_summary": issue_summary,
        "status": "Open",
        "category": category,
        "priority": priority,
        "eta": eta,
        "eta_datetime": eta_datetime.isoformat(),
        "assigned_queue": assigned_queue,
        "created_at": created_at,
        "last_update": f"Ticket created at {created_at}"
    }
    
    # Store ticket
    TICKET_STORAGE[ticket_id] = ticket
    
    # Return ticket details
    return TicketResponse(
        ticket_id=ticket_id,
        status=ticket["status"],
        category=ticket["category"],
        priority=ticket["priority"],
        eta=ticket["eta"],
        assigned_queue=ticket["assigned_queue"],
        created_at=ticket["created_at"]
    )

# Made with Bob
