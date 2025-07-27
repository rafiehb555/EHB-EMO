#!/usr/bin/env python3
"""
Quick EHB Page Opener
Automatically opens all pages without user interaction
"""

import time
import webbrowser

import requests


def check_server():
    """Check if server is running"""
    try:
        response = requests.get("http://localhost:3002/", timeout=3)
        return response.status_code == 200
    except:
        return False

def open_all_pages():
    """Open all pages automatically"""
    base_url = "http://localhost:3002"
    
    pages = [
        "/",                    # Home
        "/test",               # Test
        "/dashboard",          # Main Dashboard
        "/dashboard/wallet",   # Wallet Dashboard
        "/dashboard/profile",  # Profile Dashboard
        "/dashboard/store",    # Store Dashboard
        "/dashboard/emo",      # Emo Dashboard
        "/medical-records",    # Medical Records
        "/appointments",       # Appointments
        "/patients",           # Patients
        "/analytics",          # Analytics
        "/telemedicine",       # Telemedicine
        "/ai-diagnosis",       # AI Diagnosis
        "/healthcare-dashboard", # Healthcare Dashboard
        "/admin",              # Admin Panel
        "/agent-dashboard"     # Agent Dashboard
    ]
    
    print("🚀 EHB Auto Page Opener")
    print("=" * 30)
    
    # Check server
    print("🔍 Checking server...")
    if not check_server():
        print("❌ Server not running on port 3002!")
        print("💡 Please start your server first:")
        print("   cd frontend && npm run dev")
        print("   or")
        print("   python start_servers.py")
        return
    
    print("✅ Server is running!")
    print(f"🌐 Opening {len(pages)} pages...")
    print("=" * 30)
    
    # Open all pages
    for i, page in enumerate(pages, 1):
        url = base_url + page
        print(f"{i:2d}/{len(pages)}: {url}")
        webbrowser.open(url)
        time.sleep(0.5)  # Small delay between pages
    
    print("=" * 30)
    print("✅ All pages opened successfully!")
    print(f"📊 Total pages: {len(pages)}")

if __name__ == "__main__":
    open_all_pages() 