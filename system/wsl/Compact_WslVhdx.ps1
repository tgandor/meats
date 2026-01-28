<#
  Optimize-WslVhdx.ps1
  - Enumerates WSL distros, finds ext4.vhdx, skips Running distros, and compacts stopped ones.
  - Uses Optimize-VHD when available (Hyper-V module); falls back to diskpart otherwise.
  - Optional: Also compact Docker Desktop’s WSL VHDX files with -IncludeDocker.
#>

[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [ValidateSet('Full','Quick','Retrim')]
    [string]$Mode = 'Full',

    [switch]$IncludeDocker,     # Also handle Docker Desktop VHDX files
    [switch]$DryRun            # Show what would be done, don’t actually compact
)

function Test-IsAdmin {
    $wi = [Security.Principal.WindowsIdentity]::GetCurrent()
    $wp = New-Object Security.Principal.WindowsPrincipal($wi)
    return $wp.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Get-WslDistroStates {
    # Returns a hashtable: Name -> State ('Running'|'Stopped'|'Installing'...)
    $map = @{}
    $lines = & wsl.exe -l -v 2>$null
    if (-not $lines) { return $map }

    # Skip header line: "  NAME                   STATE           VERSION"
    foreach ($line in $lines | Select-Object -Skip 1) {
        if (-not $line.Trim()) { continue }
        # Robust parse: Split from the right to get VERSION, then STATE; the rest is NAME
        $parts = $line -replace '\s+$','' -split '\s{2,}'  # columns separated by 2+ spaces
        if ($parts.Count -ge 3) {
            $name  = $parts[0].Trim()
            $state = $parts[1].Trim()
            $map[$name] = $state
        }
    }
    return $map
}

function Get-WslVhdxEntries {
    <#
      Enumerate distro BasePath from HKCU:\Software\Microsoft\Windows\CurrentVersion\Lxss
      and yield [pscustomobject]@{ Name; BasePath; VhdxPath } for distros that have a VHDX.
      (Per Microsoft Learn, path = BasePath + '\ext4.vhdx')  [2](https://learn.microsoft.com/en-us/windows/wsl/disk-space)
    #>
    $key = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Lxss'
    if (-not (Test-Path $key)) { return @() }

    $entries = @()
    foreach ($sub in Get-ChildItem -Path $key -ErrorAction SilentlyContinue) {
        $p = Get-ItemProperty $sub.PSPath -ErrorAction SilentlyContinue
        if (-not $p) { continue }
        $name = $p.DistributionName
        $base = $p.BasePath
        if (-not $name -or -not $base) { continue }

        # Normalize possible \\?\-prefixed paths
        $normBase = ($base -replace '^[\\]{2}\?\\','')
        $vhdx = Join-Path $normBase 'ext4.vhdx'
        if (Test-Path $vhdx) {
            $entries += [pscustomobject]@{
                Name     = $name
                BasePath = $normBase
                VhdxPath = $vhdx
            }
        }
    }
    return $entries
}

function Get-SizeString([long]$bytes) {
    switch ($bytes) {
        { $_ -ge 1TB } { '{0:N2} TB' -f ($bytes/1TB); break }
        { $_ -ge 1GB } { '{0:N2} GB' -f ($bytes/1GB); break }
        { $_ -ge 1MB } { '{0:N2} MB' -f ($bytes/1MB); break }
        default        { '{0:N0} bytes' -f $bytes }
    }
}

function Invoke-OptimizeVhdx {
    [CmdletBinding(SupportsShouldProcess)]
    param(
        [string]$Path,
        [string]$Mode
    )

    $before = (Get-Item $Path).Length
    Write-Host "  Size before: $(Get-SizeString $before)"

    $optCmd = Get-Command Optimize-VHD -ErrorAction SilentlyContinue
    if ($optCmd) {
        $msg = "Optimize-VHD -Path `"$Path`" -Mode $Mode"
        if ($PSCmdlet.ShouldProcess($Path, $msg)) {
            Optimize-VHD -Path $Path -Mode $Mode -ErrorAction Stop
        }
    } else {
        # Fallback to diskpart compact  (official method also documented widely)  [5](https://github.com/astral-sh/uv/issues/5589)
        $dp = @(
            "select vdisk file=`"$Path`"",
            "compact vdisk"
        )
        $script = New-TemporaryFile
        try {
            Set-Content -LiteralPath $script -Value ($dp -join [Environment]::NewLine) -Encoding ASCII
            $msg = "diskpart /s `"$($script.FullName)`""
            if ($PSCmdlet.ShouldProcess($Path, $msg)) {
                Start-Process -FilePath diskpart.exe -ArgumentList "/s `"$($script.FullName)`"" -Wait -NoNewWindow
            }
        } finally {
            Remove-Item -ErrorAction SilentlyContinue $script
        }
    }

    $after = (Get-Item $Path).Length
    $finish = Get-Date
    $elapsed = New-TimeSpan -Start $start -End $finish
    Write-Host "  Optimization finished at: $finish (elapsed: $([math]::Round($elapsed.TotalSeconds, 2)) seconds)"
    Write-Host "  Size after : $(Get-SizeString $after)"
    Write-Host "  Reclaimed  : $(Get-SizeString ($before - $after))"
}

# -------- Main --------

if (-not (Test-IsAdmin)) {
    Write-Warning "Run this script in an elevated PowerShell (Administrator) to compact VHDX files."
}

$states  = Get-WslDistroStates
$entries = Get-WslVhdxEntries
$start = Get-Date
Write-Host "WSL VHDX Optimization started at: $start"

if (-not $entries) {
    Write-Host "No WSL2 VHDX files found via registry BasePath. (Nothing to optimize.)" -ForegroundColor Yellow
    return
}

Write-Host "Found $($entries.Count) WSL distro(s) with VHDX:" -ForegroundColor Cyan
$entries | ForEach-Object {
    $st = $states[$_.Name]
    if (-not $st) { $st = 'Unknown' }
    Write-Host ("- {0}  [{1}]" -f $_.Name, $st)

    if ($st -eq 'Running') {
        Write-Host "  Skipping: distro is Running. Shut it down manually (wsl --terminate '$($_.Name)' or wsl --shutdown)." -ForegroundColor Yellow
        return
    }

    if ($DryRun) {
        Write-Host "  (DryRun) Would optimize: $($_.VhdxPath)"
        return
    }

    try {
        Invoke-OptimizeVhdx -Path $_.VhdxPath -Mode $Mode
    } catch {
        Write-Warning "  Failed to optimize '$($_.VhdxPath)': $($_.Exception.Message)"
    }
}

if ($IncludeDocker) {
    Write-Host "`n-- Docker Desktop WSL VHDX --" -ForegroundColor Cyan
    # Skip if docker WSL distros are running
    $dockerRunning = @('docker-desktop','docker-desktop-data') | Where-Object { $states[$_] -eq 'Running' }
    if ($dockerRunning) {
        Write-Host "Docker Desktop WSL distros are running ($($dockerRunning -join ', ')). Please quit Docker Desktop / stop those distros and re-run." -ForegroundColor Yellow
    } else {
        $dockerRoots = @(
            Join-Path $env:LOCALAPPDATA 'Docker\wsl\data',
            Join-Path $env:LOCALAPPDATA 'Docker\wsl\disk'
        )
        foreach ($root in $dockerRoots) {
            if (-not (Test-Path $root)) { continue }
            Get-ChildItem -Path $root -Filter '*.vhdx' -File -ErrorAction SilentlyContinue | ForEach-Object {
                $path = $_.FullName
                if ($DryRun) {
                    Write-Host "  (DryRun) Would optimize Docker VHDX: $path"
                } else {
                    try {
                        Invoke-OptimizeVhdx -Path $path -Mode $Mode
                    } catch {
                        Write-Warning "  Failed to optimize '$path': $($_.Exception.Message)"
                    }
                }
            }
        }
    }
}
