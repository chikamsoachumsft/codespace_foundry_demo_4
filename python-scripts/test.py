import requests
import json
import os
from datetime import datetime

# Azure AI Services endpoint
base_url = "https://foundry-codespace-demo.services.ai.azure.com"

# Headers for authentication - you'll need to set your API key
headers = {
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": os.getenv("AZURE_AI_API_KEY", "YOUR_API_KEY_HERE"),
    # Alternative authentication header if using different auth method:
    # "Authorization": f"Bearer {os.getenv('AZURE_AI_TOKEN', 'YOUR_TOKEN_HERE')}"
}

def test_post_request(endpoint_path="/", payload=None, test_name="Basic POST"):
    """
    Test function to send POST requests to the AI services endpoint
    """
    url = f"{base_url}{endpoint_path}"
    
    print(f"\n{'='*50}")
    print(f"Testing: {test_name}")
    print(f"URL: {url}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")
    
    try:
        response = requests.post(
            url, 
            headers=headers, 
            json=payload,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        # Try to parse JSON response
        try:
            response_json = response.json()
            print(f"Response Body (JSON): {json.dumps(response_json, indent=2)}")
        except json.JSONDecodeError:
            print(f"Response Body (Text): {response.text}")
            
        return response
        
    except requests.exceptions.Timeout:
        print("Error: Request timed out")
    except requests.exceptions.ConnectionError:
        print("Error: Connection failed")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def test_health_check():
    """Test basic health/status endpoint"""
    return test_post_request("/health", {}, "Health Check")

def test_chat_completion():
    """Test chat completion endpoint (common for AI services)"""
    payload = {
        "messages": [
            {
                "role": "user",
                "content": "Hello, this is a test message."
            }
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }
    return test_post_request("/chat/completions", payload, "Chat Completion")

def test_text_generation():
    """Test text generation endpoint"""
    payload = {
        "prompt": "Generate a short test response:",
        "max_tokens": 50,
        "temperature": 0.5
    }
    return test_post_request("/completions", payload, "Text Generation")

def test_embeddings():
    """Test embeddings endpoint"""
    payload = {
        "input": "This is a test sentence for embeddings.",
        "model": "text-embedding-ada-002"
    }
    return test_post_request("/embeddings", payload, "Embeddings")

def test_custom_endpoint():
    """Test a custom endpoint - modify as needed"""
    payload = {
        "query": "test query",
        "parameters": {
            "max_results": 5
        }
    }
    return test_post_request("/custom", payload, "Custom Endpoint")

def discover_endpoints():
    """Try to discover available endpoints using GET requests"""
    print(f"\n{'='*50}")
    print("ENDPOINT DISCOVERY")
    print(f"{'='*50}")
    
    # Common paths to try
    paths_to_try = [
        "/",
        "/health",
        "/status",
        "/api",
        "/api/v1",
        "/openapi.json",
        "/swagger.json",
        "/docs",
        "/v1/chat/completions",
        "/openai/deployments",
        "/openai/chat/completions",
        "/azure-openai/chat/completions",
        "/inference/chat/completions",
        "/models",
        "/deployments"
    ]
    
    successful_endpoints = []
    
    for path in paths_to_try:
        url = f"{base_url}{path}"
        print(f"\nTrying GET {path}...")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"  Status Code: {response.status_code}")
            
            if response.status_code in [200, 201, 202]:
                successful_endpoints.append((path, response.status_code))
                try:
                    content = response.json()
                    print(f"  Response: {json.dumps(content, indent=2)[:200]}...")
                except:
                    print(f"  Response: {response.text[:200]}...")
            elif response.status_code == 405:  # Method not allowed - endpoint exists but needs POST
                successful_endpoints.append((path, f"{response.status_code} (Method Not Allowed - try POST)"))
                
        except Exception as e:
            print(f"  Error: {e}")
    
    print(f"\n{'='*30}")
    print("SUCCESSFUL ENDPOINTS:")
    print(f"{'='*30}")
    for endpoint, status in successful_endpoints:
        print(f"  {endpoint} -> {status}")
    
    return successful_endpoints

def test_foundry_specific_endpoints():
    """Test Azure AI Foundry specific endpoints"""
    print(f"\n{'='*50}")
    print("TESTING FOUNDRY-SPECIFIC ENDPOINTS")
    print(f"{'='*50}")
    
    # Azure AI Foundry might use different endpoint patterns
    foundry_endpoints = [
        ("/openai/deployments/{deployment-id}/chat/completions", "OpenAI Chat Completions"),
        ("/openai/deployments/{deployment-id}/completions", "OpenAI Completions"),
        ("/openai/deployments/{deployment-id}/embeddings", "OpenAI Embeddings"),
        ("/inference/chat/completions", "Inference Chat"),
        ("/inference/completions", "Inference Completions"),
        ("/models", "Available Models"),
        ("/deployments", "Available Deployments")
    ]
    
    for endpoint, description in foundry_endpoints:
        if "{deployment-id}" in endpoint:
            # Try with a placeholder deployment ID
            test_endpoint = endpoint.replace("{deployment-id}", "gpt-35-turbo")
            print(f"\nTrying {description} with placeholder deployment ID...")
            test_post_request(test_endpoint, {
                "messages": [{"role": "user", "content": "test"}],
                "max_tokens": 10
            }, f"{description} (gpt-35-turbo)")
        else:
            print(f"\nTrying {description}...")
            if "models" in endpoint or "deployments" in endpoint:
                # Use GET for listing endpoints
                url = f"{base_url}{endpoint}"
                try:
                    response = requests.get(url, headers=headers, timeout=10)
                    print(f"GET {endpoint} -> Status: {response.status_code}")
                    if response.status_code == 200:
                        try:
                            print(f"Response: {json.dumps(response.json(), indent=2)}")
                        except:
                            print(f"Response: {response.text}")
                except Exception as e:
                    print(f"Error: {e}")
            else:
                test_post_request(endpoint, {
                    "messages": [{"role": "user", "content": "test"}],
                    "max_tokens": 10
                }, description)

if __name__ == "__main__":
    print("Azure AI Foundry Services Endpoint Testing")
    print(f"Base URL: {base_url}")
    
    # Check if API key is set
    api_key = headers.get("Ocp-Apim-Subscription-Key", "")
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        print("\n⚠️  WARNING: Please set your AZURE_AI_API_KEY environment variable")
        print("You can set it by running: $env:AZURE_AI_API_KEY='your-actual-api-key'")
    else:
        print(f"✅ API Key is set (ending with: ...{api_key[-4:]})")
    
    # First, discover available endpoints
    print("\n🔍 Starting endpoint discovery...")
    successful_endpoints = discover_endpoints()
    
    # Test Foundry-specific endpoints
    test_foundry_specific_endpoints()
    
    print(f"\n{'='*50}")
    print("RECOMMENDATIONS:")
    print(f"{'='*50}")
    print("Based on the 404 error you received, try these approaches:")
    print("1. Check if you need to specify a deployment ID in the URL")
    print("2. The correct format might be: /openai/deployments/{deployment-name}/chat/completions")
    print("3. Contact your Azure admin to get the exact endpoint paths")
    print("4. Check the Azure AI Foundry portal for the correct API endpoints")
    
    print(f"\n{'='*50}")
    print("Testing completed!")
    print(f"{'='*50}")