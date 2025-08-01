#!/usr/bin/env python3
"""
Deploy Showcase Agents Script

This script deploys all the showcase agents to the GenAI AgentOS system using the CLI tools.
It registers agents via the backend API and starts them using the standard deployment process.
"""

import asyncio
import sys
import time
from pathlib import Path
from typing import List, Dict, Any
import requests
import json
import subprocess
import os
from loguru import logger

# Configuration
BACKEND_URL = os.getenv("CLI_BACKEND_ORIGIN_URL", "http://localhost:8000")
AGENT_DIR = Path(__file__).parent / "agents"

# Showcase agents configuration
SHOWCASE_AGENTS = [
    {
        "name": "document_parser",
        "description": "Handles various document formats and extracts raw content with OCR support",
        "file": "document_parser.py",
        "capabilities": ["PDF processing", "OCR", "metadata extraction", "multi-format support"]
    },
    {
        "name": "text_extractor", 
        "description": "Cleans and structures extracted text with entity recognition",
        "file": "text_extractor.py",
        "capabilities": ["text normalization", "language detection", "entity extraction", "section identification"]
    },
    {
        "name": "analytics_agent",
        "description": "Performs deep content analysis, risk assessment, and business intelligence",
        "file": "analytics_agent.py", 
        "capabilities": ["topic analysis", "risk detection", "compliance checking", "business metrics"]
    },
    {
        "name": "sentiment_analyzer",
        "description": "Analyzes emotional tone and sentiment with confidence scoring",
        "file": "sentiment_analyzer.py",
        "capabilities": ["sentiment scoring", "emotion classification", "context analysis", "confidence metrics"]
    },
    {
        "name": "report_generator",
        "description": "Generates formatted reports, visualizations, and executive summaries", 
        "file": "report_generator.py",
        "capabilities": ["report generation", "data visualization", "executive summaries", "multi-format export"]
    }
]

class ShowcaseDeployer:
    """Handles deployment of showcase agents using GenAI AgentOS CLI."""
    
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.agent_dir = AGENT_DIR
        self.cli_path = Path(__file__).parent.parent / "cli" / "cli.py"
        
    def check_prerequisites(self) -> bool:
        """Check if all prerequisites are met."""
        logger.info("Checking deployment prerequisites...")
        
        # Check if backend is running
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            if response.status_code != 200:
                logger.error("❌ Backend is not healthy. Please start with 'make up'")
                return False
            logger.info("✅ Backend is running")
        except Exception as e:
            logger.error(f"❌ Cannot connect to backend at {self.backend_url}: {str(e)}")
            logger.error("Please start the infrastructure with 'make up'")
            return False
        
        # Check if CLI exists
        if not self.cli_path.exists():
            logger.error(f"❌ CLI not found at {self.cli_path}")
            return False
        logger.info("✅ CLI found")
        
        # Check if agent files exist
        missing_agents = []
        for agent in SHOWCASE_AGENTS:
            agent_file = self.agent_dir / agent["file"]
            if not agent_file.exists():
                missing_agents.append(agent["file"])
        
        if missing_agents:
            logger.error(f"❌ Missing agent files: {', '.join(missing_agents)}")
            return False
        logger.info("✅ All agent files found")
        
        # Check if requirements are installed
        try:
            import genai_protocol
            import matplotlib
            import reportlab
            import textblob
            logger.info("✅ Required packages are installed")
        except ImportError as e:
            logger.error(f"❌ Missing required packages: {str(e)}")
            logger.error("Please run: pip install -r requirements.txt")
            return False
        
        return True
    
    def register_agents_via_cli(self) -> bool:
        """Register all showcase agents using the CLI."""
        logger.info("Registering showcase agents...")
        
        success_count = 0
        for agent in SHOWCASE_AGENTS:
            logger.info(f"Registering {agent['name']}...")
            
            try:
                # Use CLI to register agent
                cmd = [
                    sys.executable, str(self.cli_path),
                    "register_agent",
                    "--name", agent["name"],
                    "--description", agent["description"]
                ]
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    logger.info(f"✅ {agent['name']} registered successfully")
                    success_count += 1
                else:
                    logger.error(f"❌ Failed to register {agent['name']}: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                logger.error(f"❌ Timeout registering {agent['name']}")
            except Exception as e:
                logger.error(f"❌ Error registering {agent['name']}: {str(e)}")
        
        logger.info(f"Registered {success_count}/{len(SHOWCASE_AGENTS)} agents")
        return success_count == len(SHOWCASE_AGENTS)
    
    def start_agents(self) -> bool:
        """Start all showcase agents."""
        logger.info("Starting showcase agents...")
        
        success_count = 0
        for agent in SHOWCASE_AGENTS:
            agent_file = self.agent_dir / agent["file"]
            logger.info(f"Starting {agent['name']}...")
            
            try:
                # Start agent process in background
                process = subprocess.Popen(
                    [sys.executable, str(agent_file)],
                    cwd=str(self.agent_dir),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                
                # Give agent time to start
                time.sleep(2)
                
                # Check if process is still running
                if process.poll() is None:
                    logger.info(f"✅ {agent['name']} started (PID: {process.pid})")
                    success_count += 1
                else:
                    logger.error(f"❌ {agent['name']} failed to start")
                    
            except Exception as e:
                logger.error(f"❌ Error starting {agent['name']}: {str(e)}")
        
        logger.info(f"Started {success_count}/{len(SHOWCASE_AGENTS)} agents")
        return success_count == len(SHOWCASE_AGENTS)
    
    def verify_deployment(self) -> bool:
        """Verify that all agents are running and accessible."""
        logger.info("Verifying agent deployment...")
        
        try:
            # Wait a bit for agents to fully initialize
            time.sleep(5)
            
            # Check active agents via API
            response = requests.get(f"{self.backend_url}/api/v1/agents/active", timeout=10)
            if response.status_code != 200:
                logger.error("❌ Could not fetch active agents list")
                return False
            
            active_agents = response.json()
            active_names = [agent.get("name", "") for agent in active_agents]
            
            showcase_active = []
            for agent in SHOWCASE_AGENTS:
                if agent["name"] in active_names:
                    showcase_active.append(agent["name"])
                    logger.info(f"✅ {agent['name']} is active")
                else:
                    logger.warning(f"⚠️  {agent['name']} is not showing as active")
            
            success_rate = len(showcase_active) / len(SHOWCASE_AGENTS)
            logger.info(f"Deployment verification: {len(showcase_active)}/{len(SHOWCASE_AGENTS)} agents active ({success_rate*100:.0f}%)")
            
            if success_rate >= 0.8:  # 80% success rate is acceptable
                return True
            else:
                return False
                
        except Exception as e:
            logger.error(f"❌ Error verifying deployment: {str(e)}")
            return False
    
    def deploy_all(self) -> bool:
        """Deploy all showcase agents with full workflow."""
        logger.info("🚀 Starting GenAI AgentOS Showcase Deployment")
        logger.info("=" * 50)
        
        # Step 1: Check prerequisites
        if not self.check_prerequisites():
            logger.error("❌ Prerequisites not met. Deployment failed.")
            return False
        
        # Step 2: Register agents
        if not self.register_agents_via_cli():
            logger.error("❌ Agent registration failed. Deployment failed.")
            return False
        
        # Step 3: Start agents
        if not self.start_agents():
            logger.error("❌ Agent startup failed. Deployment failed.")
            return False
        
        # Step 4: Verify deployment
        if not self.verify_deployment():
            logger.warning("⚠️  Deployment verification had issues, but some agents may be working")
            logger.info("You can check agent status manually or try running the showcase")
        
        logger.info("=" * 50)
        logger.info("🎉 Showcase deployment completed!")
        logger.info("")
        logger.info("Next steps:")
        logger.info("1. Upload sample data: python upload_samples.py")
        logger.info("2. Run the showcase: python run_showcase.py --document sample_proposal.pdf")
        logger.info("3. Or use the web interface at http://localhost:3000/flows")
        
        return True

def main():
    """Main deployment function."""
    deployer = ShowcaseDeployer()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--verify-only":
        # Just verify current deployment
        if deployer.verify_deployment():
            logger.info("✅ Showcase agents are properly deployed")
            sys.exit(0)
        else:
            logger.error("❌ Showcase deployment verification failed")
            sys.exit(1)
    else:
        # Full deployment
        if deployer.deploy_all():
            sys.exit(0)
        else:
            sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Deployment interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Deployment failed with error: {str(e)}")
        sys.exit(1)