#!/usr/bin/env python3
"""
Endless Improvement Loop Launcher
Simple launcher for the endless improvement system with different modes.
"""

import os
import sys
import asyncio
import argparse
from pathlib import Path

# Add the scripts directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from endless_improvement_loop import EndlessImprovementLoop

def main():
    """Main launcher function."""
    parser = argparse.ArgumentParser(
        description="Launch the Endless Improvement Loop",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launch_improvement.py --mode demo          # Run 3 demo cycles
  python launch_improvement.py --mode test          # Run 1 test cycle
  python launch_improvement.py --mode continuous    # Run endless loop
  python launch_improvement.py --mode fast          # 1-minute intervals
        """
    )

    parser.add_argument(
        "--mode",
        choices=["demo", "test", "continuous", "fast", "custom"],
        default="demo",
        help="Improvement loop mode (default: demo)"
    )

    parser.add_argument(
        "--workspace",
        type=str,
        default="/workspaces/semantic-kernel/ai-workspace",
        help="Path to workspace root"
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=300,
        help="Cycle interval in seconds (for custom mode)"
    )

    parser.add_argument(
        "--cycles",
        type=int,
        default=0,
        help="Number of cycles to run (for custom mode, 0 = endless)"
    )

    args = parser.parse_args()

    # Configure based on mode
    if args.mode == "demo":
        interval = 60  # 1 minute intervals for demo
        cycles = 3     # Run 3 cycles
        print("🎮 Demo Mode: Running 3 cycles with 1-minute intervals")

    elif args.mode == "test":
        interval = 30  # 30 second intervals for testing
        cycles = 1     # Run 1 cycle
        print("🧪 Test Mode: Running 1 cycle for testing")

    elif args.mode == "continuous":
        interval = 300  # 5 minute intervals
        cycles = 0      # Endless
        print("🔄 Continuous Mode: Running endless improvement loop")

    elif args.mode == "fast":
        interval = 60   # 1 minute intervals
        cycles = 0      # Endless
        print("⚡ Fast Mode: Running with 1-minute intervals")

    else:  # custom mode
        interval = args.interval
        cycles = args.cycles
        print(f"⚙️  Custom Mode: {cycles if cycles > 0 else 'Endless'} cycles, {interval}s intervals")

    # Create and run the improvement loop
    loop = EndlessImprovementLoop(args.workspace)

    async def run_improvement():
        """Run the improvement loop."""
        try:
            if cycles > 0:
                print(f"🏁 Starting {cycles} improvement cycles...")
                for i in range(cycles):
                    print(f"\n🔄 Starting cycle {i+1}/{cycles}")
                    await loop._run_improvement_cycle()

                    if i < cycles - 1:  # Don't wait after last cycle
                        print(f"⏳ Waiting {interval} seconds until next cycle...")
                        await asyncio.sleep(interval)

                await loop._save_final_report()
                print(f"\n🎉 Completed {cycles} improvement cycles!")

            else:
                print("🚀 Starting endless improvement loop...")
                await loop.start_endless_loop(interval)

        except KeyboardInterrupt:
            print("\n🛑 Improvement loop stopped by user")
            await loop._save_final_report()
        except Exception as e:
            print(f"\n❌ Error in improvement loop: {e}")
            await loop._save_final_report()

    # Show startup information
    print("🤖 Endless Improvement Loop")
    print("=" * 50)
    print(f"📁 Workspace: {args.workspace}")
    print(f"⏰ Interval: {interval} seconds")
    print(f"🔄 Cycles: {'Endless' if cycles == 0 else cycles}")
    print(f"🎯 Mode: {args.mode}")
    print("\n🚀 Starting in 3 seconds...")
    print("   Press Ctrl+C to stop at any time")

    # Countdown
    import time
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)

    print("\n🎬 Action!")

    # Run the improvement loop
    try:
        asyncio.run(run_improvement())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()
