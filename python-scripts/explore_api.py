import requests
import json

# Your Azure AI Foundry endpoint
base_url = "https://foundry-codespace-demo.services.ai.azure.com"
headers = {
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": "YOUR_API_KEY_HERE"  # Replace with your actual API key
}

def explore_root_endpoint():
    """Explore what the root endpoint returns"""
    print("🔍 Exploring Root Endpoint")
    print("=" * 50)
    
    # Try GET request to root
    try:
        response = requests.get(base_url, headers=headers, timeout=10)
        print(f"GET / -> Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        # Print full response
        try:
            content = response.json()
            print(f"JSON Response:\n{json.dumps(content, indent=2)}")
        except:
            print(f"Text Response:\n{response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

def try_azure_openai_patterns():
    """Try different Azure OpenAI API patterns"""
    print("\n🤖 Trying Azure OpenAI Patterns")
    print("=" * 50)
    
    # Common Azure OpenAI patterns
    patterns = [
        "/openai/deployments",
        "/openai/models",
        "/cognitive/openai/deployments",
        "/api/openai/deployments",
        "/v1/models",
        "/api/v1/models"
    ]
    
    for pattern in patterns:
        url = f"{base_url}{pattern}"
        print(f"\nTrying GET {pattern}...")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    content = response.json()
                    print(f"  Success! Response: {json.dumps(content, indent=2)[:500]}...")
                except:
                    print(f"  Success! Response: {response.text[:500]}...")
            elif response.status_code == 404:
                print("  Not found")
            else:
                print(f"  Response: {response.text[:200]}...")
                
        except Exception as e:
            print(f"  Error: {e}")

def try_with_api_version():
    """Try endpoints with API version parameter"""
    print("\n🔢 Trying with API Version Parameters")
    print("=" * 50)
    
    api_versions = ["2023-05-15", "2023-12-01-preview", "2024-02-01", "2024-06-01"]
    base_paths = [
        "/openai/deployments",
        "/chat/completions",
        "/openai/chat/completions"
    ]
    
    for api_version in api_versions:
        for path in base_paths:
            url = f"{base_url}{path}?api-version={api_version}"
            print(f"\nTrying GET {path}?api-version={api_version}...")
            
            try:
                response = requests.get(url, headers=headers, timeout=5)
                print(f"  Status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        content = response.json()
                        print(f"  Success! Response: {json.dumps(content, indent=2)[:300]}...")
                        return url  # Found a working endpoint
                    except:
                        print(f"  Success! Response: {response.text[:300]}...")
                        return url
                elif response.status_code != 404:
                    print(f"  Interesting response: {response.text[:100]}...")
                    
            except Exception as e:
                print(f"  Error: {e}")

def check_common_headers():
    """Check if different headers work"""
    print("\n📋 Trying Different Authentication Headers")
    print("=" * 50)
    
    # Try different header combinations
    header_variants = [
        {"Ocp-Apim-Subscription-Key": "YOUR_API_KEY_HERE"},
        {"api-key": "YOUR_API_KEY_HERE"},
        {"Authorization": "Bearer YOUR_API_KEY_HERE"},
        {"x-api-key": "YOUR_API_KEY_HERE"}
    ]
    
    for i, header_variant in enumerate(header_variants):
        print(f"\nTrying header variant {i+1}: {list(header_variant.keys())[0]}")
        test_headers = {"Content-Type": "application/json", **header_variant}
        
        try:
            response = requests.get(f"{base_url}/openai/deployments", headers=test_headers, timeout=5)
            print(f"  Status: {response.status_code}")
            
            if response.status_code != 404:
                print(f"  Response: {response.text[:200]}...")
                
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    print("🚀 Azure AI Foundry API Explorer")
    print("=" * 60)
    
    # Explore root endpoint in detail
    explore_root_endpoint()
    
    # Try various Azure OpenAI patterns
    try_azure_openai_patterns()
    
    # Try with API version parameters
    try_with_api_version()
    
    # Try different authentication headers
    check_common_headers()
    
    print("\n" + "=" * 60)
    print("✅ Exploration completed!")
    print("=" * 60)
    print("\n💡 NEXT STEPS:")
    print("1. Check the Azure AI Foundry portal for deployment names")
    print("2. Look for API documentation in your Azure resource")
    print("3. Try using Azure CLI: az cognitiveservices account list")
    print("4. Contact your Azure administrator for the correct endpoint format")