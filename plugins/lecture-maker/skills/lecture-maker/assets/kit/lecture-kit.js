/* ═══════════════════════════════════════════════════════════════
   LECTURE KIT · shared runtime. build.py puts it before the slides' own scripts.
   The engine calls window.sceneFx(slide, step) on every beat (also when a slide opens
   at beat 0, and when you step back into a slide at its last beat). This answers it:
     1. beat classes on the slide: data-beat="N" and .b1 … .bN
     2. data-shrink-at / data-out / data-gone → .shrunk / .lm-out
     3. the topic strip along the top, from data-topic on each section
     4. the slide's own scene, if it registered one:
          LM.scene('s03', function(slide, step){ … });
   A scene must draw the state of `step` whichever way you arrived. Nothing loops;
   no timer outlives the slide.
   ═══════════════════════════════════════════════════════════════ */
(function(){
const deck = document.getElementById('deck');
const slides = [...deck.querySelectorAll('.slide')];

/* ---------- topic strip: the topics in deck order ---------- */
const topics = [];
slides.forEach(s => { const t = s.dataset.topic; if(t && !topics.includes(t)) topics.push(t); });
const strip = document.createElement('div');
strip.id = 'topics';
strip.setAttribute('aria-hidden', 'true');
strip.innerHTML = topics.map(t => '<b>' + t.replace(/</g, '&lt;') + '</b>').join('');
if(topics.length) deck.insertBefore(strip, deck.querySelector('.slide'));
const items = [...strip.children];

function topicStrip(sl){
  const t = sl.dataset.topic;
  const k = t ? topics.indexOf(t) : -1;
  strip.classList.toggle('on', k >= 0 && sl.dataset.strip !== 'none');
  items.forEach((it, n) => {
    it.classList.toggle('past', k >= 0 && n < k);
    it.classList.toggle('now', n === k);
  });
}

const scenes = {};
window.LM = { scene(id, fn){ scenes[id] = fn; }, deck, topics };

window.sceneFx = function(sl, step){
  sl.dataset.beat = step;
  for(let k = 1; k <= 12; k++) sl.classList.toggle('b' + k, k <= step);
  sl.querySelectorAll('[data-shrink-at]').forEach(e => e.classList.toggle('shrunk', step >= +e.dataset.shrinkAt));
  sl.querySelectorAll('[data-out]').forEach(e => e.classList.toggle('lm-out', step >= +e.dataset.out));
  sl.querySelectorAll('[data-gone]').forEach(e => e.classList.toggle('lm-out', step >= +e.dataset.gone));
  topicStrip(sl);
  const fn = scenes[sl.dataset.s];
  if(fn){ try{ fn(sl, step); }catch(e){ console.error('scene ' + sl.dataset.s, e); } }
};
})();
