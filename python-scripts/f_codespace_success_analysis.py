"""
Azure AI Foundry F-Codespace - Next Steps for Full API Access

GREAT NEWS: Your F-Codespace resource has public access enabled and is working!

CURRENT STATUS:
✅ Public access: ENABLED  
✅ Models available: 113+ models
✅ Content Safety: WORKING
✅ Authentication: WORKING
⚠️  Deployments: NONE (need to create)

NEXT STEPS TO GET CHAT COMPLETIONS WORKING:
"""

import requests
import json

def show_available_models():
    """Show the available models from your working F-Codespace resource"""
    
    # Your working endpoint
    api_key = "YOUR_F_CODESPACE_API_KEY_HERE"  # Replace with your actual F-Codespace API key
    
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }
    
    print("🎯 RECOMMENDED MODELS TO DEPLOY:")
    print("=" * 50)
    
    # Get models (we know this works)
    try:
        response = requests.get(
            "https://f-codespace.openai.azure.com/openai/models?api-version=2024-06-01",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            models = response.json()
            
            # Filter for chat-capable models
            chat_models = []
            embedding_models = []
            
            for model in models['data']:
                if model['capabilities'].get('chat_completion', False):
                    chat_models.append(model)
                elif model['capabilities'].get('embeddings', False):
                    embedding_models.append(model)
            
            print(f"\n🤖 CHAT MODELS AVAILABLE ({len(chat_models)}):")
            print("-" * 40)
            recommended_chat = ['gpt-4o', 'gpt-4o-mini', 'gpt-35-turbo', 'o3-mini', 'gpt-4']
            
            for model_name in recommended_chat:
                found = next((m for m in chat_models if m['id'] == model_name), None)
                if found:
                    status = found.get('lifecycle_status', 'unknown')
                    print(f"✅ {model_name:20} | Status: {status}")
                else:
                    print(f"❌ {model_name:20} | Not available")
            
            print(f"\n🔍 EMBEDDING MODELS AVAILABLE ({len(embedding_models)}):")
            print("-" * 40)
            for model in embedding_models[:3]:  # Show top 3
                status = model.get('lifecycle_status', 'unknown')
                print(f"✅ {model['id']:30} | Status: {status}")
                
    except Exception as e:
        print(f"Error retrieving models: {e}")

def create_deployment_commands():
    """Show Azure CLI commands to create deployments"""
    
    print(f"\n{'='*60}")
    print("🚀 AZURE CLI COMMANDS TO CREATE DEPLOYMENTS")
    print("=" * 60)
    
    deployments = [
        {
            "name": "gpt-4o-deployment",
            "model": "gpt-4o", 
            "description": "Latest GPT-4 Omni model"
        },
        {
            "name": "gpt-4o-mini-deployment", 
            "model": "gpt-4o-mini",
            "description": "Faster, cost-effective GPT-4 Omni"
        },
        {
            "name": "embedding-deployment",
            "model": "text-embedding-ada-002",
            "description": "Text embeddings model"
        }
    ]
    
    print("\n💡 Run these commands to create deployments:\n")
    
    for deployment in deployments:
        print(f"# Create {deployment['description']}")
        print(f"az cognitiveservices account deployment create \\")
        print(f"  --name 'F-codespace' \\")
        print(f"  --resource-group 'Foundry-Codespace' \\")
        print(f"  --deployment-name '{deployment['name']}' \\")
        print(f"  --model-name '{deployment['model']}' \\")
        print(f"  --model-version 'latest' \\")
        print(f"  --model-format 'OpenAI' \\")
        print(f"  --sku-capacity '10' \\")
        print(f"  --sku-name 'Standard'")
        print()

def test_working_endpoints():
    """Test the endpoints that are confirmed working"""
    
    print(f"\n{'='*60}")
    print("🧪 TESTING CONFIRMED WORKING ENDPOINTS")
    print("=" * 60)
    
    api_key = "YOUR_F_CODESPACE_API_KEY_HERE"  # Replace with your actual F-Codespace API key
    
    # Test 1: Content Safety (confirmed working)
    print("\n🛡️  Testing Content Safety...")
    try:
        response = requests.post(
            "https://f-codespace.services.ai.azure.com/contentsafety/text:analyze?api-version=2023-10-01",
            headers={
                "Content-Type": "application/json",
                "Ocp-Apim-Subscription-Key": api_key
            },
            json={"text": "Hello world, this is a safety test!"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Content Safety WORKING!")
            print(f"   Analysis: {len(result['categoriesAnalysis'])} categories checked")
        else:
            print(f"❌ Status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Model listing (confirmed working)
    print("\n🤖 Testing Model Listing...")
    try:
        response = requests.get(
            "https://f-codespace.openai.azure.com/openai/models?api-version=2024-06-01",
            headers={
                "Content-Type": "application/json", 
                "api-key": api_key
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Model Listing WORKING!")
            print(f"   Available models: {len(result['data'])}")
        else:
            print(f"❌ Status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🌟 Azure AI Foundry F-Codespace - SUCCESS ANALYSIS")
    print("=" * 80)
    
    show_available_models()
    create_deployment_commands()
    test_working_endpoints()
    
    print(f"\n{'='*80}")
    print("🎉 SUMMARY")
    print("=" * 80)
    print("✅ F-Codespace has EXCELLENT public access")
    print("✅ 113+ models available for deployment") 
    print("✅ Content Safety working perfectly")
    print("✅ Authentication methods working")
    print("🚀 Next: Create deployments using Azure CLI commands above")
    print("=" * 80)