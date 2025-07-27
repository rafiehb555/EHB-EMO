#!/usr/bin/env python3
"""
EHB Auto Page Opener
Automatically opens all project pages in the browser
"""

import os
import sys
import time
import webbrowser
from typing import Dict, List


class AutoPageOpener:
    def __init__(self, base_url: str = "http://localhost:3002"):
        self.base_url = base_url
        self.pages = [
            {"name": "Home Page", "url": "/"},
            {"name": "Test Page", "url": "/test"},
            {"name": "Main Dashboard", "url": "/dashboard"},
            {"name": "Wallet Dashboard", "url": "/dashboard/wallet"},
            {"name": "Profile Dashboard", "url": "/dashboard/profile"},
            {"name": "Store Dashboard", "url": "/dashboard/store"},
            {"name": "Emo Dashboard", "url": "/dashboard/emo"},
            {"name": "Medical Records", "url": "/medical-records"},
            {"name": "Appointments", "url": "/appointments"},
            {"name": "Patients", "url": "/patients"},
            {"name": "Analytics", "url": "/analytics"},
            {"name": "Telemedicine", "url": "/telemedicine"},
            {"name": "AI Diagnosis", "url": "/ai-diagnosis"},
            {"name": "Healthcare Dashboard", "url": "/healthcare-dashboard"},
            {"name": "Admin Panel", "url": "/admin"},
            {"name": "Agent Dashboard", "url": "/agent-dashboard"}
        ]
        
    def check_server_running(self) -> bool:
        """Check if the server is running on port 3002"""
        import requests
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def open_page(self, page: Dict) -> None:
        """Open a single page in the browser"""
        full_url = f"{self.base_url}{page['url']}"
        print(f"🌐 Opening: {page['name']} - {full_url}")
        webbrowser.open(full_url)
    
    def open_all_pages(self, delay: float = 1.0) -> None:
        """Open all pages with a delay between each"""
        print("🚀 Starting Auto Page Opener for EHB Project")
        print("=" * 50)
        
        # Check if server is running
        print("🔍 Checking if server is running...")
        if not self.check_server_running():
            print("❌ Server not running on port 3002!")
            print("💡 Please start your server first using:")
            print("   npm run dev (in frontend directory)")
            print("   or")
            print("   python start_servers.py")
            return
        
        print("✅ Server is running!")
        print(f"📊 Opening {len(self.pages)} pages...")
        print("=" * 50)
        
        for i, page in enumerate(self.pages, 1):
            print(f"\n{i:2d}/{len(self.pages)}: {page['name']}")
            self.open_page(page)
            
            if i < len(self.pages):  # Don't delay after the last page
                print(f"⏳ Waiting {delay} seconds...")
                time.sleep(delay)
        
        print("\n" + "=" * 50)
        print("✅ All pages opened successfully!")
        print(f"📋 Total pages opened: {len(self.pages)}")
    
    def open_quick_pages(self) -> None:
        """Open only the main/important pages"""
        quick_pages = [
            {"name": "Home Page", "url": "/"},
            {"name": "Main Dashboard", "url": "/dashboard"},
            {"name": "Healthcare Dashboard", "url": "/healthcare-dashboard"},
            {"name": "Medical Records", "url": "/medical-records"},
            {"name": "Admin Panel", "url": "/admin"}
        ]
        
        print("🚀 Opening Quick Pages (Main Pages Only)")
        print("=" * 40)
        
        for i, page in enumerate(quick_pages, 1):
            print(f"{i}/{len(quick_pages)}: {page['name']}")
            self.open_page(page)
            if i < len(quick_pages):
                time.sleep(0.5)
        
        print("✅ Quick pages opened!")

def main():
    """Main function"""
    opener = AutoPageOpener()
    
    print("EHB Auto Page Opener")
    print("=" * 30)
    print("1. Open all pages")
    print("2. Open quick pages (main pages only)")
    print("3. Check server status")
    print("4. Exit")
    
    try:
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            delay = input("Enter delay between pages (default 1.0s): ").strip()
            delay = float(delay) if delay else 1.0
            opener.open_all_pages(delay)
        elif choice == "2":
            opener.open_quick_pages()
        elif choice == "3":
            if opener.check_server_running():
                print("✅ Server is running on port 3002")
            else:
                print("❌ Server is not running on port 3002")
        elif choice == "4":
            print("👋 Goodbye!")
        else:
            print("❌ Invalid choice!")
            
    except KeyboardInterrupt:
        print("\n👋 Operation cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 