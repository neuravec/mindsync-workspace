/*! MindSync blog attribution v1.0.0. No cookies, no storage. See README.md */
(function(){
var APPLE_PROVIDER_TOKEN='127496944';           // App Store Connect provider token; empty = no pt
var HUBS=['/','/features'];            // internal pages with store badges
var HOST=/^(www\.)?mindsync\.app$/,L=location,slug=null,post=false;
var m=L.pathname.match(/^\/journal\/([^\/]+)/);
if(m){slug=m[1].toLowerCase();post=true}
else{try{var f=new URLSearchParams(L.search).get('from')||'';if(/^blog-[a-z0-9-]{1,80}$/.test(f))slug=f.slice(5)}catch(e){}}
if(!slug||!/^[a-z0-9-]{1,80}$/.test(slug))return;
function kind(u){
if(u.hostname=='play.google.com'&&u.pathname=='/store/apps/details'&&u.searchParams.get('id')=='com.mindsync.app')return'google';
if(u.hostname=='apps.apple.com'&&/\/id6739644256(\/|$)/.test(u.pathname))return'apple';
return null}
// medium: post page -> 'inline' inside post body (.w-richtext), else 'badge'
// (template CTA block, footer); other page reached via ?from= -> 'card'
function medium(a){return!post?'card':a.closest('.w-richtext')?'inline':'badge'}
function deco(a){
if(a.getAttribute('data-msb'))return;
var u;try{u=new URL(a.href)}catch(e){return}
var s=kind(u);if(!s)return;
var md=medium(a),p=u.searchParams;
if(s=='google'){if(!p.has('referrer'))p.set('referrer','utm_source=blog&utm_medium='+md+'&utm_campaign='+slug)}
else{if(!p.has('ct'))p.set('ct',('blog-'+slug).slice(0,40));if(APPLE_PROVIDER_TOKEN&&!p.has('pt'))p.set('pt',APPLE_PROVIDER_TOKEN)}
a.href=u.toString();a.setAttribute('data-msb',s+'|'+md)}
// internal hub links get ?from= only at interaction time, so crawlers never see it
function hub(a){
if(!post||a.getAttribute('data-msb'))return;
var u;try{u=new URL(a.getAttribute('href'),L.href)}catch(e){return}
if(!HOST.test(u.hostname)||HUBS.indexOf(u.pathname.replace(/\/+$/,'')||'/')<0)return;
if(!u.searchParams.has('from'))u.searchParams.set('from','blog-'+slug);
a.href=u.toString();a.setAttribute('data-msb','hub')}
function link(e){var t=e.target;return t&&t.closest?t.closest('a[href]'):null}
function scan(){var l=document.querySelectorAll('a[href]');for(var i=0;i<l.length;i++)deco(l[i])}
document.addEventListener('pointerdown',function(e){var a=link(e);if(a)hub(a)},true);
document.addEventListener('click',function(e){
var a=link(e);if(!a)return;hub(a);deco(a);
var d=(a.getAttribute('data-msb')||'').split('|');if(!d[1])return;
if(window.posthog&&window.__msA){try{window.posthog.capture('blog_store_click',{store:d[0],blog_slug:slug,medium:d[1],page_path:L.pathname})}catch(x){}}
},true);
if(document.readyState=='loading')document.addEventListener('DOMContentLoaded',scan);else scan();
window.addEventListener('load',scan);
})();
