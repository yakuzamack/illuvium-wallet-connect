import requests
import re
import os
from bs4 import BeautifulSoup
import json

# Ensure directories exist
os.makedirs('media_cache/web/video/illuvium/ExplorePlanet', exist_ok=True)
os.makedirs('media_cache/web/video/overworld/inhabitants', exist_ok=True)
os.makedirs('media_cache/web/video/beyond', exist_ok=True)

# Headers to mimic a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    'Accept': 'text/html,application/xhtml+xml,application/xml',
    'Accept-Language': 'en-US,en;q=0.9'
}

# Get the main page
response = requests.get('https://overworld.illuvium.io', headers=headers)
html_content = response.text

# Extract all video URLs
video_urls = re.findall(r'(https://[^"\'\s]+\.(?:mp4|webm)[^"\'\s]*)', html_content)
print(f"Found {len(video_urls)} video URLs")

# Extract from Next.js data
soup = BeautifulSoup(html_content, 'html.parser')
next_data = soup.find('script', id='__NEXT_DATA__')
if next_data and next_data.string:
    try:
        data = json.loads(next_data.string)
        # Save the full Next.js data for inspection
        with open('next_data.json', 'w') as f:
            json.dump(data, f, indent=2)
        print("Saved Next.js data for inspection")
    except:
        print("Error parsing Next.js data")

# Download found videos
for i, url in enumerate(video_urls):
    filename = url.split('/')[-1].split('?')[0]  # Remove query params
    path = os.path.join('media_cache', 'extracted', filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    print(f"Downloading {i+1}/{len(video_urls)}: {filename}")
    try:
        video_response = requests.get(url, headers=headers, stream=True)
        if video_response.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in video_response.iter_content(8192):
                    if chunk:
                        f.write(chunk)
            print(f"✅ Downloaded {path} ({os.path.getsize(path)} bytes)")
        else:
            print(f"❌ Failed: {video_response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")