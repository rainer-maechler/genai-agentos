# GenAI AgentOS User Guide

## Overview

GenAI AgentOS is a comprehensive framework for building, deploying, and orchestrating AI agents. It provides a complete infrastructure that allows you to create intelligent agents that can communicate with each other, process files, handle complex workflows, and integrate with various AI models.

## Table of Contents

1. [Quick Start](#quick-start)
2. [System Architecture](#system-architecture)  
3. [Agent Types](#agent-types)
4. [Creating Your First Agent](#creating-your-first-agent)
5. [Agent Communication](#agent-communication)
6. [Workflow Management](#workflow-management)
7. [File Handling](#file-handling)
8. [Security & Authentication](#security--authentication)
9. [Monitoring & Logging](#monitoring--logging)
10. [Advanced Features](#advanced-features)
11. [Troubleshooting](#troubleshooting)

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.12+ (for CLI)
- Node.js 18+ (for frontend development)

### Installation

1. **Clone and Setup**
   ```bash
   git clone https://github.com/rainer-maechler/genai-agentos.git
   cd genai-agentos
   cp .env-example .env
   ```

2. **Start the Infrastructure**
   ```bash
   make up
   # or
   docker compose up --build
   ```

3. **Access the Platform**
   - Frontend UI: http://localhost:3000
   - API Documentation: http://localhost:8000/docs
   - WebSocket Router: ws://localhost:8080/ws

### First Time Setup

1. **Create User Account**
   ```bash
   cd cli/
   python cli.py signup -u your_username
   ```

2. **Login**
   ```bash
   python cli.py login -u your_username -p your_password
   ```

3. **Configure AI Model**
   - Go to http://localhost:3000/settings
   - Add your OpenAI API key or configure other providers

## System Architecture

### Core Components

- **Backend**: FastAPI-based API server handling authentication, agent registry, and data persistence
- **Frontend**: React-based web interface for managing agents and workflows
- **Router**: WebSocket router managing real-time communication between agents
- **Master Agent**: Orchestration layer for complex multi-agent workflows
- **Database**: PostgreSQL for persistent storage
- **Message Queue**: Redis + Celery for background tasks

### Communication Flow

```
User/Frontend → Backend API → Router → Agent(s) → LLM Provider
     ↑                                      ↓
     ←────── WebSocket Updates ←────────────
```

## Agent Types

### 1. GenAI Agents
Native agents built with the `genai-protocol` library. These are full-featured agents that can:
- Handle complex conversations
- Process files and data
- Call other agents
- Maintain state across interactions

### 2. MCP Servers (Model Context Protocol)
Standardized servers that provide specific capabilities:
- File system access
- Database queries  
- API integrations
- Tool execution

### 3. A2A Servers (Agent to Agent Protocol)
Lightweight agents designed for inter-agent communication:
- Simple request/response patterns
- Specialized micro-services
- External system integrations

## Creating Your First Agent

### Using the CLI Generator

1. **Register Agent**
   ```bash
   cd cli/
   python cli.py register_agent \
     --name "weather_assistant" \
     --description "Provides weather information for any location"
   ```

2. **Generated Files**
   The CLI creates:
   - `agents/weather_assistant.py` - Main agent code
   - `agents/weather_assistant/pyproject.toml` - Dependencies

3. **Customize Agent Logic**
   ```python
   # agents/weather_assistant.py
   from genai_protocol import GenAISession
   
   async def handle_message(session: GenAISession, message: str) -> str:
       # Your agent logic here
       if "weather" in message.lower():
           return "I can help you get weather information!"
       return "How can I assist you with weather-related questions?"
   ```

4. **Run Your Agent**
   ```bash
   cd agents/
   uv run python weather_assistant.py
   ```

### Manual Agent Creation

For more control, create agents manually:

```python
import asyncio
from genai_protocol import GenAISession, GenAIProtocol

class CustomAgent:
    def __init__(self):
        self.protocol = GenAIProtocol(
            name="custom_agent",
            description="My custom agent",
            version="1.0.0"
        )
    
    async def process_message(self, message: str) -> str:
        # Agent logic here
        return f"Processed: {message}"
    
    async def start(self):
        session = GenAISession(
            ws_url="ws://localhost:8080/ws",
            agent_token="your_agent_token"
        )
        await session.connect()
        
        async for message in session.listen():
            response = await self.process_message(message.content)
            await session.send_response(message.id, response)

if __name__ == "__main__":
    agent = CustomAgent()
    asyncio.run(agent.start())
```

## Agent Communication

### Direct Agent Calls

Agents can call other agents directly:

```python
from genai_protocol import GenAISession

async def call_another_agent(session: GenAISession, agent_name: str, message: str):
    response = await session.call_agent(
        agent_name=agent_name,
        message=message,
        timeout=30
    )
    return response.content
```

### Workflow Orchestration

Use the Master Agent for complex workflows:

```python
# Define workflow in frontend or via API
workflow = {
    "steps": [
        {
            "agent": "data_extractor",
            "input": "Extract key metrics from uploaded file"
        },
        {
            "agent": "report_generator", 
            "input": "Create summary report from: {previous_output}",
            "depends_on": ["data_extractor"]
        }
    ]
}
```

## Workflow Management

### Creating Workflows

1. **Via Web Interface**
   - Go to "Agent Flows" page
   - Drag and drop agents to create workflow
   - Configure inputs/outputs between steps
   - Save and execute

2. **Via API**
   ```python
   import requests
   
   workflow_data = {
       "name": "Document Processing Pipeline",
       "description": "Processes documents through multiple stages",
       "steps": [
           {
               "agent_id": "pdf_parser",
               "input_template": "Parse document: {file_url}",
               "order": 1
           },
           {
               "agent_id": "summarizer",
               "input_template": "Summarize: {step_1_output}",
               "order": 2
           }
       ]
   }
   
   response = requests.post(
       "http://localhost:8000/api/v1/flows",
       json=workflow_data,
       headers={"Authorization": f"Bearer {jwt_token}"}
   )
   ```

### Executing Workflows

```bash
# Via CLI
python cli.py execute_flow --flow-id 123 --input "Process this document"

# Via API
curl -X POST "http://localhost:8000/api/v1/flows/123/execute" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"input": "Process this document"}'
```

## File Handling

### Uploading Files

```python
# Via agent code
async def handle_file_upload(session: GenAISession, file_path: str):
    file_id = await session.upload_file(file_path)
    return f"File uploaded with ID: {file_id}"

# Via API
files = {'file': open('document.pdf', 'rb')}
response = requests.post(
    "http://localhost:8000/api/v1/files/upload",
    files=files,
    headers={"Authorization": f"Bearer {token}"}
)
```

### Processing Files in Agents

```python
async def process_uploaded_file(session: GenAISession, file_id: str):
    # Download file content
    file_content = await session.get_file_content(file_id)
    
    # Process based on file type
    if file_content.mime_type == "application/pdf":
        text = extract_pdf_text(file_content.data)
    elif file_content.mime_type.startswith("image/"):
        analysis = analyze_image(file_content.data)
    
    return processed_result
```

## Security & Authentication

### User Authentication

The system uses JWT tokens for authentication:

```python
# Login to get token
response = requests.post("http://localhost:8000/api/v1/auth/login", {
    "username": "your_username",
    "password": "your_password"
})
token = response.json()["access_token"]

# Use token in requests
headers = {"Authorization": f"Bearer {token}"}
```

### Agent Authentication

Agents authenticate using generated tokens:

```python
# Agent token is provided when registering
session = GenAISession(
    ws_url="ws://localhost:8080/ws",
    agent_token="your_agent_token_here"
)
```

### LLM Configuration Security

API keys are encrypted before storage:

```python
# Keys are automatically encrypted when saved via UI
# Or via API:
model_config = {
    "provider": "openai",
    "api_key": "sk-...",  # Will be encrypted
    "model": "gpt-4",
    "max_tokens": 1000
}
```

## Monitoring & Logging

### Agent Logs

View agent interactions:

```python
# Via API
logs = requests.get(
    f"http://localhost:8000/api/v1/logs/agent/{agent_id}",
    headers={"Authorization": f"Bearer {token}"}
)

# Via Web Interface
# Go to "Logs" section in frontend
```

### System Monitoring

```bash
# Check system health
curl http://localhost:8000/health

# Monitor WebSocket connections
curl http://localhost:8080/status

# Database status
docker exec genai-postgres psql -U postgres -c "\l"
```

### Performance Metrics

```python
# Get agent performance stats
stats = requests.get(
    f"http://localhost:8000/api/v1/agents/{agent_id}/stats",
    headers={"Authorization": f"Bearer {token}"}
)
```

## Advanced Features

### Custom MCP Server Integration

```python
# Add MCP server via API
mcp_config = {
    "name": "File System MCP",
    "description": "Provides file system access",
    "url": "http://localhost:9000/mcp",
    "capabilities": ["read_file", "write_file", "list_directory"]
}

response = requests.post(
    "http://localhost:8000/api/v1/mcp/servers",
    json=mcp_config,
    headers={"Authorization": f"Bearer {token}"}
)
```

### A2A Protocol Implementation

```python
# Simple A2A server
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class AgentRequest(BaseModel):
    input: str
    context: dict = {}

@app.post("/process")
async def process_request(request: AgentRequest):
    # Your processing logic
    result = f"Processed: {request.input}"
    return {"output": result, "status": "success"}

@app.get("/.well-known/agent.json")
async def agent_manifest():
    return {
        "name": "My A2A Agent",
        "description": "Processes text input",
        "version": "1.0.0",
        "endpoints": {
            "process": "/process"
        }
    }
```

### Custom Master Agent Strategies

```python
# Implement custom orchestration logic
class CustomMasterAgent(BaseMasterAgent):
    async def execute_workflow(self, workflow_config, input_data):
        # Custom execution strategy
        results = []
        for step in workflow_config.steps:
            if self.should_execute_parallel(step):
                result = await self.execute_parallel(step, input_data)
            else:
                result = await self.execute_sequential(step, input_data)
            results.append(result)
        
        return self.combine_results(results)
```

## Troubleshooting

### Common Issues

1. **Agent Connection Failed**
   ```bash
   # Check if router is running
   curl http://localhost:8080/status
   
   # Verify agent token
   python cli.py list_agents
   ```

2. **Database Connection Error**
   ```bash
   # Check PostgreSQL status
   docker exec genai-postgres pg_isready -U postgres
   
   # Run migrations
   cd backend/
   uv run alembic upgrade head
   ```

3. **WebSocket Connection Issues**
   ```bash
   # Check firewall/network settings
   netstat -tulpn | grep 8080
   
   # Verify CORS settings in .env
   echo $BACKEND_CORS_ORIGINS
   ```

4. **File Upload Problems**
   ```bash
   # Check file permissions
   ls -la /files
   
   # Verify Docker volume mounts
   docker inspect genai-backend | grep Mounts
   ```

### Debug Mode

Enable detailed logging:

```bash
# Set DEBUG=True in .env
echo "DEBUG=True" >> .env

# Restart services
docker compose down
docker compose up --build
```

### Getting Help

1. **Check logs**
   ```bash
   docker compose logs backend
   docker compose logs router
   docker compose logs master-agent
   ```

2. **API Documentation**
   - Visit http://localhost:8000/docs for interactive API docs

3. **Community Support**
   - GitHub Issues: Report bugs and feature requests
   - Documentation: Check README files in each component directory

## Best Practices

### Agent Development

1. **Keep agents focused** - Each agent should have a single, well-defined responsibility
2. **Handle errors gracefully** - Always implement proper error handling and timeouts
3. **Use type hints** - Leverage Python's type system for better code quality
4. **Test thoroughly** - Write unit tests for your agent logic

### Security

1. **Never hardcode secrets** - Use environment variables or the encrypted config system
2. **Validate inputs** - Always sanitize and validate user inputs
3. **Use least privilege** - Agents should only have access to resources they need
4. **Monitor usage** - Keep track of agent interactions and resource usage

### Performance

1. **Optimize for async** - Use async/await patterns for better concurrency
2. **Cache when appropriate** - Store frequently accessed data to reduce latency
3. **Set reasonable timeouts** - Prevent hanging operations
4. **Monitor resource usage** - Keep track of memory and CPU consumption

This user guide provides a comprehensive overview of the GenAI AgentOS framework. For specific implementation examples, see the showcase documentation and sample agents included in this repository.