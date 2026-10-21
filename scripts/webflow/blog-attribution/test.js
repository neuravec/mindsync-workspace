// Local test harness: node scripts/webflow/blog-attribution/test.js
// Runs blog-attribution.js in a vm sandbox with a minimal fake DOM. No deps.
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm'), assert = require('assert');
// Without an argument: run the suite against both builds (readable + minified) in child processes.
if (!process.argv[2]) {
  const { execFileSync } = require('child_process');
  for (const f of ['blog-attribution.js', 'blog-attribution.min.js']) {
    console.log('### ' + f);
    process.stdout.write(execFileSync(process.execPath, [__filename, f], { encoding: 'utf8' }));
  }
  process.exit(0);
}
const FILE = process.argv[2], MIN = /\.min\.js$/.test(FILE);
const SRC = fs.readFileSync(path.join(__dirname, FILE), 'utf8');
const PLAY = 'https://play.google.com/store/apps/details?id=com.mindsync.app';
const APPLE = 'https://apps.apple.com/us/app/mindsync-ai-health-journal/id6739644256';

class El {
  constructor(cls, parent, href) {
    this.cls = cls ? cls.split(' ') : []; this.parent = parent || null; this.attrs = {};
    if (href !== undefined) { this.tag = 'a'; this.attrs.href = href; } else this.tag = 'div';
  }
  matches(sel) {
    if (sel === 'a[href]' || sel === 'a') return this.tag === 'a' && 'href' in this.attrs;
    if (sel[0] === '.') return this.cls.includes(sel.slice(1));
    return false;
  }
  closest(sel) { for (let n = this; n; n = n.parent) if (n.matches(sel)) return n; return null; }
  getAttribute(k) { return k in this.attrs ? this.attrs[k] : null; }
  setAttribute(k, v) { this.attrs[k] = String(v); }
}

function page(url, opts = {}) {
  const loc = new URL(url);
  const anchors = [], listeners = {}, winListeners = {}, captured = [], calls = [];
  const location = { pathname: loc.pathname, search: loc.search, href: loc.href };
  const mk = (href, cls, parentCls) => {
    const parent = new El(parentCls || 'body');
    const a = new El(cls || '', parent, href);
    Object.defineProperty(a, 'href', {
      get() { return new URL(this.attrs.href, location.href).toString(); },
      set(v) { this.attrs.href = v; },
    });
    anchors.push(a); return a;
  };
  const document = {
    readyState: opts.readyState || 'loading',
    querySelectorAll: () => anchors.slice(),
    addEventListener(t, fn) { (listeners[t] = listeners[t] || []).push(fn); },
  };
  const window = {
    __msA: !!opts.consent,
    posthog: opts.noPosthog ? undefined : {
      capture: (n, p) => captured.push([n, p]),
      identify: () => calls.push('identify'),
    },
    addEventListener(t, fn) { (winListeners[t] = winListeners[t] || []).push(fn); },
  };
  // Simulated msconsent-1.0.0.js click handler (same logic as live), registered FIRST.
  document.addEventListener('click', function (e) {
    const link = e.target.closest('a'); if (!link) return;
    const href = link.href || ''; let store = null;
    if (href.indexOf('apps.apple.com') > -1) store = 'apple';
    else if (href.indexOf('play.google.com') > -1) store = 'google';
    if (!store) return;
    if (window.posthog && window.__msA) window.posthog.capture('app_store_click', { store });
  });
  const src = opts.src || SRC;
  return {
    mk, captured, calls,
    run() { vm.runInNewContext(src, { window, document, location, URL, URLSearchParams }); },
    fire(t) { (listeners[t] || []).forEach(f => f()); },
    load() { (winListeners.load || []).forEach(f => f()); },
    click(a) {
      const e = { target: a };
      (listeners.pointerdown || []).forEach(f => f(e));
      (listeners.click || []).forEach(f => f(e));
    },
  };
}
const q = (a, k) => new URL(a.attrs.href, 'https://www.mindsync.app/').searchParams.get(k);
// JSON round-trip: objects created inside the vm realm have a different Object prototype.
const blogEvents = p => JSON.parse(JSON.stringify(p.captured.filter(c => c[0] === 'blog_store_click')));

let n = 0;
const t = (name, fn) => { fn(); n++; console.log('ok ' + n + ' ' + name); };

t('post page: template badge, inline links, apple ct, configured pt', () => {
  const p = page('https://www.mindsync.app/journal/how-to-use-mindsync', { consent: true });
  const badgeG = p.mk(PLAY, 'w-inline-block', 'blog-cta-buttons');
  const inlineG = p.mk(PLAY, '', 'rich-text-block w-richtext');
  const badgeA = p.mk(APPLE, 'w-inline-block', 'blog-cta-buttons');
  const footerA = p.mk(APPLE, 'link-block-footer applestore', 'footer');
  p.run(); p.fire('DOMContentLoaded');
  assert.strictEqual(q(badgeG, 'referrer'), 'utm_source=blog&utm_medium=badge&utm_campaign=how-to-use-mindsync');
  assert.ok(badgeG.attrs.href.includes('referrer=utm_source%3Dblog%26utm_medium%3Dbadge%26utm_campaign%3Dhow-to-use-mindsync'));
  assert.strictEqual(q(badgeG, 'id'), 'com.mindsync.app');
  assert.strictEqual(q(inlineG, 'referrer'), 'utm_source=blog&utm_medium=inline&utm_campaign=how-to-use-mindsync');
  assert.strictEqual(q(badgeA, 'ct'), 'blog-how-to-use-mindsync');
  assert.strictEqual(q(badgeA, 'pt'), '127496944');
  assert.strictEqual(q(footerA, 'ct'), 'blog-how-to-use-mindsync');
});

t('idempotent: load rescan does not double-add; existing params preserved', () => {
  const p = page('https://www.mindsync.app/journal/abc');
  const pre = p.mk(PLAY + '&hl=en&referrer=utm_source%3Dother', '', 'blog-cta-buttons');
  const g = p.mk(PLAY, '', 'blog-cta-buttons');
  p.run(); p.fire('DOMContentLoaded'); const once = g.attrs.href; p.load(); p.load();
  assert.strictEqual(g.attrs.href, once);
  assert.strictEqual((g.attrs.href.match(/referrer=/g) || []).length, 1);
  assert.strictEqual(q(pre, 'referrer'), 'utm_source=other');
  assert.strictEqual(q(pre, 'hl'), 'en');
});

t('internal hub links get from= only on interaction, others untouched', () => {
  const p = page('https://www.mindsync.app/journal/abc');
  const card = p.mk('https://mindsync.app/features', '', 'w-richtext');
  const nav = p.mk('/features', 'nav-link');
  const logo = p.mk('/', 'logo');
  const faq = p.mk('https://mindsync.app/faq', '', 'w-richtext');
  const other = p.mk('/journal/other-post');
  const ext = p.mk('https://example.com/features');
  p.run(); p.fire('DOMContentLoaded'); p.load();
  assert.strictEqual(card.attrs.href, 'https://mindsync.app/features', 'no rewrite before interaction (crawlers)');
  [card, nav, logo, faq, other, ext].forEach(a => p.click(a));
  assert.strictEqual(card.attrs.href, 'https://mindsync.app/features?from=blog-abc');
  assert.strictEqual(nav.attrs.href, 'https://www.mindsync.app/features?from=blog-abc');
  assert.strictEqual(logo.attrs.href, 'https://www.mindsync.app/?from=blog-abc');
  assert.strictEqual(faq.attrs.href, 'https://mindsync.app/faq');
  assert.strictEqual(other.attrs.href, '/journal/other-post');
  assert.strictEqual(ext.attrs.href, 'https://example.com/features');
  p.click(card);
  assert.strictEqual((card.attrs.href.match(/from=/g) || []).length, 1);
  assert.strictEqual(blogEvents(p).length, 0, 'hub clicks are not store clicks');
});

t('/features?from=blog-<slug>: store links tagged with medium=card, event fires', () => {
  const p = page('https://www.mindsync.app/features?from=blog-therapy-hangover', { readyState: 'complete', consent: true });
  const g = p.mk(PLAY, 'msf-btn'); const a = p.mk(APPLE, 'msf-btn'); const home = p.mk('/', 'logo');
  p.run();
  assert.strictEqual(q(g, 'referrer'), 'utm_source=blog&utm_medium=card&utm_campaign=therapy-hangover');
  assert.strictEqual(q(a, 'ct'), 'blog-therapy-hangover');
  p.click(home); assert.strictEqual(home.attrs.href, '/', 'no hub rewrite off-post');
  p.click(g);
  assert.deepStrictEqual(blogEvents(p)[0],
    ['blog_store_click', { store: 'google', blog_slug: 'therapy-hangover', medium: 'card', page_path: '/features' }]);
});

t('no slug (no from, bad from, bad journal slug, /blog): nothing touched, no event', () => {
  for (const u of ['https://www.mindsync.app/features', 'https://www.mindsync.app/features?from=blog-X!',
    'https://www.mindsync.app/?from=newsletter-abc', 'https://www.mindsync.app/journal/%3Cscript%3E',
    'https://www.mindsync.app/blog', 'https://www.mindsync.app/journal/']) {
    const p = page(u, { readyState: 'complete', consent: true });
    const g = p.mk(PLAY); const c = p.mk('/features'); p.run(); p.load(); p.click(g); p.click(c);
    assert.strictEqual(g.attrs.href, PLAY, u); assert.strictEqual(c.attrs.href, '/features', u);
    assert.strictEqual(blogEvents(p).length, 0, u);
  }
});

t('consent: event only with posthog && __msA; app_store_click not duplicated; never identify', () => {
  const p = page('https://www.mindsync.app/journal/abc', { consent: true });
  const g = p.mk(PLAY, '', 'blog-cta-buttons'); const a = p.mk(APPLE, '', 'w-richtext');
  p.run(); p.fire('DOMContentLoaded'); p.click(g); p.click(a);
  const app = p.captured.filter(c => c[0] === 'app_store_click');
  assert.strictEqual(blogEvents(p).length, 2); assert.strictEqual(app.length, 2);
  assert.deepStrictEqual(blogEvents(p)[1][1], { store: 'apple', blog_slug: 'abc', medium: 'inline', page_path: '/journal/abc' });
  assert.deepStrictEqual(p.calls, []);
  const p2 = page('https://www.mindsync.app/journal/abc', { consent: false });
  const g2 = p2.mk(PLAY, '', 'blog-cta-buttons'); p2.run(); p2.fire('DOMContentLoaded'); p2.click(g2);
  assert.strictEqual(p2.captured.length, 0);
  assert.ok(g2.attrs.href.includes('referrer='), 'href still decorated without consent (URL param only, nothing sent)');
  const p3 = page('https://www.mindsync.app/journal/abc', { consent: true, noPosthog: true });
  const g3 = p3.mk(PLAY); p3.run(); p3.fire('DOMContentLoaded'); p3.click(g3); // must not throw
});

t('late links: picked up by load rescan, and lazily on click', () => {
  const p = page('https://www.mindsync.app/journal/abc', { consent: true });
  p.run(); p.fire('DOMContentLoaded');
  const late = p.mk(PLAY, '', 'blog-cta-buttons'); p.load();
  assert.ok(q(late, 'referrer').includes('utm_medium=badge'));
  const later = p.mk(APPLE, '', 'w-richtext'); p.click(later);
  assert.strictEqual(q(later, 'ct'), 'blog-abc');
  assert.ok(blogEvents(p).some(c => c[1].store === 'apple' && c[1].medium === 'inline'));
});

t('ct truncated to 40 chars; pt only when APPLE_PROVIDER_TOKEN set, existing pt kept', () => {
  const long = 'a-very-long-slug-about-therapy-homework-and-journaling-between-sessions';
  const p = page('https://www.mindsync.app/journal/' + long);
  const a = p.mk(APPLE); p.run(); p.fire('DOMContentLoaded');
  assert.strictEqual(q(a, 'ct'), ('blog-' + long).slice(0, 40));
  assert.strictEqual(q(a, 'ct').length, 40);
  const src = MIN ? SRC.replace(/T='\d*'/, "T='123456'") : SRC.replace(/APPLE_PROVIDER_TOKEN='\d*'/, "APPLE_PROVIDER_TOKEN='123456'");
  assert.notStrictEqual(src, SRC);
  const p2 = page('https://www.mindsync.app/journal/abc', { src });
  const a2 = p2.mk(APPLE); const a3 = p2.mk(APPLE + '?pt=999'); p2.run(); p2.fire('DOMContentLoaded');
  assert.strictEqual(q(a2, 'pt'), '123456'); assert.strictEqual(q(a3, 'pt'), '999');
});

t('non-MindSync store links are ignored', () => {
  const p = page('https://www.mindsync.app/journal/abc');
  const otherApp = p.mk('https://play.google.com/store/apps/details?id=com.other.app');
  const otherIos = p.mk('https://apps.apple.com/us/app/x/id123');
  p.run(); p.fire('DOMContentLoaded');
  assert.strictEqual(q(otherApp, 'referrer'), null); assert.strictEqual(q(otherIos, 'ct'), null);
});

t('static constraints: size < 3 KB, no storage/cookies/identify, no long dashes', () => {
  // full build < 3 KB; min build must fit the Webflow inline registered-script limit (2000 chars)
  assert.ok(Buffer.byteLength(SRC) < (MIN ? 2000 : 3072), 'size ' + Buffer.byteLength(SRC));
  const code = SRC.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/.*$/gm, '');
  assert.ok(!/cookie|localStorage|sessionStorage|identify|fbq/i.test(code));
  for (const f of ['blog-attribution.js', 'blog-attribution.min.js', 'README.md', 'test.js', 'test.html']) {
    const p = path.join(__dirname, f);
    if (fs.existsSync(p)) assert.ok(![...fs.readFileSync(p, 'utf8')].some(ch => ch.charCodeAt(0) === 0x2013 || ch.charCodeAt(0) === 0x2014), f);
  }
});

console.log('ALL ' + n + ' TESTS PASSED (' + FILE + '), size ' + Buffer.byteLength(SRC) + ' B');
