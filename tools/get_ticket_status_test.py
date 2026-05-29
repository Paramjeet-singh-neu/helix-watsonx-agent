"""
Tests for get_ticket_status tool.
"""
import pytest
from create_ticket import create_ticket
from get_ticket_status import get_ticket_status


def test_get_ticket_status_returns_created_ticket():
    """Test that get_ticket_status returns the created ticket."""
    # First create a ticket
    created = create_ticket(
        user_email="test@company.com",
        issue_summary="Test issue for status check",
        category="Software",
        priority="MEDIUM"
    )
    
    ticket_id = created["ticket_id"]
    
    # Now get its status
    result = get_ticket_status(ticket_id)
    
    assert result["found"] is True
    assert result["ticket_id"] == ticket_id
    assert result["status"] == "Open"
    assert result["category"] == "Software"
    assert result["priority"] == "MEDIUM"
    assert result["issue_summary"] == "Test issue for status check"
    assert result["user_email"] == "test@company.com"
    assert "eta" in result
    assert "assigned_queue" in result
    assert "created_at" in result
    assert "last_update" in result


def test_get_ticket_status_not_found():
    """Test that non-existent ticket returns not found."""
    result = get_ticket_status("TKT-99999")
    
    assert result["found"] is False
    assert "message" in result
    assert "TKT-99999" in result["message"]


def test_get_ticket_status_empty_id():
    """Test that empty ticket ID returns error."""
    result = get_ticket_status("")
    
    assert result["found"] is False
    assert "message" in result


def test_get_ticket_status_includes_all_fields():
    """Test that status includes all expected fields."""
    # Create a ticket
    created = create_ticket(
        user_email="alice@company.com",
        issue_summary="Urgent hardware issue",
        category="Hardware",
        priority="HIGH"
    )
    
    # Get status
    result = get_ticket_status(created["ticket_id"])
    
    required_fields = [
        "found", "ticket_id", "status", "category", "priority",
        "issue_summary", "user_email", "eta", "assigned_queue",
        "created_at", "last_update"
    ]
    
    for field in required_fields:
        assert field in result, f"Missing field: {field}"

# Made with Bob
