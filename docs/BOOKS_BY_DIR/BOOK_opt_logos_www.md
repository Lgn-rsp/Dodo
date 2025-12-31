# LOGOS — Directory Book

## ROOT: /opt/logos/www

---
## STRUCTURE
```
/opt/logos/www
/opt/logos/www/.bak_20251212_093738
/opt/logos/www/.bak_20251212_093738/explorer
/opt/logos/www/.bak_20251212_093738/wallet
/opt/logos/www/explorer
/opt/logos/www/shared
/opt/logos/www/wallet
/opt/logos/www/wallet_backup_20251129T115355Z
```

---
## FILES (FULL SOURCE)


### FILE: /opt/logos/www/explorer/explorer.css
```
:root{
  --bg: var(--wallet-bg, #0b0c10);
  --card: var(--wallet-card, #11151a);
  --line: var(--wallet-line, #1e242c);
  --txt: var(--wallet-text, #e6edf3);
  --muted: var(--wallet-muted, #9aa4b2);
  --accent: var(--wallet-accent, #2f81f7);
  --accent-b: var(--wallet-accent-b, #1f6feb);
  --ok: #0bd464;
  --bad:#ff5252;
}

*{ box-sizing:border-box; }

body{
  margin:0;
  background:var(--bg);
  color:var(--txt);
  font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;
}

.wrap{
  max-width:960px;
  margin:0 auto;
  padding:0 12px;
}

.topbar{
  border-bottom:1px solid var(--line);
  background:#0f1318;
  padding:12px 0;
}

.toprow{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:12px;
}

h1{ margin:0; font-size:18px; font-weight:900; }
h2{ margin:0 0 10px; font-size:15px; font-weight:900; }

.stat{
  font-size:12px;
  padding:6px 10px;
  border-radius:999px;
  border:1px solid var(--line);
}

.stat.ok{ color:var(--ok); }
.stat.bad{ color:var(--bad); }

.card{
  background:var(--card);
  border:1px solid var(--line);
  border-radius:14px;
  padding:12px 14px 14px;
  margin:12px 0;
}

label{
  display:block;
  margin:10px 0 4px;
  font-size:12px;
  color:var(--muted);
}

input{
  width:100%;
  padding:10px;
  border-radius:10px;
  border:1px solid var(--line);
  background:#05070b;
  color:var(--txt);
  font-size:13px;
  outline:none;
}

.mono{
  font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace;
}

.muted{
  margin-top:6px;
  font-size:12px;
  color:var(--muted);
}

.btn-row{
  display:flex;
  flex-wrap:wrap;
  gap:10px;
  margin-top:10px;
}

button{
  padding:10px 12px;
  border-radius:10px;
  border:1px solid var(--accent-b);
  background:var(--accent);
  color:#fff;
  font-weight:800;
  font-size:13px;
  cursor:pointer;
}

button:hover{ filter:brightness(1.05); }

.out{
  margin-top:10px;
  padding:10px;
  border-radius:10px;
  border:1px dashed var(--line);
  background:#05070b;
  min-height:48px;
  white-space:pre-wrap;
  word-break:break-word;
}

```

### FILE: /opt/logos/www/explorer/explorer.js
```
'use strict';

(function () {
  const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/api'));
  const $ = (sel) => document.querySelector(sel);

  function setStatus(ok, text) {
    const s = $('#jsStat');
    if (!s) return;
    s.textContent = text;
    s.classList.toggle('ok', !!ok);
    s.classList.toggle('bad', !ok);
  }

  function out(id, v) {
    const el = document.getElementById(id);
    if (!el) return;
    if (typeof v === 'string') el.textContent = v;
    else el.textContent = JSON.stringify(v, null, 2);
  }

  async function fetchText(url, opts) {
    const r = await fetch(url, opts || {});
    const t = await r.text().catch(() => '');
    if (!r.ok) throw new Error(`${r.status} ${t}`);
    try { return JSON.parse(t); } catch { return t; }
  }

  async function boot() {
    const apiEl = document.getElementById('api');
    if (apiEl) apiEl.textContent = API;

    setStatus(true, 'js: готов');

    const btnHead = document.getElementById('btn-head');
    if (btnHead) btnHead.addEventListener('click', async () => {
      try {
        const j = await fetchText(`${API}/head`);
        out('out-head', j);
      } catch (e) {
        out('out-head', 'ERR: ' + (e.message || String(e)));
      }
    });

    const btnBal = document.getElementById('btn-balance');
    if (btnBal) btnBal.addEventListener('click', async () => {
      try {
        const rid = String((document.getElementById('rid-balance') || {}).value || '').trim();
        if (!rid) throw new Error('RID пустой');
        const j = await fetchText(`${API}/balance/${encodeURIComponent(rid)}`);
        out('out-balance', j);
      } catch (e) {
        out('out-balance', 'ERR: ' + (e.message || String(e)));
      }
    });

    const btnBlock = document.getElementById('btn-block');
    if (btnBlock) btnBlock.addEventListener('click', async () => {
      try {
        const h = Number((document.getElementById('height') || {}).value || '0');
        if (!Number.isFinite(h) || h < 0) throw new Error('height invalid');
        const j = await fetchText(`${API}/block/${h}`);
        out('out-block', j);
      } catch (e) {
        out('out-block', 'ERR: ' + (e.message || String(e)));
      }
    });

    const btnHist = document.getElementById('btn-history');
    if (btnHist) btnHist.addEventListener('click', async () => {
      try {
        const rid = String((document.getElementById('rid-history') || {}).value || '').trim();
        if (!rid) throw new Error('RID пустой');
        const j = await fetchText(`${API}/history/${encodeURIComponent(rid)}`);
        out('out-history', j);
      } catch (e) {
        out('out-history', 'ERR: ' + (e.message || String(e)));
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => boot().catch((e)=>setStatus(false,'js: err')));
  } else {
    boot().catch((e)=>setStatus(false,'js: err'));
  }
})();

```

### FILE: /opt/logos/www/explorer/index.html
```
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta http-equiv="Cache-Control" content="no-store"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Explorer</title>

  <link rel="stylesheet" href="/shared/wallet-theme.css"/>
  <link rel="stylesheet" href="./explorer.css"/>

  <script src="./explorer.js?v=20251212_01" defer></script>
</head>
<body>
  <header class="topbar">
    <div class="wrap">
      <div class="toprow">
        <h1>LOGOS Explorer</h1>
        <div id="jsStat" class="stat">js: ...</div>
      </div>
      <div class="muted">API: <span id="api" class="mono"></span></div>
    </div>
  </header>

  <main class="wrap">
    <section class="card">
      <h2>Head</h2>
      <div class="btn-row">
        <button id="btn-head" type="button">GET /head</button>
      </div>
      <pre id="out-head" class="mono out"></pre>
    </section>

    <section class="card">
      <h2>Balance</h2>
      <label for="rid-balance">RID</label>
      <input id="rid-balance" class="mono" placeholder="RID"/>

      <div class="btn-row">
        <button id="btn-balance" type="button">GET /balance/:rid</button>
      </div>
      <pre id="out-balance" class="mono out"></pre>
    </section>

    <section class="card">
      <h2>Block</h2>
      <label for="height">Height</label>
      <input id="height" type="number" min="0" step="1" value="0"/>

      <div class="btn-row">
        <button id="btn-block" type="button">GET /block/:height</button>
      </div>
      <pre id="out-block" class="mono out"></pre>
    </section>

    <section class="card">
      <h2>History</h2>
      <label for="rid-history">RID</label>
      <input id="rid-history" class="mono" placeholder="RID"/>

      <div class="btn-row">
        <button id="btn-history" type="button">GET /history/:rid</button>
      </div>
      <pre id="out-history" class="mono out"></pre>
    </section>
  </main>
</body>
</html>

```

### FILE: /opt/logos/www/shared/airdrop.css
```
/* LOGOS Airdrop UI (CSP-safe) */

.heroTitle{ margin:0 0 6px; }
.heroSub{ margin:0; }

.heroGrid{
  display:flex;
  gap:18px;
  justify-content:space-between;
  align-items:flex-start;
  flex-wrap:wrap;
}

.stats{
  display:flex;
  gap:10px;
  flex-wrap:wrap;
}

.stat{
  padding:10px 12px;
  border-radius:14px;
  border:1px solid rgba(255,255,255,.10);
  background:rgba(0,0,0,.18);
  min-width:120px;
}

.stat__k{ font-size:12px; }
.stat__v{ font-size:18px; font-weight:700; margin-top:2px; }

.row2{
  display:flex;
  gap:10px;
  align-items:center;
  flex-wrap:wrap;
}

.stack{ display:flex; flex-direction:column; gap:14px; }

.monoInput{
  width:100%;
  min-width:260px;
  padding:12px 12px;
  border-radius:14px;
  border:1px solid rgba(255,255,255,.10);
  background:rgba(0,0,0,.22);
  color:var(--text);
  font-family:var(--mono);
  font-size:13px;
  outline:none;
}

.monoInput:focus{
  border-color:rgba(77,163,255,.35);
  box-shadow:0 0 0 4px rgba(77,163,255,.10);
}

.taskRow{
  display:flex;
  justify-content:space-between;
  align-items:flex-start;
  gap:12px;
  padding:12px 12px;
  border-radius:16px;
  border:1px solid rgba(255,255,255,.08);
  background:rgba(0,0,0,.16);
}

.taskL{ flex:1; min-width:260px; }
.taskR{ display:flex; gap:10px; align-items:center; flex-wrap:wrap; }

.taskTitle{ font-weight:700; }
.taskDesc{ margin-top:4px; font-size:12.5px; color:var(--muted2); }

.btnRefresh{ margin-top:12px; }
.outPanel{ min-height:320px; max-height:420px; overflow:auto; }

.badge{
  padding:6px 10px;
  border-radius:999px;
  border:1px solid rgba(255,255,255,.12);
  font-size:12px;
  font-weight:700;
}
.badge.ok{ border-color:rgba(45,227,138,.35); color:rgba(45,227,138,.95); }
.badge.no{ border-color:rgba(255,77,109,.35); color:rgba(255,77,109,.95); }
.badge.wait{ border-color:rgba(255,255,255,.18); color:rgba(233,238,248,.75); }

```

### FILE: /opt/logos/www/shared/airdrop-fix.js
```
(() => {
  'use strict';
  const API='/airdrop-api/api/airdrop';
  const K_T='logos_airdrop_token_v1', K_X='logos_airdrop_xu_v1';
  // SYNC_TOKEN_KEYS_V1 (compat: logos_airdrop_token <-> logos_airdrop_token_v1)
  try{
    const t_old = localStorage.getItem("logos_airdrop_token");
    const t_v1  = localStorage.getItem(K_T);
    if(!t_v1 && t_old) localStorage.setItem(K_T, t_old);
    const t_now = localStorage.getItem(K_T);
    if(t_now) localStorage.setItem("logos_airdrop_token", t_now);
  }catch(e){}


  const qs = (k)=>{ try{return new URL(location.href).searchParams.get(k);}catch{return null;} };

  const post = async (path, body) => {
    const r = await fetch(API+path, {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify(body||{}),
      credentials:'same-origin',
    });
    const ct=r.headers.get('content-type')||'';
    const data = ct.includes('application/json') ? await r.json().catch(()=>({})) : await r.text().catch(()=> '');
    return {ok:r.ok, status:r.status, data};
  };

  const findInput = (re)=> Array.from(document.querySelectorAll('input')).find(i => re.test((i.placeholder||'')+' '+(i.name||'')+' '+(i.id||''))) || null;
  const findBtn = (t)=> Array.from(document.querySelectorAll('button,a')).find(b => ((b.textContent||'').trim().toLowerCase()===t)) || null;

  async function ensureToken(){
    let t=(localStorage.getItem(K_T)||'').trim();
    const ti = findInput(/token/i);
    if (ti && (ti.value||'').trim().length>=8) { t=(ti.value||'').trim(); localStorage.setItem(K_T,t); return t; }
    if (!t){
      const ref = (qs('ref')||qs('ref_token')||'').trim();
      const rr = await post('/register_web', ref ? {ref_token:ref}:{});
      if(!rr.ok || !rr.data || !rr.data.token) throw new Error('register_web failed');
      t=String(rr.data.token); localStorage.setItem(K_T,t);
      if (ti) ti.value=t;
    }
    return t;
  }

  function setRef(token, siteOrigin){
    const ri = findInput(/ref/i);
    if(!ri) return;
    const origin=(siteOrigin||'https://mw-expedition.com').replace(/\/+$/,'');
    ri.value = `${origin}/airdrop?ref=${encodeURIComponent(token)}`;
    const copy = findBtn('copy link') || findBtn('copy');
    if(copy && !copy.__l){ copy.__l=true; copy.addEventListener('click', async (e)=>{ e.preventDefault(); try{ await navigator.clipboard.writeText(ri.value);}catch{} }); }
  }

  function setTG(token){
    const url=`https://t.me/Logos_lrb_bot?start=airdrop_${encodeURIComponent(token)}`;
    for(const a of Array.from(document.querySelectorAll('a'))){
      const href=(a.getAttribute('href')||'');
      if(href.includes('t.me') && href.toLowerCase().includes('logos')) a.href=url;
      if(((a.textContent||'').trim().toLowerCase()==='open') && (a.closest('*')?.textContent||'').toLowerCase().includes('telegram')) a.href=url;
    }
  }

  function patchBadges(s){
    const set = (k, ok)=>{
      const blocks = Array.from(document.querySelectorAll('div,li,section'));
      const b = blocks.find(x => (x.textContent||'').toLowerCase().includes(k) && /(wait|ok)/i.test(x.textContent||''));
      if(!b) return;
      const badge = Array.from(b.querySelectorAll('span,div')).find(x => /^(wait|ok)$/i.test((x.textContent||'').trim()));
      if(badge) badge.textContent = ok ? 'OK':'WAIT';
    };
    set('wallet', !!s.wallet_bound);
    set('telegram', !!s.telegram_ok);
    set('follow', !!s.twitter_follow);
    set('like', !!s.twitter_like);
    set('repost', !!s.twitter_retweet);
    set('retweet', !!s.twitter_retweet);
  }

  async function refresh(){
    let t = await ensureToken();
    let r = await post('/status', {token:t});
    if(!r.ok && r.status===404){
      localStorage.removeItem(K_T);
      t = await ensureToken();
      r = await post('/status', {token:t});
    }
    if(!r.ok) return null;
    const s=r.data||{};
    setRef(t, s.site_origin);
    setTG(t);
    patchBadges(s);
    return s;
  }

  function wireX(){
    const xu = findInput(/yourname|username|twitter|x/i);
    const saved=(localStorage.getItem(K_X)||'').trim();
    if(xu && saved && !(xu.value||'').trim()) xu.value=saved;

    for(const b of Array.from(document.querySelectorAll('button')).filter(x => (x.textContent||'').trim().toLowerCase()==='save')){
      if(b.__xs) continue; b.__xs=true;
      b.addEventListener('click', async (e)=>{
        e.preventDefault();
        const t=await ensureToken();
        const inp = findInput(/yourname|username|twitter|x/i);
        let v=(inp?.value||'').trim().replace(/^@/,'');
        if(!v) return;
        localStorage.setItem(K_X,v);
        // ВАЖНО: поле именно twitter_username
        await post('/set_x_username', {token:t, twitter_username:v});
        await refresh();
      });
    }

    const vb=findBtn('verify');
    if(vb && !vb.__xv){ vb.__xv=true;
      vb.addEventListener('click', async (e)=>{
        e.preventDefault();
        const t=await ensureToken();
        await post('/verify_x', {token:t});
        await refresh();
      });
    }
  }

  function wireRefresh(){
    const b=findBtn('refresh status') || findBtn('refresh');
    if(!b || b.__rs) return;
    b.__rs=true;
    b.addEventListener('click', async (e)=>{ e.preventDefault(); await refresh(); });
  }

  async function boot(){
    try{
      await ensureToken();
      wireRefresh();
      wireX();
      await refresh();
    }catch(e){ console.error('airdrop-fix boot', e); }
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();

  function setLatestTweetLink(st) {
    try {
      const id = st && (st.x_latest_tweet_id || st.x_latest_tweet || st.latest_tweet_id);
      if (!id) return;
      const url = `https://x.com/RspLogos/status/${id}`;
      const el = document.querySelector('[data-task="x_repost"], #task_x_repost, #xRepostLink') || null;
      // fallback: find by text
      let container = el;
      if (!container) {
        const nodes = Array.from(document.querySelectorAll("div,section,li,p"));
        container = nodes.find(n => (n.textContent||"").toLowerCase().includes("x repost") || (n.textContent||"").toLowerCase().includes("ретвит"));
      }
      if (!container) return;
      let a = document.getElementById("x_latest_tweet_a");
      if (!a) {
        a = document.createElement("a");
        a.id = "x_latest_tweet_a";
        a.target = "_blank";
        a.rel = "noopener noreferrer";
        a.style.display = "inline-block";
        a.style.marginLeft = "10px";
        a.textContent = "Открыть проверяемый пост";
        container.appendChild(a);
      }
      a.href = url;
    } catch {}
  }

})();

;

```

### FILE: /opt/logos/www/shared/airdrop.js
```
(() => {
  const API = "/api/airdrop";
  const SITE = "https://mw-expedition.com";

  const LS_TOKEN = "airdrop_token";
  const LS_REF   = "airdrop_ref";

  const $ = (q) => document.querySelector(q);

  function out(s){
    const el = $("#out");
    if (el) el.textContent = String(s || "");
  }

  function badge(sel, state){
    const el = $(sel);
    if (!el) return;
    el.className = "badge " + (state || "wait");
    el.textContent = (state || "WAIT").toUpperCase();
  }

  function normX(s){
    s = (s||"").trim();
    if (s.startsWith("@")) s = s.slice(1);
    s = s.replace("https://x.com/","").replace("http://x.com/","");
    s = s.replace("https://twitter.com/","").replace("http://twitter.com/","");
    s = s.split("?")[0].split("/")[0].trim().toLowerCase();
    return s;
  }

  async function jpost(url, body){
    const r = await fetch(url, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify(body || {})
    });
    const t = await r.text();
    let j = null;
    try{ j = t ? JSON.parse(t) : {}; }catch(e){ j = {raw:t}; }
    if (!r.ok){
      const msg = (j && (j.detail || j.error || j.message)) ? JSON.stringify(j) : t;
      throw new Error(`API ${r.status}: ${msg}`);
    }
    return j;
  }

  async function apiPost(path, body){
    return await jpost(API + path, body);
  }

  function getRefFromUrl(){
    try{
      const q = new URLSearchParams(location.search);
      const r = (q.get("ref") || "").trim();
      return r || "";
    }catch(e){
      return "";
    }
  }

  async function ensureToken(){
    // 1) ref из URL сохраняем (если есть)
    const urlRef = getRefFromUrl();
    if (urlRef) localStorage.setItem(LS_REF, urlRef);

    // 2) если токена нет — регистрируемся
    let tok = (localStorage.getItem(LS_TOKEN) || "").trim();
    if (tok) return tok;

    const ref = (localStorage.getItem(LS_REF) || "").trim() || null;
    const rr = await apiPost("/register_web", { ref_token: ref });
    if (!rr || !rr.ok || !rr.token) throw new Error("register_web failed");
    tok = String(rr.token).trim();
    localStorage.setItem(LS_TOKEN, tok);
    return tok;
  }

  function fillTokenUI(tok){
    const tokenEl = $("#inpToken");
    if (tokenEl) tokenEl.value = tok;

    const refEl = $("#inpRef");
    if (refEl) refEl.value = `${SITE}/airdrop.html?ref=${encodeURIComponent(tok)}`;
  }

  async function status(){
    const tok = await ensureToken();
    const st = await apiPost("/status", { token: tok });

    // badges
    badge("#b_wallet", st.wallet_bound ? "ok" : "no");
    badge("#b_tg", st.telegram_ok ? "ok" : "wait");
    badge("#b_tw_follow", st.twitter_follow ? "ok" : "wait");
    badge("#b_tw_like", st.twitter_like ? "ok" : "wait");
    badge("#b_tw_rt", st.twitter_retweet ? "ok" : "wait");
    badge("#b_tw_user", (st && st.token) ? "ok" : "wait");

    // stats
    const sp = $("#s_points"); if (sp) sp.textContent = String(st.points ?? "—");
    const sr = $("#s_rank");   if (sr) sr.textContent = String(st.rank ?? "—");
    const sf = $("#s_refs");   if (sf) sf.textContent = String(st.referrals ?? "—");

    // token/ref UI
    fillTokenUI(tok);

    out(JSON.stringify(st, null, 2));
    return st;
  }

  async function saveXUser(){
    const tok = await ensureToken();
    const inp = $("#inpTwUser") || $("#inpXUser");
    const u = normX(inp ? inp.value : "");
    if(!u) throw new Error("Введите X username");
    await apiPost("/set_x_username", { token: tok, twitter_username: u });
    out("X username сохранён: @" + u);
    await status();
  }

  async function verifyX(){
    const tok = await ensureToken();
    const res = await apiPost("/verify_x", { token: tok });
    out(JSON.stringify(res, null, 2));
    await status();
  }

  // wallet connect flow (postMessage)
  function b64urlToBytes(s){
    s = (s||"").trim().replace(/-/g,"+").replace(/_/g,"/");
    s += "===".slice((s.length + 3) % 4);
    const bin = atob(s);
    const out = new Uint8Array(bin.length);
    for(let i=0;i<bin.length;i++) out[i]=bin.charCodeAt(i);
    return out;
  }
  function bytesToHex(u8){
    let h="";
    for(const b of u8){ h += b.toString(16).padStart(2,"0"); }
    return h;
  }

    async function walletConnect(){
    const tok = localStorage.getItem(LS_TOKEN) || "";
    if(!tok) throw new Error("no token");

    out("Запрашиваю challenge...");
    const ridHint = ""; // rid получим в кошельке после логина
    const ch = await apiPost("/wallet_challenge", { token: tok, wallet_rid: "RID_PLACEHOLDER" });

    // IMPORTANT: backend требует wallet_rid, но мы не знаем RID до логина.
    // Поэтому делаем так: запросим challenge ещё раз уже в wallet после логина.
    // Тут просто сохраняем токен и открываем connect режим.
    try{ localStorage.setItem("logos_airdrop_token", tok); }catch(e){}
    out("Открыл wallet. Войди в кошелёк — привязка произойдёт автоматически.");
    const url = "/wallet/auth.html?connect=1";
    window.open(url, "_blank");
  }

  window.addEventListener("message", async (ev) => {
    try{
      if(ev.origin !== location.origin) return;
      const d = ev.data || {};

      // wallet says RID ready
      if(d.type === "LOGOS_WALLET_CONNECT_READY" && d.rid){
        const tok = await ensureToken();
        const rid = String(d.rid).trim();
        if(!rid) return;

        out("RID получен. Запрашиваю challenge...");
        const ch = await apiPost("/wallet_challenge", { token: tok, wallet_rid: rid });

        // fallback channel: store challenge in shared localStorage (works even if postMessage fails)
        try{ localStorage.setItem("logos_connect_challenge", String(ch.challenge||"")); }catch(e){}


        if(window.__logosConnectWin && !window.__logosConnectWin.closed){
          window.__logosConnectWin.postMessage({ type:"LOGOS_WALLET_CONNECT_CHALLENGE", challenge: ch.challenge }, location.origin);
        } else {
          out("Окно wallet закрыто. Нажми Connect ещё раз.");
        }
        return;
      }

      // wallet returns signature
      if(d.type === "LOGOS_WALLET_CONNECT" && d.rid && d.sig && d.challenge){
        const tok = await ensureToken();
        const rid = String(d.rid).trim();
        const sigHex = bytesToHex(b64urlToBytes(String(d.sig)));

        out("Подпись получена. Привязываю кошелёк...");
        const res = await apiPost("/wallet_bind", { token: tok, wallet_rid: rid, sig_b64: String(d.sig) });

        try{ localStorage.removeItem("logos_connect_challenge"); }catch(e){}


        out(JSON.stringify(res, null, 2));
        await status();
        return;
      }
    }catch(e){
      out("ERR: " + (e && e.message ? e.message : String(e)));
    }
  });

  function copy(id){
    const el = $(id);
    if(!el) return;
    el.select && el.select();
    try{ document.execCommand("copy"); }catch(e){}
  }

  function bind(){
    const b1=$("#btnCopyToken"); if(b1) b1.addEventListener("click", ()=>copy("#inpToken"));
    const b2=$("#btnCopyRef");   if(b2) b2.addEventListener("click", ()=>copy("#inpRef"));

    const bw=$("#btnWallet"); if(bw) bw.addEventListener("click", ()=>walletConnect().catch(e=>out(e.message||e)));

    const bs=$("#btnTwSave"); if(bs) bs.addEventListener("click", ()=>saveXUser().catch(e=>out(e.message||e)));
    const bx=$("#btnXSave");  if(bx) bx.addEventListener("click", ()=>saveXUser().catch(e=>out(e.message||e)));
    const bv=$("#btnXVerify");if(bv) bv.addEventListener("click", ()=>verifyX().catch(e=>out(e.message||e)));

    const br=$("#btnRefresh"); if(br) br.addEventListener("click", async ()=>{
      try{
        await status();
      }catch(e){
        out(e.message||e);
      }
    });

    status().catch(e=>out(e.message||e));
  }

  document.addEventListener("DOMContentLoaded", bind);
})();

```

### FILE: /opt/logos/www/shared/airdrop-x.js
```
(function(){
  const API = "/airdrop-api/api/airdrop";
  const LS_TOKEN = "logos_airdrop_token";
  // SYNC_TOKEN_KEYS_V1 (compat: logos_airdrop_token <-> logos_airdrop_token_v1)
  try{
    const t_v1 = localStorage.getItem("logos_airdrop_token_v1");
    const t_old = localStorage.getItem(LS_TOKEN);
    if(!t_old && t_v1) localStorage.setItem(LS_TOKEN, t_v1);
    const t_now = localStorage.getItem(LS_TOKEN);
    if(t_now) localStorage.setItem("logos_airdrop_token_v1", t_now);
  }catch(e){}


  const $ = (s)=>document.querySelector(s);

  function getToken(){
    const t = (localStorage.getItem(LS_TOKEN) || "").trim();
    if (t) return t;
    const inp = $("#inpToken");
    return (inp && inp.value ? String(inp.value).trim() : "");
  }

  async function post(path, body){
    const r = await fetch(API + path, {
      method: "POST",
      headers: {"content-type":"application/json"},
      body: JSON.stringify(body),
    });
    const txt = await r.text();
    let data = {};
    try { data = txt ? JSON.parse(txt) : {}; } catch(e){ data = { ok:false, error:"bad_json", message: txt }; }
    if (!r.ok) {
      const msg = (data && (data.detail || data.message || data.error)) || ("HTTP " + r.status);
      throw new Error(msg);
    }
    return data;
  }

  function out(msg){
    const el = $("#out");
    if (el) el.textContent = String(msg);
  }

  function refresh(){
    const b = $("#btnRefresh");
    if (b) b.click();
  }

  async function saveX(){
    const tok = getToken();
    if (!tok) throw new Error("Нет token (сначала зарегистрируйся на airdrop)");
    const inp = $("#inpXUser");
    const uname = (inp && inp.value ? String(inp.value).trim() : "");
    if (!uname) throw new Error("Введи X username (@name или ссылку)");
    const st = await post("/set_x_username", { token: tok, twitter_username: uname });
    out("X username сохранён: " + (st.twitter_username || uname));
    refresh();
  }

  async function verifyX(){
    const tok = getToken();
    if (!tok) throw new Error("Нет token");
    const st = await post("/verify_x", { token: tok });
    out("X verify OK: follow=" + st.twitter_follow + " like=" + st.twitter_like + " rt=" + st.twitter_retweet);
    refresh();
  }

  window.addEventListener("DOMContentLoaded", ()=>{
    const s = $("#btnXSave");
    const v = $("#btnXVerify");
    if (s) s.addEventListener("click", ()=>saveX().catch(e=>out("Ошибка: " + e.message)));
    if (v) v.addEventListener("click", ()=>verifyX().catch(e=>out("Ошибка: " + e.message)));
  });
})();

```

### FILE: /opt/logos/www/shared/i18n.js
```
(() => {
  const SUPPORTED = [
    'ru','en','de',
    'es','fr','it','pt',
    'id','vi','hi',
    'ja','ko','zh',
    'ar','cs'
  ];
  const DEFAULT = 'en';

  const DICT = {
    en: {
      'wallet.title': 'LOGOS Wallet — Secure',
      'wallet.subtitle': 'WebCrypto + IndexedDB + 16-word backup phrase',
      'wallet.login_existing': 'Log in to existing wallet',
      'wallet.create_new': 'Create a new wallet',
      'wallet.restore': 'Restore wallet from phrase'
    },
    ru: {
      'wallet.title': 'LOGOS Wallet — Кошелёк',
      'wallet.subtitle': 'WebCrypto + IndexedDB + резервная фраза из 16 слов',
      'wallet.login_existing': 'Вход в существующий кошелёк',
      'wallet.create_new': 'Создать новый кошелёк',
      'wallet.restore': 'Восстановить кошелёк по фразе'
    },
    de: {
      'wallet.title': 'LOGOS Wallet — Wallet',
      'wallet.subtitle': 'WebCrypto + IndexedDB + 16‑Wörter‑Backup',
      'wallet.login_existing': 'Bestehendes Wallet öffnen',
      'wallet.create_new': 'Neues Wallet erstellen',
      'wallet.restore': 'Wallet mit Phrase wiederherstellen'
    },

    # остальные языки пока пустые — для них будет fallback на EN
    es: {}, fr: {}, it: {}, pt: {},
    id: {}, vi: {}, hi: {},
    ja: {}, ko: {}, zh: {},
    ar: {}, cs: {}
  };

  function pickLang() {
    try {
      const stored = localStorage.getItem('logos_lang');
      if (stored && SUPPORTED.includes(stored)) return stored;
    } catch (_) {}

    const nav = (navigator.language || navigator.userLanguage || '')
      .slice(0, 2).toLowerCase();
    if (SUPPORTED.includes(nav)) return nav;
    return DEFAULT;
  }

  function applyLang(lang) {
    const dict = DICT[lang] || DICT[DEFAULT] || {};
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      const value = dict[key]
        || (DICT[DEFAULT] && DICT[DEFAULT][key])
        || '';
      if (value) el.textContent = value;
    });
    document.documentElement.lang = lang;
  }

  function renderSwitcher(containerSelector) {
    const cont = document.querySelector(containerSelector);
    if (!cont) return;

    cont.classList.add('logos-lang-switcher');

    SUPPORTED.forEach(code => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.textContent = code.toUpperCase();
      btn.dataset.lang = code;
      btn.addEventListener('click', () => {
        const lang = btn.dataset.lang;
        try { localStorage.setItem('logos_lang', lang); } catch (_) {}
        applyLang(lang);
        cont.querySelectorAll('button').forEach(b =>
          b.classList.toggle('active', b === btn)
        );
      });
      cont.appendChild(btn);
    });
  }

  window.LOGOS_I18N = {
    init(containerSelector) {
      const lang = pickLang();
      try { localStorage.setItem('logos_lang', lang); } catch (_) {}
      applyLang(lang);
      if (containerSelector) renderSwitcher(containerSelector);
    }
  };
})();

```

### FILE: /opt/logos/www/shared/tweetnacl.min.js
```
!function(i){"use strict";var m=function(r,n){this.hi=0|r,this.lo=0|n},v=function(r){var n,e=new Float64Array(16);if(r)for(n=0;n<r.length;n++)e[n]=r[n];return e},a=function(){throw new Error("no PRNG")},o=new Uint8Array(16),e=new Uint8Array(32);e[0]=9;var c=v(),w=v([1]),g=v([56129,1]),y=v([30883,4953,19914,30187,55467,16705,2637,112,59544,30585,16505,36039,65139,11119,27886,20995]),l=v([61785,9906,39828,60374,45398,33411,5274,224,53552,61171,33010,6542,64743,22239,55772,9222]),t=v([54554,36645,11616,51542,42930,38181,51040,26924,56412,64982,57905,49316,21502,52590,14035,8553]),f=v([26200,26214,26214,26214,26214,26214,26214,26214,26214,26214,26214,26214,26214,26214,26214,26214]),s=v([41136,18958,6951,50414,58488,44335,6150,12099,55207,15867,153,11085,57099,20417,9344,11139]);function h(r,n){return r<<n|r>>>32-n}function b(r,n){var e=255&r[n+3];return(e=(e=e<<8|255&r[n+2])<<8|255&r[n+1])<<8|255&r[n+0]}function B(r,n){var e=r[n]<<24|r[n+1]<<16|r[n+2]<<8|r[n+3],t=r[n+4]<<24|r[n+5]<<16|r[n+6]<<8|r[n+7];return new m(e,t)}function p(r,n,e){var t;for(t=0;t<4;t++)r[n+t]=255&e,e>>>=8}function S(r,n,e){r[n]=e.hi>>24&255,r[n+1]=e.hi>>16&255,r[n+2]=e.hi>>8&255,r[n+3]=255&e.hi,r[n+4]=e.lo>>24&255,r[n+5]=e.lo>>16&255,r[n+6]=e.lo>>8&255,r[n+7]=255&e.lo}function u(r,n,e,t,o){var i,a=0;for(i=0;i<o;i++)a|=r[n+i]^e[t+i];return(1&a-1>>>8)-1}function A(r,n,e,t){return u(r,n,e,t,16)}function _(r,n,e,t){return u(r,n,e,t,32)}function U(r,n,e,t,o){var i,a,f,u=new Uint32Array(16),c=new Uint32Array(16),w=new Uint32Array(16),y=new Uint32Array(4);for(i=0;i<4;i++)c[5*i]=b(t,4*i),c[1+i]=b(e,4*i),c[6+i]=b(n,4*i),c[11+i]=b(e,16+4*i);for(i=0;i<16;i++)w[i]=c[i];for(i=0;i<20;i++){for(a=0;a<4;a++){for(f=0;f<4;f++)y[f]=c[(5*a+4*f)%16];for(y[1]^=h(y[0]+y[3]|0,7),y[2]^=h(y[1]+y[0]|0,9),y[3]^=h(y[2]+y[1]|0,13),y[0]^=h(y[3]+y[2]|0,18),f=0;f<4;f++)u[4*a+(a+f)%4]=y[f]}for(f=0;f<16;f++)c[f]=u[f]}if(o){for(i=0;i<16;i++)c[i]=c[i]+w[i]|0;for(i=0;i<4;i++)c[5*i]=c[5*i]-b(t,4*i)|0,c[6+i]=c[6+i]-b(n,4*i)|0;for(i=0;i<4;i++)p(r,4*i,c[5*i]),p(r,16+4*i,c[6+i])}else for(i=0;i<16;i++)p(r,4*i,c[i]+w[i]|0)}function E(r,n,e,t){U(r,n,e,t,!1)}function x(r,n,e,t){return U(r,n,e,t,!0),0}var d=new Uint8Array([101,120,112,97,110,100,32,51,50,45,98,121,116,101,32,107]);function K(r,n,e,t,o,i,a){var f,u,c=new Uint8Array(16),w=new Uint8Array(64);if(!o)return 0;for(u=0;u<16;u++)c[u]=0;for(u=0;u<8;u++)c[u]=i[u];for(;64<=o;){for(E(w,c,a,d),u=0;u<64;u++)r[n+u]=(e?e[t+u]:0)^w[u];for(f=1,u=8;u<16;u++)f=f+(255&c[u])|0,c[u]=255&f,f>>>=8;o-=64,n+=64,e&&(t+=64)}if(0<o)for(E(w,c,a,d),u=0;u<o;u++)r[n+u]=(e?e[t+u]:0)^w[u];return 0}function Y(r,n,e,t,o){return K(r,n,null,0,e,t,o)}function L(r,n,e,t,o){var i=new Uint8Array(32);return x(i,t,o,d),Y(r,n,e,t.subarray(16),i)}function T(r,n,e,t,o,i,a){var f=new Uint8Array(32);return x(f,i,a,d),K(r,n,e,t,o,i.subarray(16),f)}function k(r,n){var e,t=0;for(e=0;e<17;e++)t=t+(r[e]+n[e]|0)|0,r[e]=255&t,t>>>=8}var z=new Uint32Array([5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,252]);function R(r,n,e,t,o,i){var a,f,u,c,w=new Uint32Array(17),y=new Uint32Array(17),l=new Uint32Array(17),s=new Uint32Array(17),h=new Uint32Array(17);for(u=0;u<17;u++)y[u]=l[u]=0;for(u=0;u<16;u++)y[u]=i[u];for(y[3]&=15,y[4]&=252,y[7]&=15,y[8]&=252,y[11]&=15,y[12]&=252,y[15]&=15;0<o;){for(u=0;u<17;u++)s[u]=0;for(u=0;u<16&&u<o;++u)s[u]=e[t+u];for(s[u]=1,t+=u,o-=u,k(l,s),f=0;f<17;f++)for(u=w[f]=0;u<17;u++)w[f]=w[f]+l[u]*(u<=f?y[f-u]:320*y[f+17-u]|0)|0;for(f=0;f<17;f++)l[f]=w[f];for(u=c=0;u<16;u++)c=c+l[u]|0,l[u]=255&c,c>>>=8;for(c=c+l[16]|0,l[16]=3&c,c=5*(c>>>2)|0,u=0;u<16;u++)c=c+l[u]|0,l[u]=255&c,c>>>=8;c=c+l[16]|0,l[16]=c}for(u=0;u<17;u++)h[u]=l[u];for(k(l,z),a=0|-(l[16]>>>7),u=0;u<17;u++)l[u]^=a&(h[u]^l[u]);for(u=0;u<16;u++)s[u]=i[u+16];for(s[16]=0,k(l,s),u=0;u<16;u++)r[n+u]=l[u];return 0}function P(r,n,e,t,o,i){var a=new Uint8Array(16);return R(a,0,e,t,o,i),A(r,n,a,0)}function M(r,n,e,t,o){var i;if(e<32)return-1;for(T(r,0,n,0,e,t,o),R(r,16,r,32,e-32,r),i=0;i<16;i++)r[i]=0;return 0}function N(r,n,e,t,o){var i,a=new Uint8Array(32);if(e<32)return-1;if(L(a,0,32,t,o),0!==P(n,16,n,32,e-32,a))return-1;for(T(r,0,n,0,e,t,o),i=0;i<32;i++)r[i]=0;return 0}function O(r,n){var e;for(e=0;e<16;e++)r[e]=0|n[e]}function C(r){var n,e;for(e=0;e<16;e++)r[e]+=65536,n=Math.floor(r[e]/65536),r[(e+1)*(e<15?1:0)]+=n-1+37*(n-1)*(15===e?1:0),r[e]-=65536*n}function F(r,n,e){for(var t,o=~(e-1),i=0;i<16;i++)t=o&(r[i]^n[i]),r[i]^=t,n[i]^=t}function Z(r,n){var e,t,o,i=v(),a=v();for(e=0;e<16;e++)a[e]=n[e];for(C(a),C(a),C(a),t=0;t<2;t++){for(i[0]=a[0]-65517,e=1;e<15;e++)i[e]=a[e]-65535-(i[e-1]>>16&1),i[e-1]&=65535;i[15]=a[15]-32767-(i[14]>>16&1),o=i[15]>>16&1,i[14]&=65535,F(a,i,1-o)}for(e=0;e<16;e++)r[2*e]=255&a[e],r[2*e+1]=a[e]>>8}function G(r,n){var e=new Uint8Array(32),t=new Uint8Array(32);return Z(e,r),Z(t,n),_(e,0,t,0)}function q(r){var n=new Uint8Array(32);return Z(n,r),1&n[0]}function D(r,n){var e;for(e=0;e<16;e++)r[e]=n[2*e]+(n[2*e+1]<<8);r[15]&=32767}function I(r,n,e){var t;for(t=0;t<16;t++)r[t]=n[t]+e[t]|0}function V(r,n,e){var t;for(t=0;t<16;t++)r[t]=n[t]-e[t]|0}function X(r,n,e){var t,o,i=new Float64Array(31);for(t=0;t<31;t++)i[t]=0;for(t=0;t<16;t++)for(o=0;o<16;o++)i[t+o]+=n[t]*e[o];for(t=0;t<15;t++)i[t]+=38*i[t+16];for(t=0;t<16;t++)r[t]=i[t];C(r),C(r)}function j(r,n){X(r,n,n)}function H(r,n){var e,t=v();for(e=0;e<16;e++)t[e]=n[e];for(e=253;0<=e;e--)j(t,t),2!==e&&4!==e&&X(t,t,n);for(e=0;e<16;e++)r[e]=t[e]}function J(r,n){var e,t=v();for(e=0;e<16;e++)t[e]=n[e];for(e=250;0<=e;e--)j(t,t),1!==e&&X(t,t,n);for(e=0;e<16;e++)r[e]=t[e]}function Q(r,n,e){var t,o,i=new Uint8Array(32),a=new Float64Array(80),f=v(),u=v(),c=v(),w=v(),y=v(),l=v();for(o=0;o<31;o++)i[o]=n[o];for(i[31]=127&n[31]|64,i[0]&=248,D(a,e),o=0;o<16;o++)u[o]=a[o],w[o]=f[o]=c[o]=0;for(f[0]=w[0]=1,o=254;0<=o;--o)F(f,u,t=i[o>>>3]>>>(7&o)&1),F(c,w,t),I(y,f,c),V(f,f,c),I(c,u,w),V(u,u,w),j(w,y),j(l,f),X(f,c,f),X(c,u,y),I(y,f,c),V(f,f,c),j(u,f),V(c,w,l),X(f,c,g),I(f,f,w),X(c,c,f),X(f,w,l),X(w,u,a),j(u,y),F(f,u,t),F(c,w,t);for(o=0;o<16;o++)a[o+16]=f[o],a[o+32]=c[o],a[o+48]=u[o],a[o+64]=w[o];var s=a.subarray(32),h=a.subarray(16);return H(s,s),X(h,h,s),Z(r,h),0}function W(r,n){return Q(r,n,e)}function $(r,n){return a(n,32),W(r,n)}function rr(r,n,e){var t=new Uint8Array(32);return Q(t,e,n),x(r,o,t,d)}var nr=M,er=N;function tr(){var r,n,e,t=0,o=0,i=0,a=0,f=65535;for(e=0;e<arguments.length;e++)t+=(r=arguments[e].lo)&f,o+=r>>>16,i+=(n=arguments[e].hi)&f,a+=n>>>16;return new m((i+=(o+=t>>>16)>>>16)&f|(a+=i>>>16)<<16,t&f|o<<16)}function or(r,n){return new m(r.hi>>>n,r.lo>>>n|r.hi<<32-n)}function ir(){var r,n=0,e=0;for(r=0;r<arguments.length;r++)n^=arguments[r].lo,e^=arguments[r].hi;return new m(e,n)}function ar(r,n){var e,t,o=32-n;return n<32?(e=r.hi>>>n|r.lo<<o,t=r.lo>>>n|r.hi<<o):n<64&&(e=r.lo>>>n|r.hi<<o,t=r.hi>>>n|r.lo<<o),new m(e,t)}var fr=[new m(1116352408,3609767458),new m(1899447441,602891725),new m(3049323471,3964484399),new m(3921009573,2173295548),new m(961987163,4081628472),new m(1508970993,3053834265),new m(2453635748,2937671579),new m(2870763221,3664609560),new m(3624381080,2734883394),new m(310598401,1164996542),new m(607225278,1323610764),new m(1426881987,3590304994),new m(1925078388,4068182383),new m(2162078206,991336113),new m(2614888103,633803317),new m(3248222580,3479774868),new m(3835390401,2666613458),new m(4022224774,944711139),new m(264347078,2341262773),new m(604807628,2007800933),new m(770255983,1495990901),new m(1249150122,1856431235),new m(1555081692,3175218132),new m(1996064986,2198950837),new m(2554220882,3999719339),new m(2821834349,766784016),new m(2952996808,2566594879),new m(3210313671,3203337956),new m(3336571891,1034457026),new m(3584528711,2466948901),new m(113926993,3758326383),new m(338241895,168717936),new m(666307205,1188179964),new m(773529912,1546045734),new m(1294757372,1522805485),new m(1396182291,2643833823),new m(1695183700,2343527390),new m(1986661051,1014477480),new m(2177026350,1206759142),new m(2456956037,344077627),new m(2730485921,1290863460),new m(2820302411,3158454273),new m(3259730800,3505952657),new m(3345764771,106217008),new m(3516065817,3606008344),new m(3600352804,1432725776),new m(4094571909,1467031594),new m(275423344,851169720),new m(430227734,3100823752),new m(506948616,1363258195),new m(659060556,3750685593),new m(883997877,3785050280),new m(958139571,3318307427),new m(1322822218,3812723403),new m(1537002063,2003034995),new m(1747873779,3602036899),new m(1955562222,1575990012),new m(2024104815,1125592928),new m(2227730452,2716904306),new m(2361852424,442776044),new m(2428436474,593698344),new m(2756734187,3733110249),new m(3204031479,2999351573),new m(3329325298,3815920427),new m(3391569614,3928383900),new m(3515267271,566280711),new m(3940187606,3454069534),new m(4118630271,4000239992),new m(116418474,1914138554),new m(174292421,2731055270),new m(289380356,3203993006),new m(460393269,320620315),new m(685471733,587496836),new m(852142971,1086792851),new m(1017036298,365543100),new m(1126000580,2618297676),new m(1288033470,3409855158),new m(1501505948,4234509866),new m(1607167915,987167468),new m(1816402316,1246189591)];function ur(r,n,e){var t,o,i,a=[],f=[],u=[],c=[];for(o=0;o<8;o++)a[o]=u[o]=B(r,8*o);for(var w,y,l,s,h,v,g,b,p,A,_,U,E,x,d=0;128<=e;){for(o=0;o<16;o++)c[o]=B(n,8*o+d);for(o=0;o<80;o++){for(i=0;i<8;i++)f[i]=u[i];for(t=tr(u[7],ir(ar(x=u[4],14),ar(x,18),ar(x,41)),(p=u[4],A=u[5],_=u[6],0,U=p.hi&A.hi^~p.hi&_.hi,E=p.lo&A.lo^~p.lo&_.lo,new m(U,E)),fr[o],c[o%16]),f[7]=tr(t,ir(ar(b=u[0],28),ar(b,34),ar(b,39)),(l=u[0],s=u[1],h=u[2],0,v=l.hi&s.hi^l.hi&h.hi^s.hi&h.hi,g=l.lo&s.lo^l.lo&h.lo^s.lo&h.lo,new m(v,g))),f[3]=tr(f[3],t),i=0;i<8;i++)u[(i+1)%8]=f[i];if(o%16==15)for(i=0;i<16;i++)c[i]=tr(c[i],c[(i+9)%16],ir(ar(y=c[(i+1)%16],1),ar(y,8),or(y,7)),ir(ar(w=c[(i+14)%16],19),ar(w,61),or(w,6)))}for(o=0;o<8;o++)u[o]=tr(u[o],a[o]),a[o]=u[o];d+=128,e-=128}for(o=0;o<8;o++)S(r,8*o,a[o]);return e}var cr=new Uint8Array([106,9,230,103,243,188,201,8,187,103,174,133,132,202,167,59,60,110,243,114,254,148,248,43,165,79,245,58,95,29,54,241,81,14,82,127,173,230,130,209,155,5,104,140,43,62,108,31,31,131,217,171,251,65,189,107,91,224,205,25,19,126,33,121]);function wr(r,n,e){var t,o=new Uint8Array(64),i=new Uint8Array(256),a=e;for(t=0;t<64;t++)o[t]=cr[t];for(ur(o,n,e),e%=128,t=0;t<256;t++)i[t]=0;for(t=0;t<e;t++)i[t]=n[a-e+t];for(i[e]=128,i[(e=256-128*(e<112?1:0))-9]=0,S(i,e-8,new m(a/536870912|0,a<<3)),ur(o,i,e),t=0;t<64;t++)r[t]=o[t];return 0}function yr(r,n){var e=v(),t=v(),o=v(),i=v(),a=v(),f=v(),u=v(),c=v(),w=v();V(e,r[1],r[0]),V(w,n[1],n[0]),X(e,e,w),I(t,r[0],r[1]),I(w,n[0],n[1]),X(t,t,w),X(o,r[3],n[3]),X(o,o,l),X(i,r[2],n[2]),I(i,i,i),V(a,t,e),V(f,i,o),I(u,i,o),I(c,t,e),X(r[0],a,f),X(r[1],c,u),X(r[2],u,f),X(r[3],a,c)}function lr(r,n,e){var t;for(t=0;t<4;t++)F(r[t],n[t],e)}function sr(r,n){var e=v(),t=v(),o=v();H(o,n[2]),X(e,n[0],o),X(t,n[1],o),Z(r,t),r[31]^=q(e)<<7}function hr(r,n,e){var t,o;for(O(r[0],c),O(r[1],w),O(r[2],w),O(r[3],c),o=255;0<=o;--o)lr(r,n,t=e[o/8|0]>>(7&o)&1),yr(n,r),yr(r,r),lr(r,n,t)}function vr(r,n){var e=[v(),v(),v(),v()];O(e[0],t),O(e[1],f),O(e[2],w),X(e[3],t,f),hr(r,e,n)}function gr(r,n,e){var t,o=new Uint8Array(64),i=[v(),v(),v(),v()];for(e||a(n,32),wr(o,n,32),o[0]&=248,o[31]&=127,o[31]|=64,vr(i,o),sr(r,i),t=0;t<32;t++)n[t+32]=r[t];return 0}var br=new Float64Array([237,211,245,92,26,99,18,88,214,156,247,162,222,249,222,20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16]);function pr(r,n){var e,t,o,i;for(t=63;32<=t;--t){for(e=0,o=t-32,i=t-12;o<i;++o)n[o]+=e-16*n[t]*br[o-(t-32)],e=Math.floor((n[o]+128)/256),n[o]-=256*e;n[o]+=e,n[t]=0}for(o=e=0;o<32;o++)n[o]+=e-(n[31]>>4)*br[o],e=n[o]>>8,n[o]&=255;for(o=0;o<32;o++)n[o]-=e*br[o];for(t=0;t<32;t++)n[t+1]+=n[t]>>8,r[t]=255&n[t]}function Ar(r){var n,e=new Float64Array(64);for(n=0;n<64;n++)e[n]=r[n];for(n=0;n<64;n++)r[n]=0;pr(r,e)}function _r(r,n,e,t){var o,i,a=new Uint8Array(64),f=new Uint8Array(64),u=new Uint8Array(64),c=new Float64Array(64),w=[v(),v(),v(),v()];wr(a,t,32),a[0]&=248,a[31]&=127,a[31]|=64;var y=e+64;for(o=0;o<e;o++)r[64+o]=n[o];for(o=0;o<32;o++)r[32+o]=a[32+o];for(wr(u,r.subarray(32),e+32),Ar(u),vr(w,u),sr(r,w),o=32;o<64;o++)r[o]=t[o];for(wr(f,r,e+64),Ar(f),o=0;o<64;o++)c[o]=0;for(o=0;o<32;o++)c[o]=u[o];for(o=0;o<32;o++)for(i=0;i<32;i++)c[o+i]+=f[o]*a[i];return pr(r.subarray(32),c),y}function Ur(r,n,e,t){var o,i=new Uint8Array(32),a=new Uint8Array(64),f=[v(),v(),v(),v()],u=[v(),v(),v(),v()];if(e<64)return-1;if(function(r,n){var e=v(),t=v(),o=v(),i=v(),a=v(),f=v(),u=v();if(O(r[2],w),D(r[1],n),j(o,r[1]),X(i,o,y),V(o,o,r[2]),I(i,r[2],i),j(a,i),j(f,a),X(u,f,a),X(e,u,o),X(e,e,i),J(e,e),X(e,e,o),X(e,e,i),X(e,e,i),X(r[0],e,i),j(t,r[0]),X(t,t,i),G(t,o)&&X(r[0],r[0],s),j(t,r[0]),X(t,t,i),G(t,o))return 1;q(r[0])===n[31]>>7&&V(r[0],c,r[0]),X(r[3],r[0],r[1])}(u,t))return-1;for(o=0;o<e;o++)r[o]=n[o];for(o=0;o<32;o++)r[o+32]=t[o];if(wr(a,r,e),Ar(a),hr(f,u,a),vr(u,n.subarray(32)),yr(f,u),sr(i,f),e-=64,_(n,0,i,0)){for(o=0;o<e;o++)r[o]=0;return-1}for(o=0;o<e;o++)r[o]=n[o+64];return e}function Er(r,n){if(32!==r.length)throw new Error("bad key size");if(24!==n.length)throw new Error("bad nonce size")}function xr(){for(var r=0;r<arguments.length;r++)if(!(arguments[r]instanceof Uint8Array))throw new TypeError("unexpected type, use Uint8Array")}function dr(r){for(var n=0;n<r.length;n++)r[n]=0}i.lowlevel={crypto_core_hsalsa20:x,crypto_stream_xor:T,crypto_stream:L,crypto_stream_salsa20_xor:K,crypto_stream_salsa20:Y,crypto_onetimeauth:R,crypto_onetimeauth_verify:P,crypto_verify_16:A,crypto_verify_32:_,crypto_secretbox:M,crypto_secretbox_open:N,crypto_scalarmult:Q,crypto_scalarmult_base:W,crypto_box_beforenm:rr,crypto_box_afternm:nr,crypto_box:function(r,n,e,t,o,i){var a=new Uint8Array(32);return rr(a,o,i),nr(r,n,e,t,a)},crypto_box_open:function(r,n,e,t,o,i){var a=new Uint8Array(32);return rr(a,o,i),er(r,n,e,t,a)},crypto_box_keypair:$,crypto_hash:wr,crypto_sign:_r,crypto_sign_keypair:gr,crypto_sign_open:Ur,crypto_secretbox_KEYBYTES:32,crypto_secretbox_NONCEBYTES:24,crypto_secretbox_ZEROBYTES:32,crypto_secretbox_BOXZEROBYTES:16,crypto_scalarmult_BYTES:32,crypto_scalarmult_SCALARBYTES:32,crypto_box_PUBLICKEYBYTES:32,crypto_box_SECRETKEYBYTES:32,crypto_box_BEFORENMBYTES:32,crypto_box_NONCEBYTES:24,crypto_box_ZEROBYTES:32,crypto_box_BOXZEROBYTES:16,crypto_sign_BYTES:64,crypto_sign_PUBLICKEYBYTES:32,crypto_sign_SECRETKEYBYTES:64,crypto_sign_SEEDBYTES:32,crypto_hash_BYTES:64,gf:v,D:y,L:br,pack25519:Z,unpack25519:D,M:X,A:I,S:j,Z:V,pow2523:J,add:yr,set25519:O,modL:pr,scalarmult:hr,scalarbase:vr},i.randomBytes=function(r){var n=new Uint8Array(r);return a(n,r),n},i.secretbox=function(r,n,e){xr(r,n,e),Er(e,n);for(var t=new Uint8Array(32+r.length),o=new Uint8Array(t.length),i=0;i<r.length;i++)t[i+32]=r[i];return M(o,t,t.length,n,e),o.subarray(16)},i.secretbox.open=function(r,n,e){xr(r,n,e),Er(e,n);for(var t=new Uint8Array(16+r.length),o=new Uint8Array(t.length),i=0;i<r.length;i++)t[i+16]=r[i];return t.length<32||0!==N(o,t,t.length,n,e)?null:o.subarray(32)},i.secretbox.keyLength=32,i.secretbox.nonceLength=24,i.secretbox.overheadLength=16,i.scalarMult=function(r,n){if(xr(r,n),32!==r.length)throw new Error("bad n size");if(32!==n.length)throw new Error("bad p size");var e=new Uint8Array(32);return Q(e,r,n),e},i.scalarMult.base=function(r){if(xr(r),32!==r.length)throw new Error("bad n size");var n=new Uint8Array(32);return W(n,r),n},i.scalarMult.scalarLength=32,i.scalarMult.groupElementLength=32,i.box=function(r,n,e,t){var o=i.box.before(e,t);return i.secretbox(r,n,o)},i.box.before=function(r,n){xr(r,n),function(r,n){if(32!==r.length)throw new Error("bad public key size");if(32!==n.length)throw new Error("bad secret key size")}(r,n);var e=new Uint8Array(32);return rr(e,r,n),e},i.box.after=i.secretbox,i.box.open=function(r,n,e,t){var o=i.box.before(e,t);return i.secretbox.open(r,n,o)},i.box.open.after=i.secretbox.open,i.box.keyPair=function(){var r=new Uint8Array(32),n=new Uint8Array(32);return $(r,n),{publicKey:r,secretKey:n}},i.box.keyPair.fromSecretKey=function(r){if(xr(r),32!==r.length)throw new Error("bad secret key size");var n=new Uint8Array(32);return W(n,r),{publicKey:n,secretKey:new Uint8Array(r)}},i.box.publicKeyLength=32,i.box.secretKeyLength=32,i.box.sharedKeyLength=32,i.box.nonceLength=24,i.box.overheadLength=i.secretbox.overheadLength,i.sign=function(r,n){if(xr(r,n),64!==n.length)throw new Error("bad secret key size");var e=new Uint8Array(64+r.length);return _r(e,r,r.length,n),e},i.sign.open=function(r,n){if(xr(r,n),32!==n.length)throw new Error("bad public key size");var e=new Uint8Array(r.length),t=Ur(e,r,r.length,n);if(t<0)return null;for(var o=new Uint8Array(t),i=0;i<o.length;i++)o[i]=e[i];return o},i.sign.detached=function(r,n){for(var e=i.sign(r,n),t=new Uint8Array(64),o=0;o<t.length;o++)t[o]=e[o];return t},i.sign.detached.verify=function(r,n,e){if(xr(r,n,e),64!==n.length)throw new Error("bad signature size");if(32!==e.length)throw new Error("bad public key size");var t,o=new Uint8Array(64+r.length),i=new Uint8Array(64+r.length);for(t=0;t<64;t++)o[t]=n[t];for(t=0;t<r.length;t++)o[t+64]=r[t];return 0<=Ur(i,o,o.length,e)},i.sign.keyPair=function(){var r=new Uint8Array(32),n=new Uint8Array(64);return gr(r,n),{publicKey:r,secretKey:n}},i.sign.keyPair.fromSecretKey=function(r){if(xr(r),64!==r.length)throw new Error("bad secret key size");for(var n=new Uint8Array(32),e=0;e<n.length;e++)n[e]=r[32+e];return{publicKey:n,secretKey:new Uint8Array(r)}},i.sign.keyPair.fromSeed=function(r){if(xr(r),32!==r.length)throw new Error("bad seed size");for(var n=new Uint8Array(32),e=new Uint8Array(64),t=0;t<32;t++)e[t]=r[t];return gr(n,e,!0),{publicKey:n,secretKey:e}},i.sign.publicKeyLength=32,i.sign.secretKeyLength=64,i.sign.seedLength=32,i.sign.signatureLength=64,i.hash=function(r){xr(r);var n=new Uint8Array(64);return wr(n,r,r.length),n},i.hash.hashLength=64,i.verify=function(r,n){return xr(r,n),0!==r.length&&0!==n.length&&(r.length===n.length&&0===u(r,0,n,0,r.length))},i.setPRNG=function(r){a=r},function(){var o="undefined"!=typeof self?self.crypto||self.msCrypto:null;if(o&&o.getRandomValues){i.setPRNG(function(r,n){var e,t=new Uint8Array(n);for(e=0;e<n;e+=65536)o.getRandomValues(t.subarray(e,e+Math.min(n-e,65536)));for(e=0;e<n;e++)r[e]=t[e];dr(t)})}else"undefined"!=typeof require&&(o=require("crypto"))&&o.randomBytes&&i.setPRNG(function(r,n){var e,t=o.randomBytes(n);for(e=0;e<n;e++)r[e]=t[e];dr(t)})}()}("undefined"!=typeof module&&module.exports?module.exports:self.nacl=self.nacl||{});
```

### FILE: /opt/logos/www/shared/wallet-theme.css
```
/* LOGOS LRB — Wallet Theme (Lux v3, CSP-safe, self-hosted)
   - no inline styles required
   - no external fonts
   - fixes Chrome autofill white background
*/

:root{
  color-scheme: dark;

  --bg0:#05060a;
  --bg1:#070b14;

  --text:#e9eef8;
  --muted:rgba(233,238,248,.72);
  --muted2:rgba(233,238,248,.52);

  --surface0:rgba(13,16,24,.60);
  --surface1:rgba(13,16,24,.78);
  --surface2:rgba(13,16,24,.92);

  --field:rgba(6,8,14,.68);
  --field2:rgba(0,0,0,.30);

  --line:rgba(255,255,255,.08);
  --line2:rgba(255,255,255,.14);

  --accent:#4da3ff;
  --accent2:#7c5cff;

  --good:#2de38a;
  --bad:#ff4d6d;

  --r:20px;
  --r2:14px;

  --shadow:0 24px 90px rgba(0,0,0,.55);
  --shadowSm:0 12px 44px rgba(0,0,0,.48);

  --container:1100px;

  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;
  --sans:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Ubuntu,"Helvetica Neue",Arial,sans-serif;
}

*{box-sizing:border-box}
html,body{height:100%}

body.logos-ui{
  margin:0;
  font-family:var(--sans);
  color:var(--text);
  line-height:1.45;
  -webkit-font-smoothing:antialiased;
  -moz-osx-font-smoothing:grayscale;

  background-color:var(--bg0);
  background-image:
    radial-gradient(1200px 650px at 12% -10%, rgba(77,163,255,.22) 0%, rgba(77,163,255,0) 60%),
    radial-gradient(900px 600px at 92% -12%, rgba(124,92,255,.18) 0%, rgba(124,92,255,0) 58%),
    radial-gradient(900px 600px at 50% 120%, rgba(45,227,138,.10) 0%, rgba(45,227,138,0) 55%),
    linear-gradient(180deg,var(--bg1) 0%, var(--bg0) 46%, var(--bg0) 100%);
  background-attachment:fixed;
}

a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}

.muted{color:var(--muted)}
.muted2{color:var(--muted2)}
.mono{font-family:var(--mono)}

.container{
  max-width:var(--container);
  margin:0 auto;
  padding:18px 18px 56px;
}

.stack{
  display:grid;
  gap:18px;
  margin-top:18px;
}

.grid-2{
  display:grid;
  grid-template-columns:repeat(2,minmax(0,1fr));
  gap:18px;
}

@media (max-width:980px){
  .grid-2{grid-template-columns:1fr}
}

/* Topbar */
.topbar{
  position:sticky;
  top:0;
  z-index:50;
  border-bottom:1px solid var(--line);
  background:rgba(6,8,14,.55);
  backdrop-filter:blur(12px);
}

.topbar__inner{
  max-width:var(--container);
  margin:0 auto;
  padding:12px 18px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:14px;
}

.brand{
  display:flex;
  align-items:center;
  gap:12px;
  min-width:0;
}

.brand__mark{
  width:38px;
  height:38px;
  border-radius:14px;
  display:grid;
  place-items:center;
  color:#0b1020;
  font-weight:900;
  letter-spacing:.08em;
  font-size:12px;

  background:
    radial-gradient(18px 18px at 25% 20%, rgba(255,255,255,.85) 0%, rgba(255,255,255,0) 70%),
    linear-gradient(135deg, rgba(77,163,255,1) 0%, rgba(124,92,255,1) 70%);
  box-shadow:0 14px 40px rgba(77,163,255,.22);
  border:1px solid rgba(255,255,255,.18);
}

.brand__title{
  font-weight:780;
  font-size:14px;
  line-height:1.1;
}

.brand__sub{
  margin-top:2px;
  font-size:12px;
  color:var(--muted);
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
  max-width:52ch;
}

.topbar__right{
  display:flex;
  align-items:center;
  gap:10px;
  flex-wrap:wrap;
  justify-content:flex-end;
}

.pill{
  display:inline-flex;
  align-items:center;
  gap:8px;
  padding:8px 10px;
  border-radius:999px;
  border:1px solid var(--line);
  background:rgba(0,0,0,.22);
  color:var(--muted);
  font-size:12px;
}

.pill .mono{color:var(--text)}

/* Cards */
.card{
  border-radius:var(--r);
  border:1px solid transparent;
  background:
    linear-gradient(180deg, rgba(18,22,34,.74), rgba(12,15,26,.70)) padding-box,
    linear-gradient(135deg, rgba(77,163,255,.34), rgba(124,92,255,.22), rgba(255,255,255,.10)) border-box;
  box-shadow:var(--shadowSm);
  padding:18px;
}

.card.hero{padding:22px}

.card.hero h1{
  margin:0 0 6px;
  font-size:22px;
  letter-spacing:.2px;
}

.card.hero p{margin:0}

.card__head{
  display:flex;
  align-items:flex-start;
  justify-content:space-between;
  gap:14px;
  margin-bottom:12px;
}

.card__head h2{
  margin:0;
  font-size:16px;
  letter-spacing:.2px;
}

.card__head p{
  margin:6px 0 0;
  color:var(--muted);
  font-size:12px;
  max-width:70ch;
}

.card__body{display:grid;gap:10px}

small{color:var(--muted)}
hr{
  border:0;
  border-top:1px solid var(--line);
  margin:14px 0;
}

/* Form */
label{
  display:block;
  margin:12px 0 6px;
  font-size:12px;
  color:var(--muted);
}

input,textarea{
  width:100%;
  border-radius:var(--r2);
  border:1px solid var(--line2);
  background:var(--field);
  color:var(--text);
  padding:12px 12px;
  font-size:14px;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.06);
  transition:border-color .12s ease, box-shadow .12s ease, background .12s ease;
}

textarea{
  min-height:110px;
  resize:vertical;
}

input.mono,textarea.mono{
  font-family:var(--mono);
  letter-spacing:.1px;
}

input::placeholder,textarea::placeholder{
  color:rgba(233,238,248,.38);
}

input:focus,textarea:focus{
  outline:none;
  border-color:rgba(77,163,255,.56);
  box-shadow:
    0 0 0 4px rgba(77,163,255,.18),
    inset 0 1px 0 rgba(255,255,255,.06);
}

input[readonly],textarea[readonly]{
  background:rgba(0,0,0,.22);
  border-color:rgba(255,255,255,.10);
}

/* Chrome autofill fix (prevents white/yellow fields) */
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
textarea:-webkit-autofill{
  -webkit-text-fill-color:var(--text);
  caret-color:var(--text);
  -webkit-box-shadow:0 0 0 1000px rgba(6,8,14,.92) inset;
  transition:background-color 9999s ease-in-out 0s;
}

/* Outputs */
pre{
  width:100%;
  border-radius:var(--r2);
  border:1px solid var(--line);
  background:rgba(0,0,0,.28);
  color:var(--text);
  padding:12px 12px;
  margin:12px 0 0;
  overflow:auto;
  white-space:pre-wrap;
  word-break:break-word;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.04);
}

pre.mono{font-family:var(--mono);font-size:12.5px}

/* Buttons */
button{
  appearance:none;
  border-radius:var(--r2);
  border:1px solid var(--line2);
  background:rgba(255,255,255,.06);
  color:var(--text);
  padding:11px 14px;
  font-size:13px;
  font-weight:700;
  letter-spacing:.1px;
  cursor:pointer;
  display:inline-flex;
  align-items:center;
  justify-content:center;
  gap:8px;
  user-select:none;
  transition:transform .08s ease, border-color .12s ease, background .12s ease, box-shadow .12s ease, filter .12s ease;
}

button.primary{
  background:linear-gradient(135deg, rgba(77,163,255,1) 0%, rgba(124,92,255,1) 100%);
  border-color:rgba(255,255,255,.22);
  box-shadow:0 14px 46px rgba(77,163,255,.20), inset 0 1px 0 rgba(255,255,255,.16);
}

button.secondary{
  background:rgba(0,0,0,.22);
  border-color:rgba(255,255,255,.14);
}

button.danger{
  background:rgba(255,77,109,.18);
  border-color:rgba(255,77,109,.35);
  color:#ffd7df;
}

button:hover{filter:brightness(1.04)}
button:active{transform:translateY(1px)}
button:disabled{opacity:.55;cursor:not-allowed;transform:none;filter:none}

/* Simple helpers */
.row{
  display:flex;
  gap:10px;
  flex-wrap:wrap;
  align-items:center;
}

/* Scrollbar (WebKit) */
*::-webkit-scrollbar{height:10px;width:10px}
*::-webkit-scrollbar-thumb{
  background:rgba(255,255,255,.12);
  border-radius:999px;
  border:2px solid rgba(0,0,0,0);
  background-clip:padding-box;
}
*::-webkit-scrollbar-thumb:hover{background:rgba(255,255,255,.18)}
*::-webkit-scrollbar-track{background:rgba(0,0,0,.14)}

/* Reduced motion */
@media (prefers-reduced-motion: reduce){
  *{scroll-behavior:auto !important}
  button{transition:none}
  body.logos-ui{background-attachment:scroll}
}

```

### FILE: /opt/logos/www/wallet/app.css
```
/* Wallet App page tweaks (Lux v3) */

/* ключи/выводы выглядят как терминал */
#pub{
  min-height:120px;
  resize:vertical;
}

#pub,
#out-balance,
#out-send,
#out-stake,
#out-bridge{
  font-family:var(--mono);
  font-size:12.5px;
  line-height:1.45;
}

/* ограничим высоту логов, чтобы не раздувало страницу */
#out-balance,#out-send,#out-stake,#out-bridge{
  max-height:280px;
}

/* часто эти id встречаются — делаем RID-поля моно (не ломает, даже если каких-то id нет) */
#rid,#to,#loginRid{
  font-family:var(--mono);
  letter-spacing:.1px;
}

```

### FILE: /opt/logos/www/wallet/app.html
```
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta http-equiv="Cache-Control" content="no-store"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Wallet</title>
  <link rel="stylesheet" href="/shared/wallet-theme.css?v=20251212_04"/>
  <link rel="stylesheet" href="./app.css?v=20251212_04"/>
</head>
<body class="logos-ui">
  <header class="topbar">
    <div class="topbar__inner">
      <div class="brand">
        <div class="brand__mark"><span>LRB</span></div>
        <div>
          <div class="brand__title">LOGOS Wallet</div>
          <div class="brand__sub">Local keys · Signed in browser · API ready</div>
        </div>
      </div>
      <div class="topbar__right">
        <div class="pill">API: <span id="endpoint" class="mono">/api</span></div>
        <button id="btn-lock" class="secondary" type="button">Выйти (лок)</button>
      </div>
    </div>
  </header>

  <main class="container">
    <div class="stack">
      <section class="card">
        <header class="card__head">
          <h2>Ключи</h2>
          <p class="muted">RID = base58(pubkey). Приватный ключ зашифрован локально (AES‑GCM + PBKDF2).</p>
        </header>
        <textarea id="pub" class="mono" readonly spellcheck="false"></textarea>
        <pre id="out-status" class="mono">OK</pre>
      </section>

      <section class="card">
        <header class="card__head">
          <h2>Баланс</h2>
        </header>

        <label>RID</label>
        <input id="rid-balance" class="mono" placeholder="RID"/>

        <div class="row">
          <button id="btn-balance" class="primary" type="button">Показать баланс</button>
          <button id="btn-nonce" type="button">Обновить nonce</button>
        </div>

        <pre id="out-balance" class="mono"></pre>
      </section>

      <section class="card">
        <header class="card__head">
          <h2>Отправить транзакцию</h2>
        </header>

        <label>Кому (RID)</label>
        <input id="to" class="mono" placeholder="RID получателя"/>

        <label>Сумма (micro‑LGN)</label>
        <input id="amount" type="number" min="1" step="1" value="1"/>

        <label>Nonce (авто)</label>
        <input id="nonce" type="number" readonly/>

        <div class="row">
          <button id="btn-send" class="primary" type="button">Подписать и отправить</button>
        </div>

        <pre id="out-send" class="mono"></pre>
      </section>

      <section class="card">
        <header class="card__head">
          <h2>Стейкинг</h2>
        </header>

        <div class="row">
          <button id="btn-stake-refresh" type="button">Обновить статус</button>
          <button id="btn-stake-claim" class="secondary" type="button">Claim</button>
        </div>

        <label>Delegate (LGN)</label>
        <input id="stake-amount" type="number" min="1" step="1" value="0"/>
        <button id="btn-stake-delegate" class="primary" type="button">Делегировать</button>

        <label>Undelegate (LGN)</label>
        <input id="unstake-amount" type="number" min="1" step="1" value="0"/>
        <button id="btn-stake-undelegate" class="secondary" type="button">Снять делегацию</button>

        <pre id="out-stake" class="mono"></pre>
      </section>

      <section class="card">
        <header class="card__head">
          <h2>Bridge deposit (demo)</h2>
        </header>

        <label>RID</label>
        <input id="rid-bridge" class="mono" placeholder="RID"/>

        <label>Amount</label>
        <input id="amount-bridge" type="number" min="1" step="1" value="1"/>

        <label>ext_txid</label>
        <input id="ext" class="mono" placeholder="например eth_txid_0xabc"/>

        <div class="row">
          <button id="btn-deposit" type="button">Deposit</button>
        </div>

        <pre id="out-bridge" class="mono"></pre>
      </section>
    </div>
  </main>

  <script src="/shared/tweetnacl.min.js?v=20251212_04" defer></script>
  <script src="./app.js?v=20251212_04" defer></script>
  <script src="./connect.js?v=20251213_01" defer></script>
</body>
</html>

```

### FILE: /opt/logos/www/wallet/app.js
```
'use strict';

const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/api'));

const DB_NAME  = 'logos_wallet_v2';
const STORE    = 'keys';
const AUTOLOCK_MS = 15 * 60 * 1000;

const enc = new TextEncoder();

const ED25519_PKCS8_PREFIX = new Uint8Array([
  0x30, 0x2e, 0x02, 0x01, 0x00,
  0x30, 0x05, 0x06, 0x03, 0x2b, 0x65, 0x70,
  0x04, 0x22, 0x04, 0x20
]);

const $ = (s) => document.querySelector(s);

let RID  = sessionStorage.getItem('logos_rid') || '';
let PASS = sessionStorage.getItem('logos_pass') || '';

let META = null;
let SEED = null;           // Uint8Array(32)
let KP   = null;           // nacl keypair
let lastActivity = Date.now();

function bump() { lastActivity = Date.now(); }

function lockNow() {
  try {
    PASS = '';
    RID = '';
    META = null;
    SEED = null;
    KP = null;
    sessionStorage.removeItem('logos_pass');
    sessionStorage.removeItem('logos_rid');
  } catch (_) {}
  location.href = './auth.html';
}

function ensureEnv() {
  if (!window.isSecureContext) throw new Error('Нужен HTTPS (secure context)');
  if (!window.crypto || !window.crypto.subtle) throw new Error('WebCrypto недоступен');
  if (!window.indexedDB) throw new Error('IndexedDB недоступен');
  if (!window.nacl || !window.nacl.sign || !window.nacl.sign.keyPair || !window.nacl.sign.keyPair.fromSeed) {
    throw new Error('tweetnacl не загружен (нет window.nacl)');
  }
}

function toHex(u8) {
  const a = (u8 instanceof Uint8Array) ? u8 : new Uint8Array(u8 || []);
  let s = '';
  for (let i = 0; i < a.length; i++) s += a[i].toString(16).padStart(2, '0');
  return s;
}
function fromHex(hex) {
  const clean = (hex || '').trim();
  if (clean.length % 2 !== 0) throw new Error('нечётная длина hex');
  const out = new Uint8Array(clean.length / 2);
  for (let i = 0; i < out.length; i++) out[i] = parseInt(clean.slice(i*2, i*2+2), 16);
  return out;
}

function extractSeedFromPkcs8(pkcs8) {
  const u = (pkcs8 instanceof Uint8Array) ? pkcs8 : new Uint8Array(pkcs8 || []);
  if (u.length !== ED25519_PKCS8_PREFIX.length + 32) throw new Error('Неверная длина PKCS8');
  for (let i = 0; i < ED25519_PKCS8_PREFIX.length; i++) {
    if (u[i] !== ED25519_PKCS8_PREFIX[i]) throw new Error('PKCS8 prefix mismatch');
  }
  return u.slice(ED25519_PKCS8_PREFIX.length);
}

// IndexedDB
let DBP = null;
function openDb() {
  if (DBP) return DBP;
  DBP = new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, 1);
    req.onupgradeneeded = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains(STORE)) db.createObjectStore(STORE);
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
  return DBP;
}
async function idbGet(key) {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE, 'readonly');
    const st = tx.objectStore(STORE);
    const r = st.get(key);
    r.onsuccess = () => resolve(r.result || null);
    r.onerror = () => reject(r.error);
  });
}

async function deriveKey(pass, saltArr) {
  const salt = (saltArr instanceof Uint8Array) ? saltArr : new Uint8Array(saltArr || []);
  const keyMat = await crypto.subtle.importKey('raw', enc.encode(pass), 'PBKDF2', false, ['deriveKey']);
  return crypto.subtle.deriveKey(
    { name: 'PBKDF2', salt, iterations: 120000, hash: 'SHA-256' },
    keyMat,
    { name: 'AES-GCM', length: 256 },
    false,
    ['decrypt']
  );
}
async function aesDecrypt(aesKey, ivArr, ctArr) {
  const iv = (ivArr instanceof Uint8Array) ? ivArr : new Uint8Array(ivArr || []);
  const ct = (ctArr instanceof Uint8Array) ? ctArr : new Uint8Array(ctArr || []);
  const plain = await crypto.subtle.decrypt({ name: 'AES-GCM', iv }, aesKey, ct);
  return new Uint8Array(plain);
}

// HTTP
async function getJSON(url) {
  const r = await fetch(url, { method:'GET', cache:'no-store', credentials:'same-origin' });
  if (!r.ok) throw new Error(`${url} ${r.status}`);
  return r.json();
}
async function postJSON(url, body) {
  const r = await fetch(url, {
    method:'POST', cache:'no-store', credentials:'same-origin',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify(body ?? {})
  });
  if (!r.ok) throw new Error(`${url} ${r.status}`);
  return r.json();
}

async function getBalance(rid) {
  return getJSON(`${API}/balance/${encodeURIComponent(rid)}`);
}
async function getNonce(rid) {
  const j = await getBalance(rid);
  if (!j || typeof j.nonce !== 'number') throw new Error('не удалось получить nonce');
  return j.nonce;
}

// msg = from | '|' | to | '|' | amount(8 BE) | '|' | nonce(8 BE)
function canonBytes(from, to, amount, nonce) {
  const fromB = enc.encode(from);
  const toB   = enc.encode(to);

  const ab = new ArrayBuffer(8);
  const av = new DataView(ab);
  av.setBigUint64(0, BigInt(amount), false);

  const nb = new ArrayBuffer(8);
  const nv = new DataView(nb);
  nv.setBigUint64(0, BigInt(nonce), false);

  const sep = new Uint8Array([ '|'.charCodeAt(0) ]);

  const parts = [fromB, sep, toB, sep, new Uint8Array(ab), sep, new Uint8Array(nb)];
  const total = parts.reduce((s,a)=>s+a.length,0);
  const out = new Uint8Array(total);
  let off=0;
  for (const p of parts) { out.set(p, off); off += p.length; }
  return out;
}

async function sha256(u8) {
  const d = await crypto.subtle.digest('SHA-256', u8);
  return new Uint8Array(d);
}

async function signHash32(hash32) {
  if (!KP) throw new Error('ключ не загружен');
  const sig = nacl.sign.detached(hash32, KP.secretKey);
  return toHex(new Uint8Array(sig));
}

async function refreshBalanceUI() {
  const out = $('#out-balance');
  try {
    const rid = ($('#rid-balance')?.value || RID || '').trim();
    const j = await getBalance(rid);
    if (out) out.textContent = JSON.stringify(j, null, 2);
    const nonce = (typeof j.nonce === 'number') ? (j.nonce + 1) : '';
    const nonceInp = $('#nonce');
    if (nonceInp) nonceInp.value = String(nonce);
  } catch (e) {
    if (out) out.textContent = 'ERR: ' + (e && e.message ? e.message : e);
  }
}

async function refreshStakeUI() {
  const out = $('#out-stake');
  try {
    const j = await getJSON(`${API}/stake/my/${encodeURIComponent(RID)}`);
    if (out) out.textContent = JSON.stringify(j, null, 2);
  } catch (e) {
    if (out) out.textContent = 'ERR: ' + (e && e.message ? e.message : e);
  }
}

async function submitBatch(txs) {
  return postJSON(`${API}/submit_tx_batch`, { txs });
}

(async () => {
  try {
    ensureEnv();

    if (!RID || !PASS) { lockNow(); return; }

    const ep = $('#endpoint');
    if (ep) ep.textContent = API;

    META = await idbGet('acct:' + RID);
    if (!META) { lockNow(); return; }

    const aes = await deriveKey(PASS, META.salt || []);
    const pkcs8 = await aesDecrypt(aes, META.iv || [], META.priv || []);
    SEED = extractSeedFromPkcs8(pkcs8);

    KP = nacl.sign.keyPair.fromSeed(SEED);

    const pubHex = toHex(new Uint8Array(KP.publicKey));
    const pubArea = $('#pub');
    if (pubArea) pubArea.value = `RID (base58): ${RID}\nPUB (hex): ${pubHex}`;

    const rb = $('#rid-balance');
    if (rb) rb.value = RID;

    const rbridge = $('#rid-bridge');
    if (rbridge) rbridge.value = RID;

    bump();
    await refreshBalanceUI();
    await refreshStakeUI();

  } catch (e) {
    console.error('wallet boot error:', e);
    const st = $('#out-status');
    if (st) st.textContent = 'ERR: ' + (e && e.message ? e.message : e);
    lockNow();
  }
})();

// глобальная активность (чтобы автолок не срабатывал “во время работы”)
['click','keydown','mousemove','touchstart'].forEach(ev=>{
  window.addEventListener(ev, ()=>bump(), { passive:true });
});

$('#btn-lock')?.addEventListener('click', () => lockNow());

$('#btn-balance')?.addEventListener('click', async () => {
  bump();
  await refreshBalanceUI();
});

$('#btn-nonce')?.addEventListener('click', async () => {
  bump();
  await refreshBalanceUI();
});

$('#btn-send')?.addEventListener('click', async () => {
  const out = $('#out-send');
  try {
    bump();
    const to = ($('#to')?.value || '').trim();
    const amount = Number(($('#amount')?.value || '').trim());
    if (!to) throw new Error('введи RID получателя');
    if (!Number.isFinite(amount) || amount <= 0) throw new Error('сумма должна быть > 0');

    const currentNonce = await getNonce(RID);
    const nonce = currentNonce + 1;
    if ($('#nonce')) $('#nonce').value = String(nonce);

    const msg = canonBytes(RID, to, amount, nonce);
    const h32 = await sha256(msg);
    const sig_hex = await signHash32(h32);

    const res = await submitBatch([{
      from: RID,
      to,
      amount,
      nonce,
      sig_hex
    }]);

    if (out) out.textContent = JSON.stringify(res, null, 2);
    await refreshBalanceUI();
  } catch (e) {
    console.error(e);
    if (out) out.textContent = 'ERR: ' + (e && e.message ? e.message : e);
  }
});

// staking
$('#btn-stake-refresh')?.addEventListener('click', async () => { bump(); await refreshStakeUI(); });
$('#btn-stake-delegate')?.addEventListener('click', async () => {
  const out = $('#out-stake');
  try {
    bump();
    const val = Number(($('#stake-amount')?.value || '0'));
    if (!Number.isFinite(val) || val <= 0) throw new Error('сумма должна быть > 0');
    const res = await postJSON(`${API}/stake/delegate`, { rid: RID, amount: val });
    if (out) out.textContent = JSON.stringify(res, null, 2);
    await refreshStakeUI();
    await refreshBalanceUI();
  } catch (e) {
    if (out) out.textContent = 'ERR: ' + (e && e.message ? e.message : e);
  }
});
$('#btn-stake-undelegate')?.addEventListener('click', async () => {
  const out = $('#out-stake');
  try {
    bump();
    const val = Number(($('#unstake-amount')?.value || '0'));
    if (!Number.isFinite(val) || val <= 0) throw new Error('сумма должна быть > 0');
    const res = await postJSON(`${API}/stake/undelegate`, { rid: RID, amount: val });
    if (out) out.textContent = JSON.stringify(res, null, 2);
    await refreshStakeUI();
    await refreshBalanceUI();
  } catch (e) {
    if (out) out.textContent = 'ERR: ' + (e && e.message ? e.message : e);
  }
});
$('#btn-stake-claim')?.addEventListener('click', async () => {
  const out = $('#out-stake');
  try {
    bump();
    const res = await postJSON(`${API}/stake/claim`, { rid: RID });
    if (out) out.textContent = JSON.stringify(res, null, 2);
    await refreshStakeUI();
    await refreshBalanceUI();
  } catch (e) {
    if (out) out.textContent = 'ERR: ' + (e && e.message ? e.message : e);
  }
});

// bridge
$('#btn-deposit')?.addEventListener('click', async () => {
  const out = $('#out-bridge');
  try {
    bump();
    const rid = ( ($('#rid-bridge')?.value || RID || '').trim() );
    const amount = Number(($('#amount-bridge')?.value || '0'));
    const ext = String($('#ext')?.value || '');
    if (!rid) throw new Error('RID пустой');
    if (!Number.isFinite(amount) || amount <= 0) throw new Error('сумма должна быть > 0');
    const res = await postJSON(`${API}/bridge/deposit`, { rid, amount, ext_txid: ext });
    if (out) out.textContent = JSON.stringify(res, null, 2);
  } catch (e) {
    if (out) out.textContent = 'ERR: ' + (e && e.message ? e.message : e);
  }
});

// autolock
setInterval(() => {
  const now = Date.now();
  if (now - lastActivity > AUTOLOCK_MS) lockNow();
}, 30_000);

```

### FILE: /opt/logos/www/wallet/auth.css
```
/* Wallet Auth page tweaks (theme in /shared/wallet-theme.css) */

/* ВАЖНО: hidden управляет видимостью, CSS его не должен ломать */
[hidden]{ display:none !important; }

/* НЕ ставим display:none на эти блоки! */
#listWrap{ margin-top:12px; }
#mnemonicSection{ margin-top:14px; }

#mnemonicShow,#mnemonicConfirm,#restoreMnemonic{ min-height:120px; }

#ridList{
  list-style:none;
  padding:0;
  margin:10px 0 0;
  display:grid;
  gap:8px;
}

#ridList li{
  padding:10px 12px;
  border-radius:14px;
  border:1px solid rgba(255,255,255,.10);
  background:rgba(0,0,0,.22);
  cursor:pointer;
  font-family:var(--mono);
  font-size:12.5px;
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
}

#ridList li:hover{
  border-color:rgba(77,163,255,.35);
  background:rgba(0,0,0,.28);
}

#out{ min-height:84px; }

```

### FILE: /opt/logos/www/wallet/auth.html
```
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta http-equiv="Cache-Control" content="no-store"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Wallet — Secure</title>
  <link rel="stylesheet" href="/shared/wallet-theme.css?v=20251212_04"/>
  <link rel="stylesheet" href="./auth.css?v=20251212_04"/>
</head>
<body class="logos-ui">
  <header class="topbar">
    <div class="topbar__inner">
      <div class="brand">
        <div class="brand__mark"><span>LRB</span></div>
        <div>
          <div class="brand__title">LOGOS Wallet</div>
          <div class="brand__sub">Local keys · AES‑GCM + PBKDF2 · Ed25519 via tweetnacl</div>
        </div>
      </div>
      <div class="topbar__right">
        <div class="pill">HTTPS only</div>
      </div>
    </div>
  </header>

  <main class="container">
    <section class="card hero">
      <h1>Доступ к кошельку</h1>
      <p class="muted">Ключи живут локально в браузере. Сервер получает только подписанные операции.</p>
    </section>

    <div class="grid-2">
      <section class="card">
        <header class="card__head">
          <h2>Вход</h2>
          <p class="muted">Если RID уже есть на этом устройстве — вход по паролю.</p>
        </header>

        <label for="loginRid">RID</label>
        <input id="loginRid" class="mono" placeholder="RID (base58) или выбери ниже" autocomplete="off"/>

        <label for="loginPass">Пароль</label>
        <input id="loginPass" type="password" placeholder="Пароль, которым шифровали ключ" autocomplete="current-password"/>

        <div class="row">
          <button id="btn-login" class="primary" type="button">Войти по RID + пароль</button>
          <button id="btn-list" type="button">Показать сохранённые RID</button>
        </div>

        <div id="listWrap" hidden>
          <div class="muted">Локально сохранённые RID (кликни, чтобы подставить):</div>
          <ul id="ridList"></ul>
        </div>
      </section>

      <section class="card">
        <header class="card__head">
          <h2>Создать новый</h2>
          <p class="muted">Ключ генерируется в браузере. Запиши 16 слов — это единственный способ восстановления.</p>
        </header>

        <label for="createPass">Новый пароль</label>
        <input id="createPass" type="password" placeholder="Минимум 10 символов, буквы + цифры" autocomplete="new-password"/>

        <div class="row">
          <button id="btn-create" class="primary" type="button">Создать новый RID + фразу</button>
        </div>

        <div id="mnemonicSection" hidden>
          <h3>Резервная фраза (16 слов)</h3>

          <label for="mnemonicShow">Фраза (только чтение)</label>
          <textarea id="mnemonicShow" class="mono" readonly spellcheck="false"></textarea>

          <label for="mnemonicConfirm">Повтори фразу для проверки ещё раз</label>
          <textarea id="mnemonicConfirm" class="mono" placeholder="введите те же 16 слов через пробел" spellcheck="false"></textarea>

          <div class="row">
            <button id="btn-mnemonic-ok" class="primary" type="button">Я записал фразу, перейти в кошелёк</button>
          </div>
        </div>
      </section>
    </div>

    <section class="card">
      <header class="card__head">
        <h2>Восстановить по фразе</h2>
        <p class="muted">Вводишь 16 слов и задаёшь новый пароль. RID восстановится автоматически.</p>
      </header>

      <label for="restoreMnemonic">Резервная фраза (16 слов)</label>
      <textarea id="restoreMnemonic" class="mono" placeholder="16 слов через пробел" spellcheck="false"></textarea>

      <label for="restorePass">Новый пароль</label>
      <input id="restorePass" type="password" placeholder="Минимум 10 символов, буквы + цифры" autocomplete="new-password"/>

      <div class="row">
        <button id="btn-restore" class="primary" type="button">Восстановить кошелёк</button>
      </div>
    </section>

    <section class="card">
      <header class="card__head">
        <h2>Сервис</h2>
        <p class="muted">Сброс локальных аккаунтов доступен только на localhost (dev).</p>
      </header>
      <div class="row">
        <button id="btn-reset" class="danger" type="button" hidden>Сбросить локальные аккаунты (DEV)</button>
      </div>
      <pre id="out" class="mono">Статус: жду действий…</pre>
    </section>
  </main>

  <script src="/shared/tweetnacl.min.js?v=20251212_04" defer></script>
<script src="/wallet/connect.js?v=directbind_01" defer></script>
  <script src="./auth.js?v=20251212_04" defer></script>
</body>
</html>

```

### FILE: /opt/logos/www/wallet/auth.js
```
/* connect hook: remember challenge if opened from airdrop */
(() => {
  try {
    const q = new URLSearchParams(location.search);
    if (q.get("connect") === "1") {
      const ch = (q.get("challenge") || "").trim();
      if (ch) sessionStorage.setItem("logos_connect_challenge", ch);
      sessionStorage.setItem("logos_connect_mode", "1");
    }
  } catch (e) {}
})();
'use strict';

// AUTH (mainnet-grade):
// - AES-GCM + PBKDF2 (WebCrypto)
// - Ed25519 via tweetnacl (НЕ зависит от WebCrypto Ed25519)
// - хранение: IndexedDB, зашифрованный PKCS8 (RFC8410 prefix + seed32)
// - CSP-safe: без inline handlers и без element.style

const DB_NAME = 'logos_wallet_v2';
const STORE   = 'keys';
const enc     = new TextEncoder();
const ALPH    = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';

const MN_WORDS = 16;
const MN_ALPH  = 'abcdefghjkmnpqrstuvwxyz';

const ED25519_PKCS8_PREFIX = new Uint8Array([
  0x30, 0x2e, 0x02, 0x01, 0x00,
  0x30, 0x05, 0x06, 0x03, 0x2b, 0x65, 0x70,
  0x04, 0x22, 0x04, 0x20
]);

const $ = (s) => document.querySelector(s);
const out = (msg) => { const el = $('#out'); if (el) el.textContent = String(msg); };

function ensureEnv() {
  if (!window.isSecureContext) throw new Error('Нужен HTTPS (secure context)');
  if (!window.indexedDB) throw new Error('IndexedDB недоступен');
  if (!window.crypto || !window.crypto.subtle) throw new Error('WebCrypto недоступен');
  if (!window.nacl || !window.nacl.sign || !window.nacl.sign.keyPair || !window.nacl.sign.keyPair.fromSeed) {
    throw new Error('tweetnacl не загружен (нет window.nacl)');
  }
}

function normRid(s) { return (s || '').replace(/\s+/g, '').trim(); }
function normalizeMnemonic(s) { return (s || '').trim().toLowerCase().replace(/\s+/g, ' '); }

function b58encode(bytes) {
  const src = (bytes instanceof Uint8Array) ? bytes : new Uint8Array(bytes || []);
  if (src.length === 0) return '';
  const digits = [0];
  for (let i = 0; i < src.length; i++) {
    let carry = src[i];
    for (let j = 0; j < digits.length; j++) {
      carry += digits[j] << 8;
      digits[j] = carry % 58;
      carry = (carry / 58) | 0;
    }
    while (carry) {
      digits.push(carry % 58);
      carry = (carry / 58) | 0;
    }
  }
  let out = '';
  for (let k = 0; k < src.length && src[k] === 0; k++) out += ALPH[0];
  for (let q = digits.length - 1; q >= 0; q--) out += ALPH[digits[q]];
  return out;
}

function validateNewPassword(pass) {
  if (!pass || pass.length < 10) throw new Error('Пароль ≥10 символов');
  if (!/[A-Za-z]/.test(pass) || !/[0-9]/.test(pass)) throw new Error('Пароль должен содержать буквы и цифры');
  return pass;
}
function ensureLoginPassword(pass) {
  if (!pass || pass.length < 6) throw new Error('Пароль ≥6 символов');
  return pass;
}

async function sha256Bytes(str) {
  const digest = await crypto.subtle.digest('SHA-256', enc.encode(str));
  return new Uint8Array(digest);
}

function randomWord(len = 5) {
  const buf = new Uint8Array(len);
  crypto.getRandomValues(buf);
  let w = '';
  for (let i = 0; i < len; i++) w += MN_ALPH[buf[i] % MN_ALPH.length];
  return w;
}
function generateMnemonic() {
  const words = [];
  for (let i = 0; i < MN_WORDS; i++) words.push(randomWord());
  return words.join(' ');
}

async function mnemonicToSeed(mnemonic) {
  const norm = normalizeMnemonic(mnemonic);
  if (!norm) throw new Error('Резервная фраза пуста');
  return sha256Bytes('logos-lrb-ed25519:' + norm); // 32 bytes
}

function buildPkcs8FromSeed(seed32) {
  if (!(seed32 instanceof Uint8Array) || seed32.length !== 32) throw new Error('seed должен быть 32 байта');
  const out = new Uint8Array(ED25519_PKCS8_PREFIX.length + 32);
  out.set(ED25519_PKCS8_PREFIX, 0);
  out.set(seed32, ED25519_PKCS8_PREFIX.length);
  return out;
}

function extractSeedFromPkcs8(pkcs8) {
  const u = (pkcs8 instanceof Uint8Array) ? pkcs8 : new Uint8Array(pkcs8 || []);
  if (u.length !== ED25519_PKCS8_PREFIX.length + 32) throw new Error('Неверная длина PKCS8');
  for (let i = 0; i < ED25519_PKCS8_PREFIX.length; i++) {
    if (u[i] !== ED25519_PKCS8_PREFIX[i]) throw new Error('PKCS8 prefix mismatch');
  }
  return u.slice(ED25519_PKCS8_PREFIX.length);
}

async function deriveKey(pass, saltU8) {
  const keyMat = await crypto.subtle.importKey('raw', enc.encode(pass), 'PBKDF2', false, ['deriveKey']);
  return crypto.subtle.deriveKey(
    { name: 'PBKDF2', salt: saltU8, iterations: 120000, hash: 'SHA-256' },
    keyMat,
    { name: 'AES-GCM', length: 256 },
    false,
    ['encrypt', 'decrypt']
  );
}

async function aesEncrypt(aesKey, plainU8) {
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const ct = new Uint8Array(await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, aesKey, plainU8));
  return { iv, ct };
}

async function aesDecrypt(aesKey, ivU8, ctU8) {
  const plain = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: ivU8 }, aesKey, ctU8);
  return new Uint8Array(plain);
}

// ---------- IndexedDB ----------
let DBP = null;
function openDb() {
  if (DBP) return DBP;
  DBP = new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, 1);
    req.onupgradeneeded = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains(STORE)) db.createObjectStore(STORE);
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
  return DBP;
}

async function idbGet(key) {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE, 'readonly');
    const st = tx.objectStore(STORE);
    const r = st.get(key);
    r.onsuccess = () => resolve(r.result || null);
    r.onerror = () => reject(r.error);
  });
}
async function idbSet(key, val) {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE, 'readwrite');
    const st = tx.objectStore(STORE);
    const r = st.put(val, key);
    r.onsuccess = () => resolve();
    r.onerror = () => reject(r.error);
  });
}
async function idbDel(key) {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE, 'readwrite');
    const st = tx.objectStore(STORE);
    const r = st.delete(key);
    r.onsuccess = () => resolve();
    r.onerror = () => reject(r.error);
  });
}

async function listAccounts() { return (await idbGet('accounts')) || []; }
async function addAccount(rid) {
  const list = (await idbGet('accounts')) || [];
  if (!list.includes(rid)) {
    list.push(rid);
    await idbSet('accounts', list);
  }
}

// Pending state
let pendingRid = null;
let pendingMnemonic = null;

async function createAccount(passRaw) {
  ensureEnv();
  const pass = validateNewPassword(passRaw);

  out('Создаём ключ и фразу…');

  const mnemonic = generateMnemonic();
  const seed = await mnemonicToSeed(mnemonic);
  const pkcs8 = buildPkcs8FromSeed(seed);

  const kp = nacl.sign.keyPair.fromSeed(seed);
  const pub = new Uint8Array(kp.publicKey);
  const rid = b58encode(pub);

  const salt = crypto.getRandomValues(new Uint8Array(16));
  const aes = await deriveKey(pass, salt);
  const { iv, ct } = await aesEncrypt(aes, pkcs8);

  const meta = {
    rid,
    pub: Array.from(pub),
    salt: Array.from(salt),
    iv: Array.from(iv),
    priv: Array.from(ct),
  };

  await idbSet('acct:' + rid, meta);
  await addAccount(rid);
  await idbSet('last_rid', rid);

  sessionStorage.setItem('logos_pass', pass);
  sessionStorage.setItem('logos_rid', rid);

  pendingRid = rid;
  pendingMnemonic = mnemonic;

  const sec = $('#mnemonicSection');
  const disp = $('#mnemonicShow');
  const confirm = $('#mnemonicConfirm');
  if (sec && disp && confirm) {
    disp.value = mnemonic;
    confirm.value = '';
    sec.hidden = false;
    sec.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  out('RID создан: ' + rid + '. Запиши фразу и подтверди её.');
}

async function loginAccount(ridRaw, passRaw) {
  ensureEnv();
  const rid = normRid(ridRaw);
  const pass = ensureLoginPassword(passRaw);
  if (!rid) throw new Error('Укажи RID');

  const meta = await idbGet('acct:' + rid);
  if (!meta) {
    const list = await listAccounts();
    throw new Error('RID не найден на этом устройстве.\n' + (list.length ? list.join('\n') : '— пусто —'));
  }

  const aes = await deriveKey(pass, new Uint8Array(meta.salt || []));
  try {
    const pkcs8 = await aesDecrypt(aes, new Uint8Array(meta.iv || []), new Uint8Array(meta.priv || []));
    // проверим, что это действительно наш PKCS8 (совместимость/коррупция)
    extractSeedFromPkcs8(pkcs8);
  } catch (_) {
    throw new Error('Неверный пароль или повреждённый ключ');
  }

  sessionStorage.setItem('logos_pass', pass);
  sessionStorage.setItem('logos_rid', rid);
  await idbSet('last_rid', rid);

  out('Вход…');
  location.href = './app.html';
}

async function restoreAccount(mnemonicRaw, passRaw) {
  ensureEnv();
  const pass = validateNewPassword(passRaw);
  const mnemonic = normalizeMnemonic(mnemonicRaw);
  if (!mnemonic) throw new Error('Введи резервную фразу');

  out('Восстанавливаем кошелёк…');

  const seed = await mnemonicToSeed(mnemonic);
  const pkcs8 = buildPkcs8FromSeed(seed);

  const kp = nacl.sign.keyPair.fromSeed(seed);
  const pub = new Uint8Array(kp.publicKey);
  const rid = b58encode(pub);

  const salt = crypto.getRandomValues(new Uint8Array(16));
  const aes = await deriveKey(pass, salt);
  const { iv, ct } = await aesEncrypt(aes, pkcs8);

  const meta = {
    rid,
    pub: Array.from(pub),
    salt: Array.from(salt),
    iv: Array.from(iv),
    priv: Array.from(ct),
  };

  await idbSet('acct:' + rid, meta);
  await addAccount(rid);
  await idbSet('last_rid', rid);

  sessionStorage.setItem('logos_pass', pass);
  sessionStorage.setItem('logos_rid', rid);

  out('Кошелёк восстановлен: ' + rid + ' → вход…');
  location.href = './app.html';
}

async function resetAll() {
  const ok = confirm('Точно стереть все локальные аккаунты? Это нельзя отменить.');
  if (!ok) return;
  const list = await listAccounts();
  for (const rid of list) await idbDel('acct:' + rid);
  await idbDel('accounts');
  await idbDel('last_rid');
  sessionStorage.clear();
  pendingRid = null;
  pendingMnemonic = null;
  out('Все аккаунты удалены.');
}

function renderRidList(list) {
  const wrap = $('#listWrap');
  const ul = $('#ridList');
  if (!wrap || !ul) return;
  ul.innerHTML = '';
  wrap.hidden = false;

  if (!list.length) {
    const li = document.createElement('li');
    li.textContent = '— пусто —';
    ul.appendChild(li);
    return;
  }

  for (const rid of list) {
    const li = document.createElement('li');
    li.textContent = rid;
    li.addEventListener('click', () => {
      const inp = $('#loginRid');
      if (inp) inp.value = rid;
      out('RID подставлен');
    });
    ul.appendChild(li);
  }
}

// boot helpers
(async () => {
  try {
    // last_rid
    const last = await idbGet('last_rid');
    const loginRid = $('#loginRid');
    if (last && loginRid) loginRid.value = last;

    // DEV reset only on localhost
    const resetBtn = $('#btn-reset');
    if (resetBtn) {
      const isDevHost = (location.hostname === 'localhost' || location.hostname === '127.0.0.1');
      resetBtn.hidden = !isDevHost;
    }
  } catch (e) {
    console.error(e);
  }
})();

// UI wiring
$('#btn-login')?.addEventListener('click', async () => {
  try {
    await loginAccount($('#loginRid')?.value || '', $('#loginPass')?.value || '');
  } catch (e) {
    out('ERR: ' + (e && e.message ? e.message : e));
  }
});

$('#btn-create')?.addEventListener('click', async () => {
  try {
    await createAccount($('#createPass')?.value || '');
  } catch (e) {
    out('ERR: ' + (e && e.message ? e.message : e));
  }
});

$('#btn-list')?.addEventListener('click', async () => {
  try {
    renderRidList(await listAccounts());
  } catch (e) {
    out('ERR: ' + (e && e.message ? e.message : e));
  }
});

$('#btn-reset')?.addEventListener('click', async () => {
  const isDevHost = (location.hostname === 'localhost' || location.hostname === '127.0.0.1');
  if (!isDevHost) {
    out('ERR: reset доступен только на localhost (dev)');
    return;
  }
  try {
    await resetAll();
  } catch (e) {
    out('ERR: ' + (e && e.message ? e.message : e));
  }
});

$('#btn-mnemonic-ok')?.addEventListener('click', () => {
  if (!pendingRid || !pendingMnemonic) {
    out('Нет созданного кошелька для подтверждения');
    return;
  }
  const typed = normalizeMnemonic($('#mnemonicConfirm')?.value || '');
  if (!typed) { out('Повтори фразу для подтверждения'); return; }
  if (typed !== normalizeMnemonic(pendingMnemonic)) { out('Фразы не совпадают'); return; }
  out('Фраза подтверждена, вход…');
  location.href = './app.html';
});

$('#btn-restore')?.addEventListener('click', async () => {
  try {
    await restoreAccount($('#restoreMnemonic')?.value || '', $('#restorePass')?.value || '');
  } catch (e) {
    out('ERR: ' + (e && e.message ? e.message : e));
  }
});

```

### FILE: /opt/logos/www/wallet/compat.js
```
"use strict";

(function () {
  // Базовый URL API
  const API = location.origin + "/api";

  const $ = (s) => document.querySelector(s);

  async function jsonGet(path) {
    const r = await fetch(API + path, { method: "GET" });
    const txt = await r.text().catch(() => "");
    if (!r.ok) {
      throw new Error(`${path} ${r.status} ${txt}`);
    }
    try {
      return JSON.parse(txt);
    } catch {
      throw new Error(`${path} bad json: ${txt}`);
    }
  }

  // Правильный формат тела для /debug_canon
  async function debugCanon(from, to, amount, nonce) {
    const body = {
      from,
      to,
      amount: Number(amount),
      nonce: Number(nonce),
      // на бэкенде старые и новые типы — шлём оба поля на всякий случай
      sig: "",
      sig_hex: ""
    };

    const r = await fetch(API + "/debug_canon", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });

    const txt = await r.text().catch(() => "");
    if (!r.ok) {
      throw new Error(`/debug_canon ${r.status} ${txt}`);
    }
    let j;
    try {
      j = JSON.parse(txt);
    } catch {
      throw new Error(`/debug_canon bad json: ${txt}`);
    }
    if (!j.canon_hex) {
      throw new Error("debug_canon: no canon_hex in response");
    }
    return j.canon_hex;
  }

  // Подпись канонического hex; если есть старый signCanon — используем его
  async function signCanonCompat(canonHex) {
    // KEYS и signCanon объявлены в старом app.js (глобальные переменные)
    if (typeof signCanon === "function") {
      return await signCanon(KEYS.privateKey, canonHex);
    }

    if (!KEYS || !KEYS.privateKey) {
      throw new Error("кошелёк заблокирован (нет ключа)");
    }

    const bytes = new Uint8Array(
      canonHex.match(/.{1,2}/g).map((x) => parseInt(x, 16))
    );
    const sig = await crypto.subtle.sign("Ed25519", KEYS.privateKey, bytes);
    return Array.from(new Uint8Array(sig))
      .map((b) => b.toString(16).padStart(2, "0"))
      .join("");
  }

  // Отправка batch'а (одна транза внутри массива)
  async function submitTx(tx) {
    const payload = { txs: [tx] };

    const r = await fetch(API + "/submit_tx_batch", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const txt = await r.text().catch(() => "");
    if (!r.ok) {
      throw new Error(`/submit_tx_batch ${r.status} ${txt}`);
    }

    try {
      return JSON.parse(txt);
    } catch {
      return txt;
    }
  }

  // Получаем текущий nonce по RID
  async function autoNonce(rid) {
    const data = await jsonGet("/balance/" + encodeURIComponent(rid));
    return Number(data.nonce || 0);
  }

  window.addEventListener("DOMContentLoaded", () => {
    const btn = $("#btn-send");
    if (!btn) return; // не на той странице

    // выпиливаем старые обработчики: клонируем кнопку
    const newBtn = btn.cloneNode(true);
    btn.parentNode.replaceChild(newBtn, btn);

    const nonceInput = $("#nonce");
    if (nonceInput) {
      nonceInput.readOnly = true;
      nonceInput.placeholder = "авто по сети";
    }
    const nonceBtn = $("#btn-nonce");
    if (nonceBtn) {
      nonceBtn.style.display = "none"; // прячем кнопку nonce
    }

    const out = $("#out-send");
    const show = (v) => {
      if (!out) return;
      out.textContent =
        typeof v === "string" ? v : JSON.stringify(v, null, 2);
    };

    newBtn.addEventListener("click", async () => {
      try {
        // RID и KEYS приходят из старого app.js
        if (typeof RID === "undefined" || !RID) {
          throw new Error("RID не найден (перезайди в кошелёк)");
        }
        if (typeof KEYS === "undefined" || !KEYS || !KEYS.privateKey) {
          throw new Error("кошелёк заблокирован (нет ключа)");
        }

        const toEl = $("#to");
        const amtEl = $("#amount");
        if (!toEl || !amtEl) throw new Error("не найдены поля формы");

        const to = toEl.value.trim();
        const amount = Number(amtEl.value);

        if (!to) throw new Error("укажи RID получателя");
        if (!Number.isFinite(amount) || amount <= 0) {
          throw new Error("сумма должна быть > 0");
        }

        // 1) узнаём nonce из /balance
        const currentNonce = await autoNonce(RID);
        const nonce = currentNonce + 1;
        if (nonceInput) nonceInput.value = String(nonce);

        // 2) получаем канонический hex от /debug_canon
        const canon = await debugCanon(RID, to, amount, nonce);

        // 3) подписываем
        const sigHex = await signCanonCompat(canon);

        // 4) собираем транзакцию под новый ApiSubmitTx
        const tx = {
          from: RID,
          to,
          amount: Number(amount),
          nonce,
          sig: sigHex,
          sig_hex: sigHex
        };

        const resp = await submitTx(tx);
        show(resp);
      } catch (e) {
        console.error(e);
        show(String(e));
      }
    });
  });
})();

```

### FILE: /opt/logos/www/wallet/connect.js
```
/* LOGOS Wallet Connect helper (DIRECT BIND, no postMessage)
   Flow:
   - airdrop stores localStorage["logos_airdrop_token"]
   - wallet in connect=1 mode:
       1) waits for login (RID+KP.secretKey)
       2) calls POST /api/airdrop/wallet_challenge {token, wallet_rid}
       3) signs challenge (Ed25519)
       4) calls POST /api/airdrop/wallet_bind {token, wallet_rid, sig_b64}
       5) shows OK and closes
*/

(function(){
  function qs(sel){ return document.querySelector(sel); }

  function isConnectMode(){
    try{
      const q = new URLSearchParams(location.search);
      return (q.get("connect") || "") === "1";
    }catch(e){}
    return false;
  }

  function b64url(bytes){
    let bin = "";
    for (let i=0;i<bytes.length;i++) bin += String.fromCharCode(bytes[i]);
    return btoa(bin).replace(/\+/g,"-").replace(/\//g,"_").replace(/=+$/,"");
  }

  function keysReady(){
    return (typeof KP !== "undefined" && KP && KP.secretKey) && (typeof RID !== "undefined" && RID);
  }

  function getTok(){
    try{ return (localStorage.getItem("logos_airdrop_token") || "").trim(); }catch(e){ return ""; }
  }

  async function jpost(url, body){
    const r = await fetch(url, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify(body || {})
    });
    const t = await r.text();
    let j = {};
    try{ j = t ? JSON.parse(t) : {}; }catch(e){ j = {raw:t}; }
    if (!r.ok){
      const msg = (j && (j.detail || j.error || j.message)) ? JSON.stringify(j) : t;
      throw new Error(`API ${r.status}: ${msg}`);
    }
    return j;
  }

  function mountPanel(){
    const host = qs(".stack") || qs("main.container") || document.body;
    if (qs("#connectAutoPanel")) return;
    const panel = document.createElement("section");
    panel.className = "card";
    panel.id = "connectAutoPanel";
    panel.innerHTML = `
      <header class="card__head">
        <h2>Подключение к Airdrop</h2>
        <p class="muted">После входа привязка произойдёт автоматически.</p>
      </header>
      <div class="card__body">
        <pre id="connectOut" class="mono" style="min-height:60px"></pre>
      </div>
    `;
    host.prepend(panel);
  }

  function setOut(msg){
    mountPanel();
    const o = qs("#connectOut");
    if (o) o.textContent = String(msg || "");
  }

  async function runBind(){
    if (typeof nacl === "undefined" || !nacl.sign || !nacl.sign.detached){
      throw new Error("tweetnacl not loaded");
    }
    const tok = getTok();
    if (!tok) throw new Error("no airdrop token (open Connect from airdrop page)");

    const rid = RID;
    setOut("Запрашиваю challenge...");
    const ch = await jpost("/api/airdrop/wallet_challenge", { token: tok, wallet_rid: rid });

    const challenge = String(ch.challenge || "");
    if (!challenge) throw new Error("no challenge in response");

    setOut("Подписываю...");
    const msg = new TextEncoder().encode(challenge);
    const sig = nacl.sign.detached(msg, KP.secretKey);
    const sig64 = b64url(sig);

    setOut("Привязываю кошелёк...");
    await jpost("/api/airdrop/wallet_bind", { token: tok, wallet_rid: rid, sig_b64: sig64 });

    setOut("✅ Привязано. Можно закрывать окно.");
    try{ localStorage.removeItem("logos_airdrop_token"); }catch(e){}
    try{ setTimeout(()=>window.close(), 700); }catch(e){}
  }

  if(!isConnectMode()){
  try{ if(!(localStorage.getItem("logos_airdrop_token")||"").trim()) return; }catch(e){ return; }
}


  setOut("Войди в кошелёк ниже (RID+пароль). После входа привязка произойдёт автоматически.");

  let tries = 0;
  const t = setInterval(async () => {
    tries++;
    if (keysReady()){
      clearInterval(t);
      try{
        await runBind();
      }catch(e){
        setOut("❌ Ошибка привязки: " + (e && e.message ? e.message : String(e)));
      }
    }
    if (tries > 400) clearInterval(t); // 40s
  }, 100);
})();

```

### FILE: /opt/logos/www/wallet/index.html
```
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <title>LOGOS Wallet — Кошелёк</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <meta name="color-scheme" content="dark"/>
  <link rel="stylesheet" href="./wallet.css?v=30"/>
</head>
<body>
  <!-- Верхняя панель -->
  <header class="topbar">
    <div class="topbar-left">
      <div class="logo-dot"></div>
      <div class="topbar-title">
        <span class="brand">LOGOS</span>
        <span class="product">Wallet</span>
      </div>
    </div>
    <div class="topbar-right">
      <span class="endpoint-label">Endpoint</span>
      <span class="endpoint-value" id="endpoint"></span>
      <button id="btn-lock" class="chip chip-ghost">Выйти</button>
    </div>
  </header>

  <main class="page-shell">
    <header class="page-header">
      <div>
        <h1>LOGOS Wallet — Кошелёк</h1>
        <p class="subtitle">
          Non‑custodial кошелёк: ключи и подписи живут только в этом браузере.
          Никакого серверного хранилища.
        </p>
      </div>
    </header>

    <!-- RID / PUB -->
    <section class="card">
      <header class="card-header">
        <div>
          <h2 class="card-title">Твой RID / Публичный ключ</h2>
          <p class="card-caption">
            RID — адрес аккаунта в сети LOGOS. Публичный ключ (hex) используется для проверки подписи.
          </p>
        </div>
      </header>
      <div class="card-body">
        <textarea id="pub" class="mono-field" readonly></textarea>
        <p class="hint">
          Ключи живут только в памяти этой вкладки. После выхода или закрытия
          вкладки для доступа к кошельку снова нужен пароль.
        </p>
      </div>
    </section>

    <!-- Баланс -->
    <section class="card">
      <header class="card-header">
        <div>
          <h2 class="card-title">Баланс</h2>
          <p class="card-caption">
            Проверка баланса и nonce для выбранного RID.
          </p>
        </div>
      </header>
      <div class="card-body">
        <label class="field">
          <span class="field-label">RID</span>
          <input id="rid-balance" type="text" class="field-input" placeholder="RID"/>
        </label>

        <div class="actions-row">
          <button id="btn-balance" class="btn primary">Показать баланс</button>
        </div>

        <pre id="out-balance" class="mono-output"></pre>
      </div>
    </section>

    <!-- Подпись и отправка -->
    <section class="card">
      <header class="card-header">
        <div>
          <h2 class="card-title">Подпись и отправка (batch)</h2>
          <p class="card-caption">
            Подписанная Ed25519 транзакция отправляется в ноду как батч (одна транзакция).
          </p>
        </div>
      </header>
      <div class="card-body">
        <label class="field">
          <span class="field-label">Получатель (RID)</span>
          <input id="to" type="text" class="field-input" placeholder="RID получателя"/>
        </label>

        <div class="field-row">
          <label class="field grow">
            <span class="field-label">Сумма (LGN)</span>
            <input id="amount" type="number" min="0" step="1" class="field-input"/>
          </label>

          <label class="field field-nonce">
            <span class="field-label">Nonce (debug)</span>
            <input id="nonce" type="number" class="field-input"/>
          </label>
        </div>

        <div class="actions-row">
          <button id="btn-send" class="btn primary">Подписать и отправить</button>
          <button id="btn-nonce" class="btn ghost">Получить nonce</button>
        </div>

        <pre id="out-send" class="mono-output"></pre>
      </div>
    </section>

    <!-- Стейкинг -->
    <section class="card">
      <header class="card-header">
        <div>
          <h2 class="card-title">Стейкинг (delegate / undelegate / claim)</h2>
          <p class="card-caption">
            Управление стейкингом текущего RID: делегирование, раз‑делегирование и заявка наград.
          </p>
        </div>
        <button id="btn-stake-refresh" class="chip chip-ghost">Обновить статус</button>
      </header>
      <div class="card-body">
        <pre id="out-stake" class="mono-output"></pre>

        <div class="field-row">
          <label class="field grow">
            <span class="field-label">Застейкать (delegate, LGN)</span>
            <input id="stake-amount" type="number" min="0" step="1" class="field-input"/>
          </label>
          <button id="btn-stake-delegate" class="btn primary">Делегировать</button>
        </div>

        <div class="field-row">
          <label class="field grow">
            <span class="field-label">Разстейкать (undelegate, LGN)</span>
            <input id="unstake-amount" type="number" min="0" step="1" class="field-input"/>
          </label>
          <button id="btn-stake-undelegate" class="btn ghost">Разстейкать</button>
        </div>

        <div class="actions-row">
          <button id="btn-stake-claim" class="btn secondary">Заявить награду (claim)</button>
        </div>
      </div>
    </section>

    <!-- Мост rToken -->
    <section class="card">
      <header class="card-header">
        <div>
          <h2 class="card-title">Мост rToken (депозит, demo)</h2>
          <p class="card-caption">
            Демонстрационный депозит rLGN через внешний txid.
          </p>
        </div>
      </header>
      <div class="card-body">
        <label class="field">
          <span class="field-label">RID</span>
          <input id="rid-bridge" type="text" class="field-input" placeholder="RID для депозита rLGN"/>
        </label>

        <div class="field-row">
          <label class="field grow">
            <span class="field-label">Сумма (rLGN)</span>
            <input id="amount-bridge" type="number" min="0" step="1" class="field-input"/>
          </label>

          <label class="field grow">
            <span class="field-label">ext_txid (например eth_txid_0xabc)</span>
            <input id="ext" type="text" class="field-input"/>
          </label>
        </div>

        <div class="actions-row">
          <button id="btn-deposit" class="btn primary">Deposit rLGN (demo)</button>
        </div>

        <pre id="out-bridge" class="mono-output"></pre>
      </div>
    </section>
  </main>

  <script src="./app.js?v=1" defer></script>
</body>
</html>

```

### FILE: /opt/logos/www/wallet/login.html
```
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta http-equiv="refresh" content="0; url=./auth.html"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Wallet</title>
</head>
<body>
  <p>Redirect to <a href="./auth.html">auth.html</a>…</p>
</body>
</html>

```

### FILE: /opt/logos/www/wallet/ui.js
```
(() => {
  // Берём API из app.js, если он есть, иначе собираем по origin
  const API_BASE = (window.API ||
                    window.API_ENDPOINT ||
                    (location.origin.replace(/\/$/, '') + '/api'));

  function fmtInt(x) {
    if (x === null || x === undefined) return '—';
    if (typeof x !== 'number') {
      const n = Number(x);
      if (!Number.isFinite(n)) return String(x);
      x = n;
    }
    return x.toLocaleString('en-US');
  }

  function fmtShare(x) {
    if (x === null || x === undefined) return '—';
    if (typeof x !== 'number') {
      const n = Number(x);
      if (!Number.isFinite(n)) return String(x);
      x = n;
    }
    return x.toFixed(6) + ' %';
  }

  function setBalanceWidgets(data) {
    const elLgn   = document.querySelector('#balance-lgn');
    const elRLgn  = document.querySelector('#balance-rlgn');
    const elMicro = document.querySelector('#balance-micro');
    const elShare = document.querySelector('#balance-share');

    const all = [elLgn, elRLgn, elMicro, elShare].filter(Boolean);
    if (!all.length) return;

    if (!data || typeof data !== 'object') {
      all.forEach((el) => { el.textContent = '—'; });
      return;
    }

    if (elLgn) {
      elLgn.textContent = (data.balance !== undefined)
        ? fmtInt(data.balance)
        : '—';
    }

    const rVal = (data.balance_rLGN !== undefined)
      ? data.balance_rLGN
      : data.balance_r_lgn;

    if (elRLgn) {
      elRLgn.textContent = (rVal !== undefined)
        ? fmtInt(rVal)
        : '—';
    }

    if (elMicro) {
      elMicro.textContent = (data.balance_micro !== undefined)
        ? fmtInt(data.balance_micro)
        : '—';
    }

    if (elShare) {
      elShare.textContent = (data.share_of_supply_percent !== undefined)
        ? fmtShare(data.share_of_supply_percent)
        : '—';
    }
  }

  async function fetchBalance(rid) {
    const resp = await fetch(
      `${API_BASE}/balance/${encodeURIComponent(rid)}`,
      { method: 'GET', credentials: 'same-origin', cache: 'no-store' },
    );
    if (!resp.ok) {
      throw new Error(`/balance ${resp.status}`);
    }
    return resp.json();
  }

  async function refreshWidgetsFromApi() {
    try {
      const inp = document.querySelector('#rid-balance');
      const rid = (inp && inp.value.trim()) || (window.RID || '').trim();
      if (!rid) return;
      const data = await fetchBalance(rid);
      setBalanceWidgets(data);
    } catch (e) {
      console.error('ui balance error:', e);
      setBalanceWidgets(null);
    }
  }

  function setup() {
    const btn = document.querySelector('#btn-balance');
    if (!btn) return;

    // При нажатии на "Показать баланс" делаем доп. запрос только для виджетов.
    btn.addEventListener('click', () => {
      // app.js уже делает свой запрос и пишет в <pre>,
      // а мы параллельно обновляем красивые плитки.
      refreshWidgetsFromApi();
    });

    // Можно один раз попробовать подтянуть баланс при загрузке,
    // если RID уже есть в сессии.
    refreshWidgetsFromApi().catch(() => {});
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setup);
  } else {
    setup();
  }
})();

```

### FILE: /opt/logos/www/wallet/wallet.css
```
:root {
  --bg: #050910;
  --bg-grad-1: rgba(56,189,248,0.18);
  --bg-grad-2: rgba(129,140,248,0.20);

  --card: #020617;
  --card-alt: #020617;

  --border-subtle: rgba(148,163,184,0.30);
  --border-strong: rgba(148,163,184,0.65);

  --accent: #3b82f6;
  --accent-soft: rgba(59,130,246,0.16);
  --accent-strong: #60a5fa;

  --danger: #f97373;

  --text-main: #e5e7eb;
  --text-muted: #9ca3af;

  --radius-card: 20px;
  --radius-sm: 10px;

  --shadow-soft: 0 24px 60px rgba(0,0,0,0.75);

  --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas,
           "Liberation Mono", "Courier New", monospace;
}

/* базовые */

*,
*::before,
*::after {
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
}

body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
               Roboto, sans-serif;
  background:
    radial-gradient(circle at top left, var(--bg-grad-1), transparent 58%),
    radial-gradient(circle at bottom right, var(--bg-grad-2), transparent 55%),
    var(--bg);
  color: var(--text-main);
  min-height: 100vh;
}

/* верхняя панель */

.topbar {
  position: sticky;
  top: 0;
  z-index: 40;
  background: linear-gradient(95deg, rgba(15,23,42,0.98), rgba(15,23,42,0.96));
  backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(148,163,184,0.18);
  box-shadow: 0 18px 40px rgba(0,0,0,0.65);
  padding: 10px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.topbar-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-dot {
  width: 26px;
  height: 26px;
  border-radius: 999px;
  background: radial-gradient(circle at 30% 30%, #22d3ee, #6366f1);
  box-shadow: 0 0 20px rgba(56,189,248,0.55);
}

.topbar-title {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
}

.topbar-title .brand {
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: #e5e7eb;
}

.topbar-title .product {
  font-size: 13px;
  color: var(--text-muted);
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12px;
}

.endpoint-label {
  color: var(--text-muted);
}

.endpoint-value {
  font-family: var(--mono);
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 999px;
  border: 1px solid var(--border-subtle);
  background: rgba(15,23,42,0.9);
}

/* общая раскладка */

.page-shell {
  max-width: 1040px;
  margin: 0 auto;
  padding: 18px 16px 40px;
}

.page-header {
  margin-bottom: 18px;
}

.page-header h1 {
  font-size: 22px;
  margin: 0 0 6px;
}

.subtitle {
  margin: 0;
  font-size: 13px;
  color: var(--text-muted);
}

/* карточки */

.card {
  background: radial-gradient(circle at top left, rgba(56,189,248,0.10), transparent 55%),
              var(--card);
  border-radius: var(--radius-card);
  border: 1px solid var(--border-subtle);
  box-shadow: var(--shadow-soft);
  margin-bottom: 18px;
  overflow: hidden;
}

.card-header {
  padding: 14px 18px 10px;
  border-bottom: 1px solid rgba(15,23,42,0.9);
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.card-title {
  font-size: 16px;
  margin: 0 0 4px;
}

.card-caption {
  margin: 0;
  font-size: 13px;
  color: var(--text-muted);
}

.card-body {
  padding: 14px 18px 16px;
}

/* поля */

.field {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 12px;
}

.field-row {
  display: flex;
  gap: 10px;
  align-items: flex-end;
  margin-bottom: 12px;
}

.field-row .grow {
  flex: 1 1 auto;
}

.field-label {
  font-size: 12px;
  color: var(--text-muted);
}

.field-input {
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  background: rgba(15,23,42,0.95);
  color: var(--text-main);
  padding: 8px 10px;
  font-size: 14px;
  outline: none;
}

.field-input:focus {
  border-color: var(--accent-strong);
  box-shadow: 0 0 0 1px rgba(59,130,246,0.55);
}

/* текстовые выводы */

.mono-field,
.mono-output {
  width: 100%;
  font-family: var(--mono);
  font-size: 13px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  background: rgba(2,6,23,0.96);
  color: var(--text-main);
  padding: 10px 12px;
  resize: vertical;
  min-height: 80px;
  white-space: pre-wrap;
}

.mono-output {
  margin-top: 8px;
}

/* кнопки */

.actions-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 6px;
  margin-bottom: 6px;
}

.btn {
  border-radius: 999px;
  border: 1px solid transparent;
  padding: 7px 14px;
  font-size: 13px;
  cursor: pointer;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.btn.primary {
  background: linear-gradient(135deg, #2563eb, #3b82f6);
  border-color: rgba(59,130,246,0.8);
  color: #fff;
}

.btn.primary:hover {
  background: linear-gradient(135deg, #1d4ed8, #2563eb);
}

.btn.secondary {
  background: rgba(15,23,42,0.95);
  border-color: var(--border-strong);
  color: var(--text-main);
}

.btn.secondary:hover {
  border-color: var(--accent-strong);
}

.btn.ghost {
  background: transparent;
  border-color: var(--border-subtle);
  color: var(--text-muted);
}

.btn.ghost:hover {
  border-color: var(--accent-soft);
  color: var(--text-main);
}

/* чипы */

.chip {
  padding: 5px 10px;
  border-radius: 999px;
  border: 1px solid var(--border-subtle);
  background: rgba(15,23,42,0.92);
  font-size: 12px;
  color: var(--text-muted);
  cursor: pointer;
}

.chip-ghost:hover {
  border-color: var(--accent-soft);
  color: var(--text-main);
}

/* подсказки */

.hint {
  margin-top: 8px;
  font-size: 12px;
  color: var(--text-muted);
}

/* адаптив */

@media (max-width: 720px) {
  .topbar {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .field-row {
    flex-direction: column;
    align-items: stretch;
  }

  .page-shell {
    padding: 14px 10px 32px;
  }
}

```
