"""
Sierra's Event Bus - Inter-Module Communication Backbone

Adapted from Derek's EventBus (Christman AI Project)
Pub/Sub messaging system for loose coupling between modules

Why Event Bus?
- 1000+ modules can't all directly call each other (spaghetti code)
- Modules publish events, other modules subscribe
- Loose coupling = modules can be added/removed without breaking system
- Priority-based event routing for crisis intervention
- Audit trail for HIPAA compliance

Architecture Pattern:
Publisher → EventBus → Subscribers
(Module A emits event) → (Bus routes) → (Modules B, C, D react)

Example Events:
- danger_detected → Triggers: Voice Cortex, Resources, Safety Planning
- empathy_response_generated → Triggers: Multimodal Output, Conversation Logger
- safety_plan_created → Triggers: Encryption, Cloud Backup, User Notification
- crisis_intervention → Triggers: ALL modules (emergency override)

Core Mission: "How can we help you love yourself more?"
"""

import logging
import threading
import time
import queue
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid

logger = logging.getLogger(__name__)


class EventPriority(Enum):
    """Event priority levels"""
    CRITICAL = 1   # Crisis events - immediate processing
    HIGH = 2       # Safety-related events
    NORMAL = 3     # Standard events
    LOW = 4        # Background events


@dataclass
class Event:
    """
    Event published to the bus

    Attributes:
        event_type: Event identifier (e.g., "danger_detected", "empathy_generated")
        priority: Processing priority
        source_module: Module that published this event
        data: Event payload
        timestamp: When event was created
        event_id: Unique identifier
        correlation_id: For tracking related events
    """
    event_type: str
    priority: EventPriority
    source_module: str
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    correlation_id: Optional[str] = None

    def __lt__(self, other):
        """Compare by priority, then timestamp"""
        if self.priority.value != other.priority.value:
            return self.priority.value < other.priority.value
        return self.timestamp < other.timestamp


@dataclass
class Subscription:
    """
    Subscription to event type

    Attributes:
        event_type: Event type to subscribe to (or "*" for all events)
        callback: Function to call when event occurs
        subscriber_id: Unique identifier for subscriber
        priority_filter: Only receive events at or above this priority
    """
    event_type: str
    callback: Callable[[Event], None]
    subscriber_id: str
    priority_filter: Optional[EventPriority] = None


class SierraEventBus:
    """
    Sierra's Event Bus - Pub/Sub Communication Backbone

    Features:
    - Priority-based event routing
    - Asynchronous event processing
    - Multiple subscribers per event type
    - Wildcard subscriptions (subscribe to all events)
    - Event filtering by priority
    - Audit trail for HIPAA compliance
    - Thread-safe

    Singleton Pattern: Only ONE event bus exists

    Integration:
    - All Sierra modules publish/subscribe through this bus
    - Cortex Executive uses bus for cross-module coordination
    - Behavioral Capture publishes danger_detected events
    - Voice Cortex subscribes to crisis events
    - Resources subscribes to safety_plan_created events
    - All modules subscribe to crisis_intervention for emergency override
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """Singleton: Only ONE event bus exists"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize event bus (only once)"""
        if self._initialized:
            return

        self._initialized = True

        # Event queue (priority queue)
        self.event_queue: queue.PriorityQueue = queue.PriorityQueue()

        # Subscriptions: event_type → list of subscriptions
        self.subscriptions: Dict[str, List[Subscription]] = {}
        self.subscription_lock = threading.Lock()

        # Event history (for audit trail - HIPAA compliant)
        self.event_history: List[Event] = []
        self.max_history = 1000  # Keep last 1000 events
        self.history_lock = threading.Lock()

        # Statistics
        self.total_events_published = 0
        self.total_events_processed = 0
        self.critical_events = 0

        # Processing thread
        self.processing_active = True
        self.processor_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.processor_thread.start()

        logger.info("Sierra Event Bus initialized")
        logger.info("  Priority system: CRITICAL → HIGH → NORMAL → LOW")
        logger.info("  Pub/Sub architecture for loose module coupling")

    def publish(
        self,
        event_type: str,
        source_module: str,
        data: Dict[str, Any],
        priority: EventPriority = EventPriority.NORMAL,
        correlation_id: Optional[str] = None
    ) -> str:
        """
        Publish event to the bus

        Args:
            event_type: Type of event (e.g., "danger_detected")
            source_module: Module publishing the event
            data: Event payload
            priority: Event priority
            correlation_id: Optional ID for tracking related events

        Returns:
            event_id: Unique identifier for this event
        """
        # Create event
        event = Event(
            event_type=event_type,
            priority=priority,
            source_module=source_module,
            data=data,
            correlation_id=correlation_id
        )

        # Add to queue
        self.event_queue.put(event)
        self.total_events_published += 1

        if priority == EventPriority.CRITICAL:
            self.critical_events += 1
            logger.warning(
                f"CRITICAL event published: {event_type} from {source_module}"
            )

        logger.debug(
            f"Event published: {event_type} ({priority.name}) from {source_module}"
        )

        return event.event_id

    def subscribe(
        self,
        event_type: str,
        callback: Callable[[Event], None],
        subscriber_id: str,
        priority_filter: Optional[EventPriority] = None
    ) -> bool:
        """
        Subscribe to event type

        Args:
            event_type: Type to subscribe to (or "*" for all events)
            callback: Function to call when event occurs
            subscriber_id: Unique identifier for subscriber
            priority_filter: Only receive events at or above this priority

        Returns:
            True if subscribed successfully
        """
        try:
            with self.subscription_lock:
                subscription = Subscription(
                    event_type=event_type,
                    callback=callback,
                    subscriber_id=subscriber_id,
                    priority_filter=priority_filter
                )

                if event_type not in self.subscriptions:
                    self.subscriptions[event_type] = []

                self.subscriptions[event_type].append(subscription)

            logger.info(
                f"Subscription added: {subscriber_id} → {event_type} "
                f"(priority filter: {priority_filter.name if priority_filter else 'None'})"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to subscribe: {e}")
            return False

    def unsubscribe(
        self,
        event_type: str,
        subscriber_id: str
    ) -> bool:
        """
        Unsubscribe from event type

        Args:
            event_type: Event type to unsubscribe from
            subscriber_id: Subscriber identifier

        Returns:
            True if unsubscribed successfully
        """
        try:
            with self.subscription_lock:
                if event_type in self.subscriptions:
                    self.subscriptions[event_type] = [
                        sub for sub in self.subscriptions[event_type]
                        if sub.subscriber_id != subscriber_id
                    ]

                    # Remove event type if no more subscribers
                    if not self.subscriptions[event_type]:
                        del self.subscriptions[event_type]

            logger.info(f"Unsubscribed: {subscriber_id} from {event_type}")
            return True

        except Exception as e:
            logger.error(f"Failed to unsubscribe: {e}")
            return False

    def _process_queue(self):
        """Background thread - processes event queue"""
        while self.processing_active:
            try:
                # Get next event (blocks until available)
                event = self.event_queue.get(timeout=0.5)

                # Process it
                self._process_event(event)

                # Mark as done
                self.event_queue.task_done()
                self.total_events_processed += 1

            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Event processing error: {e}", exc_info=True)

    def _process_event(self, event: Event):
        """Process a single event - notify subscribers"""
        try:
            # Add to history
            with self.history_lock:
                self.event_history.append(event)
                if len(self.event_history) > self.max_history:
                    self.event_history.pop(0)

            # Get subscribers for this event type
            subscribers = []

            with self.subscription_lock:
                # Specific subscribers
                if event.event_type in self.subscriptions:
                    subscribers.extend(self.subscriptions[event.event_type])

                # Wildcard subscribers (subscribed to all events)
                if "*" in self.subscriptions:
                    subscribers.extend(self.subscriptions["*"])

            # Notify subscribers
            for subscription in subscribers:
                # Apply priority filter
                if subscription.priority_filter:
                    if event.priority.value > subscription.priority_filter.value:
                        continue  # Event priority too low, skip

                # Call subscriber callback
                try:
                    subscription.callback(event)
                except Exception as e:
                    logger.error(
                        f"Subscriber {subscription.subscriber_id} callback failed: {e}",
                        exc_info=True
                    )

            logger.debug(
                f"Event processed: {event.event_type} "
                f"({len(subscribers)} subscribers notified)"
            )

        except Exception as e:
            logger.error(f"Error processing event: {e}", exc_info=True)

    def get_event_history(
        self,
        event_type: Optional[str] = None,
        since: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Event]:
        """
        Get event history (for audit trail)

        Args:
            event_type: Filter by event type (None = all types)
            since: Filter by timestamp (None = all time)
            limit: Maximum events to return

        Returns:
            List of events matching filters
        """
        with self.history_lock:
            events = self.event_history.copy()

        # Apply filters
        if event_type:
            events = [e for e in events if e.event_type == event_type]

        if since:
            events = [e for e in events if e.timestamp >= since]

        # Sort by timestamp (most recent first)
        events.sort(key=lambda e: e.timestamp, reverse=True)

        # Limit
        return events[:limit]

    def get_statistics(self) -> Dict[str, Any]:
        """Get event bus statistics"""
        with self.subscription_lock:
            total_subscriptions = sum(
                len(subs) for subs in self.subscriptions.values()
            )
            subscription_breakdown = {
                event_type: len(subs)
                for event_type, subs in self.subscriptions.items()
            }

        return {
            "total_events_published": self.total_events_published,
            "total_events_processed": self.total_events_processed,
            "critical_events": self.critical_events,
            "queue_size": self.event_queue.qsize(),
            "total_subscriptions": total_subscriptions,
            "subscription_breakdown": subscription_breakdown,
            "history_size": len(self.event_history),
            "processing_active": self.processing_active
        }

    def shutdown(self):
        """Clean shutdown"""
        logger.info("Event Bus: Shutting down...")
        self.processing_active = False

        # Clear queue
        while not self.event_queue.empty():
            try:
                self.event_queue.get_nowait()
            except queue.Empty:
                break

        # Wait for processor thread
        if self.processor_thread:
            self.processor_thread.join(timeout=2.0)

        logger.info("Event Bus: Shutdown complete")


# Global singleton instance
_event_bus = None

def get_event_bus() -> SierraEventBus:
    """Get the singleton event bus instance"""
    global _event_bus
    if _event_bus is None:
        _event_bus = SierraEventBus()
    return _event_bus


# Convenience functions
def publish_event(
    event_type: str,
    source_module: str,
    data: Dict[str, Any],
    priority: EventPriority = EventPriority.NORMAL
) -> str:
    """Publish event to bus"""
    return get_event_bus().publish(event_type, source_module, data, priority)


def subscribe_to_event(
    event_type: str,
    callback: Callable[[Event], None],
    subscriber_id: str
) -> bool:
    """Subscribe to event"""
    return get_event_bus().subscribe(event_type, callback, subscriber_id)


# Test execution
if __name__ == "__main__":
    print("="*70)
    print("SIERRA EVENT BUS TEST")
    print("="*70)
    print()

    # Initialize bus
    bus = get_event_bus()

    # Define mock subscribers
    def on_danger_detected(event: Event):
        print(f"[Voice Cortex] Received: {event.event_type}")
        print(f"  Danger Level: {event.data.get('level')}")
        print(f"  → Speaking crisis message")

    def on_empathy_generated(event: Event):
        print(f"[Multimodal Output] Received: {event.event_type}")
        print(f"  Empathy: {event.data.get('validation')}")

    def on_any_event(event: Event):
        print(f"[Logger] {event.event_type} from {event.source_module} ({event.priority.name})")

    # Subscribe
    print("Subscribing modules...")
    bus.subscribe("danger_detected", on_danger_detected, "voice_cortex")
    bus.subscribe("empathy_generated", on_empathy_generated, "multimodal_output")
    bus.subscribe("*", on_any_event, "event_logger")  # Wildcard - all events
    print()

    # Publish events
    print("Test 1: Normal empathy event")
    bus.publish(
        event_type="empathy_generated",
        source_module="empathy_engine",
        data={"validation": "I hear you", "emotion": "fear"},
        priority=EventPriority.NORMAL
    )
    time.sleep(0.5)
    print()

    print("Test 2: High-priority danger event")
    bus.publish(
        event_type="danger_detected",
        source_module="behavioral_capture",
        data={"level": "HIGH", "confidence": 0.85},
        priority=EventPriority.HIGH
    )
    time.sleep(0.5)
    print()

    print("Test 3: CRITICAL crisis event")
    bus.publish(
        event_type="crisis_intervention",
        source_module="cortex_executive",
        data={"action": "call_911", "reason": "Immediate danger detected"},
        priority=EventPriority.CRITICAL
    )
    time.sleep(0.5)
    print()

    # Statistics
    print("="*70)
    print("EVENT BUS STATISTICS")
    print("="*70)
    stats = bus.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print()

    # Event history
    print("="*70)
    print("EVENT HISTORY")
    print("="*70)
    history = bus.get_event_history(limit=5)
    for event in history:
        print(f"  {event.timestamp.strftime('%H:%M:%S')} - "
              f"{event.event_type} ({event.priority.name}) "
              f"from {event.source_module}")
    print()

    print("✅ Event Bus test complete")
    print("📡 Pub/Sub communication ready")
    print("💜 Infrastructure for loose coupling at scale")

    # Cleanup
    bus.shutdown()


# ==============================================================================
# © 2025 Everett Nathaniel Christman
# The Christman AI Project — Luma Cognify AI
# All rights reserved. Unauthorized use, replication, or derivative training
# of this material is prohibited.
#
# Core Directive: "How can we help you love yourself more?"
# Autonomy & Alignment Protocol v3.0
# ==============================================================================
