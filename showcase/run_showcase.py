#!/usr/bin/env python3
"""
Run Showcase Pipeline Script

This script executes the complete document analysis pipeline using the deployed showcase agents.
It demonstrates the full workflow from document upload to final report generation.
"""

import asyncio
import argparse
import sys
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional
import requests
from loguru import logger
import tempfile
import base64

# Configuration
BACKEND_URL = "http://localhost:8000"
SAMPLE_DATA_DIR = Path(__file__).parent / "sample_data"

class ShowcasePipeline:
    """Orchestrates the complete document analysis pipeline."""
    
    def __init__(self, backend_url: str = BACKEND_URL):
        self.backend_url = backend_url
        self.session_token = None
        
        # Pipeline configuration
        self.pipeline_stages = [
            {"agent": "document_parser", "stage": "Document Parsing"},
            {"agent": "text_extractor", "stage": "Text Extraction"}, 
            {"agent": "analytics_agent", "stage": "Content Analysis"},
            {"agent": "sentiment_analyzer", "stage": "Sentiment Analysis"},
            {"agent": "report_generator", "stage": "Report Generation"}
        ]
    
    def authenticate(self, username: str = "demo", password: str = "demo") -> bool:
        """Authenticate with the backend (using demo credentials)."""
        try:
            response = requests.post(
                f"{self.backend_url}/api/v1/users/login_access_token",
                data={"username": username, "password": password},
                timeout=10
            )
            
            if response.status_code == 200:
                self.session_token = response.json().get("access_token")
                logger.info("✅ Authenticated successfully")
                return True
            else:
                logger.error(f"❌ Authentication failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Authentication error: {str(e)}")
            return False
    
    def upload_document(self, file_path: Path) -> Optional[str]:
        """Upload document to the system and return file ID."""
        if not file_path.exists():
            logger.error(f"❌ File not found: {file_path}")
            return None
        
        logger.info(f"📄 Uploading document: {file_path.name}")
        
        try:
            headers = {"Authorization": f"Bearer {self.session_token}"}
            files = {"file": (file_path.name, open(file_path, "rb"))}
            
            response = requests.post(
                f"{self.backend_url}/api/v1/files/upload",
                files=files,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                file_data = response.json()
                file_id = file_data.get("file_id")
                logger.info(f"✅ Document uploaded successfully (ID: {file_id})")
                return file_id
            else:
                logger.error(f"❌ Upload failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Upload error: {str(e)}")
            return None
    
    def execute_agent_flow(self, file_id: str, output_format: str = "detailed") -> Optional[Dict[str, Any]]:
        """Execute the document analysis flow using the agents."""
        logger.info("🔄 Executing document analysis pipeline...")
        
        # Create the flow configuration
        flow_config = {
            "name": "Document Analysis Showcase",
            "description": "Complete document analysis pipeline showcase",
            "input": {"file_id": file_id},
            "config": {
                "detailed_analysis": True,
                "include_visualizations": True,
                "output_format": output_format
            },
            "agents_flow": [
                {
                    "agent_name": "document_parser",
                    "input_mapping": {"file_id": "file_id"},
                    "output_mapping": {"parsed_content": "content", "metadata": "metadata"}
                },
                {
                    "agent_name": "text_extractor", 
                    "input_mapping": {"content": "parsed_content"},
                    "output_mapping": {"structured_text": "text", "entities": "extracted_entities"}
                },
                {
                    "agent_name": "analytics_agent",
                    "input_mapping": {"text": "structured_text", "entities": "extracted_entities"},
                    "output_mapping": {"analysis": "content_analysis", "topics": "topic_analysis"}
                },
                {
                    "agent_name": "sentiment_analyzer",
                    "input_mapping": {"text": "structured_text"},
                    "output_mapping": {"sentiment": "sentiment_analysis", "emotions": "emotion_analysis"}
                },
                {
                    "agent_name": "report_generator",
                    "input_mapping": {
                        "content_analysis": "analysis",
                        "sentiment_analysis": "sentiment", 
                        "emotion_analysis": "emotions",
                        "topic_analysis": "topics",
                        "entities": "extracted_entities",
                        "metadata": "metadata"
                    },
                    "output_mapping": {"final_report": "report"}
                }
            ]
        }
        
        try:
            headers = {"Authorization": f"Bearer {self.session_token}"}
            
            # Execute the flow
            response = requests.post(
                f"{self.backend_url}/api/v1/flows/execute",
                json=flow_config,
                headers=headers,
                timeout=120  # Allow 2 minutes for processing
            )
            
            if response.status_code == 200:
                result = response.json()
                flow_id = result.get("flow_id")
                logger.info(f"✅ Flow started successfully (ID: {flow_id})")
                
                # Monitor flow execution
                return self._monitor_flow_execution(flow_id)
            else:
                logger.error(f"❌ Flow execution failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Flow execution error: {str(e)}")
            return None
    
    def _monitor_flow_execution(self, flow_id: str) -> Optional[Dict[str, Any]]:
        """Monitor flow execution and return results."""
        logger.info(f"⏳ Monitoring flow execution: {flow_id}")
        
        headers = {"Authorization": f"Bearer {self.session_token}"}
        max_attempts = 30  # 5 minutes max
        attempt = 0
        
        while attempt < max_attempts:
            try:
                response = requests.get(
                    f"{self.backend_url}/api/v1/flows/{flow_id}/status",
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    status_data = response.json()
                    status = status_data.get("status", "unknown")
                    
                    if status == "completed":
                        logger.info("✅ Flow completed successfully")
                        # Get results
                        return self._get_flow_results(flow_id)
                    elif status == "failed":
                        logger.error("❌ Flow execution failed")
                        error_msg = status_data.get("error", "Unknown error")
                        logger.error(f"Error: {error_msg}")
                        return None
                    elif status == "running":
                        current_stage = status_data.get("current_stage", "unknown")
                        logger.info(f"🔄 Flow running - Current stage: {current_stage}")
                    
                    # Wait before next check
                    time.sleep(10)
                    attempt += 1
                else:
                    logger.error(f"❌ Status check failed: {response.status_code}")
                    return None
                    
            except Exception as e:
                logger.error(f"❌ Status monitoring error: {str(e)}")
                attempt += 1
                time.sleep(10)
        
        logger.error("❌ Flow execution timeout")
        return None
    
    def _get_flow_results(self, flow_id: str) -> Optional[Dict[str, Any]]:
        """Get flow execution results."""
        try:
            headers = {"Authorization": f"Bearer {self.session_token}"}
            response = requests.get(
                f"{self.backend_url}/api/v1/flows/{flow_id}/results",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"❌ Failed to get results: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error getting results: {str(e)}")
            return None
    
    def save_results(self, results: Dict[str, Any], output_path: Path):
        """Save pipeline results to file."""
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            logger.info(f"📁 Results saved to: {output_path}")
            
            # Also save formatted reports if available
            if "final_report" in results:
                report_data = results["final_report"]
                
                # Save executive summary
                if "executive_summary" in report_data:
                    summary_path = output_path.parent / f"{output_path.stem}_executive_summary.md"
                    with open(summary_path, "w", encoding="utf-8") as f:
                        f.write(report_data["executive_summary"])
                    logger.info(f"📋 Executive summary saved to: {summary_path}")
                
                # Save HTML report
                if "formatted_reports" in report_data and "html" in report_data["formatted_reports"]:
                    html_path = output_path.parent / f"{output_path.stem}_report.html"
                    with open(html_path, "w", encoding="utf-8") as f:
                        f.write(report_data["formatted_reports"]["html"])
                    logger.info(f"🌐 HTML report saved to: {html_path}")
                
                # Save PDF if available
                if "formatted_reports" in report_data and "pdf_data" in report_data["formatted_reports"]:
                    pdf_path = output_path.parent / f"{output_path.stem}_report.pdf"
                    pdf_data = base64.b64decode(report_data["formatted_reports"]["pdf_data"])
                    with open(pdf_path, "wb") as f:
                        f.write(pdf_data)
                    logger.info(f"📄 PDF report saved to: {pdf_path}")
            
        except Exception as e:
            logger.error(f"❌ Error saving results: {str(e)}")
    
    def print_summary(self, results: Dict[str, Any]):
        """Print a summary of the analysis results."""
        logger.info("=" * 60)
        logger.info("📊 ANALYSIS SUMMARY")
        logger.info("=" * 60)
        
        try:
            if "final_report" in results:
                report = results["final_report"]
                
                # Document info
                if "report_metadata" in report:
                    metadata = report["report_metadata"]
                    logger.info(f"📄 Document Analysis Complete")
                    logger.info(f"   Report Formats: {', '.join(metadata.get('report_formats', []))}")
                    logger.info(f"   Confidence: {metadata.get('analysis_confidence', 'medium').title()}")
                
                # Key metrics from executive summary
                logger.info("\n🎯 Key Findings:")
                if "executive_summary" in report:
                    # Extract key points from summary (simplified)
                    summary = report["executive_summary"]
                    lines = summary.split('\n')
                    for line in lines:
                        if line.strip().startswith('-') and len(line.strip()) > 5:
                            logger.info(f"   {line.strip()}")
                
                # Visualizations info
                if "visualizations" in report:
                    viz_count = len([k for k, v in report["visualizations"].items() if v and k != 'error'])
                    logger.info(f"\n📈 Generated {viz_count} visualizations")
                
            logger.info("\n✅ Showcase pipeline execution completed successfully!")
            
        except Exception as e:
            logger.error(f"Error printing summary: {str(e)}")

def main():
    """Main function to run the showcase pipeline."""
    parser = argparse.ArgumentParser(description="Run GenAI AgentOS Document Analysis Showcase")
    parser.add_argument("--document", "-d", type=str, help="Path to document to analyze")
    parser.add_argument("--output", "-o", type=str, default="analysis_result.json", help="Output file path")
    parser.add_argument("--format", "-f", choices=["basic", "detailed"], default="detailed", help="Analysis format")
    parser.add_argument("--username", "-u", type=str, default="demo", help="Username for authentication")
    parser.add_argument("--password", "-p", type=str, default="demo", help="Password for authentication")
    
    args = parser.parse_args()
    
    # Initialize pipeline
    pipeline = ShowcasePipeline()
    
    logger.info("🚀 Starting GenAI AgentOS Document Analysis Showcase")
    logger.info("=" * 60)
    
    # Step 1: Authentication
    if not pipeline.authenticate(args.username, args.password):
        logger.error("❌ Authentication failed. Exiting.")
        sys.exit(1)
    
    # Step 2: Determine document to analyze
    if args.document:
        doc_path = Path(args.document)
        if not doc_path.is_absolute():
            # Try relative to current directory first, then sample_data
            if not doc_path.exists():
                doc_path = SAMPLE_DATA_DIR / args.document
    else:
        # Use default sample document
        doc_path = SAMPLE_DATA_DIR / "sample_proposal.pdf"
        logger.info(f"No document specified, using default: {doc_path.name}")
    
    if not doc_path.exists():
        logger.error(f"❌ Document not found: {doc_path}")
        logger.error("Please provide a valid document path or run 'python upload_samples.py' first")
        sys.exit(1)
    
    # Step 3: Upload document
    file_id = pipeline.upload_document(doc_path)
    if not file_id:
        logger.error("❌ Document upload failed. Exiting.")
        sys.exit(1)
    
    # Step 4: Execute pipeline
    results = pipeline.execute_agent_flow(file_id, args.format)
    if not results:
        logger.error("❌ Pipeline execution failed. Exiting.")
        sys.exit(1)
    
    # Step 5: Save results
    output_path = Path(args.output)
    pipeline.save_results(results, output_path)
    
    # Step 6: Print summary
    pipeline.print_summary(results)
    
    logger.info("🎉 Showcase completed successfully!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Showcase interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Showcase failed: {str(e)}")
        sys.exit(1)