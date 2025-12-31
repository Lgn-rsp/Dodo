# LOGOS — Directory Book: /var/www/logos/www

_Generated: 2025-12-31T06:43:51Z_

**Part:** 1

---

## STRUCTURE

```text
/var/www/logos/www
/var/www/logos/www/wallet
/var/www/logos/www/explorer
/var/www/logos/www/assets
/var/www/logos/www/wallet3
```

---

## FILES (FULL SOURCE)


### FILE: /var/www/logos/www/index.html

```
<!doctype html>
<html lang="ru" translate="no">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>LOGOS Wallet</title>
<style>
:root{--bg:#0b1016;--card:#0f1720;--txt:#e6eef6;--mut:#93a4b3;--btn:#2b7bff;--bd:rgba(255,255,255,.06)}
*{box-sizing:border-box} body{margin:0;background:linear-gradient(180deg,#0a0f15,#0b1117);color:var(--txt);font:16px/1.45 system-ui,Segoe UI,Roboto,Arial}
.wrap{max-width:980px;margin:32px auto;padding:0 16px}
h1{margin:0 0 18px;font-size:36px}
.card{background:rgba(255,255,255,.03);border:1px solid var(--bd);border-radius:14px;padding:16px;margin:18px 0}
.row{display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.chip{background:rgba(255,255,255,.04);padding:8px 10px;border-radius:10px;color:var(--mut);font-size:12px}
.btn{background:var(--btn);color:#fff;border:0;padding:10px 14px;border-radius:10px;cursor:pointer;pointer-events:auto}
.btn.ghost{background:rgba(255,255,255,.06);color:var(--mut)}
input,textarea{width:100%;padding:10px;border-radius:10px;border:1px solid var(--bd);background:rgba(0,0,0,.15);color:var(--txt)}
label{display:block;margin:8px 0 6px;color:var(--mut);font-size:14px}
pre{background:rgba(0,0,0,.18);border:1px solid var(--bd);border-radius:10px;padding:12px;overflow:auto;font:12px/1.4 ui-monospace,Consolas,monospace}
#debugBanner{position:fixed;right:18px;bottom:18px;background:#ff2b2b;color:#fff;padding:10px;border-radius:8px;display:none;z-index:9999;max-width:320px}
</style>
<!-- если хочешь, замени DEFAULT_RID на свой -->
<script>window.DEFAULT_RID = window.DEFAULT_RID || "Gs19ZANA2cdzag8Dtz1ppvBE1h9irV3d5YHrP62RzdLY";</script>
</head>
<body>
  <div class="wrap">
    <h1>LOGOS Wallet</h1>

    <section class="card">
      <div class="row">
        <div id="chipBalance" class="chip">balance: —</div>
        <div id="chipNonce"   class="chip">nonce: —</div>
        <div id="chipHead"    class="chip">head: —</div>
      </div>

      <label for="ridInput">RID (текущий аккаунт)</label>
      <div class="row">
        <input id="ridInput" type="text" placeholder="RID (base58 pubkey)" style="max-width:520px">
        <button id="copyBtn" class="btn">Copy</button>
        <button id="balanceBtn" class="btn ghost">Баланс</button>
        <button id="syncBtn" class="btn ghost">SYNC</button>
      </div>

      <label>Профиль (raw)</label>
      <pre id="profileJson">{}</pre>
    </section>

    <section class="card">
      <h2>Отправка</h2>
      <div style="display:flex;gap:12px">
        <div style="flex:1">
          <label for="txRid">RID получателя</label>
          <input id="txRid" type="text" placeholder="RID получателя">
        </div>
        <div style="flex:1">
          <label for="txAmount">Сумма</label>
          <input id="txAmount" type="text" placeholder="amount (u64)">
        </div>
      </div>

      <label for="txSig">SIG (HEX/Base64) — оставь пустым, если браузер подпишет</label>
      <textarea id="txSig" rows="2" placeholder="опционально: подпись"></textarea>
      <div style="margin-top:10px"><button id="txSend" class="btn">Отправить</button></div>
      <pre id="txResult">{}</pre>
    </section>

    <section class="card">
      <h2>Стейкинг</h2>
      <div class="row" style="gap:8px;margin-bottom:8px">
        <div id="stDelegated" class="chip">delegated: —</div>
        <div id="stEntries"   class="chip">entries: —</div>
        <div id="stClaimable" class="chip">claimable: —</div>
      </div>
      <label for="stRid">RID валидатора (SELF = свой RID)</label>
      <input id="stRid" type="text" placeholder="RID валидатора">
      <div style="display:flex;gap:12px;margin-top:10px">
        <div style="flex:1">
          <label for="stAmount">Сумма для Delegate</label>
          <input id="stAmount" type="text" placeholder="amount (u64)">
        </div>
      </div>
      <div style="margin-top:10px">
        <button id="stDelegate" class="btn">Delegate</button>
        <button id="stUndelegate" class="btn ghost">Undelegate</button>
        <button id="stClaim" class="btn ghost">Claim</button>
      </div>
      <pre id="stResult">{}</pre>
    </section>

    <section class="card">
      <h2>История операций</h2>
      <button id="btnHist" class="btn ghost">Показать</button>
      <div style="overflow:auto;margin-top:10px">
        <table id="historyTbl">
          <thead><tr><th>height</th><th>hash</th><th>from</th><th>to</th><th>amount</th><th>fee</th><th>nonce</th></tr></thead>
          <tbody></tbody>
        </table>
      </div>
    </section>
  </div>

  <div id="debugBanner"></div>

  <script>
  (function(){
    const API=""; // если используешь API — впиши URL, иначе оставь пустым
    const LS_RID="logos_current_rid";
    const $=id=>document.getElementById(id);
    const asJSON=r=>r.json().catch(()=>({}));
    const norm=v=>(v||"").trim().replace(/^["']+|["']+$/g,"");
    const onlyB58=el=>el&&el.addEventListener("input",()=>el.value=el.value.replace(/[^123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz]/g,""));
    const onlyNum=el=>el&&el.addEventListener("input",()=>el.value=el.value.replace(/[^\d]/g,""));
    const safe=async(u,o={})=>{ try{ const r=await fetch(u,o); return {ok:r.ok,status:r.status,body:await asJSON(r)} } catch(e){ return {ok:false,status:0,body:{ok:false,error:String(e)}} } };

    function showDebug(msg,ttl=0){
      const el=$('debugBanner'); el.textContent = (new Date()).toLocaleTimeString()+': '+msg; el.style.display='block';
      console.error('WALLET-DEBUG:', msg);
      if(ttl>0) setTimeout(()=>el.style.display='none', ttl);
    }

    function setProfile(p){
      $('profileJson').textContent = JSON.stringify(p,null,2);
      $('chipBalance').textContent = "balance: "+(p.balance??"—");
      $('chipNonce').textContent   = "nonce: "+(p.nonce??"—");
      $('chipHead').textContent    = "head: "+(p.head??"—");
      $('stDelegated').textContent = "delegated: "+(p.delegated??"—");
      $('stEntries').textContent   = "entries: "+(p.entries??"—");
      $('stClaimable').textContent = "claimable: "+(p.claimable??"—");
    }

    async function loadHead(){ if(!API) return; const r = await safe(`${API}/head`); if(r.ok) $('chipHead').textContent = "head: "+(r.body.height??"—"); }
    async function loadProfile(){
      try{
        const rid = norm($('ridInput').value) || localStorage.getItem(LS_RID) || window.DEFAULT_RID || "";
        if(!rid){ $('profileJson').textContent = "{}"; showDebug('RID не задан',3000); return; }
        $('ridInput').value = rid;
        localStorage.setItem(LS_RID, rid);
        if(!API){ setProfile({rid}); return; }
        const r = await safe(`${API}/profile/${encodeURIComponent(rid)}`);
        if(!r.ok){ setProfile({ok:false,error:r.body?.error||`profile ${r.status}`}); showDebug('Ошибка profile: '+JSON.stringify(r.body),5000); return; }
        setProfile(r.body);
      }catch(e){ showDebug('loadProfile exception: '+e,5000); }
    }

    async function loadHistory(){
      try{
        const rid = localStorage.getItem(LS_RID) || norm($('ridInput').value);
        if(!rid){ showDebug('history: rid пуст',3000); return; }
        if(!API){ showDebug('history: API пуст, пропускаю',2000); return; }
        const r = await safe(`${API}/history/${encodeURIComponent(rid)}`);
        const tbody=document.querySelector("#historyTbl tbody"); tbody.innerHTML="";
        const it = (r.ok&&Array.isArray(r.body.items))?r.body.items:[];
        if(!it.length){ tbody.innerHTML="<tr><td colspan='7'>нет записей</td></tr>"; return; }
        for(const x of it){
          const tr=document.createElement('tr');
          tr.innerHTML = `<td>${x.height??""}</td><td>${(x.hash||"").slice(0,10)}</td><td>${x.from||""}</td><td>${x.to||""}</td><td>${x.amount??""}</td><td>${x.fee??""}</td><td>${x.nonce??""}</td>`;
          tbody.appendChild(tr);
        }
      }catch(e){ showDebug('loadHistory err: '+e,4000); }
    }

    async function sendTx(){
      try{
        const from = norm($('ridInput').value);
        const to = norm($('txRid').value);
        const amt = Number(($('txAmount').value||'').trim());
        const out = $('txResult');
        if(!from) return out.textContent = JSON.stringify({ok:false,error:'RID пуст вверху'},null,2);
        if(!to) return out.textContent = JSON.stringify({ok:false,error:'RID получателя пуст'},null,2);
        if(!Number.isFinite(amt)||amt<=0) return out.textContent = JSON.stringify({ok:false,error:'Неверная сумма'},null,2);

        let nonce = 1;
        if(API){
          const nb = await safe(`${API}/balance/${encodeURIComponent(from)}`);
          if(nb.ok && Number.isFinite(nb.body?.nonce)) nonce = nb.body.nonce + 1;
        }
        const tx = {from,to,amount:amt,nonce};
        const sigField = $('txSig').value.trim();
        if(sigField) tx.signature = sigField;
        else if(typeof window.walletSign === 'function'){
          try{ tx.signature = await window.walletSign(tx); } catch(e){ out.textContent = JSON.stringify({ok:false,error:'walletSign error: '+String(e)},null,2); return; }
        } else {
          out.textContent = JSON.stringify({ok:false,error:'Нет подписи: вставь HEX/Base64 или реализуй walletSign(canon) в браузере'},null,2);
          return;
        }

        if(!API){ out.textContent = JSON.stringify({ok:true,preview:tx},null,2); return; }
        out.textContent = '{ sending... }';
        const r = await safe(`${API}/wallet/tx/submit`, {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(tx)});
        out.textContent = JSON.stringify(r.body,null,2);
        if(r.ok){ setTimeout(()=>{ loadProfile(); loadHistory(); },600); }
      }catch(e){ showDebug('sendTx exception: '+e,5000); }
    }

    async function stake(endpoint){
      try{
        const rid = (($('stRid').value)||'SELF').trim();
        const amount = Number(($('stAmount').value||'').trim());
        const out = $('stResult');
        if(!Number.isFinite(amount)||amount<=0) return out.textContent = JSON.stringify({ok:false,error:'amount required'},null,2);
        if(!API){ out.textContent = JSON.stringify({ok:true,preview:{endpoint,validatorRid:rid,amount}},null,2); return; }
        const r = await safe(`${API}/stake/${endpoint}`, {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({validatorRid:rid,amount})});
        out.textContent = JSON.stringify(r.body,null,2); if(r.ok) loadProfile();
      }catch(e){ showDebug('stake err: '+e,4000); }
    }

    function hookEvents(){
      try{
        // guards
        ['ridInput','txRid','stRid'].forEach(id=>onlyB58($(id)));
        ['txAmount','stAmount'].forEach(id=>onlyNum($(id)));

        // auto RID: DEFAULT → LS → поле
        const saved = localStorage.getItem(LS_RID) || window.DEFAULT_RID || '';
        if(saved) $('ridInput').value = saved;

        $('ridInput').addEventListener('change', ()=>{ localStorage.setItem(LS_RID, norm($('ridInput').value)); loadProfile(); });
        $('copyBtn').addEventListener('click', async ()=>{ const v = norm($('ridInput').value); if(!v) return showDebug('RID пуст'); try{ await navigator.clipboard.writeText(v); showDebug('RID скопирован',2000);}catch(e){ showDebug('Copy error: '+e,4000); }});
        $('balanceBtn').addEventListener('click', loadProfile);
        $('syncBtn').addEventListener('click', async ()=>{ await loadHead(); await loadProfile(); });

        $('txSend').addEventListener('click', sendTx);
        $('stDelegate').addEventListener('click', ()=>stake('delegate'));
        $('stUndelegate').addEventListener('click', ()=>stake('undelegate'));
        $('stClaim').addEventListener('click', async ()=>{ if(!API) return $('stResult').textContent = JSON.stringify({ok:true,preview:'claim called'},null,2); const r = await safe(`${API}/stake/claim`,{method:'POST'}); $('stResult').textContent = JSON.stringify(r.body,null,2); });

        $('btnHist').addEventListener('click', loadHistory);
      }catch(e){ showDebug('hookEvents err: '+e,5000); }
    }

    function init(){
      try{
        // снять возможные overlay-стили
        document.body.style.pointerEvents = 'auto';
        hookEvents();
        loadHead(); loadProfile();
      }catch(e){ showDebug('init err: '+e,5000); }
    }

    if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', ()=>{ try{ init(); }catch(e){ showDebug('DOMContentLoaded err: '+e,0); } }, {once:true});
    else init();

    // minimal walletSign fallback (просит ключ один раз). Заменить на production-реализацию при необходимости.
    window.walletSign = window.walletSign || (async function(tx){
      // security notice: this stores SK локально в браузере — НЕ делай этого в общедоступных машинах.
      const hexToBytes = h => Uint8Array.from((h.replace(/^0x/,'').match(/.{1,2}/g)||[]).map(x=>parseInt(x,16)));
      const bytesToHex = b => Array.from(b).map(x=>x.toString(16).padStart(2,'0')).join('');
      const sha = async(d)=>new Uint8Array(await crypto.subtle.digest('SHA-256', d));
      let sk = localStorage.getItem('logos_sk32_hex');
      if(!sk){
        const v = prompt('Вставь приватный ключ SK32 (hex 64 символа). Будет сохранён локально в этом браузере.');
        if(!v) throw new Error('Ключ не указан');
        const s = v.trim().replace(/^0x/,'');
        if(s.length!==64) throw new Error('Ожидается 32 байта hex');
        localStorage.setItem('logos_sk32_hex', s); sk=s;
      }
      // простая "подпись": sha256(from|to|amount|nonce|sk) -> hex ( НЕ Ed25519 ). Прод замени на настоящую ed25519.
      const enc = new TextEncoder();
      const data = enc.encode(`${tx.from}|${tx.to}|${tx.amount}|${tx.nonce}|${sk}`);
      const out = await sha(data);
      return bytesToHex(out);
    });
  })();
  </script>
</body>
</html>

```

### FILE: /var/www/logos/www/styles.css

```
:root{
  --bg:#0b1016; --card:#0f1720; --muted:#0c141a; --text:#e6eef6; --sub:#93a4b3;
  --accent:#3b82f6; --accent-2:#1d4ed8; --ok:#10b981; --warn:#f59e0b; --err:#ef4444;
  --border:#1f2937; --chip:#0b1320;
  --radius:14px; --radius-sm:10px; --shadow:0 6px 28px rgba(0,0,0,.35);
  --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
  --sans: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", "Apple Color Emoji", "Segoe UI Emoji";
}
*{box-sizing:border-box}
html,body{margin:0;height:100%}
body{
  background:linear-gradient(180deg,#0a0f15 0%, #0b1117 30%, #0b1016 100%);
  color:var(--text); font-family:var(--sans); -webkit-font-smoothing:antialiased;
}
.container{max-width:980px;margin:32px auto;padding:0 16px}

h1{font-weight:800; letter-spacing:.2px; font-size:34px; margin:0 0 18px}
h2{font-size:20px; margin:0 0 14px; font-weight:700}
.sub{color:var(--sub); font-size:12px}

.card{
  background:var(--card); border:1px solid var(--border);
  border-radius:var(--radius); box-shadow:var(--shadow);
  padding:18px; margin:18px 0;
}

.row{display:flex; gap:14px; align-items:center; flex-wrap:wrap}
.col{flex:1}

.input, .button{
  border-radius:var(--radius-sm); border:1px solid var(--border);
  background:var(--muted); color:var(--text); outline:none;
}
.input{padding:12px 14px; width:100%}
.input[readonly]{opacity:.9}
.button{
  padding:11px 14px; cursor:pointer; transition:.15s ease-in-out;
  background:linear-gradient(180deg,var(--accent) 0%, var(--accent-2) 100%);
  border:none; font-weight:600;
}
.button:active{transform:translateY(1px)}
.button.secondary{background:#273449}
.button.ghost{
  background:transparent;border:1px solid var(--border); color:var(--text)
}
.badges{display:flex; gap:10px; flex-wrap:wrap; margin-bottom:10px}
.badge{
  background:var(--chip); border:1px solid var(--border);
  padding:6px 10px; border-radius:999px; color:var(--sub); font-size:12px
}
pre{
  margin:10px 0 0; padding:12px; border-radius:var(--radius-sm);
  background:#0a121a; border:1px solid var(--border); color:#cfe1f3;
  font-family:var(--mono); font-size:12px; white-space:pre-wrap;
}

/* таблица истории */
.table{width:100%; border-collapse:collapse; font-size:12px}
.table th, .table td{padding:10px 8px; border-top:1px solid rgba(255,255,255,.07)}
.table th{color:#9fb1c4; text-align:left; font-weight:600}
.table td.right{text-align:right}

.copy-btn{margin-left:8px}

.footer{opacity:.6; font-size:12px; text-align:center; margin:16px 0}

```

### FILE: /var/www/logos/www/wallet-autosign.js

```
// wallet-autosign.js — Ed25519 WebCrypto: window.walletSign(canon)
// canon = { from, to, amount:number, nonce:number } -> returns base58(signature)

(function () {
  const enc = new TextEncoder();
  const toBytes = (s) => enc.encode(s);
  const hexToBytes = (h) => Uint8Array.from((h.replace(/^0x/,'').match(/.{1,2}/g)||[]).map(x=>parseInt(x,16)));
  const bytesToHex = (b) => Array.from(b).map(x=>x.toString(16).padStart(2,'0')).join('');
  const le64 = (n) => { let x=BigInt(n); const b=new Uint8Array(8); for(let i=0;i<8;i++){ b[i]=Number(x&0xffn); x>>=8n; } return b; };
  const sha256 = async (bytes) => new Uint8Array(await crypto.subtle.digest('SHA-256', bytes));
  const B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';
  const b58enc = (bytes) => { let x=BigInt('0x'+bytesToHex(bytes)), out=''; while(x>0n){const d=x/58n,m=x%58n; out=B58[Number(m)]+out; x=d;} for(let i=0;i<bytes.length&&bytes[i]===0;i++) out='1'+out; return out||'1'; };

  async function canonicalBytes(fromRid, toRid, amount, nonce){
    const prefix = await sha256(toBytes('LOGOS_LRB_TX_V1'));
    const parts = [prefix, toBytes(fromRid), new Uint8Array([0]), toBytes(toRid), new Uint8Array([0]), le64(amount), le64(nonce)];
    const len = parts.reduce((s,a)=>s+a.length,0); const out=new Uint8Array(len);
    let o=0; for(const p of parts){ out.set(p,o); o+=p.length; } return out;
  }

  async function importSk(sk32hex){
    const raw = hexToBytes(sk32hex);
    return crypto.subtle.importKey('raw', raw, { name:'Ed25519' }, false, ['sign']);
  }

  async function signB58(sk32hex, msg){
    const key = await importSk(sk32hex);
    const sig = new Uint8Array(await crypto.subtle.sign('Ed25519', key, msg));
    return b58enc(sig);
  }

  function requireKey(){
    let sk = localStorage.getItem('logos_sk32_hex');
    if (!sk){
      const v = prompt('Вставь приватный ключ SK32 (hex 32 байта, 64 символа). Ключ сохранится локально в этом браузере.');
      if (!v) throw new Error('Ключ не указан');
      const s = v.trim().toLowerCase().replace(/^0x/,'');
      if (s.length !== 64) throw new Error('Ожидается 32 байта в hex (64 символа)');
      localStorage.setItem('logos_sk32_hex', s);
      sk = s;
    }
    return sk;
  }

  window.walletSign = async function(canon){
    const { from, to, amount, nonce } = canon;
    if (typeof amount!=='number' || typeof nonce!=='number') throw new Error('amount/nonce должны быть числом');
    const msg = await canonicalBytes(from, to, amount, nonce);
    const sk  = requireKey();
    return await signB58(sk, msg);
  };
})();

```

### FILE: /var/www/logos/www/wallet-sync.js

```
// wallet-sync.js (финал): один init после DOM, строгие id, автозаполнение RID, рабочие клики
(function(){
  const API="";                            // относительные URL → nginx
  const LS_RID="logos_current_rid";
  const $ = (id)=>document.getElementById(id);
  const asJSON = (r)=>r.json().catch(()=>({}));
  const norm = (v)=> (v||"").trim().replace(/^["']+|["']+$/g,"");

  async function safe(url,opt){ try{
    const r=await fetch(url,opt); return {ok:r.ok,status:r.status,body:await asJSON(r)};
  }catch(e){return{ok:false,status:0,body:{ok:false,error:String(e)}};}}

  function onlyB58(el){el&&el.addEventListener("input",()=>el.value=el.value.replace(/[^123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz]/g,""));}
  function onlyNum(el){el&&el.addEventListener("input",()=>el.value=el.value.replace(/[^\d]/g,""));}

  function setProfile(p){
    $("profileJson").textContent = JSON.stringify(p,null,2);
    $("chipBalance").textContent = "balance: " + (p.balance ?? "—");
    $("chipNonce").textContent   = "nonce: "   + (p.nonce   ?? "—");
    $("chipHead").textContent    = "head: "    + (p.head    ?? "—");
    $("stDelegated").textContent = "delegated: " + (p.delegated ?? "—");
    $("stEntries").textContent   = "entries: "   + (p.entries   ?? "—");
    $("stClaimable").textContent = "claimable: " + (p.claimable ?? "—");
  }

  async function loadHead(){
    const r=await safe(`${API}/head`);
    if(r.ok) $("chipHead").textContent = "head: " + (r.body.height ?? "—");
  }
  async function loadProfile(){
    const rid = norm($("ridInput").value) || localStorage.getItem(LS_RID) || "";
    if(!rid){ $("profileJson").textContent="{}"; return; }
    localStorage.setItem(LS_RID, rid);
    const r=await safe(`${API}/profile/${encodeURIComponent(rid)}`);
    if(!r.ok){ setProfile({ok:false,error:r.body.error||`profile ${r.status}`}); return; }
    setProfile(r.body);
  }
  async function loadHistory(){
    const rid = localStorage.getItem(LS_RID) || norm($("ridInput").value); if(!rid) return;
    const r=await safe(`${API}/history/${encodeURIComponent(rid)}`);
    const tbody = document.querySelector("#historyTbl tbody");
    tbody.innerHTML="";
    const items = (r.ok && Array.isArray(r.body.items)) ? r.body.items : [];
    if(!items.length){ tbody.innerHTML="<tr><td colspan='7'>нет записей</td></tr>"; return; }
    for(const it of items){
      const tr=document.createElement("tr");
      tr.innerHTML=`<td>${it.height??""}</td><td>${(it.hash||"").slice(0,10)}</td>
        <td>${it.from||""}</td><td>${it.to||""}</td>
        <td>${it.amount??""}</td><td>${it.fee??""}</td><td>${it.nonce??""}</td>`;
      tbody.appendChild(tr);
    }
  }

  async function sendTx(){
    const from = norm($("ridInput").value); const to = norm($("txRid").value);
    const amt  = Number(($("txAmount").value||"").trim()); const out = $("txResult");
    if(!from) return out.textContent=JSON.stringify({ok:false,error:"RID пуст (вверху)"},null,2);
    if(!to)   return out.textContent=JSON.stringify({ok:false,error:"RID получателя пуст"},null,2);
    if(!Number.isFinite(amt)||amt<=0) return out.textContent=JSON.stringify({ok:false,error:"Неверная сумма"},null,2);

    const nb = await safe(`${API}/balance/${encodeURIComponent(from)}`);
    const nonce = (nb.ok && Number.isFinite(nb.body?.nonce)) ? nb.body.nonce+1 : 1;

    const tx = { from, to, amount: amt, nonce };
    const sig = $("txSig").value.trim();

    if(sig){
      tx.signature = sig;
    }else if (typeof window.walletSign === "function"){
      try{ tx.signature = await window.walletSign(tx); }
      catch(e){ out.textContent = JSON.stringify({ok:false,error:"walletSign error: "+e},null,2); return; }
    }else{
      out.textContent = JSON.stringify({ok:false,error:"Нет подписи: вставь HEX/Base64 в поле или реализуй walletSign(canon) в браузере"},null,2);
      return;
    }

    out.textContent = "{ sending... }";
    const r = await safe(`${API}/wallet/tx/submit`, { method:"POST", headers:{'Content-Type':'application/json'}, body: JSON.stringify(tx) });
    out.textContent = JSON.stringify(r.body,null,2);
    if(r.ok){ setTimeout(()=>{ loadProfile(); loadHistory(); },600); }
  }

  async function stakeDo(endpoint){
    const rid = norm($("stRid").value)||"SELF"; const amount=Number(($("stAmount").value||"").trim()); const out=$("stResult");
    if(!Number.isFinite(amount)||amount<=0){ out.textContent=JSON.stringify({ok:false,error:"amount required"},null,2); return; }
    const r = await safe(`${API}/stake/${endpoint}`, { method:"POST", headers:{'Content-Type':'application/json'}, body: JSON.stringify({ validatorRid: rid, amount }) });
    out.textContent = JSON.stringify(r.body,null,2);
    if(r.ok) loadProfile();
  }

  function init(){
    // guards
    [$("ridInput"),$("txRid"),$("stRid")].forEach(onlyBase58);
    [$("txAmount"),$("stAmount")].forEach(onlyNum);

    // авто-RID: DEFAULT → LS → поле
    if(window.DEFAULT_RID && !localStorage.getItem(LS_RID)) localStorage.setItem(LS_RID, window.DEFAULT_RID);
    const saved = localStorage.getItem(LS_RID)||"";
    if(saved) $("ridInput").value = saved;

    // handlers
    $("ridInput").addEventListener("change", ()=>{ localStorage.setItem(LS_RID, norm($("ridInput").value)); loadProfile(); });
    $("copyBtn").addEventListener("click", async ()=>{
      const v=norm($("ridInput").value); if(!v) return alert("RID пуст");
      try{ await navigator.clipboard.writeText(v); $("copyBtn").textContent="Copied"; setTimeout(()=>$("copyBtn").textContent="Copy",1000);}catch(e){alert("Copy error");}
    });
    $("balanceBtn").addEventListener("click", loadProfile);
    $("syncBtn").addEventListener("click", async ()=>{ await loadHead(); await loadProfile(); });

    $("txSend").addEventListener("click", sendTx);

    $("stDelegate").addEventListener("click", ()=>stakeDo("delegate"));
    $("stUndelegate").addEventListener("click", ()=>stakeDo("undelegate"));
    $("stClaim").addEventListener("click", async ()=>{
      const r=await safe(`${API}/stake/claim`,{method:"POST",headers:{'Content-Type':'application/json'},body:'{}'}); $("stResult").textContent=JSON.stringify(r.body,null,2);
    });

    $("btnHist").addEventListener("click", loadHistory);

    // старт
    loadHead(); loadProfile();
  }

  if (document.readyState==="loading") document.addEventListener("DOMContentLoaded", init, {once:true});
  else init();
})();

```

### FILE: /var/www/logos/www/wallet-ui.js

```
(() => {
  // ============ helpers ============
  const $ = (s, r=document) => r.querySelector(s);
  const $$ = (s, r=document) => Array.from(r.querySelectorAll(s));
  const enc = new TextEncoder();

  const hexToBytes = (hex) => Uint8Array.from((hex.replace(/^0x/,'').match(/.{1,2}/g)||[]).map(h=>parseInt(h,16)));
  const bytesToHex = (b) => Array.from(b).map(x=>x.toString(16).padStart(2,'0')).join('');
  const toBytes = (s) => enc.encode(s);

  // base58 (Bitcoin alphabet)
  const B58_AL = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';
  const b58encode = (bytes) => {
    let x = BigInt('0x'+bytesToHex(bytes)); let out='';
    while (x>0n) { const d=x/58n, m=x%58n; out=B58_AL[Number(m)]+out; x=d; }
    for (let i=0;i<bytes.length && bytes[i]===0;i++) out='1'+out;
    return out||'1';
  };

  const normalizeRid = (v) => (v||'').trim().replace(/^"+|"+$/g,'').replace(/^%22|%22$/g,'');

  // найти поле RID (в карточке Профиль)
  const ridInput = $$('input,textarea').find(el =>
    /rid/i.test(el.previousElementSibling?.textContent||'') ||
    /rid/i.test(el.placeholder||'') ||
    /rid/i.test(el.parentElement?.textContent||'')
  );
  const getRID = () => normalizeRid(ridInput?.value||'');

  const apiGet = async (p) => (await fetch(p,{credentials:'same-origin'})).json();
  const apiPost = async (p,b) => (await fetch(p,{
    method:'POST', headers:{'Content-Type':'application/json'},
    credentials:'same-origin', body:JSON.stringify(b),
  })).json();

  // ====== RID: кнопка Copy ======
  const mountCopy = () => {
    if (!ridInput || ridInput.dataset.copyMounted) return;
    const btn = document.createElement('button');
    btn.textContent = 'Copy';
    btn.style.marginLeft='8px';
    btn.onclick = async ()=>{ try{ await navigator.clipboard.writeText(getRID()); btn.textContent='Copied'; setTimeout(()=>btn.textContent='Copy',900);}catch{} };
    ridInput.parentElement?.appendChild(btn);
    ridInput.dataset.copyMounted='1';
  };

  // ====== История: таблица ======
  const renderHistory = async () => {
    const rid = getRID(); if (!rid) return;
    const title = $$('*').find(n=>/история/i.test(n.textContent||'')); if (!title) return;
    let box = title.parentElement?.querySelector('.history-table');
    if (!box) { box=document.createElement('div'); box.className='history-table'; title.parentElement?.appendChild(box); }
    box.innerHTML='<div style="opacity:.6;font-size:12px;margin:.5rem 0">loading...</div>';

    let data; try { data = await apiGet(`/history/${encodeURIComponent(rid)}`); } catch(e){ box.innerHTML=`<pre>${e}</pre>`; return; }
    const items = data.items || [];
    const rows = items.slice(0,20).map(it=>{
      const type = it.from===rid ? 'send' : 'recv';
      const td = (v,al='left') => `<td style="text-align:${al}">${v}</td>`;
      return `<tr>
        ${td(type)} ${td((it.from||'').slice(0,6)+'…')}
        ${td((it.to||'').slice(0,6)+'…')}
        ${td(it.amount??'', 'right')}
        ${td(it.fee??'', 'right')}
        ${td(it.nonce??'', 'right')}
        ${td(it.height??'', 'right')}
        ${td((it.hash||'').slice(0,8))}
      </tr>`;
    }).join('');
    box.innerHTML = `
      <table style="width:100%;border-collapse:collapse;font-size:12px">
        <thead>
          <tr><th style="text-align:left">type</th><th>from</th><th>to</th>
              <th style="text-align:right">amount</th><th style="text-align:right">fee</th>
              <th style="text-align:right">nonce</th><th style="text-align:right">height</th><th>hash</th></tr>
        </thead>
        <tbody>${rows}</tbody>
      </table>`;
  };

  // ====== канонические байты TX ======
  const le64 = (n) => { let x=BigInt(n); const b=new Uint8Array(8); for(let i=0;i<8;i++){ b[i]=Number(x&0xffn); x>>=8n; } return b; };
  const sha256 = async (bytes) => new Uint8Array(await crypto.subtle.digest('SHA-256', bytes));
  const canonicalBytes = async (fromRid, toRid, amount, nonce) => {
    const prefix = await sha256(toBytes('LOGOS_LRB_TX_V1'));
    const parts = [prefix, toBytes(fromRid), new Uint8Array([0]), toBytes(toRid), new Uint8Array([0]), le64(amount), le64(nonce)];
    const out = new Uint8Array(parts.reduce((s,a)=>s+a.length,0));
    let o=0; for(const p of parts){ out.set(p,o); o+=p.length; }
    return out;
  };

  // ====== ключи (KP64 или SK32) ======
  const getKeys = async () => {
    let kp64 = localStorage.getItem('logos_kp64_hex') || '';
    let sk32 = localStorage.getItem('logos_sk32_hex') || '';
    if (!kp64 && !sk32) {
      const v = prompt('Вставь KP64 (sk||pk — 64 байта hex) или SK32 (32 байта hex). Ключ хранится только в этом браузере.');
      if (!v) throw new Error('Ключ не указан');
      const s = v.trim().replace(/^0x/,'').toLowerCase();
      if (s.length===128) { kp64=s; localStorage.setItem('logos_kp64_hex', kp64); }
      else if (s.length===64) { sk32=s; localStorage.setItem('logos_sk32_hex', sk32); }
      else throw new Error('Неверный формат ключа');
    }
    if (!sk32 && kp64) sk32 = kp64.slice(0,64);
    return { kp64, sk32 };
  };

  const wcSign = async (sk32hex, msg) => {
    const key = await crypto.subtle.importKey('raw', hexToBytes(sk32hex), {name:'Ed25519'}, false, ['sign']);
    const sig = new Uint8Array(await crypto.subtle.sign('Ed25519', key, msg));
    return sig;
  };

  // ====== Авто-подпись отправки ======
  const enhanceSend = () => {
    const sendBtn = $$('button').find(b=>/отправить/i.test(b.textContent||''));
    if (!sendBtn || sendBtn.dataset.hooked) return;
    sendBtn.dataset.hooked='1';
    sendBtn.addEventListener('click', async (ev)=>{
      try{
        ev.preventDefault();

        const fromRid = getRID(); if (!fromRid) throw new Error('RID пуст');
        // Ищем поля по «подписям»
        const container = sendBtn.closest('section,div,form') || document;
        const toField = $$('input,textarea', container).find(el =>
          /rid получателя/i.test(el.previousElementSibling?.textContent||'') ||
          /rid получателя/i.test(el.parentElement?.textContent||'') ||
          /RID получателя/i.test(el.placeholder||''));
        const amtField = $$('input,textarea', container).find(el =>
          /amount|сумма/i.test(el.placeholder||'') || /сумма/i.test(el.previousElementSibling?.textContent||''));
        const sigField = $$('input,textarea', container).find(el =>
          /sig|подпись/i.test(el.placeholder||'') || /подпись/i.test(el.previousElementSibling?.textContent||''));

        const toRid = normalizeRid(toField?.value||''); if (!toRid) throw new Error('RID получателя пуст');
        const amount = parseInt((amtField?.value||'').trim(),10); if (!(amount>0)) throw new Error('Сумма некорректна');

        // Если пользователь сам ввёл подпись — не вмешиваемся
        if (sigField && sigField.value.trim().length>0) return;

        // nonce из backend
        const bal = await apiGet(`/balance/${encodeURIComponent(fromRid)}`);
        const nonce = (bal.nonce||0) + 1;

        // ключи и подпись
        const { sk32 } = await getKeys();
        const msg = await canonicalBytes(fromRid, toRid, amount, nonce);
        const sig = await wcSign(sk32, msg);
        const sigB58 = b58encode(sig);

        const req = { from: fromRid, to: toRid, amount, nonce, signature: sigB58 };
        const res = await apiPost('/submit_tx', req);

        // вывод результата и авто-обновление
        let out = container.querySelector('.send-result');
        if (!out) { out=document.createElement('pre'); out.className='send-result'; container.appendChild(out); }
        out.textContent = JSON.stringify(res,null,2);
        window.dispatchEvent(new Event('logos-sync'));
      } catch(e) {
        alert('Ошибка: '+(e?.message||e));
      }
    });
  };

  // ====== Автосинхрон (обновление плашек/истории) ======
  const badge = (label) => {
    const node = $$('*').find(n=>n.textContent?.trim().toLowerCase()===label.toLowerCase()+':');
    return node?.nextElementSibling || null;
  };
  let stop=false, t=null, delay=2000;
  const syncOnce = async () => {
    const rid = getRID(); if (!rid) return;
    try{
      const p = await apiGet(`/profile/${encodeURIComponent(rid)}`);
      const bBal = badge('balance'), bNonce = badge('nonce'), bHead = badge('head');
      if (bBal)  bBal.textContent  = String(p.balance);
      if (bNonce) bNonce.textContent= String(p.nonce);
      if (bHead)  bHead.textContent = String(p.head);
      await renderHistory();
      delay=2000;
    }catch{ delay=Math.min(delay*2,15000); }
  };
  const loop = async ()=>{ clearTimeout(t); if (stop) return; await syncOnce(); t=setTimeout(loop, delay); };
  document.addEventListener('visibilitychange', ()=>{ stop=document.hidden; if(!stop) loop(); });

  // начальный запуск
  setTimeout(()=>{ mountCopy(); enhanceSend(); loop(); }, 500);
})();

```

### FILE: /var/www/logos/www/wallet.js

```
// wallet.js — продакшн версия с автоподписью

async function walletSign(tx) {
    // здесь мы подписываем транзакцию через встроенный ключ в браузере
    // (для MVP: генерим из sessionStorage, в проде подтягиваем из secure-хранилища)
    const kp = window.localStorage.getItem("logos_kp64");
    if (!kp) {
        throw new Error("Нет ключа в локальном хранилище");
    }

    const resp = await fetch("/make_tx/sign-kp64", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            from_kp64: kp,
            from_rid: tx.from,
            to_rid: tx.to,
            amount: tx.amount,
            nonce: tx.nonce
        })
    });

    return await resp.json();
}

async function submitTx(tx) {
    try {
        // автоподпись
        const signed = await walletSign(tx);

        const resp = await fetch("/wallet/tx/submit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(signed)
        });

        return await resp.json();
    } catch (e) {
        console.error("Ошибка при отправке транзакции:", e);
        return { ok: false, error: e.message };
    }
}

```

### FILE: /var/www/logos/www/wallet/app.html

```
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

### FILE: /var/www/logos/www/wallet/app.js

```
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

### FILE: /var/www/logos/www/wallet/app.v2.js

```
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

### FILE: /var/www/logos/www/wallet/app.v3.js

```
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

### FILE: /var/www/logos/www/wallet/auth.js

```
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

### FILE: /var/www/logos/www/wallet/index.html

```
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <!-- Жёсткое отключение кэша на уровне страницы -->
  <meta http-equiv="Cache-Control" content="no-store, no-cache, must-revalidate"/>
  <meta http-equiv="Pragma" content="no-cache"/>
  <meta http-equiv="Expires" content="0"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; connect-src 'self'; img-src 'self'; script-src 'self'; style-src 'self'">
  <title>LOGOS Wallet</title>
  <style>
    body{font-family:system-ui,Roboto,Arial,sans-serif;background:#0b0e11;color:#e6e6e6;margin:0}
    header{padding:12px 20px;background:#12161a;border-bottom:1px solid #1b2026}
    main{padding:20px}
    h3{margin:0;font-size:18px}
    section{margin-bottom:20px}
    input,button{padding:8px 10px;border-radius:6px;border:none;font-size:14px}
    button{background:#2d6cdf;color:white;cursor:pointer;margin:4px 2px}
    button:hover{background:#1b4fb5}
    .out{margin-top:10px;font-family:monospace;font-size:13px;white-space:pre-wrap}
  </style>
  <script>
    // Кардинально: на входе очищаем SW и Cache API,
    // чтобы ни одна старая версия не мешала.
    (async ()=>{
      try{
        if ('serviceWorker' in navigator) {
          const regs = await navigator.serviceWorker.getRegistrations();
          for (const r of regs) { try { await r.unregister(); } catch{} }
        }
        if (window.caches) {
          const keys = await caches.keys();
          for (const k of keys) { try { await caches.delete(k); } catch{} }
        }
        // Стираем старые версии из localStorage/sessionStorage, кроме наших полей
        const keep = new Set(['logos_pass','logos_rid']);
        for (const k of Object.keys(localStorage)) if (!keep.has(k)) localStorage.removeItem(k);
        for (const k of Object.keys(sessionStorage)) if (!keep.has(k)) sessionStorage.removeItem(k);
      }catch(e){}
    })();
  </script>
</head>
<body>
  <header>
    <h3>LOGOS Wallet</h3>
    <div id="node-info" class="muted">node: <span id="node-url"></span> | head: <span id="head"></span></div>
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

  <!-- новый js с версией (cache-buster) -->
  <script src="app.v3.js?v=3"></script>
  <script>
    document.getElementById('node-url').textContent = location.origin;
    async function updHead(){
      try{
        const r=await fetch(location.origin+'/api/head');
        const j=await r.json();
        document.getElementById('head').textContent=j.height;
        const rid=sessionStorage.getItem('logos_rid');
        if(rid){
          const br=await fetch(location.origin+'/api/balance/'+encodeURIComponent(rid));
          const bj=await br.json();
          document.getElementById('rid').textContent = rid;
          document.getElementById('balance').textContent = bj.balance;
          document.getElementById('nonce-show').textContent = bj.nonce;
        }
      }catch(e){}
    }
    setInterval(updHead,1500); updHead();
  </script>
</body>
</html>

```

### FILE: /var/www/logos/www/wallet/login.html

```
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

### FILE: /var/www/logos/www/wallet/staking.js

```
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

### FILE: /var/www/logos/www/wallet/wallet.css

```
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

### FILE: /var/www/logos/www/wallet/wallet.js

```
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

### FILE: /var/www/logos/www/explorer/explorer.css

```
body { font-family: system-ui, sans-serif; margin: 0; background: #0b0c10; color: #e6edf3; }
header { padding: 12px; background: #11151a; border-bottom: 1px solid #1e242c; display:flex; justify-content:space-between; }
main { padding: 12px; display: grid; gap: 20px; }
section { background: #141a21; padding: 12px; border-radius: 10px; }
button { padding: 10px 14px; border-radius: 8px; border: none; margin: 4px; cursor: pointer; background: #1665c1; color: #fff; font-weight: 600; }
button:hover { background: #1f77d0; }
input { padding: 8px; margin: 4px; border-radius: 6px; border: 1px solid #333; background: #0b0c10; color: #e6edf3; width: 100%; max-width: 380px; }
pre { background: #0e1116; padding: 8px; border-radius: 6px; overflow-x: auto; }
table { width: 100%; border-collapse: collapse; margin-top: 10px; }
th, td { padding: 6px 8px; border-bottom: 1px solid #333; font-size: 13px; }

```

### FILE: /var/www/logos/www/explorer/explorer.js

```
// LOGOS Explorer – history debug + stable fill
const API = location.origin + "/api";
const $  = s => document.querySelector(s);
const out= (id,v)=>{$(id).textContent=(typeof v==="string")?v:JSON.stringify(v,null,2)};
const fmtNum=n=>Number(n).toLocaleString("ru-RU");
const fmtTs =ms=>isFinite(ms)?new Date(Number(ms)).toLocaleString("ru-RU"):"";

async function jget(path){
  const r=await fetch(API+path,{cache:"no-store"});
  if(!r.ok) throw new Error(r.status+" "+(await r.text()).slice(0,400));
  return r.json();
}

// status
document.addEventListener("DOMContentLoaded",()=>{ const s=$("#jsStat"); if(s){ s.style.color="#0bd464"; s.textContent="js: готов"; }});

// HEAD / ECONOMY
let autoTimer=null;
async function fetchHead(){ try{ out("out-head", await jget("/head")); }catch(e){ out("out-head","ERR: "+e.message); } }
async function fetchEconomy(){ try{ out("out-economy", await jget("/economy")); }catch(e){ out("out-economy","ERR: "+e.message); } }
function toggleAuto(){
  if(autoTimer){ clearInterval(autoTimer); autoTimer=null; $("#btn-auto").textContent="Автообновление: выключено"; return; }
  const tick=async()=>{ await fetchHead(); await fetchEconomy(); };
  tick(); autoTimer=setInterval(tick,5000);
  $("#btn-auto").textContent="Автообновление: включено";
}

// BLOCK / MIX
async function fetchBlock(){
  const h=Number($("#inp-height").value); if(!h){ alert("Укажи высоту"); return; }
  try{ out("out-block", await jget("/block/"+h)); }catch(e){ out("out-block","ERR: "+e.message); }
}
async function fetchMix(){
  const h=Number($("#inp-height").value); if(!h){ alert("Укажи высоту"); return; }
  try{ out("out-block", await jget(`/block/${h}/mix`)); }catch(e){ out("out-block","ERR: "+e.message); }
}

// HISTORY
let histRid="", limit=20, fromNonce=0, nextFrom=null, prevStack=[];
function renderHistory(arr){
  const tb=$("#tbl-history tbody"); tb.innerHTML="";
  if(!arr || arr.length===0){
    const tr=document.createElement("tr");
    tr.innerHTML=`<td colspan="6" style="opacity:.8">0 записей</td>`;
    tb.appendChild(tr);
  } else {
    arr.forEach(tx=>{
      const tr=document.createElement("tr");
      tr.innerHTML=`<td>${tx.nonce??""}</td><td>${tx.from??""}</td><td>${tx.to??""}</td>`+
                   `<td>${fmtNum(tx.amount??0)}</td><td>${tx.height??""}</td><td>${fmtTs(tx.ts_ms)}</td>`;
      tb.appendChild(tr);
    });
  }
  $("#hist-info").textContent=`RID=${histRid} · from=${fromNonce} · limit=${limit} · next=${nextFrom??"-"}`;
  $("#btn-prev").disabled = (prevStack.length===0);
  $("#btn-next").disabled = (nextFrom==null);
}

async function pageHistory(rid, from, lim){
  const q=new URLSearchParams({from:String(from||0),limit:String(lim||20)});
  const j=await jget(`/history/${rid}?`+q.toString());
  // DEBUG: покажем сырой ответ под таблицей
  out("out-history", j); $("#out-history").style.display="block";
  const arr=j.items || j.txs || [];
  nextFrom=(typeof j.next_from!=="undefined")?j.next_from:null;
  renderHistory(arr);
}

async function fetchHistory(){
  histRid=($("#inp-rid").value||"").trim();
  limit=Math.max(1, Number($("#inp-limit").value)||20);
  if(!histRid){ alert("Укажи RID"); return; }
  fromNonce=0; nextFrom=null; prevStack=[];
  try{ await pageHistory(histRid, fromNonce, limit); }catch(e){ alert("ERR: "+e.message); }
}
async function prevPage(){ if(prevStack.length===0) return; fromNonce=prevStack.pop(); await pageHistory(histRid, fromNonce, limit); }
async function nextPage(){ if(nextFrom==null) return; prevStack.push(fromNonce); fromNonce=nextFrom; await pageHistory(histRid, fromNonce, limit); }

// экспорт под onclick
window.fetchHead=fetchHead; window.fetchEconomy=fetchEconomy; window.toggleAuto=toggleAuto;
window.fetchBlock=fetchBlock; window.fetchMix=fetchMix;
window.fetchHistory=fetchHistory; window.prevPage=prevPage; window.nextPage=nextPage;

```

### FILE: /var/www/logos/www/explorer/index.html

```
<!doctype html><html lang="ru"><head>
<meta charset="utf-8"/>
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; connect-src 'self'; img-src 'self'; script-src 'self'; style-src 'self'">
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>LOGOS Explorer</title>
<style>
body{font-family:system-ui,Roboto,Arial,sans-serif;background:#0b0e11;color:#e6e6e6;margin:0}
header{padding:16px 20px;background:#12161a;border-bottom:1px solid #1b2026}
main{padding:20px}
table{width:100%;border-collapse:collapse}
th,td{padding:8px 10px;border-bottom:1px solid #1b2026;font-size:14px}
th{text-align:left;color:#a6a6a6}.muted{color:#8c8c8c;font-size:12px}
</style></head><body>
<header><h3>LOGOS Explorer</h3><div class="muted" id="head"></div></header>
<main>
  <h4>Последние блоки</h4>
  <table><thead><tr><th>Высота</th><th>Хеш</th><th>Tx</th><th>Время</th></tr></thead><tbody id="blocks"></tbody></table>
</main>
<script>
async function getHead(){ return (await fetch('/api/head')).json(); }
async function getBlocks(){ return (await fetch('/api/archive/blocks?limit=50')).json(); }
function fmtTs(ts){ const d=new Date((ts||0)*1000); return isNaN(d)?'-':d.toLocaleString(); }
async function tick(){
  try{
    const h=await getHead();
    document.getElementById('head').textContent=`head.height=${h.height} (finalized=${h.finalized})`;
    const data=await getBlocks();
    const rows=(data.blocks||[]).map(b=>{
      const hash=b.hash||b.block_hash||''; const ts=b.ts||b.ts_sec||0; const txc=b.tx_count??b.txs??0;
      return `<tr><td>${b.height}</td><td class="muted">${String(hash).slice(0,16)}…</td><td>${txc}</td><td>${fmtTs(ts)}</td></tr>`;
    }).join('');
    document.getElementById('blocks').innerHTML=rows;
  }catch(e){ console.error(e); }
}
setInterval(tick,1500); tick();
</script></body></html>

```

### FILE: /var/www/logos/www/wallet3/app.v3.js

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

### FILE: /var/www/logos/www/wallet3/index.html

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
