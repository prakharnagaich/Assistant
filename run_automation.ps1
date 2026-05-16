# PowerShell script to run NSE Automation as a background service

param(
    [string]$Mode = "continuous",
    [int]$Interval = 120
)

# Set working directory
Set-Location "C:\Users\Prakhar\Desktop\AICode"

# Ensure Python is available
try {
    $python = (Get-Command python -ErrorAction Stop).Source
    Write-Host "Python found: $python"
} catch {
    Write-Error "Python not found. Please install Python 3.8+"
    exit 1
}

# Check dependencies
Write-Host "Checking dependencies..."
$deps = @("selenium", "pandas", "openpyxl")
foreach ($dep in $deps) {
    try {
        python -c "import $dep" -ErrorAction Stop | Out-Null
        Write-Host "? $dep installed"
    } catch {
        Write-Warning "$dep not installed, installing..."
        pip install -r requirements.txt
        break
    }
}

# Run application
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "NSE Automation Application" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

if ($Mode -eq "once") {
    Write-Host "Running in test mode (once only)..."
    python nse_automation_app.py --run-once
} elseif ($Mode -eq "continuous") {
    Write-Host "Running in continuous mode (every $Interval seconds)..."
    Write-Host "Press Ctrl+C to stop"
    Write-Host ""
    python nse_automation_app.py --interval $Interval
} else {
    Write-Host "Invalid mode: $Mode"
    Write-Host "Use 'once' or 'continuous'"
    exit 1
}
