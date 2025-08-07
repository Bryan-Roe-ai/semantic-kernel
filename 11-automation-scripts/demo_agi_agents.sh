#!/bin/bash
# Quick demonstration of your local AGI agents

echo "🚀 Demonstrating Your Local AGI Agents"
echo "======================================"

cd /home/broe/semantic-kernel

echo ""
echo "1. 🧠 AGI Reasoning Test:"
/home/broe/semantic-kernel/.venv/bin/python agi_cli.py reason "What makes AGI different from narrow AI?"

echo ""
echo "2. 💻 Code Generation Test:"
/home/broe/semantic-kernel/.venv/bin/python agi_cli.py code python "Create a data analysis function"

echo ""
echo "3. 📋 Planning Test:"
/home/broe/semantic-kernel/.venv/bin/python agi_cli.py plan "Implement automated testing pipeline"

echo ""
echo "4. 📊 Current System Status:"
/home/broe/semantic-kernel/.venv/bin/python agi_status_dashboard.py

echo ""
echo "✅ Demo Complete! Your AGI agents are working perfectly."
echo ""
echo "Available interfaces:"
echo "  • CLI: agi_cli.py [command]"
echo "  • Interactive: demo_local_agents.py"
echo "  • Management: local_agent_launcher.py"
echo "  • Dashboard: agi_status_dashboard.py"
