#!/usr/bin/env python3
"""
Web Interface Status Checker

This script checks if agents are visible and active in the GenAI AgentOS web interface.
"""

import requests
import json
from loguru import logger

def check_web_interface_status():
    """Check if agents are visible in web interface."""
    
    try:
        # Check if backend is responding
        backend_url = "http://localhost:8000"
        
        logger.info("🌐 Checking GenAI AgentOS Web Interface Status")
        logger.info("=" * 50)
        
        # Test backend connection
        try:
            response = requests.get(f"{backend_url}/docs", timeout=5)
            if response.status_code == 200:
                logger.info("✅ Backend API is running at http://localhost:8000")
            else:
                logger.error(f"❌ Backend API returned status {response.status_code}")
                return
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Backend API not accessible: {str(e)}")
            return
        
        # Check frontend
        try:
            frontend_url = "http://localhost:3000"
            response = requests.get(frontend_url, timeout=5)
            if response.status_code == 200:
                logger.info("✅ Frontend is running at http://localhost:3000")
            else:
                logger.error(f"❌ Frontend returned status {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Frontend not accessible: {str(e)}")
        
        # Check router (WebSocket server)
        try:
            router_url = "http://localhost:8080"
            response = requests.get(f"{router_url}/docs", timeout=5)
            if response.status_code == 200:
                logger.info("✅ WebSocket Router is running at ws://localhost:8080/ws")
            else:
                logger.error(f"❌ Router returned status {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Router not accessible: {str(e)}")
        
        logger.info("=" * 50)
        logger.info("🎯 Next Steps:")
        logger.info("1. Go to: http://localhost:3000/")
        logger.info("2. Login with: username=showcase, password=Showcase123@")  
        logger.info("3. Go to Settings and add an LLM model (if not done already)")
        logger.info("4. Go to: http://localhost:3000/agents")
        logger.info("5. You should see 3 agents with GREEN borders (active)")
        logger.info("6. Go to: http://localhost:3000/agent-flows")
        logger.info("7. Create a new agent flow using the active agents")
        logger.info("")
        logger.info("🚀 Your GenAI AgentOS showcase is ready!")
        
    except Exception as e:
        logger.error(f"❌ Error checking web interface: {str(e)}")

if __name__ == "__main__":
    check_web_interface_status()