#!/usr/bin/env python3
"""
Check Agent Status

This script checks if agents are properly registered and active.
"""

import requests
import json
from loguru import logger

def check_agent_status():
    """Check agent status in the backend."""
    
    # Login to get auth token
    login_url = "http://localhost:8000/api/login/access-token"
    login_data = {
        "username": "showcase",
        "password": "Showcase123@"
    }
    
    try:
        logger.info("🔐 Logging in...")
        response = requests.post(login_url, data=login_data)
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}
            logger.info("✅ Successfully authenticated")
        else:
            logger.error(f"❌ Login failed: {response.status_code}")
            return
        
        # Get all agents
        logger.info("📋 Fetching all agents...")
        agents_response = requests.get("http://localhost:8000/api/agents/", headers=headers)
        
        if agents_response.status_code == 200:
            agents = agents_response.json()
            logger.info(f"📊 Found {len(agents)} registered agents:")
            
            for agent in agents:
                name = agent.get('name', 'Unknown')
                description = agent.get('description', 'No description')
                logger.info(f"  • {name} - {description}")
                logger.debug(f"    Agent data: {agent}")
        else:
            logger.error(f"❌ Failed to fetch agents: {agents_response.status_code}")
            return
        
        # Get active agents
        logger.info("🟢 Checking active agents...")
        active_response = requests.get("http://localhost:8000/api/agents/active?agent_type=all", headers=headers)
        
        if active_response.status_code == 200:
            active_agents = active_response.json()
            logger.info(f"🎯 Active agents: {len(active_agents)}")
            
            if active_agents:
                for agent in active_agents:
                    name = agent.get('name', 'Unknown')
                    logger.info(f"  ✅ {name} - ACTIVE")
            else:
                logger.warning("⚠️  No agents are currently active")
                logger.info("💡 This means agents are registered but not connected via WebSocket")
        else:
            logger.error(f"❌ Failed to fetch active agents: {active_response.status_code}")
            logger.error(f"Response: {active_response.text}")
        
        # Check WebSocket connections in router
        logger.info("🔗 WebSocket connections should be visible in router logs")
        
    except Exception as e:
        logger.error(f"❌ Error checking status: {str(e)}")

if __name__ == "__main__":
    check_agent_status()