#!/usr/bin/env python3
"""
Deploy Telethon userbot to Render.com via API
"""
import requests
import json
import time
import base64

# Render API configuration
RENDER_API_KEY = "rnd_Sr3rAy81D0cahPvTtsaaFcBAR7xp"
RENDER_API_URL = "https://api.render.com/v1"

# Read session file
with open("session.b64", "r") as f:
    SESSION_B64 = f.read().strip()

headers = {
    "Authorization": f"Bearer {RENDER_API_KEY}",
    "Content-Type": "application/json"
}

def create_web_service():
    """Create a new web service on Render"""
    print("Creating web service on Render...")
    
    # Service configuration
    service_config = {
        "type": "web_service",
        "name": f"ipa-userbot-{int(time.time())}",
        "ownerId": "tea-d4biguhr0fns73ffobmg",  # From workspace settings
        "repo": "https://github.com/placeholder/repo",  # We'll use Docker image instead
        "autoDeploy": "yes",
        "branch": "main",
        "buildCommand": "",
        "startCommand": "/app/start.sh",
        "envVars": [
            {"key": "API_ID", "value": "39967356"},
            {"key": "API_HASH", "value": "6aea1aa164d582ea5b233a795673d4a5"},
            {"key": "PHONE_NUMBER", "value": "+37062838692"},
            {"key": "LOG_LEVEL", "value": "INFO"},
            {"key": "PORT", "value": "8080"},
            {"key": "SESSION_FILE_B64", "value": SESSION_B64}
        ],
        "serviceDetails": {
            "env": "docker",
            "envSpecificDetails": {
                "dockerCommand": "/app/start.sh",
                "dockerContext": ".",
                "dockerfilePath": "./Dockerfile"
            }
        },
        "disk": {
            "name": "userbot-data",
            "mountPath": "/tmp/ipa_bot",
            "sizeGB": 1
        }
    }
    
    response = requests.post(
        f"{RENDER_API_URL}/services",
        headers=headers,
        json=service_config
    )
    
    if response.status_code in [200, 201]:
        service = response.json()
        print(f"✅ Service created: {service.get('id')}")
        print(f"✅ Service name: {service.get('name')}")
        print(f"✅ Service URL: {service.get('serviceDetails', {}).get('url')}")
        return service
    else:
        print(f"❌ Failed to create service: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def get_services():
    """List all services"""
    print("Fetching existing services...")
    
    response = requests.get(
        f"{RENDER_API_URL}/services",
        headers=headers
    )
    
    if response.status_code == 200:
        services = response.json()
        print(f"Found {len(services)} services")
        for svc in services:
            print(f"  - {svc.get('name')} ({svc.get('id')})")
        return services
    else:
        print(f"❌ Failed to fetch services: {response.status_code}")
        print(f"Response: {response.text}")
        return []

if __name__ == "__main__":
    print("=" * 70)
    print("DEPLOYING TO RENDER.COM")
    print("=" * 70)
    print()
    
    # Try to get services first
    services = get_services()
    
    print()
    print("Note: Render API requires GitHub repository for deployment.")
    print("Please create a GitHub repository and push the code there.")
    print()
    print("Then use Render Dashboard to:")
    print("1. Click 'New +' → 'Web Service'")
    print("2. Connect your GitHub repository")
    print("3. Set environment variables (will be shown next)")
    print()
    print("=" * 70)
    print("ENVIRONMENT VARIABLES TO SET:")
    print("=" * 70)
    print()
    print("API_ID=39967356")
    print("API_HASH=6aea1aa164d582ea5b233a795673d4a5")
    print("PHONE_NUMBER=+37062838692")
    print("LOG_LEVEL=INFO")
    print("PORT=8080")
    print(f"SESSION_FILE_B64={SESSION_B64[:50]}...")
    print()
    print("=" * 70)
