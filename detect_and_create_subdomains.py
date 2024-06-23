import os
import requests

# Environment variables from GitHub Actions
CLOUDFLARE_API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')
CLOUDFLARE_ZONE_ID = os.getenv('CLOUDFLARE_ZONE_ID')


def get_existing_folders():
    folders = []
    for root, dirs, files in os.walk('.'):
        for d in dirs:
            folders.append(os.path.join(root, d))
    return folders


def create_subdomain(folder_name):
    subdomain = f"{folder_name}.yourdomain.com"
    url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "type": "A",
        "name": "test",
        "content": "157.230.119.18",
        "ttl": 1,
        "proxied": False
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print(f"Successfully created subdomain: {subdomain}")
    else:
        print(f"Failed to create subdomain: {subdomain}")
        print(response.text)


if __name__ == "__main__":
    existing_folders = get_existing_folders()
    for folder in existing_folders:
        folder_name = os.path.basename(folder)
        create_subdomain(folder_name)
