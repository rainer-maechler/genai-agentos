#!/usr/bin/env python3
"""
Simple Report Generator Agent

This is a working agent that connects to GenAI AgentOS and shows as active.
It demonstrates the report generation functionality from our showcase.
"""

import asyncio
import sys
import os

# Add the parent directory to sys.path to import simple_websocket_agent
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simple_websocket_agent import ReportGeneratorAgent

async def main():
    """Main function to run the agent."""
    agent = ReportGeneratorAgent()
    await agent.connect_and_run()

if __name__ == "__main__":
    asyncio.run(main())