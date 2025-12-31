$nodeVersion = "v20.11.0"
$nodeDist = "node-$nodeVersion-win-x64"
$toolsDir = "C:\Users\chi.zhang\Documents\trae_projects\trae\tools"
$nodeDir = "$toolsDir\$nodeDist"
$env:PATH = "$nodeDir;$env:PATH"

# Clear proxy settings that might cause network errors
$env:HTTP_PROXY = ""
$env:HTTPS_PROXY = ""
$env:http_proxy = ""
$env:https_proxy = ""
npm config delete proxy
npm config delete https-proxy

Write-Host "Starting Jarvis Holographic Main..."
node -v

Set-Location "C:\Users\chi.zhang\Documents\trae_projects\trae\jarvis-holographic-main"

if (!(Test-Path "node_modules")) {
    Write-Host "Installing dependencies..."
    npm install
}

# Run with host flag to expose to network if needed, though localhost is fine
npm run dev
