# GenAI AgentOS Showcase: Smart Document Analysis Pipeline

## Overview

This showcase demonstrates a complete document analysis pipeline using GenAI AgentOS. The scenario simulates a business intelligence system where multiple specialized agents work together to process documents, extract insights, and generate comprehensive reports.

## Scenario: Business Intelligence Document Pipeline

**Use Case**: A consulting firm needs to analyze client documents (contracts, reports, presentations) to extract key information, perform sentiment analysis, generate summaries, and create actionable insights.

### Workflow Stages

1. **Document Ingestion** → Document Parser Agent
2. **Content Extraction** → Text Extractor Agent  
3. **Information Analysis** → Analytics Agent
4. **Sentiment Analysis** → Sentiment Analyzer Agent
5. **Report Generation** → Report Generator Agent
6. **Quality Review** → QA Reviewer Agent

## Agent Architecture

```
Input Document
       ↓
[Document Parser] → [Text Extractor] → [Analytics Agent]
                                            ↓
[QA Reviewer] ← [Report Generator] ← [Sentiment Analyzer]
       ↓
Final Report
```

## Showcase Agents

### 1. Document Parser Agent
**Purpose**: Handles various document formats and extracts raw content
**Capabilities**:
- PDF text extraction
- Word document processing
- Image text recognition (OCR)
- Metadata extraction

### 2. Text Extractor Agent
**Purpose**: Cleans and structures extracted text
**Capabilities**:
- Text normalization
- Language detection
- Section identification
- Entity extraction (names, dates, amounts)

### 3. Analytics Agent
**Purpose**: Performs deep content analysis
**Capabilities**:
- Key topic identification
- Statistical analysis
- Risk factor detection
- Compliance checking

### 4. Sentiment Analyzer Agent
**Purpose**: Analyzes emotional tone and sentiment
**Capabilities**:
- Sentiment scoring (-1 to +1)
- Emotion classification
- Confidence levels
- Context-aware analysis

### 5. Report Generator Agent
**Purpose**: Creates formatted reports and visualizations
**Capabilities**:
- Executive summary generation
- Chart and graph creation
- Formatted output (PDF, HTML, JSON)
- Template-based reporting

### 6. QA Reviewer Agent
**Purpose**: Reviews and validates the analysis
**Capabilities**:
- Accuracy checking
- Consistency validation
- Completeness assessment
- Quality scoring

## Sample Data and Results

### Input Document
```
BUSINESS PROPOSAL
Client: TechCorp Industries
Date: December 15, 2024

Executive Summary:
We are excited to propose a comprehensive digital transformation 
initiative for TechCorp Industries. This project will modernize 
your infrastructure, improve efficiency by 40%, and reduce 
operational costs by $2.3M annually.

Key Benefits:
- Automated workflow systems
- Enhanced data analytics
- Improved customer satisfaction
- Streamlined operations

Investment Required: $5.8M over 18 months
Expected ROI: 180% within 3 years

We look forward to partnering with TechCorp on this exciting journey.
```

### Expected Output
```json
{
  "document_analysis": {
    "document_type": "Business Proposal",
    "client": "TechCorp Industries",
    "date": "2024-12-15",
    "key_metrics": {
      "efficiency_improvement": "40%",
      "cost_reduction": "$2.3M annually",
      "investment_required": "$5.8M",
      "roi": "180% within 3 years",
      "project_duration": "18 months"
    },
    "sentiment_analysis": {
      "overall_sentiment": 0.85,
      "confidence": 0.92,
      "emotions": ["optimistic", "professional", "confident"],
      "key_phrases": ["excited to propose", "look forward to partnering"]
    },
    "risk_factors": [
      "Large upfront investment",
      "Long project timeline",
      "ROI dependent on adoption"
    ],
    "compliance_check": {
      "financial_disclosure": "complete",
      "timeline_clarity": "good",
      "deliverables_specified": "partial"
    },
    "recommendations": [
      "Request detailed implementation plan",
      "Negotiate milestone-based payments",
      "Define success metrics clearly"
    ]
  },
  "quality_score": 8.5,
  "processing_time": "2.3 seconds",
  "confidence_level": 0.89
}
```

## Installation and Setup

### 1. Deploy Showcase Agents

```bash
# Navigate to showcase directory
cd showcase/

# Install dependencies
pip install -r requirements.txt

# Deploy all agents
python deploy_showcase.py
```

### 2. Configure Sample Data

```bash
# Upload sample documents
python upload_samples.py

# This uploads:
# - sample_proposal.pdf
# - contract_template.docx  
# - market_report.xlsx
# - presentation_slides.pptx
```

### 3. Run the Showcase

```bash
# Execute the complete pipeline
python run_showcase.py --document sample_proposal.pdf

# Or run via the web interface
# 1. Go to http://localhost:3000/flows
# 2. Select "Document Analysis Pipeline"
# 3. Upload a document
# 4. Click "Execute Workflow"
```

## Step-by-Step Execution

### Via CLI

```bash
# 1. Start the infrastructure
make up

# 2. Deploy showcase agents
cd showcase/
python deploy_agents.py

# 3. Run pipeline with sample document
python run_pipeline.py \
  --input "sample_proposal.pdf" \
  --output "analysis_report.json" \
  --format "detailed"

# 4. View results
cat analysis_report.json | jq '.'
```

### Via Web Interface

1. **Upload Document**: Go to Files → Upload → Select document
2. **Create Workflow**: Flows → New Flow → "Document Analysis Pipeline"
3. **Configure Steps**: Drag agents in order, connect inputs/outputs
4. **Execute**: Click "Run Flow" → Monitor progress
5. **View Results**: Check Logs and download generated report

### Via API

```python
import requests

# Upload document
files = {'file': open('sample_proposal.pdf', 'rb')}
upload_response = requests.post(
    "http://localhost:8000/api/v1/files/upload",
    files=files,
    headers={"Authorization": f"Bearer {token}"}
)
file_id = upload_response.json()["file_id"]

# Execute workflow
workflow_response = requests.post(
    "http://localhost:8000/api/v1/flows/document-analysis/execute",
    json={
        "input": {"file_id": file_id},
        "config": {"detailed_analysis": True}
    },
    headers={"Authorization": f"Bearer {token}"}
)

# Get results
flow_id = workflow_response.json()["flow_id"]
results = requests.get(
    f"http://localhost:8000/api/v1/flows/{flow_id}/results",
    headers={"Authorization": f"Bearer {token}"}
)
```

## Performance Metrics

### Expected Performance

| Metric | Value |
|--------|-------|
| **Total Processing Time** | 15-30 seconds |
| **Document Parser** | 2-5 seconds |
| **Text Extractor** | 1-3 seconds |
| **Analytics Agent** | 5-10 seconds |
| **Sentiment Analyzer** | 2-4 seconds |
| **Report Generator** | 3-6 seconds |
| **QA Reviewer** | 2-4 seconds |

### Scalability

- **Concurrent Documents**: Up to 10 documents simultaneously
- **File Size Limit**: 50MB per document
- **Supported Formats**: PDF, DOCX, XLSX, PPTX, TXT, HTML
- **Languages**: English, Spanish, French, German

## Customization Options

### 1. Add Custom Analysis

```python
# Create custom analyzer agent
class CustomAnalyzer(BaseAgent):
    async def analyze(self, text: str) -> Dict:
        # Your custom analysis logic
        return {
            "custom_metric": self.calculate_custom_metric(text),
            "industry_specific": self.industry_analysis(text)
        }
```

### 2. Modify Report Templates

```python
# Custom report template
CUSTOM_TEMPLATE = """
# Analysis Report for {client}

## Executive Summary
{executive_summary}

## Key Findings
{key_findings}

## Recommendations
{recommendations}

## Risk Assessment
{risk_assessment}
"""
```

### 3. Configure Agent Behavior

```yaml
# agent_config.yaml
document_parser:
  ocr_enabled: true
  languages: ["en", "es", "fr"]
  quality_threshold: 0.8

analytics_agent:
  deep_analysis: true
  industry_models: ["finance", "healthcare", "technology"]
  custom_metrics: ["roi_calculation", "risk_scoring"]

sentiment_analyzer:
  model: "advanced"
  context_window: 1000
  emotion_detection: true
```

## Integration Examples

### 1. Slack Integration

```python
# Slack bot integration
@app.event("file_shared")
def handle_file_share(event, say):
    file_url = event["file"]["url_private"]
    
    # Trigger analysis pipeline
    result = requests.post(
        "http://localhost:8000/api/v1/flows/document-analysis/execute",
        json={"input": {"file_url": file_url}}
    )
    
    say(f"Document analysis started! Results will be available in ~30 seconds.")
```

### 2. Email Processing

```python
# Email attachment processor
def process_email_attachment(email):
    for attachment in email.attachments:
        if attachment.content_type in SUPPORTED_FORMATS:
            # Upload to GenAI AgentOS
            file_id = upload_file(attachment.content)
            
            # Process with pipeline
            analysis = execute_pipeline(file_id)
            
            # Send results back
            send_analysis_email(email.sender, analysis)
```

### 3. REST API Wrapper

```python
# Simple API wrapper
@app.post("/analyze-document")
async def analyze_document(file: UploadFile):
    # Upload to GenAI AgentOS
    file_id = await upload_to_genai(file)
    
    # Execute analysis
    result = await execute_analysis_pipeline(file_id)
    
    return {
        "status": "completed",
        "analysis": result,
        "processing_time": result.get("processing_time"),
        "confidence": result.get("confidence_level")
    }
```

## Troubleshooting

### Common Issues

1. **Agent Connection Timeout**
   ```bash
   # Check agent status
   curl http://localhost:8000/api/v1/agents/status
   
   # Restart specific agent
   python restart_agent.py document_parser
   ```

2. **File Processing Errors**
   ```bash
   # Check file format support
   python check_file_support.py sample.pdf
   
   # Validate file integrity
   python validate_file.py sample.pdf
   ```

3. **Memory Issues with Large Files**
   ```bash
   # Increase Docker memory limits
   docker-compose -f docker-compose.yml -f docker-compose.override.yml up
   
   # Enable file chunking
   export ENABLE_FILE_CHUNKING=true
   ```

### Debug Mode

```bash
# Enable detailed logging
export DEBUG_SHOWCASE=true
python run_pipeline.py --debug --input sample.pdf
```

## Next Steps

1. **Extend the Pipeline**: Add more specialized agents (Legal Review, Financial Analysis, etc.)
2. **Custom Models**: Train domain-specific models for your industry
3. **Real-time Processing**: Implement streaming document analysis
4. **Advanced Reporting**: Create interactive dashboards and visualizations
5. **Multi-language Support**: Extend to support more languages and regions

This showcase demonstrates the power and flexibility of GenAI AgentOS for building sophisticated document analysis pipelines. The modular architecture allows easy customization and extension for specific business needs.