# NSE Automation Application - Complete Setup Guide

## Overview

This guide walks you through setting up and running the NSE Option Chain Automation Application on your Windows computer.

## Prerequisites

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - ? Check "Add Python to PATH" during installation

2. **Google Chrome**
   - Download from: https://www.google.com/chrome/
   - Application uses Chrome for automation

3. **Required Files** (in `C:\Users\Prakhar\Desktop\AICode\`)
   - `abcd.png` - Image of download link
   - `prediction.xlsx` - Excel file where data will be pasted

## Installation Steps

### Step 1: Verify Python Installation (30 seconds)

Open Command Prompt and run:
```bash
python --version
```

Expected output: `Python 3.x.x`

If not found, reinstall Python with "Add Python to PATH" checked.

### Step 2: Install Dependencies (2 minutes)

Navigate to the application directory:
```bash
cd C:\Users\Prakhar\Desktop\AICode
```

Install all required packages:
```bash
pip install -r requirements.txt
```

Verify installation:
```bash
python -c "import selenium, pandas, openpyxl; print('All dependencies OK')"
```

### Step 3: Verify Configuration

Check that these files exist:
```bash
dir C:\Users\Prakhar\Desktop\AICode\
```

Should show:
- ? nse_automation_app.py
- ? requirements.txt
- ? README.md
- ? abcd.png
- ? prediction.xlsx

### Step 4: Test Run (2 minutes)

Run a single test cycle:
```bash
python nse_automation_app.py --run-once
```

This will:
1. Open NSE website
2. Find and click the download link
3. Wait for download
4. Paste to prediction.xlsx
5. Clean up
6. Exit

**Expected output**:
```
Starting automation cycle at 2024-01-15 10:30:45
Opening NSE URL: https://www.nseindia.com/option-chain
Searching for download link using image: abcd.png
Successfully clicked element
Waiting for file download...
File download complete: option_chain.xlsx (125432 bytes)
Pasting data to prediction file...
Successfully pasted data to RAW sheet
Automation cycle completed successfully
```

### Step 5: Configure for Your Needs

#### Option A: Run Every 2 Minutes (Default)
```bash
python nse_automation_app.py
```

#### Option B: Run Every X Minutes
```bash
python nse_automation_app.py --interval 300
```
(300 seconds = 5 minutes)

#### Option C: Use Custom Directories
```bash
python nse_automation_app.py --download-dir D:\Downloads --prediction D:\Files\pred.xlsx
```

## Running the Application

### Method 1: Command Prompt (Simple)

```bash
cd C:\Users\Prakhar\Desktop\AICode
python nse_automation_app.py
```

Click Ctrl+C to stop.

### Method 2: Batch File (Easier)

Double-click: `run_automation.bat`

Interactive menu will appear with options.

### Method 3: PowerShell

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
C:\Users\Prakhar\Desktop\AICode\run_automation.ps1
```

### Method 4: Windows Task Scheduler (Background Service)

Create a scheduled task:

1. Open Task Scheduler (search "Task Scheduler")
2. Click "Create Basic Task"
3. Name: "NSE Automation"
4. Trigger: Daily or on startup
5. Action:
   - Program: `python.exe`
   - Arguments: `nse_automation_app.py`
   - Start in: `C:\Users\Prakhar\Desktop\AICode`

## Monitoring & Logs

### View Logs

The application creates `nse_automation.log` in the application directory:

```bash
type nse_automation.log
```

Or in PowerShell:
```powershell
Get-Content nse_automation.log -Tail 50
```

### Real-Time Monitoring

In PowerShell (Linux-style `tail -f` equivalent):
```powershell
Get-Content nse_automation.log -Wait
```

### Log Example

```
2024-01-15 10:30:45,123 - INFO - ================================================================================
2024-01-15 10:30:45,234 - INFO - Starting automation cycle at 2024-01-15 10:30:45
2024-01-15 10:30:45,345 - INFO - ================================================================================
2024-01-15 10:30:45,456 - INFO - Initialized NSEAutomationApp
2024-01-15 10:30:45,567 - INFO -   Download dir: C:\Users\Prakhar\Desktop\AICode\downloads
2024-01-15 10:30:45,678 - INFO -   Image file: C:\Users\Prakhar\Desktop\AICode\abcd.png
2024-01-15 10:30:45,789 - INFO -   Prediction file: C:\Users\Prakhar\Desktop\AICode\prediction.xlsx
2024-01-15 10:30:45,890 - INFO - Chrome WebDriver created successfully
2024-01-15 10:30:46,001 - INFO - Opening NSE URL: https://www.nseindia.com/option-chain
2024-01-15 10:30:50,234 - INFO - Searching for download link using image: abcd.png
2024-01-15 10:30:52,567 - INFO - Successfully clicked element
2024-01-15 10:30:53,890 - INFO - Waiting for file download (timeout: 180s)...
2024-01-15 10:30:57,123 - INFO - New file detected: option_chain.xlsx
2024-01-15 10:31:01,456 - INFO - File download complete: option_chain.xlsx (125432 bytes)
2024-01-15 10:31:02,789 - INFO - Reading downloaded file: C:\Users\Prakhar\Desktop\AICode\downloads\option_chain.xlsx
2024-01-15 10:31:03,012 - INFO - Successfully read file as Excel
2024-01-15 10:31:03,234 - INFO - Data shape: (100, 15)
2024-01-15 10:31:03,456 - INFO - Pasting data to prediction file: C:\Users\Prakhar\Desktop\AICode\prediction.xlsx
2024-01-15 10:31:03,789 - INFO - Successfully pasted data to RAW sheet
2024-01-15 10:31:04,012 - INFO - Data pasted: 100 rows, 15 columns
2024-01-15 10:31:04,234 - INFO - Cleaning up downloaded file: C:\Users\Prakhar\Desktop\AICode\downloads\option_chain.xlsx
2024-01-15 10:31:04,456 - INFO - Successfully deleted file
2024-01-15 10:31:04,678 - INFO - ================================================================================
2024-01-15 10:31:04,789 - INFO - Automation cycle completed successfully
2024-01-15 10:31:04,890 - INFO - ================================================================================
```

## Troubleshooting

### Issue: "Python is not installed"

**Solution**:
1. Download Python from https://www.python.org/
2. Run installer
3. ? CHECK "Add Python to PATH"
4. Restart Command Prompt

### Issue: "Could not find or click download link"

**Solution**:
1. Run with debugging:
   ```bash
   python nse_automation_app.py --run-once --no-headless
   ```
2. Watch the browser window
3. Verify `abcd.png` exists and is correct
4. Check if NSE website structure changed

### Issue: "No file downloaded within timeout"

**Solution**:
1. Check internet connection
2. Try running manually with `--no-headless`
3. Check if download was blocked by Chrome settings

### Issue: "Could not read downloaded file"

**Solution**:
1. Check if file is corrupted
2. Verify file format (should be .xlsx or .csv)
3. Check file permissions

### Issue: "Permission denied" when running batch file

**Solution**:
1. Right-click Command Prompt
2. Select "Run as administrator"
3. Navigate to folder and run command again

## Performance

Typical cycle timing:
- Page load: 5 seconds
- Find & click: 2 seconds
- Download: 10 seconds
- Data paste: 3 seconds
- **Total: ~20 seconds per cycle**

With 2-minute intervals, application uses minimal resources.

## System Resources

On a typical machine:
- **Memory**: ~150-200 MB per cycle
- **CPU**: <5% during execution, 0% while waiting
- **Disk**: <1 MB for logs, downloads auto-deleted

## Advanced Configuration

### Change Default Interval

Edit line in `nse_automation_app.py`:
```python
DEFAULT_DOWNLOADS_DIR = Path(DEFAULT_BASE_DIR) / "downloads"
```

Or use command-line:
```bash
python nse_automation_app.py --interval 300
```

### Run on System Startup

Create a .bat file and add to Windows Startup folder:
```
C:\Users\Prakhar\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\
```

### Email Notifications

Modify the application to send email on failure (extend the code as needed).

## Uninstallation

To remove the application:

1. Stop the running process (Ctrl+C if in terminal)
2. Delete the directory: `C:\Users\Prakhar\Desktop\AICode\`
3. Uninstall Python if no longer needed

Remove installed packages (optional):
```bash
pip uninstall -r requirements.txt -y
```

## Support

For issues:

1. Check `nse_automation.log` for error details
2. Run `--run-once --no-headless` for debugging
3. Verify all files exist in correct locations
4. Check internet connection
5. Restart the application

## Success Indicators

? Application is running correctly if:
- Automation cycle completes in ~20 seconds
- New data appears in `prediction.xlsx` RAW sheet
- Downloaded files are automatically deleted
- Logs show "Automation cycle completed successfully"
- Process repeats every 2 minutes (or custom interval)

Congratulations! Your NSE Automation is now running. ??
