"""
Tests for list_my_tickets tool.
"""
import pytest
from create_ticket import create_ticket
from list_my_tickets import list_my_tickets


def test_list_my_tickets_returns_all_user_tickets():
    """Test that list_my_tickets returns all tickets for a user."""
    user_email = "bob@company.com"
    
    # Create multiple tickets for the same user
    ticket1 = create_ticket(
        user_email=user_email,
        issue_summary="First issue",
        category="Hardware",
        priority="HIGH"
    )
    
    ticket2 = create_ticket(
        user_email=user_email,
        issue_summary="Second issue",
        category="Software",
        priority="MEDIUM"
    )
    
    ticket3 = create_ticket(
        user_email=user_email,
        issue_summary="Third issue",
        category="Network",
        priority="LOW"
    )
    
    # List tickets
    result = list_my_tickets(user_email)
    
    assert result["count"] >= 3
    assert len(result["tickets"]) >= 3
    
    # Check that our tickets are in the list
    ticket_ids = [t["ticket_id"] for t in result["tickets"]]
    assert ticket1["ticket_id"] in ticket_ids
    assert ticket2["ticket_id"] in ticket_ids
    assert ticket3["ticket_id"] in ticket_ids


def test_list_my_tickets_sorted_by_created_at():
    """Test that tickets are sorted by created_at descending (newest first)."""
    user_email = "charlie@company.com"
    
    # Create tickets
    ticket1 = create_ticket(
        user_email=user_email,
        issue_summary="Older issue",
        category="Hardware",
        priority="MEDIUM"
    )
    
    ticket2 = create_ticket(
        user_email=user_email,
        issue_summary="Newer issue",
        category="Software",
        priority="HIGH"
    )
    
    result = list_my_tickets(user_email)
    
    # Find our tickets in the result
    our_tickets = [t for t in result["tickets"] if t["ticket_id"] in [ticket1["ticket_id"], ticket2["ticket_id"]]]
    
    # Newer ticket should come first
    assert len(our_tickets) >= 2
    # The first ticket in our_tickets should be ticket2 (newer)
    assert our_tickets[0]["ticket_id"] == ticket2["ticket_id"]


def test_list_my_tickets_empty_for_new_user():
    """Test that new user with no tickets gets empty list."""
    result = list_my_tickets("newuser@company.com")
    
    assert result["count"] == 0
    assert result["tickets"] == []


def test_list_my_tickets_case_insensitive_email():
    """Test that email matching is case-insensitive."""
    user_email = "TestUser@Company.COM"
    
    # Create ticket with mixed case email
    ticket = create_ticket(
        user_email=user_email,
        issue_summary="Test issue",
        category="Access",
        priority="MEDIUM"
    )
    
    # Query with different case
    result = list_my_tickets("testuser@company.com")
    
    ticket_ids = [t["ticket_id"] for t in result["tickets"]]
    assert ticket["ticket_id"] in ticket_ids


def test_list_my_tickets_empty_email():
    """Test that empty email returns error message."""
    result = list_my_tickets("")
    
    assert result["count"] == 0
    assert "message" in result


def test_list_my_tickets_includes_all_fields():
    """Test that each ticket includes all expected fields."""
    user_email = "diana@company.com"
    
    create_ticket(
        user_email=user_email,
        issue_summary="Test for fields",
        category="Hardware",
        priority="HIGH"
    )
    
    result = list_my_tickets(user_email)
    
    assert result["count"] > 0
    
    ticket = result["tickets"][0]
    required_fields = [
        "ticket_id", "status", "category", "priority",
        "issue_summary", "eta", "assigned_queue",
        "created_at", "last_update"
    ]
    
    for field in required_fields:
        assert field in ticket, f"Missing field: {field}"

# Made with Bob
