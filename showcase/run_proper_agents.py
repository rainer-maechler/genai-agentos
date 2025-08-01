#!/usr/bin/env python3
"""
Run Proper GenAI AgentOS Agents

This script runs agents using the correct genai-session protocol.
These agents will show as ACTIVE (green borders) in the web interface.
"""

import subprocess
import sys
import time
import signal
import os
from pathlib import Path
from loguru import logger

class ProperAgentManager:
    """Manages proper GenAI AgentOS agents."""
    
    def __init__(self):
        self.agents_dir = Path(__file__).parent / "working_agents"
        self.agent_processes = []
        self.running = True
        
        # Proper agent files
        self.agents = [
            {
                "file": "document_analyzer_agent.py",
                "name": "Document Analyzer",
                "description": "Analyzes documents using proper GenAI protocol"
            },
            {
                "file": "sentiment_analyzer_agent.py", 
                "name": "Sentiment Analyzer",
                "description": "Performs sentiment analysis using proper GenAI protocol"
            },
            {
                "file": "report_generator_agent.py",
                "name": "Report Generator", 
                "description": "Generates reports using proper GenAI protocol"
            }
        ]
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info("\\n🛑 Shutdown signal received...")
        self.running = False
        self.stop_all_agents()
        sys.exit(0)
    
    def start_agent(self, agent_file: str, agent_name: str) -> subprocess.Popen:
        """Start a single agent."""
        agent_path = self.agents_dir / agent_file
        
        try:
            logger.info(f"📡 Starting {agent_name}...")
            
            # Set Python path to include local packages
            env = os.environ.copy()
            env['PYTHONPATH'] = f"/home/eramue/.local/lib/python3.10/site-packages:{env.get('PYTHONPATH', '')}"
            
            process = subprocess.Popen(
                [sys.executable, str(agent_path)],
                cwd=str(self.agents_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env
            )
            
            # Give it a moment to start
            time.sleep(3)
            
            # Check if still running
            if process.poll() is None:
                logger.info(f"✅ {agent_name} started successfully (PID: {process.pid})")
                return process
            else:
                stdout, stderr = process.communicate()
                logger.error(f"❌ {agent_name} failed to start")
                if stderr:
                    logger.error(f"Error: {stderr.decode()}")
                if stdout:
                    logger.info(f"Output: {stdout.decode()}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Failed to start {agent_name}: {str(e)}")
            return None
    
    def start_all_agents(self):
        """Start all proper agents."""
        logger.info("🚀 Starting GenAI AgentOS Proper Protocol Agents")
        logger.info("=" * 60)
        logger.info("📋 These agents use the official genai-session library")
        logger.info("🟢 They will show as ACTIVE (green borders) in web interface")
        logger.info("=" * 60)
        
        for agent in self.agents:
            process = self.start_agent(agent["file"], agent["name"])
            if process:
                self.agent_processes.append({
                    'process': process,
                    'name': agent["name"],
                    'file': agent["file"]
                })
        
        if self.agent_processes:
            logger.info("=" * 60)
            logger.info(f"✅ Started {len(self.agent_processes)} agents successfully")
            return True
        else:
            logger.error("❌ No agents started successfully")
            return False
    
    def stop_all_agents(self):
        """Stop all running agents."""
        logger.info("🛑 Stopping all agents...")
        
        for agent_info in self.agent_processes:
            try:
                process = agent_info['process']
                if process.poll() is None:
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                        logger.info(f"✅ Stopped {agent_info['name']}")
                    except subprocess.TimeoutExpired:
                        process.kill()
                        logger.warning(f"⚠️  Force killed {agent_info['name']}")
            except Exception as e:
                logger.error(f"❌ Error stopping {agent_info['name']}: {str(e)}")
        
        logger.info("🏁 All agents stopped")
    
    def monitor_agents(self):
        """Monitor running agents."""
        while self.running:
            time.sleep(5)
            
            # Check if any processes died
            for agent_info in self.agent_processes[:]:
                if agent_info['process'].poll() is not None:
                    logger.warning(f"⚠️  {agent_info['name']} stopped unexpectedly")
                    
                    # Try to restart
                    logger.info(f"🔄 Restarting {agent_info['name']}...")
                    new_process = self.start_agent(agent_info['file'], agent_info['name'])
                    
                    if new_process:
                        agent_info['process'] = new_process
                        logger.info(f"✅ {agent_info['name']} restarted successfully")
                    else:
                        self.agent_processes.remove(agent_info)
                        logger.error(f"❌ Failed to restart {agent_info['name']}")
            
            if not self.agent_processes:
                logger.error("❌ All agents stopped - shutting down")
                self.running = False
    
    def show_instructions(self):
        """Show web interface instructions."""
        logger.info("")
        logger.info("🌐 PROPER GENAI AGENTOS AGENTS RUNNING!")
        logger.info("=" * 60)
        logger.info("📍 STEP 1: Open your web browser and go to:")
        logger.info("   👉 http://localhost:3000/")
        logger.info("")
        logger.info("📍 STEP 2: Login with showcase credentials:")
        logger.info("   👤 Username: showcase")
        logger.info("   🔑 Password: Showcase123@")
        logger.info("")
        logger.info("📍 STEP 3: View Active Agents:")
        logger.info("   👉 http://localhost:3000/agents")
        logger.info("   ✅ You should see 3 agents with GREEN borders (ACTIVE)")
        logger.info("   🎯 These agents use the official genai-session protocol")
        logger.info("")
        logger.info("📍 STEP 4: Create Agent Flows:")
        logger.info("   👉 http://localhost:3000/agent-flows")
        logger.info("   1. Click 'Create New Flow'")
        logger.info("   2. Select agents from the active list")
        logger.info("   3. Design your processing pipeline")
        logger.info("   4. Execute the flow with real data")
        logger.info("")
        logger.info("🔬 PROTOCOL DETAILS:")
        logger.info("• Uses genai-session library (genai-protocol==1.0.9)")
        logger.info("• Proper WebSocket message format")
        logger.info("• JWT-based authentication")
        logger.info("• Function binding with @session.bind() decorator")
        logger.info("• Type annotations for parameters")
        logger.info("")
        logger.info("=" * 60)
        logger.info("🛑 TO STOP: Press Ctrl+C in this terminal")
        logger.info("")
    
    def run(self):
        """Run the proper agent manager."""
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Start agents
        if not self.start_all_agents():
            logger.error("❌ Failed to start agents")
            return
        
        # Show instructions
        self.show_instructions()
        
        # Monitor agents
        try:
            self.monitor_agents()
        except KeyboardInterrupt:
            logger.info("\\n🛑 Received keyboard interrupt")
        finally:
            self.stop_all_agents()

def main():
    """Main function."""
    try:
        manager = ProperAgentManager()
        manager.run()
    except Exception as e:
        logger.error(f"❌ Manager error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()