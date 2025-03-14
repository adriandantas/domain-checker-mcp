# domain-checker-mcp
Give LLM an ability to check if domain is available or already registered


## Installation
### Install dependencies
```
pip install mcp dnspython requests
```

### MCP config
edit your claude_desktop_config.json file (linux ~/.config/Claude/claude_desktop_config.json)
```
{
  "mcpServers": {
    "domain-checker": {
      "command": "python3",
      "args": [
        "/path/to/the/domain-checker-mcp/simple-domain-checker-server.py"
      ]
    }
  }
}
```

