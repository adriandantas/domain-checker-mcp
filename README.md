# Domain Checker MCP Server

A Model Context Protocol (MCP) server that provides domain availability checking capabilities for Claude and other AI assistants.

## Features

- Check if a domain is available for registration
- Query for available domains across multiple top-level domains (TLDs)
- RDAP (Registration Data Access Protocol) integration for detailed domain registration information
- DNS verification for better accuracy
- Support for multiple TLDs including .com, .net, .org, .io, .ai, and more

## Prerequisites

- Python 3.8 or higher
- Windows (for the provided batch scripts)
- Basic understanding of MCP server configuration
- An installation of Claude Desktop

## Installation

1. Clone this repository
   ```bash
   git clone https://github.com/yourusername/domain-checker-mcp.git
   cd domain-checker-mcp
   ```

2. Install dependencies using one of these methods:
   
   Using the setup script (Windows):
   ```bash
   setup.bat
   ```

   Manual installation:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Unix/MacOS
   # OR
   .\venv\Scripts\activate  # On Windows
   pip install -r requirements.txt
   ```

## Configuration

### Claude Desktop Configuration

Run the setup script first, which will provide you with the correct configuration to add to your Claude Desktop configuration file:

```bash
setup.bat
```

The script will output the necessary JSON configuration with the correct paths for your installation. For example:

```json
{
  "mcpServers": {
    "domain-checker": {
      "command": "cmd",
      "args": [
        "/c",
        "C:\\Users\\YourUsername\\domain-checker-mcp\\domain-checker-server.bat"
      ],
      "cwd": "C:\\Users\\YourUsername\\domain-checker-mcp"
    }
  }
}
```

Note: Your actual paths will be different based on where you installed the server.

## Usage

The domain-checker MCP server provides two main tools:

1. **check_domain**: Checks if a specific domain is available
   - Example queries:
     - "Check if example.com is available"
     - "Is anthropic.ai registered?"
     - "Tell me the registration status of google.com"

2. **check_tlds**: Searches for available domains across multiple TLDs
   - Example queries:
     - "Find available domains for the keyword 'assistant'"
     - "What TLDs are available for the name 'myproject'"
     - "Show me domain options for 'techstart'"

## Supported TLDs

Currently supported top-level domains include:
- .com
- .net
- .org
- .io
- .ai
- .dev
- .app
- .co
(Add or modify this list based on actual supported TLDs)

## Error Handling

Common error messages and their solutions:
- "Connection timeout" - Check your internet connection
- "Rate limit exceeded" - Wait a few minutes before trying again
- "Invalid domain name" - Ensure the domain follows correct formatting

## Project Structure

```
domain-checker-mcp/
├── .gitignore                      # Git ignore file
├── README.md                       # Documentation
├── requirements.txt                # Python dependencies
├── setup_mcp_env.bat              # Environment setup script
├── domain-checker-server.bat      # Server startup script
└── simple-domain-checker-server.py # Main MCP server implementation
```

## Troubleshooting

To modify the server or add new features:

1. Activate the virtual environment
   ```bash
   call venv\Scripts\activate.bat
   ```

2. Make your changes to the Python script
3. Test the server by running:
   ```bash
   python simple-domain-checker-server.py
   ```

Common issues:
- If setup fails, ensure Python is installed and added to your PATH
- Check that all required dependencies are listed in requirements.txt
- Verify that your virtual environment is properly activated
- Make sure all paths in your Claude Desktop configuration are correct

## License

[MIT License](LICENSE)

## Acknowledgements

- Built using the Model Context Protocol (MCP)
- Uses RDAP for domain registration information
- Uses DNS resolver for verification
- Powered by dnspython and requests libraries

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.