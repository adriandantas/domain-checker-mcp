# Domain Checker MCP Server

A powerful Model Context Protocol (MCP) server that enables AI assistants like Claude to check domain availability and registration status across multiple top-level domains (TLDs).

## Features

- 🔍 Real-time domain availability checking
- 🌐 Multi-TLD support (.com, .net, .org, .io, .ai, .dev, .app, .co)
- 📊 Detailed domain registration information via RDAP
- 🔒 DNS verification for accurate results
- ⚡ Fast and reliable domain status queries
- 🔄 Batch domain checking capabilities

## Prerequisites

- Python 3.8 or higher
- Windows operating system
- Claude Desktop installed
- Basic understanding of MCP server configuration
- Internet connection for domain queries

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/domain-checker-mcp.git
   cd domain-checker-mcp
   ```

2. Run the setup script:
   ```bash
   setup.bat
   ```

3. Follow the on-screen instructions to configure Claude Desktop

## Detailed Installation

### Step 1: Environment Setup
The setup script (`setup.bat`) will:
- Create a Python virtual environment
- Install all required dependencies
- Generate the correct configuration for Claude Desktop

### Step 2: Claude Desktop Configuration
After running the setup script, you'll receive a JSON configuration snippet. Add this to your Claude Desktop configuration file:

```json
{
  "mcpServers": {
    "domain-checker": {
      "command": "cmd",
      "args": [
        "/c",
        "C:\\Path\\To\\domain-checker-mcp\\domain-checker-server.bat"
      ],
      "cwd": "C:\\Path\\To\\domain-checker-mcp"
    }
  }
}
```

## Usage Guide

### Basic Domain Checking
Use the `check_domain` tool to verify domain availability:
- "Check if example.com is available"
- "Is anthropic.ai registered?"
- "Tell me the registration status of google.com"

### Multi-TLD Search
Use the `check_tlds` tool to find available domains across different TLDs:
- "Find available domains for the keyword 'assistant'"
- "What TLDs are available for the name 'myproject'"
- "Show me domain options for 'techstart'"

## Supported TLDs

The server supports checking availability for the following top-level domains:
- .com (Commercial)
- .net (Network)
- .org (Organization)
- .io (Indian Ocean)
- .ai (Artificial Intelligence)
- .dev (Development)
- .app (Applications)
- .co (Company/Commercial)

## Troubleshooting Guide

### Common Issues

1. **Setup Fails**
   - Ensure Python is installed and in PATH
   - Verify virtual environment creation
   - Check internet connection

2. **Server Won't Start**
   - Verify all dependencies are installed
   - Check configuration paths
   - Ensure virtual environment is activated

3. **Domain Checks Fail**
   - Verify internet connection
   - Check for rate limiting
   - Ensure domain format is correct

### Development

To modify or enhance the server:

1. Activate the virtual environment:
   ```bash
   call venv\Scripts\activate.bat
   ```

2. Make your changes to `simple-domain-checker-server.py`

3. Test the server:
   ```bash
   python simple-domain-checker-server.py
   ```

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
