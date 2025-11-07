"""
Foundry API Client for testing connectivity behind VNET.
"""

import os
import logging
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FoundryAPIClient:
    """Client for interacting with Palantir Foundry API behind a VNET."""
    
    def __init__(
        self,
        api_url: Optional[str] = None,
        api_token: Optional[str] = None,
        verify_ssl: bool = True,
        timeout: int = 30
    ):
        """
        Initialize the Foundry API client.
        
        Args:
            api_url: The Foundry API URL (defaults to env var FOUNDRY_API_URL)
            api_token: The API token for authentication (defaults to env var FOUNDRY_API_TOKEN)
            verify_ssl: Whether to verify SSL certificates
            timeout: Request timeout in seconds
        """
        self.api_url = (api_url or os.getenv('FOUNDRY_API_URL', '')).rstrip('/')
        self.api_token = api_token or os.getenv('FOUNDRY_API_TOKEN', '')
        self.verify_ssl = verify_ssl
        self.timeout = timeout
        
        # Configure proxy if specified
        self.proxies = {}
        if os.getenv('HTTP_PROXY'):
            self.proxies['http'] = os.getenv('HTTP_PROXY')
        if os.getenv('HTTPS_PROXY'):
            self.proxies['https'] = os.getenv('HTTPS_PROXY')
        
        # Set up session
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        logger.info(f"Initialized Foundry API client for URL: {self.api_url}")
        if self.proxies:
            logger.info(f"Using proxies: {list(self.proxies.keys())}")
    
    def test_connectivity(self) -> Dict[str, Any]:
        """
        Test basic connectivity to the Foundry API.
        
        Returns:
            Dict containing test results
        """
        results = {
            'success': False,
            'status_code': None,
            'message': '',
            'error': None
        }
        
        try:
            logger.info("Testing connectivity to Foundry API...")
            
            # Try to hit a basic health/info endpoint
            # Most Foundry instances have a /api/v1/ endpoint
            test_url = f"{self.api_url}/api/v1/"
            
            response = self.session.get(
                test_url,
                verify=self.verify_ssl,
                timeout=self.timeout,
                proxies=self.proxies
            )
            
            results['status_code'] = response.status_code
            
            if response.status_code < 400:
                results['success'] = True
                results['message'] = f"Successfully connected to Foundry API (Status: {response.status_code})"
                logger.info(results['message'])
            else:
                results['message'] = f"Connection failed with status code: {response.status_code}"
                logger.warning(results['message'])
                
        except requests.exceptions.ConnectTimeout as e:
            results['error'] = f"Connection timeout: {str(e)}"
            results['message'] = "Connection timeout - check VNET connectivity and firewall rules"
            logger.error(results['message'])
        except requests.exceptions.ConnectionError as e:
            results['error'] = f"Connection error: {str(e)}"
            results['message'] = "Connection error - check VNET configuration and DNS resolution"
            logger.error(results['message'])
        except requests.exceptions.SSLError as e:
            results['error'] = f"SSL error: {str(e)}"
            results['message'] = "SSL error - check certificate configuration"
            logger.error(results['message'])
        except Exception as e:
            results['error'] = str(e)
            results['message'] = f"Unexpected error: {str(e)}"
            logger.error(results['message'])
        
        return results
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        """
        Make a GET request to the Foundry API.
        
        Args:
            endpoint: API endpoint (without base URL)
            params: Query parameters
            
        Returns:
            Response object
        """
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        logger.debug(f"GET request to: {url}")
        
        response = self.session.get(
            url,
            params=params,
            verify=self.verify_ssl,
            timeout=self.timeout,
            proxies=self.proxies
        )
        
        logger.debug(f"Response status: {response.status_code}")
        return response
    
    def post(self, endpoint: str, data: Optional[Dict] = None) -> requests.Response:
        """
        Make a POST request to the Foundry API.
        
        Args:
            endpoint: API endpoint (without base URL)
            data: JSON data to send
            
        Returns:
            Response object
        """
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        logger.debug(f"POST request to: {url}")
        
        response = self.session.post(
            url,
            json=data,
            verify=self.verify_ssl,
            timeout=self.timeout,
            proxies=self.proxies
        )
        
        logger.debug(f"Response status: {response.status_code}")
        return response
    
    def check_vnet_configuration(self) -> Dict[str, Any]:
        """
        Check VNET configuration and network settings.
        
        Returns:
            Dict containing configuration check results
        """
        config_info = {
            'api_url': self.api_url,
            'has_token': bool(self.api_token),
            'token_length': len(self.api_token) if self.api_token else 0,
            'verify_ssl': self.verify_ssl,
            'timeout': self.timeout,
            'proxies_configured': bool(self.proxies),
            'proxy_details': self.proxies
        }
        
        logger.info("VNET Configuration:")
        for key, value in config_info.items():
            if 'token' not in key.lower():
                logger.info(f"  {key}: {value}")
            else:
                logger.info(f"  {key}: {'*' * min(value, 10) if isinstance(value, int) and value > 0 else value}")
        
        return config_info


def main():
    """Main function for testing the Foundry API client."""
    print("=" * 60)
    print("Foundry API VNET Connectivity Test")
    print("=" * 60)
    print()
    
    # Initialize client
    client = FoundryAPIClient()
    
    # Check configuration
    print("Checking configuration...")
    config = client.check_vnet_configuration()
    print()
    
    # Test connectivity
    print("Testing connectivity to Foundry API...")
    results = client.test_connectivity()
    print()
    
    # Display results
    print("=" * 60)
    print("Test Results:")
    print("=" * 60)
    print(f"Success: {results['success']}")
    print(f"Status Code: {results['status_code']}")
    print(f"Message: {results['message']}")
    if results['error']:
        print(f"Error Details: {results['error']}")
    print()
    
    return 0 if results['success'] else 1


if __name__ == '__main__':
    exit(main())
