import requests
import json
from datetime import datetime

# Your Azure AI Foundry endpoints from the service configuration
base_url = "https://foundry-codespace-demo.services.ai.azure.com"
openai_url = "https://foundry-codespace-demo.openai.azure.com"

# API Key (from your existing configuration)
api_key = "YOUR_API_KEY_HERE"  # Replace with your actual API key

def test_endpoint(url, headers, payload=None, method="POST", test_name="Test"):
    """Generic function to test endpoints"""
    print(f"\n{'='*60}")
    print(f"🧪 {test_name}")
    print(f"URL: {url}")
    print(f"Method: {method}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        else:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"✅ Status Code: {response.status_code}")
        print(f"📋 Response Headers: {dict(response.headers)}")
        
        # Parse response
        try:
            response_json = response.json()
            print(f"📄 Response (JSON):\n{json.dumps(response_json, indent=2)}")
        except json.JSONDecodeError:
            print(f"📄 Response (Text): {response.text}")
        
        return response
        
    except requests.exceptions.Timeout:
        print("⏰ Error: Request timed out")
    except requests.exceptions.ConnectionError:
        print("🔌 Error: Connection failed")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return None

def test_ai_foundry_api():
    """Test AI Foundry API endpoints"""
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": api_key
    }
    
    print("🚀 Testing AI Foundry API Endpoints")
    print("=" * 60)
    
    # Test 1: Models endpoint
    test_endpoint(
        f"{base_url}/models",
        headers,
        method="GET",
        test_name="List Available Models"
    )
    
    # Test 2: Chat completions (try different API versions)
    api_versions = ["2024-06-01", "2024-02-01", "2023-12-01-preview"]
    
    for api_version in api_versions:
        chat_payload = {
            "model": "gpt-4",  # or whatever model is available
            "messages": [
                {
                    "role": "user",
                    "content": "Hello, this is a test message from Azure AI Foundry API."
                }
            ],
            "max_tokens": 50,
            "temperature": 0.7
        }
        
        # Try with API version parameter
        test_endpoint(
            f"{base_url}/chat/completions?api-version={api_version}",
            headers,
            chat_payload,
            test_name=f"Chat Completions (API v{api_version})"
        )

def test_openai_endpoints():
    """Test OpenAI-compatible endpoints"""
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key  # OpenAI endpoints typically use 'api-key' header
    }
    
    print("\n🤖 Testing OpenAI-Compatible Endpoints")
    print("=" * 60)
    
    # Test 1: List models via OpenAI endpoint
    test_endpoint(
        f"{openai_url}/openai/models?api-version=2024-06-01",
        headers,
        method="GET",
        test_name="OpenAI - List Models"
    )
    
    # Test 2: Chat completions via OpenAI endpoint
    chat_payload = {
        "messages": [
            {
                "role": "user",
                "content": "Hello from OpenAI endpoint test!"
            }
        ],
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    test_endpoint(
        f"{openai_url}/openai/chat/completions?api-version=2024-06-01",
        headers,
        chat_payload,
        test_name="OpenAI - Chat Completions"
    )

def test_content_safety():
    """Test Content Safety endpoints"""
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": api_key
    }
    
    print("\n🛡️  Testing Content Safety Endpoints")
    print("=" * 60)
    
    # Content safety text analysis
    safety_payload = {
        "text": "This is a test message for content safety analysis."
    }
    
    test_endpoint(
        f"{base_url}/contentsafety/text:analyze?api-version=2023-10-01",
        headers,
        safety_payload,
        test_name="Content Safety - Text Analysis"
    )

def discover_deployment_names():
    """Try to discover available deployment names"""
    print("\n🔍 Attempting to Discover Deployments")
    print("=" * 60)
    
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": api_key
    }
    
    # Try different deployment discovery endpoints
    discovery_urls = [
        f"{base_url}/deployments",
        f"{base_url}/openai/deployments",
        f"{openai_url}/openai/deployments?api-version=2024-06-01",
        f"{base_url}/models",
        f"{openai_url}/openai/models?api-version=2024-06-01"
    ]
    
    for url in discovery_urls:
        test_endpoint(url, headers, method="GET", test_name=f"Discovery: {url.split('/')[-1]}")

def test_with_deployment_id():
    """Test endpoints with common deployment names"""
    print("\n🎯 Testing with Common Deployment Names")
    print("=" * 60)
    
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }
    
    # Common deployment names to try
    deployment_names = [
        "gpt-4",
        "gpt-4o",
        "gpt-35-turbo",
        "gpt-3.5-turbo",
        "text-embedding-ada-002",
        "text-embedding-3-small"
    ]
    
    chat_payload = {
        "messages": [
            {
                "role": "user", 
                "content": "Hello, testing deployment endpoint!"
            }
        ],
        "max_tokens": 50
    }
    
    for deployment in deployment_names:
        # Test OpenAI deployment format
        test_endpoint(
            f"{openai_url}/openai/deployments/{deployment}/chat/completions?api-version=2024-06-01",
            headers,
            chat_payload,
            test_name=f"Deployment Test: {deployment}"
        )

if __name__ == "__main__":
    print("🌟 Azure AI Foundry Complete API Testing Suite")
    print("=" * 80)
    print(f"🎯 Base URL: {base_url}")
    print(f"🤖 OpenAI URL: {openai_url}")
    print(f"🔑 API Key: ...{api_key[-4:]}")
    print("=" * 80)
    
    # Run all tests
    test_ai_foundry_api()
    test_openai_endpoints()
    test_content_safety()
    discover_deployment_names()
    test_with_deployment_id()
    
    print(f"\n{'='*80}")
    print("🎉 Testing Suite Completed!")
    print("💡 Check the results above to identify working endpoints")
    print("=" * 80)