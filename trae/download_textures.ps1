
$baseUrl = "https://raw.githubusercontent.com/mrdoob/three.js/master/examples/textures/planets"
$files = @(
    "earth_atmos_2048.jpg",
    "earth_normal_2048.jpg",
    "earth_specular_2048.jpg"
)

$targetDir = "c:\Users\chi.zhang\Documents\trae_projects\trae\jarvis-holographic-main\public\textures"

# Create directory if it doesn't exist
if (!(Test-Path -Path $targetDir)) {
    New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
    Write-Host "Created directory: $targetDir"
}

foreach ($file in $files) {
    $url = "$baseUrl/$file"
    $outputPath = Join-Path -Path $targetDir -ChildPath $file
    
    Write-Host "Downloading $file..."
    try {
        Invoke-WebRequest -Uri $url -OutFile $outputPath
        Write-Host "Successfully downloaded $file"
    } catch {
        Write-Error "Failed to download $file : $_"
    }
}

Write-Host "Texture download process completed."
