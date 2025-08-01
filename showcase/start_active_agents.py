#!/usr/bin/env python3
"""
Start Active Showcase Agents

This script starts all the showcase agents so they show as active (green) in the web interface.
"""

import subprocess
import sys
import time
from pathlib import Path
from loguru import logger

def start_agents():
    """Start all showcase agents in background."""
    
    agents_dir = Path(__file__).parent / "active_agents"
    
    agents = [
        "simple_document_analyzer.py",
        "simple_report_generator.py", 
        "simple_sentiment_analyzer.py"
    ]
    
    processes = []
    
    logger.info("🚀 Starting GenAI AgentOS Showcase Agents")
    logger.info("=" * 50)
    
    for agent_file in agents:
        agent_path = agents_dir / agent_file
        agent_name = agent_file.replace("simple_", "").replace(".py", "")
        
        try:
            logger.info(f"📡 Starting {agent_name}...")
            
            # Start agent in background
            process = subprocess.Popen(
                [sys.executable, str(agent_path)],
                cwd=str(agents_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            processes.append({
                'process': process,
                'name': agent_name,
                'file': agent_file
            })
            
            # Give it a moment to start
            time.sleep(2)
            
            # Check if still running
            if process.poll() is None:
                logger.info(f"✅ {agent_name} started successfully (PID: {process.pid})")
            else:
                stdout, stderr = process.communicate()
                logger.error(f"❌ {agent_name} failed to start")
                if stderr:
                    logger.error(f"Error: {stderr.decode()[:200]}")
                    
        except Exception as e:
            logger.error(f"❌ Failed to start {agent_name}: {str(e)}")
    
    logger.info("=" * 50)
    
    if processes:
        logger.info(f"✅ Started {len(processes)} agents")
        logger.info("")
        logger.info("🌐 Check the web interface:")
        logger.info("1. Go to: http://localhost:3000/agents")
        logger.info("2. Agents should now show as ACTIVE (green border)")
        logger.info("3. You can create flows at: http://localhost:3000/agent-flows")
        logger.info("")
        logger.info("🛑 To stop agents: Press Ctrl+C")
        
        try:
            # Wait for keyboard interrupt
            while True:
                time.sleep(1)
                # Check if any processes died
                for agent_info in processes[:]:
                    if agent_info['process'].poll() is not None:
                        logger.warning(f"⚠️  {agent_info['name']} stopped unexpectedly")
                        processes.remove(agent_info)
                
                if not processes:
                    logger.error("❌ All agents stopped")
                    break
                    
        except KeyboardInterrupt:
            logger.info("\n🛑 Stopping all agents...")
            
            for agent_info in processes:
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
    
    else:
        logger.error("❌ No agents started successfully")

if __name__ == "__main__":
    start_agents()