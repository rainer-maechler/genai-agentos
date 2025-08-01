# GenAI AgentOS Showcase

This showcase demonstrates the full capabilities of GenAI AgentOS through both command-line and web interface interactions. It features a complete business intelligence pipeline with document analysis, sentiment analysis, and report generation.

## 🚀 Quick Start - Web Interface Showcase

**For the full interactive web experience:**

```bash
cd /home/eramue/sym/genai-agentos/showcase
python3 run_web_showcase.py
```

This will:
- Start all 3 showcase agents (they'll show as ACTIVE with green borders)
- Provide step-by-step instructions for using the web interface
- Monitor and restart agents if they crash
- Allow you to create agent flows visually

**Then follow the on-screen instructions to:**
1. Login at http://localhost:3000/
2. View active agents at http://localhost:3000/agents
3. Create agent flows at http://localhost:3000/agent-flows

## 📊 Showcase Components

### 1. Document Analyzer Agent
- **Function**: Extracts key information from business documents
- **Capabilities**: Entity recognition, topic identification, metadata extraction
- **Input**: Text documents, PDFs, business proposals
- **Output**: Structured analysis with organizations, dates, financial figures

### 2. Sentiment Analyzer Agent  
- **Function**: Advanced sentiment and emotional tone analysis
- **Capabilities**: Sentiment scoring, emotion detection, business tone assessment
- **Input**: Text content from documents
- **Output**: Sentiment scores, emotional analysis, confidence metrics

### 3. Report Generator Agent
- **Function**: Comprehensive report creation with visualizations
- **Capabilities**: Executive summaries, charts, multi-format export
- **Input**: Analysis data from other agents
- **Output**: Professional reports (HTML, PDF), executive summaries

## 🖥️ Command Line Showcase (Alternative)

If you prefer command-line demonstrations:

```bash
# Deploy agents (registers them in the system)
python3 deploy_showcase.py

# Run complete pipeline demonstration
python3 run_showcase.py

# Generate sample business documents
python3 upload_samples.py

# Run comprehensive standalone demo
python3 comprehensive_demo.py
```

## 🏗️ Architecture

The showcase implements a modern multi-agent architecture:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Document        │    │ Sentiment        │    │ Report          │
│ Analyzer        │───▶│ Analyzer         │───▶│ Generator       │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│              GenAI AgentOS Router (WebSocket)                   │
│                    ws://localhost:8080/ws                      │
└─────────────────────────────────────────────────────────────────┘
```

## 📋 Prerequisites

Make sure GenAI AgentOS is running:

```bash
cd /home/eramue/sym/genai-agentos
docker compose up --build
```

Services should be available at:
- **Frontend**: http://localhost:3000/
- **Backend API**: http://localhost:8000/docs  
- **WebSocket Router**: ws://localhost:8080/ws

## 🎯 Usage Scenarios

### Business Document Analysis Pipeline
1. **Upload** business proposals, contracts, or reports
2. **Analyze** documents for key information and entities
3. **Assess** sentiment and emotional tone
4. **Generate** executive summaries with visualizations
5. **Export** professional reports in multiple formats

### Interactive Web Flows
- Create custom agent workflows in the web interface
- Chain agents together for complex processing pipelines
- Monitor agent execution in real-time
- View detailed results and analytics

## 📁 File Structure

```
showcase/
├── README.md                     # This file
├── run_web_showcase.py          # Main web interface launcher
├── check_web_interface.py       # Status checker
├── start_active_agents.py       # Agent starter script
├── agents/                      # Original CLI agents
│   ├── report_generator.py      # Full-featured report generator
│   ├── analytics_agent.py       # Business analytics
│   └── ...
├── active_agents/               # WebSocket-enabled agents
│   ├── simple_websocket_agent.py    # Base WebSocket agent class
│   ├── simple_document_analyzer.py  # Document analysis agent
│   ├── simple_report_generator.py   # Report generation agent
│   └── simple_sentiment_analyzer.py # Sentiment analysis agent
├── deploy_showcase.py           # CLI deployment script
├── run_showcase.py             # CLI pipeline runner
├── upload_samples.py           # Sample data generator
└── comprehensive_demo.py       # Standalone demonstration
```

## 🔧 Troubleshooting

### Agents Not Showing as Active
```bash
# Check if agents are running
ps aux | grep -E "(simple_document|simple_report|simple_sentiment)"

# Restart showcase
python3 run_web_showcase.py
```

### Web Interface Issues
```bash
# Check service status
python3 check_web_interface.py

# Restart GenAI AgentOS
cd /home/eramue/sym/genai-agentos
docker compose restart
```

### Connection Problems
- Ensure all Docker services are running
- Check that ports 3000, 8000, and 8080 are not blocked
- Verify JWT tokens are valid (agents auto-refresh)

## 🎉 Success Indicators

✅ **Web Interface Working**:
- Login successful at http://localhost:3000/
- Agents page shows 3 agents with GREEN borders
- Agent flows page allows creating new flows

✅ **Agents Active**:
- All 3 agents show "ACTIVE" status
- No red error indicators
- Agents respond to test messages

✅ **Full Pipeline**:
- Can create multi-agent flows
- Document processing completes successfully
- Reports generate with proper formatting

## 🚀 Ready to Showcase!

Your GenAI AgentOS showcase is now ready for demonstration. The system provides both programmatic and visual interfaces for creating sophisticated agent workflows, making it perfect for showcasing the platform's capabilities to stakeholders and potential users.

Run `python3 run_web_showcase.py` and follow the instructions to start your interactive demonstration!