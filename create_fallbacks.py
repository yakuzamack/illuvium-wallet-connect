import os
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_fallback_videos():
    """Download small fallback videos for different formats"""
    fallback_dir = 'static/fallbacks'
    os.makedirs(fallback_dir, exist_ok=True)
    
    # Source URLs for small sample videos
    sources = {
        'mp4': 'https://samplelib.com/lib/preview/mp4/sample-5s.mp4',
        'webm': 'https://samplelib.com/lib/preview/webm/sample-5s.webm'
    }
    
    for ext, url in sources.items():
        fallback_path = os.path.join(fallback_dir, f"fallback.{ext}")
        
        try:
            logger.info(f"Downloading fallback {ext} video from {url}")
            response = requests.get(url, stream=True)
            
            if response.status_code == 200:
                with open(fallback_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                logger.info(f"Downloaded fallback video: {fallback_path} ({os.path.getsize(fallback_path)} bytes)")
            else:
                logger.error(f"Failed to download fallback video: {response.status_code}")
        except Exception as e:
            logger.error(f"Error downloading fallback: {str(e)}")

if __name__ == "__main__":
    download_fallback_videos()