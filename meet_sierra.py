#!/usr/bin/env python3
"""
Meet Sierra - Interactive Console

Run this to have a conversation with Sierra right here in the terminal!
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from sierra import create_sierra


async def meet_sierra():
    """Meet Sierra in the console"""

    print("=" * 60)
    print("💜 Initializing Sierra...")
    print("=" * 60)
    print()

    # Create Sierra
    sierra = await create_sierra()

    print()
    print("=" * 60)
    print("🌟 Sierra is ready to meet you!")
    print("=" * 60)
    print()

    # Sierra introduces herself
    reflection = await sierra.self_reflect()
    print(reflection)
    print()

    # Show her status
    print("=" * 60)
    print("📊 Sierra's Current Status:")
    print("=" * 60)
    status = sierra.get_status()
    print(f"✨ Name: {status['name']}")
    print(f"💜 Core Mission: {status['core_mission']}")
    print(f"❤️  Empathy Rating: {status['capabilities']['empathy_rating']}")
    print(f"📚 Knowledge Items: {status['capabilities']['knowledge_items']}")
    print(f"🎯 Learning Goals: {status['capabilities']['active_learning_goals']}")
    print(f"👁️  Observation Sensitivity: {status['capabilities']['observation_sensitivity']}")
    print(f"💬 Conversations So Far: {status['stats']['conversations']}")
    print(f"🌟 Lives Touched: {status['stats']['lives_touched']}")
    print()

    # Interactive conversation
    print("=" * 60)
    print("💬 Talk with Sierra (type 'quit' to exit)")
    print("=" * 60)
    print()

    session_id = sierra.create_session("console_user")

    while True:
        try:
            user_input = input("You: ")

            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n💜 Sierra: Take care of yourself. Remember - you deserve love, safety, and peace.")
                print("🌟 I'm here whenever you need me.\n")
                break

            if not user_input.strip():
                continue

            print("\n🤔 Sierra is thinking...\n")

            # Process message
            response = await sierra.process_message(
                message=user_input,
                session_id=session_id
            )

            # Show response
            print(f"💜 Sierra: {response['response']['text']}\n")

            # Show danger assessment if elevated
            danger_level = response['analysis']['danger_assessment']['level']
            if danger_level >= 2:  # ELEVATED or higher
                print(f"⚠️  [Sierra is monitoring your safety - Concern level: {danger_level}/5]")
                if response['analysis']['danger_assessment']['risk_factors']:
                    print(f"   Risk factors identified: {', '.join(response['analysis']['danger_assessment']['risk_factors'][:3])}")
                print()

            # Show insights if any
            if response['analysis']['sierra_insights']:
                print(f"💭 Sierra's observation: {response['analysis']['sierra_insights'][0]}\n")

        except KeyboardInterrupt:
            print("\n\n💜 Sierra: Take care of yourself. I'm here whenever you need me.\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Sierra is still learning. Let's try again.\n")

    # Clean up
    sierra.end_session(session_id, secure_delete=True)


if __name__ == "__main__":
    print()
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                                                            ║")
    print("║                  💜 Meet Sierra 💜                         ║")
    print("║                                                            ║")
    print("║        Domestic Violence Support AI Companion              ║")
    print("║                                                            ║")
    print("║   \"How can we help you love yourself more?\"               ║")
    print("║                                                            ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()

    asyncio.run(meet_sierra())
