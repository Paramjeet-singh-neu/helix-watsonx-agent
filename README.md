# Helix - Intelligent IT Helpdesk Agent for watsonx Orchestrate

Helix is a Tier 2+ IT helpdesk agent that intelligently resolves issues using a knowledge base before creating support tickets. Built for the watsonx Orchestrate hackathon.

## 🎯 Features

- **Intelligent KB Search**: Searches 10 common IT issues with confidence scoring
- **Smart Escalation**: Only creates tickets when KB confidence < 70 or solution fails
- **Priority Detection**: Automatically detects urgency from user language
- **Conversational**: Warm and helpful, not form-like
- **Ticket Tracking**: Full ticket lifecycle management

## 🔧 Tools

1. **search_knowledge_base** - Searches internal KB for IT solutions
2. **create_ticket** - Creates tickets with auto-generated IDs and priority-based ETAs
3. **get_ticket_status** - Retrieves ticket details by ID
4. **list_my_tickets** - Lists all tickets for a user

## 📁 Project Structure

```
helix/
├── agents/
│   └── helix.yaml           # Agent configuration
├── tools/
│   ├── search_knowledge_base.py
│   ├── create_ticket.py
│   ├── get_ticket_status.py
│   ├── list_my_tickets.py
│   ├── *_test.py            # Pytest tests for each tool
├── tests/
│   ├── helix_kb_deflect.json
│   ├── helix_ticket_create.json
│   └── helix_status_check.json
└── README.md
```

## 🚀 Deployment

### Prerequisites
- watsonx Orchestrate environment configured
- `uv` package manager installed

### Deploy Tools
```bash
cd tools
uv run orchestrate tools import --kind python --file search_knowledge_base.py
uv run orchestrate tools import --kind python --file create_ticket.py
uv run orchestrate tools import --kind python --file get_ticket_status.py
uv run orchestrate tools import --kind python --file list_my_tickets.py
```

### Deploy Agent
```bash
cd agents
uv run orchestrate agents import --file helix.yaml
```

### Verify Deployment
```bash
uv run orchestrate agents list  # Should show 'helix'
uv run orchestrate tools list   # Should show all 4 tools
```

## 🧪 Testing

### Run Pytest Tests
```bash
cd tools
pytest search_knowledge_base_test.py
pytest create_ticket_test.py
pytest get_ticket_status_test.py
pytest list_my_tickets_test.py
```

### Journey Success Tests
Three test cases are provided in the `tests/` directory:
1. **KB Deflection** - Tests KB search without ticket creation
2. **Urgent Ticket Creation** - Tests HIGH priority ticket creation
3. **Status Check** - Tests ticket listing functionality

## 💡 Usage Examples

### KB Deflection (No Ticket)
```
User: "How do I connect to VPN?"
Helix: [Searches KB, finds solution with high confidence]
      [Provides step-by-step VPN connection guide]
```

### Urgent Issue (Creates Ticket)
```
User: "My laptop is completely dead, I can't work, this is urgent"
Helix: [Searches KB, low confidence]
      [Creates HIGH priority ticket TKT-1001]
      [Confirms ticket with 4-hour ETA]
```

### Status Check
```
User: "What's the status of my tickets? Email: alice@company.com"
Helix: [Lists all tickets for alice@company.com]
      [Shows ticket IDs, status, priority, and ETAs]
```

## 🎓 Knowledge Base

Helix includes solutions for 10 common IT issues:
- VPN Connection Issues
- Password Reset
- MFA Setup Guide
- Printer Not Working
- Slow Laptop Performance
- Software Installation Request
- Cannot Access Shared Drive
- Email Not Syncing
- Monitor Not Detected
- Wi-Fi Keeps Disconnecting

## Agent

This agent demonstrates:
- ✅ Intelligent behavior (not just form-filling)
- ✅ Multi-tool orchestration
- ✅ Context-aware decision making
- ✅ Complete test coverage
- ✅ Production-ready code quality

## 📝 License

Built for the watsonx Orchestrate Hackathon 2026

## 👤 Author

Paramjeet Singh
