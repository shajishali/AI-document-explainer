#!/usr/bin/env python3
"""
Simple API test script for Phase 1
"""

import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing API Endpoints...")
    print("=" * 50)
    
    # Test info endpoint
    try:
        response = requests.get(f"{base_url}/api/v1/info")
        print(f"✅ Info endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Project: {data.get('project_name', 'N/A')}")
            print(f"   Version: {data.get('version', 'N/A')}")
            print(f"   Phase: {data.get('current_phase', 'N/A')}")
    except Exception as e:
        print(f"❌ Info endpoint failed: {e}")
    
    # Test status endpoint
    try:
        response = requests.get(f"{base_url}/api/v1/status")
        print(f"✅ Status endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Status: {data.get('status', 'N/A')}")
    except Exception as e:
        print(f"❌ Status endpoint failed: {e}")
    
    # Test text analysis endpoint
    try:
        test_text = "This is a test contract with terms and conditions."
        response = requests.post(
            f"{base_url}/api/v1/analyze_text",
            json={"text": test_text, "analysis_type": "comprehensive"}
        )
        print(f"✅ Text analysis endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Success: {data.get('success', 'N/A')}")
            print(f"   Risk level: {data.get('risk_level', 'N/A')}")
    except Exception as e:
        print(f"❌ Text analysis endpoint failed: {e}")

if __name__ == "__main__":
    test_api()

