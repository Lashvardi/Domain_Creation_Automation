import os
import requests
from datetime import datetime

# Environment variables from GitHub Actions
CLOUDFLARE_API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')
CLOUDFLARE_ZONE_ID = os.getenv('CLOUDFLARE_ZONE_ID')


def get_folders_in_projects():
    projects_dir = 'projects'
    if not os.path.exists(projects_dir):
        print(f"The directory {projects_dir} does not exist.")
        return []

    folders = [f for f in os.listdir(projects_dir) if os.path.isdir(os.path.join(projects_dir, f))]

    if not folders:
        print(f"No folders found in {projects_dir}.")
        return []

    # Sort folders by creation time
    folders.sort(key=lambda f: os.path.getctime(os.path.join(projects_dir, f)))
    return [os.path.join(projects_dir, f) for f in folders]


def subdomain_exists(subdomain):
    url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records?type=A&name={subdomain}"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        return len(result['result']) > 0
    else:
        print(f"Failed to check subdomain existence: {subdomain}")
        print(response.text)
        return False


def create_subdomain(folder_name):
    subdomain = f"{folder_name}.500ml.ge"
    if subdomain_exists(subdomain):
        print(f"Subdomain already exists: {subdomain}")
        return False

    url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "type": "A",
        "name": subdomain,
        "content": "157.230.119.18",
        "ttl": 1,
        "proxied": True
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print(f"Successfully created subdomain: {subdomain}")
        return True
    else:
        print(f"Failed to create subdomain: {subdomain}")
        print(response.text)
        return False


if __name__ == "__main__":
    folders = get_folders_in_projects()
    for folder in folders:
        folder_name = os.path.basename(folder)
        if create_subdomain(folder_name):
            break
