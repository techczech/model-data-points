// Client-side filtering of the entry list; entries stay in the HTML so the page works without JS.
const cards = [...document.querySelectorAll('.list .card')];
const val = (id) => document.getElementById(id).value;
function apply() {
  const t = val('f-type'), m = val('f-model'), o = val('f-open'), y = val('f-year');
  let n = 0;
  cards.forEach((c) => {
    const ok = (!t || c.dataset.type === t)
      && (!m || c.dataset.models.split('|').includes(m))
      && (!o || c.dataset.open.split(' ').includes(o))
      && (!y || c.dataset.date.startsWith(y));
    c.style.display = ok ? '' : 'none';
    if (ok) n++;
  });
  document.getElementById('count').textContent = n + ' of ' + cards.length + ' entries shown (newest first)';
}
document.querySelectorAll('#filters select').forEach((s) => (s.onchange = apply));
apply();
