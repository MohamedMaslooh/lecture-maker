/* ═══════════════════════════════════════════════════════════════
   SLIDE NAVIGATOR · self-contained, drop-in (pair: deck-nav.css).
   From Lecture 4's source/js/00-nav.js (5 Oct 2026); build.py puts it in every deck instead of the engine's older copy.
   Same navigator as the lecture site (maslooh.com, My Page/scripts/deck-nav), with one change for presenting:
   it is HIDDEN until asked for, so it never covers a slide during the talk.

     mouse to the right edge   a slim ladder of ticks appears (one per slide, the current one lit)
     hover the ladder          the panel of slide thumbnails slides in; it folds away when the mouse leaves
     click the ladder or G     the panel opens and stays (pinned); G, Esc, the X or a click outside closes it
     hover a thumbnail         a large preview beside the panel (desktop)
     click a thumbnail         jump to that slide, at its first beat
     keys while open           Up/Down (or Left/Right) move the highlight, digits type a number ("1" "0"),
                               Enter jumps; nothing reaches the deck while the panel is open
     touch                     a touch shows the ladder for 4 s; tap it to open, tap a slide, tap outside or
                               swipe right to close

   Contract with the deck engine (the animated-html-deck engine, and any engine like it):
     #deck holds the slides as .slide; the current one has .on; beats are [data-step] that get .show.
     Slides change ONLY through the engine's own keys (Home, then ArrowRight), so beats, scenes (sceneFx), the
     topic strip, counters and the progress bar update exactly as with the keyboard.
   Thumbnails: window.DNAV.thumbs (before this file) = {data-s or id or 1-based number: image URL}, or an array
     in slide order; real renders, light. A slide without one gets a live mini copy (a DOM clone, every beat
     shown, no video/script/id), as on the website.
   Other options in window.DNAV: theme 'light'|'dark', accent '#hex', key 'g', edge px (hover band, 28).
   Hidden on the turned phone board (body.rot) and in print. Leaves room for a right-hand column whose width is
     in the CSS variable --nres on <html> (unused in this skill; 0 by default).
   ═══════════════════════════════════════════════════════════════ */
(function(){
  var deck = document.getElementById('deck'); if(!deck) return;
  var slides = [].slice.call(deck.querySelectorAll('.slide')), N = slides.length; if(!N) return;
  if(document.querySelector('.dnav')) return;
  var cfg = window.DNAV || {};
  var KEY = (cfg.key || 'g').toLowerCase(), EDGE = cfg.edge || 28;
  var body = document.body, docEl = document.documentElement;
  var shell = slides[0].parentElement;
  var wrapCls = (shell && shell !== deck) ? shell.className : '';
  var CAN_HOVER = matchMedia('(hover:hover) and (pointer:fine)').matches;

  function el(tag, cls, html){ var e = document.createElement(tag); if(cls) e.className = cls; if(html != null) e.innerHTML = html; return e; }
  var root = el('div', 'dnav');

  /* ---- colours from the deck's own tokens, unless window.DNAV fixes them ---- */
  (function(){
    var cs = getComputedStyle(slides[0]), cv = document.createElement('canvas').getContext('2d');
    function rgb(s){ if(!s || !cv) return null; cv.fillStyle = '#010203'; cv.fillStyle = s; var v = cv.fillStyle;
      if(v === '#010203' && s.replace(/\s/g, '') !== '#010203') return null;
      var m = v.match(/^#(..)(..)(..)$/); if(m) return [parseInt(m[1], 16), parseInt(m[2], 16), parseInt(m[3], 16)];
      m = v.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?/); return m && (m[4] == null || +m[4] > .5) ? [+m[1], +m[2], +m[3]] : null; }
    function lum(c){ return (0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]) / 255; }
    var theme = cfg.theme;
    if(!theme){
      var page = rgb(cs.getPropertyValue('--page').trim()) || rgb(getComputedStyle(body).backgroundColor) || [255, 255, 255];
      theme = lum(page) < .45 ? 'dark' : 'light';
    }
    root.setAttribute('data-theme', theme);
    var acc = cfg.accent || (cfg.theme ? '' : cs.getPropertyValue('--accent').trim());
    var ac = rgb(acc);
    if(ac && (theme === 'light' ? lum(ac) < .7 : lum(ac) > .35)) root.style.setProperty('--n-accent', acc);
    var font = cfg.theme ? '' : cs.getPropertyValue('--sans').trim();
    if(font) root.style.setProperty('--n-font', font);
  })();

  /* ---- thumbnails given by the deck (real renders), by data-s, id, number or position ---- */
  var given = cfg.thumbs || {};
  function thumbSrc(k){
    var s = slides[k];
    if(Array.isArray(given)) return given[k] || null;
    return given[s.dataset.s] || (s.id && given[s.id]) || given[k + 1] || given[String(k + 1).padStart(2, '0')] || null;
  }

  var handle = el('button', 'dnav-h'); handle.type = 'button';
  handle.setAttribute('aria-label', 'Slides (' + KEY.toUpperCase() + ')'); handle.setAttribute('aria-expanded', 'false');
  var ticks = [];
  for(var k = 0; k < N; k++){ var t = el('i'); handle.appendChild(t); ticks.push(t); }
  var panel = el('aside', 'dnav-p'); panel.setAttribute('aria-label', 'Slides');
  var head = el('div', 'dnav-hd', '<b>Slides</b><span class="dnav-ct"></span><span class="dnav-ky">' + KEY.toUpperCase() + '</span>');
  var closeB = el('button', 'dnav-x', '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>');
  closeB.type = 'button'; closeB.setAttribute('aria-label', 'Close');
  head.appendChild(closeB);
  var list = el('div', 'dnav-l');
  var preview = el('div', 'dnav-pv'); var pvFrame = el('div', 'dnav-fr-box'); preview.appendChild(pvFrame); preview.appendChild(el('span', 'dnav-pn'));
  panel.appendChild(head); panel.appendChild(list);
  root.appendChild(handle); root.appendChild(panel); root.appendChild(preview);
  body.appendChild(root);

  var items = [], cur = 0, openState = 0 /* 0 closed, 1 hover, 2 pinned */, busy = false, built = {}, pvBuilt = {}, sel = -1, typed = '', typedT = null;
  for(var n = 0; n < N; n++) (function(n){
    var it = el('div', 'dnav-i'); it.setAttribute('role', 'button'); it.setAttribute('aria-label', 'Slide ' + (n + 1));
    var num = el('span', 'dnav-n', String(n + 1)); var box = el('div', 'dnav-th'); it.appendChild(num); it.appendChild(box);
    it._box = box; it._n = n; list.appendChild(it); items.push(it);
    it.addEventListener('click', function(e){ e.stopPropagation(); goto(n); });
    it.addEventListener('pointerenter', function(e){ if(e.pointerType === 'mouse'){ select(n, false); showPreview(n, it); } });
    it.addEventListener('pointerleave', function(e){ if(e.pointerType === 'mouse') hidePreview(); });
  })(n);
  head.querySelector('.dnav-ct').textContent = N;

  /* ---- a live mini copy: the slide cloned with every beat on, scaled by CSS ---- */
  function clone(k){
    var c = slides[k].cloneNode(true);
    [].forEach.call(c.querySelectorAll('video,audio,script,iframe,source,object'), function(x){ x.remove(); });
    [].forEach.call(c.querySelectorAll('[id]'), function(x){ x.removeAttribute('id'); }); c.removeAttribute('id');
    c.classList.remove('past'); c.classList.add('on');
    [].forEach.call(c.querySelectorAll('[data-step]'), function(x){ x.classList.add('show'); });
    if(c.dataset.act1) c.classList.add('act1');
    [].forEach.call(c.querySelectorAll('[data-count]'), function(x){
      var to = +x.dataset.count, dec = x.dataset.dec ? +x.dataset.dec : 0, suf = x.dataset.suf || '', v = dec ? to.toFixed(dec) : String(Math.round(to));
      if(x.dataset.comma !== undefined) v = (+v).toLocaleString('en-US');
      x.innerHTML = v + (suf ? '<small>' + suf + '</small>' : '');
    });
    [].forEach.call(c.querySelectorAll('[data-flip]'), function(x){ x.removeAttribute('data-flip'); });
    var w = el('div', wrapCls); w.style.display = 'contents'; w.appendChild(c);
    var fr = el('div', 'dnav-fr'); fr.appendChild(w); return fr;
  }
  function picture(k){
    var src = thumbSrc(k);
    if(!src) return clone(k);
    var im = el('img', 'dnav-img'); im.alt = ''; im.decoding = 'async'; im.draggable = false; im.src = src; return im;
  }
  function fill(it){
    if(built[it._n]) return; built[it._n] = 1;
    it._box.appendChild(picture(it._n));
  }
  var io = ('IntersectionObserver' in window) ? new IntersectionObserver(function(es){
    es.forEach(function(e){ if(e.isIntersecting){ fill(e.target); io.unobserve(e.target); } });
  }, {root: list, rootMargin: '200px 0px'}) : null;

  function sizes(){
    var w = items[0]._box.clientWidth || 210;
    panel.style.setProperty('--k', (w / 1280).toFixed(5));
  }
  function reserved(){ return parseFloat(getComputedStyle(docEl).getPropertyValue('--nres')) || 0; }

  /* ---- the large preview beside the panel (desktop) ---- */
  var pvT = null;
  function showPreview(n, it){
    if(!CAN_HOVER || innerWidth < 900) return;
    clearTimeout(pvT);
    pvT = setTimeout(function(){
      if(!openState) return;
      if(!pvBuilt[n]){ var f = picture(n); f.classList.add('big'); pvBuilt[n] = f; }
      pvFrame.textContent = ''; pvFrame.appendChild(pvBuilt[n]);
      preview.querySelector('.dnav-pn').textContent = String(n + 1) + ' / ' + N;
      var right = reserved() + panel.offsetWidth + 14;
      var pw = Math.min(480, innerWidth - right - 26), ph = pw * 9 / 16;
      preview.style.width = pw + 'px'; preview.style.setProperty('--pk', (pw / 1280).toFixed(5));
      var r = it.getBoundingClientRect(), top = r.top + r.height / 2 - ph / 2;
      top = Math.max(12, Math.min(innerHeight - ph - 12, top));
      preview.style.top = top + 'px'; preview.style.right = right + 'px';
      preview.classList.add('vis');
    }, 90);
  }
  function hidePreview(){ clearTimeout(pvT); pvT = setTimeout(function(){ preview.classList.remove('vis'); }, 60); }

  /* ---- hidden until asked: the ladder peeks only when the pointer reaches the edge ---- */
  var peekT = null;
  function peek(on, ms){
    clearTimeout(peekT);
    root.classList.toggle('peek', !!on);
    if(on && ms) peekT = setTimeout(function(){ if(!openState) root.classList.remove('peek'); }, ms);
  }
  addEventListener('mousemove', function(e){
    if(openState) return;
    var edge = innerWidth - reserved();
    var near = e.clientX >= edge - EDGE && e.clientX <= edge + 2;
    if(near) peek(true);
    else if(root.classList.contains('peek') && !root.contains(e.target)){ clearTimeout(peekT); peekT = setTimeout(function(){ if(!openState) root.classList.remove('peek'); }, 500); }
  });
  document.addEventListener('mouseleave', function(){ if(!openState) peek(false); });

  /* ---- open / close ---- */
  var closeT = null;
  function setOpen(state){
    clearTimeout(closeT);
    var was = openState; openState = state;
    root.classList.toggle('open', !!state);
    if(state) peek(true); else peek(false);
    handle.setAttribute('aria-expanded', state ? 'true' : 'false');
    if(state && !was){
      sizes(); mark(true); select(cur, false);
      items.forEach(function(it){ if(io){ if(!built[it._n]) io.observe(it); } else fill(it); });
    }
    if(!state){ preview.classList.remove('vis'); typed = ''; }
  }
  function leaveSoon(){ if(openState !== 1) return; clearTimeout(closeT); closeT = setTimeout(function(){ if(openState === 1) setOpen(0); }, 380); }
  function stay(){ clearTimeout(closeT); }
  handle.addEventListener('pointerenter', function(e){ if(e.pointerType === 'mouse' && !openState) setOpen(1); else stay(); });
  [handle, panel, preview].forEach(function(x){
    x.addEventListener('pointerenter', function(e){ if(e.pointerType === 'mouse') stay(); });
    x.addEventListener('pointerleave', function(e){ if(e.pointerType === 'mouse') leaveSoon(); });
  });
  handle.addEventListener('click', function(e){ e.stopPropagation(); handle.blur(); setOpen(openState === 2 ? 0 : 2); });
  closeB.addEventListener('click', function(e){ e.stopPropagation(); setOpen(0); });
  /* the handle, the panel and the preview are never part of a page turn */
  ['click', 'dblclick', 'mousedown', 'keyup'].forEach(function(ev){ root.addEventListener(ev, function(e){ e.stopPropagation(); }); });

  /* a click outside closes the panel and does nothing else */
  window.addEventListener('click', function(e){
    if(!openState || root.contains(e.target)) return;
    e.stopPropagation(); e.preventDefault(); setOpen(0);
  }, true);

  /* touch: a touch shows the ladder for a moment; our own gestures never reach the deck's swipe / tap handlers */
  var tx = 0, ty = 0, tIn = false, tOut = false;
  window.addEventListener('touchstart', function(e){
    var inside = root.contains(e.target); tIn = inside; tOut = !inside && !!openState;
    if(!inside && !openState) peek(true, 4000);
    if(inside || tOut){ e.stopPropagation(); var t = e.changedTouches[0]; tx = t.clientX; ty = t.clientY; }
  }, {capture: true, passive: true});
  window.addEventListener('touchend', function(e){
    if(tIn){
      e.stopPropagation();
      var t = e.changedTouches[0], dx = t.clientX - tx, dy = t.clientY - ty;
      if(dx > 60 && dx > Math.abs(dy) * 1.4 && openState){ setOpen(0); if(e.cancelable) e.preventDefault(); }
      tIn = false;
    } else if(tOut){
      e.stopPropagation(); if(e.cancelable) e.preventDefault(); setOpen(0); tOut = false;
    }
  }, {capture: true, passive: false});
  window.addEventListener('touchcancel', function(e){ if(tIn || tOut) e.stopPropagation(); tIn = tOut = false; }, {capture: true, passive: true});

  /* ---- keys: G opens and closes; while open, the panel owns the keyboard ---- */
  function select(n, scroll){
    sel = Math.max(0, Math.min(N - 1, n));
    items.forEach(function(it, k){ it.classList.toggle('sel', k === sel); });
    if(scroll && openState){ var it = items[sel], r = it.getBoundingClientRect(), lr = list.getBoundingClientRect();
      if(r.top < lr.top || r.bottom > lr.bottom) it.scrollIntoView({block: 'nearest'}); }
  }
  window.addEventListener('keydown', function(e){
    if(busy || hidden()) return;
    if(e.ctrlKey || e.metaKey || e.altKey) return;
    var k = e.key, low = k.toLowerCase();
    if(!openState){
      if(low === KEY){ e.preventDefault(); e.stopPropagation(); setOpen(2); }
      return;
    }
    /* open: nothing below turns a page */
    e.preventDefault(); e.stopPropagation();
    if(low === KEY || k === 'Escape'){ setOpen(0); return; }
    if(k === 'ArrowDown' || k === 'ArrowRight' || k === 'PageDown'){ typed = ''; select(sel + 1, true); }
    else if(k === 'ArrowUp' || k === 'ArrowLeft' || k === 'PageUp'){ typed = ''; select(sel - 1, true); }
    else if(k === 'Home'){ select(0, true); }
    else if(k === 'End'){ select(N - 1, true); }
    else if(/^[0-9]$/.test(k)){
      typed = (typed + k).slice(-3); clearTimeout(typedT); typedT = setTimeout(function(){ typed = ''; }, 1600);
      var v = parseInt(typed, 10); if(v >= 1 && v <= N) select(v - 1, true);
    }
    else if(k === 'Enter' || k === ' '){ goto(sel); }
  }, true);

  /* ---- which slide is on ---- */
  function readCur(){
    for(var k = 0; k < N; k++) if(slides[k].classList.contains('on')) return k;
    return cur;
  }
  function mark(scroll){
    cur = readCur();
    ticks.forEach(function(t, k){ t.classList.toggle('on', k === cur); });
    items.forEach(function(it, k){ it.classList.toggle('on', k === cur); });
    if(scroll && openState){
      var it = items[cur], top = it.offsetTop - (list.clientHeight - it.offsetHeight) / 2;
      list.scrollTop = Math.max(0, top);
    }
  }
  new MutationObserver(function(ms){
    for(var m = 0; m < ms.length; m++) if(ms[m].target.classList && ms[m].target.classList.contains('slide')){ if(readCur() !== cur) mark(false); return; }
  }).observe(deck, {attributes: true, attributeFilter: ['class'], subtree: true});
  new MutationObserver(function(){ if(hidden()) setOpen(0); }).observe(body, {attributes: true, attributeFilter: ['class']});
  function hidden(){ return body.classList.contains('rot'); }

  /* ---- go to a slide, at its first beat, by the engine's own keys ---- */
  function key(k){ window.dispatchEvent(new KeyboardEvent('keydown', {key: k, bubbles: true, cancelable: true})); }
  function atStart(k){ var s = slides[k]; return !s.querySelector('[data-step].show') && !s.classList.contains('act1'); }
  function goto(n){
    setOpen(0);
    cur = readCur();
    busy = true;
    try{
      if(n < cur || (n === cur && !atStart(n))) key('Home');
      var guard = 0;
      while(!slides[n].classList.contains('on') && guard++ < 1000) key('ArrowRight');
    } finally { busy = false; }
    mark(false);
  }
  window.__dnav = {goto: goto, open: function(s){ setOpen(s || 2); }, close: function(){ setOpen(0); }, count: N};

  /* ---- ladder spacing follows the window height ---- */
  function layout(){
    var avail = Math.min(innerHeight * 0.62, 360), gap = Math.max(2, Math.min(7, (avail - N * 2) / Math.max(1, N - 1)));
    handle.style.setProperty('--g', gap.toFixed(1) + 'px');
    if(openState) sizes();
  }
  addEventListener('resize', layout); layout(); mark(false);
})();
