#!/usr/bin/env python3
"""
Quick start script to test Foundry API connectivity.
This script provides an interactive setup and testing experience.
"""

import os
import sys
from pathlib import Path


def check_environment():
    """Check if environment is properly set up."""
    print("Checking environment setup...")
    
    issues = []
    
    # Check if .env exists
    env_file = Path('.env')
    if not env_file.exists():
        issues.append("- .env file not found. Copy .env.example to .env and configure it.")
    
    # Check if dependencies are installed
    try:
        import requests
        import dotenv
        print("✓ Dependencies installed")
    except ImportError as e:
        issues.append(f"- Missing dependency: {e.name}. Run: pip install -r requirements.txt")
    
    # Check environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    api_url = os.getenv('FOUNDRY_API_URL')
    api_token = os.getenv('FOUNDRY_API_TOKEN')
    
    if not api_url or api_url == 'https://your-foundry-instance.palantirfoundry.com':
        issues.append("- FOUNDRY_API_URL not configured in .env")
    else:
        print(f"✓ API URL configured: {api_url}")
    
    if not api_token or api_token == 'your_api_token_here':
        issues.append("- FOUNDRY_API_TOKEN not configured in .env")
    else:
        print(f"✓ API Token configured (length: {len(api_token)})")
    
    if issues:
        print("\n⚠ Setup Issues Found:")
        for issue in issues:
            print(f"  {issue}")
        return False
    
    print("\n✓ Environment setup looks good!")
    return True


def run_tests():
    """Run connectivity tests."""
    print("\n" + "=" * 60)
    print("Running Foundry API Connectivity Tests")
    print("=" * 60 + "\n")
    
    from foundry_client import FoundryAPIClient
    
    # Create client
    client = FoundryAPIClient()
    
    # Check configuration
    print("1. Checking VNET Configuration...")
    config = client.check_vnet_configuration()
    print()
    
    # Test connectivity
    print("2. Testing API Connectivity...")
    results = client.test_connectivity()
    print()
    
    # Display results
    print("=" * 60)
    print("Results Summary:")
    print("=" * 60)
    
    if results['success']:
        print("✓ SUCCESS: Connected to Foundry API")
        print(f"  Status Code: {results['status_code']}")
        print(f"  Message: {results['message']}")
        return 0
    else:
        print("✗ FAILED: Could not connect to Foundry API")
        print(f"  Status Code: {results['status_code']}")
        print(f"  Message: {results['message']}")
        if results['error']:
            print(f"  Error: {results['error']}")
        
        print("\nTroubleshooting Tips:")
        print("- Verify your API URL and token are correct")
        print("- Check if you're connected to the VNET")
        print("- Verify firewall rules allow outbound HTTPS")
        print("- Check DNS resolution for the Foundry hostname")
        print("- Review logs for more details")
        
        return 1


def main():
    """Main entry point."""
    print("=" * 60)
    print("Foundry API VNET Test - Quick Start")
    print("=" * 60 + "\n")
    
    # Check environment
    if not check_environment():
        print("\nPlease fix the issues above and try again.")
        print("\nQuick setup:")
        print("  1. cp .env.example .env")
        print("  2. Edit .env with your settings")
        print("  3. pip install -r requirements.txt")
        print("  4. python quick_start.py")
        return 1
    
    # Run tests
    return run_tests()


if __name__ == '__main__':
    sys.exit(main())