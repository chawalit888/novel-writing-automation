#!/usr/bin/env python3
"""
Sync Platform URLs from Google Sheets
อ่าน URL จาก Google Sheets แล้วอัปเดตลงใน novel-platform-urls.json
"""

import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    # Import Google Sheets MCP tools
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    HAS_GOOGLE_API = True
except ImportError:
    HAS_GOOGLE_API = False
    print("⚠️  Google API libraries not installed")
    print("   Install with: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
JSON_FILE = PROJECT_ROOT / "novel-platform-urls.json"
SPREADSHEET_ID = "1VU92nVfCaNH0AUjH9oy-SoIawiu4lePXUOC6RPRLaog"
SHEET_NAME = "Platform URLs"

def get_sheets_service():
    """Get Google Sheets service using MCP credentials"""
    # Note: This assumes MCP credentials are properly configured
    # You may need to adjust this based on your MCP setup
    try:
        # Try to use MCP's authentication
        import subprocess
        result = subprocess.run(
            ['mcp', 'tool', 'call', 'google-sheets', 'get_sheet_data',
             '--spreadsheet_id', SPREADSHEET_ID,
             '--sheet', SHEET_NAME],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data
    except:
        pass

    return None

def main():
    """Main function"""
    print("🚀 Sync Platform URLs from Google Sheets\n")
    print(f"📊 Spreadsheet: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")
    print(f"📄 Sheet: {SHEET_NAME}\n")

    # Note: Since we can't directly access Google Sheets API from Python easily,
    # we'll provide alternative instructions
    print("⚠️  Direct API access requires additional setup")
    print("\n💡 วิธีใช้ทางเลือก:")
    print("   1. เปิด Google Sheet: https://docs.google.com/spreadsheets/d/{}/edit")
    print("   2. กรอก URL ในคอลัมน์ที่ต้องการ")
    print("   3. File → Download → CSV (.csv)")
    print("   4. บันทึกเป็น 'novel-platform-urls.csv' ที่ root ของโปรเจกต์")
    print("   5. รัน: python scripts/import-platform-urls-from-csv.py")
    print("\nหรือใช้ Claude Code MCP tools เพื่ออ่านข้อมูลโดยตรง\n")

if __name__ == "__main__":
    main()
