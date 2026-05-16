# NSE Option Chain Automation Application

A robust Python automation application that downloads CSV files from NSE India's option-chain page and integrates the data into your prediction workbook.

## Features

? **Automated Download**: Clicks image-based download links on the NSE website
? **Smart File Detection**: Waits for complete file download with size stabilization
? **Data Integration**: Copies downloaded sheet content to prediction.xlsx RAW sheet
? **Continuous Operation**: Runs on schedule (default: every 2 minutes)
? **Error Handling**: Comprehensive logging and error recovery
? **Cleanup**: Automatically deletes downloaded files after processing
? **Flexible Configuration**: Command-line arguments for custom paths and intervals

## Requirements

- Python 3.8+
- Chrome/Chromium browser installed
- Internet connection
- Files in `C:\Users\Prakhar\Desktop\AICode\`:
  - `abcd.png` (download link image reference)
  - `prediction.xlsx` (destination workbook)

## Installation

1. **Clone/Copy the project**:
```bash
cd C:\Users\Prakhar\Desktop\AICode
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Usage

### Run Once
Execute a single automation cycle:
```bash
python nse_automation_app.py --run-once
```

### Run Continuously (Every 2 Minutes)
```bash
python nse_automation_app.py
```

Or specify a custom interval (in seconds):
```bash
python nse_automation_app.py --interval 300
```

### Run with Custom Directories
```bash
python nse_automation_app.py --download-dir "D:\Downloads" --prediction "D:\files\prediction.xlsx"
```

### Run in Non-Headless Mode (For Debugging)
```bash
python nse_automation_app.py --no-headless
```

## Command-Line Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--download-dir` | `C:\Users\Prakhar\Desktop\AICode\downloads` | Directory to save downloads |
| `--image` | `abcd.png` | Image filename to find and click |
| `--prediction` | `C:\Users\Prakhar\Desktop\AICode\prediction.xlsx` | Path to prediction workbook |
| `--base-dir` | `C:\Users\Prakhar\Desktop\AICode` | Base directory for image/prediction files |
| `--interval` | `120` | Interval between continuous runs (seconds) |
| `--run-once` | - | Run once instead of continuous |
| `--no-headless` | - | Run browser in visible mode |

## How It Works

```
1. Open NSE Option-Chain URL in Chrome
   ?
2. Dismiss any overlay dialogs
   ?
3. Find and click download link (based on abcd.png image)
   ?
4. Wait for file to download and stabilize
   ?
5. Read downloaded file (Excel/CSV)
   ?
6. Write content to prediction.xlsx RAW sheet
   ?
7. Delete original downloaded file
   ?
8. Wait for next interval or exit
```

## Logging

Logs are written to two places:

1. **Console Output**: Real-time status updates
2. **Log File**: `nse_automation.log` - Detailed log of all operations

Sample log output:
```
2024-01-15 10:30:45,123 - INFO - Started automation cycle
2024-01-15 10:30:48,456 - INFO - Opening NSE URL: https://www.nseindia.com/option-chain
2024-01-15 10:30:52,789 - INFO - Searching for download link using image: abcd.png
2024-01-15 10:30:55,012 - INFO - Successfully clicked element
2024-01-15 10:30:58,345 - INFO - New file detected: option-chain-data.xlsx
2024-01-15 10:31:02,678 - INFO - File download complete: 125432 bytes
2024-01-15 10:31:03,901 - INFO - Successfully pasted data to RAW sheet
2024-01-15 10:31:04,234 - INFO - Successfully deleted file
```

## File Structure

```
C:\Users\Prakhar\Desktop\AICode\
??? nse_automation_app.py          # Main application
??? requirements.txt                # Python dependencies
??? README.md                       # This file
??? nse_automation.log             # Log file (created on first run)
??? abcd.png                       # Download link image reference
??? prediction.xlsx                # Destination workbook
??? downloads/                     # Temporary download directory
    ??? (downloaded files - auto-deleted)
```

## Troubleshooting

### "Could not find or click download link"
- **Cause**: Image element not found on page or XPath strategies failed
- **Solution**: 
  - Run with `--no-headless` to see what's happening
  - Verify `abcd.png` exists and is in the correct directory
  - Check if NSE page structure has changed

### "No file downloaded within timeout"
- **Cause**: Download didn't start or took too long
- **Solution**:
  - Check internet connection
  - Run with `--no-headless` to verify click worked
  - Try again - NSE might be slow

### "Could not read downloaded file"
- **Cause**: File format not supported
- **Solution**:
  - Application supports .xlsx, .xls, and .csv
  - Verify file downloaded correctly

### "Could not paste to prediction file"
- **Cause**: `prediction.xlsx` is locked or corrupted
- **Solution**:
  - Close `prediction.xlsx` in Excel
  - Verify file is not read-only
  - Create fresh `prediction.xlsx` if corrupted

### "Chrome WebDriver not found"
- **Cause**: Chrome not installed or webdriver-manager failed
- **Solution**:
  - Install Chrome: https://www.google.com/chrome/
  - Reinstall webdriver-manager: `pip install --upgrade webdriver-manager`

## Running as Windows Service

To run as a background service, create a batch file:

**run_automation.bat**:
```batch
@echo off
cd C:\Users\Prakhar\Desktop\AICode
python nse_automation_app.py
```

Then use a tool like NSSM (Non-Sucking Service Manager) to create a Windows service.

## Performance Notes

- **Page Load**: ~5 seconds
- **Download**: ~5-15 seconds (depends on file size)
- **Data Paste**: ~2-5 seconds
- **Total per cycle**: ~15-30 seconds

At 2-minute intervals, the application runs ~720 times per day with minimal resource usage.

## Security Notes

- Application uses headless mode by default (no visual window)
- Logs stored locally - ensure log file security
- No credentials stored (uses browser automation only)
- Downloaded files are automatically deleted

## Development

### Extending the Application

To add custom logic:

```python
from nse_automation_app import NSEAutomationApp

app = NSEAutomationApp()
success = app.run_once()
```

### Testing

Run a single cycle:
```bash
python nse_automation_app.py --run-once --no-headless
```

Monitor logs in real-time:
```bash
tail -f nse_automation.log
```

## Support & Issues

If you encounter issues:

1. Check `nse_automation.log` for detailed error messages
2. Run with `--no-headless` to see browser behavior
3. Verify files exist in the correct locations
4. Check internet connection
5. Try running manually once with `--run-once`

## License

This automation application is provided as-is for personal use.

## Changelog

### Version 1.0 (2024-01-15)
- Initial release
- Core automation features
- Continuous scheduling
- Comprehensive logging
- Error handling and recovery
