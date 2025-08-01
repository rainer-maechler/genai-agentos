#!/usr/bin/env python3
"""
Upload Sample Documents Script

This script creates and uploads sample documents for the GenAI AgentOS showcase.
It generates realistic business documents that demonstrate the pipeline capabilities.
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, List
import requests
from loguru import logger
from datetime import datetime, timedelta
import tempfile

# For document generation
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

# Configuration
BACKEND_URL = "http://localhost:8000"
SAMPLE_DATA_DIR = Path(__file__).parent / "sample_data"

class SampleDataGenerator:
    """Generates sample documents for the showcase."""
    
    def __init__(self):
        self.sample_data_dir = SAMPLE_DATA_DIR
        self.sample_data_dir.mkdir(exist_ok=True)
        self.session_token = None
        
        # Sample document templates
        self.sample_documents = {
            "sample_proposal.pdf": {
                "type": "business_proposal",
                "title": "Digital Transformation Initiative Proposal",
                "content": self._get_proposal_content()
            },
            "market_analysis.txt": {
                "type": "market_report", 
                "title": "Q4 2024 Market Analysis Report",
                "content": self._get_market_analysis_content()
            },
            "contract_review.txt": {
                "type": "legal_document",
                "title": "Software License Agreement Review",
                "content": self._get_contract_content()
            },
            "financial_summary.txt": {
                "type": "financial_report",
                "title": "Annual Financial Performance Summary",
                "content": self._get_financial_content()
            }
        }
    
    def _get_proposal_content(self) -> str:
        """Generate business proposal content."""
        return """
DIGITAL TRANSFORMATION INITIATIVE PROPOSAL

Client: TechCorp Industries
Date: December 15, 2024
Prepared by: Innovation Consulting Group

EXECUTIVE SUMMARY

We are excited to propose a comprehensive digital transformation initiative for TechCorp Industries. This strategic project will modernize your technology infrastructure, streamline business processes, and position your organization for sustainable growth in the digital economy.

The proposed solution will deliver significant value through improved operational efficiency, enhanced customer experience, and reduced operational costs. Our analysis indicates potential efficiency improvements of 40% and annual cost savings of $2.3M.

KEY BENEFITS AND DELIVERABLES

1. Automated Workflow Systems
   - Implementation of intelligent process automation
   - Reduction of manual tasks by 60%
   - Improved accuracy and consistency in operations

2. Enhanced Data Analytics Platform
   - Real-time business intelligence dashboard
   - Predictive analytics capabilities
   - Data-driven decision making framework

3. Customer Experience Optimization
   - Omnichannel customer portal
   - AI-powered customer support
   - Personalized service delivery

4. Cloud Infrastructure Migration
   - Scalable cloud-native architecture
   - Enhanced security and compliance
   - Improved system reliability and performance

INVESTMENT AND TIMELINE

Total Investment Required: $5.8M over 18 months
Phase 1 (Months 1-6): Infrastructure Setup - $2.1M
Phase 2 (Months 7-12): System Implementation - $2.4M  
Phase 3 (Months 13-18): Integration & Optimization - $1.3M

Expected Return on Investment: 180% within 3 years
Payback Period: 24 months
Net Present Value: $8.2M over 5 years

RISK ASSESSMENT

Low Risk Factors:
- Proven technology stack
- Experienced implementation team
- Strong executive support

Medium Risk Factors:
- User adoption and change management
- Integration complexity with legacy systems
- Resource availability during peak periods

Mitigation Strategies:
- Comprehensive training and support program
- Phased implementation approach
- Dedicated project management office

NEXT STEPS

We recommend proceeding with a detailed technical assessment and project planning phase. This will include stakeholder interviews, system architecture design, and detailed implementation timeline.

We look forward to partnering with TechCorp Industries on this exciting digital transformation journey. Our team is committed to delivering exceptional results and ensuring the success of this strategic initiative.

For questions or to schedule a detailed presentation, please contact:
Sarah Johnson, Project Director
Email: sarah.johnson@innovationconsulting.com
Phone: (555) 123-4567
        """
    
    def _get_market_analysis_content(self) -> str:
        """Generate market analysis content."""
        return """
Q4 2024 MARKET ANALYSIS REPORT

Industry: Enterprise Software Solutions
Report Date: January 15, 2025
Analyst: Market Intelligence Division

MARKET OVERVIEW

The enterprise software market demonstrated remarkable resilience and growth in Q4 2024, with total market value reaching $847 billion, representing a 12.3% year-over-year increase. Cloud-native solutions continue to dominate market adoption, accounting for 68% of new deployments.

Key market drivers include increased demand for automation, artificial intelligence integration, and remote collaboration capabilities. Organizations are prioritizing solutions that offer immediate ROI and long-term scalability.

COMPETITIVE LANDSCAPE

Market Leaders:
1. Microsoft Corporation - 23.4% market share
2. Salesforce Inc. - 18.7% market share  
3. Oracle Corporation - 15.2% market share
4. SAP SE - 12.9% market share
5. ServiceNow Inc. - 8.3% market share

Emerging Players:
- Specialized AI/ML platforms showing 45% growth
- Industry-specific solutions gaining traction
- Open-source alternatives capturing 12% market share

GROWTH OPPORTUNITIES

High-Growth Segments:
- Artificial Intelligence and Machine Learning: 35% CAGR
- Cybersecurity Solutions: 28% CAGR
- Customer Experience Platforms: 22% CAGR
- Data Analytics and BI: 19% CAGR

Geographic Expansion:
- Asia-Pacific region showing strongest growth at 24%
- European market stabilizing with 8% growth
- North American market maturing at 6% growth

MARKET CHALLENGES

Primary Concerns:
- Talent shortage in technical roles
- Increasing cybersecurity threats
- Economic uncertainty affecting IT budgets
- Rapid technology evolution requiring constant adaptation

Regulatory Environment:
- Data privacy regulations becoming more stringent
- Industry-specific compliance requirements increasing
- Cross-border data transfer restrictions tightening

RECOMMENDATIONS

Strategic Priorities:
1. Invest in AI and automation capabilities
2. Strengthen cybersecurity offerings
3. Expand into emerging markets
4. Focus on industry-specific solutions
5. Build strategic partnerships with cloud providers

Investment Areas:
- Research and development: Increase by 25%
- Market expansion: Target APAC region
- Talent acquisition: Focus on AI/ML expertise
- Customer success programs: Reduce churn by 15%

FORECAST

Market projections for 2025 indicate continued growth at 14-16% annually. Organizations that adapt quickly to AI integration and maintain strong customer relationships will capture the majority of market growth.

The competitive landscape will likely see consolidation among smaller players, while market leaders invest heavily in next-generation technologies to maintain their positions.

Success factors for 2025:
- Customer-centric innovation
- Agile development methodologies  
- Strong ecosystem partnerships
- Focus on measurable business outcomes
        """
    
    def _get_contract_content(self) -> str:
        """Generate contract review content."""
        return """
SOFTWARE LICENSE AGREEMENT REVIEW

Document: Enterprise Software License Agreement v2.4
Client: TechCorp Industries
Review Date: January 10, 2025
Legal Counsel: Thompson & Associates

EXECUTIVE SUMMARY

This review analyzes the proposed Enterprise Software License Agreement for TechCorp Industries' new customer relationship management system. The agreement presents generally favorable terms with some areas requiring negotiation to better align with company interests.

Overall Risk Assessment: MEDIUM
Recommendation: Proceed with negotiations on identified terms

KEY CONTRACTUAL TERMS

Licensing Model:
- Named user licensing at $150/user/month
- Minimum commitment: 500 users
- Term: 3 years with automatic renewal
- Volume discounts available for 1000+ users

Payment Terms:
- Annual payment in advance
- 30-day payment terms
- Late payment penalty: 1.5% per month
- Price escalation: 5% annually (NEGOTIATION REQUIRED)

Service Level Agreements:
- 99.5% uptime guarantee
- 4-hour response time for critical issues
- 24/7 technical support included
- Planned maintenance windows: 4 hours monthly

AREAS OF CONCERN

1. Liability Limitations
Current Terms: Vendor liability capped at 12 months of fees
Recommendation: Negotiate for uncapped liability for data breaches and IP violations

2. Data Ownership and Privacy
Current Terms: Vendor retains analytics rights to aggregated data
Recommendation: Restrict data usage and require explicit consent

3. Termination Clauses
Current Terms: 90-day notice required, data export limited to 30 days
Recommendation: Extend data retention to 180 days, add termination for convenience

4. Intellectual Property Rights
Current Terms: Vendor retains all IP rights, customer configurations not protected
Recommendation: Secure rights to custom configurations and integrations

COMPLIANCE ASSESSMENT

Regulatory Compliance:
✓ GDPR compliance measures included
✓ SOC 2 Type II certification provided
✓ HIPAA requirements addressed (if applicable)
⚠ Industry-specific regulations need verification

Security Requirements:
✓ Encryption at rest and in transit
✓ Multi-factor authentication supported
✓ Regular security audits conducted
⚠ Penetration testing reports need review

FINANCIAL ANALYSIS

Year 1 Costs: $1,125,000 (750 users × $150 × 12 months)
Year 2 Costs: $1,181,250 (5% increase)
Year 3 Costs: $1,240,313 (5% increase)
Total 3-Year Cost: $3,546,563

Cost Comparison:
- 15% higher than current solution
- Includes additional functionality worth estimated $200K annually
- ROI expected within 18 months through efficiency gains

NEGOTIATION PRIORITIES

High Priority:
1. Reduce annual price escalation to 3%
2. Increase liability caps for critical breaches
3. Extend data retention period post-termination
4. Add termination for convenience clause

Medium Priority:
1. Volume discount at 750 users instead of 1000
2. Quarterly payment option
3. Enhanced SLA for business-critical hours
4. Additional training credits included

RECOMMENDATIONS

1. PROCEED with contract negotiations focusing on identified priority items
2. ENGAGE technical team to validate security and integration requirements  
3. COORDINATE with procurement to explore competitive alternatives
4. SCHEDULE executive review before final signature

The proposed agreement provides a solid foundation for a strategic technology partnership. With appropriate negotiations on key terms, this contract can deliver significant value while protecting TechCorp's interests.

Risk mitigation strategies should be implemented regardless of contract terms, including data backup procedures, contingency planning, and regular compliance audits.
        """
    
    def _get_financial_content(self) -> str:
        """Generate financial report content."""
        return """
ANNUAL FINANCIAL PERFORMANCE SUMMARY

Company: TechCorp Industries
Fiscal Year: 2024
Report Date: January 20, 2025

EXECUTIVE OVERVIEW

TechCorp Industries delivered strong financial performance in FY2024, with revenue growth of 18.2% and improved operational efficiency across all business segments. The company successfully navigated market challenges while maintaining profitability and investing in strategic growth initiatives.

Key Performance Highlights:
- Total Revenue: $847.3M (vs $717.2M in 2023)
- Net Income: $127.4M (vs $98.6M in 2023)  
- Operating Margin: 22.1% (vs 19.3% in 2023)
- EBITDA: $187.2M (vs $142.8M in 2023)

REVENUE ANALYSIS

Revenue by Segment:
- Enterprise Solutions: $423.7M (50.0% of total, +22% YoY)
- Cloud Services: $254.2M (30.0% of total, +28% YoY)
- Professional Services: $127.4M (15.0% of total, +8% YoY)
- Support & Maintenance: $42.0M (5.0% of total, +5% YoY)

Geographic Revenue Distribution:
- North America: $508.4M (60.0%)
- Europe: $220.0M (26.0%)
- Asia-Pacific: $101.7M (12.0%)
- Other Markets: $17.2M (2.0%)

Customer Metrics:
- Total Active Customers: 2,847 (vs 2,134 in 2023)
- Customer Retention Rate: 94.2%
- Average Contract Value: $298K (vs $274K in 2023)
- Net Revenue Retention: 112%

PROFITABILITY ANALYSIS

Gross Profit Margins:
- Enterprise Solutions: 68.4%
- Cloud Services: 72.1%
- Professional Services: 34.2%
- Support & Maintenance: 78.9%

Operating Expenses:
- Sales & Marketing: $254.2M (30.0% of revenue)
- Research & Development: $152.5M (18.0% of revenue)
- General & Administrative: $84.7M (10.0% of revenue)
- Total Operating Expenses: $491.4M

Cost Management Initiatives:
- Automation reduced operational costs by $12.3M
- Cloud migration saved $8.7M in infrastructure costs
- Process optimization delivered $15.2M in efficiency gains

CASH FLOW AND BALANCE SHEET

Cash Flow Statement:
- Operating Cash Flow: $164.8M (vs $128.3M in 2023)
- Free Cash Flow: $142.1M (vs $108.7M in 2023)
- Capital Expenditures: $22.7M
- Cash Conversion Cycle: 42 days

Balance Sheet Highlights:
- Total Assets: $623.4M
- Cash and Equivalents: $187.9M
- Total Debt: $89.2M
- Shareholders' Equity: $423.7M
- Debt-to-Equity Ratio: 0.21

INVESTMENT AND GROWTH

Strategic Investments:
- AI and Machine Learning Platform: $28.4M
- Market Expansion (APAC): $15.7M
- Cybersecurity Enhancement: $12.1M
- Talent Acquisition: $23.8M

Merger and Acquisition Activity:
- Acquired DataInsights Inc. for $45M in Q3
- Strategic partnership with CloudTech Solutions
- Investment in three early-stage AI startups

RISK FACTORS AND CHALLENGES

Market Risks:
- Increasing competition from established players
- Economic uncertainty affecting customer spending
- Rapid technology evolution requiring constant innovation

Operational Risks:
- Talent retention in competitive market
- Cybersecurity threats and data protection
- Supply chain disruptions affecting hardware components

Financial Risks:
- Foreign exchange rate fluctuations
- Credit risk from large enterprise customers
- Interest rate changes affecting borrowing costs

OUTLOOK FOR 2025

Revenue Projections:
- Target Revenue: $950M - $1,000M (+12-18% growth)
- New Customer Acquisition: 700-800 customers
- Geographic Expansion: 25% growth in APAC region

Investment Priorities:
- Product Innovation: $180M (+18% vs 2024)
- Market Expansion: $45M
- Infrastructure Scaling: $35M
- Strategic Acquisitions: $100M allocation

Profitability Targets:
- Operating Margin: 23-25%
- EBITDA Margin: 24-26%
- Free Cash Flow Margin: 16-18%

The company is well-positioned for continued growth with strong fundamentals, innovative product portfolio, and expanding market opportunities. Management remains confident in achieving 2025 targets while maintaining operational excellence and profitability.
        """
    
    def generate_pdf_document(self, filename: str, title: str, content: str):
        """Generate a PDF document from text content."""
        pdf_path = self.sample_data_dir / filename
        
        try:
            doc = SimpleDocTemplate(str(pdf_path), pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=20,
                alignment=1  # Center
            )
            story.append(Paragraph(title, title_style))
            story.append(Spacer(1, 20))
            
            # Content paragraphs
            paragraphs = content.strip().split('\n\n')
            for para in paragraphs:
                if para.strip():
                    if para.strip().isupper() and len(para.strip()) < 100:
                        # Section headers
                        story.append(Paragraph(para.strip(), styles['Heading2']))
                        story.append(Spacer(1, 10))
                    else:
                        # Regular content
                        story.append(Paragraph(para.strip(), styles['Normal']))
                        story.append(Spacer(1, 8))
            
            doc.build(story)
            logger.info(f"✅ Generated PDF: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error generating PDF {filename}: {str(e)}")
            return False
    
    def generate_text_document(self, filename: str, content: str):
        """Generate a text document."""
        text_path = self.sample_data_dir / filename
        
        try:
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(content.strip())
            logger.info(f"✅ Generated text file: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error generating text file {filename}: {str(e)}")
            return False
    
    def generate_all_samples(self):
        """Generate all sample documents."""
        logger.info("📝 Generating sample documents...")
        
        success_count = 0
        for filename, doc_info in self.sample_documents.items():
            if filename.endswith('.pdf'):
                if self.generate_pdf_document(filename, doc_info['title'], doc_info['content']):
                    success_count += 1
            else:
                if self.generate_text_document(filename, doc_info['content']):
                    success_count += 1
        
        logger.info(f"Generated {success_count}/{len(self.sample_documents)} sample documents")
        return success_count == len(self.sample_documents)
    
    def authenticate(self, username: str = "demo", password: str = "demo") -> bool:
        """Authenticate with the backend."""
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/v1/users/login_access_token",
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
    
    def upload_sample_documents(self):
        """Upload generated sample documents to the system."""
        if not self.session_token:
            logger.error("❌ Not authenticated. Cannot upload documents.")
            return False
        
        logger.info("📤 Uploading sample documents...")
        
        headers = {"Authorization": f"Bearer {self.session_token}"}
        success_count = 0
        
        for filename in self.sample_documents.keys():
            file_path = self.sample_data_dir / filename
            
            if not file_path.exists():
                logger.warning(f"⚠️  Sample file not found: {filename}")
                continue
            
            try:
                with open(file_path, 'rb') as f:
                    files = {"file": (filename, f)}
                    response = requests.post(
                        f"{BACKEND_URL}/api/v1/files/upload",
                        files=files,
                        headers=headers,
                        timeout=30
                    )
                
                if response.status_code == 200:
                    file_data = response.json()
                    logger.info(f"✅ Uploaded {filename} (ID: {file_data.get('file_id')})")
                    success_count += 1
                else:
                    logger.error(f"❌ Failed to upload {filename}: {response.status_code}")
                    
            except Exception as e:
                logger.error(f"❌ Error uploading {filename}: {str(e)}")
        
        logger.info(f"Uploaded {success_count}/{len(self.sample_documents)} documents")
        return success_count > 0

def main():
    """Main function to generate and upload sample documents."""
    generator = SampleDataGenerator()
    
    logger.info("🎯 GenAI AgentOS Showcase - Sample Data Setup")
    logger.info("=" * 50)
    
    # Generate sample documents
    if not generator.generate_all_samples():
        logger.error("❌ Failed to generate sample documents")
        sys.exit(1)
    
    logger.info("\n📁 Sample documents generated successfully!")
    logger.info(f"Location: {generator.sample_data_dir}")
    logger.info("Files created:")
    for filename in generator.sample_documents.keys():
        file_path = generator.sample_data_dir / filename
        if file_path.exists():
            size_kb = file_path.stat().st_size / 1024
            logger.info(f"  - {filename} ({size_kb:.1f} KB)")
    
    # Optional: Upload to system if backend is available
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            logger.info("\n🔄 Backend detected. Uploading sample documents...")
            
            if generator.authenticate():
                generator.upload_sample_documents()
                logger.info("\n🎉 Sample documents uploaded successfully!")
                logger.info("You can now run: python run_showcase.py")
            else:
                logger.warning("⚠️  Authentication failed. Documents generated but not uploaded.")
        else:
            logger.info("\n⚠️  Backend not available. Documents generated locally only.")
            logger.info("Start the system with 'make up' and re-run to upload documents.")
            
    except Exception:
        logger.info("\n⚠️  Backend not available. Documents generated locally only.")
        logger.info("Start the system with 'make up' and re-run to upload documents.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Sample data setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Sample data setup failed: {str(e)}")
        sys.exit(1)