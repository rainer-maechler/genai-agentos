#!/usr/bin/env python3
"""
Simple Agent Registration for Web Interface

This creates a demo user and registers agents using the correct API endpoints.
"""

import requests
import json
from loguru import logger

BACKEND_URL = "http://localhost:8000"

def register_user_and_agents():
    """Register user and agents using correct API endpoints."""
    
    # Step 1: Register user
    logger.info("🔐 Registering demo user...")
    try:
        user_response = requests.post(
            f"{BACKEND_URL}/api/register",
            json={"username": "showcase", "password": "showcase123"},
            timeout=10
        )
        
        if user_response.status_code in [200, 201]:
            logger.info("✅ User registered successfully")
        elif user_response.status_code == 400:
            logger.info("✅ User already exists")
        else:
            logger.warning(f"⚠️  User registration: {user_response.status_code}")
            
    except Exception as e:
        logger.warning(f"⚠️  User registration issue: {str(e)}")
    
    # Step 2: Login
    logger.info("🔑 Logging in...")
    try:
        login_response = requests.post(
            f"{BACKEND_URL}/api/login/access-token",
            data={"username": "showcase", "password": "showcase123"},
            timeout=10
        )
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            access_token = token_data.get("access_token")
            logger.info("✅ Login successful")
        else:
            logger.error(f"❌ Login failed: {login_response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Login error: {str(e)}")
        return False
    
    # Step 3: Register agents
    logger.info("🤖 Registering showcase agents...")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    agents = [
        {
            "name": "document_analyzer",
            "description": "Analyzes documents and extracts key information, sentiment, and business metrics for comprehensive reporting"
        },
        {
            "name": "report_generator", 
            "description": "Generates professional reports with visualizations, executive summaries, and strategic recommendations"
        },
        {
            "name": "sentiment_analyzer",
            "description": "Performs advanced sentiment analysis and emotional tone assessment on business documents"
        }
    ]
    
    success_count = 0
    for agent in agents:
        try:
            agent_response = requests.post(
                f"{BACKEND_URL}/api/agents/register",
                json=agent,
                headers=headers,
                timeout=15
            )
            
            if agent_response.status_code in [200, 201]:
                logger.info(f"✅ Registered {agent['name']}")
                success_count += 1
            elif agent_response.status_code == 400:
                logger.info(f"✅ {agent['name']} already exists")
                success_count += 1
            else:
                logger.error(f"❌ Failed to register {agent['name']}: {agent_response.status_code}")
                logger.error(f"Response: {agent_response.text}")
                
        except Exception as e:
            logger.error(f"❌ Error registering {agent['name']}: {str(e)}")
    
    # Step 4: Verify registration
    logger.info("🔍 Verifying agent registration...")
    try:
        agents_response = requests.get(
            f"{BACKEND_URL}/api/agents/",
            headers=headers,
            timeout=10
        )
        
        if agents_response.status_code == 200:
            registered_agents = agents_response.json()
            logger.info(f"✅ Found {len(registered_agents)} total agents")
            
            showcase_agents = [a for a in registered_agents if a.get('name', '').startswith(('document_', 'report_', 'sentiment_'))]
            logger.info(f"🎯 Showcase agents registered: {len(showcase_agents)}")
            
            for agent in showcase_agents:
                logger.info(f"  📋 {agent.get('name', 'unknown')}")
                
        else:
            logger.warning(f"⚠️  Could not verify agents: {agents_response.status_code}")
            
    except Exception as e:
        logger.warning(f"⚠️  Verification error: {str(e)}")
    
    logger.info("=" * 60)
    logger.info("✅ AGENT REGISTRATION COMPLETE!")
    logger.info("=" * 60)
    logger.info("🌐 Web Interface Access:")
    logger.info("1. Go to: http://localhost:3000/login")
    logger.info("2. Username: showcase")
    logger.info("3. Password: showcase123")
    logger.info("4. IMPORTANT: Go to Settings and add an LLM model first!")
    logger.info("5. Then check: http://localhost:3000/agents")
    logger.info("6. Create flows at: http://localhost:3000/agent-flows")
    logger.info("")
    logger.info("🎯 Your showcase agents should now be visible in the web interface!")
    
    return success_count > 0

if __name__ == "__main__":
    try:
        register_user_and_agents()
    except Exception as e:
        logger.error(f"Registration failed: {str(e)}")