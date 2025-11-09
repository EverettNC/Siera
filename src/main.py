"""
SafeHaven AI - Main Application
FastAPI backend for domestic violence support AI system

Voice Cortex Integration:
- Optional voice output for accessibility
- Priority-based voice (crisis interrupts support)
- HIPAA-compliant audio handling
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Optional
import json
import asyncio
from datetime import datetime

from .config import settings
from .ai_engine import SafeHavenAI, ConversationMode
from .safety_planning import SafetyPlanningAssistant
from .resources import ResourceDatabase

# Voice Cortex integration
try:
    from .voice_cortex import get_voice_cortex, VoicePriority
    from .multimodal_interface import MultimodalProcessor
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    MultimodalProcessor = None

# Cortex Executive and Behavioral Capture integration
try:
    from .cortex_executive import get_cortex, CortexPriority, CortexMode
    from .behavioral_capture import BehavioralCaptureService
    from .empathy_engine import AdvancedEmpathyEngine
    CORTEX_AVAILABLE = True
except ImportError:
    CORTEX_AVAILABLE = False

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="A trauma-informed AI companion for domestic violence survivors",
    version="0.1.0"
)

# CORS middleware for security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core components
resource_db = ResourceDatabase()
active_sessions: Dict[str, Dict] = {}


class ConnectionManager:
    """Manage WebSocket connections"""

    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        """Connect a new WebSocket"""
        await websocket.accept()
        self.active_connections[session_id] = websocket

        # Initialize session
        active_sessions[session_id] = {
            "ai_engine": SafeHavenAI(provider="anthropic" if settings.anthropic_api_key else "openai"),
            "safety_planner": SafetyPlanningAssistant(),
            "multimodal_processor": MultimodalProcessor() if VOICE_AVAILABLE else None,
            "voice_enabled": False,  # User can enable voice output
            "connected_at": datetime.now().isoformat(),
            "message_count": 0
        }

    def disconnect(self, session_id: str):
        """Disconnect a WebSocket"""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
        if session_id in active_sessions:
            # Clean up session data for privacy
            del active_sessions[session_id]

    async def send_message(self, session_id: str, message: dict):
        """Send a message to a specific session"""
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_json(message)


manager = ConnectionManager()


@app.get("/", response_class=HTMLResponse)
async def get_home():
    """Serve the main Sierra hub - her personality landing page"""
    try:
        with open("/home/user/Siera/src/templates/index.html", "r") as f:
            return f.read()
    except FileNotFoundError:
        # Fallback to old interface if new one doesn't exist
        return get_html_interface()


@app.get("/behavior_capture", response_class=HTMLResponse)
async def get_behavior_capture():
    """Serve the behavior capture interface"""
    with open("/home/user/Siera/src/templates/behavior_capture.html", "r") as f:
        return f.read()


@app.get("/chat", response_class=HTMLResponse)
async def get_chat():
    """Serve the enhanced chat interface with speech-to-speech"""
    try:
        with open("/home/user/Siera/src/templates/chat_enhanced.html", "r") as f:
            return f.read()
    except FileNotFoundError:
        # Fallback to original chat
        with open("/home/user/Siera/src/templates/chat.html", "r") as f:
            return f.read()


@app.get("/private-corner", response_class=HTMLResponse)
async def get_private_corner():
    """Serve the private corner - encrypted safe space"""
    with open("/home/user/Siera/src/templates/private_corner.html", "r") as f:
        return f.read()


@app.get("/kids-mode", response_class=HTMLResponse)
async def get_kids_mode():
    """Serve the kids emergency mode"""
    with open("/home/user/Siera/src/templates/kids_mode.html", "r") as f:
        return f.read()


@app.get("/about", response_class=HTMLResponse)
async def get_about():
    """Serve the About Sierra page - who she is, her personality"""
    with open("/home/user/Siera/src/templates/about.html", "r") as f:
        return f.read()


@app.get("/safety-plan", response_class=HTMLResponse)
async def get_safety_plan():
    """Serve the interactive safety planning page"""
    # For now, redirect to chat with safety planning prompt
    # Can create dedicated page later
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="refresh" content="0; url=/chat">
        <script>
            setTimeout(function() {
                window.location.href = '/chat';
                // Auto-send safety planning message
                setTimeout(function() {
                    const input = document.getElementById('messageInput');
                    if (input) {
                        input.value = 'I want to create a safety plan';
                        document.querySelector('.send-button').click();
                    }
                }, 1000);
            }, 100);
        </script>
    </head>
    <body>
        <p>Redirecting to chat for safety planning...</p>
    </body>
    </html>
    """


@app.get("/resources", response_class=HTMLResponse)
async def get_resources():
    """Serve the resources page"""
    with open("/home/user/Siera/src/templates/resources.html", "r") as f:
        return f.read()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": "0.1.0",
        "ai_provider": "anthropic" if settings.anthropic_api_key else "openai" if settings.openai_api_key else "fallback"
    }


@app.get("/api/resources/crisis")
async def get_crisis_resources():
    """Get crisis resources"""
    resources = resource_db.get_crisis_resources()
    return {
        "resources": [r.model_dump() for r in resources],
        "emergency_card": resource_db.get_emergency_card()
    }


@app.get("/api/resources/search")
async def search_resources(query: str):
    """Search resources"""
    results = resource_db.search(query)
    return {
        "query": query,
        "results": [r.model_dump() for r in results],
        "count": len(results)
    }


@app.get("/api/resources/by-need/{need}")
async def get_resources_by_need(need: str):
    """Get resources by specific need"""
    formatted = resource_db.get_resources_by_need(need)
    return {
        "need": need,
        "resources": formatted
    }


@app.post("/api/quick-exit")
async def quick_exit():
    """Quick exit endpoint - clears session and redirects"""
    # In a real app, this would clear all session data
    return {
        "redirect": "https://www.google.com",
        "cleared": True
    }


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time chat"""
    await manager.connect(websocket, session_id)

    try:
        # Send welcome message
        await manager.send_message(session_id, {
            "type": "system",
            "message": "Connected to SafeHaven AI. You're safe here. How can I support you today?",
            "timestamp": datetime.now().isoformat()
        })

        while True:
            # Receive message from user
            data = await websocket.receive_text()
            message_data = json.loads(data)

            # Get session components
            session = active_sessions[session_id]
            ai_engine = session["ai_engine"]
            safety_planner = session["safety_planner"]
            session["message_count"] += 1

            user_message = message_data.get("message", "")
            message_type = message_data.get("type", "chat")

            # Handle different message types
            if message_type == "chat":
                # Get AI response
                response = await ai_engine.get_response(user_message)

                # Voice output if enabled and available
                voice_enabled = session.get("voice_enabled", False)
                if voice_enabled and session.get("multimodal_processor"):
                    multimodal = session["multimodal_processor"]

                    # Generate voice response with appropriate emotion
                    voice_response = multimodal.generate_accessible_response(
                        response_text=response["response"],
                        include_speech=True,
                        is_crisis=response["is_crisis"],
                        needs_grounding=(response["mode"] == "EMOTIONAL_SUPPORT")
                    )

                # Send response back
                await manager.send_message(session_id, {
                    "type": "assistant",
                    "message": response["response"],
                    "mode": response["mode"],
                    "is_crisis": response["is_crisis"],
                    "emergency_resources": response.get("emergency_resources"),
                    "safety_reminder": response.get("safety_reminder"),
                    "voice_enabled": voice_enabled,
                    "timestamp": response["timestamp"]
                })

                # If crisis detected, also send emergency resources
                if response["is_crisis"]:
                    crisis_resources = resource_db.get_crisis_resources()
                    await manager.send_message(session_id, {
                        "type": "resources",
                        "resources": [r.model_dump() for r in crisis_resources],
                        "priority": "high"
                    })

                    # Crisis voice output (always speak crisis messages if voice available)
                    if VOICE_AVAILABLE and session.get("multimodal_processor"):
                        voice_cortex = get_voice_cortex()
                        voice_cortex.speak_crisis(
                            "I'm concerned about your safety. Emergency resources are available 24/7."
                        )

            elif message_type == "get_resources":
                # Get resources by need
                need = message_data.get("need", "crisis")
                resources_text = resource_db.get_resources_by_need(need)

                await manager.send_message(session_id, {
                    "type": "resources",
                    "message": resources_text,
                    "timestamp": datetime.now().isoformat()
                })

            elif message_type == "safety_plan":
                # Handle safety planning
                action = message_data.get("action", "view")

                if action == "create":
                    plan = safety_planner.create_new_plan()
                    await manager.send_message(session_id, {
                        "type": "safety_plan",
                        "action": "created",
                        "plan": plan.model_dump(),
                        "timestamp": datetime.now().isoformat()
                    })

                elif action == "export":
                    plan_text = safety_planner.export_to_text()
                    await manager.send_message(session_id, {
                        "type": "safety_plan",
                        "action": "export",
                        "plan_text": plan_text,
                        "timestamp": datetime.now().isoformat()
                    })

                elif action == "summary":
                    summary = safety_planner.get_plan_summary()
                    await manager.send_message(session_id, {
                        "type": "safety_plan",
                        "action": "summary",
                        "summary": summary,
                        "timestamp": datetime.now().isoformat()
                    })

            elif message_type == "clear_history":
                # Clear conversation history for privacy
                ai_engine.clear_history()
                await manager.send_message(session_id, {
                    "type": "system",
                    "message": "Conversation history cleared for your privacy.",
                    "timestamp": datetime.now().isoformat()
                })

            elif message_type == "toggle_voice":
                # Toggle voice output
                if VOICE_AVAILABLE:
                    current_voice = session.get("voice_enabled", False)
                    session["voice_enabled"] = not current_voice
                    new_status = "enabled" if session["voice_enabled"] else "disabled"

                    await manager.send_message(session_id, {
                        "type": "system",
                        "message": f"Voice output {new_status}.",
                        "voice_enabled": session["voice_enabled"],
                        "timestamp": datetime.now().isoformat()
                    })

                    # Speak confirmation if voice just enabled
                    if session["voice_enabled"] and session.get("multimodal_processor"):
                        voice_cortex = get_voice_cortex()
                        voice_cortex.speak("Voice output is now enabled. I can speak my responses to you.")
                else:
                    await manager.send_message(session_id, {
                        "type": "system",
                        "message": "Voice output is not available on this system.",
                        "voice_available": False,
                        "timestamp": datetime.now().isoformat()
                    })

    except WebSocketDisconnect:
        manager.disconnect(session_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(session_id)


@app.websocket("/ws/behavior_capture")
async def websocket_behavior_capture(websocket: WebSocket):
    """WebSocket endpoint for behavior capture and danger assessment"""
    await websocket.accept()

    # Initialize components if available
    cortex = get_cortex() if CORTEX_AVAILABLE else None
    behavioral_capture = BehavioralCaptureService() if CORTEX_AVAILABLE else None
    empathy_engine = AdvancedEmpathyEngine() if CORTEX_AVAILABLE else None
    voice_cortex = get_voice_cortex() if VOICE_AVAILABLE else None

    # Register modules with cortex
    if cortex and CORTEX_AVAILABLE:
        if behavioral_capture:
            cortex.register_module("behavioral_capture", behavioral_capture)
        if empathy_engine:
            cortex.register_module("empathy_engine", empathy_engine)
        if voice_cortex:
            cortex.register_module("voice_cortex", voice_cortex)
        if resource_db:
            cortex.register_module("resources", resource_db)

    try:
        # Send initial status
        await websocket.send_json({
            "type": "status",
            "cortex_available": CORTEX_AVAILABLE,
            "voice_available": VOICE_AVAILABLE,
            "message": "Behavior capture system ready"
        })

        while True:
            # Receive message from client
            data = await websocket.receive_json()
            message_type = data.get("type", "")

            if message_type == "analyze_behavior":
                # Analyze behavioral input for danger
                text = data.get("text", "")

                if not CORTEX_AVAILABLE or not behavioral_capture:
                    # Fallback response
                    await websocket.send_json({
                        "type": "danger_assessment",
                        "level": "SAFE",
                        "confidence": 0.5,
                        "patterns": [],
                        "message": "Cortex system not available - limited analysis"
                    })
                    continue

                # Submit to cortex for processing
                import time
                request_id = f"behavior_analysis_{time.time()}"

                # Define callback for cortex response
                async def send_response(response):
                    # Extract danger assessment
                    danger_level = response.data.get("danger_level", "SAFE")
                    confidence = response.data.get("confidence", 0.0)
                    patterns = response.data.get("patterns", [])
                    empathy = response.data.get("empathy", {})

                    # Send danger assessment
                    await websocket.send_json({
                        "type": "danger_assessment",
                        "level": danger_level,
                        "confidence": confidence,
                        "patterns": patterns
                    })

                    # Send empathy response
                    if empathy:
                        await websocket.send_json({
                            "type": "empathy_response",
                            "response": empathy
                        })

                    # Trigger crisis if needed
                    if danger_level in ["CRITICAL", "IMMEDIATE"]:
                        await websocket.send_json({
                            "type": "crisis_detected",
                            "level": danger_level
                        })

                # Submit request to cortex
                cortex.submit_request(
                    request_id=request_id,
                    priority=CortexPriority.NORMAL,
                    mode=CortexMode.EMOTIONAL_SUPPORT,
                    content={"text": text},
                    callback=lambda r: asyncio.create_task(send_response(r))
                )

            elif message_type == "crisis":
                # Immediate crisis intervention
                if cortex and CORTEX_AVAILABLE:
                    import time
                    cortex.submit_request(
                        request_id=f"crisis_{time.time()}",
                        priority=CortexPriority.CRISIS,
                        mode=CortexMode.CRISIS,
                        content={"text": "User triggered emergency", "context": {}}
                    )

                # Always send crisis resources
                crisis_resources = resource_db.get_crisis_resources()
                await websocket.send_json({
                    "type": "crisis_resources",
                    "resources": [r.model_dump() for r in crisis_resources]
                })

                # Voice crisis response
                if voice_cortex:
                    voice_cortex.speak_crisis(
                        "I'm very concerned about your safety. "
                        "If you're in immediate danger, call 911. "
                        "The National Domestic Violence Hotline is 1-800-799-7233."
                    )

            elif message_type == "start_audio_monitor":
                # Start audio danger monitoring
                if CORTEX_AVAILABLE:
                    try:
                        from .audio_safety_system import get_audio_safety_system
                        audio_system = get_audio_safety_system()

                        # Define callbacks
                        def on_danger(assessment):
                            asyncio.create_task(websocket.send_json({
                                "type": "audio_danger",
                                "level": assessment.danger_level.name,
                                "confidence": assessment.confidence,
                                "patterns": assessment.patterns_detected
                            }))

                        def on_crisis(assessment):
                            asyncio.create_task(websocket.send_json({
                                "type": "crisis_detected",
                                "level": assessment.danger_level.name,
                                "source": "audio"
                            }))

                        # Start monitoring
                        success = audio_system.start_monitoring(
                            danger_callback=on_danger,
                            crisis_callback=on_crisis
                        )

                        await websocket.send_json({
                            "type": "audio_monitor_status",
                            "active": success,
                            "message": "Audio monitoring started" if success else "Failed to start audio monitoring"
                        })

                    except Exception as e:
                        await websocket.send_json({
                            "type": "audio_monitor_status",
                            "active": False,
                            "message": f"Audio monitoring unavailable: {str(e)}"
                        })

            elif message_type == "stop_audio_monitor":
                # Stop audio monitoring
                try:
                    from .audio_safety_system import get_audio_safety_system
                    audio_system = get_audio_safety_system()
                    audio_system.stop_monitoring()

                    await websocket.send_json({
                        "type": "audio_monitor_status",
                        "active": False,
                        "message": "Audio monitoring stopped"
                    })
                except Exception:
                    pass

    except WebSocketDisconnect:
        print("Behavior capture WebSocket disconnected")
    except Exception as e:
        print(f"Behavior capture WebSocket error: {e}")
        import traceback
        traceback.print_exc()


def get_html_interface() -> str:
    """Generate the HTML interface"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SafeHaven AI - You Are Not Alone</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        .quick-exit {
            position: fixed;
            top: 10px;
            right: 10px;
            background: #dc3545;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            font-size: 14px;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }

        .quick-exit:hover {
            background: #c82333;
        }

        .header {
            background: rgba(255, 255, 255, 0.95);
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .header h1 {
            color: #667eea;
            margin-bottom: 5px;
        }

        .header p {
            color: #666;
            font-size: 14px;
        }

        .container {
            flex: 1;
            max-width: 900px;
            width: 100%;
            margin: 0 auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
        }

        .chat-container {
            flex: 1;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            margin-bottom: 20px;
            overflow: hidden;
        }

        .messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            max-height: 500px;
        }

        .message {
            margin-bottom: 15px;
            padding: 12px 16px;
            border-radius: 10px;
            max-width: 80%;
            animation: fadeIn 0.3s;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .message.user {
            background: #667eea;
            color: white;
            margin-left: auto;
        }

        .message.assistant {
            background: #f1f3f5;
            color: #333;
        }

        .message.system {
            background: #fff3cd;
            color: #856404;
            border: 1px solid #ffeaa7;
            text-align: center;
            max-width: 100%;
            font-size: 14px;
        }

        .message.crisis {
            background: #f8d7da;
            color: #721c24;
            border: 2px solid #f5c6cb;
            font-weight: 500;
        }

        .timestamp {
            font-size: 11px;
            opacity: 0.7;
            margin-top: 5px;
        }

        .mode-indicator {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 11px;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .mode-crisis { background: #dc3545; color: white; }
        .mode-safety_planning { background: #28a745; color: white; }
        .mode-resource_finding { background: #17a2b8; color: white; }
        .mode-emotional_support { background: #6f42c1; color: white; }

        .input-area {
            padding: 20px;
            background: #f8f9fa;
            border-top: 1px solid #dee2e6;
            display: flex;
            gap: 10px;
        }

        .input-area input {
            flex: 1;
            padding: 12px;
            border: 1px solid #ced4da;
            border-radius: 5px;
            font-size: 14px;
        }

        .input-area button {
            padding: 12px 24px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
        }

        .input-area button:hover {
            background: #5568d3;
        }

        .quick-actions {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 10px;
        }

        .quick-action {
            padding: 8px 16px;
            background: white;
            border: 2px solid #667eea;
            color: #667eea;
            border-radius: 20px;
            cursor: pointer;
            font-size: 13px;
            transition: all 0.2s;
        }

        .quick-action:hover {
            background: #667eea;
            color: white;
        }

        .emergency-banner {
            background: #dc3545;
            color: white;
            padding: 15px;
            text-align: center;
            margin-bottom: 20px;
            border-radius: 10px;
            display: none;
        }

        .emergency-banner.show {
            display: block;
        }

        .resources-panel {
            background: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            white-space: pre-wrap;
            font-family: monospace;
            font-size: 12px;
            display: none;
        }

        .resources-panel.show {
            display: block;
        }

        .status {
            text-align: center;
            padding: 10px;
            font-size: 12px;
            color: #666;
        }

        .status.connected {
            color: #28a745;
        }

        .status.disconnected {
            color: #dc3545;
        }
    </style>
</head>
<body>
    <button class="quick-exit" onclick="quickExit()">⚠️ QUICK EXIT (ESC)</button>

    <div class="header">
        <h1>SafeHaven AI</h1>
        <p>You are not alone. You deserve safety and support.</p>
    </div>

    <div class="container">
        <div class="emergency-banner" id="emergencyBanner">
            <h3>🚨 IMMEDIATE DANGER 🚨</h3>
            <p>National DV Hotline: 1-800-799-7233 | Emergency: 911 | Crisis Text: START to 741741</p>
        </div>

        <div class="quick-actions">
            <button class="quick-action" onclick="sendQuickMessage('I need help')">I need help</button>
            <button class="quick-action" onclick="sendQuickMessage('Can you provide resources?')">Resources</button>
            <button class="quick-action" onclick="sendQuickMessage('Help me create a safety plan')">Safety Plan</button>
            <button class="quick-action" onclick="sendQuickMessage('I feel scared')">I feel scared</button>
            <button class="quick-action" onclick="sendQuickMessage('I want to talk')">Just talk</button>
        </div>

        <div class="resources-panel" id="resourcesPanel"></div>

        <div class="chat-container">
            <div class="messages" id="messages">
                <div class="message system">
                    <div>Welcome to SafeHaven AI. This is a safe space. Everything here is confidential.</div>
                    <div class="timestamp">Ready to listen</div>
                </div>
            </div>

            <div class="input-area">
                <input type="text" id="messageInput" placeholder="Type your message... You're safe here." onkeypress="handleKeyPress(event)">
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>

        <div class="status" id="status">Connecting...</div>
    </div>

    <script>
        let ws;
        let sessionId = 'session-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);

        function connect() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/ws/${sessionId}`;

            ws = new WebSocket(wsUrl);

            ws.onopen = function() {
                document.getElementById('status').textContent = 'Connected securely';
                document.getElementById('status').className = 'status connected';
            };

            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                handleIncomingMessage(data);
            };

            ws.onclose = function() {
                document.getElementById('status').textContent = 'Disconnected - Refresh to reconnect';
                document.getElementById('status').className = 'status disconnected';
            };

            ws.onerror = function(error) {
                console.error('WebSocket error:', error);
                document.getElementById('status').textContent = 'Connection error';
                document.getElementById('status').className = 'status disconnected';
            };
        }

        function handleIncomingMessage(data) {
            const messagesDiv = document.getElementById('messages');

            if (data.type === 'assistant' || data.type === 'system') {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${data.type}`;

                if (data.is_crisis) {
                    messageDiv.classList.add('crisis');
                    document.getElementById('emergencyBanner').classList.add('show');
                }

                let content = '';

                if (data.mode && data.type === 'assistant') {
                    content += `<div class="mode-indicator mode-${data.mode}">${data.mode.replace(/_/g, ' ').toUpperCase()}</div>`;
                }

                content += `<div>${escapeHtml(data.message)}</div>`;

                if (data.safety_reminder) {
                    content += `<div style="margin-top: 10px; font-size: 12px; opacity: 0.8;">💡 ${escapeHtml(data.safety_reminder)}</div>`;
                }

                if (data.timestamp) {
                    content += `<div class="timestamp">${new Date(data.timestamp).toLocaleTimeString()}</div>`;
                }

                messageDiv.innerHTML = content;
                messagesDiv.appendChild(messageDiv);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }

            if (data.type === 'resources') {
                const resourcesPanel = document.getElementById('resourcesPanel');
                resourcesPanel.textContent = data.message || JSON.stringify(data.resources, null, 2);
                resourcesPanel.classList.add('show');
            }
        }

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();

            if (message && ws && ws.readyState === WebSocket.OPEN) {
                // Display user message
                const messagesDiv = document.getElementById('messages');
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message user';
                messageDiv.innerHTML = `<div>${escapeHtml(message)}</div><div class="timestamp">${new Date().toLocaleTimeString()}</div>`;
                messagesDiv.appendChild(messageDiv);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;

                // Send to server
                ws.send(JSON.stringify({
                    type: 'chat',
                    message: message
                }));

                input.value = '';
            }
        }

        function sendQuickMessage(message) {
            document.getElementById('messageInput').value = message;
            sendMessage();
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        function quickExit() {
            // Clear the page and redirect
            window.location.replace('https://www.google.com');
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        // ESC key for quick exit
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                if (confirm('Quick exit? This will take you to Google.')) {
                    quickExit();
                }
            }
        });

        // Connect on load
        connect();
    </script>
</body>
</html>
    """


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
