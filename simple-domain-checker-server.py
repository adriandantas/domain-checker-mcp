#!/usr/bin/env python3
"""
Domain Availability Checker MCP Server
This server accepts domain queries and checks availability using RDAP.
"""

import json
import logging
import sys
import dns.resolver
import requests
import time
from mcp.server import Server
import mcp.types as types

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)

logger = logging.getLogger("domain_checker")

# Constants
RDAP_BOOTSTRAP_URL = "https://data.iana.org/rdap/dns.json"
USER_AGENT = "DomainCheckerBot/1.0"

# Top TLDs to check
TOP_TLDS = [
    "com", "net", "org", "io", "co", "app", "dev", "ai", 
    "me", "info", "xyz", "online", "site", "tech"
    # Add more TLDs as needed
]

# Initialize the server
app = Server("domain-checker")

# Helper functions
async def get_rdap_data(domain):
    """Get RDAP data for a domain"""
    try:
        # Special case for .ch and .li domains
        tld = domain.split('.')[-1].lower()
        if tld in ['ch', 'li']:
            rdap_url = f"https://rdap.nic.{tld}/domain/{domain}"
        else:
            # Use common RDAP servers for known TLDs
            if tld in ["com", "net"]:
                rdap_url = f"https://rdap.verisign.com/{tld}/v1/domain/{domain}"
            elif tld == "org":
                rdap_url = f"https://rdap.publicinterestregistry.org/rdap/domain/{domain}"
            else:
                rdap_url = f"https://rdap.org/domain/{domain}"
        
        headers = {
            "Accept": "application/rdap+json",
            "User-Agent": USER_AGENT
        }
        
        response = requests.get(rdap_url, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        logger.error(f"RDAP error for {domain}: {e}")
        return None

async def check_dns(domain):
    """Check if a domain has DNS records"""
    try:
        answers = dns.resolver.resolve(domain, 'A')
        return True
    except:
        try:
            answers = dns.resolver.resolve(domain, 'NS')
            return True
        except:
            return False

async def check_domain_tool(domain):
    """Check if a domain is available for registration"""
    logger.info(f"Checking domain: {domain}")
    
    # First check DNS
    has_dns = await check_dns(domain)
    
    if has_dns:
        # Domain exists, get RDAP data if possible
        rdap_data = await get_rdap_data(domain)
        
        if rdap_data:
            # Extract data from RDAP
            registrar = "Unknown"
            reg_date = "Unknown"
            exp_date = "Unknown"
            
            # Extract registrar
            entities = rdap_data.get("entities", [])
            for entity in entities:
                if "registrar" in entity.get("roles", []):
                    vcard = entity.get("vcardArray", [])
                    if len(vcard) > 1 and isinstance(vcard[1], list):
                        for entry in vcard[1]:
                            if entry[0] in ["fn", "org"] and len(entry) > 3:
                                registrar = entry[3]
                                break
            
            # Extract dates
            events = rdap_data.get("events", [])
            for event in events:
                if event.get("eventAction") == "registration":
                    reg_date = event.get("eventDate", "Unknown")
                elif event.get("eventAction") == "expiration":
                    exp_date = event.get("eventDate", "Unknown")
            
            return f"""
Domain: {domain}
Status: Registered
Registrar: {registrar}
Registration Date: {reg_date}
Expiration Date: {exp_date}
"""
        else:
            return f"""
Domain: {domain}
Status: Registered
Note: Domain has DNS records but RDAP data couldn't be retrieved
"""
    
    # Try RDAP one more time even if DNS not found
    rdap_data = await get_rdap_data(domain)
    if rdap_data:
        return f"""
Domain: {domain}
Status: Registered
Note: Domain found in RDAP registry
"""
    
    # If we get here, the domain is likely available
    return f"""
Domain: {domain}
Status: Available
Note: No DNS records or RDAP data found
"""

async def check_tlds_tool(keyword):
    """Check a keyword across top TLDs"""
    logger.info(f"Checking keyword: {keyword} across TLDs")
    
    results = []
    available = []
    
    # Check each TLD in sequence
    for tld in TOP_TLDS:
        domain = f"{keyword}.{tld}"
        has_dns = await check_dns(domain)
        
        if not has_dns:
            # Double-check with RDAP if no DNS
            rdap_data = await get_rdap_data(domain)
            if not rdap_data:
                available.append(domain)
    
    # Format the response
    response = f"Keyword: {keyword}\n"
    response += f"TLDs checked: {len(TOP_TLDS)}\n"
    response += f"Available domains: {len(available)}\n\n"
    
    if available:
        response += "Available domains:\n"
        for domain in available:
            response += f"- {domain}\n"
    else:
        response += "No available domains found for this keyword.\n"
    
    return response

# Register tools using the older non-decorator syntax
@app.list_tools()
async def list_tools():
    return [
        types.Tool(
            name="check_domain",
            description="Check if a domain is available for registration",
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {
                        "type": "string",
                        "description": "Domain name to check (e.g., example.com)"
                    }
                },
                "required": ["domain"]
            }
        ),
        types.Tool(
            name="check_tlds",
            description="Check a keyword across top TLDs",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Keyword to check across TLDs"
                    }
                },
                "required": ["keyword"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name, arguments):
    if name == "check_domain":
        domain = arguments.get("domain")
        result = await check_domain_tool(domain)
        return [types.TextContent(type="text", text=result)]
    elif name == "check_tlds":
        keyword = arguments.get("keyword")
        result = await check_tlds_tool(keyword)
        return [types.TextContent(type="text", text=result)]
    else:
        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

if __name__ == "__main__":
    # Run the server with stdio transport
    from mcp.server.stdio import stdio_server
    import asyncio
    
    async def main():
        async with stdio_server() as streams:
            await app.run(
                streams[0],
                streams[1],
                app.create_initialization_options()
            )
    
    asyncio.run(main())