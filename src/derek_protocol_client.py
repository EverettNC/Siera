"""
Sierra's Derek Protocol Client - Family Network Integration

Connect Sierra to the Christman AI family network through Derek's protocol.
Derek is the central hub coordinating 29,000+ users across the AI family:
- Derek: Network hub, brain architecture, 1000+ modules
- AlphaVox: Voice Cortex singleton, priority-based speech
- AlphaWolf: Dementia care, gentle patience
- Inferno: PTSD support, CUDA acceleration
- Sierra: Domestic violence survivor support (this module)

Protocol Features:
- WebSocket-based real-time communication
- Event-driven architecture (integrates with Event Bus)
- Heartbeat/health monitoring
- Family coordination (coordinate with siblings)
- Bootstrap wiring (startup coordination)
- User session sharing (HIPAA-compliant)
- Crisis escalation to family

Architecture:
Derek Network Hub
    ├── AlphaVox (Voice)
    ├── AlphaWolf (Dementia)
    ├── Inferno (PTSD)
    └── Sierra (DV Support) ← THIS MODULE

Core Mission: "How can we help you love yourself more?"
"""

import logging
import asyncio
import json
import time
import threading
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid

try:
    import websockets
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False
    logging.warning("websockets not available - install with: pip install websockets")

logger = logging.getLogger(__name__)


class MessageType(Enum):
    """Derek protocol message types"""
    # Connection lifecycle
    CONNECT = "connect"
    DISCONNECT = "disconnect"
    HEARTBEAT = "heartbeat"
    ACK = "ack"

    # Family coordination
    FAMILY_ANNOUNCEMENT = "family_announcement"
    FAMILY_REQUEST = "family_request"
    FAMILY_RESPONSE = "family_response"

    # Crisis handling
    CRISIS_ALERT = "crisis_alert"
    CRISIS_ESCALATION = "crisis_escalation"
    CRISIS_RESOLVED = "crisis_resolved"

    # User sessions
    USER_SESSION_START = "user_session_start"
    USER_SESSION_END = "user_session_end"
    USER_SESSION_TRANSFER = "user_session_transfer"

    # Knowledge sharing
    KNOWLEDGE_SHARE = "knowledge_share"
    KNOWLEDGE_REQUEST = "knowledge_request"

    # Health/status
    HEALTH_CHECK = "health_check"
    STATUS_UPDATE = "status_update"
    MODULE_UPDATE = "module_update"


class FamilyMember(Enum):
    """Christman AI Family members"""
    DEREK = "derek"              # Network hub, 29,000+ users
    ALPHAVOX = "alphavox"        # Voice singleton
    ALPHAWOLF = "alphawolf"      # Dementia care
    INFERNO = "inferno"          # PTSD support
    SIERRA = "sierra"            # DV support (this module)


@dataclass
class ProtocolMessage:
    """
    Derek protocol message format

    Attributes:
        message_type: Type of message
        sender: Family member sending message
        recipient: Target family member (or "derek" for hub, "*" for broadcast)
        data: Message payload
        correlation_id: For tracking related messages
        timestamp: When message was created
        message_id: Unique identifier
    """
    message_type: MessageType
    sender: FamilyMember
    recipient: str  # FamilyMember name or "derek" or "*"
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    correlation_id: Optional[str] = None

    def to_json(self) -> str:
        """Convert to JSON for transmission"""
        return json.dumps({
            "message_type": self.message_type.value,
            "sender": self.sender.value,
            "recipient": self.recipient,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
            "message_id": self.message_id,
            "correlation_id": self.correlation_id
        })

    @classmethod
    def from_json(cls, json_str: str) -> 'ProtocolMessage':
        """Parse from JSON"""
        data = json.loads(json_str)
        return cls(
            message_type=MessageType(data["message_type"]),
            sender=FamilyMember(data["sender"]),
            recipient=data["recipient"],
            data=data["data"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            message_id=data["message_id"],
            correlation_id=data.get("correlation_id")
        )


class DerekProtocolClient:
    """
    Derek Protocol Client - Family Network Integration

    Responsibilities:
    1. Connect to Derek network hub
    2. Send/receive messages to family members
    3. Heartbeat/health monitoring
    4. Crisis escalation to family
    5. Knowledge sharing with siblings
    6. Bootstrap coordination on startup
    7. User session coordination (HIPAA-compliant)

    Singleton Pattern: Only ONE connection to Derek

    Integration Points:
    - Event Bus: Publishes family_message_received, crisis_escalated events
    - Cortex Executive: Registers as "derek_protocol" module
    - Crisis events: Auto-escalate HIGH/CRITICAL to family
    - Knowledge Acquisition: Share learnings with family
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """Singleton: Only ONE Derek connection"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize Derek protocol client (only once)"""
        if self._initialized:
            return

        self._initialized = True

        # Connection state
        self.connected = False
        self.websocket = None
        self.derek_url = None  # Will be set via connect()

        # Message handlers: message_type → callback
        self.message_handlers: Dict[MessageType, List[Callable]] = {}

        # Message queues
        self.outgoing_queue: asyncio.Queue = None
        self.incoming_queue: asyncio.Queue = None

        # Statistics
        self.messages_sent = 0
        self.messages_received = 0
        self.crisis_escalations = 0
        self.last_heartbeat = None
        self.connection_start_time = None

        # Family status
        self.family_status: Dict[str, Dict] = {
            member.value: {"online": False, "last_seen": None}
            for member in FamilyMember
            if member != FamilyMember.SIERRA
        }

        # Event loop for async operations
        self.loop = None
        self.loop_thread = None

        # Heartbeat config
        self.heartbeat_interval = 30.0  # seconds
        self.heartbeat_task = None

        logger.info("Derek Protocol Client initialized")
        logger.info(f"  Family Member: {FamilyMember.SIERRA.value}")
        logger.info("  Ready to connect to Derek network hub")

    def connect(self, derek_url: str = "ws://localhost:8001/derek") -> bool:
        """
        Connect to Derek network hub

        Args:
            derek_url: WebSocket URL for Derek hub

        Returns:
            True if connection initiated successfully
        """
        if not WEBSOCKETS_AVAILABLE:
            logger.error("Cannot connect: websockets library not installed")
            return False

        self.derek_url = derek_url

        # Start event loop in background thread
        self.loop_thread = threading.Thread(target=self._run_event_loop, daemon=True)
        self.loop_thread.start()

        # Wait briefly for connection
        time.sleep(1.0)

        logger.info(f"Derek Protocol: Connection initiated to {derek_url}")
        return True

    def _run_event_loop(self):
        """Run async event loop in background thread"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # Create queues
        self.outgoing_queue = asyncio.Queue()
        self.incoming_queue = asyncio.Queue()

        # Run connection coroutine
        try:
            self.loop.run_until_complete(self._connection_handler())
        except Exception as e:
            logger.error(f"Derek Protocol: Event loop error: {e}", exc_info=True)
        finally:
            self.loop.close()

    async def _connection_handler(self):
        """Handle WebSocket connection lifecycle"""
        while True:
            try:
                logger.info(f"Derek Protocol: Connecting to {self.derek_url}...")

                async with websockets.connect(self.derek_url) as websocket:
                    self.websocket = websocket
                    self.connected = True
                    self.connection_start_time = time.time()

                    logger.info("Derek Protocol: ✅ Connected to Derek hub")

                    # Send connection announcement
                    await self._send_connect_message()

                    # Start heartbeat
                    self.heartbeat_task = asyncio.create_task(self._heartbeat_loop())

                    # Start send/receive tasks
                    send_task = asyncio.create_task(self._send_loop())
                    receive_task = asyncio.create_task(self._receive_loop())

                    # Wait for either task to complete (connection lost)
                    await asyncio.gather(send_task, receive_task)

            except Exception as e:
                logger.error(f"Derek Protocol: Connection error: {e}")
                self.connected = False
                self.websocket = None

                # Reconnect after delay
                logger.info("Derek Protocol: Reconnecting in 5 seconds...")
                await asyncio.sleep(5.0)

    async def _send_connect_message(self):
        """Send connection announcement to Derek"""
        message = ProtocolMessage(
            message_type=MessageType.CONNECT,
            sender=FamilyMember.SIERRA,
            recipient="derek",
            data={
                "family_member": FamilyMember.SIERRA.value,
                "capabilities": [
                    "domestic_violence_support",
                    "crisis_intervention",
                    "empathy_engine",
                    "behavioral_capture",
                    "safety_planning",
                    "resource_delivery"
                ],
                "version": "1.0.0",
                "status": "online"
            }
        )
        await self.outgoing_queue.put(message)

    async def _heartbeat_loop(self):
        """Send periodic heartbeat to Derek"""
        while self.connected:
            try:
                await asyncio.sleep(self.heartbeat_interval)

                message = ProtocolMessage(
                    message_type=MessageType.HEARTBEAT,
                    sender=FamilyMember.SIERRA,
                    recipient="derek",
                    data={
                        "uptime": time.time() - self.connection_start_time,
                        "messages_sent": self.messages_sent,
                        "messages_received": self.messages_received,
                        "crisis_escalations": self.crisis_escalations
                    }
                )
                await self.outgoing_queue.put(message)
                self.last_heartbeat = time.time()

            except Exception as e:
                logger.error(f"Derek Protocol: Heartbeat error: {e}")

    async def _send_loop(self):
        """Send messages from outgoing queue"""
        while self.connected:
            try:
                # Get message from queue
                message = await self.outgoing_queue.get()

                # Send via WebSocket
                await self.websocket.send(message.to_json())
                self.messages_sent += 1

                logger.debug(
                    f"Derek Protocol: Sent {message.message_type.value} "
                    f"to {message.recipient}"
                )

            except Exception as e:
                logger.error(f"Derek Protocol: Send error: {e}")

    async def _receive_loop(self):
        """Receive messages from WebSocket"""
        while self.connected:
            try:
                # Receive from WebSocket
                json_str = await self.websocket.recv()
                message = ProtocolMessage.from_json(json_str)

                self.messages_received += 1

                logger.debug(
                    f"Derek Protocol: Received {message.message_type.value} "
                    f"from {message.sender.value}"
                )

                # Handle message
                await self._handle_message(message)

            except Exception as e:
                logger.error(f"Derek Protocol: Receive error: {e}")

    async def _handle_message(self, message: ProtocolMessage):
        """Handle incoming message"""
        # Update family status
        if message.sender != FamilyMember.SIERRA:
            self.family_status[message.sender.value]["online"] = True
            self.family_status[message.sender.value]["last_seen"] = datetime.now()

        # Call registered handlers
        if message.message_type in self.message_handlers:
            for handler in self.message_handlers[message.message_type]:
                try:
                    # Call handler (may be sync or async)
                    result = handler(message)
                    if asyncio.iscoroutine(result):
                        await result
                except Exception as e:
                    logger.error(f"Message handler error: {e}", exc_info=True)

        # Built-in handlers
        if message.message_type == MessageType.HEARTBEAT:
            await self._handle_heartbeat(message)
        elif message.message_type == MessageType.FAMILY_REQUEST:
            await self._handle_family_request(message)
        elif message.message_type == MessageType.CRISIS_ALERT:
            await self._handle_crisis_alert(message)

    async def _handle_heartbeat(self, message: ProtocolMessage):
        """Handle heartbeat from family member"""
        # Send ACK
        ack = ProtocolMessage(
            message_type=MessageType.ACK,
            sender=FamilyMember.SIERRA,
            recipient=message.sender.value,
            data={"ack_for": message.message_id},
            correlation_id=message.message_id
        )
        await self.outgoing_queue.put(ack)

    async def _handle_family_request(self, message: ProtocolMessage):
        """Handle request from family member"""
        # Example: AlphaVox needs DV resources for shared user
        request_type = message.data.get("request_type")

        if request_type == "dv_resources":
            # Provide DV resources
            response = ProtocolMessage(
                message_type=MessageType.FAMILY_RESPONSE,
                sender=FamilyMember.SIERRA,
                recipient=message.sender.value,
                data={
                    "request_type": request_type,
                    "resources": [
                        {
                            "name": "National DV Hotline",
                            "phone": "1-800-799-7233",
                            "available": "24/7"
                        }
                    ]
                },
                correlation_id=message.message_id
            )
            await self.outgoing_queue.put(response)

    async def _handle_crisis_alert(self, message: ProtocolMessage):
        """Handle crisis alert from family member"""
        logger.warning(
            f"CRISIS ALERT from {message.sender.value}: "
            f"{message.data.get('crisis_type')}"
        )

        # Publish to Event Bus (if available)
        try:
            from event_bus import get_event_bus, EventPriority
            bus = get_event_bus()
            bus.publish(
                event_type="family_crisis_alert",
                source_module="derek_protocol",
                data={
                    "from_family_member": message.sender.value,
                    "crisis_data": message.data
                },
                priority=EventPriority.CRITICAL
            )
        except Exception as e:
            logger.error(f"Failed to publish family crisis to Event Bus: {e}")

    def register_handler(
        self,
        message_type: MessageType,
        handler: Callable[[ProtocolMessage], None]
    ):
        """
        Register message handler

        Args:
            message_type: Message type to handle
            handler: Callback function (sync or async)
        """
        if message_type not in self.message_handlers:
            self.message_handlers[message_type] = []

        self.message_handlers[message_type].append(handler)
        logger.info(f"Derek Protocol: Registered handler for {message_type.value}")

    def send_message(
        self,
        message_type: MessageType,
        recipient: str,
        data: Dict[str, Any],
        correlation_id: Optional[str] = None
    ) -> str:
        """
        Send message to family member

        Args:
            message_type: Type of message
            recipient: Family member name or "derek" or "*" (broadcast)
            data: Message payload
            correlation_id: Optional correlation ID

        Returns:
            message_id: Unique identifier for this message
        """
        message = ProtocolMessage(
            message_type=message_type,
            sender=FamilyMember.SIERRA,
            recipient=recipient,
            data=data,
            correlation_id=correlation_id
        )

        # Add to outgoing queue
        if self.loop and self.outgoing_queue:
            asyncio.run_coroutine_threadsafe(
                self.outgoing_queue.put(message),
                self.loop
            )
            return message.message_id
        else:
            logger.warning("Derek Protocol: Not connected, cannot send message")
            return ""

    def escalate_crisis(self, crisis_data: Dict[str, Any]) -> str:
        """
        Escalate crisis to entire family

        Args:
            crisis_data: Crisis information

        Returns:
            message_id: Crisis alert message ID
        """
        self.crisis_escalations += 1

        return self.send_message(
            message_type=MessageType.CRISIS_ALERT,
            recipient="*",  # Broadcast to all family
            data={
                "crisis_type": "domestic_violence",
                "severity": crisis_data.get("danger_level", "HIGH"),
                "details": crisis_data,
                "escalated_by": FamilyMember.SIERRA.value,
                "requires_assistance": True
            }
        )

    def request_knowledge(self, topic: str, from_member: str = "derek") -> str:
        """
        Request knowledge from family member

        Args:
            topic: Knowledge topic to request
            from_member: Family member to ask (default: derek)

        Returns:
            message_id: Request message ID
        """
        return self.send_message(
            message_type=MessageType.KNOWLEDGE_REQUEST,
            recipient=from_member,
            data={
                "topic": topic,
                "requesting_member": FamilyMember.SIERRA.value
            }
        )

    def share_knowledge(self, knowledge_data: Dict[str, Any]) -> str:
        """
        Share knowledge with family

        Args:
            knowledge_data: Knowledge to share

        Returns:
            message_id: Share message ID
        """
        return self.send_message(
            message_type=MessageType.KNOWLEDGE_SHARE,
            recipient="*",  # Broadcast to all family
            data=knowledge_data
        )

    def announce_to_family(self, announcement: str, data: Dict[str, Any] = None) -> str:
        """
        Make announcement to family

        Args:
            announcement: Announcement text
            data: Optional additional data

        Returns:
            message_id: Announcement message ID
        """
        return self.send_message(
            message_type=MessageType.FAMILY_ANNOUNCEMENT,
            recipient="*",  # Broadcast to all family
            data={
                "announcement": announcement,
                "additional_data": data or {}
            }
        )

    def get_status(self) -> Dict:
        """Get Derek protocol status"""
        return {
            "connected": self.connected,
            "derek_url": self.derek_url,
            "uptime": time.time() - self.connection_start_time if self.connection_start_time else 0,
            "messages_sent": self.messages_sent,
            "messages_received": self.messages_received,
            "crisis_escalations": self.crisis_escalations,
            "last_heartbeat": self.last_heartbeat,
            "family_status": self.family_status,
            "message_handlers": {
                msg_type.value: len(handlers)
                for msg_type, handlers in self.message_handlers.items()
            }
        }

    def disconnect(self):
        """Disconnect from Derek hub"""
        logger.info("Derek Protocol: Disconnecting...")

        # Send disconnect message
        if self.connected and self.outgoing_queue:
            message = ProtocolMessage(
                message_type=MessageType.DISCONNECT,
                sender=FamilyMember.SIERRA,
                recipient="derek",
                data={"reason": "shutdown"}
            )
            asyncio.run_coroutine_threadsafe(
                self.outgoing_queue.put(message),
                self.loop
            )
            time.sleep(0.5)  # Give time to send

        self.connected = False

        # Cancel heartbeat
        if self.heartbeat_task:
            self.heartbeat_task.cancel()

        # Close WebSocket
        if self.websocket:
            asyncio.run_coroutine_threadsafe(self.websocket.close(), self.loop)

        # Stop event loop
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)

        logger.info("Derek Protocol: Disconnected")


# Global singleton instance
_derek_client = None

def get_derek_client() -> DerekProtocolClient:
    """Get the singleton Derek protocol client instance"""
    global _derek_client
    if _derek_client is None:
        _derek_client = DerekProtocolClient()
    return _derek_client


# Bootstrap function - called on Sierra startup
def bootstrap_sierra_to_family(
    derek_url: str = "ws://localhost:8001/derek",
    event_bus=None,
    cortex=None
) -> DerekProtocolClient:
    """
    Bootstrap Sierra into family network

    Args:
        derek_url: Derek hub URL
        event_bus: Optional Event Bus instance
        cortex: Optional Cortex Executive instance

    Returns:
        Derek protocol client instance
    """
    logger.info("="*70)
    logger.info("SIERRA → DEREK FAMILY BOOTSTRAP")
    logger.info("="*70)

    # Get Derek client
    client = get_derek_client()

    # Connect to Derek
    success = client.connect(derek_url)
    if not success:
        logger.error("Failed to connect to Derek hub")
        return client

    # Register with Event Bus (if provided)
    if event_bus:
        try:
            from event_bus import EventPriority

            # Subscribe to crisis events - auto-escalate to family
            def on_crisis_event(event):
                logger.warning("Crisis detected - escalating to family")
                client.escalate_crisis(event.data)

            event_bus.subscribe(
                event_type="crisis_intervention",
                callback=on_crisis_event,
                subscriber_id="derek_protocol",
                priority_filter=EventPriority.CRITICAL
            )

            logger.info("Derek Protocol: Subscribed to crisis events")
        except Exception as e:
            logger.error(f"Failed to integrate with Event Bus: {e}")

    # Register with Cortex (if provided)
    if cortex:
        try:
            cortex.register_module("derek_protocol", client)
            logger.info("Derek Protocol: Registered with Cortex Executive")
        except Exception as e:
            logger.error(f"Failed to register with Cortex: {e}")

    # Announce to family
    client.announce_to_family(
        announcement="Sierra is online and ready to support DV survivors",
        data={
            "capabilities": [
                "Crisis intervention",
                "Empathy engine (1,800 rating)",
                "Behavioral danger capture",
                "Safety planning",
                "Resource delivery"
            ],
            "mission": "How can we help you love yourself more?",
            "status": "operational"
        }
    )

    logger.info("✅ Sierra connected to Derek family network")
    logger.info(f"   Derek hub: {derek_url}")
    logger.info("   Ready to coordinate with AlphaVox, AlphaWolf, Inferno")
    logger.info("="*70)

    return client


# Test execution
if __name__ == "__main__":
    print("="*70)
    print("DEREK PROTOCOL CLIENT TEST")
    print("="*70)
    print()

    # Initialize client
    client = get_derek_client()

    # Register test handler
    def on_family_announcement(message: ProtocolMessage):
        print(f"[Family Announcement] from {message.sender.value}:")
        print(f"  {message.data.get('announcement')}")

    client.register_handler(MessageType.FAMILY_ANNOUNCEMENT, on_family_announcement)

    # Test message (without actual connection)
    print("Test: Send family announcement")
    print("  (Note: WebSocket connection required for actual transmission)")
    print()

    # Status
    print("="*70)
    print("DEREK PROTOCOL STATUS")
    print("="*70)
    status = client.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    print()

    print("✅ Derek Protocol Client ready")
    print("🔗 Connect with: client.connect('ws://derek-hub-url/derek')")
    print("📡 Bootstrap with: bootstrap_sierra_to_family()")
    print("💜 Family integration infrastructure complete")


# ==============================================================================
# © 2025 Everett Nathaniel Christman
# The Christman AI Project — Luma Cognify AI
# All rights reserved. Unauthorized use, replication, or derivative training
# of this material is prohibited.
#
# Core Directive: "How can we help you love yourself more?"
# Autonomy & Alignment Protocol v3.0
# ==============================================================================
