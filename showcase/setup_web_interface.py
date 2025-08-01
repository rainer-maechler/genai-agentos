#!/usr/bin/env python3
"""
Setup Web Interface for Showcase

This script helps set up the showcase for the web interface by:
1. Creating a demo user account
2. Registering showcase agents via API
3. Creating the Document Analysis Pipeline flow
"""

import requests
import json
import sys
from pathlib import Path
from loguru import logger

BACKEND_URL = "http://localhost:8000"

class WebInterfaceSetup:
    """Setup showcase for web interface."""
    
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.session_token = None
        self.user_id = None
        
        # Showcase agents to register
        self.showcase_agents = [
            {
                "name": "document_parser",
                "description": "Handles various document formats and extracts raw content with OCR support"
            },
            {
                "name": "text_extractor", 
                "description": "Cleans and structures extracted text with entity recognition"
            },
            {
                "name": "analytics_agent",
                "description": "Performs deep content analysis, risk assessment, and business intelligence"
            },
            {
                "name": "sentiment_analyzer",
                "description": "Analyzes emotional tone and sentiment with confidence scoring"
            },
            {
                "name": "report_generator",
                "description": "Generates formatted reports, visualizations, and executive summaries"
            }
        ]
    
    def create_demo_user(self, username: str = "showcase", password: str = "showcase123") -> bool:
        """Create a demo user account."""
        try:
            user_data = {
                "username": username,
                "password": password
            }
            
            response = requests.post(
                f"{self.backend_url}/api/v1/users/register",
                json=user_data,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"✅ Demo user '{username}' created successfully")
                return True
            elif response.status_code == 400 and "already registered" in response.text.lower():
                logger.info(f"✅ Demo user '{username}' already exists")
                return True
            else:
                logger.error(f"❌ Failed to create user: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error creating user: {str(e)}")
            return False
    
    def login_user(self, username: str = "showcase", password: str = "showcase123") -> bool:
        """Login and get authentication token."""
        try:
            response = requests.post(
                f"{self.backend_url}/api/v1/users/login_access_token",
                data={"username": username, "password": password},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.session_token = data.get("access_token")
                self.user_id = data.get("user_id")
                logger.info("✅ Successfully authenticated")
                return True
            else:
                logger.error(f"❌ Login failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Login error: {str(e)}")
            return False
    
    def register_agents(self) -> bool:
        """Register showcase agents via API."""
        if not self.session_token:
            logger.error("❌ Not authenticated. Cannot register agents.")
            return False
        
        logger.info("📝 Registering showcase agents...")
        headers = {"Authorization": f"Bearer {self.session_token}"}
        
        success_count = 0
        for agent in self.showcase_agents:
            try:
                agent_data = {
                    "name": agent["name"],
                    "description": agent["description"]
                }
                
                response = requests.post(
                    f"{self.backend_url}/api/v1/agents/register",
                    json=agent_data,
                    headers=headers,
                    timeout=15
                )
                
                if response.status_code == 200:
                    logger.info(f"✅ Registered {agent['name']}")
                    success_count += 1
                elif response.status_code == 400 and "already exists" in response.text.lower():
                    logger.info(f"✅ {agent['name']} already registered")
                    success_count += 1
                else:
                    logger.error(f"❌ Failed to register {agent['name']}: {response.status_code}")
                    logger.error(f"Response: {response.text}")
                    
            except Exception as e:
                logger.error(f"❌ Error registering {agent['name']}: {str(e)}")
        
        logger.info(f"Agent registration: {success_count}/{len(self.showcase_agents)} successful")
        return success_count >= len(self.showcase_agents) * 0.8  # 80% success rate
    
    def create_document_analysis_flow(self) -> bool:
        """Create the Document Analysis Pipeline flow."""
        if not self.session_token:
            logger.error("❌ Not authenticated. Cannot create flow.")
            return False
        
        logger.info("🔄 Creating Document Analysis Pipeline flow...")
        headers = {"Authorization": f"Bearer {self.session_token}"}
        
        # Define the flow structure
        flow_data = {
            "name": "Document Analysis Pipeline",
            "description": "Complete document analysis showcase with sentiment analysis, risk assessment, and report generation",
            "agents_flow": [
                {
                    "agent_name": "document_parser",
                    "position": {"x": 100, "y": 100},
                    "input_mapping": {"file_id": "input.file_id"},
                    "output_mapping": {"parsed_content": "content", "metadata": "doc_metadata"}
                },
                {
                    "agent_name": "text_extractor",
                    "position": {"x": 300, "y": 100}, 
                    "input_mapping": {"content": "parsed_content"},
                    "output_mapping": {"structured_text": "text", "entities": "extracted_entities"}
                },
                {
                    "agent_name": "analytics_agent",
                    "position": {"x": 500, "y": 100},
                    "input_mapping": {"text": "structured_text", "entities": "extracted_entities"},
                    "output_mapping": {"analysis": "content_analysis", "topics": "topic_analysis", "risk": "risk_analysis"}
                },
                {
                    "agent_name": "sentiment_analyzer",
                    "position": {"x": 300, "y": 300},
                    "input_mapping": {"text": "structured_text"},
                    "output_mapping": {"sentiment": "sentiment_analysis", "emotions": "emotion_analysis"}
                },
                {
                    "agent_name": "report_generator",
                    "position": {"x": 500, "y": 300},
                    "input_mapping": {
                        "content_analysis": "content_analysis",
                        "sentiment_analysis": "sentiment_analysis", 
                        "emotion_analysis": "emotion_analysis",
                        "topic_analysis": "topic_analysis",
                        "risk_analysis": "risk_analysis",
                        "entities": "extracted_entities",
                        "metadata": "doc_metadata"
                    },
                    "output_mapping": {"final_report": "report"}
                }
            ]
        }
        
        try:
            response = requests.post(
                f"{self.backend_url}/api/v1/agentflows/register-flow",
                json=flow_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                flow_result = response.json()
                flow_id = flow_result.get("flow_id")
                logger.info(f"✅ Document Analysis Pipeline created (ID: {flow_id})")
                return True
            else:
                logger.error(f"❌ Failed to create flow: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error creating flow: {str(e)}")
            return False
    
    def check_agents_status(self) -> bool:
        """Check if agents are active and ready."""
        if not self.session_token:
            return False
        
        headers = {"Authorization": f"Bearer {self.session_token}"}
        
        try:
            response = requests.get(
                f"{self.backend_url}/api/v1/agents/active",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                active_agents = response.json()
                active_names = [agent.get("name", "") for agent in active_agents]
                
                logger.info(f"📊 Active agents: {len(active_names)}")
                for name in active_names:
                    if name in [a["name"] for a in self.showcase_agents]:
                        logger.info(f"  ✅ {name}")
                
                return len(active_names) > 0
            else:
                logger.warning(f"⚠️  Could not check agent status: {response.status_code}")
                return True  # Assume OK
                
        except Exception as e:
            logger.warning(f"⚠️  Error checking agents: {str(e)}")
            return True  # Assume OK
    
    def setup_complete_showcase(self) -> bool:
        """Complete setup process."""
        logger.info("🚀 Setting up GenAI AgentOS Showcase for Web Interface")
        logger.info("=" * 60)
        
        # Step 1: Create demo user
        if not self.create_demo_user():
            return False
        
        # Step 2: Login
        if not self.login_user():
            return False
        
        # Step 3: Register agents
        if not self.register_agents():
            logger.warning("⚠️  Some agents failed to register, but continuing...")
        
        # Step 4: Create document analysis flow
        if not self.create_document_analysis_flow():
            logger.warning("⚠️  Flow creation failed, but agents should be available...")
        
        # Step 5: Check status
        self.check_agents_status()
        
        logger.info("=" * 60)
        logger.info("✅ Showcase setup completed!")
        logger.info("")
        logger.info("🌐 Web Interface Access:")
        logger.info("  Login: http://localhost:3000/login") 
        logger.info("  Username: showcase")
        logger.info("  Password: showcase123")
        logger.info("")
        logger.info("📋 After login, go to:")
        logger.info("  Agent Flows: http://localhost:3000/agent-flows")
        logger.info("  Agents: http://localhost:3000/agents")
        logger.info("")
        logger.info("🎯 You should now see the showcase agents and can create/run flows!")
        
        return True

def main():
    """Main setup function."""
    setup = WebInterfaceSetup()
    
    if setup.setup_complete_showcase():
        sys.exit(0)
    else:
        logger.error("❌ Setup failed")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Setup failed: {str(e)}")
        sys.exit(1)