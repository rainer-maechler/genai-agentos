#!/usr/bin/env python3
"""
Database Fix Script

This script fixes the input_parameters format issue in the database
by converting string values to proper JSON objects.
"""

import requests
import json
from loguru import logger

def fix_database():
    """Fix agents with string input_parameters in the database."""
    
    # First, let's login to get an auth token
    login_url = "http://localhost:8000/api/login/access-token"
    login_data = {
        "username": "showcase",
        "password": "Showcase123@"
    }
    
    try:
        logger.info("🔐 Logging in to get auth token...")
        response = requests.post(login_url, data=login_data)
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}
            logger.info("✅ Successfully authenticated")
        else:
            logger.error(f"❌ Login failed: {response.status_code}")
            return
        
        # Try to get agents - this might fail due to the string issue
        agents_url = "http://localhost:8000/api/agents/"
        
        logger.info("🔍 Attempting to fetch agents...")
        response = requests.get(agents_url, headers=headers)
        
        if response.status_code == 500:
            logger.warning("⚠️  Backend is crashing due to string input_parameters")
            logger.info("📊 This is expected - we need to fix the database directly")
            
            # The issue is in the database, we need to update via SQL
            logger.info("🔧 Database needs manual fixing via SQL")
            logger.info("💡 Restarting backend should help if we can't access via API")
            
            # Let's try restarting the backend to see if it helps
            logger.info("🔄 Let's restart the backend service...")
            return "restart_needed"
            
        elif response.status_code == 200:
            agents = response.json()
            logger.info(f"✅ Successfully fetched {len(agents)} agents")
            
            # Check if any agents have string input_parameters
            fixed_count = 0
            for agent in agents:
                if isinstance(agent.get("input_parameters"), str):
                    logger.info(f"🔧 Fixing agent: {agent['name']}")
                    
                    # Convert string to proper JSON
                    try:
                        if agent["input_parameters"]:
                            parsed_params = json.loads(agent["input_parameters"])
                        else:
                            parsed_params = {}
                    except json.JSONDecodeError:
                        # If it's not valid JSON, create a default structure
                        parsed_params = {"document": "string", "format": "text"}
                    
                    # Update the agent
                    update_url = f"http://localhost:8000/api/agents/{agent['id']}"
                    update_data = {
                        **agent,
                        "input_parameters": parsed_params
                    }
                    
                    update_response = requests.put(update_url, json=update_data, headers=headers)
                    if update_response.status_code == 200:
                        logger.info(f"✅ Fixed agent: {agent['name']}")
                        fixed_count += 1
                    else:
                        logger.error(f"❌ Failed to fix agent: {agent['name']}")
            
            if fixed_count > 0:
                logger.info(f"🎉 Fixed {fixed_count} agents")
            else:
                logger.info("✅ All agents already have correct format")
                
        else:
            logger.error(f"❌ Failed to fetch agents: {response.status_code}")
            logger.error(f"Response: {response.text}")
            
    except Exception as e:
        logger.error(f"❌ Error fixing database: {str(e)}")
        return "restart_needed"

if __name__ == "__main__":
    result = fix_database()
    if result == "restart_needed":
        logger.info("🔄 Restart needed - run: docker restart genai-backend")