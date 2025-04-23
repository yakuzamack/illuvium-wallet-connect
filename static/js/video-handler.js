// Handle all media.illuvium.io videos
document.addEventListener('DOMContentLoaded', function() {
  console.log('Video handler initialized');
  
  function processVideoElements() {
    // Find all video elements and sources
    const videos = document.querySelectorAll('video');
    console.log(`Found ${videos.length} video elements`);
    
    videos.forEach(function(video) {
      // Handle direct src attribute
      if (video.src && video.src.includes('media.illuvium.io')) {
        const originalPath = video.src.replace('https://media.illuvium.io/', '');
        console.log(`Redirecting video src: ${video.src} -> /proxy/media/${originalPath}`);
        video.src = `/proxy/media/${originalPath}`;
        
        // For direct src attributes, we need to trigger load
        try {
          video.load();
        } catch(e) {
          console.error('Error reloading video:', e);
        }
      }
      
      // Handle source elements
      const sources = video.querySelectorAll('source');
      let sourcesChanged = false;
      
      sources.forEach(function(source) {
        if (source.src && source.src.includes('media.illuvium.io')) {
          const originalPath = source.src.replace('https://media.illuvium.io/', '');
          console.log(`Redirecting video source: ${source.src} -> /proxy/media/${originalPath}`);
          source.src = `/proxy/media/${originalPath}`;
          sourcesChanged = true;
        }
      });
      
      // If we changed any sources, reload the video
      if (sourcesChanged) {
        try {
          video.load();
        } catch(e) {
          console.error('Error reloading video after source change:', e);
        }
      }
    });
  }
  
  // Process videos on page load
  processVideoElements();
  
  // Watch for dynamically added videos
  const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
      if (mutation.addedNodes && mutation.addedNodes.length > 0) {
        // Check if any added node is a video or contains videos
        for (let i = 0; i < mutation.addedNodes.length; i++) {
          const node = mutation.addedNodes[i];
          if (node.nodeName === 'VIDEO') {
            processVideoElements();
            break;
          } else if (node.nodeType === 1) { // Element node
            if (node.querySelector('video')) {
              processVideoElements();
              break;
            }
          }
        }
      }
    });
  });
  
  // Start observing the document
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
});