# LOGOS — Directory Book: /var/www/logos/wallet3

_Generated: 2025-12-31T06:43:51Z_

**Part:** 1

---

## STRUCTURE

```text
/var/www/logos/wallet3
```

---

## FILES (FULL SOURCE)


### FILE: /var/www/logos/wallet3/app.v3.js

```
const API = location.origin + '/api/';
const enc = new TextEncoder();

// utils
const $ = s => document.querySelector(s);
const toHex   = b => [...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('');
const fromHex = h => new Uint8Array((h.match(/.{1,2}/g)||[]).map(x=>parseInt(x,16)));
function u64le(n){ const b=new Uint8Array(8); new DataView(b.buffer).setBigUint64(0, BigInt(n), true); return b; }
async function sha256(bytes){ const d=await crypto.subtle.digest('SHA-256', bytes); return new Uint8Array(d); }
async function fetchJSON(url, opts){
  const r = await fetch(url, opts);
  const t = await r.text();
  try { const j = t?JSON.parse(t):{}; if(!r.ok) throw j; return j; }
  catch(e){ throw { ok:false, error:(typeof e==='object'&&e.error)?e.error:(t||'not json'), status:r.status||0 }; }
}

// session/keys
const PASS = sessionStorage.getItem('logos_pass');
const RID  = sessionStorage.getItem('logos_rid');
if (!PASS || !RID) { location.replace('../wallet/login.html'); throw new Error('locked'); } // переиспользуем старую страницу логина

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
  if(!META){ sessionStorage.clear(); location.replace('../wallet/login.html'); return; }
  KEYS=await importKey(PASS, META);
})();

// canonical + sign
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

// API
const getBalance=(rid)=>fetchJSON(`${API}balance/${encodeURIComponent(rid)}`);
const submitTxBatch=(txs)=>fetchJSON(`${API}submit_tx_batch`,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({txs})});
const stakeDelegate=(delegator,validator,amount)=>fetchJSON(`${API}stake/delegate`,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({delegator,validator,amount:Number(amount)})});
const stakeUndelegate=(delegator,validator,amount)=>fetchJSON(`${API}stake/undelegate`,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({delegator,validator,amount:Number(amount)})});
const stakeClaim=(delegator,validator)=>fetchJSON(`${API}stake/claim`,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({delegator,validator,amount:0})});
const stakeMy=(rid)=>fetchJSON(`${API}stake/my/${encodeURIComponent(rid)}`);

// UI
$('#btn-balance')?.addEventListener('click', async ()=>{
  try{ const rid=($('#rid-balance')?.value||RID).trim(); const j=await getBalance(rid); $('#out-balance') && ($('#out-balance').textContent=JSON.stringify(j)); }
  catch(e){ $('#out-balance') && ($('#out-balance').textContent=`ERR: ${JSON.stringify(e)}`); }
});
$('#btn-nonce')?.addEventListener('click', async ()=>{
  try{ const j=await getBalance(RID); const n=$('#nonce'); if(n) n.value=String(j.nonce||0); }catch(e){}
});
$('#btn-send')?.addEventListener('click', async ()=>{
  try{
    const to=$('#to')?.value.trim(), amount=$('#amount')?.value.trim(), nonce=$('#nonce')?.value.trim();
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
    const val=($('#validator')?.value||RID).trim();
    const amount=$('#stake-amount')?.value.trim();
    const res=await stakeDelegate(RID,val,amount);
    $('#out-stake') && ($('#out-stake').textContent=JSON.stringify(res));
  }catch(e){ $('#out-stake') && ($('#out-stake').textContent=`ERR: ${JSON.stringify(e)}`); }
});
$('#btn-undelegate')?.addEventListener('click', async ()=>{
  try{
    const val=($('#validator')?.value||RID).trim();
    const amount=$('#stake-amount')?.value.trim();
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

### FILE: /var/www/logos/wallet3/index.html

```
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta http-equiv="Cache-Control" content="no-store, no-cache, must-revalidate"/>
  <meta http-equiv="Pragma" content="no-cache"/>
  <meta http-equiv="Expires" content="0"/>
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; connect-src 'self'; img-src 'self'; script-src 'self'; style-src 'self'">
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>LOGOS Wallet (v3)</title>
  <style>
    body{font-family:system-ui,Roboto,Arial,sans-serif;background:#0b0e11;color:#e6e6e6;margin:0}
    header{padding:12px 20px;background:#12161a;border-bottom:1px solid #1b2026}
    main{padding:20px} h3{margin:0}
    section{margin-bottom:20px}
    input,button{padding:8px 10px;border-radius:6px;border:none;font-size:14px}
    button{background:#2d6cdf;color:#fff;cursor:pointer;margin:4px 2px}
    .out{margin-top:10px;font-family:monospace;font-size:13px;white-space:pre-wrap}
  </style>
  <script>
    (async()=>{ // убьём SW/Cache на всякий случай
      try{
        if('serviceWorker' in navigator){
          for(const r of await navigator.serviceWorker.getRegistrations()) try{await r.unregister()}catch{}
        }
        if(window.caches){ for(const k of await caches.keys()) try{await caches.delete(k)}catch{} }
      }catch(e){}
    })();
  </script>
</head>
<body>
<header>
  <h3>LOGOS Wallet (v3)</h3>
  <div>node: <span id="node-url"></span> | head: <span id="head"></span></div>
</header>
<main>
  <section>
    <h4>Настройки</h4>
    <div>RID: <span id="rid"></span></div>
    <div>Баланс: <span id="balance"></span> | Nonce: <span id="nonce-show"></span></div>
    <input id="rid-balance" placeholder="RID для проверки"/>
    <button id="btn-balance">Баланс</button>
    <div id="out-balance" class="out"></div>
  </section>

  <section>
    <h4>Отправка</h4>
    <input id="to" placeholder="RID получателя"/>
    <input id="amount" type="number" placeholder="Сумма (микро-LGN)"/>
    <input id="nonce" type="number" placeholder="Nonce"/>
    <button id="btn-nonce">NONCE</button>
    <button id="btn-send">Отправить</button>
    <div id="out-send" class="out"></div>
  </section>

  <section>
    <h4>Стейкинг</h4>
    <input id="validator" placeholder="RID валидатора"/>
    <input id="stake-amount" type="number" placeholder="Сумма (микро-LGN)"/>
    <button id="btn-delegate">Delegate</button>
    <button id="btn-undelegate">Undelegate</button>
    <button id="btn-claim">Claim</button>
    <button id="btn-my">Мои делегации</button>
    <div id="out-stake" class="out"></div>
    <div id="out-my" class="out"></div>
  </section>
</main>

<script src="app.v3.js?v=3"></script>
<script>
  document.getElementById('node-url').textContent = location.origin;
  (async function tick(){
    try{
      const h=await (await fetch(location.origin+'/api/head')).json();
      document.getElementById('head').textContent=h.height;
      const rid=sessionStorage.getItem('logos_rid');
      if(rid){
        const bj=await (await fetch(location.origin+'/api/balance/'+encodeURIComponent(rid))).json();
        document.getElementById('rid').textContent=rid;
        document.getElementById('balance').textContent=bj.balance;
        document.getElementById('nonce-show').textContent=bj.nonce;
      }
    }catch(e){}
    setTimeout(tick,1500);
  })();
</script>
</body>
</html>

```
