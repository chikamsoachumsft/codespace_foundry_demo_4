import requests
import json
from datetime import datetime

# Your second Azure AI Foundry endpoints
base_url = "https://f-codespace.services.ai.azure.com"
openai_url = "https://f-codespace.openai.azure.com"

# API Key for the second resource
api_key = "YOUR_F_CODESPACE_API_KEY_HERE"  # Replace with your actual F-Codespace API key

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
    
    print("🚀 Testing AI Foundry API Endpoints (F-Codespace)")
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
                    "content": "Hello, this is a test message from F-Codespace Azure AI Foundry API."
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
    
    print("\n🤖 Testing OpenAI-Compatible Endpoints (F-Codespace)")
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
                "content": "Hello from F-Codespace OpenAI endpoint test!"
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
    
    print("\n🛡️  Testing Content Safety Endpoints (F-Codespace)")
    print("=" * 60)
    
    # Content safety text analysis
    safety_payload = {
        "text": "This is a test message for content safety analysis from F-Codespace."
    }
    
    test_endpoint(
        f"{base_url}/contentsafety/text:analyze?api-version=2023-10-01",
        headers,
        safety_payload,
        test_name="Content Safety - Text Analysis"
    )

def discover_deployment_names():
    """Try to discover available deployment names"""
    print("\n🔍 Attempting to Discover Deployments (F-Codespace)")
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
    print("\n🎯 Testing with Common Deployment Names (F-Codespace)")
    print("=" * 60)
    
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }
    
    # Common deployment names to try
    deployment_names = [
        "gpt-4",
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-35-turbo",
        "gpt-3.5-turbo",
        "text-embedding-ada-002",
        "text-embedding-3-small",
        "text-embedding-3-large"
    ]
    
    chat_payload = {
        "messages": [
            {
                "role": "user", 
                "content": "Hello from F-Codespace deployment test!"
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

def test_alternative_authentication():
    """Test different authentication methods"""
    print("\n🔐 Testing Alternative Authentication Methods (F-Codespace)")
    print("=" * 60)
    
    # Try different header combinations
    auth_methods = [
        {
            "name": "Ocp-Apim-Subscription-Key",
            "headers": {
                "Content-Type": "application/json",
                "Ocp-Apim-Subscription-Key": api_key
            }
        },
        {
            "name": "api-key",
            "headers": {
                "Content-Type": "application/json",
                "api-key": api_key
            }
        },
        {
            "name": "Authorization Bearer",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
        },
        {
            "name": "x-api-key",
            "headers": {
                "Content-Type": "application/json",
                "x-api-key": api_key
            }
        }
    ]
    
    test_payload = {
        "messages": [
            {
                "role": "user",
                "content": "Testing authentication method"
            }
        ],
        "max_tokens": 10
    }
    
    for auth_method in auth_methods:
        test_endpoint(
            f"{base_url}/chat/completions?api-version=2024-06-01",
            auth_method["headers"],
            test_payload,
            test_name=f"Auth Test: {auth_method['name']}"
        )

def test_root_endpoint_details():
    """Test root endpoint in detail"""
    print("\n🏠 Testing Root Endpoint Details (F-Codespace)")
    print("=" * 60)
    
    methods_to_try = ["GET", "POST", "OPTIONS"]
    
    for method in methods_to_try:
        headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": api_key
        }
        
        if method == "POST":
            payload = {"test": "data"}
        else:
            payload = None
            
        test_endpoint(
            base_url + "/",
            headers,
            payload,
            method=method,
            test_name=f"Root Endpoint - {method}"
        )

if __name__ == "__main__":
    print("🌟 Azure AI Foundry Complete API Testing Suite - F-Codespace Resource")
    print("=" * 80)
    print(f"🎯 Base URL: {base_url}")
    print(f"🤖 OpenAI URL: {openai_url}")
    print(f"🔑 API Key: ...{api_key[-4:]}")
    print("=" * 80)
    
    # Run all tests
    test_root_endpoint_details()
    test_ai_foundry_api()
    test_openai_endpoints()
    test_content_safety()
    discover_deployment_names()
    test_with_deployment_id()
    test_alternative_authentication()
    
    print(f"\n{'='*80}")
    print("🎉 F-Codespace Testing Suite Completed!")
    print("💡 Compare these results with the original Foundry-Codespace-Demo")
    print("🔍 Look for differences in status codes and access patterns")
    print("=" * 80)