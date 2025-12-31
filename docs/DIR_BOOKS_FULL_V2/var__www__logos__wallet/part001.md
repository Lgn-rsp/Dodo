# FULL SOURCE — `/var/www/logos/wallet`

**No truncation.** Full file contents inside code fences.


---

## FILE: `/var/www/logos/wallet/app.html`

```html
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Wallet — Кошелёк</title>
  <style>
    body{font-family:system-ui,Segoe UI,Roboto,Arial,sans-serif;margin:0;background:#0b0c10;color:#e6edf3}
    header{padding:16px 20px;background:#11151a;border-bottom:1px solid #1e242c;position:sticky;top:0}
    h1{font-size:18px;margin:0}
    main{max-width:1024px;margin:24px auto;padding:0 16px}
    section{background:#11151a;margin:16px 0;border-radius:12px;padding:16px;border:1px solid #1e242c}
    label{display:block;margin:8px 0 6px}
    .grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
    @media (max-width:900px){.grid{grid-template-columns:1fr}}
    input,button,textarea{width:100%;padding:10px;border-radius:10px;border:1px solid #2a313a;background:#0b0f14;color:#e6edf3}
    button{cursor:pointer;border:1px solid #3b7ddd;background:#1665c1}
    button.secondary{background:#1b2129}
    .mono{font-family:ui-monospace,Menlo,Consolas,monospace}
    small{opacity:.8}
  </style>
</head>
<body>
<header>
  <h1>LOGOS Wallet — Кошелёк</h1>
</header>
<main>
  <section>
    <div class="grid">
      <div>
        <h3>Твой RID / Публичный ключ</h3>
        <textarea id="pub" class="mono" rows="4" readonly></textarea>
        <div style="display:flex;gap:10px;margin-top:10px">
          <button id="btn-lock" class="secondary">Выйти (заблокировать)</button>
          <button id="btn-nonce" class="secondary">Получить nonce</button>
        </div>
        <p><small>Ключ в памяти. Закроешь вкладку — понадобится пароль на странице входа.</small></p>
      </div>
      <div>
        <h3>Баланс</h3>
        <div class="grid">
          <div><label>RID</label><input id="rid-balance" class="mono" placeholder="RID (base58)"/></div>
          <div><label>&nbsp;</label><button id="btn-balance">Показать баланс</button></div>
        </div>
        <pre id="out-balance" class="mono" style="margin-top:12px"></pre>
      </div>
    </div>
  </section>

  <section>
    <h3>Подпись и отправка (batch)</h3>
    <div class="grid">
      <div><label>Получатель (RID)</label><input id="to" class="mono" placeholder="RID получателя"/></div>
      <div><label>Сумма (LGN)</label><input id="amount" type="number" min="1" step="1" value="1"/></div>
    </div>
    <div class="grid">
      <div><label>Nonce</label><input id="nonce" type="number" min="1" step="1" placeholder="нажми 'Получить nonce'"/></div>
      <div><label>&nbsp;</label><button id="btn-send">Подписать и отправить</button></div>
    </div>
    <pre id="out-send" class="mono" style="margin-top:12px"></pre>
  </section>

  <section>
    <h3>Мост rToken (депозит, демо)</h3>
    <div class="grid">
      <div><label>ext_txid</label><input id="ext" class="mono" placeholder="например eth_txid_0xabc"/></div>
      <div><label>&nbsp;</label><button id="btn-deposit">Deposit rLGN</button></div>
    </div>
    <pre id="out-bridge" class="mono" style="margin-top:12px"></pre>
  </section>
</main>
<script src="./app.js?v=20250906_01" defer></script>
</body>
</html>
```

---

## FILE: `/var/www/logos/wallet/app.js`

```js
// === БАЗА ===
const API = location.origin + '/api/';     // ГАРАНТИРОВАННЫЙ префикс
const enc = new TextEncoder();

const $ = s => document.querySelector(s);
const toHex   = b => [...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('');
const fromHex = h => new Uint8Array((h.match(/.{1,2}/g)||[]).map(x=>parseInt(x,16)));

function u64le(n){ const b=new Uint8Array(8); new DataView(b.buffer).setBigUint64(0, BigInt(n), true); return b; }
async function sha256(bytes){ const d=await crypto.subtle.digest('SHA-256', bytes); return new Uint8Array(d); }

// === НАДЁЖНЫЙ fetchJSON: ВСЕГДА JSON (даже при ошибке) ===
async function fetchJSON(url, opts) {
  const r = await fetch(url, opts);
  const text = await r.text();
  try {
    const json = text ? JSON.parse(text) : {};
    if (!r.ok) throw json;
    return json;
  } catch(e) {
    // если прилетел текст/HTML — упакуем в JSON с сообщением
    throw { ok:false, error: (typeof e==='object' && e.error) ? e.error : (text || 'not json') };
  }
}

// === КЛЮЧИ/SESSION ===
const PASS = sessionStorage.getItem('logos_pass');
const RID  = sessionStorage.getItem('logos_rid');
if (!PASS || !RID) { location.replace('./login.html'); throw new Error('locked'); }

const DB_NAME='logos_wallet_v2', STORE='keys';
function idb(){ return new Promise((res,rej)=>{ const r=indexedDB.open(DB_NAME,1); r.onupgradeneeded=()=>r.result.createObjectStore(STORE); r.onsuccess=()=>res(r.result); r.onerror=()=>rej(r.error); }); }
async function idbGet(k){ const db=await idb(); return new Promise((res,rej)=>{ const tx=db.transaction(STORE,'readonly'); const st=tx.objectStore(STORE); const rq=st.get(k); rq.onsuccess=()=>res(rq.result||null); rq.onerror=()=>rej(rq.error); }); }
async function deriveKey(pass,salt){ const km=await crypto.subtle.importKey('raw', enc.encode(pass), {name:'PBKDF2'}, false, ['deriveKey']); return crypto.subtle.deriveKey({name:'PBKDF2',hash:'SHA-256',salt,iterations:120000}, km, {name:'AES-GCM',length:256}, false, ['encrypt','decrypt']); }
async function aesDecrypt(aesKey,iv,ct){ return new Uint8Array(await crypto.subtle.decrypt({name:'AES-GCM',iv}, aesKey, ct)); }
async function importKey(pass, meta){
  const aesKey = await deriveKey(pass, new Uint8Array(meta.salt));
  const pkcs8  = await aesDecrypt(aesKey, new Uint8Array(meta.iv_priv), new Uint8Array(meta.priv));
  const pubraw = await aesDecrypt(aesKey, new Uint8Array(meta.iv_pub),  new Uint8Array(meta.pub));
  const privateKey = await crypto.subtle.importKey('pkcs8', pkcs8, {name:'Ed25519'}, false, ['sign']);
  const publicKey  = await crypto.subtle.importKey('raw',   pubraw, {name:'Ed25519'}, true,  ['verify']);
  return { privateKey, publicKey, pub_hex: toHex(pubraw) };
}

let KEYS=null, META=null;
(async ()=>{
  META = await idbGet('acct:'+RID);
  if (!META) { sessionStorage.clear(); location.replace('./login.html'); return; }
  KEYS = await importKey(PASS, META);
  $('#pub') && ($('#pub').value = `RID: ${RID}\npub: ${KEYS.pub_hex}`);
  $('#rid-balance') && ($('#rid-balance').value = RID);
})();

// === КАНОНИКА/ПОДПИСЬ ===
async function canonHex(from_rid,to_rid,amount,nonce,pubkey_hex){
  const parts=[enc.encode(from_rid),enc.encode(to_rid),u64le(Number(amount)),u64le(Number(nonce)),enc.encode(pubkey_hex)];
  const buf=new Uint8Array(parts.reduce((s,p)=>s+p.length,0)); let o=0; for(const p of parts){ buf.set(p,o); o+=p.length; }
  return toHex(await sha256(buf));
}
async function signCanon(privateKey, canonHexStr){
  const msg = fromHex(canonHexStr);
  const sig = await crypto.subtle.sign('Ed25519', privateKey, msg);
  return toHex(sig);
}

// === API HELPERS ===
async function getBalance(rid){ return fetchJSON(`${API}balance/${encodeURIComponent(rid)}`); }
async function submitTxBatch(txs){
  return fetchJSON(`${API}submit_tx_batch`, {
    method:'POST', headers:{'content-type':'application/json'},
    body: JSON.stringify({ txs })
  });
}
async function stakeDelegate(delegator, validator, amount){
  return fetchJSON(`${API}stake/delegate`, {
    method:'POST', headers:{'content-type':'application/json'},
    body: JSON.stringify({ delegator, validator, amount:Number(amount) })
  });
}
async function stakeUndelegate(delegator, validator, amount){
  return fetchJSON(`${API}stake/undelegate`, {
    method:'POST', headers:{'content-type':'application/json'},
    body: JSON.stringify({ delegator, validator, amount:Number(amount) })
  });
}
async function stakeClaim(delegator, validator){
  return fetchJSON(`${API}stake/claim`, {
    method:'POST', headers:{'content-type':'application/json'},
    body: JSON.stringify({ delegator, validator, amount:0 })
  });
}
async function stakeMy(rid){ return fetchJSON(`${API}stake/my/${encodeURIComponent(rid)}`); }

// === UI ===
$('#btn-balance')?.addEventListener('click', async ()=>{
  try{ const rid = ($('#rid-balance')?.value || RID).trim(); const j=await getBalance(rid); $('#out-balance') && ($('#out-balance').textContent=JSON.stringify(j)); }
  catch(e){ alert(`ERR: ${JSON.stringify(e)}`); }
});

$('#btn-send')?.addEventListener('click', async ()=>{
  try{
    const to     = $('#to')?.value.trim();
    const amount = $('#amount')?.value.trim();
    const nonce  = $('#nonce')?.value.trim();
    if (!to || !amount || !nonce) throw {error:'fill to/amount/nonce'};
    const ch = await canonHex(RID, to, amount, nonce, KEYS.pub_hex);
    const sigHex = await signCanon(KEYS.privateKey, ch);
    const tx = { from_rid:RID, to_rid:to, amount:Number(amount), nonce:Number(nonce), pubkey_hex:KEYS.pub_hex, sig_hex:sigHex };
    const res = await submitTxBatch([tx]);
    $('#out-send') && ($('#out-send').textContent = JSON.stringify(res,null,2));
  }catch(e){ $('#out-send') && ($('#out-send').textContent = `ERR: ${JSON.stringify(e)}`); }
});

$('#btn-delegate')?.addEventListener('click', async ()=>{
  try{
    const val = ($('#validator')?.value || RID).trim();
    const amount = ($('#stake-amount')?.value || '').trim() || ($('#amount')?.value || '').trim();
    const res = await stakeDelegate(RID, val, amount);
    $('#out-stake') && ($('#out-stake').textContent = JSON.stringify(res));
  }catch(e){ $('#out-stake') && ($('#out-stake').textContent = `ERR: ${JSON.stringify(e)}`); }
});
$('#btn-undelegate')?.addEventListener('click', async ()=>{
  try{
    const val = ($('#validator')?.value || RID).trim();
    const amount = ($('#stake-amount')?.value || '').trim() || ($('#amount')?.value || '').trim();
    const res = await stakeUndelegate(RID, val, amount);
    $('#out-stake') && ($('#out-stake').textContent = JSON.stringify(res));
  }catch(e){ $('#out-stake') && ($('#out-stake').textContent = `ERR: ${JSON.stringify(e)}`); }
});
$('#btn-claim')?.addEventListener('click', async ()=>{
  try{
    const val = ($('#validator')?.value || RID).trim();
    const res = await stakeClaim(RID, val);
    $('#out-stake') && ($('#out-stake').textContent = JSON.stringify(res));
  }catch(e){ $('#out-stake') && ($('#out-stake').textContent = `ERR: ${JSON.stringify(e)}`); }
});
$('#btn-my')?.addEventListener('click', async ()=>{
  try{
    const res = await stakeMy(RID);
    $('#out-my') && ($('#out-my').textContent = JSON.stringify(res));
  }catch(e){ $('#out-my') && ($('#out-my').textContent = `ERR: ${JSON.stringify(e)}`); }
});

// кнопка NONCE (если есть)
$('#btn-nonce')?.addEventListener('click', async ()=>{
  try{ const j=await getBalance(RID); $('#nonce') && ($('#nonce').value = String(j.nonce||0)); }
  catch(e){ alert(`ERR: ${JSON.stringify(e)}`); }
});
```

---

## FILE: `/var/www/logos/wallet/app.v2.js`

```js
// == CONFIG ==
const API = location.origin + '/api/';
const enc = new TextEncoder();

// == utils ==
const $ = s => document.querySelector(s);
const toHex   = b => [...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('');
const fromHex = h => new Uint8Array((h.match(/.{1,2}/g)||[]).map(x=>parseInt(x,16)));
function u64le(n){ const b=new Uint8Array(8); new DataView(b.buffer).setBigUint64(0, BigInt(n), true); return b; }
async function sha256(bytes){ const d=await crypto.subtle.digest('SHA-256', bytes); return new Uint8Array(d); }

// == robust fetch: always JSON ==
async function fetchJSON(url, opts){
  try{
    const r = await fetch(url, opts);
    const text = await r.text();
    try {
      const js = text ? JSON.parse(text) : {};
      if(!r.ok) throw js;
      return js;
    } catch(parseErr){
      throw { ok:false, error:(text||'not json'), status:r.status||0 };
    }
  }catch(netErr){
    throw { ok:false, error:(netErr?.message||'network error') };
  }
}

// == session/keys ==
const PASS = sessionStorage.getItem('logos_pass');
const RID  = sessionStorage.getItem('logos_rid');
if (!PASS || !RID) { location.replace('./login.html'); throw new Error('locked'); }

const DB_NAME='logos_wallet_v2', STORE='keys';
function idb(){ return new Promise((res,rej)=>{ const r=indexedDB.open(DB_NAME,1); r.onupgradeneeded=()=>r.result.createObjectStore(STORE); r.onsuccess=()=>res(r.result); r.onerror=()=>rej(r.error); }); }
async function idbGet(k){ const db=await idb(); return new Promise((res,rej)=>{ const tx=db.transaction(STORE,'readonly'); const st=tx.objectStore(STORE); const rq=st.get(k); rq.onsuccess=()=>res(rq.result||null); rq.onerror=()=>rej(rq.error); }); }
async function deriveKey(pass,salt){ const km=await crypto.subtle.importKey('raw', enc.encode(pass), {name:'PBKDF2'}, false, ['deriveKey']); return crypto.subtle.deriveKey({name:'PBKDF2',hash:'SHA-256',salt,iterations:120000}, km, {name:'AES-GCM',length:256}, false, ['encrypt','decrypt']); }
async function aesDecrypt(aesKey,iv,ct){ return new Uint8Array(await crypto.subtle.decrypt({name:'AES-GCM',iv}, aesKey, ct)); }
async function importKey(pass, meta){
  const aesKey=await deriveKey(pass,new Uint8Array(meta.salt));
  const pkcs8 =await aesDecrypt(aesKey,new Uint8Array(meta.iv_priv),new Uint8Array(meta.priv));
  const pubraw=await aesDecrypt(aesKey,new Uint8Array(meta.iv_pub), new Uint8Array(meta.pub));
  const privateKey=await crypto.subtle.importKey('pkcs8',pkcs8,{name:'Ed25519'},false,['sign']);
  const publicKey =await crypto.subtle.importKey('raw',  pubraw,{name:'Ed25519'},true, ['verify']);
  return { privateKey, publicKey, pub_hex: toHex(pubraw) };
}
let KEYS=null, META=null;
(async()=>{
  META=await idbGet('acct:'+RID);
  if(!META){ sessionStorage.clear(); location.replace('./login.html'); return; }
  KEYS=await importKey(PASS, META);
  $('#pub') && ($('#pub').value=`RID: ${RID}\npub: ${KEYS.pub_hex}`);
  ($('#rid-balance')||{}).value = RID;
})();

// == canonical/sign ==
async function canonHex(from_rid,to_rid,amount,nonce,pubkey_hex){
  const parts=[enc.encode(from_rid),enc.encode(to_rid),u64le(Number(amount)),u64le(Number(nonce)),enc.encode(pubkey_hex)];
  const buf=new Uint8Array(parts.reduce((s,p)=>s+p.length,0)); let o=0; for(const p of parts){ buf.set(p,o); o+=p.length; }
  return toHex(await sha256(buf));
}
async function signCanon(priv, canonHexStr){
  const msg = fromHex(canonHexStr);
  const sig = await crypto.subtle.sign('Ed25519', priv, msg);
  return toHex(sig);
}

// == API wrappers ==
async function getBalance(rid){ return fetchJSON(`${API}balance/${encodeURIComponent(rid)}`); }
async function submitTxBatch(txs){
  return fetchJSON(`${API}submit_tx_batch`, { method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify({ txs }) });
}
async function stakeDelegate(delegator,validator,amount){
  return fetchJSON(`${API}stake/delegate`, { method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify({delegator,validator,amount:Number(amount)}) });
}
async function stakeUndelegate(delegator,validator,amount){
  return fetchJSON(`${API}stake/undelegate`, { method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify({delegator,validator,amount:Number(amount)}) });
}
async function stakeClaim(delegator,validator){
  return fetchJSON(`${API}stake/claim`, { method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify({delegator,validator,amount:0}) });
}
async function stakeMy(rid){ return fetchJSON(`${API}stake/my/${encodeURIComponent(rid)}`); }

// == UI handlers ==
$('#btn-balance')?.addEventListener('click', async ()=>{
  try{ const rid=($('#rid-balance')?.value||RID).trim(); const j=await getBalance(rid); $('#out-balance') && ($('#out-balance').textContent=JSON.stringify(j)); }
  catch(e){ $('#out-balance') && ($('#out-balance').textContent=`ERR: ${JSON.stringify(e)}`); }
});

$('#btn-send')?.addEventListener('click', async ()=>{
  try{
    const to = ($('#to')||$('#rid-to'))?.value.trim();
    const amount = ($('#amount')||$('#sum')||$('#stake-amount'))?.value.trim();
    const nonce  = ($('#nonce')||$('#tx-nonce'))?.value.trim();
    if(!to||!amount||!nonce) throw {error:'fill to/amount/nonce'};
    const ch = await canonHex(RID, to, amount, nonce, KEYS.pub_hex);
    const sigHex = await signCanon(KEYS.privateKey, ch);
    const tx = { from_rid:RID, to_rid:to, amount:Number(amount), nonce:Number(nonce), pubkey_hex:KEYS.pub_hex, sig_hex:sigHex };
    const res = await submitTxBatch([tx]);
    $('#out-send') && ($('#out-send').textContent = JSON.stringify(res,null,2));
  }catch(e){ $('#out-send') && ($('#out-send').textContent = `ERR: ${JSON.stringify(e)}`); }
});

$('#btn-delegate')?.addEventListener('click', async ()=>{
  try{
    const val = ($('#validator')||$('#val')||$('#rid-validator'))?.value.trim() || RID;
    const amount = ($('#stake-amount')||$('#amount')||$('#sum'))?.value.trim();
    const res = await stakeDelegate(RID, val, amount);
    $('#out-stake') && ($('#out-stake').textContent = JSON.stringify(res));
  }catch(e){ $('#out-stake') && ($('#out-stake').textContent = `ERR: ${JSON.stringify(e)}`); }
});
$('#btn-undelegate')?.addEventListener('click', async ()=>{
  try{
    const val = ($('#validator')||$('#val')||$('#rid-validator'))?.value.trim() || RID;
    const amount = ($('#stake-amount')||$('#amount')||$('#sum'))?.value.trim();
    const res = await stakeUndelegate(RID, val, amount);
    $('#out-stake') && ($('#out-stake').textContent = JSON.stringify(res));
  }catch(e){ $('#out-stake') && ($('#out-stake').textContent = `ERR: ${JSON.stringify(e)}`); }
});
$('#btn-claim')?.addEventListener('click', async ()=>{
  try{
    const val = ($('#validator')||$('#val')||$('#rid-validator'))?.value.trim() || RID;
    const res = await stakeClaim(RID, val);
    $('#out-stake') && ($('#out-stake').textContent = JSON.stringify(res));
  }catch(e){ $('#out-stake') && ($('#out-stake').textContent = `ERR: ${JSON.stringify(e)}`); }
});
$('#btn-my')?.addEventListener('click', async ()=>{
  try{ const res = await stakeMy(RID); $('#out-my') && ($('#out-my').textContent = JSON.stringify(res)); }
  catch(e){ $('#out-my') && ($('#out-my').textContent = `ERR: ${JSON.stringify(e)}`); }
});

// nonce helper
$('#btn-nonce')?.addEventListener('click', async ()=>{
  try{ const j=await getBalance(RID); ($('#nonce')||$('#tx-nonce')) && ((($('#nonce')||$('#tx-nonce')).value)=String(j.nonce||0)); }
  catch(e){ /* ignore */ }
});
```

---

## FILE: `/var/www/logos/wallet/app.v3.js`

```js
const API = location.origin + '/api/';
const enc = new TextEncoder();

// utils
const $ = s => document.querySelector(s);
const toHex   = b => [...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('');
const fromHex = h => new Uint8Array((h.match(/.{1,2}/g)||[]).map(x=>parseInt(x,16)));
function u64le(n){ const b=new Uint8Array(8); new DataView(b.buffer).setBigUint64(0, BigInt(n), true); return b; }
async function sha256(bytes){ const d=await crypto.subtle.digest('SHA-256', bytes); return new Uint8Array(d); }

// robust fetch → всегда JSON
async function fetchJSON(url, opts){
  const r = await fetch(url, opts);
  const text = await r.text();
  try {
    const js = text ? JSON.parse(text) : {};
    if (!r.ok) throw js;
    return js;
  } catch(e) {
    throw { ok:false, error:(typeof e==='object'&&e.error)?e.error:(text||'not json'), status:r.status||0 };
  }
}

// session/keys
const PASS = sessionStorage.getItem('logos_pass');
const RID  = sessionStorage.getItem('logos_rid');
if (!PASS || !RID) { location.replace('./login.html'); throw new Error('locked'); }

const DB_NAME='logos_wallet_v2', STORE='keys';
function idb(){ return new Promise((res,rej)=>{ const r=indexedDB.open(DB_NAME,1); r.onupgradeneeded=()=>r.result.createObjectStore(STORE); r.onsuccess=()=>res(r.result); r.onerror=()=>rej(r.error); }); }
async function idbGet(k){ const db=await idb(); return new Promise((res,rej)=>{ const tx=db.transaction(STORE,'readonly'); const st=tx.objectStore(STORE); const rq=st.get(k); rq.onsuccess=()=>res(rq.result||null); rq.onerror=()=>rej(rq.error); }); }
async function deriveKey(pass,salt){ const km=await crypto.subtle.importKey('raw', enc.encode(pass), {name:'PBKDF2'}, false, ['deriveKey']); return crypto.subtle.deriveKey({name:'PBKDF2',hash:'SHA-256',salt,iterations:120000}, km, {name:'AES-GCM',length:256}, false, ['encrypt','decrypt']); }
async function aesDecrypt(aesKey,iv,ct){ return new Uint8Array(await crypto.subtle.decrypt({name:'AES-GCM',iv}, aesKey, ct)); }
async function importKey(pass, meta){
  const aesKey=await deriveKey(pass,new Uint8Array(meta.salt));
  const pkcs8 =await aesDecrypt(aesKey,new Uint8Array(meta.iv_priv),new Uint8Array(meta.priv));
  const pubraw=await aesDecrypt(aesKey,new Uint8Array(meta.iv_pub), new Uint8Array(meta.pub));
  const privateKey=await crypto.subtle.importKey('pkcs8',pkcs8,{name:'Ed25519'},false,['sign']);
  const publicKey =await crypto.subtle.importKey('raw',  pubraw,{name:'Ed25519'},true, ['verify']);
  return { privateKey, publicKey, pub_hex: toHex(pubraw) };
}
let KEYS=null, META=null;
(async()=>{
  META=await idbGet('acct:'+RID);
  if(!META){ sessionStorage.clear(); location.replace('./login.html'); return; }
  KEYS=await importKey(PASS, META);
  const pubEl=$('#pub'); if(pubEl) pubEl.value=`RID: ${RID}\npub: ${KEYS.pub_hex}`;
  const rb=$('#rid-balance'); if(rb) rb.value=RID;
})();

// canonical+sign
async function canonHex(from_rid,to_rid,amount,nonce,pubkey_hex){
  const parts=[enc.encode(from_rid),enc.encode(to_rid),u64le(Number(amount)),u64le(Number(nonce)),enc.encode(pubkey_hex)];
  const buf=new Uint8Array(parts.reduce((s,p)=>s+p.length,0)); let o=0; for(const p of parts){ buf.set(p,o); o+=p.length; }
  return toHex(await sha256(buf));
}
async function signCanon(priv, canonHexStr){
  const msg = fromHex(canonHexStr);
  const sig = await crypto.subtle.sign('Ed25519', priv, msg);
  return toHex(sig);
}

// API wrappers
const getBalance = (rid)=>fetchJSON(`${API}balance/${encodeURIComponent(rid)}`);
const submitTxBatch = (txs)=>fetchJSON(`${API}submit_tx_batch`,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({txs})});
const stakeDelegate   = (delegator,validator,amount)=>fetchJSON(`${API}stake/delegate`,  {method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({delegator,validator,amount:Number(amount)})});
const stakeUndelegate = (delegator,validator,amount)=>fetchJSON(`${API}stake/undelegate`,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({delegator,validator,amount:Number(amount)})});
const stakeClaim      = (delegator,validator)=>fetchJSON(`${API}stake/claim`,            {method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({delegator,validator,amount:0})});
const stakeMy         = (rid)=>fetchJSON(`${API}stake/my/${encodeURIComponent(rid)}`);

// UI handlers
$('#btn-balance')?.addEventListener('click', async ()=>{
  try{ const rid=($('#rid-balance')?.value||RID).trim(); const j=await getBalance(rid); $('#out-balance') && ($('#out-balance').textContent=JSON.stringify(j)); }
  catch(e){ $('#out-balance') && ($('#out-balance').textContent=`ERR: ${JSON.stringify(e)}`); }
});

$('#btn-nonce')?.addEventListener('click', async ()=>{
  try{ const j=await getBalance(RID); const n=($('#nonce')); if(n) n.value=String(j.nonce||0); } catch(e){}
});

$('#btn-send')?.addEventListener('click', async ()=>{
  try{
    const to=$('#to')?.value.trim(); const amount=$('#amount')?.value.trim(); const nonce=$('#nonce')?.value.trim();
    if(!to||!amount||!nonce) throw {error:'fill to/amount/nonce'};
    const ch=await canonHex(RID,to,amount,nonce,KEYS.pub_hex);
    const sig=await signCanon(KEYS.privateKey,ch);
    const tx={from_rid:RID,to_rid:to,amount:Number(amount),nonce:Number(nonce),pubkey_hex:KEYS.pub_hex,sig_hex:sig};
    const res=await submitTxBatch([tx]);
    $('#out-send') && ($('#out-send').textContent=JSON.stringify(res,null,2));
  }catch(e){ $('#out-send') && ($('#out-send').textContent=`ERR: ${JSON.stringify(e)}`); }
});

$('#btn-delegate')?.addEventListener('click', async ()=>{
  try{
    const val=($('#validator')?.value||RID).trim(); const amount=$('#stake-amount')?.value.trim();
    const res=await stakeDelegate(RID,val,amount);
    $('#out-stake') && ($('#out-stake').textContent=JSON.stringify(res));
  }catch(e){ $('#out-stake') && ($('#out-stake').textContent=`ERR: ${JSON.stringify(e)}`); }
});
$('#btn-undelegate')?.addEventListener('click', async ()=>{
  try{
    const val=($('#validator')?.value||RID).trim(); const amount=$('#stake-amount')?.value.trim();
    const res=await stakeUndelegate(RID,val,amount);
    $('#out-stake') && ($('#out-stake').textContent=JSON.stringify(res));
  }catch(e){ $('#out-stake') && ($('#out-stake').textContent=`ERR: ${JSON.stringify(e)}`); }
});
$('#btn-claim')?.addEventListener('click', async ()=>{
  try{
    const val=($('#validator')?.value||RID).trim();
    const res=await stakeClaim(RID,val);
    $('#out-stake') && ($('#out-stake').textContent=JSON.stringify(res));
  }catch(e){ $('#out-stake') && ($('#out-stake').textContent=`ERR: ${JSON.stringify(e)}`); }
});
$('#btn-my')?.addEventListener('click', async ()=>{
  try{ const res=await stakeMy(RID); $('#out-my') && ($('#out-my').textContent=JSON.stringify(res)); }
  catch(e){ $('#out-my') && ($('#out-my').textContent=`ERR: ${JSON.stringify(e)}`); }
});
```

---

## FILE: `/var/www/logos/wallet/auth.js`

```js
// AUTH v3: RID + пароль. Сохраняем под "acct:<RID>".
// Фичи: авто-подстановка last_rid, кликабельный список, чистка всех пробелов/переносов в RID.

const DB_NAME='logos_wallet_v2', STORE='keys', enc=new TextEncoder();
const $ = s => document.querySelector(s);
const out = msg => { const el=$('#out'); if(el) el.textContent=String(msg); };

function normRid(s){ return (s||'').replace(/\s+/g,'').trim(); } // убираем все пробелы/переносы

function ensureEnv() {
  if (!window.isSecureContext) throw new Error('Нужен HTTPS (secure context)');
  if (!window.indexedDB) throw new Error('IndexedDB недоступен');
  if (!crypto || !crypto.subtle) throw new Error('WebCrypto недоступен');
}

const idb=()=>new Promise((res,rej)=>{const r=indexedDB.open(DB_NAME,1);r.onupgradeneeded=()=>r.result.createObjectStore(STORE);r.onsuccess=()=>res(r.result);r.onerror=()=>rej(r.error);});
const idbGet=async k=>{const db=await idb();return new Promise((res,rej)=>{const t=db.transaction(STORE,'readonly').objectStore(STORE).get(k);t.onsuccess=()=>res(t.result||null);t.onerror=()=>rej(t.error);});};
const idbSet=async (k,v)=>{const db=await idb();return new Promise((res,rej)=>{const t=db.transaction(STORE,'readwrite').objectStore(STORE).put(v,k);t.onsuccess=()=>res(true);t.onerror=()=>rej(t.error);});};
const idbDel=async k=>{const db=await idb();return new Promise((res,rej)=>{const t=db.transaction(STORE,'readwrite').objectStore(STORE).delete(k);t.onsuccess=()=>res(true);t.onerror=()=>rej(t.error);});};

async function deriveKey(pass,salt){
  const keyMat=await crypto.subtle.importKey('raw',enc.encode(pass),'PBKDF2',false,['deriveKey']);
  return crypto.subtle.deriveKey({name:'PBKDF2',salt,iterations:120000,hash:'SHA-256'},keyMat,{name:'AES-GCM',length:256},false,['encrypt','decrypt']);
}
async function aesEncrypt(aesKey,data){const iv=crypto.getRandomValues(new Uint8Array(12));const ct=await crypto.subtle.encrypt({name:'AES-GCM',iv},aesKey,data);return{iv:Array.from(iv),ct:Array.from(new Uint8Array(ct))}}
async function aesDecrypt(aesKey,iv,ct){return new Uint8Array(await crypto.subtle.decrypt({name:'AES-GCM',iv:new Uint8Array(iv)},aesKey,new Uint8Array(ct)))}

function b58(bytes){
  const ALPH="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";
  const hex=[...new Uint8Array(bytes)].map(b=>b.toString(16).padStart(2,'0')).join('');
  let x=BigInt('0x'+hex), out=''; while(x>0n){ out=ALPH[Number(x%58n)]+out; x/=58n; } return out||'1';
}

async function addAccount(rid){ const list=(await idbGet('accounts'))||[]; if(!list.includes(rid)){ list.push(rid); await idbSet('accounts',list); } }
async function listAccounts(){ return (await idbGet('accounts'))||[]; }

async function createAccount(pass){
  ensureEnv();
  if(!pass || pass.length<6) throw new Error('Пароль ≥6 символов');

  out('Создаём ключ…');
  const kp=await crypto.subtle.generateKey({name:'Ed25519'},true,['sign','verify']);
  const rawPub=new Uint8Array(await crypto.subtle.exportKey('raw',kp.publicKey));
  const rid=b58(rawPub);
  const pkcs8=new Uint8Array(await crypto.subtle.exportKey('pkcs8',kp.privateKey));
  const salt=crypto.getRandomValues(new Uint8Array(16));
  const aes=await deriveKey(pass,salt);
  const {iv,ct}=await aesEncrypt(aes,pkcs8);
  const meta={rid,pub:Array.from(rawPub),salt:Array.from(salt),iv,priv:ct};

  await idbSet('acct:'+rid,meta);
  await addAccount(rid);
  await idbSet('last_rid', rid);

  sessionStorage.setItem('logos_pass',pass);
  sessionStorage.setItem('logos_rid',rid);
  out('RID создан: '+rid+' → вход…');
  location.href='./app.html';
}

async function loginAccount(rid, pass){
  ensureEnv();
  rid = normRid(rid);
  if(!rid) throw new Error('Укажи RID');
  if(!pass || pass.length<6) throw new Error('Пароль ≥6 символов');

  const meta=await idbGet('acct:'+rid);
  if(!meta){
    const list=await listAccounts();
    throw new Error('RID не найден на этом устройстве. Сохранённые RID:\n'+(list.length?list.join('\n'):'—'));
  }
  const aes=await deriveKey(pass,new Uint8Array(meta.salt));
  try{ await aesDecrypt(aes,meta.iv,meta.priv); } catch(e){ throw new Error('Неверный пароль'); }

  sessionStorage.setItem('logos_pass',pass);
  sessionStorage.setItem('logos_rid',rid);
  await idbSet('last_rid', rid);
  out('Вход…'); location.href='./app.html';
}

async function resetAll(){
  const list=await listAccounts();
  for(const rid of list){ await idbDel('acct:'+rid); }
  await idbDel('accounts'); await idbDel('last_rid');
  sessionStorage.clear();
  out('Все аккаунты удалены (DEV).');
}

function renderRidList(list){
  const wrap=$('#listWrap'), ul=$('#ridList'); ul.innerHTML='';
  if(!list.length){ wrap.style.display='block'; ul.innerHTML='<li>— пусто —</li>'; return; }
  wrap.style.display='block';
  list.forEach(rid=>{
    const li=document.createElement('li'); li.textContent=rid;
    li.addEventListener('click', ()=>{ $('#loginRid').value=rid; out('RID подставлен'); });
    ul.appendChild(li);
  });
}

// авто-подстановка last_rid при загрузке
(async ()=>{
  const last=await idbGet('last_rid'); if(last){ $('#loginRid').value=last; }
})();

// wire UI
$('#btn-login').addEventListener('click', async ()=>{
  const rid=$('#loginRid').value; const pass=$('#pass').value;
  try{ await loginAccount(rid,pass); }catch(e){ out('ERR: '+(e&&e.message?e.message:e)); }
});
$('#btn-create').addEventListener('click', async ()=>{
  const pass=$('#pass').value;
  try{ await createAccount(pass); }catch(e){ out('ERR: '+(e&&e.message?e.message:e)); }
});
$('#btn-list').addEventListener('click', async ()=>{
  try{ renderRidList(await listAccounts()); }catch(e){ out('ERR: '+e); }
});
$('#btn-reset').addEventListener('click', resetAll);
```

---

## FILE: `/var/www/logos/wallet/index.html`

```html
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Wallet</title>
  <link rel="stylesheet" href="./css/styles.css?v=1757930528">
</head>
<body>
<div class="wrap">
  <h1>LOGOS Wallet</h1>

  <!-- App (показывается после unlock) -->
  <section id="viewApp" class="card hidden">
    <h3>Кошелёк разблокирован</h3>
    <div class="kpi">
      <span class="badge">RID: <b class="mono" id="kpiRid">—</b></span>
      <span class="badge">balance: <b id="kpiBal">—</b></span>
      <span class="badge">nonce: <b id="kpiNonce">—</b></span>
      <span class="badge">head: <b id="kpiHead">—</b></span>
      <span class="badge">delegated: <b id="kpiDelegated">—</b></span>
      <span class="badge">entries: <b id="kpiEntries">—</b></span>
      <span class="badge">claimable: <b id="kpiClaimable">—</b></span>
    </div>
  </section>

  <section id="viewSend" class="card hidden">
    <h3>Отправка</h3>
    <div class="grid cols-2">
      <div><label>RID получателя</label><input id="sendTo" class="mono" placeholder="RID"/></div>
      <div><label>Сумма</label><input id="sendAmount" type="number" min="1" step="1" placeholder="amount (u64)"/></div>
    </div>
    <div class="row mt10"><button id="btnSendTx">Отправить</button></div>
  </section>

  <section id="viewStake" class="card hidden">
    <h3>Стейкинг</h3>
    <div class="grid cols-3">
      <div><label>RID валидатора (SELF = свой RID)</label><input id="stakeValidator" class="mono" readonly/></div>
      <div><label>Сумма</label><input id="stakeAmount" type="number" min="1" step="1" placeholder="amount (u64)"/></div>
      <div class="row" style="align-items:end">
        <button id="btnStakeDel">Delegate</button>
        <button id="btnStakeUn" class="secondary">Undelegate</button>
        <button id="btnStakeClaim" class="secondary">Claim</button>
      </div>
    </div>
  </section>

  <section id="viewHistory" class="card hidden">
    <h3>История</h3>
    <div class="scroll">
      <table class="table">
        <thead><tr><th>type</th><th>counterparty</th><th>amount</th><th>nonce</th><th>height</th><th>tx</th></tr></thead>
        <tbody id="histBody"></tbody>
      </table>
    </div>
  </section>
</div>

<!-- Secure Unlock overlay -->
<div id="lockOverlay">
  <div id="lockCard">
    <div id="brand">
      <div><b>LOGOS Wallet — Secure Unlock</b></div>
      <div class="badge mono" id="rpHost">—</div>
    </div>
    <div id="phish">Проверь домен и значок 🔒 TLS. Никому не сообщай пароль.</div>

    <!-- Лэндинг -->
    <div id="viewLanding">
      <p class="muted">Выберите действие:</p>
      <div class="row">
        <button id="goCreate">Создать новый</button>
        <button id="goImport" class="secondary">Импортировать</button>
        <button id="goUnlock" class="ghost">Разблокировать</button>
      </div>
    </div>

    <!-- Создать: пароль -->
    <div id="viewCreatePwd" class="hidden mt10">
      <h3>Создать пароль</h3>
      <div class="grid cols-2">
        <div><label>Пароль</label><input id="newPwd1" type="password" autocomplete="new-password" placeholder="(≥8)"/></div>
        <div><label>Повтор</label><input id="newPwd2" type="password" autocomplete="new-password" placeholder="повтор"/></div>
      </div>
      <div class="row mt10"><button id="createNext">Далее</button><button id="back1" class="ghost">Назад</button></div>
    </div>

    <!-- Создать: бэкап -->
    <div id="viewBackup" class="hidden mt10">
      <h3>Резервный ключ</h3>
      <p class="muted">Сохраните PKCS8 Base64 (как seed). Без него восстановление невозможно.</p>
      <textarea id="backupArea" class="mono" readonly></textarea>
      <label class="row mt10" style="gap:8px;align-items:center"><input type="checkbox" id="chkSaved"/> Я записал ключ</label>
      <div class="row mt10"><button id="finishCreate" disabled>Завершить и разблокировать</button><button id="back2" class="ghost">Назад</button></div>
    </div>

    <!-- Импорт -->
    <div id="viewImport" class="hidden mt10">
      <h3>Импорт</h3>
      <label>PKCS8 Base64</label><textarea id="impKey" class="mono" placeholder="----- base64 -----"></textarea>
      <div class="grid cols-2 mt10">
        <div><label>Пароль</label><input id="impPwd1" type="password" autocomplete="new-password" placeholder="(≥8)"/></div>
        <div><label>Повтор</label><input id="impPwd2" type="password" autocomplete="new-password" placeholder="повтор"/></div>
      </div>
      <div class="row mt10"><button id="doImport">Импортировать и разблокировать</button><button id="back3" class="ghost">Назад</button></div>
    </div>

    <!-- Разблокировать -->
    <div id="viewUnlock" class="hidden mt10">
      <h3>Разблокировать</h3>
      <label>Пароль</label><input id="unPwd" type="password" autocomplete="current-password" placeholder="Пароль"/>
      <div class="row mt10"><button id="btnUnlock">Разблокировать</button><button id="btnReset" class="secondary">Сбросить</button></div>
    </div>
  </div>
</div>

<div id="toast" class="toast"></div>

<!-- Модули -->
<script type="module" src="./js/core.js?v=1757930528"></script>
<script type="module" src="./js/vault.js?v=1757930528"></script>
<script type="module" src="./js/unlock.js?v=1757930528"></script>
<script type="module" src="./js/app.js?v=1757930528"></script>
</body>
</html>
```

---

## FILE: `/var/www/logos/wallet/login.html`

```html
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Wallet — Вход</title>
  <style>
    body{font-family:system-ui,Segoe UI,Roboto,Arial,sans-serif;margin:0;background:#0b0c10;color:#e6edf3}
    header{padding:16px 20px;background:#11151a;border-bottom:1px solid #1e242c}
    h1{font-size:18px;margin:0}
    main{max-width:720px;margin:48px auto;padding:0 16px}
    section{background:#11151a;margin:16px 0;border-radius:12px;padding:16px;border:1px solid #1e242c}
    label{display:block;margin:8px 0 6px}
    input,button{width:100%;padding:12px;border-radius:10px;border:1px solid #2a313a;background:#0b0f14;color:#e6edf3}
    button{cursor:pointer;border:1px solid #3b7ddd;background:#1665c1}
    button.secondary{background:#1b2129}
    small{opacity:.8}
    .grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
    @media (max-width:720px){.grid{grid-template-columns:1fr}}
    .mono{font-family:ui-monospace,Menlo,Consolas,monospace}
    ul{list-style:none;padding:0;margin:8px 0}
    li{padding:8px;border:1px solid #2a313a;border-radius:8px;margin-bottom:6px;cursor:pointer;background:#0b0f14}
  </style>
</head>
<body>
<header><h1>LOGOS Wallet — Secure (WebCrypto + IndexedDB)</h1></header>
<main>
  <section>
    <h3>Вход в аккаунт</h3>
    <label>Логин (RID)</label>
    <input id="loginRid" class="mono" placeholder="Вставь RID (base58) или выбери из списка ниже"/>
    <label>Пароль</label>
    <input id="pass" type="password" placeholder="Пароль для шифрования ключа"/>

    <div class="grid" style="margin-top:12px">
      <button id="btn-login">Войти по RID + пароль</button>
      <button id="btn-create">Создать новый RID</button>
    </div>

    <div style="margin-top:12px">
      <button id="btn-list" class="secondary">Показать сохранённые RID</button>
      <button id="btn-reset" class="secondary">Сбросить все аккаунты (DEV)</button>
    </div>

    <div id="listWrap" style="display:none;margin-top:10px">
      <small>Сохранённые на этом устройстве RID (тапни, чтобы подставить):</small>
      <ul id="ridList"></ul>
    </div>

    <p><small>Ключ Ed25519 хранится зашифрованным AES-GCM (PBKDF2) в IndexedDB. Ничего не уходит в сеть.</small></p>
    <pre id="out" class="mono"></pre>
  </section>
</main>
<script src="./auth.js?v=20250906_03" defer></script>
</body>
</html>
```

---

## FILE: `/var/www/logos/wallet/ping.html`

```html
<!doctype html><meta charset="utf-8">
<title>Wallet JS Ping</title>
<button onclick="alert('JS OK')">JS TEST</button>
```

---

## FILE: `/var/www/logos/wallet/staking.js`

```js
// LOGOS Wallet — staking (prod)
async function stakeSign(op, validator, amount, nonce){
  const msg = `${session.rid}|${op}|${validator}|${amount||0}|${nonce}`;
  return await crypto.subtle.sign('Ed25519', session.privKey, new TextEncoder().encode(msg)).then(buf=>{
    return Array.from(new Uint8Array(buf)).map(b=>b.toString(16).padStart(2,'0')).join('');
  });
}
document.getElementById('btnDelegate').onclick = async ()=>{
  try{
    const b=await (await fetch(`${location.origin + '/api'}/balance/${encodeURIComponent(session.rid)}`)).json();
    const validator=document.getElementById('valRid').value.trim();
    const amount=Number(document.getElementById('stakeAmt').value);
    const nonce=(b.nonce??0)+1;
    const sig_hex=await stakeSign('delegate',validator,amount,nonce);
    const r=await fetch(`${location.origin + '/api'}/stake/submit`,{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({from:session.rid,op:'delegate',validator,amount,nonce,sig_hex})});
    const j=await r.json(); document.getElementById('stakeStatus').textContent = j.ok?'Delegate OK':'ERR '+j.info;
  }catch(e){ document.getElementById('stakeStatus').textContent='Ошибка delegate'; }
};
document.getElementById('btnUndelegate').onclick = async ()=>{
  try{
    const b=await (await fetch(`${location.origin + '/api'}/balance/${encodeURIComponent(session.rid)}`)).json();
    const validator=document.getElementById('valRid').value.trim();
    const amount=Number(document.getElementById('stakeAmt').value);
    const nonce=(b.nonce??0)+1;
    const sig_hex=await stakeSign('undelegate',validator,amount,nonce);
    const r=await fetch(`${location.origin + '/api'}/stake/submit`,{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({from:session.rid,op:'undelegate',validator,amount,nonce,sig_hex})});
    const j=await r.json(); document.getElementById('stakeStatus').textContent = j.ok?'Undelegate OK':'ERR '+j.info;
  }catch(e){ document.getElementById('stakeStatus').textContent='Ошибка undelegate'; }
};
document.getElementById('btnClaim').onclick = async ()=>{
  try{
    const b=await (await fetch(`${location.origin + '/api'}/balance/${encodeURIComponent(session.rid)}`)).json();
    const validator=document.getElementById('valRid').value.trim();
    const nonce=(b.nonce??0)+1;
    const sig_hex=await stakeSign('claim',validator,0,nonce);
    const r=await fetch(`${location.origin + '/api'}/stake/submit`,{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({from:session.rid,op:'claim',validator,amount:0,nonce,sig_hex})});
    const j=await r.json(); document.getElementById('stakeStatus').textContent = j.ok?'Claim OK':'ERR '+j.info;
  }catch(e){ document.getElementById('stakeStatus').textContent='Ошибка claim'; }
};
```

---

## FILE: `/var/www/logos/wallet/wallet.css`

```css
:root {
  --bg: #0e1116;
  --fg: #e6edf3;
  --muted: #9aa4ae;
  --card: #161b22;
  --border: #2d333b;
  --accent: #2f81f7;
  --accent-2: #7ee787;
  --warn: #f0883e;
  --error: #ff6b6b;
  --mono: ui-monospace, SFMono-Regular, Menlo, monospace;
  --sans: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, sans-serif;
}
html[data-theme="light"] {
  --bg: #f6f8fa;
  --fg: #0b1117;
  --muted: #57606a;
  --card: #ffffff;
  --border: #d0d7de;
  --accent: #0969da;
  --accent-2: #1a7f37;
  --warn: #9a6700;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--fg); font-family: var(--sans); }
a { color: var(--accent); text-decoration: none; }
.topbar {
  position: sticky; top: 0; z-index: 10;
  display: flex; align-items: center; gap: 8px;
  padding: 10px 14px; border-bottom: 1px solid var(--border); background: var(--card);
}
.brand { font-weight: 700; }
.spacer { flex: 1; }
.endpoint { font-size: 12px; color: var(--muted); }
.container { max-width: 980px; margin: 16px auto; padding: 0 12px; display: grid; gap: 16px; }
.card {
  border: 1px solid var(--border); border-radius: 10px;
  background: var(--card); padding: 14px;
}
h2 { margin: 0 0 10px 0; font-size: 18px; }
.row { display: flex; gap: 8px; align-items: center; }
.wrap { flex-wrap: wrap; }
.grid2 { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 8px; }
.mt8 { margin-top: 8px; }
.input {
  border: 1px solid var(--border); background: transparent; color: var(--fg);
  padding: 8px 10px; border-radius: 8px; outline: none;
}
.input:focus { border-color: var(--accent); }
.grow { flex: 1; min-width: 260px; }
.w100 { width: 100px; }
.w120 { width: 120px; }
.btn {
  border: 1px solid var(--border); background: var(--accent); color: #fff;
  padding: 8px 12px; border-radius: 8px; cursor: pointer;
}
.btn.secondary { background: transparent; color: var(--fg); }
.btn.warn { background: var(--warn); color: #111; }
.btn:disabled { opacity: .6; cursor: not-allowed; }
.mono { font-family: var(--mono); }
.log {
  font-family: var(--mono); background: transparent; border: 1px dashed var(--border);
  border-radius: 8px; padding: 8px; min-height: 40px; white-space: pre-wrap;
}
.statusbar {
  position: sticky; bottom: 0; margin-top: 12px; padding: 8px 14px;
  border-top: 1px solid var(--border); background: var(--card); color: var(--muted);
}

/* auto-theming для системной темы, если юзер не переключал вручную */
@media (prefers-color-scheme: light) {
  html[data-theme="auto"] { --bg: #f6f8fa; --fg: #0b1117; --muted:#57606a; --card:#fff; --border:#d0d7de; --accent:#0969da; --accent-2:#1a7f37; --warn:#9a6700; }
}
```

---

## FILE: `/var/www/logos/wallet/wallet.js`

```js
// LOGOS Wallet core — PROD
// Подключение к API через /api (nginx proxy)
const BASE = location.origin + '/api';

// ===== IndexedDB =====
const DB_NAME='logos_wallet', DB_STORE='keys';
function idbOpen(){return new Promise((res,rej)=>{const r=indexedDB.open(DB_NAME,1);r.onupgradeneeded=e=>{const db=e.target.result;if(!db.objectStoreNames.contains(DB_STORE))db.createObjectStore(DB_STORE,{keyPath:'rid'})};r.onsuccess=()=>res(r.result);r.onerror=()=>rej(r.error);});}
async function idbPut(rec){const db=await idbOpen();await new Promise((res,rej)=>{const tx=db.transaction(DB_STORE,'readwrite');tx.objectStore(DB_STORE).put(rec);tx.oncomplete=res;tx.onerror=()=>rej(tx.error)});db.close();}
async function idbGet(rid){const db=await idbOpen();return await new Promise((res,rej)=>{const tx=db.transaction(DB_STORE,'readonly');const rq=tx.objectStore(DB_STORE).get(rid);rq.onsuccess=()=>res(rq.result||null);rq.onerror=()=>rej(rq.error);tx.oncomplete=()=>db.close()});}

// ===== UI refs =====
const ui={
  loginRid:document.getElementById('loginRid'), loginPass:document.getElementById('loginPass'),
  btnLogin:document.getElementById('btnLogin'), loginStatus:document.getElementById('loginStatus'),
  newPass:document.getElementById('newPass'), btnCreate:document.getElementById('btnCreate'), createStatus:document.getElementById('createStatus'),
  panel:document.getElementById('walletPanel'),
  ridView:document.getElementById('ridView'), balView:document.getElementById('balView'), nonceView:document.getElementById('nonceView'),
  toRid:document.getElementById('toRid'), amount:document.getElementById('amount'), btnSend:document.getElementById('btnSend'), sendStatus:document.getElementById('sendStatus'),
  ridStake:document.getElementById('ridStake'),
  histBody:document.getElementById('histBody'), btnMoreHist:document.getElementById('btnMoreHist'),
  tabs:[...document.querySelectorAll('.tab')],
  btnExport:document.getElementById('btnExport'), btnImport:document.getElementById('btnImport'), impFile:document.getElementById('impFile'),
  settingsInfo:document.getElementById('settingsInfo'), exportStatus:document.getElementById('exportStatus')
};

// ===== WebCrypto helpers =====
function hex(buf){return Array.from(new Uint8Array(buf)).map(b=>b.toString(16).padStart(2,'0')).join('');}
async function sha256(s){const h=await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s)); return hex(h);}
async function pbkdf2(pass,salt,iters=300000){const key=await crypto.subtle.importKey('raw', new TextEncoder().encode(pass), 'PBKDF2', false, ['deriveKey']);return crypto.subtle.deriveKey({name:'PBKDF2', hash:'SHA-256', salt, iterations:iters}, key, {name:'AES-GCM', length:256}, false, ['encrypt','decrypt']);}
async function signHex(bytes){const sig=await crypto.subtle.sign('Ed25519', session.privKey, bytes); return hex(sig);}

// ===== Anti-bot PoW (на создание) =====
async function powCreate(){const ts=Date.now().toString();let n=0;for(;;){const h=await sha256(ts+'|'+n);if(h.startsWith('00000'))return{ts,nonce:n,h};n++; if(n%5000===0) await new Promise(r=>setTimeout(r));}}

// ===== Session =====
let session={rid:null, privKey:null, pubKeyRaw:null};

// ===== Balance/nonce =====
async function refreshBalance(){
  const enc=encodeURIComponent(session.rid);
  const r=await fetch(`${BASE}/balance/${enc}`); const j=await r.json();
  ui.balView.textContent=j.balance??0; ui.nonceView.textContent=j.nonce??0;
  return j;
}

// ===== Create wallet =====
ui.btnCreate.onclick = async ()=>{
  try{
    ui.createStatus.textContent='Генерация…';
    const pass = ui.newPass.value.trim();
    if(pass.length<8){ ui.createStatus.textContent='Сложнее пароль'; return; }
    await powCreate();

    const kp = await crypto.subtle.generateKey({name:'Ed25519'}, true, ['sign','verify']);
    const pubRaw = await crypto.subtle.exportKey('raw', kp.publicKey);
    const privRaw = await crypto.subtle.exportKey('pkcs8', kp.privateKey);

    const rid = 'Λ0@7.83Hzφ' + (await sha256(hex(pubRaw))).slice(0,6);

    const salt = crypto.getRandomValues(new Uint8Array(16));
    const iv   = crypto.getRandomValues(new Uint8Array(12));
    const aek  = await pbkdf2(pass, salt);
    const enc  = await crypto.subtle.encrypt({name:'AES-GCM', iv}, aek, privRaw);

    await idbPut({ rid, pub_hex: hex(pubRaw), enc_priv_b64: btoa(String.fromCharCode(...new Uint8Array(enc))), salt_hex: hex(salt), iv_hex: hex(iv) });

    ui.loginRid.value = rid; ui.loginPass.value = pass;
    ui.createStatus.textContent='OK — кошелёк создан';
  }catch(e){ console.error(e); ui.createStatus.textContent='Ошибка создания'; }
};

// ===== Login =====
ui.btnLogin.onclick = async ()=>{
  try{
    ui.loginStatus.textContent = 'Поиск…';
    const rid = ui.loginRid.value.trim(), pass = ui.loginPass.value.trim();
    const rec = await idbGet(rid);
    if(!rec){ ui.loginStatus.textContent = 'RID не найден в этом браузере'; return; }

    const salt = Uint8Array.from(rec.salt_hex.match(/.{2}/g).map(h=>parseInt(h,16)));
    const iv   = Uint8Array.from(rec.iv_hex.match(/.{2}/g).map(h=>parseInt(h,16)));
    const enc  = Uint8Array.from(atob(rec.enc_priv_b64), c=>c.charCodeAt(0));
    const aek  = await pbkdf2(pass, salt);
    const privRaw = await crypto.subtle.decrypt({name:'AES-GCM', iv}, aek, enc);
    const privKey = await crypto.subtle.importKey('pkcs8', privRaw, {name:'Ed25519'}, false, ['sign']);

    session = { rid, privKey, pubKeyRaw: Uint8Array.from(rec.pub_hex.match(/.{2}/g).map(h=>parseInt(h,16))).buffer };

    // UI
    document.getElementById('walletPanel').style.display='';
    document.getElementById('ridView').textContent = rid;
    document.getElementById('ridStake').textContent = rid;
    ui.loginStatus.textContent='OK';

    await refreshBalance();
    histCursor=null; ui.histBody.innerHTML=''; await loadHistoryPage();
  }catch(e){ console.error(e); ui.loginStatus.textContent='Ошибка входа'; }
};

// ===== Send TX =====
ui.btnSend.onclick = async ()=>{
  try{
    ui.sendStatus.textContent='Отправка…';
    const b=await refreshBalance();
    const to=ui.toRid.value.trim();
    const amt=Number(ui.amount.value);
    const nonce=(b.nonce??0)+1;

    const msg=`${session.rid}|${to}|${amt}|${nonce}`;
    const sig_hex = await signHex(new TextEncoder().encode(msg));

    // Лёгкий локальный троттлинг (anti-bot throttle)
    await new Promise(r=>setTimeout(r, 300 + Math.random()*500));

    const res = await fetch(`${BASE}/submit_tx`,{
      method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({from:session.rid,to,amount:amt,nonce,sig_hex})
    });
    const j=await res.json();
    ui.sendStatus.textContent = j.ok ? ('OK: '+(j.txid||'')) : ('ERR: '+j.info);
    await refreshBalance();
  }catch(e){ console.error(e); ui.sendStatus.textContent='Ошибка'; }
};

// ===== History (пагинация by height) =====
let histCursor=null;
async function loadHistoryPage(){
  const enc=encodeURIComponent(session.rid);
  let url=`${BASE}/archive/history/${enc}`; if(histCursor!=null) url+=`?before_height=${histCursor}`;
  const r=await fetch(url); const list=await r.json(); if(!Array.isArray(list) || list.length===0) return;
  histCursor = Number(list[list.length-1].height) - 1;
  const frag=document.createDocumentFragment();
  for(const t of list){
    const tr=document.createElement('tr');
    tr.innerHTML=`<td class="mono">${String(t.txid).slice(0,16)}…</td><td class="mono">${t.from}</td><td class="mono">${t.to}</td><td>${t.amount}</td><td>${t.height}</td><td>${t.ts??''}</td>`;
    ui.histBody.appendChild(tr);
  }
}
ui.btnMoreHist.onclick = ()=> loadHistoryPage();

// ===== Tabs =====
ui.tabs.forEach(tab=>{
  tab.onclick=()=>{
    ui.tabs.forEach(t=>t.classList.remove('active')); tab.classList.add('active');
    const name=tab.dataset.tab;
    document.getElementById('tab-send').classList.toggle('hide', name!=='send');
    document.getElementById('tab-stake').classList.toggle('hide', name!=='stake');
    document.getElementById('tab-history').classList.toggle('hide', name!=='history');
    document.getElementById('tab-settings').classList.toggle('hide', name!=='settings');
  };
});

// ===== Export / Import =====
ui.btnExport.onclick = async ()=>{
  const rec = await idbGet(session.rid);
  const blob = new Blob([JSON.stringify(rec)], {type:'application/json'});
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob);
  a.download = `logos_wallet_${session.rid}.json`; a.click();
  ui.exportStatus.textContent='Экспортирован зашифрованный бэкап';
};
ui.btnImport.onclick = ()=> ui.impFile.click();
ui.impFile.onchange = async (e)=>{
  try{
    const f=e.target.files[0]; const text=await f.text(); const rec=JSON.parse(text);
    if(!rec.rid || !rec.enc_priv_b64) throw new Error('bad backup');
    await idbPut(rec); ui.exportStatus.textContent='Импорт OK';
  }catch(err){ ui.exportStatus.textContent='Ошибка импорта'; }
};
```

---

## FILE: `/var/www/logos/wallet/js/api.js`

```js
export const API = "/api";

export async function apiGet(p){
  const r = await fetch(API+p);
  if(!r.ok) throw new Error(`GET ${p} -> ${r.status}`);
  return r.json();
}
export async function apiPost(p,b){
  const r = await fetch(API+p,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)});
  if(!r.ok){ const t=await r.text().catch(()=> ""); throw new Error(`POST ${p} -> ${r.status} ${t}`); }
  return r.json();
}
```

---

## FILE: `/var/www/logos/wallet/js/app.js`

```js
import { $, toast, canon, short, fmt } from "./core.js";
import { apiGet, apiPost } from "./core.js";   // API в core.js
import { currentRID, ensureSessionKey, signEd25519 } from "./vault.js";

async function loadPassport(){
  const rid = currentRID(); if(!rid){ toast("RID отсутствует"); return; }
  const [p,s,h] = await Promise.allSettled([
    apiGet(`/profile/${rid}`),
    apiGet(`/stake/summary/${rid}`),
    apiGet(`/history/${rid}?limit=50`)
  ]);
  const prof=p.status==="fulfilled"?p.value:{}, sum=s.status==="fulfilled"?s.value:{}, items=h.status==="fulfilled"?(h.value.items||[]):[];
  $('#kpiRid').textContent = rid;
  $('#kpiBal').textContent = fmt(prof.balance??0);
  $('#kpiNonce').textContent = (prof.nonce&&prof.nonce.next)??"-";
  $('#kpiHead').textContent = prof.head??"-";
  $('#kpiDelegated').textContent = fmt(sum.delegated??0);
  $('#kpiEntries').textContent  = fmt(sum.entries??0);
  $('#kpiClaimable').textContent= fmt(sum.claimable??0);

  $('#stakeValidator').value = rid;
  const tb=$('#histBody'); tb.innerHTML="";
  for(const it of items){
    const e=it.evt||{}; const cp=e.dir==="out"?e.to:(e.dir==="in"?e.from:(e.rid||"-"));
    const tr=document.createElement('tr');
    tr.innerHTML=`<td>${e.type||"transfer"}</td><td class="mono">${short(cp,24)}</td><td>${fmt(e.amount??0)}</td><td>${e.nonce??"-"}</td><td>${e.height??"-"}</td><td class="mono">${short(e.tx,28)}</td>`;
    tb.appendChild(tr);
  }
}

async function sendTx(){
  const rid=currentRID(); const to=($('#sendTo').value||"").trim(); const amount=Number($('#sendAmount').value||"0");
  if(!rid){ toast("Разблокируйте кошелёк"); return; }
  if(!to||!amount){ toast("RID/сумма?"); return;}
  const nn=await apiGet(`/nonce/${rid}`); const nonce=nn.next;
  await ensureSessionKey();
  const sig=await signEd25519(canon(rid,to,amount,nonce));
  const b=$('#btnSendTx'); const orig=b.textContent; b.disabled=true; b.textContent="Отправляем…";
  try{ const r=await apiPost(`/submit_tx`,{from:rid,to,amount,nonce,sig}); toast(r?.status==="queued"?"Tx отправлена":"Отправлено"); await loadPassport(); }
  catch(e){ toast("Ошибка: "+e.message); }
  finally{ b.disabled=false; b.textContent=orig; }
}
async function stakeDel(){ const rid=currentRID(); const a=Number($('#stakeAmount').value||"0"); if(!rid||!a){toast("RID/сумма?");return;} const r=await apiPost(`/stake/delegate`,{validator:rid,amount:a}); toast(r.ok?"Delegated":"Delegate failed"); await loadPassport(); }
async function stakeUn(){  const rid=currentRID(); const a=Number($('#stakeAmount').value||"0"); if(!rid||!a){toast("RID/сумма?");return;} const r=await apiPost(`/stake/undelegate`,{validator:rid,amount:a}); toast(r.ok?"Undelegated":"Undelegate failed"); await loadPassport(); }
async function stakeClaim(){const rid=currentRID(); if(!rid){toast("RID?");return;} const r=await apiPost(`/stake/claim`,{rid}); toast(r.ok?`Claimed ${r.claimed}`:"Claim failed"); await loadPassport(); }

document.addEventListener('DOMContentLoaded', ()=>{
  // если App уже показан (после unlock) — инициализируем
  if(!document.getElementById('viewApp').classList.contains('hidden')){
    loadPassport().catch(e=>toast(String(e)));
  }
  // действия
  $('#btnSendTx').onclick = ()=>sendTx().catch(e=>toast(String(e)));
  $('#btnStakeDel').onclick= ()=>stakeDel().catch(e=>toast(String(e)));
  $('#btnStakeUn').onclick = ()=>stakeUn().catch(e=>toast(String(e)));
  $('#btnStakeClaim').onclick=()=>stakeClaim().catch(e=>toast(String(e)));
});
```

---

## FILE: `/var/www/logos/wallet/js/app_wallet.js`

```js
import { $, toast, canon, short, fmtInt, be8, enc } from "./core.js";
import { apiGet, apiPost } from "./api.js";
import { currentRID, signEd25519, ensureSessionKey } from "./vault_bridge.js";

function ui(){
  return {
    passport: $("#viewApp"),
    ridOut:   $("#ridOut"),
    // поля отправки
    to: $("#sendTo"),
    amount: $("#sendAmount"),
    btnSend: $("#btnSendTx"),
    // профиль/паспорт KPI
    kpiBal: $("#kpiBal"), kpiNonce: $("#kpiNonce"), kpiHead: $("#kpiHead"),
    kpiDel: $("#kpiDelegated"), kpiEnt: $("#kpiEntries"), kpiClaim: $("#kpiClaimable"),
    // история
    histBody: $("#histBody"),
    // стейкинг
    val: $("#stakeValidator"), stakeAmt: $("#stakeAmount"),
    btnDel: $("#btnStakeDel"), btnUn: $("#btnStakeUn"), btnClaim: $("#btnStakeClaim"),
  };
}

async function loadPassport(){
  const rid = currentRID();
  const u = ui();
  u.ridOut.textContent = rid || "—";
  if(!rid){ toast("RID не найден. Разблокируйте кошелёк."); return; }

  const [p,s,h] = await Promise.allSettled([
    apiGet(`/profile/${rid}`),
    apiGet(`/stake/summary/${rid}`),
    apiGet(`/history/${rid}?limit=25`)
  ]);

  const prof = p.status==="fulfilled" ? p.value : {};
  const sum  = s.status==="fulfilled" ? s.value : {};
  const hist = h.status==="fulfilled" ? (h.value.items||[]) : [];

  u.kpiBal.textContent   = fmtInt(prof.balance ?? 0);
  u.kpiNonce.textContent = (prof.nonce && prof.nonce.next) ?? "-";
  u.kpiHead.textContent  = prof.head ?? "-";
  u.kpiDel.textContent   = fmtInt(sum.delegated ?? 0);
  u.kpiEnt.textContent   = fmtInt(sum.entries ?? 0);
  u.kpiClaim.textContent = fmtInt(sum.claimable ?? 0);

  // история
  u.histBody.innerHTML = "";
  for(const it of hist){
    const e = it.evt || {};
    const cp = e.dir==="out" ? e.to : (e.dir==="in" ? e.from : (e.rid||"-"));
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${e.type||"transfer"}</td>
      <td class="mono">${short(cp,24)}</td>
      <td>${fmtInt(e.amount ?? 0)}</td>
      <td>${e.nonce ?? "-"}</td>
      <td>${e.height ?? "-"}</td>
      <td class="mono">${short(e.tx,28)}</td>`;
    u.histBody.appendChild(tr);
  }
}

async function sendTx(){
  const rid = currentRID();
  const u = ui();
  const to = (u.to.value||"").trim();
  const amount = Number(u.amount.value||"0");
  if(!rid){ toast("Разблокируйте кошелёк"); return; }
  if(!to || !amount){ toast("Укажите получателя и сумму"); return; }

  // ensure key in memory (может запросить пароль один раз)
  await ensureSessionKey();

  const nn = await apiGet(`/nonce/${rid}`);
  const nonce = nn.next;
  const msg = canon(rid, to, amount, nonce);
  const sigB64 = await signEd25519(msg);

  u.btnSend.disabled = true;
  u.btnSend.textContent = "Отправляем…";
  try{
    const res = await apiPost(`/submit_tx`, {from: rid, to, amount, nonce, sig: sigB64});
    toast(res?.status==="queued" ? "Tx отправлена" : "Отправлено");
    await loadPassport();
  }catch(e){ toast("Ошибка: "+e.message); }
  finally{ u.btnSend.disabled=false; u.btnSend.textContent = "Отправить"; }
}

async function stakeDelegate(){
  const u = ui(); const rid = currentRID(); const a = Number(u.stakeAmt.value||"0");
  if(!rid || !a){ toast("RID/сумма?"); return; }
  try{
    const r = await apiPost(`/stake/delegate`, {validator: rid, amount: a});
    toast(r.ok ? "Delegated" : "Delegate failed");
    await loadPassport();
  }catch(e){ toast("Ошибка: "+e.message); }
}
async function stakeUndelegate(){
  const u = ui(); const rid = currentRID(); const a = Number(u.stakeAmt.value||"0");
  if(!rid || !a){ toast("RID/сумма?"); return; }
  try{
    const r = await apiPost(`/stake/undelegate`, {validator: rid, amount: a});
    toast(r.ok ? "Undelegated" : "Undelegate failed");
    await loadPassport();
  }catch(e){ toast("Ошибка: "+e.message); }
}
async function stakeClaim(){
  const rid = currentRID();
  if(!rid){ toast("RID?"); return; }
  try{
    const r = await apiPost(`/stake/claim`, {rid});
    toast(r.ok ? `Claimed ${r.claimed}` : "Claim failed");
    await loadPassport();
  }catch(e){ toast("Ошибка: "+e.message); }
}

export function initAppWallet(){
  $("#kpiRid").textContent = currentRID() || "—";
  $("#btnSendTx").addEventListener("click", ()=>sendTx().catch(e=>toast(String(e))));
  $("#btnStakeDel").addEventListener("click", ()=>stakeDelegate().catch(e=>toast(String(e))));
  $("#btnStakeUn").addEventListener("click", ()=>stakeUndelegate().catch(e=>toast(String(e))));
  $("#btnStakeClaim").addEventListener("click", ()=>stakeClaim().catch(e=>toast(String(e))));
  loadPassport().catch(e=>toast(String(e)));
}
```

---

## FILE: `/var/www/logos/wallet/js/core.js`

```js
export const enc = new TextEncoder();
export const API = "/api";
export const $ = (sel)=>document.querySelector(sel);

export function toast(m){ const t=document.getElementById('toast'); if(!t) return; t.textContent=m; t.classList.add('show'); setTimeout(()=>t.classList.remove('show'),2000); }

export function be8(n){ const a=new Uint8Array(8); new DataView(a.buffer).setBigUint64(0, BigInt(n)); return a; }
export function cat(...xs){ let L=0; for(const a of xs)L+=a.length; const out=new Uint8Array(L); let o=0; for(const a of xs){ out.set(a,o); o+=a.length; } return out; }
export function canon(from,to,amount,nonce){ return cat(new TextEncoder().encode(from),Uint8Array.of(0x7c),new TextEncoder().encode(to),Uint8Array.of(0x7c),be8(amount),Uint8Array.of(0x7c),be8(nonce)); }
export function fmt(x){ return (x??0).toLocaleString('ru-RU'); }
export function short(s,n=28){ if(!s) return "-"; return s.length>n ? s.slice(0,n-3)+"…" : s; }
const B58="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";
export function b58(bytes){ let x=0n; for(const v of bytes) x=(x<<8n)+BigInt(v); let s=""; while(x>0n){const r=Number(x%58n);x/=58n;s=B58[r]+s;} for(const v of bytes){ if(v===0)s="1"+s; else break;} return s||"1"; }

export async function apiGet(p){ const r=await fetch(API+p); if(!r.ok) throw new Error(`GET ${p} -> ${r.status}`); return r.json(); }
export async function apiPost(p,b){ const r=await fetch(API+p,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)}); if(!r.ok){const t=await r.text().catch(()=> ""); throw new Error(`POST ${p} -> ${r.status} ${t}`);} return r.json(); }
```

---

## FILE: `/var/www/logos/wallet/js/unlock.js`

```js
import { $, toast } from "./core.js";
import { hasVault, createPairAndBackup, finalizeCreate, importVault, unlockWith, currentRID } from "./vault.js";

function show(id){ ['#viewLanding','#viewCreatePwd','#viewBackup','#viewImport','#viewUnlock'].forEach(v=>$(v).classList.add('hidden')); $(id).classList.remove('hidden'); }
function showApp(){ document.getElementById('lockOverlay').style.display='none'; ['#viewApp','#viewSend','#viewStake','#viewHistory'].forEach(id=>$(id).classList.remove('hidden')); }

document.addEventListener('DOMContentLoaded', ()=>{
  $('#rpHost').textContent = location.host + ' JS✓';
  if(hasVault()) show('#viewUnlock'); else show('#viewLanding');

  // роутинг
  $('#goCreate').onclick = ()=> show('#viewCreatePwd');
  $('#goImport').onclick = ()=> show('#viewImport');
  $('#goUnlock').onclick = ()=> show('#viewUnlock');
  $('#back1').onclick = ()=> show('#viewLanding');
  $('#back2').onclick = ()=> show('#viewCreatePwd');
  $('#back3').onclick = ()=> show('#viewLanding');

  // создание шаг1
  $('#createNext').onclick = async ()=>{
    const p1=$('#newPwd1').value.trim(), p2=$('#newPwd2').value.trim();
    if(p1.length<8){ toast('Пароль минимум 8 символов'); return;}
    if(p1!==p2){ toast('Пароли не совпадают'); return;}
    try{
      const b64 = await createPairAndBackup(p1);
      $('#backupArea').value = b64; $('#chkSaved').checked=false; $('#finishCreate').disabled=true;
      show('#viewBackup');
    }catch(e){ toast('Крипто-ошибка. Обнови браузер.'); }
  };
  $('#chkSaved').onchange = ()=> $('#finishCreate').disabled = !$('#chkSaved').checked;
  $('#finishCreate').onclick = async ()=>{
    try{ await finalizeCreate(); toast('Кошелёк создан'); show('#viewUnlock'); }
    catch(e){ toast('Не удалось сохранить'); }
  };

  // импорт
  $('#doImport').onclick = async ()=>{
    const b64=$('#impKey').value.trim(), p1=$('#impPwd1').value.trim(), p2=$('#impPwd2').value.trim();
    if(!b64){ toast('Вставьте ключ'); return;}
    if(p1.length<8){ toast('Пароль минимум 8 символов'); return;}
    if(p1!==p2){ toast('Пароли не совпадают'); return;}
    try{ await importVault(b64,p1); toast('Импорт выполнен'); show('#viewUnlock'); }
    catch(e){ toast('Импорт не удался'); }
  };

  // разблокировать
  $('#btnUnlock').onclick = async ()=>{
    const pass=$('#unPwd').value.trim();
    if(pass.length<8){ toast('Пароль минимум 8 символов'); return; }
    const b=$('#btnUnlock'); const orig=b.textContent; b.disabled=true; b.textContent='Разблокируем…';
    try{
      await Promise.race([ unlockWith(pass), new Promise((_,rej)=>setTimeout(()=>rej(new Error('TIMEOUT')),12000)) ]);
      $('#kpiRid').textContent = currentRID() || "—";
      showApp(); toast('Готово');
    }catch(e){
      const code=String(e&&e.message||e);
      if(code==='NO_KEY') toast('Кошелёк не найден');
      else if(code==='BAD_PASS') toast('Неверный пароль');
      else if(code==='TIMEOUT') toast('Долго думает… повторите');
      else toast('Ошибка разблокировки');
    }finally{ b.disabled=false; b.textContent=orig; }
  };

  $('#btnReset').onclick = ()=>{ if(confirm('Очистить локальный ключ?')){ try{localStorage.removeItem('logos_secure_v3_vault');}catch{} toast('Сброшено'); show('#viewLanding'); } };
});
```

---

## FILE: `/var/www/logos/wallet/js/vault.js`

```js
import { enc, b58, toast } from "./core.js";

const LS="logos_secure_v3_vault";
const ITER=250000;

function getVault(){ const raw=localStorage.getItem(LS); if(!raw) return null; try{ return JSON.parse(raw);}catch{ return null; } }
function saveVault(salt,iv,ct,pub){ localStorage.setItem(LS, JSON.stringify({
  salt:btoa(String.fromCharCode(...salt)), iv:btoa(String.fromCharCode(...iv)), ct:btoa(String.fromCharCode(...ct)), pub:btoa(String.fromCharCode(...pub)), iter:ITER
})); }
async function kdf(pass,salt){ const base=await crypto.subtle.importKey("raw",enc.encode(pass),{name:"PBKDF2"},false,["deriveKey"]); return crypto.subtle.deriveKey({name:"PBKDF2",salt,iterations:ITER,hash:"SHA-256"},base,{name:"AES-GCM",length:256},false,["encrypt","decrypt"]); }

export const hasVault = ()=> !!getVault();
export const currentRID = ()=>{ const v=getVault(); if(!v) return ""; const pub=Uint8Array.from(atob(v.pub),c=>c.charCodeAt(0)); return b58(pub); };

let __priv=null, __pub=null, __timer=null;
function sessionSet(priv,pub){ __priv=priv; __pub=pub; clearTimeout(__timer); __timer=setTimeout(()=>{__priv=null;__pub=null;}, 5*60*1000); }
export const hasSession = ()=> !!__priv;

export async function createPairAndBackup(pw){
  const kp=await crypto.subtle.generateKey({name:"Ed25519"},true,["sign","verify"]);
  const pkcs8=new Uint8Array(await crypto.subtle.exportKey("pkcs8",kp.privateKey));
  const pub=new Uint8Array(await crypto.subtle.exportKey("raw",kp.publicKey));
  sessionStorage.setItem('TMP_PK', btoa(String.fromCharCode(...pkcs8)));
  sessionStorage.setItem('TMP_PW', pw);
  sessionStorage.setItem('TMP_PUB', btoa(String.fromCharCode(...pub)));
  return btoa(String.fromCharCode(...pkcs8));
}
export async function finalizeCreate(){
  const b64=sessionStorage.getItem('TMP_PK'), p1=sessionStorage.getItem('TMP_PW'), pubB=sessionStorage.getItem('TMP_PUB');
  if(!b64||!p1||!pubB) throw new Error("CREATE_SESSION_LOST");
  const pk = Uint8Array.from(atob(b64),c=>c.charCodeAt(0));
  const pub= Uint8Array.from(atob(pubB),c=>c.charCodeAt(0));
  const s=new Uint8Array(16); crypto.getRandomValues(s);
  const iv=new Uint8Array(12); crypto.getRandomValues(iv);
  const key=await kdf(p1,s); const ct=new Uint8Array(await crypto.subtle.encrypt({name:"AES-GCM",iv},key,pk));
  saveVault(s,iv,ct,pub); sessionStorage.clear();
}
export async function importVault(b64,p1){
  const pk = Uint8Array.from(atob(b64),c=>c.charCodeAt(0));
  const tmp=await crypto.subtle.generateKey({name:"Ed25519"},true,["sign","verify"]);
  const pub=new Uint8Array(await crypto.subtle.exportKey("raw",tmp.publicKey));
  const s=new Uint8Array(16); crypto.getRandomValues(s);
  const iv=new Uint8Array(12); crypto.getRandomValues(iv);
  const key=await kdf(p1,s); const ct=new Uint8Array(await crypto.subtle.encrypt({name:"AES-GCM",iv},key,pk));
  saveVault(s,iv,ct,pub);
}
export async function unlockWith(pass){
  const v=getVault(); if(!v) throw new Error("NO_KEY");
  const s=Uint8Array.from(atob(v.salt),c=>c.charCodeAt(0));
  const iv=Uint8Array.from(atob(v.iv),c=>c.charCodeAt(0));
  const ct=Uint8Array.from(atob(v.ct),c=>c.charCodeAt(0));
  const key=await kdf(pass,s);
  const pk8=await crypto.subtle.decrypt({name:"AES-GCM",iv},key,ct).catch(()=>{throw new Error("BAD_PASS")});
  const priv=await crypto.subtle.importKey("pkcs8",pk8,{name:"Ed25519"},false,["sign"]);
  const pub =Uint8Array.from(atob(v.pub),c=>c.charCodeAt(0));
  sessionSet(priv,pub);
}
export async function ensureSessionKey(){
  if(__priv) return {priv:__priv, pub:__pub};
  const v=getVault(); if(!v){ toast("Кошелёк не найден"); throw new Error("NO_KEY"); }
  const pass = prompt("Пароль для подписи"); if(!pass||pass.length<8){ throw new Error("PASS_SHORT"); }
  await unlockWith(pass); return {priv:__priv, pub:__pub};
}
export async function signEd25519(bytes){
  const {priv}=await ensureSessionKey();
  const sig=new Uint8Array(await crypto.subtle.sign({name:"Ed25519"},priv,bytes));
  let bin=""; for(let i=0;i<sig.length;i++) bin+=String.fromCharCode(sig[i]); return btoa(bin);
}
```

---

## FILE: `/var/www/logos/wallet/js/vault_bridge.js`

```js
import { enc, b58, toast } from "./core.js";

// Шифрованный сейф (как на экране unlock)
const LS = "logos_secure_v3_vault";
const ITER = 250000;

function getVault(){
  const raw = localStorage.getItem(LS);
  if(!raw) return null;
  try{ return JSON.parse(raw); }catch{ return null; }
}

async function kdf(pass, salt){
  const base = await crypto.subtle.importKey("raw", enc.encode(pass), {name:"PBKDF2"}, false, ["deriveKey"]);
  return crypto.subtle.deriveKey({name:"PBKDF2", salt, iterations:ITER, hash:"SHA-256"}, base, {name:"AES-GCM", length:256}, false, ["encrypt","decrypt"]);
}

// Сессионный приватник (в памяти страницы), авто-очистка через 5 минут
let __priv = null, __pubRaw = null, __timer = null;
function sessionSet(priv, pub){
  __priv = priv; __pubRaw = pub;
  clearTimeout(__timer); __timer = setTimeout(()=>{ __priv=null; __pubRaw=null; }, 5*60*1000);
}

export function hasSession(){ return !!__priv; }
export function currentRID(){ const v=getVault(); if(!v) return ""; const pub = Uint8Array.from(atob(v.pub),c=>c.charCodeAt(0)); return b58(pub); }

// Гарантирует, что в памяти есть приватник. Если нет — запросит пароль и расшифрует.
export async function ensureSessionKey(){
  if(__priv) return {priv:__priv, pubRaw: __pubRaw};
  const v = getVault();
  if(!v){ toast("Кошелёк не найден. Создайте/импортируйте."); throw new Error("NO_KEY"); }
  const pass = prompt("Введите пароль кошелька для подписи");
  if(!pass || pass.length<8){ toast("Пароль минимум 8 символов"); throw new Error("PASS_SHORT"); }

  const salt = Uint8Array.from(atob(v.salt), c=>c.charCodeAt(0));
  const iv   = Uint8Array.from(atob(v.iv),   c=>c.charCodeAt(0));
  const ct   = Uint8Array.from(atob(v.ct),   c=>c.charCodeAt(0));
  const pub  = Uint8Array.from(atob(v.pub),  c=>c.charCodeAt(0));

  const key  = await kdf(pass, salt);
  let pkcs8;
  try{ pkcs8 = await crypto.subtle.decrypt({name:"AES-GCM", iv}, key, ct); }
  catch{ toast("Неверный пароль"); throw new Error("BAD_PASS"); }

  const priv = await crypto.subtle.importKey("pkcs8", pkcs8, {name:"Ed25519"}, false, ["sign"]);
  sessionSet(priv, pub);
  return {priv, pubRaw: pub};
}

export async function signEd25519(bytes){
  const { priv } = await ensureSessionKey();
  const sig = new Uint8Array(await crypto.subtle.sign({name:"Ed25519"}, priv, bytes));
  let bin=""; for(let i=0;i<sig.length;i++) bin += String.fromCharCode(sig[i]);
  return btoa(bin);
}
```

---

## FILE: `/var/www/logos/wallet/css/styles.css`

```css
:root{color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:#0b1016;color:#e7eef7;font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
.wrap{max-width:1100px;margin:24px auto;padding:0 16px}
.card{background:#0f1723;border:1px solid #243048;border-radius:16px;padding:18px;margin:12px 0}
h1,h2,h3{margin:0 0 10px}
.muted{color:#9fb2c9}
.row{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.grid{display:grid;gap:12px}
.cols-2{grid-template-columns:1fr 1fr}
.cols-3{grid-template-columns:1fr 1fr 1fr}
.mt10{margin-top:10px}
@media(max-width:980px){.cols-2,.cols-3{grid-template-columns:1fr}}
input,button,textarea{border-radius:12px;border:1px solid #28344c;background:#0d1420;color:#e7eef7;padding:12px;width:100%}
textarea{min-height:100px;resize:vertical}
input:focus,textarea:focus{outline:none;border-color:#3a70ff;box-shadow:0 0 0 2px #3a70ff26}
button{background:#3366ff;border:none;cursor:pointer;transition:.15s}
button.secondary{background:#1a2333}
button.ghost{background:#0d1420;border:1px dashed #2a3a56}
.badge{background:#141e2d;border:1px solid #2a3a56;border-radius:999px;padding:6px 10px;font-size:12px}
.kpi{display:flex;gap:8px;flex-wrap:wrap;margin-top:6px}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;word-break:break-all}
.table{width:100%;border-collapse:collapse}
.table th,.table td{border-bottom:1px solid #1a2436;padding:10px 8px;text-align:left;font-size:13px}
.table th{color:#9fb2c9;font-weight:600}
.scroll{overflow:auto}
.toast{position:fixed;right:16px;bottom:16px;display:none;background:#0e1520;border:1px solid #20406f;color:#bfe0ff;padding:12px 14px;border-radius:10px;box-shadow:0 10px 30px rgba(0,0,0,.35);max-width:80%}
.toast.show{display:block}

/* Secure overlay */
#lockOverlay{position:fixed;inset:0;background:rgba(11,16,22,.96);backdrop-filter:saturate(120%) blur(2px);display:flex;align-items:center;justify-content:center;z-index:9999}
#lockCard{width:min(620px,92%);background:#0f1723;border:1px solid #243048;border-radius:18px;padding:18px}
#brand{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
#phish{background:#0c1420;border:1px solid #2a3a56;border-radius:12px;padding:10px;font-size:12px;color:#9fb2c9}
.hidden{display:none}
```
