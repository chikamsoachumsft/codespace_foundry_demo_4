"""
Test script for Foundry API connectivity behind VNET.
"""

import unittest
import os
from unittest.mock import patch, Mock
from foundry_client import FoundryAPIClient


class TestFoundryAPIClient(unittest.TestCase):
    """Test cases for FoundryAPIClient."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_url = "https://test.palantirfoundry.com"
        self.test_token = "test_token_123"
        
    def test_client_initialization(self):
        """Test client initialization with parameters."""
        client = FoundryAPIClient(
            api_url=self.test_url,
            api_token=self.test_token
        )
        
        self.assertEqual(client.api_url, self.test_url)
        self.assertEqual(client.api_token, self.test_token)
        self.assertTrue(client.verify_ssl)
        self.assertEqual(client.timeout, 30)
        
    def test_client_initialization_from_env(self):
        """Test client initialization from environment variables."""
        with patch.dict(os.environ, {
            'FOUNDRY_API_URL': self.test_url,
            'FOUNDRY_API_TOKEN': self.test_token
        }):
            client = FoundryAPIClient()
            self.assertEqual(client.api_url, self.test_url)
            self.assertEqual(client.api_token, self.test_token)
    
    def test_proxy_configuration(self):
        """Test proxy configuration from environment."""
        with patch.dict(os.environ, {
            'HTTP_PROXY': 'http://proxy:8080',
            'HTTPS_PROXY': 'https://proxy:8443'
        }):
            client = FoundryAPIClient(
                api_url=self.test_url,
                api_token=self.test_token
            )
            self.assertEqual(client.proxies['http'], 'http://proxy:8080')
            self.assertEqual(client.proxies['https'], 'https://proxy:8443')
    
    @patch('foundry_client.requests.Session.get')
    def test_connectivity_success(self, mock_get):
        """Test successful connectivity check."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        client = FoundryAPIClient(
            api_url=self.test_url,
            api_token=self.test_token
        )
        
        results = client.test_connectivity()
        
        self.assertTrue(results['success'])
        self.assertEqual(results['status_code'], 200)
        self.assertIsNone(results['error'])
        
    @patch('foundry_client.requests.Session.get')
    def test_connectivity_failure(self, mock_get):
        """Test failed connectivity check."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response
        
        client = FoundryAPIClient(
            api_url=self.test_url,
            api_token=self.test_token
        )
        
        results = client.test_connectivity()
        
        self.assertFalse(results['success'])
        self.assertEqual(results['status_code'], 401)
        
    @patch('foundry_client.requests.Session.get')
    def test_connectivity_timeout(self, mock_get):
        """Test connectivity timeout."""
        from requests.exceptions import ConnectTimeout
        mock_get.side_effect = ConnectTimeout("Connection timeout")
        
        client = FoundryAPIClient(
            api_url=self.test_url,
            api_token=self.test_token
        )
        
        results = client.test_connectivity()
        
        self.assertFalse(results['success'])
        self.assertIsNone(results['status_code'])
        self.assertIn('timeout', results['message'].lower())
        
    @patch('foundry_client.requests.Session.get')
    def test_get_request(self, mock_get):
        """Test GET request method."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'test'}
        mock_get.return_value = mock_response
        
        client = FoundryAPIClient(
            api_url=self.test_url,
            api_token=self.test_token
        )
        
        response = client.get('/api/v1/test')
        
        self.assertEqual(response.status_code, 200)
        mock_get.assert_called_once()
        
    @patch('foundry_client.requests.Session.post')
    def test_post_request(self, mock_post):
        """Test POST request method."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response
        
        client = FoundryAPIClient(
            api_url=self.test_url,
            api_token=self.test_token
        )
        
        test_data = {'key': 'value'}
        response = client.post('/api/v1/test', data=test_data)
        
        self.assertEqual(response.status_code, 201)
        mock_post.assert_called_once()
        
    def test_check_vnet_configuration(self):
        """Test VNET configuration check."""
        client = FoundryAPIClient(
            api_url=self.test_url,
            api_token=self.test_token
        )
        
        config = client.check_vnet_configuration()
        
        self.assertEqual(config['api_url'], self.test_url)
        self.assertTrue(config['has_token'])
        self.assertEqual(config['token_length'], len(self.test_token))
        self.assertTrue(config['verify_ssl'])


if __name__ == '__main__':
    unittest.main()
