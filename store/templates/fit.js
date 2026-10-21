// MindSync store screenshots: text fitting before the screenshot (render_store.py waits for
// window.__ready). Copy lines are forced (.ln, nowrap), so a line that is too wide shrinks the whole
// block instead of wrapping. Steps of 1%, floor 60%. Result in window.__ready:
//   font_ok      Figtree loaded (otherwise a fallback font was used)
//   scales       final text scale per block (1 = design size)
//   overflow     blocks that still do not fit at the floor
//   text_share   share of the image covered by headline + subtitle line boxes (Play guideline: <= 0.20)
//   decor_clash  optional decor that comes too close to the text or the phone (empty without decor)
//   error        exception message, if any
(function () {
  'use strict';
  var out = { font_ok: true, scales: {}, overflow: [], text_share: 0 };

  function widestLine(el) {
    var m = 0, tx = el.querySelectorAll('.tx');
    for (var i = 0; i < tx.length; i++) m = Math.max(m, tx[i].getBoundingClientRect().width);
    return m;
  }
  function boxWidth(el) {
    var cs = getComputedStyle(el);
    return el.clientWidth - parseFloat(cs.paddingLeft || 0) - parseFloat(cs.paddingRight || 0);
  }
  // Shrinks CSS variable `name` on `el` until every forced line fits the width of `el`
  // and, when given, `fitsHeight()` returns true.
  function fit(el, name, fitsHeight) {
    var s = 1;
    el.style.setProperty(name, String(s));
    function ok() {
      return widestLine(el) <= boxWidth(el) + 0.5 && (!fitsHeight || fitsHeight());
    }
    var guard = 0;
    while (!ok() && s > 0.6 && guard++ < 60) {
      s = Math.round((s - 0.01) * 100) / 100;
      el.style.setProperty(name, String(s));
    }
    return { s: s, ok: ok() };
  }

  // line boxes of the text nodes in `el`, merged per row (avoids counting block boxes)
  function textArea(el) {
    var rows = textRows(el), a = 0;
    for (var k = 0; k < rows.length; k++) a += (rows[k].r - rows[k].l) * rows[k].h;
    return a;
  }
  function textRows(el) {
    if (!el || !el.textContent.trim()) return [];
    var rows = [], tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null), n;
    while ((n = tw.nextNode())) {
      if (!n.nodeValue.trim()) continue;
      var r = document.createRange();
      r.selectNodeContents(n);
      var rects = r.getClientRects();
      for (var i = 0; i < rects.length; i++) {
        var b = rects[i];
        if (b.width < 1 || b.height < 1) continue;
        var cy = b.top + b.height / 2, hit = null;
        for (var j = 0; j < rows.length; j++) {
          if (Math.abs(rows[j].cy - cy) < b.height / 2) { hit = rows[j]; break; }
        }
        if (hit) {
          hit.l = Math.min(hit.l, b.left); hit.r = Math.max(hit.r, b.right); hit.h = Math.max(hit.h, b.height);
        } else {
          rows.push({ cy: cy, l: b.left, r: b.right, h: b.height });
        }
      }
    }
    return rows;
  }

  // Optional background decor: the bird must keep a clear margin from every text row and from the
  // phone; the wave may pass behind the phone but must stay clear of the text.
  function decorClash() {
    var layer = document.getElementById('decor');
    if (!layer) return [];
    var gap = window.innerWidth * 0.03, out = [], blocks = [];
    var rows = textRows(document.getElementById('hl')).map(function (r) { return ['headline', r]; })
      .concat(textRows(document.getElementById('sub')).map(function (r) { return ['subtitle', r]; }));
    rows.forEach(function (x) {
      var r = x[1];
      blocks.push([x[0], { left: r.l, right: r.r, top: r.cy - r.h / 2, bottom: r.cy + r.h / 2 }]);
    });
    var phone = document.getElementById('phone').getBoundingClientRect();
    function near(a, b) {
      return a.left < b.right + gap && a.right > b.left - gap && a.top < b.bottom + gap && a.bottom > b.top - gap;
    }
    var bird = layer.querySelector('.bird'), wave = layer.querySelector('.wave');
    if (bird) {
      var bb = bird.getBoundingClientRect();
      blocks.forEach(function (b) {
        if (near(bb, b[1]) && out.indexOf('bird near ' + b[0]) < 0) out.push('bird near ' + b[0]);
      });
      if (near(bb, phone)) out.push('bird near the phone');
    }
    if (wave) {
      var wb = wave.getBoundingClientRect();
      blocks.forEach(function (b) {
        if (near(wb, b[1]) && out.indexOf('wave near ' + b[0]) < 0) out.push('wave near ' + b[0]);
      });
    }
    return out;
  }

  function layoutScreen() {
    var hl = document.getElementById('hl');
    var r = fit(hl, '--hl-s');
    out.scales.headline = r.s;
    if (!r.ok) out.overflow.push('headline');
    var sub = document.getElementById('sub'), zone = document.getElementById('subzone');
    if (sub && sub.textContent.trim()) {
      r = fit(sub, '--sub-s', function () {
        return sub.getBoundingClientRect().height <= zone.clientHeight + 0.5;
      });
      out.scales.subtitle = r.s;
      if (!r.ok) out.overflow.push('subtitle');
    }
    out.text_share = (textArea(hl) + textArea(sub)) / (window.innerWidth * window.innerHeight);
    out.decor_clash = decorClash();
  }

  function layoutTestimonial() {
    var col = document.getElementById('tcol'), quote = document.getElementById('quote');
    var stars = document.getElementById('stars'), il = document.getElementById('illus');
    var last = (stars && stars.children.length) ? stars : quote;
    var r = fit(col, '--t-s', function () {
      var b = il.getBoundingClientRect();
      var limit = b.top + b.height * parseFloat(il.getAttribute('data-safe') || '0.16') - 20;
      return last.getBoundingClientRect().bottom <= limit;
    });
    out.scales.quote = r.s;
    if (!r.ok) out.overflow.push('quote');
  }

  function run() {
    try {
      out.font_ok = document.fonts.check('700 64px "Figtree"') && document.fonts.check('400 36px "Figtree"');
    } catch (e) { out.font_ok = false; }
    try {
      if (document.body.classList.contains('testimonial-slide')) layoutTestimonial();
      else layoutScreen();
    } catch (e) {
      out.error = String((e && e.message) || e);
    }
    window.__ready = out;
  }

  function start() {
    var waits = [];
    if (document.fonts && document.fonts.load) {
      ['400', '500', '600', '700'].forEach(function (w) {
        waits.push(document.fonts.load(w + ' 40px "Figtree"'));
      });
    }
    for (var i = 0; i < document.images.length; i++) {
      var img = document.images[i];
      if (img.decode) waits.push(img.decode().catch(function () {}));
    }
    Promise.all(waits)
      .then(function () { return document.fonts ? document.fonts.ready : null; })
      .then(run, run);
  }

  if (document.readyState === 'complete') start();
  else window.addEventListener('load', start);
})();
