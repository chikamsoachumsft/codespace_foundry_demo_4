# Azure AI Foundry API Testing Suite

A comprehensive collection of tools and scripts for testing Azure AI Foundry (formerly Azure OpenAI) endpoints, including private endpoint connectivity testing.

## 🚀 Overview

This repository contains Python and PowerShell scripts designed to test various Azure AI Foundry configurations, including:
- Public vs Private endpoint access
- Multiple authentication methods
- Different API endpoint patterns
- Network connectivity testing
- Deployment discovery

## 📁 Project Structure

```
├── README.md                              # This file
├── requirements.txt                       # Python dependencies
├── .gitignore                            # Git ignore patterns
│
├── python-scripts/
│   ├── complete_api_test.py              # Comprehensive API testing (Original Foundry)
│   ├── complete_api_test_f_codespace.py  # API testing for F-Codespace resource
│   ├── compare_foundry_resources.py      # Side-by-side comparison of two resources
│   ├── explore_api.py                    # Deep API exploration and discovery
│   ├── foundry_solution.py               # Analysis and solution recommendations
│   ├── f_codespace_success_analysis.py   # Success analysis for F-Codespace
│   └── test.py                           # Basic connectivity test
│
└── powershell-scripts/
    └── test-foundry-private-endpoint.ps1  # PowerShell version for VNet testing
```

## 🔧 Setup and Installation

### Prerequisites
- Python 3.7+ (for Python scripts)
- PowerShell 5.1+ (for PowerShell scripts)
- Azure CLI (optional, for deployment management)
- Valid Azure AI Foundry resource with API keys

### Python Dependencies
```bash
pip install -r requirements.txt
```

## 🎯 Usage

### Python Scripts

#### 1. Basic API Testing
```bash
# Test original Foundry resource
python complete_api_test.py

# Test F-Codespace resource  
python complete_api_test_f_codespace.py
```

#### 2. Resource Comparison
```bash
# Compare two Foundry resources side-by-side
python compare_foundry_resources.py
```

#### 3. API Discovery
```bash
# Deep exploration of API structure
python explore_api.py

# Analyze successful configurations
python f_codespace_success_analysis.py
```

### PowerShell Scripts

#### Private Endpoint Testing (Run from VNet machine)
```powershell
# Test private endpoint connectivity
.\test-foundry-private-endpoint.ps1
```

## 🔑 Configuration

### API Keys and Endpoints
Update the following variables in each script:

```python
# Python scripts
base_url = "https://your-foundry-resource.services.ai.azure.com"
openai_url = "https://your-foundry-resource.openai.azure.com"
api_key = "your-api-key-here"
```

```powershell
# PowerShell scripts
$baseUrl = "https://your-foundry-resource.services.ai.azure.com"
$openaiUrl = "https://your-foundry-resource.openai.azure.com"
$apiKey = "your-api-key-here"
```

## 📊 Key Findings

### Resource Comparison Results

| Feature | Foundry-Codespace-Demo | F-Codespace |
|---------|------------------------|-------------|
| Public Access | ❌ Disabled (Private endpoint required) | ✅ Enabled |
| Models Endpoint | ❌ 403 Forbidden | ✅ 200 OK (113+ models) |
| Content Safety | ❌ 403 Forbidden | ✅ 200 OK |
| Authentication | ✅ Valid API Key | ✅ Valid API Key |
| Deployments | ❓ Unknown (access blocked) | ⚠️ Available but none created |

### Network Access Patterns

#### Public Internet Access
- **Foundry-Codespace-Demo**: Blocked with 403 "Public access is disabled"
- **F-Codespace**: Full access with 200 responses

#### Private Endpoint Access (VNet)
- **Foundry-Codespace-Demo**: Should work from VNet machines
- **F-Codespace**: Works from both public and private networks

## 🔍 Testing Scenarios

### 1. Public vs Private Access Testing
- Compare API responses from public internet vs VNet
- Identify network access restrictions
- Validate private endpoint configurations

### 2. API Endpoint Discovery
- Systematically test various endpoint patterns
- Discover available models and capabilities
- Find working authentication methods

### 3. Deployment Testing
- Test common deployment names
- Validate OpenAI-compatible endpoints
- Check deployment availability

## 🛠️ Troubleshooting

### Common Issues

#### 403 "Public access is disabled"
```bash
# Enable public access
az cognitiveservices account update \
  --name 'your-resource-name' \
  --resource-group 'your-rg' \
  --public-network-access Enabled
```

#### 404 "Resource not found"
- Check endpoint URLs
- Verify API versions
- Ensure deployments exist

#### 401 "Access denied"
- Verify API key validity
- Check authentication header format
- Confirm resource permissions

### Deployment Creation
```bash
# Create a GPT-4 deployment
az cognitiveservices account deployment create \
  --name 'your-resource-name' \
  --resource-group 'your-rg' \
  --deployment-name 'gpt-4-deployment' \
  --model-name 'gpt-4' \
  --model-version 'latest' \
  --model-format 'OpenAI' \
  --sku-capacity '10' \
  --sku-name 'Standard'
```

## 📈 Success Metrics

### F-Codespace Resource Achievements
- ✅ 113+ models discovered and accessible
- ✅ Content Safety API working (severity analysis)
- ✅ Multiple authentication methods supported
- ✅ Full public access enabled
- ✅ Ready for deployment creation

### API Endpoint Patterns Discovered
- `/models` - List available models
- `/contentsafety/text:analyze` - Content safety analysis
- `/openai/models` - OpenAI-compatible model listing
- `/openai/deployments/{name}/chat/completions` - Chat completions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Resources

- [Azure AI Foundry Documentation](https://docs.microsoft.com/en-us/azure/ai-services/)
- [Azure OpenAI Service Documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/openai/)
- [Azure Private Endpoints](https://docs.microsoft.com/en-us/azure/private-link/private-endpoint-overview)

## 📧 Contact

For questions or support, please open an issue in this repository.

---
**Note**: Remember to keep your API keys secure and never commit them to version control. Use environment variables or Azure Key Vault for production deployments.
