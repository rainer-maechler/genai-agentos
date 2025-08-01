#!/usr/bin/env python3
"""
Simple Active Check

Debug what the active agents endpoint actually returns.
"""

import requests
import json
from loguru import logger

def check_active_endpoint():
    """Check what the active agents endpoint returns."""
    
    # Login
    login_url = "http://localhost:8000/api/login/access-token"
    login_data = {"username": "showcase", "password": "Showcase123@"}
    
    try:
        response = requests.post(login_url, data=login_data)
        if response.status_code != 200:
            logger.error(f"Login failed: {response.status_code}")
            return
        
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test different active endpoints
        endpoints = [
            "/api/agents/active",
            "/api/agents/active?agent_type=all",
            "/api/agents/active?agent_type=genai"
        ]
        
        for endpoint in endpoints:
            logger.info(f"🔍 Testing: {endpoint}")
            url = f"http://localhost:8000{endpoint}"
            
            try:
                response = requests.get(url, headers=headers)
                logger.info(f"Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"Response: {json.dumps(data, indent=2)}")
                else:
                    logger.info(f"Error: {response.text}")
                    
            except Exception as e:
                logger.error(f"Request failed: {str(e)}")
            
            logger.info("-" * 50)
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")

if __name__ == "__main__":
    check_active_endpoint()