<#
Launcher copied from repo `n8n/run-client.ps1` to product bundle.
#>
param(
  [string]$Client = 'example'
)

$envRoot = Resolve-Path (Join-Path $PSScriptRoot "..\clients")

# Ensure we use the resolved path string
$envRootPath = $envRoot.ProviderPath

$envFile = Join-Path $envRootPath "$Client\.env"
$envExample = Join-Path $envRootPath "$Client\.env.example"

if (-not (Test-Path $envFile)) {
  Write-Error "ERROR: Env file not found for client '$Client': $envFile`nCreate it by copying $envExample -> $envFile and filling values."
  exit 1
}

# Debug: show the final resolved env path
Write-Host "Resolved env file path: $envFile"

Get-Content $envFile | ForEach-Object {
  $line = $_.Trim()
  if ($line.StartsWith('#') -or [string]::IsNullOrWhiteSpace($line)) { return }
  $parts = $line -split '=', 2
  if ($parts.Count -eq 2) {
    $name = $parts[0].Trim()
    $value = $parts[1].Trim()
    Set-Item -Path Env:\$name -Value $value
  }
}

# Small helper to mask secret values for debug output
function Protect-Secret([string]$s) {
  if ([string]::IsNullOrEmpty($s)) { return "" }
  if ($s.Length -le 8) { return "****" }
  return $s.Substring(0,4) + "..." + $s.Substring($s.Length - 4)
}

# Debug: print a few key env values (mask secrets)
$clientName = (Get-Item -Path Env:CLIENT_NAME -ErrorAction SilentlyContinue).Value
$sheetId = (Get-Item -Path Env:SHEET_ID -ErrorAction SilentlyContinue).Value
$discord = (Get-Item -Path Env:DISCORD_WEBHOOK_URL -ErrorAction SilentlyContinue).Value
$llm = (Get-Item -Path Env:LLM_API_KEY -ErrorAction SilentlyContinue).Value

Write-Host "Client: $clientName"
Write-Host "SHEET_ID: $sheetId"
Write-Host "DISCORD_WEBHOOK_URL: " (Protect-Secret $discord)
Write-Host "LLM_API_KEY: " (Protect-Secret $llm)

Write-Host "Starting n8n for client '$Client' using env file: $envFile"
& n8n
