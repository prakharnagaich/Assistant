# Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies (1 minute)
```bash
pip install -r requirements.txt
```

### Step 2: Verify Files (30 seconds)
Ensure these files exist in `C:\Users\Prakhar\Desktop\AICode\`:
- ? `abcd.png` - The download link image
- ? `prediction.xlsx` - Your destination workbook

### Step 3: Test Run (2 minutes)
```bash
python nse_automation_app.py --run-once
```

Expected output:
```
Starting automation cycle at 2024-01-15 10:30:45
Opening NSE URL: https://www.nseindia.com/option-chain
Searching for download link...
Successfully clicked element
Waiting for file download...
File download complete
Pasting data to prediction file...
Successfully pasted data to RAW sheet
```

### Step 4: Start Continuous Mode (Setup once, runs forever)
```bash
python nse_automation_app.py
```

This runs every 2 minutes continuously until you press Ctrl+C.

## Common Commands

| Command | What It Does |
|---------|------------|
| `python nse_automation_app.py --run-once` | Test mode - runs once and exits |
| `python nse_automation_app.py` | Continuous mode - runs every 2 minutes |
| `python nse_automation_app.py --interval 300` | Runs every 5 minutes instead of 2 |
| `python nse_automation_app.py --no-headless` | Shows browser window (for debugging) |

## Troubleshooting

### Problem: "Chrome WebDriver not found"
**Solution**: 
```bash
pip install --upgrade webdriver-manager
```

### Problem: "Could not find or click download link"
**Solution**: Run with debugging:
```bash
python nse_automation_app.py --run-once --no-headless
```
Watch the browser to see if it finds the download link.

### Problem: "File not found" (abcd.png or prediction.xlsx)
**Solution**: Verify files exist:
```bash
dir C:\Users\Prakhar\Desktop\AICode\
```
Should show: `abcd.png`, `prediction.xlsx`, `nse_automation_app.py`, etc.

### Problem: Permission denied
**Solution**: Run Command Prompt as Administrator

## Next Steps

1. ? Run `python nse_automation_app.py --run-once` to test
2. ? Check `nse_automation.log` for details
3. ? If test successful, run `python nse_automation_app.py` for continuous mode
4. ? Leave running to automate downloads every 2 minutes

## Need Help?

Check the logs:
```bash
type nse_automation.log
```

This shows exactly what happened during each run.
