#!/usr/bin/env python3
"""
Report Generator Agent for GenAI AgentOS Showcase

This agent creates formatted reports and visualizations.
Capabilities:
- Executive summary generation
- Chart and graph creation
- Formatted output (PDF, HTML, JSON)
- Template-based reporting
- Data visualization
"""

import asyncio
import json
import tempfile
from typing import Dict, Any, List
from datetime import datetime, timedelta
from pathlib import Path
import base64
import io
from loguru import logger

# Reporting and visualization imports
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from jinja2 import Template

# GenAI Protocol
from genai_protocol import GenAISession


class ReportGeneratorAgent:
    """Agent that generates comprehensive reports and visualizations."""
    
    def __init__(self):
        self.name = "report_generator"
        self.description = "Generates formatted reports, visualizations, and executive summaries"
        self.version = "1.0.0"
        
        # Report templates
        self.templates = {
            "executive_summary": """
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
{% if risk.detected_risks %}
- **Key Risk Areas**: {{ risk.detected_risks.keys()|list|join(', ')|title }}
{% endif %}

## Business Metrics
{% if metrics.has_financial_data %}
- **Financial Data**: Present
{% endif %}
{% if metrics.roi_indicators %}
- **ROI Indicators**: {{ metrics.roi_indicators|join(', ') }}
{% endif %}

## Recommendations
{% for recommendation in recommendations %}
1. {{ recommendation }}
{% endfor %}

---
*Report generated on {{ generated_at }} by GenAI AgentOS*
            """,
            
            "detailed_report": """
# Comprehensive Analysis Report

**Document**: {{ document_title }}  
**Analysis Date**: {{ generated_at }}  
**Processing Time**: {{ processing_time }}  

## Document Information
- **Document Type**: {{ document_info.document_type|title }}
- **Word Count**: {{ document_info.word_count }}
- **Language**: {{ document_info.language }}
- **Quality Score**: {{ document_info.quality_score }}/100

## Content Analysis

### Topics and Themes
**Primary Focus**: {{ topics.primary_focus|title }}
{% for category, phrases in topics.categorized_topics.items() %}
- **{{ category|title }}**: {{ phrases|join(', ') }}
{% endfor %}

### Extracted Entities
{% for entity_type, values in entities.items() %}
- **{{ entity_type|title }}**: {{ values|join(', ') }}
{% endfor %}

## Sentiment & Emotional Analysis

### Overall Sentiment
- **Sentiment**: {{ sentiment.overall_sentiment|title }}
- **Polarity**: {{ sentiment.polarity }} (-1 to +1 scale)
- **Subjectivity**: {{ sentiment.subjectivity }} (0 to 1 scale)
- **Intensity**: {{ sentiment.intensity|title }}

### Emotional Profile
{% if emotions.emotions_detected %}
{% for emotion in emotions.emotions_detected %}
- **{{ emotion|title }}**: {{ emotions.emotion_percentages[emotion] }}%
{% endfor %}
{% endif %}

### Business Sentiment
- **Business Tone**: {{ business_sentiment.business_tone|title }}
- **Financial Sentiment**: {{ business_sentiment.financial_sentiment.sentiment|title }}
- **Performance Sentiment**: {{ business_sentiment.performance_sentiment.sentiment|title }}

## Risk Analysis

### Risk Assessment
- **Overall Risk Level**: {{ risk.overall_risk_level|title }}
- **Risk Score**: {{ risk.risk_score }}/20

{% if risk.detected_risks %}
### Identified Risk Categories
{% for risk_type, details in risk.detected_risks.items() %}
- **{{ risk_type|title }}**: {{ details.severity|title }} severity ({{ details.count }} indicators)
{% endfor %}
{% endif %}

### Risk Recommendations
{% for rec in risk.recommendations %}
- {{ rec }}
{% endfor %}

## Business Intelligence

### Performance Metrics
{% if metrics.performance_indicators %}
- **Performance Indicators**: {{ metrics.performance_indicators|join(', ') }}
{% endif %}
{% if metrics.growth_indicators %}
- **Growth Indicators**: {{ metrics.growth_indicators|join(', ') }}
{% endif %}

### Compliance Analysis
{% if compliance.frameworks_identified %}
- **Compliance Frameworks**: {{ compliance.frameworks_identified|join(', ')|upper }}
- **Compliance Focus**: {{ compliance.compliance_focus|title }}
{% endif %}

## Quality Assessment
- **Content Quality**: {{ quality.quality_level|title }}
- **Structure Complexity**: {{ quality.structure_complexity|title }}
{% if quality.quality_factors %}
- **Quality Factors**: {{ quality.quality_factors|join(', ') }}
{% endif %}

## Insights and Recommendations

### Key Insights
{% for insight in insights.key_findings %}
- {{ insight }}
{% endfor %}

### Recommended Actions
{% for recommendation in insights.recommendations %}
1. {{ recommendation }}
{% endfor %}

{% if insights.opportunities %}
### Opportunities
{% for opportunity in insights.opportunities %}
- {{ opportunity }}
{% endfor %}
{% endif %}

{% if insights.concerns %}
### Areas of Concern
{% for concern in insights.concerns %}
- {{ concern }}
{% endfor %}
{% endif %}

---
**Analysis Confidence**: {{ analysis_summary.analysis_confidence|title }}  
**Report Generated**: {{ generated_at }}  
**Agent**: {{ agent_name }} v{{ agent_version }}
            """
        }
        
        # Chart color schemes
        self.color_schemes = {
            'sentiment': ['#2E8B57', '#FFD700', '#DC143C'],  # Green, Yellow, Red
            'emotions': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F'],
            'business': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'],
            'risk': ['#28a745', '#ffc107', '#dc3545']  # Green, Yellow, Red
        }
    
    async def process_message(self, session: GenAISession, message: str) -> Dict[str, Any]:
        """Process incoming message and generate reports."""
        try:
            # Parse the input message
            request = json.loads(message)
            
            # Extract all analysis data
            analysis_data = {
                'document_info': self._extract_document_info(request),
                'entities': request.get('entities', {}),
                'topics': request.get('topics', {}),
                'sentiment': request.get('sentiment_summary', {}),
                'emotions': request.get('emotions', {}),
                'business_sentiment': request.get('business_sentiment', {}),
                'risk': request.get('risk_analysis', {}),
                'metrics': request.get('business_metrics', {}),
                'compliance': request.get('compliance', {}),
                'quality': request.get('quality_assessment', {}),
                'insights': request.get('insights', {}),
                'analysis_summary': request.get('analysis_summary', {})
            }
            
            # Generate different report formats
            result = await self._generate_reports(analysis_data, request.get('options', {}))
            
            # Add agent metadata
            result.update({
                "agent": self.name,
                "generated_at": datetime.now().isoformat(),
                "status": "success"
            })
            
            logger.info("Successfully generated comprehensive reports")
            return result
            
        except json.JSONDecodeError:
            return {"error": "Invalid JSON input", "status": "error"}
        except Exception as e:
            logger.error(f"Error generating reports: {str(e)}")
            return {"error": str(e), "status": "error"}
    
    async def _generate_reports(self, data: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
        """Generate various report formats."""
        
        # Generate text reports
        executive_summary = self._generate_executive_summary(data)
        detailed_report = self._generate_detailed_report(data)
        
        # Generate visualizations
        charts = await self._generate_charts(data)
        
        # Generate formatted reports
        formatted_reports = {}
        
        # HTML Report
        if options.get('include_html', True):
            formatted_reports['html'] = self._generate_html_report(detailed_report, charts)
        
        # PDF Report (simplified version)
        if options.get('include_pdf', True):
            formatted_reports['pdf_data'] = await self._generate_pdf_report(data, charts)
        
        # JSON Report
        formatted_reports['json'] = self._generate_json_report(data)
        
        return {
            "executive_summary": executive_summary,
            "detailed_report": detailed_report,
            "visualizations": charts,
            "formatted_reports": formatted_reports,
            "report_metadata": {
                "total_sections": len(detailed_report.split('\n## ')),
                "chart_count": len(charts),
                "report_formats": list(formatted_reports.keys()),
                "analysis_confidence": data.get('analysis_summary', {}).get('analysis_confidence', 'medium')
            }
        }
    
    def _extract_document_info(self, request: Dict) -> Dict[str, Any]:
        """Extract document information from request."""
        return {
            'document_type': request.get('document_type', 'unknown'),
            'filename': request.get('filename', 'Unknown Document'),
            'word_count': request.get('statistics', {}).get('word_count', 0),
            'language': request.get('language', {}).get('name', 'Unknown'),
            'quality_score': request.get('quality_assessment', {}).get('quality_score', 0)
        }
    
    def _generate_executive_summary(self, data: Dict[str, Any]) -> str:
        """Generate executive summary using template."""
        try:
            template = Template(self.templates['executive_summary'])
            
            # Prepare template data
            template_data = {
                'document_title': data['document_info'].get('filename', 'Document Analysis'),
                'overview': self._create_overview(data),
                'key_findings': self._extract_key_findings(data),
                'sentiment': data['sentiment'],
                'risk': data['risk'],
                'metrics': data['metrics'],
                'recommendations': self._generate_executive_recommendations(data),
                'generated_at': datetime.now().strftime('%B %d, %Y at %I:%M %p')
            }
            
            return template.render(**template_data)
            
        except Exception as e:
            logger.error(f"Error generating executive summary: {str(e)}")
            return f"Error generating executive summary: {str(e)}"
    
    def _generate_detailed_report(self, data: Dict[str, Any]) -> str:
        """Generate detailed report using template."""
        try:
            template = Template(self.templates['detailed_report'])
            
            # Prepare template data
            template_data = {
                **data,
                'document_title': data['document_info'].get('filename', 'Document Analysis'),
                'generated_at': datetime.now().strftime('%B %d, %Y at %I:%M %p'),
                'processing_time': '2-5 seconds',
                'agent_name': self.name,
                'agent_version': self.version
            }
            
            return template.render(**template_data)
            
        except Exception as e:
            logger.error(f"Error generating detailed report: {str(e)}")
            return f"Error generating detailed report: {str(e)}"
    
    def _create_overview(self, data: Dict[str, Any]) -> str:
        """Create overview text for executive summary."""
        doc_info = data['document_info']
        sentiment = data['sentiment']
        risk = data['risk']
        
        overview_parts = []
        
        # Document type and size
        overview_parts.append(f"Analysis of {doc_info.get('document_type', 'document')} containing {doc_info.get('word_count', 0)} words.")
        
        # Sentiment
        sentiment_label = sentiment.get('overall_sentiment', 'neutral')
        overview_parts.append(f"Overall sentiment is {sentiment_label} with {sentiment.get('confidence', 0) * 100:.0f}% confidence.")
        
        # Risk level
        risk_level = risk.get('overall_risk_level', 'unknown')
        overview_parts.append(f"Risk assessment indicates {risk_level} risk level.")
        
        return ' '.join(overview_parts)
    
    def _extract_key_findings(self, data: Dict[str, Any]) -> List[str]:
        """Extract key findings from analysis data."""
        findings = []
        
        # Sentiment finding
        sentiment = data['sentiment']
        if sentiment.get('overall_sentiment') != 'neutral':
            findings.append(f"Strong {sentiment.get('overall_sentiment')} sentiment detected throughout document")
        
        # Risk findings
        risk = data['risk']
        if risk.get('risk_score', 0) > 5:
            findings.append(f"Multiple risk factors identified (score: {risk.get('risk_score')}/20)")
        
        # Business metrics
        metrics = data['metrics']
        if metrics.get('has_financial_data'):
            findings.append("Significant financial data and metrics present")
        
        # Topics
        topics = data['topics']
        primary_focus = topics.get('primary_focus', '')
        if primary_focus and primary_focus != 'general':
            findings.append(f"Primary focus area identified as {primary_focus}")
        
        # Quality
        quality = data['quality']
        quality_level = quality.get('quality_level', '')
        if quality_level in ['excellent', 'good']:
            findings.append(f"Content quality assessed as {quality_level}")
        
        return findings[:5]  # Return top 5 findings
    
    def _generate_executive_recommendations(self, data: Dict[str, Any]) -> List[str]:
        """Generate executive-level recommendations."""
        recommendations = []
        
        # Sentiment-based recommendations
        sentiment = data['sentiment']
        if sentiment.get('overall_sentiment') == 'negative':
            recommendations.append("Address negative sentiment factors to improve stakeholder perception")
        
        # Risk-based recommendations
        risk = data['risk']
        if risk.get('overall_risk_level') in ['high', 'medium']:
            recommendations.append("Develop comprehensive risk mitigation strategy")
        
        # Compliance recommendations
        compliance = data['compliance']
        if compliance.get('frameworks_identified'):
            recommendations.append("Ensure compliance with identified regulatory frameworks")
        
        # Quality recommendations
        quality = data['quality']
        if quality.get('quality_level') in ['fair', 'needs improvement']:
            recommendations.append("Improve content structure and clarity")
        
        # Business metrics recommendations
        metrics = data['metrics']
        if metrics.get('has_performance_data'):
            recommendations.append("Leverage performance data for strategic decision making")
        
        return recommendations[:4]  # Return top 4 recommendations
    
    async def _generate_charts(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Generate visualization charts."""
        charts = {}
        
        try:
            # Sentiment chart
            sentiment_chart = self._create_sentiment_chart(data['sentiment'], data['emotions'])
            if sentiment_chart:
                charts['sentiment_analysis'] = sentiment_chart
            
            # Risk assessment chart
            risk_chart = self._create_risk_chart(data['risk'])
            if risk_chart:
                charts['risk_assessment'] = risk_chart
            
            # Topics distribution chart
            topics_chart = self._create_topics_chart(data['topics'])
            if topics_chart:
                charts['topics_distribution'] = topics_chart
            
            # Business metrics chart
            if data['metrics'].get('has_financial_data') or data['metrics'].get('performance_indicators'):
                metrics_chart = self._create_metrics_chart(data['metrics'])
                if metrics_chart:
                    charts['business_metrics'] = metrics_chart
            
        except Exception as e:
            logger.error(f"Error generating charts: {str(e)}")
            charts['error'] = f"Chart generation failed: {str(e)}"
        
        return charts
    
    def _create_sentiment_chart(self, sentiment: Dict, emotions: Dict) -> str:
        """Create sentiment analysis chart."""
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            
            # Sentiment gauge
            sentiment_score = sentiment.get('sentiment_score', 50)
            colors = ['#DC143C' if sentiment_score < 40 else '#FFD700' if sentiment_score < 60 else '#2E8B57']
            
            ax1.barh(['Sentiment'], [sentiment_score], color=colors[0])
            ax1.set_xlim(0, 100)
            ax1.set_xlabel('Sentiment Score')
            ax1.set_title('Overall Sentiment')
            ax1.text(sentiment_score + 2, 0, f"{sentiment_score}%", va='center')
            
            # Emotions pie chart
            emotions_detected = emotions.get('emotions_detected', [])
            emotion_percentages = emotions.get('emotion_percentages', {})
            
            if emotions_detected and emotion_percentages:
                labels = [emotion.title() for emotion in emotions_detected[:6]]  # Top 6 emotions
                sizes = [emotion_percentages.get(emotion, 0) for emotion in emotions_detected[:6]]
                colors_emotions = self.color_schemes['emotions'][:len(labels)]
                
                ax2.pie(sizes, labels=labels, colors=colors_emotions, autopct='%1.1f%%', startangle=90)
                ax2.set_title('Emotional Profile')
            else:
                ax2.text(0.5, 0.5, 'No emotions detected', ha='center', va='center', transform=ax2.transAxes)
                ax2.set_title('Emotional Profile')
            
            plt.tight_layout()
            
            # Convert to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            chart_b64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return chart_b64
            
        except Exception as e:
            logger.error(f"Error creating sentiment chart: {str(e)}")
            return None
    
    def _create_risk_chart(self, risk: Dict) -> str:
        """Create risk assessment chart."""
        try:
            detected_risks = risk.get('detected_risks', {})
            if not detected_risks:
                return None
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            risk_types = list(detected_risks.keys())
            risk_counts = [detected_risks[risk_type]['count'] for risk_type in risk_types]
            severities = [detected_risks[risk_type]['severity'] for risk_type in risk_types]
            
            # Color map for severity
            severity_colors = {'low': '#28a745', 'medium': '#ffc107', 'high': '#dc3545'}
            colors = [severity_colors.get(severity, '#6c757d') for severity in severities]
            
            bars = ax.bar(risk_types, risk_counts, color=colors)
            ax.set_xlabel('Risk Categories')
            ax.set_ylabel('Number of Indicators')
            ax.set_title('Risk Assessment by Category')
            
            # Add value labels on bars
            for bar, count in zip(bars, risk_counts):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                       f'{count}', ha='center', va='bottom')
            
            # Add legend
            handles = [mpatches.Patch(color=color, label=severity.title()) 
                      for severity, color in severity_colors.items()]
            ax.legend(handles=handles, title='Severity')
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            # Convert to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            chart_b64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return chart_b64
            
        except Exception as e:
            logger.error(f"Error creating risk chart: {str(e)}")
            return None
    
    def _create_topics_chart(self, topics: Dict) -> str:
        """Create topics distribution chart."""
        try:
            categorized_topics = topics.get('categorized_topics', {})
            if not categorized_topics:
                return None
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            categories = list(categorized_topics.keys())
            topic_counts = [len(categorized_topics[category]) for category in categories]
            
            colors = self.color_schemes['business'][:len(categories)]
            bars = ax.bar(categories, topic_counts, color=colors)
            
            ax.set_xlabel('Topic Categories')
            ax.set_ylabel('Number of Topics')
            ax.set_title('Topic Distribution by Category')
            
            # Add value labels on bars
            for bar, count in zip(bars, topic_counts):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                       f'{count}', ha='center', va='bottom')
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            # Convert to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            chart_b64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return chart_b64
            
        except Exception as e:
            logger.error(f"Error creating topics chart: {str(e)}")
            return None
    
    def _create_metrics_chart(self, metrics: Dict) -> str:
        """Create business metrics chart."""
        try:
            fig, ax = plt.subplots(figsize=(8, 6))
            
            # Create a simple metrics overview
            metric_types = []
            metric_values = []
            
            if metrics.get('has_financial_data'):
                metric_types.append('Financial Data')
                metric_values.append(100)
            
            if metrics.get('has_performance_data'):
                metric_types.append('Performance Data')
                metric_values.append(100)
            
            roi_indicators = metrics.get('roi_indicators', [])
            if roi_indicators:
                metric_types.append('ROI Indicators')
                metric_values.append(len(roi_indicators) * 20)
            
            performance_indicators = metrics.get('performance_indicators', [])
            if performance_indicators:
                metric_types.append('Performance Metrics')
                metric_values.append(len(performance_indicators) * 15)
            
            if not metric_types:
                ax.text(0.5, 0.5, 'No metrics data available', ha='center', va='center', transform=ax.transAxes)
                ax.set_title('Business Metrics Overview')
            else:
                colors = self.color_schemes['business'][:len(metric_types)]
                bars = ax.bar(metric_types, metric_values, color=colors)
                
                ax.set_ylabel('Metric Score')
                ax.set_title('Business Metrics Overview')
                
                # Add value labels on bars
                for bar, value in zip(bars, metric_values):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                           f'{value}', ha='center', va='bottom')
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            # Convert to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            chart_b64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return chart_b64
            
        except Exception as e:
            logger.error(f"Error creating metrics chart: {str(e)}")
            return None
    
    def _generate_html_report(self, detailed_report: str, charts: Dict[str, str]) -> str:
        """Generate HTML formatted report."""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Document Analysis Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                h1, h2, h3 { color: #2c3e50; }
                .chart { text-align: center; margin: 20px 0; }
                .chart img { max-width: 100%; border: 1px solid #ddd; border-radius: 8px; }
                .summary-box { background: #f8f9fa; padding: 15px; border-left: 4px solid #007bff; margin: 20px 0; }
                pre { background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }
                table { border-collapse: collapse; width: 100%; margin: 15px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <div class="summary-box">
                <h2>📊 Document Analysis Report</h2>
                <p><strong>Generated:</strong> {{ generated_at }}</p>
                <p><strong>Agent:</strong> GenAI AgentOS Report Generator</p>
            </div>
            
            {% if charts %}
            <div class="charts">
                <h2>📈 Visualizations</h2>
                {% for chart_name, chart_data in charts.items() %}
                    {% if chart_data and chart_data != 'error' %}
                    <div class="chart">
                        <h3>{{ chart_name.replace('_', ' ').title() }}</h3>
                        <img src="data:image/png;base64,{{ chart_data }}" alt="{{ chart_name }}">
                    </div>
                    {% endif %}
                {% endfor %}
            </div>
            {% endif %}
            
            <div class="report-content">
                <pre>{{ detailed_report }}</pre>
            </div>
        </body>
        </html>
        """
        
        template = Template(html_template)
        return template.render(
            detailed_report=detailed_report,
            charts=charts,
            generated_at=datetime.now().strftime('%B %d, %Y at %I:%M %p')
        )
    
    async def _generate_pdf_report(self, data: Dict[str, Any], charts: Dict[str, str]) -> str:
        """Generate PDF report (returns base64 encoded PDF)."""
        try:
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
                # Create PDF document
                doc = SimpleDocTemplate(tmp_file.name, pagesize=letter)
                styles = getSampleStyleSheet()
                story = []
                
                # Title
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=24,
                    spaceAfter=30,
                    alignment=1  # Center alignment
                )
                story.append(Paragraph("Document Analysis Report", title_style))
                story.append(Spacer(1, 12))
                
                # Executive Summary
                story.append(Paragraph("Executive Summary", styles['Heading2']))
                
                doc_info = data['document_info']
                sentiment = data['sentiment']
                risk = data['risk']
                
                summary_text = f"""
                <b>Document:</b> {doc_info.get('filename', 'Unknown')}<br/>
                <b>Document Type:</b> {doc_info.get('document_type', 'Unknown').title()}<br/>
                <b>Word Count:</b> {doc_info.get('word_count', 0):,}<br/>
                <b>Overall Sentiment:</b> {sentiment.get('overall_sentiment', 'neutral').title()}<br/>
                <b>Risk Level:</b> {risk.get('overall_risk_level', 'unknown').title()}<br/>
                <b>Analysis Date:</b> {datetime.now().strftime('%B %d, %Y')}
                """
                
                story.append(Paragraph(summary_text, styles['Normal']))
                story.append(Spacer(1, 12))
                
                # Key Findings Table
                if data.get('insights', {}).get('key_findings'):
                    story.append(Paragraph("Key Findings", styles['Heading2']))
                    
                    findings_data = [['Finding', 'Description']]
                    for i, finding in enumerate(data['insights']['key_findings'][:5], 1):
                        findings_data.append([f"Finding {i}", finding])
                    
                    findings_table = Table(findings_data, colWidths=[1*inch, 4*inch])
                    findings_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 12),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    
                    story.append(findings_table)
                    story.append(Spacer(1, 12))
                
                # Build PDF
                doc.build(story)
                
                # Read and encode PDF
                with open(tmp_file.name, 'rb') as pdf_file:
                    pdf_data = pdf_file.read()
                    pdf_b64 = base64.b64encode(pdf_data).decode()
                
                # Clean up temp file
                Path(tmp_file.name).unlink()
                
                return pdf_b64
                
        except Exception as e:
            logger.error(f"Error generating PDF report: {str(e)}")
            return f"PDF generation failed: {str(e)}"
    
    def _generate_json_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate structured JSON report."""
        return {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "agent": self.name,
                "version": self.version,
                "report_type": "comprehensive_analysis"
            },
            "document_summary": {
                "filename": data['document_info'].get('filename'),
                "document_type": data['document_info'].get('document_type'),
                "word_count": data['document_info'].get('word_count'),
                "language": data['document_info'].get('language'),
                "quality_score": data.get('quality', {}).get('quality_score')
            },
            "analysis_results": {
                "sentiment_analysis": data['sentiment'],
                "emotion_analysis": data['emotions'],
                "risk_assessment": data['risk'],
                "business_intelligence": data['metrics'],
                "compliance_analysis": data['compliance'],
                "topic_analysis": data['topics']
            },
            "insights_and_recommendations": data['insights'],
            "quality_assessment": data['quality']
        }


async def main():
    """Main function to run the Report Generator Agent."""
    agent = ReportGeneratorAgent()
    
    # Connect to GenAI AgentOS
    session = GenAISession(
        ws_url="ws://localhost:8080/ws",
        agent_name=agent.name,
        agent_description=agent.description,
        agent_version=agent.version
    )
    
    logger.info(f"Starting {agent.name} agent...")
    
    try:
        await session.connect()
        logger.info("Connected to GenAI AgentOS")
        
        # Listen for messages
        async for message in session.listen():
            logger.info(f"Received message: {message.id}")
            
            try:
                result = await agent.process_message(session, message.content)
                await session.send_response(message.id, json.dumps(result))
                logger.info(f"Sent response for message: {message.id}")
                
            except Exception as e:
                error_response = {
                    "error": f"Processing failed: {str(e)}",
                    "status": "error",
                    "agent": agent.name
                }
                await session.send_response(message.id, json.dumps(error_response))
                logger.error(f"Error processing message {message.id}: {str(e)}")
                
    except KeyboardInterrupt:
        logger.info("Agent stopped by user")
    except Exception as e:
        logger.error(f"Agent error: {str(e)}")
    finally:
        await session.disconnect()
        logger.info("Agent disconnected")


if __name__ == "__main__":
    asyncio.run(main())