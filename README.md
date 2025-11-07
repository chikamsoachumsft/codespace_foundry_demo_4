# Foundry API VNET Testing

This repository contains code to test hitting Palantir Foundry API behind a VNET (Virtual Network).

## Overview

The solution provides a Python-based client for testing connectivity to Palantir Foundry APIs that are deployed behind Azure VNET or other private network configurations. It includes:

- **Foundry API Client**: A robust client for making API calls to Foundry
- **Connectivity Testing**: Tools to verify network connectivity through VNET
- **Proxy Support**: Configuration for HTTP/HTTPS proxies if needed
- **Authentication**: Support for token-based authentication
- **Comprehensive Logging**: Detailed logging for debugging connectivity issues

## Prerequisites

- Python 3.7 or higher
- Access to a Palantir Foundry instance
- API token for authentication
- Network access to the Foundry instance (through VNET if applicable)

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/chikamsoachumsft/codespace_foundry_demo_4.git
   cd codespace_foundry_demo_4
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and set your configuration:
   ```
   FOUNDRY_API_URL=https://your-foundry-instance.palantirfoundry.com
   FOUNDRY_API_TOKEN=your_api_token_here
   ```
   
   Optional VNET/Proxy settings:
   ```
   HTTP_PROXY=http://your-proxy:8080
   HTTPS_PROXY=https://your-proxy:8443
   ```

## Usage

### Basic Connectivity Test

Run the connectivity test script:

```bash
python foundry_client.py
```

This will:
1. Load configuration from environment variables
2. Check VNET configuration
3. Test connectivity to the Foundry API
4. Display detailed results

### Using the Client in Your Code

```python
from foundry_client import FoundryAPIClient

# Initialize the client
client = FoundryAPIClient(
    api_url="https://your-foundry-instance.palantirfoundry.com",
    api_token="your_token_here"
)

# Test connectivity
results = client.test_connectivity()
print(f"Connection successful: {results['success']}")

# Make API calls
response = client.get('/api/v1/datasets')
print(response.json())
```

### Running Tests

Run the unit tests:

```bash
python -m unittest test_foundry_client.py
```

Or with verbose output:

```bash
python -m unittest test_foundry_client.py -v
```

## Troubleshooting VNET Connectivity

### Common Issues

1. **Connection Timeout**
   - Check firewall rules in your VNET configuration
   - Verify NSG (Network Security Group) rules allow outbound HTTPS
   - Ensure the Foundry instance is accessible from your VNET

2. **DNS Resolution Failures**
   - Verify DNS configuration in your VNET
   - Check if private DNS zones are correctly configured
   - Test DNS resolution: `nslookup your-foundry-instance.palantirfoundry.com`

3. **SSL Certificate Errors**
   - Verify SSL certificates are properly configured
   - For testing only, you can disable SSL verification (not recommended for production):
     ```python
     client = FoundryAPIClient(verify_ssl=False)
     ```

4. **Authentication Failures**
   - Verify your API token is valid and not expired
   - Check token permissions in Foundry
   - Ensure the token has necessary scopes for the API endpoints you're accessing

### Debugging

Enable debug logging by setting the log level:

```bash
export LOG_LEVEL=DEBUG
python foundry_client.py
```

## Configuration Options

| Environment Variable | Description | Required | Default |
|---------------------|-------------|----------|---------|
| `FOUNDRY_API_URL` | Foundry instance URL | Yes | - |
| `FOUNDRY_API_TOKEN` | API authentication token | Yes | - |
| `HTTP_PROXY` | HTTP proxy URL | No | - |
| `HTTPS_PROXY` | HTTPS proxy URL | No | - |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | No | INFO |

## Project Structure

```
.
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .env.example             # Example environment configuration
├── .gitignore               # Git ignore rules
├── foundry_client.py        # Main Foundry API client
└── test_foundry_client.py   # Unit tests
```

## Security Considerations

- Never commit `.env` files or tokens to version control
- Use Azure Key Vault or similar services for storing secrets in production
- Enable SSL verification in production environments
- Rotate API tokens regularly
- Follow the principle of least privilege when assigning API permissions

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is provided as-is for testing and development purposes.