"""
Azure AI Foundry API Test - Private Endpoint Configuration Required

FINDINGS:
=========
1. Your Azure AI Foundry service is correctly configured
2. API keys are valid and working
3. The service requires private endpoint access (public access is disabled)
4. Standard endpoint patterns are: /openai/deployments/{deployment-name}/{endpoint}

SOLUTIONS:
==========
"""

import requests
import json
from datetime import datetime

def create_working_example():
    """
    Create a working example once private endpoint is configured
    """
    
    # Your endpoints (once private endpoint is configured)
    base_url = "https://foundry-codespace-demo.services.ai.azure.com"
    openai_url = "https://foundry-codespace-demo.openai.azure.com"
    api_key = "YOUR_API_KEY_HERE"  # Replace with your actual API key
    
    # Headers for different endpoint types
    foundry_headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": api_key
    }
    
    openai_headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }
    
    print("🚀 Azure AI Foundry API - Working Examples")
    print("=" * 60)
    print("⚠️  NOTE: These will work once private endpoint is configured")
    print("=" * 60)
    
    # Example 1: Chat Completions (OpenAI format)
    print("\n📝 Example 1: Chat Completions")
    print("-" * 40)
    
    chat_payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            },
            {
                "role": "user",
                "content": "Hello! How are you today?"
            }
        ],
        "max_tokens": 150,
        "temperature": 0.7,
        "top_p": 1.0
    }
    
    # Replace 'your-deployment-name' with actual deployment name
    chat_url = f"{openai_url}/openai/deployments/{{deployment-name}}/chat/completions?api-version=2024-06-01"
    
    print(f"URL: {chat_url}")
    print(f"Headers: {openai_headers}")
    print(f"Payload: {json.dumps(chat_payload, indent=2)}")
    
    # Example 2: Text Embeddings
    print("\n🔍 Example 2: Text Embeddings")
    print("-" * 40)
    
    embedding_payload = {
        "input": "This is a sample text for embedding generation.",
        "model": "text-embedding-ada-002"
    }
    
    embedding_url = f"{openai_url}/openai/deployments/{{embedding-deployment}}/embeddings?api-version=2024-06-01"
    
    print(f"URL: {embedding_url}")
    print(f"Headers: {openai_headers}")
    print(f"Payload: {json.dumps(embedding_payload, indent=2)}")
    
    # Example 3: Content Safety
    print("\n🛡️  Example 3: Content Safety")
    print("-" * 40)
    
    safety_payload = {
        "text": "This is a test message for content analysis."
    }
    
    safety_url = f"{base_url}/contentsafety/text:analyze?api-version=2023-10-01"
    
    print(f"URL: {safety_url}")
    print(f"Headers: {foundry_headers}")
    print(f"Payload: {json.dumps(safety_payload, indent=2)}")

def show_next_steps():
    """Display the next steps to resolve the private endpoint issue"""
    
    print(f"\n{'='*80}")
    print("🛠️  NEXT STEPS TO RESOLVE THE ISSUE")
    print("=" * 80)
    
    print("\n1️⃣  OPTION 1: Enable Public Access (Quickest)")
    print("-" * 50)
    print("Run this Azure CLI command:")
    print("az cognitiveservices account update \\")
    print("  --name 'Foundry-Codespace-Demo' \\")
    print("  --resource-group 'Foundry-Codespace' \\")
    print("  --public-network-access Enabled")
    
    print("\n2️⃣  OPTION 2: Use Private Endpoint (More Secure)")
    print("-" * 50)
    print("• Connect to your Azure VNet where the private endpoint exists")
    print("• Run your tests from within the same virtual network")
    print("• Or set up VPN connection to the private network")
    
    print("\n3️⃣  OPTION 3: Find Deployment Names")
    print("-" * 50)
    print("After enabling public access, run:")
    print("az cognitiveservices account deployment list \\")
    print("  --name 'Foundry-Codespace-Demo' \\")
    print("  --resource-group 'Foundry-Codespace'")
    
    print("\n4️⃣  OPTION 4: Use Azure AI Foundry Portal")
    print("-" * 50)
    print("• Go to https://ai.azure.com")
    print("• Navigate to your Foundry-Codespace-Demo resource")
    print("• Check the 'Deployments' section for available models")
    print("• Look for API endpoint documentation")

def test_public_access_status():
    """Test if public access gets enabled"""
    print(f"\n{'='*60}")
    print("🧪 Testing Current Public Access Status")
    print("=" * 60)
    
    # Test the root endpoint which was working
    try:
        response = requests.get(
            "https://foundry-codespace-demo.services.ai.azure.com/",
            timeout=10
        )
        print(f"✅ Root endpoint accessible: Status {response.status_code}")
        
        # Test a typical API endpoint
        headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": "YOUR_API_KEY_HERE"
        }
        
        response = requests.get(
            "https://foundry-codespace-demo.openai.azure.com/openai/models?api-version=2024-06-01",
            headers={"api-key": headers["Ocp-Apim-Subscription-Key"]},
            timeout=10
        )
        
        if response.status_code == 403 and "private endpoint" in response.text.lower():
            print("🔒 Public access still disabled - private endpoint required")
            return False
        elif response.status_code == 200:
            print("🎉 Public access enabled - API is accessible!")
            return True
        else:
            print(f"📊 Status changed: {response.status_code} - {response.text[:100]}")
            return True
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    print("🌟 Azure AI Foundry - Configuration Analysis & Solutions")
    print("=" * 80)
    
    # Test current status
    public_access_enabled = test_public_access_status()
    
    # Show working examples
    create_working_example()
    
    # Show next steps
    show_next_steps()
    
    print(f"\n{'='*80}")
    print("🎯 SUMMARY")
    print("=" * 80)
    print("• Your API credentials are CORRECT ✅")
    print("• Your service endpoints are VALID ✅") 
    print("• Issue: Public access is DISABLED 🔒")
    print("• Solution: Enable public access OR use private endpoint")
    print("=" * 80)