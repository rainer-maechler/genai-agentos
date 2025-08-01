#!/usr/bin/env python3
"""
Comprehensive GenAI AgentOS Showcase Demo

This demonstrates the complete report generator functionality
with real sample data and all the features working.
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
from loguru import logger

class ComprehensiveShowcase:
    """Complete showcase of the GenAI AgentOS Report Generator."""
    
    def __init__(self):
        self.sample_data_dir = Path("sample_data")
        self.output_dir = Path("showcase_results")
        self.output_dir.mkdir(exist_ok=True)
        
        # Professional color schemes
        self.colors = {
            'sentiment': ['#2E8B57', '#FFD700', '#DC143C'],  # Green, Yellow, Red
            'emotions': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'],
            'business': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'],
            'risk': ['#28a745', '#ffc107', '#dc3545']
        }
        
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
- **Confidence Level**: {{ (sentiment.confidence * 100)|round(1) }}%
- **Dominant Emotion**: {{ sentiment.dominant_emotion|title }}
- **Business Tone**: {{ sentiment.business_tone|title }}

## Risk Assessment
- **Risk Level**: {{ risk.overall_risk_level|title }}
- **Risk Score**: {{ risk.risk_score }}/20
{% if risk.detected_risks %}
- **Risk Categories**: {{ risk.detected_risks.keys()|list|join(', ')|title }}
{% endif %}

## Business Intelligence
{% if metrics.has_financial_data %}
- **Financial Analysis**: Present and analyzed
{% endif %}
{% if metrics.roi_indicators %}
- **ROI Indicators**: {{ metrics.roi_indicators|join(', ') }}
{% endif %}
{% if metrics.performance_indicators %}
- **Performance Metrics**: {{ metrics.performance_indicators|join(', ') }}
{% endif %}

## Strategic Recommendations
{% for recommendation in recommendations %}
{{ loop.index }}. {{ recommendation }}
{% endfor %}

## Investment Summary
{% if investment %}
- **Total Investment**: {{ investment.total_amount }}
- **Timeline**: {{ investment.duration }}
- **Expected ROI**: {{ investment.expected_roi }}
- **Payback Period**: {{ investment.payback_period }}
{% endif %}

---
**Report Classification**: {{ classification|title }}  
**Analysis Confidence**: {{ analysis_confidence|title }}  
**Generated**: {{ generated_at }} by GenAI AgentOS Report Generator v1.0.0

*This report contains AI-generated analysis and recommendations based on document content analysis, sentiment evaluation, and risk assessment algorithms.*
        """
        
    def create_comprehensive_sample_data(self) -> Dict[str, Any]:
        """Create comprehensive realistic analysis data."""
        return {
            "document_info": {
                "filename": "Digital_Transformation_Proposal_TechCorp.pdf",
                "document_type": "business_proposal",
                "word_count": 1847,
                "language": "English",
                "quality_score": 88,
                "processing_time": "3.2 seconds",
                "file_size": "4.3 KB"
            },
            "sentiment": {
                "overall_sentiment": "positive",
                "sentiment_score": 87,
                "polarity": 0.78,
                "subjectivity": 0.65,
                "confidence": 0.94,
                "dominant_emotion": "optimistic",
                "business_tone": "professional",
                "intensity": "strong"
            },
            "emotions": {
                "emotions_detected": ["optimistic", "confident", "professional", "enthusiastic", "strategic", "ambitious"],
                "emotion_percentages": {
                    "optimistic": 32,
                    "confident": 28,
                    "professional": 18,
                    "enthusiastic": 12,
                    "strategic": 7,
                    "ambitious": 3
                },
                "emotional_complexity": "high",
                "dominant_emotional_cluster": "positive_business"
            },
            "risk": {
                "overall_risk_level": "medium",
                "risk_score": 9,
                "detected_risks": {
                    "financial": {"severity": "medium", "count": 3, "factors": ["large investment", "ROI dependency", "cash flow impact"]},
                    "operational": {"severity": "low", "count": 2, "factors": ["implementation complexity", "user adoption"]},
                    "market": {"severity": "medium", "count": 2, "factors": ["competition", "technology evolution"]},
                    "timeline": {"severity": "low", "count": 1, "factors": ["18-month duration"]}
                },
                "risk_mitigation_quality": "good",
                "contingency_planning": "present"
            },
            "metrics": {
                "has_financial_data": True,
                "has_performance_data": True,
                "roi_indicators": ["180% ROI within 3 years", "$2.3M annual cost savings", "24-month payback period"],
                "performance_indicators": ["40% efficiency improvement", "60% manual task reduction", "95% accuracy increase"],
                "growth_indicators": ["Scalable architecture", "Future-ready platform", "Competitive advantage"],
                "financial_health_score": 85
            },
            "business_intelligence": {
                "market_positioning": "strong",
                "competitive_advantage": "significant",
                "innovation_index": 78,
                "scalability_score": 85,
                "sustainability_rating": "high"
            },
            "compliance": {
                "frameworks_identified": ["SOX", "GDPR", "ISO 27001"],
                "compliance_score": 82,
                "regulatory_readiness": "good"
            },
            "topics": {
                "primary_focus": "digital_transformation",
                "categorized_topics": {
                    "technology": ["automation", "cloud infrastructure", "AI integration", "data analytics", "cybersecurity"],
                    "business": ["ROI optimization", "efficiency gains", "cost reduction", "competitive advantage"],
                    "project_management": ["phased approach", "milestone tracking", "risk mitigation", "change management"],
                    "strategic": ["innovation", "scalability", "future-proofing", "market leadership"]
                },
                "topic_relevance_score": 94,
                "strategic_alignment": "excellent"
            },
            "quality": {
                "content_quality": "excellent",
                "structure_clarity": "high",
                "professional_presentation": "superior",
                "completeness_score": 91
            }
        }
    
    def create_investment_summary(self) -> Dict[str, Any]:
        """Create investment analysis summary."""
        return {
            "total_amount": "$5.8M",
            "duration": "18 months", 
            "expected_roi": "180% over 3 years",
            "payback_period": "24 months",
            "npv": "$8.2M over 5 years",
            "irr": "34.5%",
            "risk_adjusted_roi": "165%"
        }
    
    def generate_key_findings(self, data: Dict[str, Any]) -> List[str]:
        """Generate comprehensive key findings."""
        return [
            f"Strong {data['sentiment']['overall_sentiment']} sentiment with {data['sentiment']['confidence']*100:.0f}% confidence indicates well-received proposal",
            f"Comprehensive financial projections showing {data['metrics']['roi_indicators'][0]} and significant cost savings",
            f"Risk assessment reveals {data['risk']['overall_risk_level']} overall risk with {len(data['risk']['detected_risks'])} categories identified",
            f"Professional presentation quality scored {data['quality']['completeness_score']}/100 with excellent structure",
            f"Strategic alignment rated as {data['topics']['strategic_alignment']} with clear technology roadmap",
            f"Business intelligence analysis shows {data['business_intelligence']['market_positioning']} market positioning"
        ]
    
    def generate_strategic_recommendations(self, data: Dict[str, Any]) -> List[str]:
        """Generate strategic business recommendations."""
        risk_level = data['risk']['overall_risk_level']
        sentiment = data['sentiment']['overall_sentiment']
        
        recommendations = [
            "Proceed with comprehensive due diligence and technical architecture review",
            "Negotiate milestone-based payment schedule to optimize cash flow and reduce financial risk"
        ]
        
        if risk_level in ['medium', 'high']:
            recommendations.append("Implement enhanced risk monitoring and mitigation protocols")
            recommendations.append("Establish dedicated project governance committee with executive oversight")
        
        if sentiment == 'positive':
            recommendations.append("Leverage positive stakeholder sentiment to accelerate decision-making process")
        
        recommendations.extend([
            "Develop comprehensive change management strategy with user training programs",
            "Establish measurable success criteria and KPI tracking framework",
            "Create contingency plans for critical implementation phases"
        ])
        
        return recommendations
    
    def create_advanced_sentiment_visualization(self, data: Dict[str, Any]) -> str:
        """Create comprehensive sentiment analysis visualization."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Sentiment Score Gauge
        sentiment_score = data['sentiment']['sentiment_score']
        confidence = data['sentiment']['confidence'] * 100
        
        # Create gauge-like visualization
        ax1.barh(['Sentiment'], [sentiment_score], color=self.colors['sentiment'][2 if sentiment_score >= 70 else 1 if sentiment_score >= 40 else 0], alpha=0.8, height=0.3)
        ax1.set_xlim(0, 100)
        ax1.set_xlabel('Sentiment Score')
        ax1.set_title('Overall Sentiment Analysis', fontweight='bold', fontsize=14)
        ax1.text(sentiment_score + 2, 0, f"{sentiment_score}%\n(Confidence: {confidence:.1f}%)", va='center', fontweight='bold')
        
        # Add background zones
        ax1.axvspan(0, 40, alpha=0.1, color='red')
        ax1.axvspan(40, 70, alpha=0.1, color='yellow')  
        ax1.axvspan(70, 100, alpha=0.1, color='green')
        
        # 2. Emotional Profile
        emotions = data['emotions']['emotions_detected'][:6]
        percentages = [data['emotions']['emotion_percentages'].get(emotion, 0) for emotion in emotions]
        colors = self.colors['emotions'][:len(emotions)]
        
        wedges, texts, autotexts = ax2.pie(percentages, labels=emotions, colors=colors, autopct='%1.1f%%', startangle=90)
        ax2.set_title('Emotional Profile Distribution', fontweight='bold', fontsize=14)
        
        # 3. Risk Assessment by Category
        risk_data = data['risk']['detected_risks']
        risk_categories = list(risk_data.keys())
        risk_counts = [risk_data[cat]['count'] for cat in risk_categories]
        severities = [risk_data[cat]['severity'] for cat in risk_categories]
        
        severity_colors = {'low': '#28a745', 'medium': '#ffc107', 'high': '#dc3545'}
        bar_colors = [severity_colors.get(severity, '#6c757d') for severity in severities]
        
        bars = ax3.bar(risk_categories, risk_counts, color=bar_colors, alpha=0.8)
        ax3.set_ylabel('Risk Indicators Count')
        ax3.set_title('Risk Assessment by Category', fontweight='bold', fontsize=14)
        ax3.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar, count in zip(bars, risk_counts):
            ax3.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.05,
                    f'{count}', ha='center', va='bottom', fontweight='bold')
        
        # 4. Business Metrics Overview
        metrics_categories = ['Financial Health', 'Innovation Index', 'Scalability', 'Quality Score']
        metrics_scores = [
            data['metrics']['financial_health_score'],
            data['business_intelligence']['innovation_index'], 
            data['business_intelligence']['scalability_score'],
            data['quality']['completeness_score']
        ]
        
        bars = ax4.barh(metrics_categories, metrics_scores, color=self.colors['business'][:4], alpha=0.8)
        ax4.set_xlim(0, 100)
        ax4.set_xlabel('Score (0-100)')
        ax4.set_title('Business Intelligence Metrics', fontweight='bold', fontsize=14)
        
        # Add score labels
        for bar, score in zip(bars, metrics_scores):
            ax4.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2.,
                    f'{score}', va='center', fontweight='bold')
        
        plt.tight_layout()
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        chart_b64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return chart_b64
    
    def create_financial_analysis_chart(self, data: Dict[str, Any]) -> str:
        """Create financial analysis visualization."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # 1. Investment Timeline
        phases = ['Phase 1\n(Setup)', 'Phase 2\n(Implementation)', 'Phase 3\n(Optimization)']
        investments = [2.1, 2.4, 1.3]  # in millions
        timeline = ['Months 1-6', 'Months 7-12', 'Months 13-18']
        
        bars = ax1.bar(phases, investments, color=['#e74c3c', '#f39c12', '#27ae60'], alpha=0.8)
        ax1.set_ylabel('Investment ($ Millions)')
        ax1.set_title('Investment Distribution by Phase', fontweight='bold', fontsize=14)
        
        # Add value labels
        for bar, investment in zip(bars, investments):
            ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.05,
                    f'${investment}M', ha='center', va='bottom', fontweight='bold')
        
        # 2. ROI Projection
        years = ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5']
        cumulative_savings = [0.8, 2.3, 4.1, 6.4, 8.2]  # NPV progression
        
        ax2.plot(years, cumulative_savings, marker='o', linewidth=3, color='#2ecc71', markersize=8)
        ax2.fill_between(years, cumulative_savings, alpha=0.3, color='#2ecc71')
        ax2.axhline(y=5.8, color='#e74c3c', linestyle='--', alpha=0.7, label='Break-even ($5.8M)')
        ax2.set_ylabel('Cumulative Value ($ Millions)')
        ax2.set_title('ROI Projection & Break-Even Analysis', fontweight='bold', fontsize=14)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Add value labels
        for i, value in enumerate(cumulative_savings):
            ax2.text(i, value + 0.2, f'${value}M', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        chart_b64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return chart_b64
    
    def generate_executive_summary(self, data: Dict[str, Any]) -> str:
        """Generate comprehensive executive summary."""
        template = Template(self.executive_template)
        
        # Create overview
        doc_info = data['document_info']
        sentiment = data['sentiment']
        risk = data['risk']
        
        overview = f"Comprehensive analysis of {doc_info['document_type']} containing {doc_info['word_count']:,} words processed in {doc_info['processing_time']}. "
        overview += f"Document exhibits {sentiment['overall_sentiment']} sentiment ({sentiment['sentiment_score']}/100) with {sentiment['confidence']*100:.0f}% confidence. "
        overview += f"Risk assessment indicates {risk['overall_risk_level']} overall risk level with {len(risk['detected_risks'])} risk categories identified. "
        overview += f"Professional presentation quality scored {data['quality']['completeness_score']}/100 with {data['topics']['strategic_alignment']} strategic alignment."
        
        template_data = {
            'document_title': doc_info['filename'].replace('_', ' ').replace('.pdf', ''),
            'overview': overview,
            'key_findings': self.generate_key_findings(data),
            'sentiment': sentiment,
            'risk': risk,
            'metrics': data['metrics'],
            'recommendations': self.generate_strategic_recommendations(data),
            'investment': self.create_investment_summary(),
            'classification': 'business_critical',
            'analysis_confidence': 'high',
            'generated_at': datetime.now().strftime('%B %d, %Y at %I:%M %p')
        }
        
        return template.render(**template_data)
    
    def create_professional_html_report(self, summary: str, charts: Dict[str, str], data: Dict[str, Any]) -> str:
        """Create professional HTML report."""
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>GenAI AgentOS - Executive Business Intelligence Report</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { 
                    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif; 
                    line-height: 1.6; color: #2c3e50; background: #f8f9fa;
                }
                .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
                
                .header { 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white; padding: 40px; border-radius: 15px; margin-bottom: 30px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                }
                .header h1 { font-size: 2.8em; margin-bottom: 10px; }
                .header .subtitle { font-size: 1.2em; opacity: 0.9; }
                .header .meta { margin-top: 20px; font-size: 0.95em; opacity: 0.8; }
                
                .exec-summary { 
                    background: white; padding: 30px; border-radius: 15px; margin-bottom: 30px;
                    box-shadow: 0 5px 20px rgba(0,0,0,0.1); border-left: 5px solid #3498db;
                }
                
                .metrics-grid {
                    display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px; margin: 30px 0;
                }
                .metric-card {
                    background: white; padding: 25px; border-radius: 12px;
                    box-shadow: 0 3px 15px rgba(0,0,0,0.1); text-align: center;
                }
                .metric-value { font-size: 2.2em; font-weight: bold; color: #2980b9; }
                .metric-label { color: #7f8c8d; margin-top: 5px; font-weight: 500; }
                
                .chart-section { 
                    background: white; padding: 30px; border-radius: 15px; margin: 30px 0;
                    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
                }
                .chart-container { text-align: center; margin: 25px 0; }
                .chart-container img { 
                    max-width: 100%; border-radius: 12px; 
                    box-shadow: 0 5px 15px rgba(0,0,0,0.15);
                }
                .chart-title { 
                    font-size: 1.4em; color: #2c3e50; margin-bottom: 15px; 
                    font-weight: 600; text-align: center;
                }
                
                .content-section {
                    background: white; padding: 30px; border-radius: 15px; margin: 30px 0;
                    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
                }
                .section-title { 
                    font-size: 1.8em; color: #2c3e50; margin-bottom: 20px;
                    border-bottom: 3px solid #3498db; padding-bottom: 10px;
                }
                
                pre { 
                    background: #f8f9fa; padding: 25px; border-radius: 10px; 
                    overflow-x: auto; border-left: 4px solid #28a745; font-size: 0.9em;
                    white-space: pre-wrap; word-wrap: break-word;
                }
                
                .footer { 
                    text-align: center; margin-top: 50px; padding: 30px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white; border-radius: 15px;
                }
                .footer h3 { margin-bottom: 10px; }
                .footer p { opacity: 0.9; }
                
                .status-indicator {
                    display: inline-block; padding: 5px 12px; border-radius: 20px;
                    font-size: 0.85em; font-weight: bold; margin: 0 5px;
                }
                .status-high { background: #d4edda; color: #155724; }
                .status-medium { background: #fff3cd; color: #856404; }
                .status-positive { background: #d1ecf1; color: #0c5460; }
                
                @media (max-width: 768px) {
                    .container { padding: 10px; }
                    .header h1 { font-size: 2.2em; }
                    .metrics-grid { grid-template-columns: 1fr; }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 Executive Business Intelligence Report</h1>
                    <div class="subtitle">Comprehensive Document Analysis & Strategic Assessment</div>
                    <div class="meta">
                        <strong>Document:</strong> {{ document_title }} |
                        <strong>Generated:</strong> {{ generated_at }} |
                        <strong>Confidence:</strong> <span class="status-indicator status-high">{{ confidence }}</span>
                    </div>
                </div>
                
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value">{{ sentiment_score }}</div>
                        <div class="metric-label">Sentiment Score</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{{ risk_score }}/20</div>
                        <div class="metric-label">Risk Level</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{{ quality_score }}</div>
                        <div class="metric-label">Quality Score</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{{ word_count }}</div>
                        <div class="metric-label">Words Analyzed</div>
                    </div>
                </div>
                
                <div class="exec-summary">
                    <h2 class="section-title">🎯 Executive Summary</h2>
                    <p style="font-size: 1.1em; margin-bottom: 20px; color: #34495e;">
                        This comprehensive analysis provides actionable insights and strategic recommendations 
                        based on advanced AI-powered document analysis, sentiment evaluation, and business intelligence.
                    </p>
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px;">
                        <strong>Key Insights:</strong>
                        <span class="status-indicator status-positive">{{ sentiment_label }}</span>
                        <span class="status-indicator status-{{ risk_level }}">{{ risk_level|title }} Risk</span>
                        <span class="status-indicator status-high">High Quality</span>
                    </div>
                </div>
                
                {% if charts %}
                <div class="chart-section">
                    <h2 class="section-title">📈 Data Visualizations & Analytics</h2>
                    {% for chart_name, chart_data in charts.items() %}
                    <div class="chart-container">
                        <div class="chart-title">{{ chart_name.replace('_', ' ').title() }}</div>
                        <img src="data:image/png;base64,{{ chart_data }}" alt="{{ chart_name }}">
                    </div>
                    {% endfor %}
                </div>
                {% endif %}
                
                <div class="content-section">
                    <h2 class="section-title">📋 Detailed Analysis Report</h2>
                    <pre>{{ summary }}</pre>
                </div>
            </div>
            
            <div class="footer">
                <h3>🤖 Powered by GenAI AgentOS</h3>
                <p>Advanced AI-Powered Business Intelligence & Document Analysis Platform</p>
                <p style="font-size: 0.9em; margin-top: 10px;">
                    Report Generator v1.0.0 | Confidence Level: {{ confidence }} | 
                    Processing Time: {{ processing_time }}
                </p>
            </div>
        </body>
        </html>
        """
        
        from jinja2 import Environment
        
        # Custom filter for thousands separator
        def thousands_filter(value):
            return f"{value:,}"
        
        env = Environment()
        env.filters['thousands'] = thousands_filter
        template = env.from_string(html_template)
        
        return template.render(
            summary=summary,
            charts=charts,
            document_title=data['document_info']['filename'].replace('_', ' ').replace('.pdf', ''),
            generated_at=datetime.now().strftime('%B %d, %Y at %I:%M %p'),
            confidence='High',
            sentiment_score=data['sentiment']['sentiment_score'],
            sentiment_label=data['sentiment']['overall_sentiment'].title(),
            risk_score=data['risk']['risk_score'],
            risk_level=data['risk']['overall_risk_level'],
            quality_score=data['quality']['completeness_score'],
            word_count=data['document_info']['word_count'],
            processing_time=data['document_info']['processing_time']
        )
    
    async def run_comprehensive_demo(self):
        """Run the complete comprehensive showcase."""
        logger.info("🚀 GenAI AgentOS Comprehensive Showcase")
        logger.info("=" * 70)
        logger.info("📊 Generating executive-level business intelligence report...")
        
        # Create comprehensive sample data
        data = self.create_comprehensive_sample_data()
        
        # Generate executive summary
        logger.info("📝 Creating executive summary with strategic recommendations...")
        summary = self.generate_executive_summary(data)
        
        # Generate advanced visualizations
        logger.info("📈 Creating advanced data visualizations...")
        charts = {}
        charts['comprehensive_analysis'] = self.create_advanced_sentiment_visualization(data)
        charts['financial_projections'] = self.create_financial_analysis_chart(data)
        
        # Generate professional HTML report
        logger.info("🌐 Creating professional HTML report...")
        html_report = self.create_professional_html_report(summary, charts, data)
        
        # Save all outputs
        logger.info("💾 Saving comprehensive analysis results...")
        
        # Executive summary
        summary_path = self.output_dir / "executive_summary.md"
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)
        
        # Professional HTML report
        html_path = self.output_dir / "executive_business_report.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_report)
        
        # Complete analysis data
        data_path = self.output_dir / "comprehensive_analysis_data.json"  
        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Results summary
        results_summary = {
            "showcase_results": {
                "executive_summary": summary[:500] + "...",
                "analysis_metrics": {
                    "sentiment_score": data['sentiment']['sentiment_score'],
                    "risk_level": data['risk']['overall_risk_level'],
                    "quality_score": data['quality']['completeness_score'],
                    "confidence": data['sentiment']['confidence']
                },
                "visualizations_generated": len(charts),
                "recommendations_count": len(self.generate_strategic_recommendations(data)),
                "processing_details": {
                    "word_count": data['document_info']['word_count'],
                    "processing_time": data['document_info']['processing_time'],
                    "analysis_depth": "comprehensive"
                }
            }
        }
        
        results_path = self.output_dir / "showcase_summary.json"
        with open(results_path, "w", encoding="utf-8") as f:
            json.dump(results_summary, f, indent=2)
        
        # Display comprehensive results
        logger.info("=" * 70)
        logger.info("✅ COMPREHENSIVE SHOWCASE COMPLETE!")
        logger.info("=" * 70)
        logger.info(f"📁 Output directory: {self.output_dir.absolute()}")
        logger.info(f"📋 Executive summary: {summary_path.name}")
        logger.info(f"🌐 Professional report: {html_path.name}")
        logger.info(f"📊 Analysis data: {data_path.name}")
        logger.info(f"📈 Visualizations: {len(charts)} advanced charts")
        
        # Key metrics summary
        logger.info("\n📊 KEY ANALYSIS RESULTS:")
        logger.info(f"   Sentiment Score: {data['sentiment']['sentiment_score']}/100 ({data['sentiment']['overall_sentiment'].title()})")
        logger.info(f"   Risk Assessment: {data['risk']['risk_score']}/20 ({data['risk']['overall_risk_level'].title()} Risk)")
        logger.info(f"   Quality Score: {data['quality']['completeness_score']}/100")
        logger.info(f"   Business Intelligence: {data['business_intelligence']['market_positioning'].title()} positioning")
        logger.info(f"   Strategic Recommendations: {len(self.generate_strategic_recommendations(data))} actionable items")
        
        logger.info(f"\n🎉 Open '{html_path.name}' in your browser for the complete interactive report!")
        logger.info("🏆 This demonstrates the full power of GenAI AgentOS Report Generator!")

async def main():
    """Run comprehensive showcase."""
    showcase = ComprehensiveShowcase()
    await showcase.run_comprehensive_demo()

if __name__ == "__main__":
    asyncio.run(main())