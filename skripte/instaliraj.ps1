# Instalacija PGH skillova i agenata na korisničkoj razini (Windows, PowerShell)
# Pokretanje iz korijena repozitorija:  powershell -ExecutionPolicy Bypass -File skripte\instaliraj.ps1
# Dodajte -Opcionalno za project-graph i graphify.
param([switch]$Opcionalno)
$ErrorActionPreference = "Stop"
$repo   = Split-Path -Parent $PSScriptRoot
$cilj   = Join-Path $env:USERPROFILE ".claude"
$agents = Join-Path $cilj "agents"
$skills = Join-Path $cilj "skills"
New-Item -ItemType Directory -Force -Path $agents, $skills | Out-Null

Get-ChildItem (Join-Path $repo ".claude\agents") -Filter *.md | ForEach-Object {
    Copy-Item $_.FullName -Destination $agents -Force
    Write-Host "agent  -> $($_.Name)"
}
$izvori = @(Join-Path $repo ".claude\skills")
if ($Opcionalno) { $izvori += (Join-Path $repo "skills-opcionalno") }
foreach ($izvor in $izvori) {
    Get-ChildItem $izvor -Directory | ForEach-Object {
        $dest = Join-Path $skills $_.Name
        if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
        Copy-Item $_.FullName -Destination $dest -Recurse
        Write-Host "skill  -> $($_.Name)"
    }
}
Write-Host "`nGotovo. Instalirano u $cilj. Ponovno pokrenite Claude Code."
