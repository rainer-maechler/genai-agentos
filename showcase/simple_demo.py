#!/usr/bin/env python3
"""
Simple Demo of Report Generator Core Functionality

This demonstrates the report generation capabilities without requiring 
the full GenAI protocol infrastructure.
"""

import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import Template
import base64
import io

class SimpleReportGenerator:
    """Simplified version of the report generator for demo purposes."""
    
    def __init__(self):
        self.name = "report_generator"
        self.version = "1.0.0"
        
        # Executive summary template
        self.executive_template = """
# Executive Summary: {{ document_title }}

## Overview
{{ overview }}

## Key Findings
{% for finding in key_findings %}
- {{ finding }}
{% endfor %}

## Sentiment Analysis
- **Overall Sentiment**: {{ sentiment.overall_sentiment|title }} ({{ sentiment.sentiment_score }}/100)
- **Confidence Level**: {{ sentiment.confidence * 100 }}%
- **Dominant Emotion**: {{ sentiment.dominant_emotion|title }}

## Risk Assessment
- **Risk Level**: {{ risk.overall_risk_level|title }}
- **Risk Score**: {{ risk.risk_score }}/20

## Business Metrics
{% if metrics.has_financial_data %}
- **Financial Data**: Present
- **ROI Indicators**: {{ metrics.roi_indicators|join(', ') }}
{% endif %}

## Recommendations
{% for recommendation in recommendations %}
1. {{ recommendation }}
{% endfor %}

---
*Report generated on {{ generated_at }} by GenAI AgentOS Report Generator*
        """
    
    def create_sample_data(self):
        """Create realistic sample data for demo."""
        return {
            "document_info": {
                "filename": "Digital_Transformation_Proposal.pdf",
                "document_type": "business_proposal",
                "word_count": 1247,
                "language": "English",
                "quality_score": 85
            },
            "sentiment": {
                "overall_sentiment": "positive",
                "sentiment_score": 85,
                "confidence": 0.92,
                "dominant_emotion": "optimistic"
            },
            "risk": {
                "overall_risk_level": "medium",
                "risk_score": 8,
                "detected_risks": {
                    "financial": {"severity": "medium", "count": 2},
                    "operational": {"severity": "low", "count": 1}
                }
            },
            "metrics": {
                "has_financial_data": True,
                "roi_indicators": ["180% ROI within 3 years", "$2.3M annual savings", "24-month payback period"]
            },
            "topics": {
                "primary_focus": "digital_transformation",
                "categorized_topics": {
                    "technology": ["automation", "cloud", "AI", "analytics"],
                    "business": ["ROI", "efficiency", "cost savings"],
                    "risk": ["implementation", "adoption", "timeline"]
                }
            }
        }
    
    def generate_executive_summary(self, data: Dict[str, Any]) -> str:
        """Generate executive summary."""
        template = Template(self.executive_template)
        
        # Create overview
        overview = f"Analysis of {data['document_info']['document_type']} containing {data['document_info']['word_count']} words. "
        overview += f"Overall sentiment is {data['sentiment']['overall_sentiment']} with {data['sentiment']['confidence']*100:.0f}% confidence. "
        overview += f"Risk assessment indicates {data['risk']['overall_risk_level']} risk level."
        
        # Extract key findings
        key_findings = [
            f"Strong {data['sentiment']['overall_sentiment']} sentiment detected throughout document",
            f"Risk factors identified with score of {data['risk']['risk_score']}/20",
            "Significant financial data and ROI projections present",
            f"Primary focus area: {data['topics']['primary_focus'].replace('_', ' ').title()}",
            "Professional presentation with detailed business case"
        ]
        
        # Generate recommendations
        recommendations = [
            "Proceed with detailed due diligence and technical assessment",
            "Negotiate milestone-based payment structure to mitigate financial risk",
            "Implement comprehensive change management program",
            "Establish dedicated project oversight and governance"
        ]
        
        template_data = {
            'document_title': data['document_info']['filename'].replace('_', ' ').replace('.pdf', ''),
            'overview': overview,
            'key_findings': key_findings,
            'sentiment': data['sentiment'],
            'risk': data['risk'],
            'metrics': data['metrics'],
            'recommendations': recommendations,
            'generated_at': datetime.now().strftime('%B %d, %Y at %I:%M %p')
        }
        
        return template.render(**template_data)
    
    def create_sentiment_chart(self, sentiment_data: Dict) -> str:
        """Create sentiment visualization."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Sentiment score gauge
        score = sentiment_data.get('sentiment_score', 50)
        color = '#DC143C' if score < 40 else '#FFD700' if score < 60 else '#2E8B57'
        
        ax1.barh(['Sentiment Score'], [score], color=color, alpha=0.8)
        ax1.set_xlim(0, 100)
        ax1.set_xlabel('Score (0-100)')
        ax1.set_title('Overall Sentiment Score')
        ax1.text(score + 2, 0, f"{score}%", va='center', fontweight='bold')
        
        # Confidence and emotions
        emotions = ['Optimistic', 'Confident', 'Professional', 'Strategic']
        percentages = [35, 25, 25, 15]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        
        ax2.pie(percentages, labels=emotions, colors=colors, autopct='%1.1f%%', startangle=90)
        ax2.set_title('Emotional Analysis')
        
        plt.tight_layout()
        
        # Save to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        chart_b64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return chart_b64
    
    def create_risk_chart(self, risk_data: Dict) -> str:
        """Create risk assessment chart."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        risk_categories = ['Financial', 'Operational', 'Technical', 'Market']
        risk_scores = [8, 4, 6, 5]  # Sample risk scores
        colors = ['#dc3545', '#28a745', '#ffc107', '#17a2b8']
        
        bars = ax.bar(risk_categories, risk_scores, color=colors, alpha=0.7)
        ax.set_ylabel('Risk Score (0-10)')
        ax.set_title('Risk Assessment by Category')
        ax.set_ylim(0, 10)
        
        # Add value labels
        for bar, score in zip(bars, risk_scores):
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.1,
                   f'{score}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        # Save to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        chart_b64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return chart_b64
    
    def generate_html_report(self, summary: str, charts: Dict[str, str]) -> str:
        """Generate HTML report with embedded charts."""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>GenAI AgentOS - Business Analysis Report</title>
            <style>
                body { font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; line-height: 1.6; color: #333; }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 30px; }
                .header h1 { margin: 0; font-size: 2.2em; }
                .header p { margin: 5px 0 0 0; opacity: 0.9; }
                h1, h2, h3 { color: #2c3e50; }
                h2 { border-bottom: 2px solid #3498db; padding-bottom: 5px; }
                .chart { text-align: center; margin: 30px 0; padding: 20px; background: #f8f9fa; border-radius: 10px; }
                .chart img { max-width: 100%; border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
                .chart h3 { color: #495057; margin-top: 0; }
                .summary-box { background: #e8f4fd; padding: 20px; border-left: 4px solid #007bff; margin: 20px 0; border-radius: 5px; }
                .content { background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                pre { background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; border-left: 4px solid #28a745; }
                .footer { text-align: center; margin-top: 40px; padding: 20px; background: #f8f9fa; border-radius: 10px; color: #6c757d; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 Business Intelligence Report</h1>
                <p>Generated by GenAI AgentOS Report Generator on {{ generated_at }}</p>
            </div>
            
            <div class="content">
                <div class="summary-box">
                    <h2>🎯 Executive Summary</h2>
                    <p>This comprehensive analysis provides actionable insights and strategic recommendations based on advanced AI-powered document analysis.</p>
                </div>
                
                {% if charts %}
                <div class="charts">
                    <h2>📈 Data Visualizations</h2>
                    {% for chart_name, chart_data in charts.items() %}
                    <div class="chart">
                        <h3>{{ chart_name.replace('_', ' ').title() }}</h3>
                        <img src="data:image/png;base64,{{ chart_data }}" alt="{{ chart_name }}">
                    </div>
                    {% endfor %}
                </div>
                {% endif %}
                
                <div class="report-content">
                    <h2>📋 Detailed Analysis</h2>
                    <pre>{{ summary }}</pre>
                </div>
            </div>
            
            <div class="footer">
                <p>🤖 Powered by GenAI AgentOS | Report Generator v1.0.0</p>
                <p>This report contains AI-generated analysis and should be reviewed by domain experts</p>
            </div>
        </body>
        </html>
        """
        
        template = Template(html_template)
        return template.render(
            summary=summary,
            charts=charts,
            generated_at=datetime.now().strftime('%B %d, %Y at %I:%M %p')
        )

async def run_demo():
    """Run the report generator demo."""
    print("🎯 GenAI AgentOS Report Generator Demo")
    print("=" * 60)
    print("📊 Generating comprehensive business intelligence report...")
    
    # Create report generator
    generator = SimpleReportGenerator()
    
    # Create sample data
    data = generator.create_sample_data()
    
    # Generate executive summary
    print("📝 Creating executive summary...")
    summary = generator.generate_executive_summary(data)
    
    # Generate visualizations
    print("📈 Creating data visualizations...")
    charts = {}
    charts['sentiment_analysis'] = generator.create_sentiment_chart(data['sentiment'])
    charts['risk_assessment'] = generator.create_risk_chart(data['risk'])
    
    # Generate HTML report
    print("🌐 Creating HTML report...")
    html_report = generator.generate_html_report(summary, charts)
    
    # Save outputs
    output_dir = Path("demo_output")
    output_dir.mkdir(exist_ok=True)
    
    # Save executive summary
    summary_path = output_dir / "executive_summary.md"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)
    
    # Save HTML report
    html_path = output_dir / "business_report.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_report)
    
    # Save sample data
    data_path = output_dir / "analysis_data.json"
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    
    print("\n" + "=" * 60)
    print("✅ REPORT GENERATION COMPLETE!")
    print("=" * 60)
    print(f"📁 Output directory: {output_dir.absolute()}")
    print(f"📋 Executive summary: {summary_path.name}")
    print(f"🌐 HTML report: {html_path.name}")
    print(f"📊 Charts generated: {len(charts)}")
    print(f"📄 Analysis data: {data_path.name}")
    
    print("\n🎉 Open 'business_report.html' in your browser to see the full interactive report!")
    
    # Show a preview of the executive summary
    print("\n" + "=" * 60)
    print("📋 EXECUTIVE SUMMARY PREVIEW")
    print("=" * 60)
    print(summary[:500] + "...")
    
if __name__ == "__main__":
    asyncio.run(run_demo())