import requests
import json
from datetime import datetime
import concurrent.futures

# Your two Azure AI Foundry endpoints
resources = {
    "Original": {
        "base_url": "https://foundry-codespace-demo.services.ai.azure.com",
        "openai_url": "https://foundry-codespace-demo.openai.azure.com",
        "api_key": "YOUR_ORIGINAL_API_KEY_HERE"  # Replace with your actual API key
    },
    "New": {
        "base_url": "https://f-codespace.services.ai.azure.com",
        "openai_url": "https://f-codespace.openai.azure.com",  # Assuming similar pattern
        "api_key": "YOUR_F_CODESPACE_API_KEY_HERE"  # Replace with your actual F-Codespace API key
    }
}

def test_single_endpoint(resource_name, resource_config, endpoint_path, headers, payload=None, method="GET", test_description=""):
    """Test a single endpoint for one resource"""
    url = f"{resource_config['base_url']}{endpoint_path}"
    
    result = {
        "resource": resource_name,
        "endpoint": endpoint_path,
        "url": url,
        "method": method,
        "description": test_description,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, timeout=15)
        else:
            response = requests.post(url, headers=headers, json=payload, timeout=15)
        
        result.update({
            "status_code": response.status_code,
            "success": response.status_code in [200, 201, 202],
            "headers": dict(response.headers),
            "response_length": len(response.text)
        })
        
        # Parse response
        try:
            result["response"] = response.json()
        except json.JSONDecodeError:
            result["response"] = response.text[:500]  # Truncate long text responses
            
    except requests.exceptions.Timeout:
        result.update({"error": "Timeout", "status_code": "TIMEOUT"})
    except requests.exceptions.ConnectionError:
        result.update({"error": "Connection Error", "status_code": "CONNECTION_ERROR"})
    except Exception as e:
        result.update({"error": str(e), "status_code": "ERROR"})
    
    return result

def compare_resources():
    """Compare both resources across multiple endpoints"""
    
    print("🔄 Azure AI Foundry Resources Comparison")
    print("=" * 80)
    print(f"🎯 Original: {resources['Original']['base_url']}")
    print(f"🆕 New:      {resources['New']['base_url']}")
    print("=" * 80)
    
    # Test endpoints to compare
    test_cases = [
        {
            "path": "/",
            "method": "GET",
            "description": "Root endpoint health check",
            "headers_type": "foundry"
        },
        {
            "path": "/models",
            "method": "GET", 
            "description": "List available models",
            "headers_type": "foundry"
        },
        {
            "path": "/chat/completions?api-version=2024-06-01",
            "method": "POST",
            "description": "Chat completions (direct)",
            "headers_type": "foundry",
            "payload": {
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 50
            }
        },
        {
            "path": "/openai/deployments",
            "method": "GET",
            "description": "List OpenAI deployments",
            "headers_type": "foundry"
        },
        {
            "path": "/contentsafety/text:analyze?api-version=2023-10-01",
            "method": "POST", 
            "description": "Content Safety text analysis",
            "headers_type": "foundry",
            "payload": {
                "text": "This is a test message"
            }
        }
    ]
    
    # OpenAI endpoint tests (using openai_url)
    openai_test_cases = [
        {
            "path": "/openai/models?api-version=2024-06-01",
            "method": "GET",
            "description": "OpenAI - List models",
            "headers_type": "openai",
            "use_openai_url": True
        },
        {
            "path": "/openai/chat/completions?api-version=2024-06-01",
            "method": "POST",
            "description": "OpenAI - Chat completions (no deployment)",
            "headers_type": "openai",
            "use_openai_url": True,
            "payload": {
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 50
            }
        }
    ]
    
    all_results = []
    
    # Test each endpoint for both resources
    for test_case in test_cases + openai_test_cases:
        print(f"\n🧪 Testing: {test_case['description']}")
        print("-" * 60)
        
        resource_results = []
        
        for resource_name, resource_config in resources.items():
            # Determine headers based on type
            if test_case['headers_type'] == 'openai':
                headers = {
                    "Content-Type": "application/json",
                    "api-key": resource_config['api_key']
                }
            else:  # foundry
                headers = {
                    "Content-Type": "application/json", 
                    "Ocp-Apim-Subscription-Key": resource_config['api_key']
                }
            
            # Determine base URL
            if test_case.get('use_openai_url', False):
                base_url = resource_config['openai_url']
            else:
                base_url = resource_config['base_url']
            
            # Override the URL construction for OpenAI endpoints
            if test_case.get('use_openai_url', False):
                url = f"{base_url}{test_case['path']}"
            else:
                url = f"{base_url}{test_case['path']}"
            
            # Run test
            result = test_single_endpoint(
                resource_name=resource_name,
                resource_config={"base_url": base_url},
                endpoint_path=test_case['path'],
                headers=headers,
                payload=test_case.get('payload'),
                method=test_case['method'],
                test_description=test_case['description']
            )
            
            resource_results.append(result)
            all_results.append(result)
            
            # Print result
            status_emoji = "✅" if result.get('success') else "❌"
            status_code = result.get('status_code', 'N/A')
            print(f"  {status_emoji} {resource_name:10} | Status: {status_code:>3} | {url}")
            
            # Print error details if any
            if 'error' in result:
                print(f"    ⚠️  Error: {result['error']}")
            elif not result.get('success') and 'response' in result:
                if isinstance(result['response'], dict) and 'error' in result['response']:
                    print(f"    📄 Response: {result['response']['error'].get('message', 'Unknown error')}")
        
        # Compare results for this test
        if len(resource_results) == 2:
            orig_status = resource_results[0].get('status_code')
            new_status = resource_results[1].get('status_code')
            
            if orig_status != new_status:
                print(f"  🔍 STATUS DIFFERENCE: Original({orig_status}) vs New({new_status})")
    
    return all_results

def analyze_differences(results):
    """Analyze the differences between the two resources"""
    
    print(f"\n{'='*80}")
    print("📊 COMPARATIVE ANALYSIS")
    print("=" * 80)
    
    # Group results by resource
    original_results = [r for r in results if r['resource'] == 'Original']
    new_results = [r for r in results if r['resource'] == 'New'] 
    
    # Success rate comparison
    orig_success = len([r for r in original_results if r.get('success', False)])
    new_success = len([r for r in new_results if r.get('success', False)])
    
    print(f"\n📈 SUCCESS RATES:")
    print(f"  Original Resource: {orig_success}/{len(original_results)} ({orig_success/len(original_results)*100:.1f}%)")
    print(f"  New Resource:      {new_success}/{len(new_results)} ({new_success/len(new_results)*100:.1f}%)")
    
    # Status code comparison
    print(f"\n🔍 STATUS CODE PATTERNS:")
    orig_codes = {}
    new_codes = {}
    
    for r in original_results:
        code = r.get('status_code', 'ERROR')
        orig_codes[code] = orig_codes.get(code, 0) + 1
    
    for r in new_results:
        code = r.get('status_code', 'ERROR')
        new_codes[code] = new_codes.get(code, 0) + 1
    
    print(f"  Original: {orig_codes}")
    print(f"  New:      {new_codes}")
    
    # Identify key differences
    print(f"\n🎯 KEY DIFFERENCES:")
    for i, (orig, new) in enumerate(zip(original_results, new_results)):
        if orig.get('status_code') != new.get('status_code'):
            print(f"  • {orig['description']}")
            print(f"    Original: {orig.get('status_code')} | New: {new.get('status_code')}")
    
    # Network access analysis
    print(f"\n🔒 NETWORK ACCESS ANALYSIS:")
    orig_403_count = len([r for r in original_results if r.get('status_code') == 403])
    new_403_count = len([r for r in new_results if r.get('status_code') == 403])
    
    print(f"  Original 403 (Private endpoint) errors: {orig_403_count}")
    print(f"  New 403 (Private endpoint) errors:      {new_403_count}")
    
    if orig_403_count > new_403_count:
        print("  🎉 New resource appears to have better public access!")
    elif new_403_count > orig_403_count:
        print("  ⚠️  New resource has more access restrictions")
    else:
        print("  📊 Both resources have similar access patterns")

def get_new_api_key():
    """Help get the API key for the new resource"""
    print(f"\n{'='*60}")
    print("🔑 API KEY REQUIRED")
    print("=" * 60)
    print("To test the new resource, we need its API key.")
    print("Run this command to get it:")
    print()
    print("az cognitiveservices account keys list \\")
    print("  --name 'F-codespace' \\")  # Assuming this is the name
    print("  --resource-group 'YOUR_RESOURCE_GROUP'")
    print()
    print("Or check the Azure portal for the API key.")
    
    # Try to get it automatically
    try:
        import subprocess
        result = subprocess.run([
            "az", "cognitiveservices", "account", "list", 
            "--query", "[?contains(endpoints.\"AI Foundry API\", 'f-codespace')].{name:name,resourceGroup:resourceGroup}",
            "--output", "json"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            accounts = json.loads(result.stdout)
            if accounts:
                account = accounts[0]
                print(f"\n💡 Found account: {account['name']} in {account['resourceGroup']}")
                
                # Try to get the key
                key_result = subprocess.run([
                    "az", "cognitiveservices", "account", "keys", "list",
                    "--name", account['name'],
                    "--resource-group", account['resourceGroup'],
                    "--query", "key1",
                    "--output", "tsv"
                ], capture_output=True, text=True, timeout=10)
                
                if key_result.returncode == 0:
                    api_key = key_result.stdout.strip()
                    resources["New"]["api_key"] = api_key
                    print(f"✅ API key retrieved automatically!")
                    return True
    except Exception as e:
        print(f"⚠️  Could not retrieve automatically: {e}")
    
    return False

if __name__ == "__main__":
    print("🚀 Azure AI Foundry Resources Comparison Suite")
    print("=" * 80)
    print(f"🔑 Original API Key: ...{resources['Original']['api_key'][-4:]}")
    print(f"🔑 New API Key:      ...{resources['New']['api_key'][-4:]}")
    print("=" * 80)
    
    # Run the comparison
    results = compare_resources()
    
    # Analyze differences  
    analyze_differences(results)
    
    print(f"\n{'='*80}")
    print("🎉 COMPARISON COMPLETED!")
    print("=" * 80)
    print("💡 Check the analysis above to see which resource works better!")
    print("=" * 80)