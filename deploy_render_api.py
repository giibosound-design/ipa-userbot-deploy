#!/usr/bin/env python3
"""
Deploy to Render.com via API
"""
import requests
import json
import time

RENDER_API_KEY = "rnd_Sr3rAy81D0cahPvTtsaaFcBAR7xp"
RENDER_API_URL = "https://api.render.com/v1"
GITHUB_REPO = "https://github.com/giibosound-design/ipa-userbot-deploy"

# Read session file
with open("session.b64", "r") as f:
    SESSION_B64 = f.read().strip()

headers = {
    "Authorization": f"Bearer {RENDER_API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def create_service():
    """Create web service on Render"""
    print("Creating web service on Render.com...")
    print()
    
    service_data = {
        "type": "web_service",
        "name": f"ipa-userbot-{int(time.time())}",
        "ownerId": "tea-d4biguhr0fns73ffobmg",
        "repo": GITHUB_REPO,
        "branch": "master",
        "autoDeploy": "yes",
        "rootDir": ".",
        "serviceDetails": {
            "env": "docker",
            "envSpecificDetails": {
                "dockerfilePath": "./Dockerfile",
                "dockerContext": "."
            },
            "healthCheckPath": "/health",
            "plan": "free",
            "region": "oregon"
        },
        "envVars": [
            {"key": "API_ID", "value": "39967356"},
            {"key": "API_HASH", "value": "6aea1aa164d582ea5b233a795673d4a5"},
            {"key": "PHONE_NUMBER", "value": "+37062838692"},
            {"key": "LOG_LEVEL", "value": "INFO"},
            {"key": "PORT", "value": "10000"},
            {"key": "SESSION_FILE_B64", "value": SESSION_B64}
        ]
    }
    
    print("Sending request to Render API...")
    response = requests.post(
        f"{RENDER_API_URL}/services",
        headers=headers,
        json=service_data
    )
    
    print(f"Status code: {response.status_code}")
    print()
    
    if response.status_code in [200, 201]:
        service = response.json()
        print("=" * 70)
        print("✅ SERVICE CREATED SUCCESSFULLY!")
        print("=" * 70)
        print()
        print(f"Service ID: {service.get('service', {}).get('id')}")
        print(f"Service Name: {service.get('service', {}).get('name')}")
        print(f"Service URL: {service.get('service', {}).get('serviceDetails', {}).get('url')}")
        print()
        print("Deployment started. This will take 5-10 minutes...")
        print()
        print("=" * 70)
        return service
    else:
        print("=" * 70)
        print("❌ FAILED TO CREATE SERVICE")
        print("=" * 70)
        print()
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        print()
        
        # Try to parse error
        try:
            error = response.json()
            print(f"Error details: {json.dumps(error, indent=2)}")
        except:
            pass
        
        print()
        print("=" * 70)
        return None

if __name__ == "__main__":
    print("=" * 70)
    print("DEPLOYING TO RENDER.COM")
    print("=" * 70)
    print()
    print(f"Repository: {GITHUB_REPO}")
    print(f"Branch: master")
    print()
    
    service = create_service()
    
    if service:
        print()
        print("✅ Deployment initiated successfully!")
        print()
        print("Next steps:")
        print("1. Wait 5-10 minutes for Docker build to complete")
        print("2. Check deployment status in Render Dashboard")
        print("3. Test the bot in Telegram with .start command")
    else:
        print()
        print("❌ Deployment failed. Please check the error above.")
