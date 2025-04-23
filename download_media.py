import os
import requests
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Base directory for media cache
MEDIA_CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media_cache')

# List of known media files from your error list
MEDIA_FILES = [
    "https://overworld.illuvium.io/web/video/illuvium/ExplorePlanet/ranger_exploring_taiga_boreal.webm",
    "web/video/illuvium/ExplorePlanet/ranger_exploring_abyssal_basin.webm",
    "web/video/illuvium/ExplorePlanet/illuvium_planet.webm",
    "web/video/overworld/inhabitants/roaming_illuvials.webm",
    "web/video/illuvium/ExplorePlanet/ranger_exploring_brightland_steppes.webm",
    "web/video/illuvium/ExplorePlanet/ranger_exploring_crimson_waste.webm",
    "web/video/illuvium/CaptureIlluvials/adoredo_thumbnail.webm",
    "web/video/illuvium/CaptureIlluvials/scarabok_thumbnail.webm",
    "web/video/illuvium/CaptureIlluvials/caradulo_thumbnail.webm",
    "web/video/illuvium/CaptureIlluvials/hunting_video_1080.webm",
    "web/video/illuvium/CaptureIlluvials/artace_thumbnail.webm",
    "web/video/zero/iz_hero.webm",
    "web/video/overworld/overworld_preview.webm",
    # Add MP4 versions
    "web/video/illuvium/ExplorePlanet/ranger_exploring_taiga_boreal.mp4",
    "web/video/arena/survival_preview_2.webm",
    "web/video/beyond/beyond_preview.webm",
    # Add more files as needed
]

def ensure_directory_exists(path):
    """Ensure the directory exists, create if it doesn't."""
    os.makedirs(path, exist_ok=True)

def download_media(url, local_path):
    """Download a media file from the URL and save it to the local path."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
            'Referer': 'https://overworld.illuvium.io/'
        }
        
        response = requests.get(url, headers=headers, stream=True, timeout=15)
        
        if response.status_code == 200:
            ensure_directory_exists(os.path.dirname(local_path))
            
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        
            logger.info(f"Downloaded: {url} -> {local_path}")
            return True
        else:
            logger.error(f"Failed to download {url}: Status code {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Error downloading {url}: {str(e)}")
        return False

def main():
    """Download all media files."""
    # Create base directory
    ensure_directory_exists(MEDIA_CACHE_DIR)
    
    success_count = 0
    
    for media_path in MEDIA_FILES:
        local_path = os.path.join(MEDIA_CACHE_DIR, media_path)
        
        # Skip if file already exists
        if os.path.exists(local_path):
            logger.info(f"Skipping existing file: {local_path}")
            success_count += 1
            continue
        
        # Try possible sources
        sources = [
            f"https://media.illuvium.io/{media_path}",
            f"https://overworld.illuvium.io/media/{media_path}",
            f"https://overworld.illuvium.io/{media_path}",
            f"https://cdn.illuvium.io/{media_path}"
        ]
        
        for source_url in sources:
            if download_media(source_url, local_path):
                success_count += 1
                break
    
    logger.info(f"Downloaded {success_count}/{len(MEDIA_FILES)} media files")

if __name__ == "__main__":
    main()