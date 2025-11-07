# Azure AI Foundry Complete API Testing Suite - PowerShell Version
# For testing from remote Windows machine in VNet with private endpoint access

# Your Azure AI Foundry endpoints from the service configuration
$baseUrl = "https://foundry-codespace-demo.services.ai.azure.com"
$openaiUrl = "https://foundry-codespace-demo.openai.azure.com"

# API Key (from your existing configuration)
$apiKey = "YOUR_API_KEY_HERE"  # Replace with your actual API key

function Test-Endpoint {
    param(
        [string]$Url,
        [hashtable]$Headers,
        [object]$Payload = $null,
        [string]$Method = "POST",
        [string]$TestName = "Test"
    )
    
    Write-Host "`n$('=' * 60)" -ForegroundColor Yellow
    Write-Host "🧪 $TestName" -ForegroundColor Cyan
    Write-Host "URL: $Url" -ForegroundColor Gray
    Write-Host "Method: $Method" -ForegroundColor Gray
    Write-Host "Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
    Write-Host "$('=' * 60)" -ForegroundColor Yellow
    
    try {
        $splat = @{
            Uri = $Url
            Headers = $Headers
            Method = $Method
            TimeoutSec = 30
            ErrorAction = 'Stop'
        }
        
        if ($Payload -and $Method -eq "POST") {
            $splat.Body = ($Payload | ConvertTo-Json -Depth 10)
        }
        
        $response = Invoke-RestMethod @splat -ResponseHeadersVariable responseHeaders
        
        Write-Host "✅ Status Code: 200 (Success)" -ForegroundColor Green
        Write-Host "📋 Response Headers:" -ForegroundColor Blue
        
        # Display response headers
        foreach ($header in $responseHeaders.GetEnumerator()) {
            Write-Host "    $($header.Key): $($header.Value)" -ForegroundColor Gray
        }
        
        # Parse and display response
        if ($response) {
            Write-Host "📄 Response (JSON):" -ForegroundColor Blue
            Write-Host ($response | ConvertTo-Json -Depth 10) -ForegroundColor White
        }
        
        return $response
        
    } catch {
        $statusCode = "Unknown"
        $errorMessage = $_.Exception.Message
        
        # Try to extract status code from exception
        if ($_.Exception.Response) {
            $statusCode = [int]$_.Exception.Response.StatusCode
            
            # Try to read error response body
            try {
                $errorStream = $_.Exception.Response.GetResponseStream()
                $reader = New-Object System.IO.StreamReader($errorStream)
                $errorBody = $reader.ReadToEnd()
                $reader.Close()
                
                if ($errorBody) {
                    $errorJson = $errorBody | ConvertFrom-Json
                    Write-Host "❌ Status Code: $statusCode" -ForegroundColor Red
                    Write-Host "📄 Error Response:" -ForegroundColor Red
                    Write-Host ($errorJson | ConvertTo-Json -Depth 10) -ForegroundColor Red
                    return $null
                }
            } catch {
                # Ignore error parsing errors
            }
        }
        
        if ($errorMessage -like "*timeout*") {
            Write-Host "⏰ Error: Request timed out" -ForegroundColor Red
        } elseif ($errorMessage -like "*connection*") {
            Write-Host "🔌 Error: Connection failed" -ForegroundColor Red
        } else {
            Write-Host "❌ Error: $errorMessage" -ForegroundColor Red
            if ($statusCode -ne "Unknown") {
                Write-Host "   Status Code: $statusCode" -ForegroundColor Red
            }
        }
        
        return $null
    }
}

function Test-AIFoundryAPI {
    $headers = @{
        "Content-Type" = "application/json"
        "Ocp-Apim-Subscription-Key" = $apiKey
    }
    
    Write-Host "🚀 Testing AI Foundry API Endpoints" -ForegroundColor Cyan
    Write-Host "=" * 60 -ForegroundColor Yellow
    
    # Test 1: Models endpoint
    Test-Endpoint -Url "$baseUrl/models" -Headers $headers -Method "GET" -TestName "List Available Models"
    
    # Test 2: Chat completions (try different API versions)
    $apiVersions = @("2024-06-01", "2024-02-01", "2023-12-01-preview")
    
    foreach ($apiVersion in $apiVersions) {
        $chatPayload = @{
            model = "gpt-4"
            messages = @(
                @{
                    role = "user"
                    content = "Hello, this is a test message from Azure AI Foundry API via PowerShell."
                }
            )
            max_tokens = 50
            temperature = 0.7
        }
        
        Test-Endpoint -Url "$baseUrl/chat/completions?api-version=$apiVersion" -Headers $headers -Payload $chatPayload -TestName "Chat Completions (API v$apiVersion)"
    }
}

function Test-OpenAIEndpoints {
    $headers = @{
        "Content-Type" = "application/json"
        "api-key" = $apiKey
    }
    
    Write-Host "`n🤖 Testing OpenAI-Compatible Endpoints" -ForegroundColor Cyan
    Write-Host "=" * 60 -ForegroundColor Yellow
    
    # Test 1: List models via OpenAI endpoint
    Test-Endpoint -Url "$openaiUrl/openai/models?api-version=2024-06-01" -Headers $headers -Method "GET" -TestName "OpenAI - List Models"
    
    # Test 2: Chat completions via OpenAI endpoint
    $chatPayload = @{
        messages = @(
            @{
                role = "user"
                content = "Hello from OpenAI endpoint test via PowerShell!"
            }
        )
        max_tokens = 50
        temperature = 0.7
    }
    
    Test-Endpoint -Url "$openaiUrl/openai/chat/completions?api-version=2024-06-01" -Headers $headers -Payload $chatPayload -TestName "OpenAI - Chat Completions"
}

function Test-ContentSafety {
    $headers = @{
        "Content-Type" = "application/json"
        "Ocp-Apim-Subscription-Key" = $apiKey
    }
    
    Write-Host "`n🛡️  Testing Content Safety Endpoints" -ForegroundColor Cyan
    Write-Host "=" * 60 -ForegroundColor Yellow
    
    $safetyPayload = @{
        text = "This is a test message for content safety analysis from PowerShell."
    }
    
    Test-Endpoint -Url "$baseUrl/contentsafety/text:analyze?api-version=2023-10-01" -Headers $headers -Payload $safetyPayload -TestName "Content Safety - Text Analysis"
}

function Find-DeploymentNames {
    Write-Host "`n🔍 Attempting to Discover Deployments" -ForegroundColor Cyan
    Write-Host "=" * 60 -ForegroundColor Yellow
    
    $headers = @{
        "Content-Type" = "application/json"
        "Ocp-Apim-Subscription-Key" = $apiKey
    }
    
    $discoveryUrls = @(
        "$baseUrl/deployments",
        "$baseUrl/openai/deployments",
        "$openaiUrl/openai/deployments?api-version=2024-06-01",
        "$baseUrl/models",
        "$openaiUrl/openai/models?api-version=2024-06-01"
    )
    
    foreach ($url in $discoveryUrls) {
        $testName = "Discovery: " + ($url -split '/')[-1]
        Test-Endpoint -Url $url -Headers $headers -Method "GET" -TestName $testName
    }
}

function Test-WithDeploymentID {
    Write-Host "`n🎯 Testing with Common Deployment Names" -ForegroundColor Cyan
    Write-Host "=" * 60 -ForegroundColor Yellow
    
    $headers = @{
        "Content-Type" = "application/json"
        "api-key" = $apiKey
    }
    
    $deploymentNames = @(
        "gpt-4",
        "gpt-4o",
        "gpt-35-turbo",
        "gpt-3.5-turbo",
        "text-embedding-ada-002",
        "text-embedding-3-small"
    )
    
    $chatPayload = @{
        messages = @(
            @{
                role = "user"
                content = "Hello, testing deployment endpoint from PowerShell!"
            }
        )
        max_tokens = 50
    }
    
    foreach ($deployment in $deploymentNames) {
        Test-Endpoint -Url "$openaiUrl/openai/deployments/$deployment/chat/completions?api-version=2024-06-01" -Headers $headers -Payload $chatPayload -TestName "Deployment Test: $deployment"
    }
}

function Test-NetworkConnectivity {
    Write-Host "`n🌐 Testing Network Connectivity from VNet" -ForegroundColor Cyan
    Write-Host "=" * 60 -ForegroundColor Yellow
    
    # Test basic DNS resolution
    Write-Host "`n🔍 Testing DNS Resolution:" -ForegroundColor Blue
    
    $endpoints = @($baseUrl, $openaiUrl)
    foreach ($endpoint in $endpoints) {
        $hostname = ([System.Uri]$endpoint).Host
        try {
            $dnsResult = Resolve-DnsName -Name $hostname -ErrorAction Stop
            Write-Host "✅ DNS Resolution for $hostname : SUCCESS" -ForegroundColor Green
            Write-Host "   IP Address: $($dnsResult[0].IPAddress)" -ForegroundColor Gray
        } catch {
            Write-Host "❌ DNS Resolution for $hostname : FAILED" -ForegroundColor Red
            Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    
    # Test basic connectivity
    Write-Host "`n🔌 Testing Basic Connectivity:" -ForegroundColor Blue
    
    foreach ($endpoint in $endpoints) {
        $hostname = ([System.Uri]$endpoint).Host
        try {
            $tcpTest = Test-NetConnection -ComputerName $hostname -Port 443 -InformationLevel Quiet
            if ($tcpTest) {
                Write-Host "✅ TCP Connection to $hostname :443 : SUCCESS" -ForegroundColor Green
            } else {
                Write-Host "❌ TCP Connection to $hostname :443 : FAILED" -ForegroundColor Red
            }
        } catch {
            Write-Host "❌ TCP Connection to $hostname :443 : FAILED" -ForegroundColor Red
            Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

function Show-SystemInfo {
    Write-Host "`n💻 System Information:" -ForegroundColor Cyan
    Write-Host "=" * 40 -ForegroundColor Yellow
    
    Write-Host "Machine Name: $env:COMPUTERNAME" -ForegroundColor Gray
    Write-Host "User: $env:USERNAME" -ForegroundColor Gray
    Write-Host "PowerShell Version: $($PSVersionTable.PSVersion)" -ForegroundColor Gray
    Write-Host "OS Version: $(Get-CimInstance Win32_OperatingSystem | Select-Object -ExpandProperty Caption)" -ForegroundColor Gray
    
    # Try to get IP configuration
    try {
        $ipConfig = Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.PrefixOrigin -eq 'Dhcp' -or $_.PrefixOrigin -eq 'Manual' } | Select-Object -First 1
        Write-Host "Local IP: $($ipConfig.IPAddress)" -ForegroundColor Gray
    } catch {
        Write-Host "Local IP: Unable to determine" -ForegroundColor Gray
    }
}

# Main execution
function Main {
    Write-Host "🌟 Azure AI Foundry Complete API Testing Suite - PowerShell Version" -ForegroundColor Magenta
    Write-Host "=" * 80 -ForegroundColor Yellow
    Write-Host "🎯 Base URL: $baseUrl" -ForegroundColor Gray
    Write-Host "🤖 OpenAI URL: $openaiUrl" -ForegroundColor Gray
    Write-Host "🔑 API Key: ...$($apiKey.Substring($apiKey.Length - 4))" -ForegroundColor Gray
    Write-Host "=" * 80 -ForegroundColor Yellow
    
    Show-SystemInfo
    Test-NetworkConnectivity
    
    # Run all API tests
    Test-AIFoundryAPI
    Test-OpenAIEndpoints
    Test-ContentSafety
    Find-DeploymentNames
    Test-WithDeploymentID
    
    Write-Host "`n$('=' * 80)" -ForegroundColor Yellow
    Write-Host "🎉 Testing Suite Completed!" -ForegroundColor Green
    Write-Host "💡 Check the results above to identify working endpoints" -ForegroundColor Cyan
    Write-Host "🔍 Compare with results from public internet to verify private endpoint access" -ForegroundColor Cyan
    Write-Host "=" * 80 -ForegroundColor Yellow
}

# Execute the main function
Main