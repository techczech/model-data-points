// Citation-only adapter of the web-design-elements copy module v1 (plain JavaScript).
function legacyCopy(text) {
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.setAttribute('readonly', '');
  ta.style.position = 'fixed';
  ta.style.opacity = '0';
  document.body.appendChild(ta);
  ta.select();
  let ok = false;
  try { ok = document.execCommand('copy'); } catch { /* no clipboard available */ }
  ta.remove();
  return ok;
}

async function copyText(text) {
  try { await navigator.clipboard.writeText(text); return true; }
  catch { return legacyCopy(text); }
}

document.addEventListener('click', async (event) => {
  const button = event.target.closest('.cite [data-copy]');
  if (!button || button.dataset.copyState) return;
  const ref = button.dataset.copy || '';
  const text = ref.startsWith('#') ? document.querySelector(ref)?.textContent?.trim() || '' : ref;
  button.dataset.copyState = 'pending';
  const ok = text !== '' && await copyText(text);
  const kept = Array.from(button.childNodes);
  button.replaceChildren(ok ? 'Copied' : 'Copy failed');
  button.dataset.copyState = ok ? 'copied' : 'failed';
  button.classList.add(ok ? 'copied' : 'copy-failed');
  const status = document.querySelector('#copy-status');
  if (status) status.textContent = ok ? 'Citation copied.' : 'Copy failed: select the text and copy it by hand.';
  window.setTimeout(() => {
    button.replaceChildren(...kept);
    button.classList.remove('copied', 'copy-failed');
    delete button.dataset.copyState;
    if (status) status.textContent = '';
  }, ok ? 1600 : 3000);
});
