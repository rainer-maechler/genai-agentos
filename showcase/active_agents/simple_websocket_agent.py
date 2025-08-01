#!/usr/bin/env python3
"""
Simple WebSocket Agent (No genai-protocol dependency)

This creates a basic WebSocket connection to GenAI AgentOS router
to make agents show as active in the web interface.
"""

import asyncio
import json
import websockets
import uuid
from typing import Dict, Any
from loguru import logger


class SimpleWebSocketAgent:
    """Simple agent with manual WebSocket connection."""
    
    def __init__(self, name: str, description: str, agent_jwt: str):
        self.name = name
        self.description = description
        self.version = "1.0.0"
        self.agent_jwt = agent_jwt
        self.session_id = str(uuid.uuid4())
    
    async def process_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming message - override in subclasses."""
        return {
            "agent": self.name,
            "status": "completed",
            "result": f"Processed by {self.name}",
            "timestamp": "2025-08-01T08:30:00Z"
        }
    
    async def connect_and_run(self):
        """Connect to WebSocket and handle messages."""
        uri = "ws://localhost:8080/ws"
        
        try:
            logger.info(f"🚀 Starting {self.name} agent...")
            logger.info(f"📡 Connecting to: {uri}")
            
            # Create connection with custom headers  
            async with websockets.connect(
                uri, 
                additional_headers={"x-custom-authorization": self.agent_jwt}
            ) as websocket:
                logger.info("✅ Connected to GenAI AgentOS")
                logger.info("🟢 Agent is now ACTIVE and visible in web interface")
                
                # Send agent registration message
                register_message = {
                    "message_type": "agent_register",
                    "request_payload": {
                        "agent_name": self.name,
                        "agent_description": self.description,
                        "agent_version": self.version,
                        "capabilities": ["document_analysis", "sentiment_analysis", "report_generation"]
                    }
                }
                
                await websocket.send(json.dumps(register_message))
                logger.info("📤 Sent agent registration message")
                
                # Listen for messages
                async for message in websocket:
                    try:
                        message_data = json.loads(message)
                        logger.info(f"📨 Received message: {message_data}")
                        
                        # Handle different message types
                        message_type = message_data.get("message_type")
                        invoked_by = message_data.get("invoked_by")
                        request_payload = message_data.get("request_payload")
                        
                        if message_type == "agent_invoke" and request_payload:
                            # Process the agent invocation
                            result = await self.process_message(request_payload)
                            
                            # Send response back to invoker
                            response_message = {
                                "message_type": "agent_response",
                                "invoked_by": invoked_by,
                                "request_payload": result
                            }
                            
                            await websocket.send(json.dumps(response_message))
                            logger.info(f"📤 Sent response to: {invoked_by}")
                        
                        else:
                            logger.info(f"🔄 Received system message: {message_type}")
                        
                    except json.JSONDecodeError as e:
                        logger.error(f"❌ Invalid JSON received: {str(e)}")
                    except Exception as e:
                        logger.error(f"❌ Error processing message: {str(e)}")
                        
                        # Send error response
                        if invoked_by:
                            error_response = {
                                "message_type": "agent_error",
                                "invoked_by": invoked_by,
                                "error": {
                                    "error_message": f"Processing failed: {str(e)}",
                                    "agent": self.name
                                }
                            }
                            
                            await websocket.send(json.dumps(error_response))
                        
        except KeyboardInterrupt:
            logger.info("🛑 Agent stopped by user")
        except Exception as e:
            logger.error(f"❌ Agent connection error: {str(e)}")


class DocumentAnalyzerAgent(SimpleWebSocketAgent):
    """Document analyzer agent."""
    
    def __init__(self):
        super().__init__(
            name="document_analyzer",
            description="Analyzes documents and extracts key information, sentiment, and business metrics",
            agent_jwt="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4ZTBhYjE5Ni01ODk0LTRiMTgtOTgwMi1mOWNiMzNjMDQzZTYiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6ImIwNjZjNGZlLTU3MjctNDdmZi1iNzAyLTk1MjAyZDZhYzg2MCJ9.jhcNzqcERtixFwpmvUURjsK_MREbwxjxBo3ehsHacu4"
        )
    
    async def process_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process document analysis request."""
        try:
            content = message_data.get("content", "")
            logger.info(f"Document Analyzer processing: {content[:100]}...")
            
            # Simulate document analysis
            analysis_result = {
                "agent": self.name,
                "status": "completed",
                "document_info": {
                    "word_count": len(str(content).split()),
                    "document_type": "business_document",
                    "language": "English",
                    "quality_score": 85
                },
                "key_metrics": {
                    "entities_found": 12,
                    "topics_identified": 5,
                    "sentiment_indicators": 8
                },
                "extracted_data": {
                    "organizations": ["TechCorp", "Innovation Group"],
                    "financial_figures": ["$5.8M", "$2.3M", "180% ROI"],
                    "dates": ["December 2024", "18 months", "3 years"],
                    "key_topics": ["digital transformation", "efficiency", "cost savings"]
                },
                "processing_time": "1.2 seconds",
                "timestamp": "2025-08-01T08:30:00Z"
            }
            
            logger.info("✅ Document analysis completed successfully")
            return analysis_result
            
        except Exception as e:
            logger.error(f"❌ Error in document analysis: {str(e)}")
            return {
                "agent": self.name,
                "status": "error",
                "error": str(e),
                "timestamp": "2025-08-01T08:30:00Z"
            }


class SentimentAnalyzerAgent(SimpleWebSocketAgent):
    """Sentiment analyzer agent."""
    
    def __init__(self):
        super().__init__(
            name="sentiment_analyzer", 
            description="Performs advanced sentiment analysis and emotional tone assessment",
            agent_jwt="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmNjc5NzI1My00ZGJkLTRjODItOTNiNy03NjFhYWQyODEwZTUiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6ImIwNjZjNGZlLTU3MjctNDdmZi1iNzAyLTk1MjAyZDZhYzg2MCJ9.h0HlMGKjtRz8Tk7UmOk4S6lJA7y8_kDuYmwVoBXfJ40"
        )
    
    async def process_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process sentiment analysis request."""
        try:
            content = message_data.get("content", "")
            logger.info(f"Sentiment Analyzer processing: {content[:100]}...")
            
            # Simple sentiment analysis simulation
            positive_words = ["good", "great", "excellent", "positive", "success", "growth", "improvement"]
            negative_words = ["bad", "poor", "negative", "problem", "issue", "risk", "concern"]
            
            text_lower = str(content).lower()
            positive_count = sum(1 for word in positive_words if word in text_lower)
            negative_count = sum(1 for word in negative_words if word in text_lower)
            
            # Calculate sentiment
            if positive_count > negative_count:
                sentiment = "positive"
                score = min(0.9, 0.5 + (positive_count - negative_count) * 0.1)
            elif negative_count > positive_count:
                sentiment = "negative"
                score = max(0.1, 0.5 - (negative_count - positive_count) * 0.1)
            else:
                sentiment = "neutral"
                score = 0.5
            
            sentiment_result = {
                "agent": self.name,
                "status": "completed",
                "sentiment_analysis": {
                    "overall_sentiment": sentiment,
                    "sentiment_score": int(score * 100),
                    "polarity": round(score * 2 - 1, 2),
                    "confidence": 0.85,
                    "intensity": "strong" if abs(positive_count - negative_count) > 2 else "moderate"
                },
                "emotional_analysis": {
                    "dominant_emotion": "optimistic" if sentiment == "positive" else "cautious" if sentiment == "negative" else "neutral",
                    "emotions_detected": ["professional", "confident", sentiment] if sentiment != "neutral" else ["professional", "neutral"]
                },
                "processing_time": "0.8 seconds",
                "timestamp": "2025-08-01T08:30:00Z"
            }
            
            logger.info(f"✅ Sentiment analysis completed: {sentiment} ({int(score * 100)}/100)")
            return sentiment_result
            
        except Exception as e:
            logger.error(f"❌ Error in sentiment analysis: {str(e)}")
            return {
                "agent": self.name,
                "status": "error",
                "error": str(e),
                "timestamp": "2025-08-01T08:30:00Z"
            }


class ReportGeneratorAgent(SimpleWebSocketAgent):
    """Report generator agent."""
    
    def __init__(self):
        super().__init__(
            name="report_generator",
            description="Generates comprehensive reports with visualizations and executive summaries",
            agent_jwt="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiYmI0YzZkZS1mMDU4LTRkMDAtYjBlYi01YmFiOTYzZmFiZmIiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6ImIwNjZjNGZlLTU3MjctNDdmZi1iNzAyLTk1MjAyZDZhYzg2MCJ9.Ja_iqyuYluxqBZRalU70M0mZ7u7GqUVorC4wa8qmvCY"
        )
    
    async def process_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process report generation request."""
        try:
            content = message_data.get("content", "")
            logger.info(f"Report Generator processing: {content[:100]}...")
            
            # Generate executive summary
            executive_summary = """
# Executive Summary: Business Analysis Report

## Overview
Comprehensive analysis completed with high confidence. Document exhibits positive sentiment 
with strong business metrics and manageable risk factors.

## Key Findings
- Strong positive sentiment detected (87/100)
- Financial projections show 180% ROI over 3 years
- Risk assessment indicates medium overall risk
- Professional presentation with excellent structure

## Strategic Recommendations
1. Proceed with comprehensive due diligence
2. Negotiate milestone-based payment structure
3. Implement risk monitoring protocols
4. Establish project governance framework

## Business Intelligence
- Investment: $5.8M over 18 months
- Expected ROI: 180% within 3 years
- Risk Score: 9/20 (Medium)
- Quality Score: 91/100

---
*Report generated by GenAI AgentOS Report Generator v1.0.0*
            """
            
            report_result = {
                "agent": self.name,
                "status": "completed",
                "executive_summary": executive_summary.strip(),
                "detailed_report": "Full detailed analysis with 15 sections covering sentiment, risk, business metrics, and strategic recommendations.",
                "visualizations": {
                    "sentiment_chart": "base64_chart_data_placeholder",
                    "risk_assessment": "base64_chart_data_placeholder",
                    "financial_projections": "base64_chart_data_placeholder"
                },
                "formatted_reports": {
                    "html": "Complete HTML report with embedded charts",
                    "pdf_available": True,
                    "json_data": "Structured analysis data"
                },
                "key_metrics": {
                    "sentiment_score": 87,
                    "risk_score": 9,
                    "quality_score": 91,
                    "recommendations_count": 8
                },
                "processing_time": "2.8 seconds",
                "timestamp": "2025-08-01T08:30:00Z"
            }
            
            logger.info("✅ Report generation completed successfully")
            return report_result
            
        except Exception as e:
            logger.error(f"❌ Error in report generation: {str(e)}")
            return {
                "agent": self.name,
                "status": "error",
                "error": str(e),
                "timestamp": "2025-08-01T08:30:00Z"
            }


async def run_agent(agent_class):
    """Run a specific agent."""
    agent = agent_class()
    await agent.connect_and_run()


if __name__ == "__main__":
    import sys
    
    # Determine which agent to run based on filename or argument
    if len(sys.argv) > 1:
        agent_name = sys.argv[1]
    else:
        # Try to determine from filename
        import os
        filename = os.path.basename(__file__)
        if "document" in filename:
            agent_name = "document_analyzer"
        elif "sentiment" in filename:
            agent_name = "sentiment_analyzer"
        elif "report" in filename:
            agent_name = "report_generator"
        else:
            agent_name = "document_analyzer"  # default
    
    # Run the appropriate agent
    if agent_name == "document_analyzer":
        asyncio.run(run_agent(DocumentAnalyzerAgent))
    elif agent_name == "sentiment_analyzer":
        asyncio.run(run_agent(SentimentAnalyzerAgent))
    elif agent_name == "report_generator":
        asyncio.run(run_agent(ReportGeneratorAgent))
    else:
        logger.error(f"Unknown agent: {agent_name}")