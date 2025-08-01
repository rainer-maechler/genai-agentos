#!/usr/bin/env python3
"""
Demo of the Report Generator Agent

This script demonstrates the report generator capabilities 
without requiring the full GenAI AgentOS infrastructure.
"""

import json
import asyncio
from datetime import datetime
from pathlib import Path
import sys
import os

# Add the agents directory to the path
sys.path.append(str(Path(__file__).parent / "agents"))

# Import the report generator
from report_generator import ReportGeneratorAgent

class MockSession:
    """Mock GenAI session for demo purposes."""
    pass

def create_sample_analysis_data():
    """Create sample analysis data that would come from other agents."""
    return {
        "document_info": {
            "filename": "sample_proposal.pdf",
            "document_type": "business_proposal",
            "word_count": 1247,
            "language": "English",
            "quality_score": 85
        },
        "entities": {
            "organizations": ["TechCorp Industries", "Innovation Consulting Group"],
            "people": ["Sarah Johnson"],
            "money": ["$5.8M", "$2.3M", "$2.1M", "$2.4M", "$1.3M"],
            "dates": ["December 15, 2024", "18 months", "3 years"],
            "locations": ["Digital Transformation"]
        },
        "topics": {
            "primary_focus": "digital_transformation",
            "categorized_topics": {
                "technology": ["automation", "cloud infrastructure", "data analytics", "AI"],
                "business": ["ROI", "efficiency", "cost savings", "transformation"],
                "project_management": ["timeline", "phases", "implementation", "integration"],
                "risk_management": ["mitigation", "assessment", "factors"]
            }
        },
        "sentiment_summary": {
            "overall_sentiment": "positive",
            "sentiment_score": 85,
            "polarity": 0.75,
            "subjectivity": 0.6,
            "confidence": 0.92,
            "dominant_emotion": "optimistic",
            "intensity": "strong"
        },
        "emotions": {
            "emotions_detected": ["optimistic", "confident", "professional", "enthusiastic", "strategic", "ambitious"],
            "emotion_percentages": {
                "optimistic": 35,
                "confident": 25,
                "professional": 20,
                "enthusiastic": 10,
                "strategic": 7,
                "ambitious": 3
            }
        },
        "business_sentiment": {
            "business_tone": "professional",
            "financial_sentiment": {"sentiment": "positive"},
            "performance_sentiment": {"sentiment": "optimistic"}
        },
        "risk_analysis": {
            "overall_risk_level": "medium",
            "risk_score": 8,
            "detected_risks": {
                "financial": {"severity": "medium", "count": 2},
                "operational": {"severity": "low", "count": 1},
                "market": {"severity": "medium", "count": 1}
            },
            "recommendations": [
                "Establish clear milestone-based payment structure",
                "Implement comprehensive change management program",
                "Develop contingency plans for integration challenges",
                "Regular stakeholder communication and progress reviews"
            ]
        },
        "business_metrics": {
            "has_financial_data": True,
            "has_performance_data": True,
            "roi_indicators": ["180% ROI", "24-month payback", "$8.2M NPV"],
            "performance_indicators": ["40% efficiency improvement", "60% task reduction"],
            "growth_indicators": ["18-month timeline", "3-phase approach"]
        },
        "compliance": {
            "frameworks_identified": ["SOX", "GDPR"],
            "compliance_focus": "data_privacy"
        },
        "quality_assessment": {
            "quality_level": "good",
            "quality_score": 85,
            "structure_complexity": "medium",
            "quality_factors": ["clear_objectives", "detailed_timeline", "financial_projections"]
        },
        "insights": {
            "key_findings": [
                "Strong financial projections with 180% ROI over 3 years",
                "Comprehensive 18-month implementation timeline with clear phases",
                "Significant efficiency gains of 40% and $2.3M annual cost savings",
                "Well-structured risk assessment with mitigation strategies",
                "Professional presentation with detailed business case"
            ],
            "recommendations": [
                "Proceed with detailed technical assessment and due diligence",
                "Negotiate milestone-based payment structure to reduce financial risk",
                "Establish dedicated project management office for oversight",
                "Implement comprehensive change management and training program"
            ],
            "opportunities": [
                "Potential for additional efficiency gains beyond 40%",
                "Opportunity to become industry leader in digital transformation",
                "Platform for future innovations and scalability",
                "Enhanced competitive advantage through modernization"
            ],
            "concerns": [
                "Large upfront investment of $5.8M requires careful cash flow management",
                "18-month timeline may face delays due to complexity",
                "Success depends on user adoption and change management effectiveness"
            ]
        },
        "analysis_summary": {
            "analysis_confidence": "high"
        }
    }

async def demo_report_generator():
    """Demonstrate the report generator capabilities."""
    print("🎯 GenAI AgentOS Report Generator Demo")
    print("=" * 50)
    
    # Create the report generator agent
    agent = ReportGeneratorAgent()
    
    # Create sample analysis data
    analysis_data = create_sample_analysis_data()
    
    # Create the message format expected by the agent
    message_data = {
        **analysis_data,
        "options": {
            "include_html": True,
            "include_pdf": True
        }
    }
    
    print("📊 Generating comprehensive business report...")
    
    # Generate the reports
    mock_session = MockSession()
    results = await agent.process_message(mock_session, json.dumps(message_data))
    
    if results.get("status") == "success":
        print("✅ Report generation successful!")
        
        # Save the results
        output_dir = Path("demo_output")
        output_dir.mkdir(exist_ok=True)
        
        # Save executive summary
        if "executive_summary" in results:
            summary_path = output_dir / "executive_summary.md"
            with open(summary_path, "w", encoding="utf-8") as f:
                f.write(results["executive_summary"])
            print(f"📋 Executive summary saved: {summary_path}")
        
        # Save detailed report
        if "detailed_report" in results:
            detailed_path = output_dir / "detailed_report.md"
            with open(detailed_path, "w", encoding="utf-8") as f:
                f.write(results["detailed_report"])
            print(f"📝 Detailed report saved: {detailed_path}")
        
        # Save HTML report
        if "formatted_reports" in results and "html" in results["formatted_reports"]:
            html_path = output_dir / "report.html"
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(results["formatted_reports"]["html"])
            print(f"🌐 HTML report saved: {html_path}")
        
        # Save complete JSON results
        json_path = output_dir / "complete_analysis.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"📄 Complete analysis saved: {json_path}")
        
        # Print summary
        print("\n" + "=" * 50)
        print("📈 REPORT GENERATION SUMMARY")
        print("=" * 50)
        
        metadata = results.get("report_metadata", {})
        print(f"✅ Report formats generated: {', '.join(metadata.get('report_formats', []))}")
        print(f"📊 Charts created: {metadata.get('chart_count', 0)}")
        print(f"📋 Report sections: {metadata.get('total_sections', 0)}")
        print(f"🎯 Analysis confidence: {metadata.get('analysis_confidence', 'medium').title()}")
        
        # Show visualizations info
        if "visualizations" in results:
            viz_count = len([k for k, v in results["visualizations"].items() if v and k != 'error'])
            print(f"📈 Visualizations: {viz_count} charts generated")
            for chart_name in results["visualizations"].keys():
                if chart_name != 'error':
                    print(f"   - {chart_name.replace('_', ' ').title()}")
        
        print(f"\n🎉 Demo completed! Check the 'demo_output' directory for all generated files.")
        
    else:
        print(f"❌ Report generation failed: {results.get('error', 'Unknown error')}")

if __name__ == "__main__":
    try:
        # Set matplotlib backend to non-interactive to avoid display issues
        import matplotlib
        matplotlib.use('Agg')
        
        asyncio.run(demo_report_generator())
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        import traceback
        traceback.print_exc()