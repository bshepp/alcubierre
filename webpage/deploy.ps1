# deploy.ps1 — sync ./webpage to S3 (and optionally invalidate CloudFront)
#
# Usage:
#   .\deploy.ps1 -Bucket your-bucket-name
#   .\deploy.ps1 -Bucket your-bucket-name -DryRun
#   .\deploy.ps1 -Bucket your-bucket-name -Profile myaws -DistributionId E1234567890 -Invalidate
#
# Requirements:
#   - AWS CLI v2 installed and on PATH
#   - AWS profile authenticated (see `aws configure --profile <name>`)
#   - Bucket already created and configured for static website hosting
#     (or fronted by CloudFront; see s3-policy.json for sample IAM policy)

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$Bucket,

    [string]$Profile = "default",

    [string]$Region = "us-east-1",

    [switch]$DryRun,

    [switch]$Invalidate,

    [string]$DistributionId
)

$ErrorActionPreference = "Stop"

# Verify AWS CLI exists.
$awsCmd = Get-Command aws -ErrorAction SilentlyContinue
if (-not $awsCmd) {
    Write-Error "aws CLI not found on PATH. Install AWS CLI v2 first."
    exit 1
}

# Resolve script root so we can run from anywhere.
$src = $PSScriptRoot
Write-Host "Source:    $src" -ForegroundColor Cyan
Write-Host "Bucket:    s3://$Bucket/" -ForegroundColor Cyan
Write-Host "Profile:   $Profile" -ForegroundColor Cyan
Write-Host "Region:    $Region" -ForegroundColor Cyan
if ($DryRun) { Write-Host "Mode:      DRY RUN (no changes pushed)" -ForegroundColor Yellow }
Write-Host ""

# Build sync arguments. We exclude internal files that should not be deployed.
$syncArgs = @(
    "s3", "sync",
    $src,
    "s3://$Bucket/",
    "--delete",
    "--profile", $Profile,
    "--region", $Region,
    "--exclude", "*.ps1",
    "--exclude", "_partials/*",
    "--exclude", "README.md",
    "--exclude", "s3-policy.json"
)
if ($DryRun) { $syncArgs += "--dryrun" }

Write-Host "Running:   aws $($syncArgs -join ' ')" -ForegroundColor DarkGray
Write-Host ""

& aws @syncArgs
if ($LASTEXITCODE -ne 0) {
    Write-Error "aws s3 sync failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Sync complete." -ForegroundColor Green

# Force charset=utf-8 on text assets (S3 sync's default Content-Type omits charset,
# which lets some browsers fall back to Windows-1252 and corrupt Greek/math glyphs).
if (-not $DryRun) {
    $textTypes = @(
        @{ Pattern = "*.html"; Type = "text/html; charset=utf-8" },
        @{ Pattern = "*.css";  Type = "text/css; charset=utf-8" },
        @{ Pattern = "*.js";   Type = "application/javascript; charset=utf-8" }
    )
    foreach ($t in $textTypes) {
        Write-Host ("Setting Content-Type for " + $t.Pattern + " ...") -ForegroundColor DarkGray
        & aws s3 cp "s3://$Bucket/" "s3://$Bucket/" `
            --recursive `
            --exclude "*" `
            --include $t.Pattern `
            --metadata-directive REPLACE `
            --content-type $t.Type `
            --profile $Profile `
            --region $Region | Out-Null
        if ($LASTEXITCODE -ne 0) {
            Write-Error ("aws s3 cp metadata pass failed for " + $t.Pattern)
            exit $LASTEXITCODE
        }
    }
    Write-Host "Content-Type charset pass complete." -ForegroundColor Green
}

# Optional CloudFront invalidation.
if ($Invalidate) {
    if (-not $DistributionId) {
        Write-Error "-Invalidate requires -DistributionId"
        exit 1
    }
    Write-Host ""
    Write-Host "Invalidating CloudFront distribution $DistributionId ..." -ForegroundColor Cyan
    & aws cloudfront create-invalidation `
        --distribution-id $DistributionId `
        --paths "/*" `
        --profile $Profile
    if ($LASTEXITCODE -ne 0) {
        Write-Error "CloudFront invalidation failed with exit code $LASTEXITCODE"
        exit $LASTEXITCODE
    }
    Write-Host "Invalidation submitted." -ForegroundColor Green
}
