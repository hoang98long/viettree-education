param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[a-z0-9][a-z0-9._-]{0,63}$')]
    [string]$Release
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$artifactDirectory = Join-Path (Join-Path $repoRoot '.artifacts') $Release
$archiveName = "viettree-$Release-linux-amd64.tar"
$archivePath = Join-Path $artifactDirectory $archiveName
if (Test-Path -LiteralPath $artifactDirectory) {
    throw 'This release artifact directory already exists. Choose a new release tag.'
}
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw 'Install Docker Desktop and enable Linux containers on the build machine.'
}
if (-not (Get-Command tar -ErrorAction SilentlyContinue)) {
    throw 'The build machine needs tar to package deployment configuration.'
}
$dockerOs = & docker info --format '{{.OSType}}'
if ($LASTEXITCODE -ne 0 -or $dockerOs -ne 'linux') {
    throw 'Docker Engine must be running in Linux containers mode. Build on a separate machine, not the small VPS.'
}

$backendImage = "viettree-backend:$Release"
$frontendImage = "viettree-frontend:$Release"
function Invoke-DockerStep {
    param([string[]]$Arguments)
    $previousPreference = $ErrorActionPreference
    try {
        # Docker build progress uses stderr. PowerShell 5 must not interpret
        # successful progress messages as terminating application errors.
        $ErrorActionPreference = 'Continue'
        & docker @Arguments 2>&1 | ForEach-Object { Write-Host $_ }
        $commandExit = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $previousPreference
    }
    if ($commandExit -ne 0) { throw "Docker step failed with exit code $commandExit." }
}
Push-Location $repoRoot
try {
    # Sequential builds keep peak memory lower on the build machine too.
    Invoke-DockerStep -Arguments @('build', '--platform', 'linux/amd64', '--file', 'deploy/backend.production.Dockerfile', '--tag', $backendImage, '.')
    Invoke-DockerStep -Arguments @('build', '--platform', 'linux/amd64', '--file', 'deploy/frontend.production.Dockerfile', '--build-arg', 'INTERNAL_API_URL=http://backend:8000', '--tag', $frontendImage, '.')

    foreach ($image in @($backendImage, $frontendImage)) {
        $imagePlatform = & docker image inspect --format '{{.Os}}/{{.Architecture}}' $image
        if ($LASTEXITCODE -ne 0 -or $imagePlatform -ne 'linux/amd64') {
            throw 'An image does not match the VPS Linux amd64 platform.'
        }
    }
    New-Item -ItemType Directory -Path $artifactDirectory | Out-Null
    Invoke-DockerStep -Arguments @('image', 'save', '--output', $archivePath, $backendImage, $frontendImage)
    $hash = (Get-FileHash -LiteralPath $archivePath -Algorithm SHA256).Hash.ToLowerInvariant()
    [IO.File]::WriteAllText("$archivePath.sha256", "$hash  $archiveName`n", [Text.Encoding]::ASCII)
    $configArchiveName = "viettree-$Release-deployment.tar.gz"
    $configArchivePath = Join-Path $artifactDirectory $configArchiveName
    & tar -czf $configArchivePath -C $repoRoot -- docker-compose.production.yml docker-compose.small-vps.yml docker-compose.vps8gb.yml .env.production.example .env.production.small.example .env.production.vps8gb.example deploy database/viettree_education_schema.sql database/seeds/verify.sql
    if ($LASTEXITCODE -ne 0) { throw 'Deployment configuration archive failed.' }
    $configHash = (Get-FileHash -LiteralPath $configArchivePath -Algorithm SHA256).Hash.ToLowerInvariant()
    [IO.File]::WriteAllText("$configArchivePath.sha256", "$configHash  $configArchiveName`n", [Text.Encoding]::ASCII)
    $metadata = @{
        release = $Release
        platform = 'linux/amd64'
        images = @($backendImage, $frontendImage)
        archive = $archiveName
        sha256 = $hash
        deployment_archive = $configArchiveName
        deployment_sha256 = $configHash
    } | ConvertTo-Json
    [IO.File]::WriteAllText((Join-Path $artifactDirectory 'release.json'), $metadata, [Text.UTF8Encoding]::new($false))
    Write-Host "Image archive: $archivePath"
    Write-Host "Deployment files: $configArchivePath"
    Write-Host 'Upload both archives and their .sha256 files; keep .env.production only on the VPS.'
} finally {
    Pop-Location
}
