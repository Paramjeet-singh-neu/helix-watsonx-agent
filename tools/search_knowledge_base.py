"""
Search internal knowledge base for IT issue solutions.
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.agent_builder.tools import tool

# In-memory knowledge base with common IT issues
KNOWLEDGE_BASE = [
    {
        "id": "KB001",
        "title": "VPN Connection Issues",
        "category": "Network",
        "solution_steps": [
            "1. Ensure you have the latest VPN client installed",
            "2. Check your internet connection is stable",
            "3. Verify your VPN credentials are correct",
            "4. Try disconnecting and reconnecting",
            "5. If issue persists, restart your computer and try again",
            "6. Contact IT if problem continues after restart"
        ],
        "keywords": ["vpn", "connection", "connect", "remote", "access", "network"]
    },
    {
        "id": "KB002",
        "title": "Password Reset",
        "category": "Access",
        "solution_steps": [
            "1. Go to the company password reset portal",
            "2. Enter your email address",
            "3. Click 'Forgot Password'",
            "4. Check your email for reset link",
            "5. Follow the link and create a new password",
            "6. Password must be at least 12 characters with uppercase, lowercase, number, and special character"
        ],
        "keywords": ["password", "reset", "forgot", "login", "credentials", "access"]
    },
    {
        "id": "KB003",
        "title": "MFA Setup Guide",
        "category": "Access",
        "solution_steps": [
            "1. Download Microsoft Authenticator or Google Authenticator app",
            "2. Log into your account settings",
            "3. Navigate to Security > Multi-Factor Authentication",
            "4. Click 'Set up MFA'",
            "5. Scan the QR code with your authenticator app",
            "6. Enter the 6-digit code to verify setup"
        ],
        "keywords": ["mfa", "multi-factor", "authentication", "2fa", "two-factor", "authenticator", "security"]
    },
    {
        "id": "KB004",
        "title": "Printer Not Working",
        "category": "Hardware",
        "solution_steps": [
            "1. Check if printer is powered on and connected to network",
            "2. Verify printer has paper and toner/ink",
            "3. Check for any error messages on printer display",
            "4. Remove and re-add the printer in your computer settings",
            "5. Restart the print spooler service",
            "6. Try printing a test page"
        ],
        "keywords": ["printer", "print", "printing", "not working", "paper", "toner", "ink"]
    },
    {
        "id": "KB005",
        "title": "Slow Laptop Performance",
        "category": "Hardware",
        "solution_steps": [
            "1. Close unnecessary applications and browser tabs",
            "2. Check Task Manager for high CPU/memory usage",
            "3. Restart your laptop",
            "4. Run Windows Update to ensure system is current",
            "5. Clear browser cache and temporary files",
            "6. Check available disk space (should have at least 20% free)",
            "7. Run antivirus scan to check for malware"
        ],
        "keywords": ["slow", "performance", "laptop", "computer", "freezing", "lagging", "speed"]
    },
    {
        "id": "KB006",
        "title": "Software Installation Request",
        "category": "Software",
        "solution_steps": [
            "1. Check if the software is available in the company software catalog",
            "2. If available, use Self-Service Portal to install",
            "3. If not available, submit a software request form",
            "4. Include business justification and manager approval",
            "5. IT will review within 2 business days",
            "6. Approved software will be deployed to your machine"
        ],
        "keywords": ["software", "install", "installation", "application", "program", "app", "request"]
    },
    {
        "id": "KB007",
        "title": "Cannot Access Shared Drive",
        "category": "Access",
        "solution_steps": [
            "1. Verify you are connected to the corporate network or VPN",
            "2. Check if you have the correct permissions for the shared drive",
            "3. Try accessing using the full UNC path (\\\\server\\share)",
            "4. Disconnect and reconnect the network drive",
            "5. Clear cached credentials in Credential Manager",
            "6. Restart your computer and try again"
        ],
        "keywords": ["shared drive", "network drive", "access", "permissions", "folder", "file share"]
    },
    {
        "id": "KB008",
        "title": "Email Not Syncing",
        "category": "Software",
        "solution_steps": [
            "1. Check your internet connection",
            "2. Verify Outlook is not in offline mode",
            "3. Click Send/Receive to manually sync",
            "4. Check if mailbox is full (delete old emails if needed)",
            "5. Repair your Outlook profile in Control Panel",
            "6. If using mobile, remove and re-add email account"
        ],
        "keywords": ["email", "outlook", "sync", "syncing", "mail", "not receiving", "not sending"]
    },
    {
        "id": "KB009",
        "title": "Monitor Not Detected",
        "category": "Hardware",
        "solution_steps": [
            "1. Check all cable connections (power and video cables)",
            "2. Try a different video cable if available",
            "3. Press Windows + P and select appropriate display mode",
            "4. Update display drivers from Device Manager",
            "5. Try connecting monitor to different port on laptop/PC",
            "6. Test monitor with another computer to rule out hardware failure"
        ],
        "keywords": ["monitor", "display", "screen", "not detected", "external monitor", "second screen"]
    },
    {
        "id": "KB010",
        "title": "Wi-Fi Keeps Disconnecting",
        "category": "Network",
        "solution_steps": [
            "1. Forget the Wi-Fi network and reconnect",
            "2. Update Wi-Fi adapter drivers",
            "3. Disable power saving mode for Wi-Fi adapter",
            "4. Move closer to the Wi-Fi access point",
            "5. Check for interference from other devices",
            "6. Reset network settings in Windows",
            "7. Contact IT if issue persists across multiple locations"
        ],
        "keywords": ["wifi", "wi-fi", "wireless", "disconnect", "disconnecting", "connection", "network"]
    }
]


class KBResult(BaseModel):
    """Knowledge base search result."""
    found: bool = Field(..., description="Whether a matching article was found")
    article_id: Optional[str] = Field(None, description="KB article ID")
    title: Optional[str] = Field(None, description="Article title")
    category: Optional[str] = Field(None, description="Issue category")
    solution_steps: List[str] = Field(default_factory=list, description="List of solution steps")
    confidence: int = Field(..., description="Match confidence score (0-100)")


@tool()
def search_knowledge_base(query: str) -> KBResult:
    """
    Search the knowledge base for solutions to IT issues.
    
    Args:
        query: User's description of their IT issue
        
    Returns:
        Knowledge base search result with article details and confidence score
    """
    if not query:
        return KBResult(
            found=False,
            confidence=0
        )
    
    query_lower = query.lower()
    query_words = set(query_lower.split())
    
    best_match = None
    best_score = 0
    
    for article in KNOWLEDGE_BASE:
        score = 0
        
        # Check for keyword matches
        keyword_matches = sum(1 for keyword in article["keywords"] if keyword in query_lower)
        score += keyword_matches * 15
        
        # Check for title substring match
        if any(word in article["title"].lower() for word in query_words):
            score += 20
        
        # Check for exact keyword in query
        for keyword in article["keywords"]:
            if keyword in query_words:
                score += 10
        
        # Bonus for category match
        if article["category"].lower() in query_lower:
            score += 10
        
        # Cap score at 100
        score = min(score, 100)
        
        if score > best_score:
            best_score = score
            best_match = article
    
    if best_match and best_score > 0:
        return KBResult(
            found=True,
            article_id=best_match["id"],
            title=best_match["title"],
            category=best_match["category"],
            solution_steps=best_match["solution_steps"],
            confidence=best_score
        )
    
    return KBResult(
        found=False,
        confidence=0
    )

# Made with Bob
