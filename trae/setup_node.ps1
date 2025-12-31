$ErrorActionPreference = "Stop"
$nodeVersion = "v20.11.0"
$nodeDist = "node-$nodeVersion-win-x64"
$baseDir = "C:\Users\chi.zhang\Documents\trae_projects\trae"
$toolsDir = "$baseDir\tools"
$nodeDir = "$toolsDir\$nodeDist"
$zipPath = "$toolsDir\node.zip"
$url = "https://nodejs.org/dist/$nodeVersion/$nodeDist.zip"

Write-Output "=== Setting up Portable Node.js Environment ==="

if (!(Test-Path $toolsDir)) {
    Write-Output "Creating tools directory..."
    New-Item -ItemType Directory -Path $toolsDir -Force | Out-Null
}

if (!(Test-Path $nodeDir)) {
    Write-Output "Downloading Node.js from $url..."
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $url -OutFile $zipPath
    
    Write-Output "Extracting Node.js..."
    Expand-Archive -Path $zipPath -DestinationPath $toolsDir -Force
    Remove-Item $zipPath
} else {
    Write-Output "Node.js already installed in $nodeDir"
}

# Add to PATH for this script execution
$env:PATH = "$nodeDir;$env:PATH"

Write-Output "Verifying Node.js version..."
node -v
npm -v

Write-Output "=== Installing Dependencies for Jarvis Holographic Main ==="
Set-Location "$baseDir\jarvis-holographic-main"

if (!(Test-Path "node_modules")) {
    Write-Output "Running npm install (this may take a minute)..."
    npm install
} else {
    Write-Output "node_modules already exists. Skipping install to save time."
    # Optional: npm ci or just assume it's good. 
    # If user wants full re-config, maybe we should run it, but let's check if it works first.
    # We'll run it just to be safe in case it was partial.
    npm install
}

Write-Output "Setup Complete!"
