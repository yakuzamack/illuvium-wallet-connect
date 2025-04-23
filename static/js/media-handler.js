// Handle media.illuvium.io video proxying
document.addEventListener('DOMContentLoaded', function() {
  console.log('Media handler initialized');
  
  // Find all video elements
  const processVideos = () => {
    const videos = document.querySelectorAll('video');
    console.log(`Found ${videos.length} video elements`);
    
    videos.forEach(video => {
      // Process source elements
      const sources = video.querySelectorAll('source');
      sources.forEach(source => {
        if (source.src && source.src.includes('media.illuvium.io')) {
          console.log(`Redirecting video source: ${source.src}`);
          const originalPath = source.src.replace('https://media.illuvium.io/', '');
          source.src = `/proxy/media/${originalPath}`;
        }
      });
      
      // Also check for src attribute directly on video
      if (video.src && video.src.includes('media.illuvium.io')) {
        console.log(`Redirecting video src: ${video.src}`);
        const originalPath = video.src.replace('https://media.illuvium.io/', '');
        video.src = `/proxy/media/${originalPath}`;
      }
      
      // Reload the video to apply the new sources
      try {
        video.load();
      } catch (e) {
        console.error('Error reloading video:', e);
      }
    });
  };
  
  // Process videos now
  processVideos();
  
  // Also process videos that might be added dynamically later
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.addedNodes && mutation.addedNodes.length > 0) {
        processVideos();
      }
    });
  });
  
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
});