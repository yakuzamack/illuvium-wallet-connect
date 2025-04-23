import os
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Base directory for media cache
MEDIA_CACHE_DIR = 'media_cache'

# List of missing video files from error logs
MISSING_VIDEOS = [
    "web/video/zero/iz_hero.mp4",
    "web/video/zero/iz_hero.webm",
    "web/video/beyond/beyond_preview.mp4",
    "web/video/beyond/beyond_preview.webm",
    "web/video/illuvium/ExplorePlanet/ranger_exploring_taiga_boreal.webm",
    "web/video/overworld/overworld_preview.webm",
    "web/video/arena/survival_preview_2.webm"
]

# Possible source domains
DOMAINS = [
    "overworld.illuvium.io",
    "illuvium.io",
    "media.illuvium.io"
]

def ensure_directory_exists(path):
    """Ensure the directory exists, create if it doesn't."""
    os.makedirs(path, exist_ok=True)

def create_fallback_video(path, is_webm=False):
    """Create fallback video file with a valid header"""
    try:
        local_path = os.path.join(MEDIA_CACHE_DIR, path)
        ensure_directory_exists(os.path.dirname(local_path))
        
        # Download a small sample video file as fallback
        url = "https://sample-videos.com/video123/mp4/240/big_buck_bunny_240p_1mb.mp4"
        if is_webm:
            url = "https://sample-videos.com/video123/webm/240/big_buck_bunny_240p_1mb.webm"
        
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            logger.info(f"Created fallback video: {local_path}")
            return True
        else:
            logger.error(f"Failed to download fallback video: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Error creating fallback: {str(e)}")
        return False

def main():
    """Create fallback videos for all missing files"""
    for video_path in MISSING_VIDEOS:
        logger.info(f"Processing: {video_path}")
        
        # Attempt to download from original sites
        success = False
        for domain in DOMAINS:
            if success:
                break
                
            url = f"https://{domain}/{video_path}"
            try:
                logger.info(f"Trying: {url}")
                response = requests.head(url, timeout=5)
                
                if response.status_code == 200:
                    logger.info(f"Found at: {url}")
                    # Download the file
                    download_response = requests.get(url, stream=True)
                    if download_response.status_code == 200:
                        local_path = os.path.join(MEDIA_CACHE_DIR, video_path)
                        ensure_directory_exists(os.path.dirname(local_path))
                        
                        with open(local_path, 'wb') as f:
                            for chunk in download_response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                        
                        logger.info(f"Downloaded: {local_path}")
                        success = True
            except Exception as e:
                logger.warning(f"Error checking {url}: {str(e)}")
        
        # If we couldn't find the original, create a fallback
        if not success:
            logger.warning(f"Creating fallback for: {video_path}")
            is_webm = video_path.endswith('.webm')
            create_fallback_video(video_path, is_webm)

if __name__ == "__main__":
    ensure_directory_exists(MEDIA_CACHE_DIR)
    main()
    logger.info("Done creating fallback videos")