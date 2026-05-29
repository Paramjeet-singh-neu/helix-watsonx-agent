"""
Tests for create_ticket tool.
"""
import pytest
from create_ticket import create_ticket, TICKET_STORAGE


def test_create_ticket_returns_valid_format():
    """Test that create_ticket returns valid TKT-XXXX format."""
    result = create_ticket(
        user_email="test@company.com",
        issue_summary="Test issue",
        category="Hardware",
        priority="MEDIUM"
    )
    
    assert "ticket_id" in result
    assert result["ticket_id"].startswith("TKT-")
    assert result["status"] == "Open"
    assert result["category"] == "Hardware"
    assert result["priority"] == "MEDIUM"
    assert "eta" in result
    assert "assigned_queue" in result
    assert "created_at" in result


def test_create_ticket_stores_in_memory():
    """Test that created ticket is stored in TICKET_STORAGE."""
    result = create_ticket(
        user_email="alice@company.com",
        issue_summary="Laptop won't turn on",
        category="Hardware",
        priority="HIGH"
    )
    
    ticket_id = result["ticket_id"]
    assert ticket_id in TICKET_STORAGE
    assert TICKET_STORAGE[ticket_id]["user_email"] == "alice@company.com"
    assert TICKET_STORAGE[ticket_id]["issue_summary"] == "Laptop won't turn on"


def test_high_priority_eta():
    """Test that HIGH priority tickets have 4 hour ETA."""
    result = create_ticket(
        user_email="urgent@company.com",
        issue_summary="Production system down",
        category="Network",
        priority="HIGH"
    )
    
    assert result["priority"] == "HIGH"
    assert result["eta"] == "4 hours"


def test_medium_priority_eta():
    """Test that MEDIUM priority tickets have 1 business day ETA."""
    result = create_ticket(
        user_email="user@company.com",
        issue_summary="Printer issue",
        category="Hardware",
        priority="MEDIUM"
    )
    
    assert result["priority"] == "MEDIUM"
    assert result["eta"] == "1 business day"


def test_low_priority_eta():
    """Test that LOW priority tickets have 3 business days ETA."""
    result = create_ticket(
        user_email="user@company.com",
        issue_summary="Minor software request",
        category="Software",
        priority="LOW"
    )
    
    assert result["priority"] == "LOW"
    assert result["eta"] == "3 business days"


def test_invalid_category_defaults_to_other():
    """Test that invalid category defaults to Other."""
    result = create_ticket(
        user_email="user@company.com",
        issue_summary="Test issue",
        category="InvalidCategory",
        priority="MEDIUM"
    )
    
    assert result["category"] == "Other"


def test_invalid_priority_defaults_to_medium():
    """Test that invalid priority defaults to MEDIUM."""
    result = create_ticket(
        user_email="user@company.com",
        issue_summary="Test issue",
        category="Software",
        priority="INVALID"
    )
    
    assert result["priority"] == "MEDIUM"


def test_assigned_queue_matches_category():
    """Test that assigned queue is based on category."""
    result = create_ticket(
        user_email="user@company.com",
        issue_summary="Network issue",
        category="Network",
        priority="MEDIUM"
    )
    
    assert result["assigned_queue"] == "Network Support Team"


def test_multiple_tickets_have_unique_ids():
    """Test that multiple tickets get unique IDs."""
    result1 = create_ticket(
        user_email="user1@company.com",
        issue_summary="Issue 1",
        category="Hardware",
        priority="MEDIUM"
    )
    
    result2 = create_ticket(
        user_email="user2@company.com",
        issue_summary="Issue 2",
        category="Software",
        priority="LOW"
    )
    
    assert result1["ticket_id"] != result2["ticket_id"]

# Made with Bob
