import os
import requests
import logging
import json
import time
import random
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Base directory for media cache
MEDIA_CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media_cache')

# User agents to rotate through
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'
]

# List of video files from your error logs
VIDEO_FILES = [
    "web/video/beyond/beyond_preview.webm",
    "web/video/illuvium/ExplorePlanet/ranger_exploring_taiga_boreal.mp4",
    "web/video/overworld/inhabitants/roaming_illuvials.mp4",
    "web/video/illuvium/ExplorePlanet/ranger_exploring_abyssal_basin.mp4",
    "web/video/illuvium/ExplorePlanet/illuvium_planet.mp4",
    "web/video/illuvium/ExplorePlanet/ranger_exploring_crimson_waste.mp4",
    "web/video/illuvium/ExplorePlanet/ranger_exploring_brightland_steppes.mp4",
    "web/video/illuvium/CaptureIlluvials/scarabok_thumbnail.mp4",
    "web/video/illuvium/CaptureIlluvials/caradulo_thumbnail.mp4",
    "web/video/illuvium/CaptureIlluvials/hunting_video_1080.mp4",
    "web/video/illuvium/CaptureIlluvials/artace_thumbnail.mp4",
    "web/video/overworld/overworld_preview.mp4",
    "web/video/arena/survival_preview_2.mp4",
    "web/video/overworld/travel_loot/Obelisk.mp4",
    "web/video/zero/iz_hero.mp4",
    "web/video/beyond/beyond_preview.mp4",
    # Add WebM versions 
    "web/video/illuvium/ExplorePlanet/ranger_exploring_taiga_boreal.webm",
    "web/video/overworld/inhabitants/roaming_illuvials.webm",
    "web/video/illuvium/ExplorePlanet/ranger_exploring_abyssal_basin.webm",
    "web/video/illuvium/ExplorePlanet/illuvium_planet.webm",
    "web/video/illuvium/ExplorePlanet/ranger_exploring_crimson_waste.webm"
]

# Possible source domains
DOMAINS = [
    "media.illuvium.io",
    "assets.illuvium.io",
    "static.illuvium.io",
    "illuvium.io",
    "overworld.illuvium.io",
    "cdn.coinary.app",
    "d26yxn7t2ufchj.cloudfront.net"
]

def ensure_directory_exists(path):
    """Ensure the directory exists, create if it doesn't."""
    os.makedirs(path, exist_ok=True)

def scrape_video_sources():
    """Scrape the Illuvium site to find video sources"""
    sources = {}
    
    try:
        # Try to load from cache if available
        cache_file = "video_sources_cache.json"
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                sources = json.load(f)
                logger.info(f"Loaded {len(sources)} video sources from cache")
                return sources
    except Exception as e:
        logger.error(f"Error loading cached sources: {str(e)}")
    
    # Scrape the main site
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        response = requests.get('https://overworld.illuvium.io/', headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all script tags
            for script in soup.find_all('script'):
                if script.string:
                    # Look for video URLs
                    matches = re.findall(r'(https?://[^"\']+\.(?:webm|mp4))', script.string)
                    for url in matches:
                        # Extract filename
                        filename = url.split('/')[-1]
                        if filename not in sources:
                            sources[filename] = []
                        sources[filename].append(url)
            
            # Try to find Next.js data
            next_data = soup.find('script', id='__NEXT_DATA__')
            if next_data and next_data.string:
                try:
                    data = json.loads(next_data.string)
                    extract_urls_from_json(data, sources)
                except json.JSONDecodeError:
                    logger.error("Failed to parse Next.js data")
    
    except Exception as e:
        logger.error(f"Error scraping main site: {str(e)}")
    
    # Cache the results
    try:
        with open(cache_file, 'w') as f:
            json.dump(sources, f)
            logger.info(f"Cached {len(sources)} video sources")
    except Exception as e:
        logger.error(f"Error caching sources: {str(e)}")
    
    return sources

def extract_urls_from_json(obj, sources, path=''):
    """Extract video URLs from JSON objects"""
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_path = f"{path}.{key}" if path else key
            
            if isinstance(value, str) and (value.endswith('.webm') or value.endswith('.mp4')):
                filename = value.split('/')[-1]
                if filename not in sources:
                    sources[filename] = []
                sources[filename].append(value)
            
            elif isinstance(value, (dict, list)):
                extract_urls_from_json(value, sources, new_path)
    
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            new_path = f"{path}[{i}]"
            extract_urls_from_json(item, sources, new_path)

def generate_source_urls(path):
    """Generate possible source URLs for a video path"""
    filename = os.path.basename(path)
    urls = []
    
    # Add direct domain sources
    for domain in DOMAINS:
        urls.append(f"https://{domain}/{path}")
        # Try with /media/ prefix
        urls.append(f"https://{domain}/media/{path}")
        # Try without web/ prefix if it exists
        if path.startswith("web/"):
            urls.append(f"https://{domain}/{path[4:]}")
            urls.append(f"https://{domain}/media/{path[4:]}")
    
    # Add potential CDN URLs
    urls.append(f"https://cdn.coinary.app/videos/{filename}")
    urls.append(f"https://d26yxn7t2ufchj.cloudfront.net/{path}")
    
    return urls

def download_video(path):
    """Download a video from various potential sources"""
    local_path = os.path.join(MEDIA_CACHE_DIR, path)
    
    # Skip if file already exists and is not empty
    if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
        logger.info(f"Skipping existing file: {local_path}")
        return True
    
    # Create directory
    ensure_directory_exists(os.path.dirname(local_path))
    
    # Get sources from scraped data
    scraped_sources = scrape_video_sources()
    filename = os.path.basename(path)
    
    urls = []
    
    # First try any scraped URLs for this filename
    if filename in scraped_sources:
        urls.extend(scraped_sources[filename])
    
    # Add generated URLs
    urls.extend(generate_source_urls(path))
    
    # Make URLs unique
    urls = list(dict.fromkeys(urls))
    
    # Try each URL
    for url in urls:
        try:
            headers = {
                'User-Agent': random.choice(USER_AGENTS),
                'Referer': 'https://overworld.illuvium.io/',
                'Origin': 'https://overworld.illuvium.io'
            }
            
            logger.info(f"Trying to download from: {url}")
            response = requests.get(url, headers=headers, stream=True, timeout=15)
            
            if response.status_code == 200:
                # Save the file
                with open(local_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                # Verify the file is not empty
                if os.path.getsize(local_path) > 0:
                    logger.info(f"Successfully downloaded: {local_path}")
                    return True
                else:
                    logger.warning(f"Downloaded file is empty: {local_path}")
                    os.remove(local_path)
        
        except Exception as e:
            logger.error(f"Error downloading from {url}: {str(e)}")
    
    logger.error(f"Failed to download: {path}")
    return False

def create_placeholder_videos():
    """Create placeholder videos for all formats"""
    # Create static/fallbacks directory
    fallback_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'fallbacks')
    ensure_directory_exists(fallback_dir)
    
    # List of placeholder files to create
    placeholders = [
        ('fallback.webm', 'video/webm'),
        ('fallback.mp4', 'video/mp4')
    ]
    
    for filename, content_type in placeholders:
        placeholder_path = os.path.join(fallback_dir, filename)
        
        # Skip if already exists
        if os.path.exists(placeholder_path):
            logger.info(f"Placeholder already exists: {placeholder_path}")
            continue
        
        try:
            # Create a minimal placeholder file
            # In production, you would want to use actual video files
            with open(placeholder_path, 'wb') as f:
                f.write(b'This is a placeholder file. Replace with an actual video.')
            
            logger.info(f"Created placeholder: {placeholder_path}")
        
        except Exception as e:
            logger.error(f"Error creating placeholder {filename}: {str(e)}")

def main():
    """Download all video files"""
    start_time = time.time()
    
    # Ensure base directory exists
    ensure_directory_exists(MEDIA_CACHE_DIR)
    
    # Create placeholder videos
    create_placeholder_videos()
    
    # Download videos in parallel
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(download_video, VIDEO_FILES))
    
    # Log results
    success_count = sum(results)
    logger.info(f"Downloaded {success_count}/{len(VIDEO_FILES)} videos in {time.time() - start_time:.2f} seconds")
    
    # List any failures
    if success_count < len(VIDEO_FILES):
        logger.warning("Failed to download these videos:")
        for i, success in enumerate(results):
            if not success:
                logger.warning(f"  - {VIDEO_FILES[i]}")

if __name__ == "__main__":
    main()