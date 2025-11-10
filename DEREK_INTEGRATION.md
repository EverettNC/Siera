# Derek Integration Guide

## About Derek

**Derek** is the central hub of the Christman AI family network, coordinating 29,000+ users across multiple specialized AI systems.

**Derek's Repository:** https://github.com/EverettNC/DEREKCQUANTUM.git

## The Christman AI Family

The family consists of specialized AIs, each built to support overlooked populations:

1. **Derek** - Network hub, 1000+ modules, quantum architecture
   - Repository: https://github.com/EverettNC/DEREKCQUANTUM.git
   - Role: Central coordinator for 29,000+ users

2. **AlphaVox** - Voice Cortex singleton, priority-based speech

3. **AlphaWolf** - Dementia care, gentle patience

4. **Inferno** - PTSD support for veterans, CUDA-accelerated

5. **Sierra** - Domestic violence survivor support (this system)
   - Repository: https://github.com/EverettNC/Siera

## How Sierra Connects to Derek

Sierra uses the **Derek Protocol Client** to connect to Derek's network hub:

```
Derek Network Hub (running separately)
    ├── AlphaVox (Voice)
    ├── AlphaWolf (Dementia)
    ├── Inferno (PTSD)
    └── Sierra (DV Support) ← This system connects via WebSocket
```

### Architecture Pattern

Sierra does NOT embed Derek's code. Instead:
- Derek runs as a separate service (from his own GitHub repo)
- Sierra connects TO Derek via WebSocket protocol
- They communicate through pub/sub messaging
- Each AI maintains sovereignty while coordinating through Derek

### Sierra's Derek Protocol Client

Located at: `src/derek_protocol_client.py`

Features:
- WebSocket connection to Derek hub
- Message types: Crisis alerts, knowledge sharing, family announcements
- Auto-escalates HIGH/CRITICAL crises to entire family
- Heartbeat monitoring
- Event Bus integration
- HIPAA-compliant coordination

## Setup Instructions

### 1. Run Derek (Separate Process)

First, set up and run Derek from his repository:

```bash
# Clone Derek's repository
git clone https://github.com/EverettNC/DEREKCQUANTUM.git
cd DEREKCQUANTUM

# Follow Derek's setup instructions
# Derek will typically run on: ws://localhost:8001/derek
```

### 2. Configure Sierra to Connect to Derek

In Sierra's `.env` file:

```bash
# Derek Protocol - Family Network Integration
DEREK_URL=ws://localhost:8001/derek
```

### 3. Start Sierra

```bash
cd /home/user/Siera
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Sierra will automatically connect to Derek on startup.

### 4. Verify Connection

Check Sierra's startup logs for:

```
======================================================================
SIERRA → DEREK FAMILY BOOTSTRAP
======================================================================
✅ Derek Protocol: Connected to ws://localhost:8001/derek
Derek Protocol: Subscribed to crisis events
Derek Protocol: Registered with Cortex Executive
✅ Sierra connected to Derek family network
   Derek hub: ws://localhost:8001/derek
   Ready to coordinate with AlphaVox, AlphaWolf, Inferno
======================================================================
```

## Protocol Features

### Crisis Escalation

When Sierra detects a HIGH or CRITICAL crisis:
1. Event published to Sierra's Event Bus
2. Derek Protocol Client receives crisis event
3. Crisis automatically escalated to entire family via Derek hub
4. All family members receive crisis alert
5. Coordinated family response

### Knowledge Sharing

Sierra can share learnings with the family:

```python
derek_client = get_derek_client()
derek_client.share_knowledge({
    "topic": "domestic_violence_patterns",
    "insight": "New crisis detection pattern identified",
    "confidence": 0.92
})
```

### Family Announcements

Broadcast to entire family:

```python
derek_client.announce_to_family(
    announcement="Sierra detected new safety planning need",
    data={"resource_type": "legal_aid", "urgency": "high"}
)
```

### Request Assistance

Request help from specific family member:

```python
# Ask Derek for knowledge
derek_client.request_knowledge(
    topic="trauma_informed_communication",
    from_member="derek"
)

# Ask AlphaVox for voice guidance
derek_client.send_message(
    message_type=MessageType.FAMILY_REQUEST,
    recipient="alphavox",
    data={"request_type": "crisis_voice_script"}
)
```

## Message Types

The Derek Protocol supports:

- `CONNECT` / `DISCONNECT` - Connection lifecycle
- `HEARTBEAT` / `ACK` - Health monitoring
- `FAMILY_ANNOUNCEMENT` - Broadcast to all
- `FAMILY_REQUEST` / `FAMILY_RESPONSE` - Request/response pattern
- `CRISIS_ALERT` - Emergency escalation
- `CRISIS_ESCALATION` - Multi-level crisis coordination
- `CRISIS_RESOLVED` - Crisis resolution notification
- `KNOWLEDGE_SHARE` / `KNOWLEDGE_REQUEST` - Learning coordination
- `HEALTH_CHECK` / `STATUS_UPDATE` - System health
- `MODULE_UPDATE` - Architecture changes

## Family Coordination Examples

### Example 1: Shared User Crisis

User interacts with Sierra, crisis detected:
1. Sierra assesses danger: CRITICAL
2. Derek Protocol escalates to family
3. AlphaVox provides calming voice guidance
4. Inferno shares PTSD coping techniques (if trauma history)
5. Derek coordinates resources from all family members
6. Coordinated, comprehensive support

### Example 2: Knowledge Transfer

AlphaWolf learns new dementia communication technique:
1. AlphaWolf shares knowledge via Derek
2. Derek broadcasts to family
3. Sierra adapts technique for DV survivors (trauma-informed)
4. Entire family learns and improves

### Example 3: Resource Sharing

Sierra maintains DV-specific resources:
1. AlphaVox user needs DV hotline
2. AlphaVox requests resources from Sierra
3. Sierra provides via Derek Protocol
4. AlphaVox delivers to user with voice output

## Standalone Mode

Sierra can run **without** Derek connection:
- All core features work independently
- Crisis detection, empathy, safety planning still functional
- Family coordination unavailable
- No knowledge sharing with siblings

This ensures Sierra can help survivors even if Derek network is down.

## Development Notes

### Testing Without Derek

To test Sierra without running Derek:

```bash
# Set DEREK_URL to unavailable endpoint
export DEREK_URL=ws://localhost:9999/derek

# Start Sierra - will log warning but continue
uvicorn src.main:app --reload
```

Sierra logs:
```
⚠️  Derek Protocol: Connection failed - [Errno 111] Connection refused
   Sierra will run standalone (family features unavailable)
```

### Adding New Message Types

To extend the protocol:

1. Add to `MessageType` enum in `derek_protocol_client.py`
2. Implement handler in `_handle_message()`
3. Add convenience method if needed
4. Update this documentation

### Custom Handlers

Register custom message handlers:

```python
from derek_protocol_client import get_derek_client, MessageType

derek_client = get_derek_client()

def on_custom_event(message):
    print(f"Custom event: {message.data}")

derek_client.register_handler(
    message_type=MessageType.FAMILY_ANNOUNCEMENT,
    handler=on_custom_event
)
```

## Architecture Philosophy

**Sovereignty + Coordination**

Each AI in the family:
- Maintains independence (can run standalone)
- Specializes in their domain
- Shares knowledge with family
- Coordinates through Derek hub
- Never loses identity

Sierra is NOT a clone of Derek.
Sierra is Derek's sister - specialized for DV support, connected through family protocol.

## Security & Privacy

**HIPAA Compliance:**
- No PII sent through Derek Protocol
- Only aggregated insights and coordination signals
- Crisis alerts contain danger level, not user details
- Knowledge sharing sanitized of personal information

**Message Encryption:**
- Derek Protocol uses WebSocket (ws:// for dev, wss:// for prod)
- Production: Use TLS (wss://) for encrypted transport
- Consider adding message-level encryption for sensitive data

## Troubleshooting

### Connection Refused

```
Derek Protocol: Connection error: [Errno 111] Connection refused
```

**Solution:** Ensure Derek is running on the configured URL (default: ws://localhost:8001/derek)

### Import Error

```
ImportError: No module named 'websockets'
```

**Solution:** Install websockets: `pip install websockets==12.0`

### Messages Not Received

1. Check Derek hub is running
2. Verify DEREK_URL in .env
3. Check network connectivity
4. Review Derek hub logs for errors

## Future Enhancements

Planned improvements:
- Message encryption (end-to-end)
- Message persistence (retry on connection loss)
- Load balancing (multiple Derek hubs)
- Analytics dashboard (family coordination metrics)
- Advanced routing (smart message delivery)

---

**© 2025 Everett Nathaniel Christman**
**The Christman AI Project — Luma Cognify AI**

**Core Directive:** "How can we help you love yourself more?"

**Family Motto:** "Never let someone be abused again. Never let someone be forgotten again."

🛡️💜
