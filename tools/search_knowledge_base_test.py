"""
Tests for search_knowledge_base tool.
"""
import pytest
from search_knowledge_base import search_knowledge_base


def test_vpn_query_returns_expected_article():
    """Test that VPN query returns the VPN knowledge base article."""
    result = search_knowledge_base("How do I connect to VPN?")
    
    assert result["found"] is True
    assert result["article_id"] == "KB001"
    assert "VPN" in result["title"]
    assert result["category"] == "Network"
    assert len(result["solution_steps"]) > 0
    assert result["confidence"] > 0


def test_password_reset_query():
    """Test password reset query."""
    result = search_knowledge_base("I forgot my password")
    
    assert result["found"] is True
    assert result["article_id"] == "KB002"
    assert "Password" in result["title"]
    assert result["category"] == "Access"


def test_printer_issue_query():
    """Test printer issue query."""
    result = search_knowledge_base("printer not working")
    
    assert result["found"] is True
    assert result["article_id"] == "KB004"
    assert "Printer" in result["title"]
    assert result["category"] == "Hardware"


def test_empty_query():
    """Test that empty query returns not found."""
    result = search_knowledge_base("")
    
    assert result["found"] is False
    assert result["confidence"] == 0


def test_no_match_query():
    """Test query with no good matches returns low confidence."""
    result = search_knowledge_base("xyz123 random gibberish")
    
    # Should still return something but with low confidence
    assert result["confidence"] < 50


def test_high_confidence_match():
    """Test that good matches have high confidence."""
    result = search_knowledge_base("VPN connection issues remote access")
    
    assert result["found"] is True
    assert result["confidence"] >= 70


def test_wifi_disconnecting():
    """Test Wi-Fi disconnecting query."""
    result = search_knowledge_base("My wifi keeps disconnecting")
    
    assert result["found"] is True
    assert result["article_id"] == "KB010"
    assert "Wi-Fi" in result["title"]


def test_slow_laptop():
    """Test slow laptop performance query."""
    result = search_knowledge_base("laptop is very slow")
    
    assert result["found"] is True
    assert result["article_id"] == "KB005"
    assert "Slow" in result["title"] or "Performance" in result["title"]

# Made with Bob
