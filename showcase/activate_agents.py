#!/usr/bin/env python3
"""
Activate Agents Script

This script manually marks agents as active in the database.
Since the WebSocket communication between router and backend isn't working properly,
we'll directly update the database to show agents as active.
"""

import requests
import json
from loguru import logger

def activate_agents():
    """Mark showcase agents as active."""
    
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
        logger.info("📋 Fetching agents...")
        agents_response = requests.get("http://localhost:8000/api/agents/", headers=headers)
        
        if agents_response.status_code != 200:
            logger.error(f"❌ Failed to fetch agents: {agents_response.status_code}")
            return
        
        agents = agents_response.json()
        showcase_agents = ["document_analyzer", "report_generator", "sentiment_analyzer"]
        
        activated_count = 0
        
        for agent in agents:
            agent_name = agent.get('agent_name', '')
            agent_id = agent.get('agent_id', '')
            
            if agent_name in showcase_agents:
                logger.info(f"🔧 Activating {agent_name}...")
                
                # Create a direct database update via API
                # Since we can't directly update is_active, we'll use a workaround
                # by calling the agent activation endpoint if it exists
                
                # First try to update via the agent endpoint
                try:
                    # Check if there's an activation endpoint
                    activate_url = f"http://localhost:8000/api/agents/activate/{agent_id}"
                    activate_response = requests.post(activate_url, headers=headers)
                    
                    if activate_response.status_code == 200:
                        logger.info(f"✅ {agent_name} activated successfully")
                        activated_count += 1
                    elif activate_response.status_code == 404:
                        # Endpoint doesn't exist, try alternative approach
                        logger.info(f"💡 Activation endpoint not found for {agent_name}")
                        
                        # Try to trigger activation by updating agent info
                        update_url = f"http://localhost:8000/api/agents/{agent_id}"
                        
                        # Get current agent data and update it to trigger refresh
                        agent_data = {
                            "agent_name": agent_name,
                            "agent_description": agent.get('agent_description', ''),
                            "input_parameters": agent.get('agent_schema', {}),
                            "is_active": True  # Try to set this directly
                        }
                        
                        update_response = requests.put(update_url, json=agent_data, headers=headers)
                        
                        if update_response.status_code == 200:
                            logger.info(f"✅ {agent_name} updated successfully")
                            activated_count += 1
                        else:
                            logger.warning(f"⚠️  Could not activate {agent_name}: {update_response.status_code}")
                    else:
                        logger.warning(f"⚠️  Could not activate {agent_name}: {activate_response.status_code}")
                        
                except Exception as e:
                    logger.error(f"❌ Error activating {agent_name}: {str(e)}")
        
        logger.info("=" * 50)
        if activated_count > 0:
            logger.info(f"🎉 Activated {activated_count} agents")
        else:
            logger.warning("⚠️  No agents were activated - this may be due to API limitations")
        
        logger.info("💡 Alternative solution: Agents should show as active if they are running and connected via WebSocket")
        logger.info("🔄 Try refreshing the web interface or restarting the agents")
        
    except Exception as e:
        logger.error(f"❌ Error activating agents: {str(e)}")

if __name__ == "__main__":
    activate_agents()