#!/usr/bin/env python3
"""
Test WebSocket Connection

This script tests the WebSocket connection to understand the protocol.
"""

import asyncio
import json
import websockets
from loguru import logger

async def test_connection():
    """Test WebSocket connection with debug output."""
    
    # Use one of the existing JWT tokens
    agent_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4ZTBhYjE5Ni01ODk0LTRiMTgtOTgwMi1mOWNiMzNjMDQzZTYiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6ImIwNjZjNGZlLTU3MjctNDdmZi1iNzAyLTk1MjAyZDZhYzg2MCJ9.jhcNzqcERtixFwpmvUURjsK_MREbwxjxBo3ehsHacu4"
    
    uri = "ws://localhost:8080/ws"
    
    try:
        logger.info(f"🔗 Testing connection to: {uri}")
        
        # Test connection with JWT in headers
        async with websockets.connect(
            uri, 
            additional_headers={"x-custom-authorization": agent_jwt}
        ) as websocket:
            logger.info("✅ Connected successfully!")
            
            # Send registration message
            register_message = {
                "message_type": "agent_register",
                "request_payload": {
                    "agent_name": "test_agent",
                    "agent_description": "Test agent for debugging",
                    "agent_version": "1.0.0"
                }
            }
            
            logger.info(f"📤 Sending: {json.dumps(register_message, indent=2)}")
            await websocket.send(json.dumps(register_message))
            
            # Wait for response
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                logger.info(f"📨 Received: {response}")
            except asyncio.TimeoutError:
                logger.warning("⏰ No response received within 5 seconds")
            
            # Keep connection alive for a bit
            logger.info("🔄 Keeping connection alive for 10 seconds...")
            await asyncio.sleep(10)
            
    except Exception as e:
        logger.error(f"❌ Connection failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_connection())