
## FRONT TREE: /opt/logos/www/wallet_prod

```
/opt/logos/www/wallet_prod/
  api_base.js
  app.css
  app.html
  app.js
  assets.js
  auth.css
  auth.css.bad_20260114T075224Z
  auth.html
  auth.html.bad_20260114T075205Z
  auth.js
  compat.js
  connect.js
  index.html
  login.html
  tabs.js
  ui.css
  ui.js
  wallet.css
/opt/logos/www/wallet_prod/modules/
    lgn_send.js
    lgn_send.js.bad_20260113T164615Z
    send.js
    settings.js
    tx_redirect.js
/opt/logos/www/wallet_prod/vendor/
    bip39_english.txt
    bip39_lite.js
    nacl-fast.min.js
    wordlist_en.js

```

## FRONT FILE: /opt/logos/www/wallet_prod/app.html

```
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>LOGOS Wallet</title>
  <script src="./api_base.js?v=1"></script>
  <link rel="stylesheet" href="./app.css?v=20260111_110230" />
</head>
<body>
  <div class="topbar">
    <div class="brand">LOGOS Wallet</div>
    <div class="topbar-right">
      <div class="pill">API: <span id="api" class="mono">/api</span></div>
      <div class="pill">RID: <span id="topRid" class="mono">—</span></div>
      <div class="pill">LGN: <span id="topBal" class="mono">—</span></div>
      <button id="btnLogout" class="btn small">Выйти</button>
    </div>
  </div>

  <div class="wrap">

    <div class="tabs">
      <div class="tab active" data-tab="assets">Активы</div>
      <div class="tab" data-tab="send">Отправка</div>
      <div class="tab" data-tab="staking">Стейкинг</div>
      <div class="tab" data-tab="bridge">Bridge</div>
      <div class="tab" data-tab="settings">Настройки</div>
    </div>

    <!-- ASSETS -->
    <div class="panel active" id="panel-assets">
      <div class="grid">
        <div class="card">
          <div class="h2">RID / Identity</div>
          <div class="muted">Это твой резонансный адрес. Сервер видит только подпись.</div>

          <label style="margin-top:10px">RID</label>
          <input id="rid" class="mono" readonly />

          <div class="row">
            <button id="btnCopyRid" class="btn">Copy</button>
            <button id="btnRefresh" class="btn primary">Refresh LOGOS</button>
            <span id="netBadge" class="muted"></span>
          </div>

          <div id="status" class="status"></div>
        </div>

        <div class="card">
          <div class="h2">Portfolio</div>
          <div class="muted">LOGOS (LGN) — баланс в сети.</div>

          <div style="margin-top:10px">
            <div class="big-num mono" id="balLgn">—</div>
            <div class="muted mono" id="balMicro">—</div>
          </div>

          <div class="row">
            <div class="pill">nonce: <span id="nonce" class="mono">—</span></div>
            <div class="pill">latency: <span id="lat" class="mono">—</span></div>
          </div>

          <details>
            <summary>Details (raw)</summary>
            <pre id="rawNode" class="pre"></pre>
          </details>
        </div>
      </div>

      <div class="grid" style="margin-top:16px">
        <div class="card">
          <div class="h2">Receive addresses</div>
          <div class="muted">BTC/ETH/TRON/USDT адреса закреплены за RID (wallet-api).</div>
          <div id="recvBox"></div>

          <details>
            <summary>Details (wallet-api raw)</summary>
            <pre id="rawRecv" class="pre"></pre>
          </details>
        </div>

        <div class="card">
          <div class="h2">External balances</div>
          <div class="muted">Баланс внешних сетей (wallet-api).</div>
          <div id="extBalBox"></div>

          <details>
            <summary>Details (wallet-api raw)</summary>
            <pre id="rawExt" class="pre"></pre>
          </details>
        </div>
      </div>
    </div>

    <!-- SEND -->
    <div class="panel" id="panel-send">
      <div class="grid">
        <div class="card">
          <div class="h2">Withdraw (USDT)</div>
          <div class="muted">Отправка через wallet-api /v1/withdraw (по OpenAPI: USDT + ETH).</div>

          <label style="margin-top:10px">Network</label>
          <select id="wdNetwork">
            <option value="ETH">ETH</option>
          </select>

          <label style="margin-top:10px">Amount (integer)</label>
          <input id="wdAmount" class="mono" placeholder="например 100" />

          <label style="margin-top:10px">To address</label>
          <input id="wdTo" class="mono" placeholder="0x... или другое" />

          <div class="row">
            <button id="btnWithdraw" class="btn primary">Send</button>
            <button id="btnWithdrawClear" class="btn">Clear</button>
          </div>

          <div id="wdStatus" class="status"></div>

          <details>
            <summary>Response</summary>
            <pre id="wdRaw" class="pre"></pre>
          </details>
        </div>

        <div class="card">
          <div class="h2">LOGOS transfer</div>
          <div class="muted">Отправка LGN внутри сети LOGOS (node-api /submit_tx).</div>

<div style="margin-top:12px;display:grid;gap:10px">
  <label>To RID</label>
  <input id="lgnTo" class="mono" placeholder="RID получателя..." autocomplete="off" />

  <label>Amount (LGN)</label>
  <input id="lgnAmount" class="mono" placeholder="например 1.25" inputmode="decimal" autocomplete="off" />

  <div class="row">
    <button id="btnLgnSend" class="btn primary" type="button">Send LGN</button>
    <button id="btnLgnClear" class="btn" type="button">Clear</button>
    <button id="btnLgnDetails" class="btn" type="button">Details (raw)</button>
  </div>

  <div id="lgnStatus" class="status"></div>
  <pre id="lgnRaw" class="mono" style="display:none;white-space:pre-wrap"></pre>
</div>
        </div>
      </div>
    </div>

    <!-- STAKING -->
    <div class="panel" id="panel-staking">
      <div class="card">
        <div class="h2">Staking</div>
        <div class="muted">
          Вкладка готова по UI. Чтобы она была “не пустая”, нужен backend endpoint стейкинга (stake/unstake/apy).
          Дай API — подключу. Пока не выдумываю, чтобы не было лжи и “пустых кнопок”.
        </div>
      </div>
    </div>

    <!-- BRIDGE -->
    <div class="panel" id="panel-bridge">
  <div id="bridgeRoot"></div>

      <div class="grid">
        <div class="card">
          <div class="h2">Topup address</div>
          <div class="muted">Получить адрес для пополнения (wallet-api /v1/topup/request).</div>

          <label style="margin-top:10px">Network</label>
          <select id="topNetwork">
            <option value="ETH">ETH</option>
          </select>

          <div class="row">
            <button id="btnTopup" class="btn primary">Get address</button>
          </div>

          <div id="topupStatus" class="status"></div>
          <div id="topupBox"></div>
        </div>

        <div class="card">
          <div class="h2">Quote</div>
          <div class="muted">Расчёт курса (wallet-api /v1/quote). amount — integer.</div>

          <label style="margin-top:10px">From</label>
          <input id="qFrom" class="mono" value="USDT" />

          <label style="margin-top:10px">To</label>
          <input id="qTo" class="mono" value="LGN" />

          <label style="margin-top:10px">Amount</label>
          <input id="qAmount" class="mono" placeholder="например 100" />

          <div class="row">
            <button id="btnQuote" class="btn primary">Get quote</button>
          </div>

          <div id="qStatus" class="status"></div>

          <details>
            <summary>Response</summary>
            <pre id="qRaw" class="pre"></pre>
          </details>
        </div>
      </div>
    </div>

    <!-- SETTINGS -->
    <div class="panel" id="panel-settings">
      <div class="grid">
        <div class="card">
          <div class="h2">Local storage</div>
          <div class="muted">RID и пароль хранятся локально в браузере.</div>

          <div class="row">
            <button id="btnShowLocal" class="btn">Show RID</button>
            <button id="btnClearLocal" class="btn danger">Clear local keys</button>
          </div>

          <div id="setStatus" class="status"></div>
        </div>

        <div class="card">
          <div class="h2">Endpoints</div>
          <div class="muted mono">API_BASE = /api, WALLET_API = /wallet-api</div>
        </div>
      </div>
    </div>

  </div>

  <script src="./app.js?v=20260112_084410" defer></script>
<script src="modules/settings.js?v=20260111_172540" defer></script>
  <script src="modules/tx_redirect.js?v=20260112_070814" defer></script>
<script src="modules/send.js?v=20260113_153723" defer></script>
<script src="/wallet/modules/lgn_send.js?v=20260113161416"></script>
</body>
</html>
```

## FRONT FILE: /opt/logos/www/wallet_prod/app.js

```
(function(){
  const $ = (id) => document.getElementById(id);

  function setStatus(t){ const el=$("status"); if(el) el.textContent = t || ""; }
  function setNetBadge(ok){
    const el = $("netBadge");
    if (!el) return;
    el.className = "muted " + (ok ? "badge-ok" : "badge-bad");
    el.textContent = ok ? "live" : "offline";
  }

  function readRID(){
    try{
      return (localStorage.getItem("RID") || localStorage.getItem("logos_rid") || "").trim();
    }catch(e){ return ""; }
  }

  function devMode(){
    try { return localStorage.getItem("logos_dev") === "1"; } catch(e){ return false; }

  function clearSessionPass(){
    try{
      sessionStorage.removeItem("PASS");
      sessionStorage.removeItem("logos_pass");
    }catch(e){}
  }
  }

  function fmtLgnFromMicro(micro){
    const s = String(micro);
    const neg = s.startsWith("-");
    const a = neg ? s.slice(1) : s;
    const pad = a.padStart(7, "0");
    const intPart = pad.slice(0, -6);
    const frac = pad.slice(-6);
    return (neg ? "-" : "") + intPart + "." + frac;
  }

  function shortRid(rid){
    if (!rid) return "—";
    if (rid.length <= 18) return rid;
    return rid.slice(0,10) + "…" + rid.slice(-6);
  }

  async function jfetch(url, opts){
    const t0 = performance.now();
    const r = await fetch(url, Object.assign({ cache: "no-store" }, opts||{}));
    const t1 = performance.now();
    return { r, ms: Math.round(t1 - t0) };
  }

  function escapeHtml(s){
    return String(s)
      .replaceAll("&","&amp;")
      .replaceAll("<","&lt;")
      .replaceAll(">","&gt;")
      .replaceAll('"',"&quot;")
      .replaceAll("'","&#039;");
  }

  function copyText(t){
    try{ navigator.clipboard.writeText(String(t||"")); setStatus("OK: copied."); }
    catch(e){ setStatus("ERR: copy failed."); }
  }

  function mkLine(container, title, value, copyValue){
    const row = document.createElement("div");
    row.className = "kv";
    row.innerHTML = `
      <div>
        <div class="k">${escapeHtml(title)}</div>
        <div class="v">${escapeHtml(value || "—")}</div>
      </div>
      <button class="btn small">Copy</button>
    `;
    row.querySelector("button").addEventListener("click", () => copyText(copyValue ?? value ?? ""));
    container.appendChild(row);
  }

  function renderReceive(container, addresses){
    container.innerHTML = "";
    if (!addresses || typeof addresses !== "object"){
      container.innerHTML = '<div class="muted">Нет адресов.</div>';
      return;
    }
    // order: BTC, ETH, TRON, USDT_ERC20, USDT_TRC20
    const order = ["BTC","ETH","TRON","USDT_ERC20","USDT_TRC20"];
    for (const k of order){
      if (addresses[k]){
        const title =
          k === "USDT_ERC20" ? "USDT (ERC20)" :
          k === "USDT_TRC20" ? "USDT (TRC20)" :
          k;
        mkLine(container, title, addresses[k], addresses[k]);
      }
    }
  }

  function satToBtc(sat){ return (Number(sat||0) / 1e8).toFixed(8).replace(/\.?0+$/,''); }
  function formatNum(x){
    if (x == null) return "0";
    const n = Number(x);
    if (!isFinite(n)) return String(x);
    return String(n);
  }

  function renderExternal(container, j){
    container.innerHTML = "";
    if (!j || typeof j !== "object"){
      container.innerHTML = '<div class="muted">Нет данных.</div>';
      return;
    }

    const b = j.balances || {};
    // BTC
    if (b.BTC && typeof b.BTC === "object"){
      const sat = (b.BTC.total_sat ?? b.BTC.confirmed_sat ?? b.BTC.confirmed ?? 0);
      const btc = (b.BTC.total_btc != null) ? formatNum(b.BTC.total_btc) : satToBtc(sat);
      mkLine(container, "BTC balance", btc + " BTC", btc);
    } else {
      mkLine(container, "BTC balance", "0 BTC", "0");
    }

    // ETH + USDT ERC20
    if (b.ETH && typeof b.ETH === "object"){
      const eth = (b.ETH.eth != null) ? formatNum(b.ETH.eth) : (b.ETH.wei != null ? (Number(b.ETH.wei)/1e18) : 0);
      mkLine(container, "ETH balance", formatNum(eth) + " ETH", String(eth));
      if (b.ETH.usdt_erc20 && typeof b.ETH.usdt_erc20 === "object"){
        const u = b.ETH.usdt_erc20.usdt ?? 0;
        mkLine(container, "USDT (ERC20) balance", formatNum(u) + " USDT", String(u));
      }
    } else {
      mkLine(container, "ETH balance", "0 ETH", "0");
      mkLine(container, "USDT (ERC20) balance", "0 USDT", "0");
    }

    // TRON + USDT TRC20
    if (b.TRON && typeof b.TRON === "object"){
      const trx = (b.TRON.trx != null) ? formatNum(b.TRON.trx) : (b.TRON.sun != null ? (Number(b.TRON.sun)/1e6) : 0);
      mkLine(container, "TRX balance", formatNum(trx) + " TRX", String(trx));
      if (b.TRON.usdt_trc20 && typeof b.TRON.usdt_trc20 === "object"){
        const u = b.TRON.usdt_trc20.usdt ?? 0;
        mkLine(container, "USDT (TRC20) balance", formatNum(u) + " USDT", String(u));
      }
    } else {
      mkLine(container, "TRX balance", "0 TRX", "0");
      mkLine(container, "USDT (TRC20) balance", "0 USDT", "0");
    }

    // latency
    if (j.latency_ms != null){
      mkLine(container, "wallet-api latency", String(j.latency_ms) + " ms", String(j.latency_ms));
    }
  }

  async function refreshAll(){
    const rid = readRID();
    if (!rid){
      setStatus("ERR: RID не найден. Зайди через auth.html");
      try{ location.href = "./auth.html"; }catch(e){}
      return;
    }

    const API_BASE = window.API_BASE || "/api";
    const WALLET_API = window.WALLET_API || "/wallet-api";

    if ($("api")) $("api").textContent = API_BASE;
    if ($("rid")) $("rid").value = rid;
    if ($("topRid")) $("topRid").textContent = shortRid(rid);

    // 1) node balance
    try{
      const { r, ms } = await jfetch(API_BASE + "/balance/" + encodeURIComponent(rid));
      if ($("lat")) $("lat").textContent = ms + " ms";
      if (!r.ok) throw new Error("HTTP " + r.status);
      const j = await r.json();

      const micro = (j && j.balance != null) ? j.balance : 0;
      if ($("balLgn")) $("balLgn").textContent = fmtLgnFromMicro(micro);
      if ($("balMicro")) $("balMicro").textContent = String(micro) + " micro-LGN";
      if ($("nonce")) $("nonce").textContent = (j && j.nonce != null) ? String(j.nonce) : "—";
      if ($("rawNode")) $("rawNode").textContent = JSON.stringify(j, null, 2);
      if ($("topBal")) $("topBal").textContent = fmtLgnFromMicro(micro);

      setNetBadge(true);
      setStatus("OK: обновлено.");
    }catch(e){
      setNetBadge(false);
      setStatus("ERR node-api: " + (e && e.message ? e.message : String(e)));
    }

    // 2) wallet receive
    try{
      const { r } = await jfetch(WALLET_API + "/v1/receive/" + encodeURIComponent(rid));
      if (!r.ok) throw new Error("HTTP " + r.status);
      const j = await r.json();

      if ($("rawRecv")) $("rawRecv").textContent = JSON.stringify(j, null, 2);
      renderReceive($("recvBox"), j.addresses || {});
    }catch(e){
      if ($("rawRecv")) $("rawRecv").textContent = "";
      if ($("recvBox")) $("recvBox").innerHTML = '<div class="muted">ERR wallet-api receive: ' + escapeHtml(e.message||String(e)) + '</div>';
    }

    // 3) wallet balances
    try{
      const { r } = await jfetch(WALLET_API + "/v1/balances/" + encodeURIComponent(rid));
      if (!r.ok) throw new Error("HTTP " + r.status);
      const j = await r.json();

      if ($("rawExt")) $("rawExt").textContent = JSON.stringify(j, null, 2);
      renderExternal($("extBalBox"), j);
    }catch(e){
      if ($("rawExt")) $("rawExt").textContent = "";
      if ($("extBalBox")) $("extBalBox").innerHTML = '<div class="muted">ERR wallet-api balances: ' + escapeHtml(e.message||String(e)) + '</div>';
    }
  }

  function setTab(name){
    document.querySelectorAll(".tab").forEach(t => {
      t.classList.toggle("active", t.dataset.tab === name);
    });
    document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
    const panel = document.getElementById("panel-" + name);
    if (panel) panel.classList.add("active");
    try{ location.hash = name; }catch(e){}
  }

  function uuid(){
    const b = crypto.getRandomValues(new Uint8Array(16));
    b[6] = (b[6] & 0x0f) | 0x40;
    b[8] = (b[8] & 0x3f) | 0x80;
    const h = [...b].map(x => x.toString(16).padStart(2,"0")).join("");
    return `${h.slice(0,8)}-${h.slice(8,12)}-${h.slice(12,16)}-${h.slice(16,20)}-${h.slice(20)}`;
  }

  async function doTopup(){
    const rid = readRID();
    const net = $("topNetwork") ? ($("topNetwork").value || "ETH") : "ETH";
    const box = $("topupBox");
    const st = $("topupStatus");
    if (st) st.textContent = "request…";
    if (box) box.innerHTML = "";

    try{
      const body = { rid, token:"USDT", network: net };
      const { r } = await jfetch((window.WALLET_API||"/wallet-api") + "/v1/topup/request", {
        method:"POST",
        headers:{ "content-type":"application/json" },
        body: JSON.stringify(body)
      });
      const j = await r.json().catch(()=>({}));
      if (!r.ok) throw new Error("HTTP " + r.status + ": " + JSON.stringify(j));
      if (st) st.textContent = "OK";

      if (box){
        box.innerHTML = "";
        if (j.address) mkLine(box, "Topup address", j.address, j.address);
        if (j.network) mkLine(box, "Network", j.network, j.network);
        if (j.token) mkLine(box, "Token", j.token, j.token);
      }
    }catch(e){
      if (st) st.textContent = "ERR: " + (e.message||String(e));
    }
  }

  async function doQuote(){
    const st = $("qStatus"), pre = $("qRaw");
    if (st) st.textContent = "request…";
    if (pre) pre.textContent = "";
    try{
      const body = {
        from_token: ***
        to_token: ***
        amount: parseInt(($("qAmount")?.value || "0").trim(), 10)
      };
      const { r } = await jfetch((window.WALLET_API||"/wallet-api") + "/v1/quote", {
        method:"POST",
        headers:{ "content-type":"application/json" },
        body: JSON.stringify(body)
      });
      const j = await r.json().catch(()=>({}));
      if (!r.ok) throw new Error("HTTP " + r.status + ": " + JSON.stringify(j));
      if (st) st.textContent = "OK";
      if (pre) pre.textContent = JSON.stringify(j, null, 2);
    }catch(e){
      if (st) st.textContent = "ERR: " + (e.message||String(e));
    }
  }

  async function doWithdraw(){
    const rid = readRID();
    const net = $("wdNetwork") ? ($("wdNetwork").value || "ETH") : "ETH";
    const amt = parseInt(($("wdAmount")?.value || "0").trim(), 10);
    const to = ($("wdTo")?.value || "").trim();

    const st = $("wdStatus"), pre = $("wdRaw");
    if (st) st.textContent = "request…";
    if (pre) pre.textContent = "";

    try{
      const body = {
        rid,
        token: ***
        network: net,
        amount: amt,
        to_address: to,
        request_id: uuid()
      };
      const { r } = await jfetch((window.WALLET_API||"/wallet-api") + "/v1/withdraw", {
        method:"POST",
        headers:{ "content-type":"application/json" },
        body: JSON.stringify(body)
      });
      const j = await r.json().catch(()=>({}));
      if (!r.ok) throw new Error("HTTP " + r.status + ": " + JSON.stringify(j));
      if (st) st.textContent = "OK";
      if (pre) pre.textContent = JSON.stringify(j, null, 2);
    }catch(e){
      if (st) st.textContent = "ERR: " + (e.message||String(e));
    }
  }

  window.addEventListener("DOMContentLoaded", () => {
    // hide raw blocks for normal users
    if (!devMode()){
      document.querySelectorAll("details").forEach(d => d.style.display = "none");
    }

    document.querySelectorAll(".tab").forEach(t => {
      t.addEventListener("click", () => setTab(t.dataset.tab));
    });
    const start = (location.hash||"").replace("#","") || "assets";
    setTab(start);

    $("btnCopyRid")?.addEventListener("click", () => copyText($("rid")?.value || ""));
    $("btnRefresh")?.addEventListener("click", refreshAll);

    $("btnLogout")?.addEventListener("click", () => {
      try{ localStorage.removeItem("PASS"); localStorage.removeItem("logos_pass"); }catch(e){}
      location.href = "./auth.html";
    });

    $("btnTopup")?.addEventListener("click", doTopup);
    $("btnQuote")?.addEventListener("click", doQuote);

    $("btnWithdraw")?.addEventListener("click", doWithdraw);
    $("btnWithdrawClear")?.addEventListener("click", () => {
      if ($("wdAmount")) $("wdAmount").value = "";
      if ($("wdTo")) $("wdTo").value = "";
      if ($("wdStatus")) $("wdStatus").textContent = "";
      if ($("wdRaw")) $("wdRaw").textContent = "";
    });

    $("btnShowLocal")?.addEventListener("click", () => {
      const rid = readRID();
      if ($("setStatus")) $("setStatus").textContent = rid ? ("RID: " + rid) : "RID не найден.";
    });
    $("btnClearLocal")?.addEventListener("click", () => {
      try{
        localStorage.removeItem("RID");
        localStorage.removeItem("logos_rid");
        localStorage.removeItem("PASS");
        localStorage.removeItem("logos_pass");
      }catch(e){}
      if ($("setStatus")) $("setStatus").textContent = "OK: local keys cleared";
    });

    refreshAll();
  });

  window._logos_refreshAll = refreshAll;
})();

/* ========= BRIDGE MODULE (v1) ========= */
(() => {
  function ridGet(){
    return (
      localStorage.getItem("RID") ||
      localStorage.getItem("logos_rid") ||
      sessionStorage.getItem("RID") ||
      sessionStorage.getItem("logos_rid") ||
      ""
    );
  }

  function apiBase(){
    // wallet-api (FastAPI proxy)
    return (window.LOGOS_WALLET_API || window.WALLET_API || (window.location.origin.replace(/\/+$/, "") + "/wallet-api"));
  }

  function esc(s){
    return String(s ?? "").replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
  }

  function q(sel, root=document){ return root.querySelector(sel); }

  function setMsg(root, text, ok=true){
    const el = q(".bridgeMsg", root);
    if (!el) return;
    el.textContent = text || "";
    el.style.opacity = text ? "1" : "0";
    el.style.color = ok ? "" : "#ff6b6b";
  }

  async function postJSON(url, body){
    const r = await fetch(url, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify(body || {})
    });
    const t = await r.text();
    let j = null;
    try { j = JSON.parse(t); } catch(e) {}
    if (!r.ok){
      const msg = (j && (j.detail || j.error)) ? JSON.stringify(j) : (t || ("HTTP " + r.status));
      throw new Error(msg);
    }
    return j ?? {};
  }

  function shortRID(rid){
    if (!rid) return "";
    if (rid.length <= 18) return rid;
    return rid.slice(0, 10) + "…" + rid.slice(-6);
  }

  function genReqId(){
    return "w_" + Date.now().toString(36) + "_" + Math.random().toString(36).slice(2,10);
  }

  function renderBridge(){
    const panel = document.getElementById("panel-bridge");
    const root = document.getElementById("bridgeRoot");
    if (!panel || !root) return;

    // прячем старое/случайное содержимое панели, оставляем только bridgeRoot
    try{
      [...panel.children].forEach(ch => { if (ch !== root) ch.style.display = "none"; });
    }catch(e){}

    const rid = ridGet();
    root.innerHTML = `
      <div class="card">
        <div class="h">Bridge</div>
        <div class="muted">Обмен/ввод/вывод через wallet-api. Для обычных людей — без сырого текста.</div>
        <div style="height:10px"></div>
        <div class="bridgeMsg muted" style="opacity:0; transition:.2s;"></div>
      </div>

      <div class="card">
        <div class="h">Quote</div>
        <div class="muted">Расчёт курса (без отправки транзакции).</div>
        <div style="height:12px"></div>

        <div class="row" style="display:flex; gap:10px; flex-wrap:wrap;">
          <div style="flex:1; min-width:200px;">
            <div class="muted" style="margin-bottom:6px;">From</div>
            <input class="mono" id="qFrom" value="USDT" />
          </div>
          <div style="flex:1; min-width:200px;">
            <div class="muted" style="margin-bottom:6px;">To</div>
            <input class="mono" id="qTo" value="LGN" />
          </div>
          <div style="flex:1; min-width:200px;">
            <div class="muted" style="margin-bottom:6px;">Amount</div>
            <input class="mono" id="qAmt" value="100" />
          </div>
        </div>

        <div style="height:12px"></div>
        <button class="btn" id="btnQuote">Get quote</button>

        <div style="height:10px"></div>
        <div class="muted" id="quoteOut" style="white-space:pre-wrap;"></div>
      </div>

      <div class="card">
        <div class="h">Top up</div>
        <div class="muted">Получить адрес для пополнения (USDT).</div>
        <div style="height:12px"></div>

        <div class="row" style="display:flex; gap:10px; flex-wrap:wrap;">
          <div style="flex:1; min-width:200px;">
            <div class="muted" style="margin-bottom:6px;">Network</div>
            <select class="mono" id="tuNet">
              <option value="ETH" selected>ETH</option>
            </select>
          </div>
          <div style="flex:1; min-width:200px;">
            <div class="muted" style="margin-bottom:6px;">Token</div>
            <select class="mono" id="tuTok">
              <option value="USDT" selected>USDT</option>
            </select>
          </div>
        </div>

        <div style="height:12px"></div>
        <button class="btn" id="btnTopup">Get deposit address</button>

        <div style="height:12px"></div>
        <div class="muted">Address</div>
        <div style="display:flex; gap:10px; align-items:center; flex-wrap:wrap;">
          <input class="mono" id="tuAddr" readonly value="" style="flex:1; min-width:260px;" />
          <button class="btn" id="btnCopyTopup" type="button">Copy</button>
        </div>
      </div>

      <div class="card">
        <div class="h">Withdraw</div>
        <div class="muted">Вывод USDT (тестовая ручка, если включена на сервере).</div>
        <div style="height:12px"></div>

        <div class="row" style="display:flex; gap:10px; flex-wrap:wrap;">
          <div style="flex:1; min-width:200px;">
            <div class="muted" style="margin-bottom:6px;">Network</div>
            <select class="mono" id="wdNet">
              <option value="ETH" selected>ETH</option>
            </select>
          </div>
          <div style="flex:1; min-width:200px;">
            <div class="muted" style="margin-bottom:6px;">Token</div>
            <select class="mono" id="wdTok">
              <option value="USDT" selected>USDT</option>
            </select>
          </div>
          <div style="flex:1; min-width:200px;">
            <div class="muted" style="margin-bottom:6px;">Amount</div>
            <input class="mono" id="wdAmt" value="1" />
          </div>
        </div>

        <div style="height:10px"></div>
        <div class="muted" style="margin-bottom:6px;">To address</div>
        <input class="mono" id="wdTo" value="" placeholder="0x... or T..." />

        <div style="height:12px"></div>
        <button class="btn" id="btnWithdraw">Withdraw</button>

        <div style="height:10px"></div>
        <div class="muted" id="wdOut" style="white-space:pre-wrap;"></div>
      </div>
    `;

    // handlers
    q("#btnQuote", root).addEventListener("click", async () => {
      try{
        setMsg(root, "Запрашиваю quote…");
        const from = q("#qFrom", root).value.trim();
        const to   = q("#qTo", root).value.trim();
        const amt  = parseInt(q("#qAmt", root).value.trim() || "0", 10);

        const data = await postJSON(apiBase() + "/v1/quote", {from_token: from, to_token: to, amount: amt});
        q("#quoteOut", root).textContent = `price: ${data.price}\nexpected_out: ${data.expected_out}`;
        setMsg(root, "OK: quote готов ✅");
      }catch(e){
        setMsg(root, "ERR: " + (e?.message || e), false);
      }
    });

    q("#btnTopup", root).addEventListener("click", async () => {
      try{
        if (!rid) throw new Error("RID не найден в localStorage");
        setMsg(root, "Запрашиваю адрес пополнения…");
        const network = q("#tuNet", root).value;
        const token   = q("#tuTok", root).value;
        const data = await postJSON(apiBase() + "/v1/topup/request", {rid, network, token});
        q("#tuAddr", root).value = data.address || "";
        setMsg(root, "OK: адрес получен ✅");
      }catch(e){
        setMsg(root, "ERR: " + (e?.message || e), false);
      }
    });

    q("#btnCopyTopup", root).addEventListener("click", async () => {
      const v = q("#tuAddr", root).value;
      if (!v) return;
      try{ await navigator.clipboard.writeText(v); setMsg(root, "Скопировано ✅"); }
      catch(e){ setMsg(root, "Не смог скопировать (браузер).", false); }
    });

    q("#btnWithdraw", root).addEventListener("click", async () => {
      try{
        if (!rid) throw new Error("RID не найден в localStorage");
        const network = q("#wdNet", root).value;
        const token   = q("#wdTok", root).value;
        const amount  = parseInt(q("#wdAmt", root).value.trim() || "0", 10);
        const to_address = q("#wdTo", root).value.trim();
        if (!to_address) throw new Error("Укажи to_address");
        const request_id = genReqId();

        setMsg(root, "Отправляю withdraw…");
        const data = await postJSON(apiBase() + "/v1/withdraw", {rid, network, token, amount, to_address, request_id});
        q("#wdOut", root).textContent = data ? JSON.stringify(data, null, 2) : "OK";
        setMsg(root, "OK: withdraw запрос отправлен ✅");
      }catch(e){
        setMsg(root, "ERR: " + (e?.message || e), false);
      }
    });

    // верхняя шапка (чисто подсказка, не ломаем существующую)
    try{
      const top = document.querySelector(".topbar") || document.body;
      // ничего не трогаем, просто подсказка в сообщении
      setMsg(root, rid ? ("RID: " + shortRID(rid)) : "RID не найден", true);
    }catch(e){}
  }

  function initBridge(){
    const tab = document.querySelector('.tab[data-tab="bridge"]');
    const panel = document.getElementById("panel-bridge");
    const root = document.getElementById("bridgeRoot");
    if (!panel || !root) return;

    // рендерим при первом клике на вкладку
    if (tab && !tab.__bridgeBound){
      tab.__bridgeBound = true;
      tab.addEventListener("click", () => {
        try{ renderBridge(); }catch(e){}
      });
    }

    // если панель уже активна — рендерим сразу
    try{
      if (panel.style.display !== "none") renderBridge();
    }catch(e){}
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initBridge);
  } else {
    initBridge();
  }
})();



/* ========= SEND LGN MODULE (v2, sig_hex) ========= */
(() => {
  const NODE_API = (window.LOGOS_NODE_API || "/api").replace(/\/+$/,"");

  function q(sel, root=document){ return root.querySelector(sel); }
  function qa(sel, root=document){ return Array.from(root.querySelectorAll(sel)); }

  function utf8(s){ return new TextEncoder().encode(String(s)); }

  function hex(u8){
    let out = "";
    for (let i=0;i<u8.length;i++){
      out += u8[i].toString(16).padStart(2,"0");
    }
    return out;
  }

  function hexToU8(h){
    h = (h||"").trim().replace(/^0x/,"");
    if (!h || (h.length % 2)) return null;
    const u = new Uint8Array(h.length/2);
    for (let i=0;i<u.length;i++) u[i] = parseInt(h.substr(i*2,2),16);
    return u;
  }

  function getRID(){
    return localStorage.getItem("RID")
      || localStorage.getItem("logos_rid")
      || localStorage.getItem("logos_last_rid")
      || sessionStorage.getItem("RID")
      || "";
  }

  // пытаемся найти private Ed25519 JWK в localStorage (если ключи хранятся так)
  function findEd25519PrivJwk(){
    for (let i=0;i<localStorage.length;i++){
      const k = localStorage.key(i);
      if (!k) continue;
      const v = localStorage.getItem(k);
      if (!v || v.length < 20) continue;
      try{
        const j = JSON.parse(v);
        if (j && j.crv === "Ed25519" && j.kty && j.d && j.x) return j;
      }catch(e){}
    }
    return null;
  }

  async function importPrivKeyFromJwk(jwk){
    return crypto.subtle.importKey("jwk", jwk, {name:"Ed25519"}, false, ["sign"]);
  }

  async function signEd25519(privKey, msgU8){
    const sig = await crypto.subtle.sign({name:"Ed25519"}, privKey, msgU8);
    return new Uint8Array(sig);
  }

  async function getNonce(rid){
    const r = await fetch(`${NODE_API}/balance/${encodeURIComponent(rid)}`);
    if(!r.ok) throw new Error(`balance http ${r.status}`);
    const j = await r.json();
    return j.nonce;
  }

  async function getCanonBytes(draft){
    // пробуем debug_canon (если включен на сервере)
    try{
      const r = await fetch(`${NODE_API}/debug_canon`, {
        method:"POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(draft)
      });
      if (r.ok){
        const t = await r.text();
        // варианты: JSON или просто строка
        try{
          const j = JSON.parse(t);
          const ch = j.canon_hex || j.canon || j.msg_hex || j.message_hex || j.bytes_hex || "";
          const u = hexToU8(ch);
          if (u) return u;
          const s = (j.canon_str || j.message || j.msg || "");
          if (s) return utf8(s);
        }catch(e){
          // если просто строка
          const u = hexToU8(t);
          if (u) return u;
          if (t && t.length) return utf8(t);
        }
      }
    }catch(e){}

    // fallback: стабильная строка (если debug_canon нет)
    const memo = (draft.memo === null || draft.memo === undefined) ? "" : String(draft.memo);
    const s = `LOGOS_TX|from=${draft.from}|to=${draft.to}|amount=${draft.amount}|nonce=${draft.nonce}|memo=${memo}`;
    return utf8(s);
  }

  function setStatus(panel, text, ok=true){
    let el = q(".sendStatus", panel);
    if(!el){
      el = document.createElement("div");
      el.className = "sendStatus";
      el.style.marginTop = "10px";
      el.style.fontSize = "13px";
      el.style.opacity = "0.95";
      panel.appendChild(el);
    }
    el.textContent = text || "";
    el.style.color = ok ? "" : "#ff6b6b";
  }

  function findSendPanel(){
    return document.getElementById("panel-send")
      || document.getElementById("panel-transfer")
      || document.querySelector('.panel[data-panel="send"]')
      || null;
  }

  function findSendControls(panel){
      const btnSend = qa("button", panel).find(b => (b.textContent||"").toLowerCase().includes("send lgn"));
      const btnFillMe = qa("button", panel).find(b => (b.textContent||"").toLowerCase().includes("мой rid"));

      // ВАЖНО: не по индексу, а по id (иначе withdraw inputs ломают логику)
      const toRid  = document.getElementById("lgnTo") || document.getElementById("lgmTo") || null;
      const amount = document.getElementById("lgnAmount") || document.getElementById("lgmAmount") || null;

      // memo optional
      const memo = document.getElementById("lgnMemo") || document.getElementById("lgmMemo") || null;

      return {btnSend, btnFillMe, toRid, amount, memo};
    }

  async function handleSend(panel, ui){
    const fromRid = getRID();
    const toRid = (ui.toRid?.value || "").trim();
    const memoStr = (ui.memo?.value || "").trim();
    const amtStr = (ui.amount?.value || "").trim();

    if(!fromRid){ setStatus(panel, "ERR: нет RID (ключи не найдены).", false); return; }
    if(!toRid || toRid.length < 10){ setStatus(panel, "ERR: введи RID получателя.", false); return; }

    const amt = Number(amtStr.replace(",", "."));
    if(!isFinite(amt) || amt <= 0){ setStatus(panel, "ERR: введи сумму > 0.", false); return; }

    const amount_mic = Math.round(amt * 1e6);

    setStatus(panel, "Отправляю…", true);

    let nonce;
    try{
      nonce = await getNonce(fromRid);
    }catch(e){
      setStatus(panel, "ERR: не смог получить nonce (balance).", false);
      return;
    }

    // draft по схеме TxIn (без подписи)
    const draft = {
      from: fromRid,
      to: toRid,
      amount: amount_mic,
      nonce: nonce,
      memo: memoStr ? memoStr : None
    };

    // JS не знает None, поэтому:
    if (!memoStr) draft.memo = null;

    // bytes for signing
    const canonBytes = await getCanonBytes(draft);

    // signer
    const jwk = findEd25519PrivJwk();
    if(!jwk){
      setStatus(panel, "ERR: приватный ключ не найден (localStorage). Если ключи в IndexedDB — скажи, сделаем доступ через существующий signer.", false);
      return;
    }

    let privKey;
    try{
      privKey = ***
    }catch(e){
      setStatus(panel, "ERR: не смог импортировать Ed25519 ключ.", false);
      return;
    }

    let sigU8;
    try{
      sigU8 = await signEd25519(privKey, canonBytes);
    }catch(e){
      setStatus(panel, "ERR: не смог подписать транзакцию.", false);
      return;
    }

    const txIn = {
      from: draft.from,
      to: draft.to,
      amount: draft.amount,
      nonce: draft.nonce,
      memo: draft.memo,
      sig_hex: hex(sigU8)
    };

    try{
      const r = await fetch(`${NODE_API}/submit_tx`, {
        method:"POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(txIn)
      });
      const text = await r.text();
      if(!r.ok){
        setStatus(panel, `ERR submit_tx: ${r.status} ${text}`.slice(0,500), false);
        return;
      }
      try{
        const j = JSON.parse(text);
        if (j && j.ok){
          setStatus(panel, `✅ Отправлено. txid: ${(j.txid||"")}`.trim(), true);
        } else {
          setStatus(panel, `⚠️ Ответ: ${text}`.slice(0,500), false);
        }
      }catch(e){
        setStatus(panel, `✅ Отправлено. Ответ: ${text}`.slice(0,200), true);
      }
    }catch(e){
      setStatus(panel, "ERR: сеть/submit_tx не доступен.", false);
    }
  }

  function initSend(){
    const panel = findSendPanel();
    if(!panel) return;
    const ui = findSendControls(panel);

    if(ui.btnFillMe){
      ui.btnFillMe.addEventListener("click", () => {
        const rid = getRID();
        if(ui.toRid) ui.toRid.value = rid || "";
      });
    }
    if(ui.btnSend){
      ui.btnSend.addEventListener("click", () => handleSend(panel, ui));
    }
  }

  try{ initSend(); }catch(e){}
})();


```

## FRONT FILE: /opt/logos/www/wallet_prod/index.html

```
<!doctype html><meta charset="utf-8">
<meta http-equiv="refresh" content="0;url=./auth.html">

```

## FRONT FILE: /opt/logos/www/wallet_prod/auth.html

```
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Wallet</title>
  <link rel="stylesheet" href="./app.css"/>
  <link rel="stylesheet" href="./auth.css"/>
</head>
<body>

  <div class="authShell">
    <div class="authCard">
      <div class="authTop">
        <div class="authBrand">
          <div class="authLogo">LOGOS</div>
          <div class="authTitle">LOGOS Wallet</div>
        </div>
        <div class="authHint">HTTPS only</div>
      </div>

      <div class="authSubtitle">
        Create / Restore / Unlock — без email. Ключи локально. Сервер seed не видит.
      </div>

      <!-- STEP 0 -->
      <div id="step0" class="authStep">
        <div class="authGrid2">
          <button id="btnCreate" class="authBtn primary">Создать новый кошелёк</button>
          <button id="btnRestore" class="authBtn ghost">Восстановить по словам</button>
        </div>

        <button id="btnUnlock" class="authBtn soft" style="display:none;margin-top:12px">Unlock (продолжить)</button>

        <div class="authDivider"></div>

        <div class="authMiniTitle">Legacy вход по RID (для старых рабочих RID)</div>

        <label class="authLabel">RID</label>
        <input id="rid" class="authInp" placeholder="RID"/>

        <label class="authLabel">Пароль (legacy, если нужен)</label>
        <input id="pass" class="authInp" type="password" placeholder="Пароль"/>

        <div class="authGrid2" style="margin-top:12px">
          <button id="btnLogin" class="authBtn ghost">Войти по RID</button>
          <button id="btnShowRid" class="authBtn soft">Показать сохранённый RID</button>
        </div>

        <div id="status" class="authStatus"></div>
      </div>

      <!-- CREATE: show mnemonic -->
      <div id="mnemonicSection" class="authStep" style="display:none">
        <div class="authMiniTitle">Seed-фраза (запиши и сохрани)</div>
        <div class="authWarn">Не скринь. Не отправляй никому. Потеряешь — потеряешь доступ.</div>
        
<div class="seedBox">
  <div class="seedHead">
    <div class="seedTitle">Seed-фраза</div>
    <div class="seedActions">
      <button type="button" id="btnSeedHide" class="chipBtn">Скрыть</button>
      <button type="button" id="btnSeedCopy" class="chipBtn">Copy</button>
    </div>
  </div>

  <div class="seedWarn">
    Не делай скриншот и не отправляй никому. Потеряешь фразу — потеряешь доступ.
  </div>

  <div id="mnemonicShow" class="seedGrid" aria-label="seed phrase"></div>

  <div class="seedFoot">
    <span class="seedHint">Проверь, что записал(а) все слова по порядку.</span>
  </div>
</div>


        <div class="authGrid2" style="margin-top:12px">
          <button id="btnRecorded" class="authBtn primary">Я записал</button>
          <button id="btnBack0" class="authBtn soft">Назад</button>
        </div>
      </div>

      <!-- CONFIRM -->
      <div id="confirmSection" class="authStep" style="display:none">
        <div class="authMiniTitle">Проверка seed-фразы</div>
        <div class="authSubtitleSmall">Введи слово № <b id="cIdx"></b></div>
        <input id="confirmWord" class="authInp" placeholder="слово"/>

        <div id="cStatus" class="authStatus"></div>

        <div class="authGrid2" style="margin-top:12px">
          <button id="btnConfirmNext" class="authBtn primary">Дальше</button>
          <button id="btnBack1" class="authBtn soft">Назад</button>
        </div>
      </div>

      <!-- SET PASSWORD -->
      <div id="setPassSection" class="authStep" style="display:none">
        <div class="authMiniTitle">Защита (пароль шифрует seed локально)</div>

        <input id="p1" class="authInp" type="password" placeholder="Пароль (мин 6 символов)"/>
        <input id="p2" class="authInp" type="password" placeholder="Повтори пароль"/>

        <div id="pStatus" class="authStatus"></div>

        <div class="authGrid2" style="margin-top:12px">
          <button id="btnFinishCreate" class="authBtn primary">Создать и войти</button>
          <button id="btnBack2" class="authBtn soft">Назад</button>
        </div>
      </div>

      <!-- RESTORE -->
      <div id="restoreSection" class="authStep" style="display:none">
        <div class="authMiniTitle">Восстановление</div>
        <textarea id="restoreMnemonic" class="authInp authText" rows="4" placeholder="12/24 слова через пробел"></textarea>
        <input id="restorePass" class="authInp" type="password" placeholder="Новый пароль для vault (мин 6 символов)"/>

        <div id="rStatus" class="authStatus"></div>

        <div class="authGrid2" style="margin-top:12px">
          <button id="btnDoRestore" class="authBtn primary">Восстановить и войти</button>
          <button id="btnBackR" class="authBtn soft">Назад</button>
        </div>
      </div>

      <!-- UNLOCK -->
      <div id="unlockSection" class="authStep" style="display:none">
        <div class="authMiniTitle">Unlock</div>
        <input id="unlockPass" class="authInp" type="password" placeholder="Пароль"/>

        <div id="uStatus" class="authStatus"></div>

        <div class="authGrid2" style="margin-top:12px">
          <button id="btnDoUnlock" class="authBtn primary">Войти</button>
          <button id="btnBackU" class="authBtn soft">Назад</button>
        </div>
      </div>

    </div>
  </div>

  <script src="./vendor/nacl-fast.min.js"></script>
<script src="./vendor/wordlist_en.js"></script>
  <script src="./vendor/bip39_lite.js"></script>
<script defer src="./auth.js"></script>
</body>
</html>
```

## FRONT FILE: /opt/logos/www/wallet_prod/auth.js

```
(() => {
  const LS_VAULT = "logos_vault_v1";
  const SS_SEED  = "logos_sk_seed_b64";     // sessionStorage (seed32)
  const LS_LAST  = "logos_last_rid";
  const LS_RID1  = "RID";
  const LS_RID2  = "logos_rid";

  const $ = (id) => document.getElementById(id);

  

  // --- BIP39 (local, offline): use window.bip39lite ---
  function BIP39(){
    const b = window.bip39lite;
    if(!b) throw new Error("BIP39 not loaded: check vendor/wordlist_en.js + vendor/bip39_lite.js in auth.html");
    return b;
  }
  const show = (id) => $(id).style.display = "";
  const hide = (id) => $(id).style.display = "none";
  const go = (id) => {
    ["step0","mnemonicSection","confirmSection","setPassSection","restoreSection","unlockSection"].forEach(hide);
    show(id);
  };

  function status(el, ok, msg){
    el.textContent = msg || "";
    el.className = ok ? "status ok" : "status err";
  }

  function norm(s){ return (s||"").toLowerCase().trim().replace(/\s+/g," "); }

  function u8ToB64(u8){
    let s=""; u8.forEach(b=>s+=String.fromCharCode(b));
    return btoa(s);
  }
  function b64ToU8(b64){
    const s = atob(b64);
    const u8 = new Uint8Array(s.length);
    for(let i=0;i<s.length;i++) u8[i]=s.charCodeAt(i);
    return u8;
  }

  async function sha256(u8){
    const h = await crypto.subtle.digest("SHA-256", u8);
    return new Uint8Array(h);
  }

  async function pbkdf2Key(password, saltU8){
    const base = await crypto.subtle.importKey("raw", new TextEncoder().encode(password), "PBKDF2", false, ["deriveKey"]);
    return crypto.subtle.deriveKey(
      {name:"PBKDF2", salt:saltU8, iterations:210000, hash:"SHA-256"},
      base,
      {name:"AES-GCM", length:256},
      false,
      ["encrypt","decrypt"]
    );
  }

  async function encryptSeed32(seed32, password){
    const salt = crypto.getRandomValues(new Uint8Array(16));
    const iv   = crypto.getRandomValues(new Uint8Array(12));
    const key  = await pbkdf2Key(password, salt);
    const ctBuf = await crypto.subtle.encrypt({name:"AES-GCM", iv}, key, seed32);
    return { salt:u8ToB64(salt), iv:u8ToB64(iv), ct:u8ToB64(new Uint8Array(ctBuf)) };
  }

  async function decryptSeed32(vault, password){
    const salt = b64ToU8(vault.salt);
    const iv   = b64ToU8(vault.iv);
    const ct   = b64ToU8(vault.ct);
    const key  = await pbkdf2Key(password, salt);
    const ptBuf = await crypto.subtle.decrypt({name:"AES-GCM", iv}, key, ct);
    return new Uint8Array(ptBuf);
  }

  // Base58 (fallback RID derivation)
  function base58(u8){
    const A = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";
    let x = 0n;
    for (const b of u8) x = (x<<8n) + BigInt(b);
    let out = "";
    while (x > 0n) {
      const mod = x % 58n;
      out = A[Number(mod)] + out;
      x = x / 58n;
    }
    return out || "1";
  }

  function makeRIDFromPub(pubU8){
    // если где-то есть ваш канон — используем его
    if (typeof window.ridFromPub === "function") return window.ridFromPub(pubU8);
    if (typeof window.makeRID === "function") return window.makeRID(pubU8);
    // fallback формат похожий на текущие Atx...
    return "Atx" + base58(pubU8).slice(0, 44);
  }

  function setRidSession(rid){
    rid = (rid||"").trim();
    if (!rid) return;
    localStorage.setItem(LS_RID1, rid);
    localStorage.setItem(LS_RID2, rid);
    localStorage.setItem(LS_LAST, rid);
    $("rid").value = rid;
  }

  function goWallet(){
    location.href = "./app.html#assets";
  }

  // ---------- Create flow ----------
  let mnemonic = "";

  // --- Premium seed renderer (chips + copy/hide) ---
  function renderSeed(wordsArr){
    const el = $("mnemonicShow");
    if(!el) return;
    el.innerHTML = wordsArr.map((w,i)=>(
      `<div class="seedWord"><div class="seedNum">${i+1}</div><div class="seedText">${w}</div></div>`
    )).join("");
    // default visible
    el.classList.remove("isHidden");
    const b = $("btnSeedHide");
    if (b) b.textContent = "Скрыть";
  }

  function bindSeedActions(){
    const btnCopy = $("btnSeedCopy");
    if (btnCopy && !btnCopy.__bound){
      btnCopy.__bound = true;
      btnCopy.addEventListener("click", async ()=>{
        try{
          if(!mnemonic) return;
          await navigator.clipboard.writeText(mnemonic);
          btnCopy.textContent = "Скопировано";
          setTimeout(()=>btnCopy.textContent="Copy", 900);
        }catch(e){
          console.warn("copy failed", e);
          btnCopy.textContent = "Не удалось";
          setTimeout(()=>btnCopy.textContent="Copy", 900);
        }
      });
    }

    const btnHide = $("btnSeedHide");
    if (btnHide && !btnHide.__bound){
      btnHide.__bound = true;
      btnHide.addEventListener("click", ()=>{
        const el = $("mnemonicShow");
        if(!el) return;
        const on = !el.classList.contains("isHidden");
        el.classList.toggle("isHidden", on);
        btnHide.textContent = on ? "Показать" : "Скрыть";
      });
    }
  }


  let words = [];
  let checkIdx = [];
  let pos = 0;

  async function startCreate(){
    mnemonic = ***
    words = mnemonic.split(" ");
    renderSeed(words);
      bindSeedActions();
checkIdx = [3, 11, 17].map(i => Math.min(i, words.length-1));
    pos = 0;
    $("cIdx").textContent = String(checkIdx[pos] + 1);
    $("confirmWord").value = "";
    $("cStatus").textContent = "";

    go("mnemonicSection");
  }

  function startConfirm(){
    $("confirmWord").value = "";
    $("cStatus").textContent = "";
    $("cIdx").textContent = String(checkIdx[pos] + 1);
    go("confirmSection");
  }

  function doConfirmNext(){
    const w = norm($("confirmWord").value);
    const idx = checkIdx[pos];
    if (w !== words[idx]) {
      status($("cStatus"), false, "Неверно. Проверь слово.");
      return;
    }
    pos++;
    if (pos >= checkIdx.length) {
      go("setPassSection");
      return;
    }
    status($("cStatus"), true, "OK");
    $("confirmWord").value = "";
    $("cIdx").textContent = String(checkIdx[pos] + 1);
  }

  async function finishCreate(){
    const p1 = $("p1").value || "";
    const p2 = $("p2").value || "";
    if (p1.length < 6) return status($("pStatus"), false, "Пароль минимум 6 символов");
    if (p1 !== p2) return status($("pStatus"), false, "Пароли не совпадают");

    status($("pStatus"), true, "Создаю…");

    const seedBuf = await BIP39().mnemonicToSeed32(mnemonic, "");
    const seedU8  = new Uint8Array(seedBuf);

    const seed32 = await sha256(seedU8);                 // 32 bytes
    const kp = nacl.sign.keyPair.fromSeed(seed32);
    const rid = makeRIDFromPub(kp.publicKey);

    const enc = await encryptSeed32(seed32, p1);

    const vault = {
      ver: 1,
      rid,
      pub: u8ToB64(kp.publicKey),
      ...enc,
      created_at: new Date().toISOString()
    };
    localStorage.setItem(LS_VAULT, JSON.stringify(vault));

    sessionStorage.setItem(SS_SEED, u8ToB64(seed32));
    setRidSession(rid);

    goWallet();
  }

  // ---------- Restore flow ----------
  async function doRestore(){
    const m = norm($("restoreMnemonic").value);
    const pass = $("restorePass").value || "";
    if (!await BIP39().validateMnemonic(m)) return status($("rStatus"), false, "Фраза некорректная (проверь слова/пробелы)");
    if (pass.length < 6) return status($("rStatus"), false, "Пароль минимум 6 символов");

    status($("rStatus"), true, "Восстанавливаю…");

    const seedBuf = await BIP39().mnemonicToSeed32(m, "");
    const seedU8  = new Uint8Array(seedBuf);
    const seed32  = await sha256(seedU8);

    const kp = nacl.sign.keyPair.fromSeed(seed32);
    const rid = makeRIDFromPub(kp.publicKey);

    const enc = await encryptSeed32(seed32, pass);
    const vault = {
      ver: 1,
      rid,
      pub: u8ToB64(kp.publicKey),
      ...enc,
      created_at: new Date().toISOString()
    };
    localStorage.setItem(LS_VAULT, JSON.stringify(vault));

    sessionStorage.setItem(SS_SEED, u8ToB64(seed32));
    setRidSession(rid);

    goWallet();
  }

  // ---------- Unlock flow ----------
  async function doUnlock(){
    let v = null;
    try { v = JSON.parse(localStorage.getItem(LS_VAULT) || "null"); } catch(_){}
    if (!v || !v.ct) return status($("uStatus"), false, "Vault не найден");
    const pass = $("unlockPass").value || "";
    if (pass.length < 6) return status($("uStatus"), false, "Пароль минимум 6 символов");

    status($("uStatus"), true, "Unlock…");
    try{
      const seed32 = await decryptSeed32(v, pass);
      sessionStorage.setItem(SS_SEED, u8ToB64(seed32));
      setRidSession(v.rid || "");
      goWallet();
    } catch(e){
      status($("uStatus"), false, "Неверный пароль или vault повреждён");
    }
  }

  // ---------- Legacy RID login ----------
  function legacyLogin(){
    const rid = ($("rid").value || "").trim();
    if (!rid) return status($("status"), false, "Введите RID");
    setRidSession(rid);
    status($("status"), true, "OK");
    goWallet();
  }

  function showSavedRid(){
    const rid = (localStorage.getItem(LS_RID2) || localStorage.getItem(LS_RID1) || localStorage.getItem(LS_LAST) || "").trim();
    if (!rid) return status($("status"), false, "RID не найден в браузере");
    $("rid").value = rid;
    status($("status"), true, "RID подставлен из браузера");
  }

  // init
  document.addEventListener("DOMContentLoaded", () => {
    // если vault есть — показываем Unlock кнопку
    try{
      const v = JSON.parse(localStorage.getItem(LS_VAULT) || "null");
      if (v && v.ct) $("btnUnlock").style.display = "";
    }catch(_){}

    $("btnCreate").onclick = startCreate;
    $("btnRestore").onclick = () => go("restoreSection");
    $("btnUnlock").onclick  = () => go("unlockSection");

    $("btnRecorded").onclick = startConfirm;
    $("btnConfirmNext").onclick = doConfirmNext;
    $("btnFinishCreate").onclick = () => finishCreate().catch(e => status($("pStatus"), false, "ERR: " + (e.message||String(e))));

    $("btnDoRestore").onclick = () => doRestore().catch(e => status($("rStatus"), false, "ERR: " + (e.message||String(e))));
    $("btnDoUnlock").onclick  = () => doUnlock().catch(e => status($("uStatus"), false, "ERR: " + (e.message||String(e))));

    $("btnBack0").onclick = () => go("step0");
    $("btnBack1").onclick = () => go("mnemonicSection");
    $("btnBack2").onclick = () => go("confirmSection");
    $("btnBackR").onclick = () => go("step0");
    $("btnBackU").onclick = () => go("step0");

    $("btnLogin").onclick = legacyLogin;
    $("btnShowRid").onclick = showSavedRid;

    // автоподстановка RID
    const rid = (localStorage.getItem(LS_RID2) || localStorage.getItem(LS_RID1) || localStorage.getItem(LS_LAST) || "").trim();
    if (rid) $("rid").value = rid;
  });
})();

```

## FRONT FILE: /opt/logos/www/wallet_prod/auth.css

```
/* Premium auth skin (matches dark wallet vibe) */

:root{
  --bg1:#070815;
  --bg2:#0b0f2a;
  --card:#0b0f1f;
  --card2:#0a0d1a;
  --stroke: rgba(255,255,255,.10);
  --stroke2: rgba(255,255,255,.06);
  --txt: rgba(255,255,255,.92);
  --muted: rgba(255,255,255,.62);
  --muted2: rgba(255,255,255,.45);
  --ok: rgba(120,255,200,.95);
  --err: rgba(255,120,120,.95);
}

html,body{height:100%}
body{
  margin:0;
  color:var(--txt);
  background:
    radial-gradient(1200px 600px at 25% 0%, rgba(120,90,255,.25), transparent 60%),
    radial-gradient(900px 500px at 80% 10%, rgba(0,200,255,.18), transparent 55%),
    linear-gradient(180deg, var(--bg1), var(--bg2));
  font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
}

.authShell{
  min-height:100%;
  display:flex;
  align-items:flex-start;
  justify-content:center;
  padding: 48px 18px;
}

.authCard{
  width: min(560px, 100%);
  background: linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.03));
  border: 1px solid var(--stroke);
  border-radius: 22px;
  padding: 18px 18px 16px;
  box-shadow: 0 30px 90px rgba(0,0,0,.55);
  backdrop-filter: blur(10px);
}

.authTop{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:12px;
}

.authBrand{display:flex; align-items:center; gap:12px;}
.authLogo{
  width:44px;height:44px;border-radius:14px;
  display:flex;align-items:center;justify-content:center;
  background: radial-gradient(circle at 30% 30%, rgba(255,255,255,.22), rgba(255,255,255,.06));
  border: 1px solid var(--stroke2);
  letter-spacing: .6px;
  font-weight: 800;
}
.authTitle{font-weight:800; font-size:18px; letter-spacing:.3px;}
.authHint{font-size:12px; color:var(--muted2); border:1px solid var(--stroke2); padding:6px 10px; border-radius:999px;}

.authSubtitle{
  margin-top:10px;
  color:var(--muted);
  font-size:13px;
  line-height:1.45;
}
.authSubtitleSmall{margin-top:8px; color:var(--muted); font-size:13px;}

.authDivider{
  height:1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,.10), transparent);
  margin: 16px 0 14px;
}

.authMiniTitle{
  font-size:13px;
  color: rgba(255,255,255,.78);
  margin-bottom:10px;
}

.authLabel{display:block; font-size:12px; color:var(--muted2); margin:10px 0 6px;}

.authInp{
  width:100%;
  box-sizing:border-box;
  background: rgba(0,0,0,.22);
  border: 1px solid var(--stroke2);
  border-radius: 14px;
  padding: 12px 12px;
  outline:none;
  color: var(--txt);
}
.authInp:focus{
  border-color: rgba(140,160,255,.35);
  box-shadow: 0 0 0 3px rgba(120,120,255,.12);
}

.authText{resize:vertical; min-height:120px;}

.authGrid2{
  display:grid;
  grid-template-columns: 1fr 1fr;
  gap:10px;
}

.authBtn{
  width:100%;
  border-radius: 14px;
  padding: 11px 12px;
  border:1px solid var(--stroke2);
  cursor:pointer;
  color: var(--txt);
  background: rgba(255,255,255,.06);
  transition: transform .08s ease, background .12s ease, border-color .12s ease;
}
.authBtn:hover{transform: translateY(-1px); border-color: rgba(255,255,255,.14);}
.authBtn:active{transform: translateY(0px);}

.authBtn.primary{
  background: linear-gradient(90deg, rgba(120,90,255,.55), rgba(0,200,255,.35));
  border-color: rgba(255,255,255,.16);
}
.authBtn.ghost{
  background: rgba(0,0,0,.20);
}
.authBtn.soft{
  background: rgba(255,255,255,.04);
  color: rgba(255,255,255,.86);
}

.authStatus{
  margin-top:10px;
  font-size:13px;
  color: var(--muted);
  min-height: 18px;
}

.authWarn{
  margin-top:10px;
  background: rgba(255,180,80,.10);
  border:1px solid rgba(255,180,80,.20);
  color: rgba(255,220,180,.92);
  padding: 10px 12px;
  border-radius: 14px;
  font-size: 13px;
}

.authMnemonic{
  margin-top:10px;
  background: rgba(0,0,0,.22);
  border: 1px solid var(--stroke2);
  border-radius: 14px;
  padding: 12px;
  white-space: pre-wrap;
  word-break: break-word;
  font-size: 14px;
  line-height: 1.55;
}

/* ===== Premium Seed UI (top-wallet style) ===== */

.seedBox{
  margin-top: 14px;
  padding: 14px;
  border-radius: 16px;
  border: 1px solid var(--stroke2);
  background: linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.03));
}

.seedHead{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap: 10px;
  margin-bottom: 10px;
}

.seedTitle{
  font-weight: 700;
  letter-spacing: .2px;
}

.seedActions{
  display:flex;
  gap: 8px;
}

.chipBtn{
  appearance: none;
  border: 1px solid var(--stroke2);
  background: rgba(255,255,255,.05);
  color: var(--txt);
  border-radius: 999px;
  padding: 8px 12px;
  font-size: 13px;
  cursor: pointer;
}
.chipBtn:hover{ background: rgba(255,255,255,.08); }

.seedWarn{
  border: 1px solid rgba(255,200,120,.25);
  background: rgba(255,170,80,.08);
  color: rgba(255,235,210,.92);
  border-radius: 12px;
  padding: 10px 12px;
  font-size: 13px;
  line-height: 1.4;
  margin-bottom: 12px;
}

.seedGrid{
  display:grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
}

.seedWord{
  user-select: none;
  display:flex;
  align-items:center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid var(--stroke2);
  background: rgba(0,0,0,.22);
  overflow:hidden;
}

.seedNum{
  width: 26px;
  height: 26px;
  border-radius: 9px;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size: 12px;
  color: rgba(255,255,255,.75);
  background: rgba(255,255,255,.06);
  flex: 0 0 auto;
}

.seedText{
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 13px;
  color: rgba(255,255,255,.92);
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
}

.seedGrid.isHidden .seedText{
  color: transparent;
  text-shadow: 0 0 10px rgba(255,255,255,.35);
}

.seedFoot{
  margin-top: 10px;
  display:flex;
  justify-content:space-between;
  gap: 10px;
  color: var(--muted);
  font-size: 12.5px;
}

@media (max-width: 720px){
  .seedGrid{ grid-template-columns: repeat(2, minmax(0, 1fr)); }
}

```

## FRONT TREE modules/: /opt/logos/www/wallet_prod/modules

```
/opt/logos/www/wallet_prod/modules/
  lgn_send.js
  lgn_send.js.bad_20260113T164615Z
  send.js
  settings.js
  tx_redirect.js

```

## FRONT MODULE FILE: /opt/logos/www/wallet_prod/modules/lgn_send.js

```
/* LGN send via /node-api/submit_tx
   Uses sessionStorage logos_sk_seed_b64 (seed32) + tweetnacl ed25519
*/
(() => {
  const NODE_API = `${location.origin}/node-api`;
  const SS_SEED = "logos_sk_seed_b64";

  const byId = (id)=>document.getElementById(id);
  const pick = (...ids)=>ids.map(byId).find(Boolean);

  function setStatus(ok, msg){
    const el = pick("lgnStatus","sendStatus","statusLGN");
    if (el){ el.textContent = msg||""; el.className = ok ? "status ok" : "status err"; }
  }

  function b64ToU8(b64){
    const s = atob(b64);
    const u8 = new Uint8Array(s.length);
    for(let i=0;i<s.length;i++) u8[i]=s.charCodeAt(i);
    return u8;
  }

  function u8tohex(u8){
    return Array.from(u8).map(b=>b.toString(16).padStart(2,"0")).join("");
  }

  function readRID(){
    return (localStorage.getItem("logos_rid") || localStorage.getItem("RID") || "").trim();
  }

  function readToRid(){
    // В твоём UI это именно lgmTo
    const el = pick("lgmTo","lgnTo","toRid","to");
    return (el?.value || "").trim();
  }

  function parseAmountMicro(){
    const el = pick("lgmAmount","lgnAmount","amountLGN","amount");
    const s0 = (el?.value || "").trim().replace(",",".");
    if (!s0) throw new Error("Введите Amount");
    if (!/^\d+(\.\d+)?$/.test(s0)) throw new Error("Некорректный Amount");
    const [a,b=""] = s0.split(".");
    const frac = (b+"000000").slice(0,6);
    const micro = BigInt(a)*1000000n + BigInt(frac);
    if (micro<=0n) throw new Error("Amount должен быть > 0");
    return micro;
  }

  async function getJSON(url){
    const r = await fetch(url,{cache:"no-store",credentials:"omit"});
    const t = await r.text();
    if (!r.ok) throw new Error(`${r.status} ${t}`.slice(0,300));
    try { return JSON.parse(t); } catch { return t; }
  }

  async function postJSON(url, body){
    const r = await fetch(url,{
      method:"POST",
      headers:{"content-type":"application/json"},
      body: JSON.stringify(body),
      cache:"no-store",
      credentials:"omit"
    });
    const t = await r.text();
    if (!r.ok) throw new Error(`${r.status} ${t}`.slice(0,600));
    try { return JSON.parse(t); } catch { return t; }
  }

  async function getNextNonce(rid){
    const j = await getJSON(`${NODE_API}/balance/${encodeURIComponent(rid)}`);
    const raw = (j && typeof j==="object" && (j.next_nonce ?? j.nonce ?? j.seq ?? j.sequence));
    if (raw===undefined || raw===null) throw new Error("В /balance нет nonce/next_nonce");
    const bn = BigInt(raw);
    // если отдаёте next_nonce — берём как есть, если nonce — добавим 1
    if (j && typeof j==="object" && j.next_nonce !== undefined) return bn;
    return bn + 1n;
  }

  function canonicalBytes(tx){
    const o = {from:tx.from,to:tx.to,amount:tx.amount,nonce:tx.nonce,memo:tx.memo??null};
    return new TextEncoder().encode(JSON.stringify(o));
  }

  async function sendLGN(){
    try{
      const from = readRID();
      if (!from) throw new Error("Нет RID. Сначала Create/Restore/Unlock или Legacy login.");
      const to = readToRid();
      if (!to) throw new Error("Введите RID получателя.");

      const seedB64 = sessionStorage.getItem(SS_SEED);
      if (!seedB64) throw new Error("Ключ не разблокирован. Вернись на старт и сделай Unlock.");
      if (!window.nacl) throw new Error("tweetnacl не загружен (проверь app.html).");

      const seed32 = b64ToU8(seedB64);
      const kp = nacl.sign.keyPair.fromSeed(seed32);

      const amount = parseAmountMicro();
      const nonce = await getNextNonce(from);

      const tx = { from, to, amount: amount.toString(), nonce: nonce.toString(), memo: null };
      const msg = canonicalBytes(tx);
      const sig = nacl.sign.detached(new Uint8Array(msg), kp.secretKey);

      const body = { ...tx, sig_hex: u8tohex(sig) };
      setStatus(true, "sending…");
      const res = await postJSON(`${NODE_API}/submit_tx`, body);
      setStatus(true, "OK: tx submitted");
      console.log("[lgn_send] submit result:", res);
    }catch(e){
      setStatus(false, "ERR: " + (e.message||String(e)));
      console.warn(e);
    }
  }

  function bind(){
    // найдём кнопку “Send LGN”
    const btn = [...document.querySelectorAll("button")].find(b => /send\s*lgn/i.test(b.textContent||""));
    if (!btn) { console.warn("[lgn_send] button not found"); return; }
    btn.addEventListener("click", (ev)=>{ ev.preventDefault(); sendLGN(); }, true);
    console.log("[lgn_send] ready (seed vault mode)");
  }

  if (document.readyState==="loading") document.addEventListener("DOMContentLoaded", bind);
  else bind();
})();

```

## FRONT MODULE FILE: /opt/logos/www/wallet_prod/modules/send.js

```
(function(){
  const $ = (id) => document.getElementById(id);

  function esc(s){
    return String(s ?? "")
      .replaceAll("&","&amp;")
      .replaceAll("<","&lt;")
      .replaceAll(">","&gt;")
      .replaceAll('"',"&quot;")
      .replaceAll("'","&#039;");
  }

  function readRID(){
    try{
      return (localStorage.getItem("RID") || localStorage.getItem("logos_rid") || "").trim();
    }catch(e){ return ""; }
  }

  function setStatus(msg){
    const el = $("wdStatus");
    if (el) el.textContent = msg || "";
  }

  function setRaw(obj){
    const pre = $("wdRaw");
    if (!pre) return;
    try{ pre.textContent = JSON.stringify(obj, null, 2); }
    catch(e){ pre.textContent = String(obj); }
  }

  function fillNetworkOptionsFromBalances(balJson){
    const sel = $("wdNetwork");
    if (!sel) return;

    const b = (balJson && balJson.balances) ? balJson.balances : {};
    const opts = [];

    // Withdraw у нас "USDT". Реальные сети вывода: ERC20 (ETH) и TRC20 (TRON)
    if (b.ETH)  opts.push({v:"ETH",  t:"ETH (ERC20)"});
    if (b.TRON) opts.push({v:"TRON", t:"TRON (TRC20)"});

    // fallback если вдруг API не дал balances
    if (opts.length === 0) opts.push({v:"ETH", t:"ETH (ERC20)"});

    const cur = sel.value;
    sel.innerHTML = "";
    for (const o of opts){
      const opt = document.createElement("option");
      opt.value = o.v;
      opt.textContent = o.t;
      sel.appendChild(opt);
    }
    if (cur && [...sel.options].some(x => x.value === cur)) sel.value = cur;
  }

  async function refreshNetworks(){
    try{
      const rid = readRID();
      if (!rid) return;

      const base = window.WALLET_API || "/wallet-api";
      const r = await fetch(base + "/v1/balances/" + encodeURIComponent(rid), { cache: "no-store" });
      if (!r.ok) return;
      const j = await r.json();
      fillNetworkOptionsFromBalances(j);
    }catch(e){}
  }

  function clearForm(){
    if ($("wdAmount")) $("wdAmount").value = "";
    if ($("wdTo")) $("wdTo").value = "";
    setStatus("");
    setRaw("");
  }

  async function doWithdraw(){
    const rid = readRID();
    if (!rid) return setStatus("ERR: RID не найден. Зайди через /wallet/auth.html");

    const base = window.WALLET_API || "/wallet-api";

    const net = ($("wdNetwork") && $("wdNetwork").value) ? $("wdNetwork").value : "ETH";
    const amountStr = String(($("wdAmount") && $("wdAmount").value) || "").trim();
    const to = String(($("wdTo") && $("wdTo").value) || "").trim();

    if (!amountStr) return setStatus("ERR: введи Amount (целое число).");
    if (!/^\d+$/.test(amountStr)) return setStatus("ERR: Amount должен быть целым числом (integer).");
    const amount = Number(amountStr);
    if (!Number.isFinite(amount) || amount <= 0) return setStatus("ERR: Amount должен быть > 0.");

    if (!to || to.length < 8) return setStatus("ERR: введи адрес получателя.");

    setStatus("request…");
    setRaw("");

    try{
      const body = { rid, network: net, amount, to };

      const r = await fetch(base + "/v1/withdraw", {
        method: "POST",
        headers: { "content-type":"application/json" },
        body: JSON.stringify(body),
        cache: "no-store"
      });

      const j = await r.json().catch(()=>({}));
      setRaw(j);

      if (!r.ok){
        return setStatus("ERR: HTTP " + r.status + " — " + (j && (j.error || j.message) ? (j.error || j.message) : "withdraw failed"));
      }

      setStatus("OK: отправлено (" + esc(net) + ").");
    }catch(e){
      setStatus("ERR: " + (e && e.message ? e.message : String(e)));
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    refreshNetworks();

    const btnSend = $("btnWithdraw");
    const btnClear = $("btnWithdrawClear");

    if (btnSend) btnSend.addEventListener("click", doWithdraw);
    if (btnClear) btnClear.addEventListener("click", clearForm);

    // enter = send (в поле адреса)
    const to = $("wdTo");
    if (to){
      to.addEventListener("keydown", (e) => {
        if (e.key === "Enter") doWithdraw();
      });
    }
  });
})();

```

## FRONT MODULE FILE: /opt/logos/www/wallet_prod/modules/settings.js

```
/* ===== LOGOS Wallet: Settings module (v1) ===== */
(() => {
  const LS_DEV = "logos_dev_mode";

  const $$ = (sel, root=document) => Array.from(root.querySelectorAll(sel));
  const $  = (sel, root=document) => root.querySelector(sel);

  function ridGet(){
    return (
      localStorage.getItem("RID") ||
      localStorage.getItem("logos_rid") ||
      sessionStorage.getItem("RID") ||
      sessionStorage.getItem("logos_rid") ||
      ""
    );
  }

  function devGet(){ return (localStorage.getItem(LS_DEV) === "1"); }
  function devSet(v){ localStorage.setItem(LS_DEV, v ? "1" : "0"); }

  function markDevOnly(){
    // 1) прячем все Details/raw блоки
    $$("details").forEach(d => {
      const t = (d.textContent || "").toLowerCase();
      const s = ($("summary", d)?.textContent || "").toLowerCase();
      if (t.includes("raw") || s.includes("details") || s.includes("raw") || t.includes("wallet-api raw")) {
        d.classList.add("devOnly");
      }
    });

    // 2) прячем pre/json дампы если есть
    $$("pre").forEach(p => {
      const t = (p.textContent || "").toLowerCase();
      if (t.includes("{") && (t.includes("rid") || t.includes("addresses") || t.includes("balances"))) {
        p.classList.add("devOnly");
      }
    });

    // 3) прячем любые элементы, где прямо написано "raw"
    $$("*").forEach(el => {
      const t = (el.textContent || "").toLowerCase();
      if (t.trim() === "details (raw)" || t.trim() === "details (wallet-api raw)" ) {
        el.classList.add("devOnly");
      }
    });
  }

  function applyDev(){
    const dev = devGet();
    document.documentElement.classList.toggle("dev", dev);

    // если у нас уже проставлены devOnly — CSS сделает остальное
    markDevOnly();

    // bridge: заменяем страшные сообщения для обычных людей
    const bridgePanel = document.getElementById("panel-bridge");
    if (bridgePanel){
      const msg = bridgePanel.querySelector(".bridgeMsg");
      if (msg){
        const txt = (msg.textContent || "");
        if (!dev && (txt.includes("HOT wallet not configured") || txt.includes('"detail"'))){
          msg.textContent = "Top up / Withdraw временно недоступны (временно).";
        }
      }
    }
  }

  function downloadJSON(filename, obj){
    const blob = new Blob([JSON.stringify(obj, null, 2)], {type:"application/json"});
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  function clearWalletStorage(){
    // аккуратно удаляем только наши ключи
    const keys = [
      "RID","logos_rid","rid","logosRID",
      "logos_key","logos_priv","logos_pub",
      "wallet_key","wallet_priv","wallet_pub",
      "logos_token","logos_auth",
      "logos_wallet","logos_state",
      "LOGOS_WALLET","LOGOS_STATE",
    ];
    keys.forEach(k => { try{ localStorage.removeItem(k); }catch(e){} });
    keys.forEach(k => { try{ sessionStorage.removeItem(k); }catch(e){} });

    // удаляем всё, что начинается с logos_
    try{
      for (let i=localStorage.length-1;i>=0;i--){
        const k = localStorage.key(i);
        if (k && (k.startsWith("logos_") || k.startsWith("LOGOS_"))) localStorage.removeItem(k);
      }
    }catch(e){}
    try{
      for (let i=sessionStorage.length-1;i>=0;i--){
        const k = sessionStorage.key(i);
        if (k && (k.startsWith("logos_") || k.startsWith("LOGOS_"))) sessionStorage.removeItem(k);
      }
    }catch(e){}
  }

  function renderSettings(){
    const panel = document.getElementById("panel-settings");
    if (!panel) return;

    panel.innerHTML = `
      <div class="card">
        <div class="h">Настройки</div>
        <div class="muted">Ключи живут локально в браузере. Сервер видит только подписанные операции.</div>

        <div style="height:12px"></div>

        <div class="kvRow">
          <div>
            <div class="k">Dev mode</div>
            <div class="v muted">Скрывает/показывает технические детали (raw, debug, тексты ошибок).</div>
          </div>
          <label class="switch">
            <input type="checkbox" id="devToggle">
            <span class="slider"></span>
          </label>
        </div>

        <div style="height:14px"></div>

        <div class="card" style="padding:14px">
          <div class="h">Локальные данные</div>
          <div class="muted">RID/ключи/состояние хранятся в localStorage.</div>

          <div style="height:10px"></div>

          <div class="btnRow">
            <button class="btn" id="btnCopyRID">Скопировать RID</button>
            <button class="btn" id="btnExport">Экспорт бэкапа</button>
            <button class="btn danger" id="btnClear">Очистить локальные данные</button>
          </div>

          <div class="muted" style="margin-top:10px" id="settingsNote"></div>
        </div>

        <div style="height:12px"></div>

        <div class="card devOnly" style="padding:14px">
          <div class="h">Dev info</div>
          <div class="muted">Только для тебя.</div>
          <div style="height:10px"></div>
          <pre id="devDump" style="white-space:pre-wrap;margin:0"></pre>
        </div>
      </div>
    `;

    const devToggle = panel.querySelector("#devToggle");
    const note = panel.querySelector("#settingsNote");
    const dump = panel.querySelector("#devDump");

    devToggle.checked = devGet();
    devToggle.addEventListener("change", () => {
      devSet(devToggle.checked);
      applyDev();
      note.textContent = devToggle.checked ? "Dev mode включён." : "Dev mode выключен (обычный режим).";
      // обновим devDump
      const rid = ridGet();
      dump.textContent = JSON.stringify({
        rid,
        origin: window.location.origin,
        api: (window.LOGOS_NODE_API || window.API_BASE || "/api"),
        wallet_api: (window.LOGOS_WALLET_API || window.WALLET_API || "/wallet-api"),
        dev_mode: devGet(),
        localStorage_keys: Object.keys(localStorage || {}).slice(0, 50)
      }, null, 2);
    });

    panel.querySelector("#btnCopyRID").addEventListener("click", async () => {
      const rid = ridGet();
      if (!rid) return (note.textContent = "RID не найден. Войди в кошелёк.");
      try{
        await navigator.clipboard.writeText(rid);
        note.textContent = "RID скопирован.";
      }catch(e){
        note.textContent = "Не удалось скопировать (браузер запретил).";
      }
    });

    panel.querySelector("#btnExport").addEventListener("click", () => {
      const rid = ridGet();
      const payload = {
        rid,
        exported_at: new Date().toISOString(),
        origin: window.location.origin,
        // сохраняем только безопасные вещи — без “сырых приватников”
        // (если приватники где-то лежат — лучше не выгружать в файл автоматически)
        hints: {
          note: "Это бэкап RID/настроек. Приватные ключи не экспортируются автоматически."
        }
      };
      const fn = `logos_wallet_backup_${Date.now()}.json`;
      downloadJSON(fn, payload);
      note.textContent = "Бэкап скачан.";
    });

    panel.querySelector("#btnClear").addEventListener("click", () => {
      const ok = confirm("Точно очистить локальные данные кошелька на этом устройстве? RID/ключи в браузере будут удалены.");
      if (!ok) return;
      clearWalletStorage();
      note.textContent = "Очищено. Перезагружаю…";
      setTimeout(() => location.reload(), 600);
    });

    // init view
    applyDev();
    note.textContent = devGet() ? "Dev mode включён." : "Dev mode выключен (обычный режим).";
    const rid = ridGet();
    dump.textContent = JSON.stringify({
      rid,
      origin: window.location.origin,
      api: (window.LOGOS_NODE_API || window.API_BASE || "/api"),
      wallet_api: (window.LOGOS_WALLET_API || window.WALLET_API || "/wallet-api"),
      dev_mode: devGet(),
    }, null, 2);

    // обновление bridge сообщений при изменениях (MutationObserver)
    const bridgePanel = document.getElementById("panel-bridge");
    if (bridgePanel){
      const obs = new MutationObserver(() => applyDev());
      obs.observe(bridgePanel, {subtree:true, childList:true, characterData:true});
    }
  }

  // старт
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderSettings);
  } else {
    renderSettings();
  }
})();


// PROD hard clear session password
try{sessionStorage.removeItem("PASS");sessionStorage.removeItem("logos_pass");}catch(e){}

```

## FRONT MODULE FILE: /opt/logos/www/wallet_prod/modules/tx_redirect.js

```
/* tx_redirect.js — redirect old /transfer -> /submit_tx and normalize body to TxIn */
(() => {
  const _fetch = window.fetch.bind(window);

  function isHex(s){
    s = String(s||"").replace(/^0x/,"").trim();
    return s.length > 0 && s.length % 2 === 0 && /^[0-9a-fA-F]+$/.test(s);
  }

  function b64urlToBytes(b64url){
    try{
      let s = String(b64url||"").replace(/-/g,'+').replace(/_/g,'/');
      while (s.length % 4) s += '=';
      const bin = atob(s);
      const u = new Uint8Array(bin.length);
      for (let i=0;i<bin.length;i++) u[i] = bin.charCodeAt(i);
      return u;
    }catch(e){ return null; }
  }

  function bytesToHex(u){
    let out = "";
    for (let i=0;i<u.length;i++) out += u[i].toString(16).padStart(2,"0");
    return out;
  }

  function normalizeTx(body){
    const j = body && typeof body === "object" ? body : {};
    const from = j.from || j.rid_from || j.sender || j.rid || "";
    const to   = j.to   || j.rid_to   || j.receiver || "";
    let amount = j.amount_mic ?? j.amount_micro ?? j.amount ?? 0;
    const nonce = j.nonce ?? j.n ?? j.account_nonce;

    // если вдруг прислали amount_lgn — переводим в micro-LGN
    if (j.amount_lgn !== undefined && j.amount_lgn !== null){
      const a = Number(j.amount_lgn);
      if (isFinite(a)) amount = Math.round(a * 1e6);
    }

    // подпись: sig_hex обязательно
    let sig_hex = j.sig_hex || j.sigHex || "";
    if (!sig_hex){
      const s = j.sig || j.signature || j.sig_b64 || j.sigB64 || "";
      if (s){
        if (isHex(s)) sig_hex = String(s).replace(/^0x/,"");
        else {
          const u = b64urlToBytes(s);
          if (u) sig_hex = bytesToHex(u);
        }
      }
    }

    const memo = (j.memo === undefined ? null : j.memo);

    return { from, to, amount, nonce, memo, sig_hex };
  }

  window.fetch = async (input, init={}) => {
    try{
      const url = (typeof input === "string") ? input : (input && input.url ? input.url : "");
      if (url.includes("/transfer")){
        const newUrl = url.replace("/transfer", "/submit_tx");

        let bodyObj = {};
        try{ bodyObj = JSON.parse(init.body || "{}"); }catch(e){ bodyObj = {}; }

        const tx = normalizeTx(bodyObj);

        const newInit = {
          ...init,
          method: "POST",
          headers: { ...(init.headers||{}), "Content-Type":"application/json" },
          body: JSON.stringify({
            from: tx.from,
            to: tx.to,
            amount: tx.amount,
            nonce: tx.nonce,
            memo: tx.memo,
            sig_hex: tx.sig_hex
          })
        };

        return _fetch(newUrl, newInit);
      }
    }catch(e){}
    return _fetch(input, init);
  };

  console.log("[tx_redirect] installed: /transfer -> /submit_tx");
})();

```

## FRONT LGN_SEND: /opt/logos/www/wallet_prod/modules/lgn_send.js

```
/* LGN send via /node-api/submit_tx
   Uses sessionStorage logos_sk_seed_b64 (seed32) + tweetnacl ed25519
*/
(() => {
  const NODE_API = `${location.origin}/node-api`;
  const SS_SEED = "logos_sk_seed_b64";

  const byId = (id)=>document.getElementById(id);
  const pick = (...ids)=>ids.map(byId).find(Boolean);

  function setStatus(ok, msg){
    const el = pick("lgnStatus","sendStatus","statusLGN");
    if (el){ el.textContent = msg||""; el.className = ok ? "status ok" : "status err"; }
  }

  function b64ToU8(b64){
    const s = atob(b64);
    const u8 = new Uint8Array(s.length);
    for(let i=0;i<s.length;i++) u8[i]=s.charCodeAt(i);
    return u8;
  }

  function u8tohex(u8){
    return Array.from(u8).map(b=>b.toString(16).padStart(2,"0")).join("");
  }

  function readRID(){
    return (localStorage.getItem("logos_rid") || localStorage.getItem("RID") || "").trim();
  }

  function readToRid(){
    // В твоём UI это именно lgmTo
    const el = pick("lgmTo","lgnTo","toRid","to");
    return (el?.value || "").trim();
  }

  function parseAmountMicro(){
    const el = pick("lgmAmount","lgnAmount","amountLGN","amount");
    const s0 = (el?.value || "").trim().replace(",",".");
    if (!s0) throw new Error("Введите Amount");
    if (!/^\d+(\.\d+)?$/.test(s0)) throw new Error("Некорректный Amount");
    const [a,b=""] = s0.split(".");
    const frac = (b+"000000").slice(0,6);
    const micro = BigInt(a)*1000000n + BigInt(frac);
    if (micro<=0n) throw new Error("Amount должен быть > 0");
    return micro;
  }

  async function getJSON(url){
    const r = await fetch(url,{cache:"no-store",credentials:"omit"});
    const t = await r.text();
    if (!r.ok) throw new Error(`${r.status} ${t}`.slice(0,300));
    try { return JSON.parse(t); } catch { return t; }
  }

  async function postJSON(url, body){
    const r = await fetch(url,{
      method:"POST",
      headers:{"content-type":"application/json"},
      body: JSON.stringify(body),
      cache:"no-store",
      credentials:"omit"
    });
    const t = await r.text();
    if (!r.ok) throw new Error(`${r.status} ${t}`.slice(0,600));
    try { return JSON.parse(t); } catch { return t; }
  }

  async function getNextNonce(rid){
    const j = await getJSON(`${NODE_API}/balance/${encodeURIComponent(rid)}`);
    const raw = (j && typeof j==="object" && (j.next_nonce ?? j.nonce ?? j.seq ?? j.sequence));
    if (raw===undefined || raw===null) throw new Error("В /balance нет nonce/next_nonce");
    const bn = BigInt(raw);
    // если отдаёте next_nonce — берём как есть, если nonce — добавим 1
    if (j && typeof j==="object" && j.next_nonce !== undefined) return bn;
    return bn + 1n;
  }

  function canonicalBytes(tx){
    const o = {from:tx.from,to:tx.to,amount:tx.amount,nonce:tx.nonce,memo:tx.memo??null};
    return new TextEncoder().encode(JSON.stringify(o));
  }

  async function sendLGN(){
    try{
      const from = readRID();
      if (!from) throw new Error("Нет RID. Сначала Create/Restore/Unlock или Legacy login.");
      const to = readToRid();
      if (!to) throw new Error("Введите RID получателя.");

      const seedB64 = sessionStorage.getItem(SS_SEED);
      if (!seedB64) throw new Error("Ключ не разблокирован. Вернись на старт и сделай Unlock.");
      if (!window.nacl) throw new Error("tweetnacl не загружен (проверь app.html).");

      const seed32 = b64ToU8(seedB64);
      const kp = nacl.sign.keyPair.fromSeed(seed32);

      const amount = parseAmountMicro();
      const nonce = await getNextNonce(from);

      const tx = { from, to, amount: amount.toString(), nonce: nonce.toString(), memo: null };
      const msg = canonicalBytes(tx);
      const sig = nacl.sign.detached(new Uint8Array(msg), kp.secretKey);

      const body = { ...tx, sig_hex: u8tohex(sig) };
      setStatus(true, "sending…");
      const res = await postJSON(`${NODE_API}/submit_tx`, body);
      setStatus(true, "OK: tx submitted");
      console.log("[lgn_send] submit result:", res);
    }catch(e){
      setStatus(false, "ERR: " + (e.message||String(e)));
      console.warn(e);
    }
  }

  function bind(){
    // найдём кнопку “Send LGN”
    const btn = [...document.querySelectorAll("button")].find(b => /send\s*lgn/i.test(b.textContent||""));
    if (!btn) { console.warn("[lgn_send] button not found"); return; }
    btn.addEventListener("click", (ev)=>{ ev.preventDefault(); sendLGN(); }, true);
    console.log("[lgn_send] ready (seed vault mode)");
  }

  if (document.readyState==="loading") document.addEventListener("DOMContentLoaded", bind);
  else bind();
})();

```

## PROXY TREE: /opt/logos/wallet-proxy

```
/opt/logos/wallet-proxy/
  app.py
  init_db.py
  requirements.txt
  scanner.py

```

## PROXY FILE: /opt/logos/wallet-proxy/app.py

```
import os, json, time, asyncio

# ====== DB session fallback (SessionLocal) ======
# Ensures SessionLocal exists even if earlier patches removed DB setup.
try:
    SessionLocal  # noqa
except NameError:
    try:
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
    except Exception as e:
        raise RuntimeError(f"SQLAlchemy missing or broken: {e}")

    _engine = globals().get("engine") or globals().get("ENGINE")
    if _engine is None:
        DB_URL = (
            os.environ.get("WALLET_PROXY_DB_URL")
            or os.environ.get("DATABASE_URL")
            or "sqlite:////opt/logos/wallet-proxy/wallet_proxy.db"
        )
        if DB_URL.startswith("sqlite"):
            _engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
        else:
            _engine = create_engine(DB_URL)
        globals()["engine"] = _engine

    SessionLocal = sessionmaker(bind=_engine, autocommit=False, autoflush=False)
    globals()["SessionLocal"] = SessionLocal
# ====== /DB session fallback ======
from typing import Optional, Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from web3 import Web3
from sqlalchemy import Column, Integer, String, BigInteger, create_engine, select, Index
from sqlalchemy.orm import declarative_base, Session
import aiohttp
from bip_utils import Bip84, Bip84Coins, Bip44, Bip44Coins, Bip44Changes
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST


# ====== env fallback loader (so systemd/envfile issues won't break XPUB) ======
def _load_env_file(path="/etc/logos/wallet-proxy.env"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                # do not override existing env
                if k and k not in os.environ:
                    os.environ[k] = v
    except FileNotFoundError:
        pass
    except Exception as e:
        print("WARN: failed to load env file:", e)

_load_env_file()

# ====== ENV ======
NODE_URL     = os.environ.get("LRB_NODE_URL", "http://127.0.0.1:8080")
BRIDGE_KEY   = os.environ.get("LRB_BRIDGE_KEY", "")
CORS         = [o.strip() for o in os.environ.get("LRB_WALLET_CORS", "*").split(",") if o.strip()]
ETH_RPC      = ***
USDT_ADDRESS = os.environ.get("USDT_ERC20_ADDRESS", "0xdAC17F958D2ee523a2206206994597C13D831ec7")
HOT_PK       = os.environ.get("ETH_HOT_WALLET_PK", "")
BTC_XPUB     = os.environ.get("BTC_XPUB", "")
ETH_XPUB     = os.environ.get("ETH_XPUB", "")
TRON_XPUB    = os.environ.get("TRON_XPUB", "")
DB_URL       = "sqlite:////opt/logos/wallet-proxy/wproxy.db"

# ====== DB ======
Base = declarative_base()

class DepositMap(Base):
    __tablename__ = "deposit_map"
    id         = Column(Integer, primary_key=True)
    rid        = Column(String, index=True, nullable=False)
    token      = ***
    network    = Column(String, nullable=False)
    index      = Column(Integer, nullable=False, default=0)
    address    = Column(String, unique=True, nullable=False)
    created_at = Column(BigInteger, default=lambda: int(time.time()))

Index("ix_dep_unique", DepositMap.rid, DepositMap.token, DepositMap.network, unique=True)

class SeenTx(Base):
    __tablename__ = "seen_tx"
    id      = Column(Integer, primary_key=True)
    txid    = Column(String, unique=True, nullable=False)
    rid     = Column(String, index=True)
    token   = ***
    network = Column(String)

engine = create_engine(DB_URL, future=True)
Base.metadata.create_all(engine)

# ====== Web3 ======
w3: Optional[Web3] = None
USDT = None
ERC20_ABI = json.loads("""
[
 {"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"},
 {"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"type":"function"},
 {"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}
]
""")
if ETH_RPC:
    try:
        w3 = Web3(Web3.HTTPProvider(ETH_RPC, request_kwargs={"timeout": 10}))
        if w3.is_connected():
            USDT = w3.eth.contract(
                address=Web3.to_checksum_address(USDT_ADDRESS),
                abi=ERC20_ABI,
            )
            print("INFO Web3 connected:", USDT_ADDRESS)
        else:
            print("WARN ETH RPC not reachable")
            w3 = None
    except Exception as e:
        print("WARN web3 init error:", e)
        w3 = None
        USDT = None

# ====== HTTP helper ======
async def http_json(method: str, url: str, body: dict = None, headers: dict = None):
    async with aiohttp.ClientSession() as sess:
        async with sess.request(method, url, json=body, headers=headers) as r:
            t = await r.text()
            try:
                data = json.loads(t) if t else {}
            except Exception:
                data = {"raw": t}
            return r.status, data

# ====== FastAPI ======
app = FastAPI(title="LRB Wallet Proxy", version="1.2")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS if CORS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====== Pydantic v2-safe models ======
class TopupRequest(BaseModel):
    rid: str
    token: ***
    network: Literal["ETH"] = "ETH"

class TopupResponse(BaseModel):
    rid: str
    token: ***
    network: str
    address: str

class WithdrawRequest(BaseModel):
    rid: str
    token: ***
    network: Literal["ETH"] = "ETH"
    amount: int
    to_address: str
    request_id: str

class QuoteRequest(BaseModel):
    from_token: ***
    to_token: ***
    amount: int

class QuoteResponse(BaseModel):
    price: float
    expected_out: float

# ====== Metrics ======
PROXY_TOPUP_REQ    = Counter("proxy_topup_requests_total", "topup requests")
PROXY_WITHDRAW_OK  = Counter("proxy_withdraw_ok_total",   "withdraw ok")
PROXY_WITHDRAW_ERR = Counter("proxy_withdraw_err_total",  "withdraw err")

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)



# ====== Address derivation (watch-only) ======

# ====== Address derivation (watch-only) ======
# NOTE: address must be globally unique in deposit_map.address
# so we allocate a unique index per chain and retry on collisions.

from sqlalchemy.exc import IntegrityError
from bip_utils import Bip84, Bip84Coins, Bip44, Bip44Coins, Bip44Changes

def _require_env(name: str) -> str:
    v = (os.environ.get(name, "") or "").strip()
    if not v:
        raise HTTPException(status_code=500, detail=f"{name} not configured")
    return v

def _derive_address(chain: str, index: int) -> str:
    chain = chain.upper()
    if chain == "BTC":
        key = _require_env("BTC_XPUB")  # actually zpub ok
        acc = Bip84.FromExtendedKey(key, Bip84Coins.BITCOIN)
        return acc.Change(Bip44Changes.CHAIN_EXT).AddressIndex(index).PublicKey().ToAddress()
    if chain == "ETH":
        key = _require_env("ETH_XPUB")
        acc = Bip44.FromExtendedKey(key, Bip44Coins.ETHEREUM)
        return acc.Change(Bip44Changes.CHAIN_EXT).AddressIndex(index).PublicKey().ToAddress()
    if chain == "TRON":
        key = _require_env("TRON_XPUB")
        acc = Bip44.FromExtendedKey(key, Bip44Coins.TRON)
        return acc.Change(Bip44Changes.CHAIN_EXT).AddressIndex(index).PublicKey().ToAddress()
    raise HTTPException(status_code=400, detail=f"unsupported chain: {chain}")

def _chain_from(token: str, network: str) -> str:
    # нормализуем в "цепь", чтобы USDT на ETH использовал тот же пул адресов ETH
    n = (network or "").upper()
    if n in ("ETH", "ETHEREUM", "ERC20"):
        return "ETH"
    if n in ("TRON", "TRC20"):
        return "TRON"
    if n in ("BTC", "BITCOIN"):
        return "BTC"
    return n

def _next_index(sess, chain: str) -> int:
    # глобальный next index по цепи (не по RID!)
    q = sess.query(DepositMap).filter(DepositMap.network == chain).order_by(DepositMap.index.desc()).first()
    if not q:
        return 0
    try:
        return int(q.index) + 1
    except Exception:
        return 0

def _get_or_create_addr(rid: str, token: str, network: str) -> str:
    chain = _chain_from(token, network)

    # 1) если уже есть адрес для rid+chain — вернём
    with SessionLocal() as sess:
        row = sess.query(DepositMap).filter(
            DepositMap.rid == rid,
            DepositMap.network == chain
        ).first()
        if row:
            return row.address

        # 2) выделяем уникальный индекс по chain
        for _ in range(0, 2048):
            idx = _next_index(sess, chain) + _
            addr = _derive_address(chain, idx)

            obj = DepositMap(
                rid=rid,
                token=***
                network=chain,
                index=idx,
                address=addr,
                created_at=int(time.time()),
            )

            sess.add(obj)

            # --- race-safe commit ---
            try:
                sess.commit()
                return addr
            except IntegrityError:
                sess.rollback()

                # 1) если параллельный запрос уже создал маппинг для этого кошелька — просто вернём его
                row2 = sess.query(DepositMap).filter(
                    DepositMap.rid == rid,
                    DepositMap.token == token,
                    DepositMap.network == chain
                ).first()
                if row2:
                    return row2.address

                # 2) иначе это коллизия по address/index (или другой UNIQUE) — пробуем следующий idx
                continue

        raise HTTPException(status_code=500, detail="unable to allocate unique address")
# ====== Endpoints ======

# --- receive addresses (watch-only) ---
@app.get("/v1/receive/{rid}")
def receive_addresses(rid: str):
    rid = (rid or "").strip()
    if not rid:
        raise HTTPException(status_code=400, detail="rid is required")

    # BTC / ETH / TRON: один адрес на цепь.
    # USDT на ETH/TRON использует тот же адрес соответствующей цепи.
    addrs = {
        "BTC": _get_or_create_addr(rid, "BTC", "BTC"),
        "ETH": _get_or_create_addr(rid, "ETH", "ETH"),
        "TRON": _get_or_create_addr(rid, "TRON", "TRON"),
        "USDT_ERC20": _get_or_create_addr(rid, "USDT", "ETH"),
        "USDT_TRC20": _get_or_create_addr(rid, "USDT", "TRON"),
    }
    return {"rid": rid, "lgn_rid": rid, "addresses": addrs}



# --- balances (live) ---
from decimal import Decimal
import time

_USDT_ETH = "0xdAC17F958D2ee523a2206206994597C13D831ec7"  # USDT ERC20 mainnet
_USDT_TRON = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"         # USDT TRC20 (Tether)

_ERC20_ABI_MIN = [
    {"name":"balanceOf","type":"function","stateMutability":"view",
     "inputs":[{"name":"account","type":"address"}],
     "outputs":[{"name":"","type":"uint256"}]},
    {"name":"decimals","type":"function","stateMutability":"view",
     "inputs":[], "outputs":[{"name":"","type":"uint8"}]},
]

def _d(x, q=18):
    try:
        return str((Decimal(x) / (Decimal(10) ** Decimal(q))).normalize())
    except Exception:
        return None

def _http_get_json(url: str, params=None, timeout=12):
    # requests может не быть -> fallback на urllib
    try:
        import requests
        r = requests.get(url, params=params, timeout=timeout, headers={"User-Agent":"logos-wallet-proxy/1.0"})
        r.raise_for_status()
        return r.json()
    except Exception:
        import json, urllib.request, urllib.parse
        if params:
            url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"User-Agent":"logos-wallet-proxy/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", "ignore"))

def _btc_balance_blockstream(addr: str):
    # confirmed + mempool balances in sats
    j = _http_get_json(f"https://blockstream.info/api/address/{addr}")
    cs = j.get("chain_stats") or {}
    ms = j.get("mempool_stats") or {}
    confirmed = int(cs.get("funded_txo_sum", 0)) - int(cs.get("spent_txo_sum", 0))
    mempool = int(ms.get("funded_txo_sum", 0)) - int(ms.get("spent_txo_sum", 0))
    total = confirmed + mempool
    return {
        "confirmed_sat": confirmed,
        "mempool_sat": mempool,
        "total_sat": total,
        "total_btc": _d(total, 8),
        "source": "blockstream.info"
    }

def _eth_balances_web3(addr: str):
    # web3 instance
    try:
        w3 = globals().get("w3") or globals().get("W3")
        if w3 is None:
            from web3 import Web3
            w3 = Web3(Web3.HTTPProvider(_require_env("ETH_PROVIDER_URL"), request_kwargs={"timeout": 12}))
            globals()["w3"] = w3
        if not w3.is_connected():
            return {"error": "ETH provider not connected"}

        wei = int(w3.eth.get_balance(addr))
        out = {"wei": wei, "eth": _d(wei, 18), "source": "web3"}

        # USDT ERC20
        c = w3.eth.contract(address=w3.to_checksum_address(_USDT_ETH), abi=_ERC20_ABI_MIN)
        try:
            dec = int(c.functions.decimals().call())
        except Exception:
            dec = 6
        raw = int(c.functions.balanceOf(w3.to_checksum_address(addr)).call())
        out["usdt_erc20"] = {"raw": raw, "usdt": _d(raw, dec), "decimals": dec, "contract": _USDT_ETH}
        return out
    except Exception as e:
        return {"error": f"eth_web3_failed: {e}"}

def _tron_balances(addr: str):
    # 1) try tronpy (if installed)
    try:
        from tronpy import Tron
        client = Tron()
        trx = client.get_account_balance(addr)  # float TRX
        # TRC20 USDT
        usdt = client.get_contract(_USDT_TRON).functions.balanceOf(addr)
        usdt_raw = int(usdt)
        return {
            "trx": str(trx),
            "sun": int(Decimal(trx) * Decimal(1_000_000)),
            "usdt_trc20": {"raw": usdt_raw, "usdt": _d(usdt_raw, 6), "decimals": 6, "contract": _USDT_TRON},
            "source": "tronpy"
        }
    except Exception:
        pass

    # 2) fallback: tronscan public api
    try:
        j = _http_get_json("https://apilist.tronscanapi.com/api/account", params={"address": addr})
        # TRX
        bal_sun = int(j.get("balance", 0))
        out = {
            "sun": bal_sun,
            "trx": _d(bal_sun, 6),
            "source": "tronscan"
        }
        # USDT TRC20 from token balances
        tb = j.get("trc20token_balances") or j.get("trc20TokenBalances") or []
        usdt_raw = None
        for it in tb:
            ca = (it.get("contract_address") or it.get("contractAddress") or "").strip()
            if ca == _USDT_TRON:
                usdt_raw = it.get("balance") or it.get("tokenBalance") or it.get("quantity")
                break
        if usdt_raw is not None:
            try:
                usdt_raw = int(str(usdt_raw))
            except Exception:
                usdt_raw = None
        out["usdt_trc20"] = {"raw": usdt_raw, "usdt": _d(usdt_raw or 0, 6), "decimals": 6, "contract": _USDT_TRON}
        return out
    except Exception as e:
        return {"error": f"tron_failed: {e}"}

@app.get("/v1/balances/{rid}")
def balances(rid: str):
    rid = (rid or "").strip()
    if not rid:
        raise HTTPException(status_code=400, detail="rid is required")

    # addresses (ensure mapping exists)
    addrs = {
        "BTC": _get_or_create_addr(rid, "BTC", "BTC"),
        "ETH": _get_or_create_addr(rid, "ETH", "ETH"),
        "TRON": _get_or_create_addr(rid, "TRON", "TRON"),
        "USDT_ERC20": _get_or_create_addr(rid, "USDT", "ETH"),
        "USDT_TRC20": _get_or_create_addr(rid, "USDT", "TRON"),
    }

    t0 = time.time()
    out = {
        "rid": rid,
        "addresses": addrs,
        "balances": {},
        "ts": int(time.time())
    }

    # BTC
    try:
        out["balances"]["BTC"] = _btc_balance_blockstream(addrs["BTC"])
    except Exception as e:
        out["balances"]["BTC"] = {"error": f"btc_failed: {e}"}

    # ETH + USDT_ERC20
    out["balances"]["ETH"] = _eth_balances_web3(addrs["ETH"])

    # TRON + USDT_TRC20
    out["balances"]["TRON"] = _tron_balances(addrs["TRON"])

    out["latency_ms"] = int((time.time() - t0) * 1000)
    return out
@app.get("/")
def root():
    return {"ok": True, "service": "wallet-proxy", "eth_connected": bool(w3)}

@app.post("/v1/topup/request", response_model=TopupResponse)
def topup_request(req: TopupRequest):
    PROXY_TOPUP_REQ.inc()
    if not w3:
        raise HTTPException(503, "ETH RPC not connected")
    if not HOT_PK:
        raise HTTPException(500, "HOT wallet not configured")

    deposit_address = w3.eth.account.from_key(HOT_PK).address

    with Session(engine) as s:
        dm = s.execute(
            select(DepositMap).where(
                DepositMap.rid == req.rid,
                DepositMap.token == req.token,
                DepositMap.network == req.network,
            )
        ).scalar_one_or_none()
        if dm is None:
            s.add(
                DepositMap(
                    rid=req.rid,
                    token=***
                    network=req.network,
                    address=deposit_address,
                )
            )
            s.commit()

    return TopupResponse(
        rid=req.rid,
        token=***
        network=req.network,
        address=deposit_address,
    )

@app.post("/v1/withdraw")
async def withdraw(req: WithdrawRequest):
    try:
        if req.amount <= 0:
            raise HTTPException(400, "amount<=0")
        if not w3 or not USDT:
            raise HTTPException(503, "ETH RPC not connected")

        acct = w3.eth.account.from_key(HOT_PK)

        # redeem из LRB-ноды
        hdr = (
            {"X-Bridge-Key": BRIDGE_KEY}
            if not BRIDGE_KEY.startswith("ey")
            else {"Authorization": f"Bearer {BRIDGE_KEY}"}
        )
        st, data = await http_json(
            "POST",
            f"{NODE_URL}/bridge/redeem",
            {
                "rid": req.rid,
                "amount": req.amount,
                "request_id": req.request_id,
            },
            hdr,
        )
        if st // 100 != 2:
            raise HTTPException(st, f"bridge redeem failed: {data}")

        # ERC-20 перевод USDT
        nonce = w3.eth.get_transaction_count(acct.address)
        tx = USDT.functions.transfer(
            Web3.to_checksum_address(req.to_address),
            int(req.amount),
        ).build_transaction(
            {
                "chainId": w3.eth.chain_id,
                "from": acct.address,
                "nonce": nonce,
                "gas": 90000,
                "maxFeePerGas": w3.to_wei("30", "gwei"),
                "maxPriorityFeePerGas": w3.to_wei("1", "gwei"),
            }
        )
        signed = w3.eth.account.sign_transaction(tx, private_key=HOT_PK)
        tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction).hex()

        with Session(engine) as s:
            s.add(
                SeenTx(
                    txid=tx_hash,
                    rid=req.rid,
                    token=***
                    network=req.network,
                )
            )
            s.commit()

        PROXY_WITHDRAW_OK.inc()
        return {"ok": True, "txid": tx_hash}
    except HTTPException:
        PROXY_WITHDRAW_ERR.inc()
        raise
    except Exception as e:
        PROXY_WITHDRAW_ERR.inc()
        raise HTTPException(500, f"withdraw error: {e}")

@app.post("/v1/quote", response_model=QuoteResponse)
async def quote(req: QuoteRequest):
    return QuoteResponse(price=1.0, expected_out=float(req.amount))

```

## PROXY FILE: /opt/logos/wallet-proxy/init_db.py

```
import os, sqlite3, sys

def db_path_from_url(url: str) -> str:
    url = (url or "").strip()
    if not url:
        return "/opt/logos/wallet-proxy/wallet_proxy.db"
    if url.startswith("sqlite:////"):
        return url[len("sqlite:////")-1:]  # keep leading /
    if url.startswith("sqlite:///"):
        return url[len("sqlite:///"):]
    if url.startswith("sqlite://"):
        # rare, but handle
        return url.replace("sqlite://", "", 1)
    # not sqlite -> do nothing here
    return ""

DB_URL = os.environ.get("WALLET_PROXY_DB_URL") or os.environ.get("DATABASE_URL") or "sqlite:////opt/logos/wallet-proxy/wallet_proxy.db"
path = db_path_from_url(DB_URL)

if not path:
    print("INFO: non-sqlite DB configured, skip init_db")
    sys.exit(0)

os.makedirs(os.path.dirname(path), exist_ok=True)

con = sqlite3.connect(path)
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS deposit_map (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  rid TEXT NOT NULL,
  token TEXT NOT NULL,
  network TEXT NOT NULL,
  "index" INTEGER NOT NULL DEFAULT 0,
  address TEXT NOT NULL,
  created_at INTEGER NOT NULL
);
""")

# глобальная уникальность адреса (у тебя это уже требуется по логике)
cur.execute("""CREATE UNIQUE INDEX IF NOT EXISTS ux_deposit_map_address ON deposit_map(address);""")

# чтобы быстро находить по (rid, network) — под ваш SELECT
cur.execute("""CREATE INDEX IF NOT EXISTS ix_deposit_map_rid_network ON deposit_map(rid, network);""")

con.commit()
con.close()

print("OK: init_db done ->", path)

```

## PROXY FILE: /opt/logos/wallet-proxy/requirements.txt

```
aiohappyeyeballs==2.6.1
aiohttp==3.12.15
aiosignal==1.4.0
aiosqlite==0.21.0
annotated-types==0.7.0
anyio==4.10.0
attrs==25.3.0
bip-utils==2.9.3
bitarray==3.7.1
cbor2==5.7.0
certifi==2025.8.3
cffi==1.17.1
charset-normalizer==3.4.3
ckzg==2.1.1
click==8.2.1
coincurve==21.0.0
crcmod==1.7
cytoolz==1.0.1
ecdsa==0.19.1
ed25519-blake2b==1.4.1
eth-account==0.13.7
eth-hash==0.7.1
eth-keyfile==0.8.1
eth-keys==0.7.0
eth-rlp==2.2.0
eth-typing==5.2.1
eth-utils==5.3.1
eth_abi==5.2.0
fastapi==0.116.1
frozenlist==1.7.0
greenlet==3.2.4
h11==0.16.0
hexbytes==1.3.1
httptools==0.6.4
idna==3.10
multidict==6.6.4
parsimonious==0.10.0
prometheus_client==0.22.1
propcache==0.3.2
py-sr25519-bindings==0.2.2
pycparser==2.22
pycryptodome==3.23.0
pydantic==2.11.7
pydantic_core==2.33.2
PyNaCl==1.5.0
python-dotenv==1.1.1
pyunormalize==16.0.0
PyYAML==6.0.2
regex==2025.9.1
requests==2.32.5
rlp==4.1.0
six==1.17.0
sniffio==1.3.1
SQLAlchemy=***
starlette==0.47.3
toolz==1.0.0
types-requests==2.32.4.20250809
typing-inspection==0.4.1
typing_extensions==4.15.0
urllib3==2.5.0
uvicorn==0.35.0
uvloop==0.21.0
watchfiles==1.1.0
web3==7.13.0
websockets==15.0.1
yarl==1.20.1

```

## PROXY FILE: /opt/logos/wallet-proxy/scanner.py

```
import os, json, time, asyncio
from typing import Optional
from web3 import Web3
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from prometheus_client import Counter, Gauge, start_http_server
import aiohttp

DB_URL       = "sqlite:////opt/logos/wallet-proxy/wproxy.db"
NODE_URL     = os.environ.get("LRB_NODE_URL", "http://127.0.0.1:8080")
BRIDGE_KEY   = os.environ.get("LRB_BRIDGE_KEY", "")
ETH_RPC      = ***
USDT_ADDRESS = os.environ.get("USDT_ERC20_ADDRESS", "0xdAC17F958D2ee523a2206206994597C13D831ec7")
CONFIRMATIONS= int(os.environ.get("ETH_CONFIRMATIONS", "6"))

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, BigInteger

Base = declarative_base()
class DepositMap(Base):
    __tablename__ = "deposit_map"
    id = Column(Integer, primary_key=True); rid = Column(String); token = Column(String); network = Column(String); address = Column(String)
class SeenTx(Base):
    __tablename__ = "seen_tx"
    id = Column(Integer, primary_key=True); txid = Column(String, unique=True); rid = Column(String); token = Column(String); network = Column(String)
class Kv(Base):
    __tablename__ = "kv"
    k = Column(String, primary_key=True); v = Column(String, nullable=False)

engine = create_engine(DB_URL, future=True)

# metrics
SCAN_LAST_BLOCK = Gauge("scanner_last_scanned_block", "last scanned block")
SCAN_LAG        = Gauge("scanner_block_lag", "chain head minus safe block")
DEP_OK          = Counter("scanner_deposit_ok_total", "successful deposits")
DEP_ERR         = Counter("scanner_deposit_err_total","failed deposits")

async def http_json(method:str, url:str, body:dict=None, headers:dict=None):
    async with aiohttp.ClientSession() as sess:
        async with sess.request(method, url, json=body, headers=headers) as r:
            t = await r.text()
            try: data = json.loads(t) if t else {}
            except: data = {"raw": t}
            return r.status, data

def kv_get(key:str, default:str="0")->str:
    with Session(engine) as s:
        row = s.get(Kv, key); return row.v if row else default
def kv_set(key:str, val:str):
    with Session(engine) as s:
        row = s.get(Kv, key)
        if row: row.v = val
        else:   s.add(Kv(k=key, v=val))
        s.commit()

async def scanner():
    if not ETH_RPC:
        print("No ETH RPC configured; scanner idle"); 
        while True: await asyncio.sleep(30)

    w3 = Web3(Web3.HTTPProvider(ETH_RPC, request_kwargs={"timeout":10}))
    if not w3.is_connected():
        print("ETH RPC unreachable; scanner idle")
        while True: await asyncio.sleep(30)

    USDT = w3.eth.contract(address=Web3.to_checksum_address(USDT_ADDRESS), abi=json.loads("""
    [
     {"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}
    ]
    """))
    key = "last_scanned_block"
    backoff = 1
    while True:
        try:
            head = w3.eth.block_number
            safe_to = head - CONFIRMATIONS
            last = int(kv_get(key, "0"))
            SCAN_LAG.set(max(0, head - safe_to))
            if safe_to <= last:
                await asyncio.sleep(5); continue

            step = 2000
            from_block = last + 1
            with Session(engine) as s:
                addr_map = {dm.address.lower(): dm for dm in s.query(DepositMap).all()}

            while from_block <= safe_to:
                to_block = min(from_block + step - 1, safe_to)
                logs = w3.eth.get_logs({
                    "fromBlock": from_block, "toBlock": to_block,
                    "address": Web3.to_checksum_address(USDT_ADDRESS),
                    "topics": [Web3.keccak(text="Transfer(address,address,uint256)")]
                })
                for lg in logs:
                    to_hex = "0x"+lg["topics"][2].hex()[-40:]
                    to_norm = Web3.to_checksum_address(to_hex).lower()
                    dm = addr_map.get(to_norm)
                    if not dm: continue
                    txid = lg["transactionHash"].hex()
                    value = int(lg["data"], 16)
                    # идемпотентность
                    with Session(engine) as s:
                        if s.execute(select(SeenTx).where(SeenTx.txid==txid)).scalar_one_or_none():
                            continue
                        s.add(SeenTx(txid=txid, rid=dm.rid, token=dm.token, network=dm.network)); s.commit()
                    # bridge deposit
                    hdr = {"X-Bridge-Key": os.environ.get("LRB_BRIDGE_KEY","")}
                    st, data = await http_json("POST", f"{NODE_URL}/bridge/deposit",
                                               {"rid": dm.rid, "amount": value, "ext_txid": txid}, hdr)
                    if st//100 == 2: DEP_OK.inc()
                    else:
                        DEP_ERR.inc()
                        print("WARN deposit fail", txid, st, data)
                kv_set(key, str(to_block))
                SCAN_LAST_BLOCK.set(to_block)
                from_block = to_block + 1
                backoff = 1
            await asyncio.sleep(5)
        except Exception as e:
            print("scanner error:", e)
            await asyncio.sleep(min(60, backoff)); backoff = min(60, backoff*2)

if __name__ == "__main__":
    # метрики на 9101
    start_http_server(9101)
    asyncio.run(scanner())

```

## NGINX VHOST FILE: /etc/nginx/sites-available/logos.conf

```
# Лимиты запросов к API
limit_req_zone $binary_remote_addr zone=api_zone:10m rate=30r/s;

# WebSocket/upgrade helper
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

# Узел LOGOS (REST API)
upstream logos_node_backend {
    server 127.0.0.1:8080;
    keepalive 32;
}

# Wallet-proxy (депозиты USDT -> rLGN)
upstream logos_wallet_api {
    server 127.0.0.1:9090;
    keepalive 16;
}

# Airdrop API — upstream объявлен в /etc/nginx/conf.d/logos_airdrop_upstream.conf
# upstream logos_airdrop_api { ... }

server {
    listen 80;
    server_name mw-expedition.com www.mw-expedition.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name mw-expedition.com www.mw-expedition.com;

    ssl_certificate     /etc/letsencrypt/live/mw-expedition.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/mw-expedition.com/privkey.pem;

    # По умолчанию — статика кошелька/эксплорера
    root /opt/logos/www;
    index index.html;

    # === Лендинг ===
    location = / {
        root /var/www/logos/landing;
        try_files /index.html =404;
        add_header Cache-Control "no-store" always;
    }

    # Страница аирдропа /airdrop.html
    # === Wallet SPA ===
    location /wallet/ {
        try_files $uri /wallet/index.html;
        add_header Cache-Control "no-store" always;
        add_header Content-Security-Policy "default-src 'self'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/api https://mw-expedition.com/proxy https://vnet.web3games.org https://mainnet.infura.io;" always;
    }

    # === Explorer SPA ===
    location /explorer/ {
        try_files $uri /explorer/index.html;
        add_header Cache-Control "no-store" always;
        # Разрешаем inline-стили и скрипты для explorer, API остаётся только self
        add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/api;" always;
    }

    # === REST API ноды ===
    location /api/ {
        limit_req zone=api_zone burst=60 nodelay;

        proxy_pass http://logos_node_backend/;
        proxy_http_version 1.1;
        proxy_set_header Connection "";

        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # === Wallet-proxy API ===
    location /proxy/ {
        proxy_pass http://logos_wallet_api/;
        proxy_http_version 1.1;
        proxy_set_header Connection "";

        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # === Airdrop API ===
    # Общая статика (JS/CSS/иконки)
    location ~* \.(?:css|js|ico|png|jpg|jpeg|svg|woff2?)$ {
        try_files $uri =404;
        add_header Cache-Control "no-store" always;
    }
}

```

## NGINX VHOST FILE: /etc/nginx/sites-available/logos.conf.bak_2025-12-13_090034

```
# Лимиты запросов к API
limit_req_zone $binary_remote_addr zone=api_zone:10m rate=30r/s;

# WebSocket/upgrade helper
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

# Узел LOGOS (REST API)
upstream logos_node_backend {
    server 127.0.0.1:8080;
    keepalive 32;
}

# Wallet-proxy (депозиты USDT -> rLGN)
upstream logos_wallet_api {
    server 127.0.0.1:9090;
    keepalive 16;
}

# Airdrop API — upstream объявлен в /etc/nginx/conf.d/logos_airdrop_upstream.conf
# upstream logos_airdrop_api { ... }

server {
    listen 80;
    server_name mw-expedition.com www.mw-expedition.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name mw-expedition.com www.mw-expedition.com;

    ssl_certificate     /etc/letsencrypt/live/mw-expedition.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/mw-expedition.com/privkey.pem;

    # По умолчанию — статика кошелька/эксплорера
    root /opt/logos/www;
    index index.html;

    # === Лендинг ===
    location = / {
        root /var/www/logos/landing;
        try_files /index.html =404;
        add_header Cache-Control "no-store" always;
    }

    # Страница аирдропа /airdrop.html
    # === Wallet SPA ===
    location /wallet/ {
        try_files $uri /wallet/index.html;
        add_header Cache-Control "no-store" always;
        add_header Content-Security-Policy "default-src 'self'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/api https://mw-expedition.com/proxy https://vnet.web3games.org https://mainnet.infura.io;" always;
    }

    # === Explorer SPA ===
    location /explorer/ {
        try_files $uri /explorer/index.html;
        add_header Cache-Control "no-store" always;
        # Разрешаем inline-стили и скрипты для explorer, API остаётся только self
        add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/api;" always;
    }

    # === REST API ноды ===
    location /api/ {
        limit_req zone=api_zone burst=60 nodelay;

        proxy_pass http://logos_node_backend/;
        proxy_http_version 1.1;
        proxy_set_header Connection "";

        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # === Wallet-proxy API ===
    location /proxy/ {
        proxy_pass http://logos_wallet_api/;
        proxy_http_version 1.1;
        proxy_set_header Connection "";

        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # === Airdrop API ===
    # Общая статика (JS/CSS/иконки)
    location ~* \.(?:css|js|ico|png|jpg|jpeg|svg|woff2?)$ {
        try_files $uri =404;
        add_header Cache-Control "no-store" always;
    }
}

```

## NGINX VHOST FILE: /etc/nginx/sites-available/logos_front.bak

```
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name mw-expedition.com www.mw-expedition.com;

    root /var/www/logos/landing;
    index index.html;

    charset utf-8;

    # Базовая защита
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # --- Лендинг LOGOS (SPA)
    location / {
        try_files $uri $uri/ /index.html;
    }

    # --- Статика с долгим кэшем
    location ~* \.(?:css|js|ico|png|jpe?g|gif|svg|webp|woff2?)$ {
        access_log off;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000, immutable";
        try_files $uri =404;
    }

    # --- Airdrop API (FastAPI на 127.0.0.1:8092)
    # более специфичный префикс, чем /api/, поэтому всегда пойдёт сюда
    location /api/airdrop/ {
        proxy_pass         http://127.0.0.1:8092;
        proxy_http_version 1.1;

        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_read_timeout    60s;
        proxy_connect_timeout 5s;
        proxy_send_timeout    60s;
    }

    # --- Прокси к ноде LOGOS (если используешь HTTP API ноды)
    # если порт другой — просто поправь 8090 на свой
    location /api/ {
        proxy_pass         http://127.0.0.1:8090;
        proxy_http_version 1.1;

        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_read_timeout    120s;
        proxy_connect_timeout 5s;
        proxy_send_timeout    120s;
    }

    ssl_certificate     /etc/letsencrypt/live/mw-expedition.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/mw-expedition.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

# HTTP → HTTPS редирект
server {
    listen 80;
    listen [::]:80;
    server_name mw-expedition.com www.mw-expedition.com;

    return 301 https://$host$request_uri;
}


```

## NGINX VHOST FILE: /etc/nginx/sites-available/logos_front.bak.20251125T072637

```
server {
    server_name mw-expedition.com www.mw-expedition.com;

    root /var/www/logos/landing;
    index index.html;

    add_header X-Content-Type-Options "nosniff" always;

    # Лендинг LOGOS (SPA)
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Статика с долгим кэшем
    location ~* \.(?:css|js|svg|woff2?)$ {
        access_log off;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000, immutable";
    }

    # Прокси к ноде (если решим использовать /api/)
    location /api/ {
        proxy_pass http://127.0.0.1:8081/;
        proxy_set_header Host               $host;
        proxy_set_header X-Real-IP          $remote_addr;
        proxy_set_header X-Forwarded-For    $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto  $scheme;
    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/mw-expedition.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/mw-expedition.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot


}

server {
    if ($host = www.mw-expedition.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    if ($host = mw-expedition.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    listen 80;
    server_name mw-expedition.com www.mw-expedition.com;
    return 404; # managed by Certbot




}
```

## NGINX VHOST FILE: /etc/nginx/sites-available/logos_front.bak.20251127T134555

```
# Upstream'ы для API
upstream logos_api {
    server 127.0.0.1:8090;
    keepalive 64;
}

upstream airdrop_api {
    server 127.0.0.1:8090;
    keepalive 64;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;

    server_name mw-expedition.com www.mw-expedition.com;

    root /var/www/logos/landing;
    index index.html;
    charset utf-8;

    # Отдельные логи проекта
    access_log /var/log/nginx/logos_front.access.log;
    error_log  /var/log/nginx/logos_front.error.log warn;

    # Безопасность
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
    add_header Permissions-Policy "geolocation=(), camera=(), microphone=()" always;

    # Сжатие — экономим трафик и ускоряем отдачу
    gzip on;
    gzip_comp_level 5;
    gzip_min_length 256;
    gzip_vary on;
    gzip_proxied any;
    gzip_types
        text/plain
        text/css
        text/javascript
        application/javascript
        application/json
        application/xml
        application/rss+xml
        font/woff2
        application/font-woff2
        image/svg+xml;

    # --- SPA фронт
    location / {
        try_files $uri $uri/ /index.html;
    }

    # --- Статика с долгим кешем
    location ~* \.(?:css|js|ico|png|jpe?g|gif|svg|webp|woff2?|ttf|eot)$ {
        access_log off;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000, immutable";
        try_files $uri =404;
    }

    # --- Airdrop API (FastAPI)
    location /api/airdrop/ {
        proxy_pass http://airdrop_api;
        proxy_http_version 1.1;

        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_read_timeout      60s;
        proxy_connect_timeout   5s;
        proxy_send_timeout      60s;

        # Буферизация для массовых нагрузок
        proxy_buffering on;
        proxy_buffers 32 16k;
        proxy_busy_buffers_size 64k;
    }

    # --- Основной LOGOS API
    location /api/ {
        proxy_pass http://logos_api;
        proxy_http_version 1.1;

        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_read_timeout      120s;
        proxy_connect_timeout   5s;
        proxy_send_timeout      120s;

        proxy_buffering on;
        proxy_buffers 32 32k;
        proxy_busy_buffers_size 256k;
        # сюда можно навесить лимиты RPS, если нужно:
        # limit_req zone=api_burst burst=20 nodelay;
    }

    # SSL от Let's Encrypt
    ssl_certificate     /etc/letsencrypt/live/mw-expedition.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/mw-expedition.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

# HTTP -> HTTPS редирект
server {
    listen 80;
    listen [::]:80;
    server_name mw-expedition.com www.mw-expedition.com;

    return 301 https://$host$request_uri;
}

```

## NGINX VHOST FILE: /etc/nginx/sites-enabled/logos.conf

```
# Лимиты запросов к API
limit_req_zone $binary_remote_addr zone=api_zone:10m rate=30r/s;

map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

upstream logos_node_backend {
    server 127.0.0.1:8080;
    keepalive 32;
}

upstream logos_wallet_api {
    server 127.0.0.1:9090;
    keepalive 16;
}

server {
    listen 80;
    server_name mw-expedition.com www.mw-expedition.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name mw-expedition.com www.mw-expedition.com;

    ssl_certificate     /etc/letsencrypt/live/mw-expedition.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/mw-expedition.com/privkey.pem;

    root /opt/logos/www;
    index index.html;

    location = / {
        root /var/www/logos/landing;
        try_files /index.html =404;
        add_header Cache-Control "no-store" always;
    }

    location ^~ /wallet_v2/ {
        try_files $uri $uri/ /wallet_v2/index.html;
        add_header Cache-Control "no-store" always;
        add_header Content-Security-Policy "default-src 'self'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/node-api https://mw-expedition.com/wallet-api; img-src 'self' data:; font-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline';" always;
    }
    location ^~ /wallet_dev/ {
        alias /opt/logos/www/wallet_dev/;
        index index.html;
        try_files $uri $uri/ /wallet_dev/index.html;
        add_header Cache-Control "no-store" always;
        add_header Content-Security-Policy "default-src 'self'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/node-api https://mw-expedition.com/wallet-api; img-src 'self' data:; font-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline';" always;
    }
    location ^~ /wallet/ {
        alias /opt/logos/www/wallet_prod/;
        index index.html;
        try_files $uri $uri/ /wallet/index.html;
        add_header Cache-Control "no-store" always;
        add_header Content-Security-Policy "default-src 'self'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/node-api https://mw-expedition.com/wallet-api; img-src 'self' data:; font-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self';" always;
    }

location ^~ /explorer/ {
        try_files $uri /explorer/index.html;
        add_header Cache-Control "no-store" always;
        add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/node-api;" always;
    }

    location = /node-api { return 301 /node-api/; }
    location ^~ /node-api/ {
        limit_req zone=api_zone burst=60 nodelay;
        proxy_pass http://logos_node_backend/;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location = /wallet-api { return 301 /wallet-api/; }
    location ^~ /wallet-api/ {
        limit_req zone=api_zone burst=60 nodelay;
        proxy_pass http://logos_wallet_api/;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Совместимость (старые пути)
    location ^~ /api/ {
        limit_req zone=api_zone burst=60 nodelay;
        proxy_pass http://logos_node_backend/;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location ^~ /proxy/ {
        limit_req zone=api_zone burst=60 nodelay;
        proxy_pass http://logos_wallet_api/;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location ~* \.(?:css|js|ico|png|jpg|jpeg|svg|woff2?)$ {
        try_files $uri =404;
        add_header Cache-Control "no-store" always;
    }
}

```

## NGINX -T (filtered mw-expedition.com)

```
    server_name mw-expedition.com www.mw-expedition.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name mw-expedition.com www.mw-expedition.com;

    ssl_certificate     /etc/letsencrypt/live/mw-expedition.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/mw-expedition.com/privkey.pem;

    root /opt/logos/www;
    index index.html;

    location = / {
        root /var/www/logos/landing;
        try_files /index.html =404;
        add_header Cache-Control "no-store" always;
    }

    location ^~ /wallet_v2/ {
        try_files $uri $uri/ /wallet_v2/index.html;
        add_header Cache-Control "no-store" always;
        add_header Content-Security-Policy "default-src 'self'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/node-api https://mw-expedition.com/wallet-api; img-src 'self' data:; font-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline';" always;
    }
    location ^~ /wallet_dev/ {
        alias /opt/logos/www/wallet_dev/;
        index index.html;
        try_files $uri $uri/ /wallet_dev/index.html;
        add_header Cache-Control "no-store" always;
        add_header Content-Security-Policy "default-src 'self'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/node-api https://mw-expedition.com/wallet-api; img-src 'self' data:; font-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline';" always;
    }
    location ^~ /wallet/ {
        alias /opt/logos/www/wallet_prod/;
        index index.html;
        try_files $uri $uri/ /wallet/index.html;
        add_header Cache-Control "no-store" always;
        add_header Content-Security-Policy "default-src 'self'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/node-api https://mw-expedition.com/wallet-api; img-src 'self' data:; font-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self';" always;
    }

location ^~ /explorer/ {
        try_files $uri /explorer/index.html;
        add_header Cache-Control "no-store" always;
        add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/node-api;" always;
    }

    location = /node-api { return 301 /node-api/; }
    location ^~ /node-api/ {
        limit_req zone=api_zone burst=60 nodelay;
        proxy_pass http://logos_node_backend/;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location = /wallet-api { return 301 /wallet-api/; }
    location ^~ /wallet-api/ {
        limit_req zone=api_zone burst=60 nodelay;
        proxy_pass http://logos_wallet_api/;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Совместимость (старые пути)
    location ^~ /api/ {
        limit_req zone=api_zone burst=60 nodelay;
        proxy_pass http://logos_node_backend/;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location ^~ /proxy/ {
        limit_req zone=api_zone burst=60 nodelay;
        proxy_pass http://logos_wallet_api/;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location ~* \.(?:css|js|ico|png|jpg|jpeg|svg|woff2?)$ {
        try_files $uri =404;
        add_header Cache-Control "no-store" always;
    }
}


```

## SYSTEMD: units list (grep logos|wallet|scanner|node)

```
  kmod-static-nodes.service                loaded    active     exited        Create List of Static Device Nodes
  logos-healthcheck.service                loaded    inactive   dead          LOGOS LRB /readyz healthcheck
  logos-ledger-backup.service              loaded    inactive   dead          LOGOS ledger backup (sled snapshot)
  logos-node@main.service                  loaded    active     running       LOGOS LRB Node (main)
  logos-sled-backup.service                loaded    inactive   dead          Backup sled to /root/sled_backups
  logos-wallet-proxy.service               loaded    active     running       LOGOS Wallet Proxy (FastAPI + Uvicorn)
  lrb-proxy.service                        loaded    active     running       LOGOS Wallet Proxy (FastAPI on :9090)
  lrb-scanner.service                      loaded    active     running       LOGOS Wallet Scanner (USDT->rLGN)
  nginx.service                            loaded    active     running       A high performance web server and a reverse proxy server
  node-exporter.service                    loaded    active     running       Node Exporter (Prometheus)
  systemd-tmpfiles-setup-dev-early.service loaded    active     exited        Create Static Device Nodes in /dev gracefully
  systemd-tmpfiles-setup-dev.service       loaded    active     exited        Create Static Device Nodes in /dev

```

## SYSTEMD CAT: logos-wallet-proxy

```
# /etc/systemd/system/logos-wallet-proxy.service
[Unit]
Description=LOGOS Wallet Proxy (FastAPI + Uvicorn)
After=network-online.target
Wants=network-online.target

[Service]
EnvironmentFile=/etc/logos/wallet-proxy.env
User=logos
Group=logos
WorkingDirectory=/opt/logos/wallet-proxy
EnvironmentFile=/etc/logos/wallet-proxy.env

ExecStart=/opt/logos/wallet-proxy/venv/bin/uvicorn app:app \
  --host 0.0.0.0 \
  --port 9090 \
  --workers 2

Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target

# /etc/systemd/system/logos-wallet-proxy.service.d/override.conf
[Service]
EnvironmentFile=
EnvironmentFile=/etc/logos/wallet-proxy.env

# гарантируем, что таблица есть до старта uvicorn
ExecStartPre=/opt/logos/wallet-proxy/venv/bin/python3 /opt/logos/wallet-proxy/init_db.py

```

## SYSTEMD CAT: lrb-proxy

```
# /etc/systemd/system/lrb-proxy.service
[Unit]
Description=LOGOS Wallet Proxy (FastAPI on :9090)
After=network-online.target
Wants=network-online.target

[Service]
User=logos
WorkingDirectory=/opt/logos/wallet-proxy
EnvironmentFile=/etc/logos/proxy.env
ExecStart=/opt/logos/wallet-proxy/venv/bin/uvicorn app:app --host 0.0.0.0 --port 9090 --workers 2
Restart=always
RestartSec=2
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target

```

## SYSTEMD CAT: lrb-scanner

```
# /etc/systemd/system/lrb-scanner.service
[Unit]
Description=LOGOS Wallet Scanner (USDT->rLGN)
After=network-online.target
Wants=network-online.target

[Service]
User=logos
WorkingDirectory=/opt/logos/wallet-proxy
EnvironmentFile=/etc/logos/proxy.env
ExecStart=/opt/logos/wallet-proxy/venv/bin/python /opt/logos/wallet-proxy/scanner.py
Restart=always
RestartSec=2
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target

```

## SYSTEMD CAT: logos-node@main

```
# /etc/systemd/system/logos-node@.service
[Unit]
Description=LOGOS LRB Node (%i)
After=network-online.target
Wants=network-online.target

[Service]
User=logos
EnvironmentFile=/etc/logos/node-%i.env
ExecStart=/opt/logos/bin/logos_node
NoNewPrivileges=yes
PrivateTmp=***
ProtectSystem=strict
ProtectHome=read-only
PrivateDevices=***
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectControlGroups=yes
LockPersonality=yes
MemoryDenyWriteExecute=yes
CapabilityBoundingSet=
SystemCallFilter=@system-service @network-io ~keyctl
ReadWritePaths=/var/lib/logos /var/log/logos
RuntimeDirectory=logos
UMask=0077
[Install]
WantedBy=multi-user.target

# /etc/systemd/system/logos-node@.service.d/10-restart-policy.conf
[Service]
Restart=on-failure
RestartSec=3
StartLimitIntervalSec=60
StartLimitBurst=5

# /etc/systemd/system/logos-node@.service.d/20-env.conf
[Service]
EnvironmentFile=-/etc/logos/node-%i.env

# /etc/systemd/system/logos-node@.service.d/30-hardening.conf
[Service]
# Sandbox
NoNewPrivileges=true
PrivateTmp=***
ProtectHome=true
ProtectSystem=full
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true
LockPersonality=true
MemoryDenyWriteExecute=true
RestrictRealtime=true
RestrictSUIDSGID=true
SystemCallArchitectures=native

# Разрешаем запись ТОЛЬКО где нужно
ReadWritePaths=/var/lib/logos
ReadWritePaths=/var/log/logos

# Ресурсные лимиты
LimitNOFILE=262144
LimitNPROC=8192

# Capabilities обрезаем в ноль
CapabilityBoundingSet=
AmbientCapabilities=

# /etc/systemd/system/logos-node@.service.d/31-bridge-key.conf
[Service]
Environment=LRB_BRIDGE_KEY=supersecret

# /etc/systemd/system/logos-node@.service.d/40-log.conf
[Service]
Environment=RUST_LOG=trace,logos=trace,consensus=trace,axum=info,h2=info,tokio=info

# /etc/systemd/system/logos-node@.service.d/41-faucet.conf
[Service]
# Типичные ключи, которые встречаются в таких сборках:
Environment=LOGOS_FAUCET_ENABLED=true
Environment=LRB_FAUCET_ENABLED=true
# (на некоторых билдах есть явный биндинг — пусть будет)
Environment=LOGOS_FAUCET_PATH=/faucet

# /etc/systemd/system/logos-node@.service.d/env.conf
[Service]
# Per-instance env (например /etc/logos/node-main.env)
EnvironmentFile=/etc/logos/node-%i.env
# Общие секреты (тот самый "keys", чтобы один раз положил — и все инстансы видят)
EnvironmentFile=/etc/logos/keys.env

# /etc/systemd/system/logos-node@.service.d/override.conf
[Service]
Environment=LOGOS_GENESIS_PATH=/etc/logos/genesis.yaml
Environment=LOGOS_NODE_KEY_PATH=/var/lib/logos/node_key

```

## SYSTEMD CAT: logos-node

```
# /etc/systemd/system/logos-node.service
[Unit]
Description=LOGOS LRB Node
After=network-online.target postgresql.service
Wants=network-online.target

[Service]
User=logos
Group=logos
ExecStart=/opt/logos/bin/logos_node
Restart=on-failure
RestartSec=2

# security hardening
AmbientCapabilities=
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=yes
PrivateTmp=***
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectControlGroups=yes
ReadWritePaths=/var/lib/logos

# env & secrets
EnvironmentFile=/etc/logos/keys.env
Environment=RUST_LOG=info
[Install]
WantedBy=multi-user.target

# /etc/systemd/system/logos-node.service.d/00-prod.conf
[Service]
Environment=LRB_DATA_PATH=/var/lib/logos/data.sled
Environment=LRB_NODE_LISTEN=127.0.0.1:8080
Environment=LRB_ARCHIVE_URL=postgres://logos:StrongPass123@127.0.0.1:5432/logos
Environment=LRB_WALLET_ORIGIN=https://45-159-248-232.sslip.io
Environment=LRB_SLOT_MS=200
# сгенерируй рандомные секреты:
#  openssl rand -hex 32
Environment=LRB_JWT_SECRET=***
Environment=LRB_BRIDGE_KEY=***

```

## SYSTEMD CAT: logos_wallet_api

```

```

## SYSTEMD CAT: logos_node_backend

```

```

## ENV (sanitized): /etc/logos/wallet-proxy.env

```
BTC_XPUB=zpub6rB41LL2MUYvPdrPNMrgpkUZyKiP2JDHJANGFWs4YhwEWP4f744e9w363B6d8faiovfRNwBPPCBKMxSqiA7kAyfyNTGNDSAKXwyJhP45kkM
ETH_XPUB=xpub6CqSrK5UrPJcfPUJ1WTTztBKacxqV6SA8637Lor6zrwbm3axCszexzcY4VpDZQ4esPqwR83RYozSHFPaE78kHGvY3AyxEPyK79AWs5r9AMi
TRON_XPUB=xpub6BgzjoofH8Qm6N1TbnhPwikBCbYCjZ9inGemDwC346JymmVCfbcL6Rfxrutr232LD8v8rJJX4zpit5QetPS9UbjSQwSckzsupJbxrfMgU3k

LRB_NODE_URL=http://127.0.0.1:8080
LRB_WALLET_CORS=*

# ETH RPC (needed for USDT / ETH)
ETH_PROVIDER_URL=https://mainnet.infura.io/v3/8b1effbe937f437fbcfd1e89470b63a4
WALLET_PROXY_DB_URL=sqlite:////opt/logos/wallet-proxy/wallet_proxy.db

```

## ENV (sanitized): /etc/logos/proxy.env

```
# === LOGOS Wallet Proxy ENV ===

# LRB node connection
LRB_NODE_URL=http://127.0.0.1:8080
LRB_BRIDGE_KEY=***

# Ethereum provider (Infura mainnet)
ETH_PROVIDER_URL=https://mainnet.infura.io/v3/8b1effbe937f437fbcfd1e89470b63a4
USDT_ERC20_ADDRESS=0xdAC17F958D2ee523a2206206994597C13D831ec7
ETH_CONFIRMATIONS=6

# HD wallet (для депозитных адресов пользователей)
ETH_MNEMONIC=***
# Hot wallet (для выводов USDT)
ETH_HOT_WALLET_PK=***
# Proxy service settings
PROXY_HOST=0.0.0.0
PROXY_PORT=9090

```

## ENV (sanitized): /etc/logos/node-main.env

```

LOGOS_HTTP_ADDR=127.0.0.1:8080
LRB_HTTP_ADDR=127.0.0.1:8080
LOGOS_ENABLE_METRICS=1
LOGOS_ENABLE_OPENAPI=1
LOGOS_BRIDGE_ENABLE=1
LOGOS_PRODUCER_ENABLE=1
RUST_LOG=info,logos_node=info,lrb=info
LOGOS_GENESIS_PATH=/etc/logos/genesis.yaml
LOGOS_NODE_KEY_PATH=/var/lib/logos/node_key
LRB_SLOT_MS=500

# X (Twitter / X) integration for LOGOS X Guard
X_API_KEY=***
X_API_SECRET=***
X_BEARER_TOKEN=***
X_ACCESS_TOKEN=***
X_ACCESS_TOKEN_SECRET=***
LRB_JWT_SECRET=***
LRB_BRIDGE_KEY=***
LRB_FAUCET_SECRET=***
```

## ENV (sanitized): /etc/logos/keys.env

```
LRB_ADMIN_KEY=superadmin_6479561f83954a3a89039b2460b34da7
FOUNDER_SK_HEX=***
RID_FOUNDER_MAIN=Λ0@7.83Hzφ0.3877
LRB_NODE_SK_HEX=***

```

## JOURNALCTL -u logos-wallet-proxy -n 300

```
Jan 10 13:33:15 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:34:15 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:35:14 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:36:14 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:37:15 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:38:15 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:39:15 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:40:14 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:41:15 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:42:14 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:43:14 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:47:56 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:48:11 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:48:25 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:48:41 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:48:56 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:49:11 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:49:26 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:49:41 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:50:14 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:51:20 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:52:14 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:53:14 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:54:14 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:55:14 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:56:14 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:57:15 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:58:15 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:59:15 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 14:00:14 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 14:01:15 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 14:02:14 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 14:03:14 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 14:04:14 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 06:42:13 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 06:42:31 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 06:42:46 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 06:43:01 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 06:43:16 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 06:43:32 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 06:43:47 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 06:44:02 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 06:44:16 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 06:44:32 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 06:44:47 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 06:45:02 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 06:45:17 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 06:46:13 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 06:47:13 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 06:48:13 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 06:49:13 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 06:50:13 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 06:51:13 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 06:52:13 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 06:53:13 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 06:54:13 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 06:55:13 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 06:56:03 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 06:56:15 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 06:57:17 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 06:57:26 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 07:12:11 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 07:12:27 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 07:12:41 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 07:12:56 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 07:13:12 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 07:13:27 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 07:13:42 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 07:13:57 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 07:14:13 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 07:15:13 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 07:16:13 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 07:17:13 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 07:18:13 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 07:19:13 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 07:20:13 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 07:21:13 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 07:22:13 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 07:23:13 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 07:24:13 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 07:24:32 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /balance/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 404 Not Found
Jan 11 07:24:41 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:25:27 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:25:41 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:25:57 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:26:11 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:26:26 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:26:41 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:26:56 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:27:12 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:27:26 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:27:42 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:27:59 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:28:11 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:28:27 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:28:42 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:28:56 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:29:11 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:29:27 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:29:42 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:29:57 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:30:12 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:31:12 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:32:12 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:33:12 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:34:12 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:35:14 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:36:14 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:37:14 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:38:15 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:39:15 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:40:14 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:41:15 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:42:15 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:43:15 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 07:44:14 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 10:32:35 vm15330919.example.com uvicorn[1101248]: INFO:     45.159.248.232:0 - "GET /openapi.json HTTP/1.1" 200 OK
Jan 11 10:32:35 vm15330919.example.com uvicorn[1101248]: INFO:     45.159.248.232:0 - "GET /openapi.json HTTP/1.1" 200 OK
Jan 11 11:03:34 vm15330919.example.com uvicorn[1101248]: INFO:     45.159.248.232:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 11:04:07 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 11:04:09 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 11:22:37 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 11:22:39 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 12:07:19 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 12:07:21 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 12:08:14 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "POST /v1/quote HTTP/1.1" 200 OK
Jan 11 12:08:20 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "POST /v1/topup/request HTTP/1.1" 500 Internal Server Error
Jan 11 12:08:23 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "POST /v1/quote HTTP/1.1" 200 OK
Jan 11 12:08:42 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "POST /v1/topup/request HTTP/1.1" 500 Internal Server Error
Jan 11 14:52:26 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 14:52:28 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 15:05:52 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 15:05:54 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 15:55:19 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 15:55:21 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 16:13:41 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 16:13:43 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 16:18:03 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 16:18:05 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 16:57:25 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 16:57:27 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 17:26:09 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 11 17:26:12 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 12 06:28:07 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 12 06:28:09 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 12 07:08:51 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 12 07:08:53 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 12 08:23:03 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 12 08:23:06 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 12 08:45:36 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 12 08:45:38 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 12 09:03:59 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 12 09:04:01 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 12 09:04:03 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 12 09:04:04 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 12 09:05:17 vm15330919.example.com uvicorn[1101247]: INFO:     127.0.0.1:36192 - "GET /openapi.json HTTP/1.1" 200 OK
Jan 13 08:44:03 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 08:44:06 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 11:34:07 vm15330919.example.com uvicorn[1101248]: INFO:     127.0.0.1:56094 - "GET /openapi.json HTTP/1.1" 200 OK
Jan 13 11:44:33 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 11:44:35 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 14:52:28 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 14:52:30 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 14:53:49 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 14:53:51 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 14:54:43 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 14:54:44 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 14:58:40 vm15330919.example.com uvicorn[1101247]: INFO:     45.159.248.232:0 - "GET /v1/balances/%D1%82%D0%B2%D0%BE%D0%B9_RID HTTP/1.1" 200 OK
Jan 13 14:58:40 vm15330919.example.com uvicorn[1101247]: INFO:     45.159.248.232:0 - "GET /v1/receive/%D1%82%D0%B2%D0%BE%D0%B9_RID HTTP/1.1" 200 OK
Jan 13 15:38:03 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 15:38:05 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 15:38:05 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 15:49:36 vm15330919.example.com uvicorn[1101247]: INFO:     45.159.248.232:0 - "GET / HTTP/1.1" 200 OK
Jan 13 15:49:36 vm15330919.example.com uvicorn[1101247]: INFO:     45.159.248.232:0 - "GET /health HTTP/1.1" 404 Not Found
Jan 13 15:49:36 vm15330919.example.com uvicorn[1101247]: INFO:     45.159.248.232:0 - "GET /openapi.json HTTP/1.1" 200 OK
Jan 13 15:49:36 vm15330919.example.com uvicorn[1101247]: INFO:     45.159.248.232:0 - "GET /docs HTTP/1.1" 200 OK
Jan 13 15:49:36 vm15330919.example.com uvicorn[1101247]: INFO:     45.159.248.232:0 - "GET /swagger HTTP/1.1" 404 Not Found
Jan 13 15:54:48 vm15330919.example.com uvicorn[1101248]: INFO:     45.159.248.232:0 - "GET /openapi.json HTTP/1.1" 200 OK
Jan 13 16:14:24 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 16:14:26 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 16:14:26 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 16:14:35 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 16:14:37 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 16:14:37 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 16:22:47 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 16:22:49 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 16:22:49 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 16:28:13 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 16:28:15 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 16:28:16 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 16:28:56 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 16:28:58 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 16:28:58 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 16:36:33 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 16:36:35 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 16:36:35 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 16:47:29 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 16:47:31 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 16:47:32 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 17:11:00 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 17:11:02 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 17:11:02 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 17:31:56 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 17:31:58 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 17:31:58 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 17:34:07 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 17:34:09 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 13 17:34:09 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 06:53:02 vm15330919.example.com systemd[1]: Stopping logos-wallet-proxy.service - LOGOS Wallet Proxy (FastAPI + Uvicorn)...
Jan 14 06:53:02 vm15330919.example.com uvicorn[1101248]: INFO:     Shutting down
Jan 14 06:53:02 vm15330919.example.com uvicorn[1101247]: INFO:     Shutting down
Jan 14 06:53:02 vm15330919.example.com uvicorn[1101241]: INFO:     Received SIGTERM, exiting.
Jan 14 06:53:02 vm15330919.example.com uvicorn[1101241]: INFO:     Terminated child process [1101247]
Jan 14 06:53:02 vm15330919.example.com uvicorn[1101241]: INFO:     Terminated child process [1101248]
Jan 14 06:53:02 vm15330919.example.com uvicorn[1101241]: INFO:     Waiting for child process [1101247]
Jan 14 06:53:02 vm15330919.example.com uvicorn[1101248]: INFO:     Waiting for application shutdown.
Jan 14 06:53:02 vm15330919.example.com uvicorn[1101248]: INFO:     Application shutdown complete.
Jan 14 06:53:02 vm15330919.example.com uvicorn[1101248]: INFO:     Finished server process [1101248]
Jan 14 06:53:02 vm15330919.example.com uvicorn[1101247]: INFO:     Waiting for application shutdown.
Jan 14 06:53:02 vm15330919.example.com uvicorn[1101247]: INFO:     Application shutdown complete.
Jan 14 06:53:02 vm15330919.example.com uvicorn[1101247]: INFO:     Finished server process [1101247]
Jan 14 06:53:02 vm15330919.example.com uvicorn[1101241]: INFO:     Waiting for child process [1101248]
Jan 14 06:53:02 vm15330919.example.com uvicorn[1101241]: INFO:     Stopping parent process [1101241]
Jan 14 06:53:02 vm15330919.example.com systemd[1]: logos-wallet-proxy.service: Deactivated successfully.
Jan 14 06:53:02 vm15330919.example.com systemd[1]: Stopped logos-wallet-proxy.service - LOGOS Wallet Proxy (FastAPI + Uvicorn).
Jan 14 06:53:02 vm15330919.example.com systemd[1]: logos-wallet-proxy.service: Consumed 1h 10min 54.069s CPU time, 193.9M memory peak, 0B memory swap peak.
Jan 14 06:53:02 vm15330919.example.com systemd[1]: Starting logos-wallet-proxy.service - LOGOS Wallet Proxy (FastAPI + Uvicorn)...
Jan 14 06:53:02 vm15330919.example.com python3[1620731]: OK: init_db done -> /opt/logos/wallet-proxy/wallet_proxy.db
Jan 14 06:53:02 vm15330919.example.com systemd[1]: Started logos-wallet-proxy.service - LOGOS Wallet Proxy (FastAPI + Uvicorn).
Jan 14 06:53:02 vm15330919.example.com uvicorn[1620733]: INFO:     Uvicorn running on http://0.0.0.0:9090 (Press CTRL+C to quit)
Jan 14 06:53:02 vm15330919.example.com uvicorn[1620733]: INFO:     Started parent process [1620733]
Jan 14 06:53:05 vm15330919.example.com uvicorn[1620739]: INFO:     Started server process [1620739]
Jan 14 06:53:05 vm15330919.example.com uvicorn[1620739]: INFO:     Waiting for application startup.
Jan 14 06:53:05 vm15330919.example.com uvicorn[1620739]: INFO:     Application startup complete.
Jan 14 06:53:05 vm15330919.example.com uvicorn[1620738]: INFO:     Started server process [1620738]
Jan 14 06:53:05 vm15330919.example.com uvicorn[1620738]: INFO:     Waiting for application startup.
Jan 14 06:53:05 vm15330919.example.com uvicorn[1620738]: INFO:     Application startup complete.
Jan 14 06:54:05 vm15330919.example.com uvicorn[1620738]: INFO Web3 connected: 0xdAC17F958D2ee523a2206206994597C13D831ec7
Jan 14 06:54:05 vm15330919.example.com uvicorn[1620738]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 06:54:07 vm15330919.example.com uvicorn[1620739]: INFO Web3 connected: 0xdAC17F958D2ee523a2206206994597C13D831ec7
Jan 14 06:54:07 vm15330919.example.com uvicorn[1620739]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 06:54:07 vm15330919.example.com uvicorn[1620738]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 07:12:49 vm15330919.example.com uvicorn[1620738]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 07:12:51 vm15330919.example.com uvicorn[1620738]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 07:12:51 vm15330919.example.com uvicorn[1620738]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 07:17:41 vm15330919.example.com uvicorn[1620738]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 07:17:43 vm15330919.example.com uvicorn[1620738]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 07:17:43 vm15330919.example.com uvicorn[1620738]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 07:18:13 vm15330919.example.com uvicorn[1620738]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 07:18:15 vm15330919.example.com uvicorn[1620738]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 07:18:15 vm15330919.example.com uvicorn[1620739]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 07:58:57 vm15330919.example.com uvicorn[1620739]: INFO:     156.246.151.196:0 - "GET /v1/receive/DCaZAAbQMPfJaFwNgzw5sPqZ2E5E7LZh1x5psi15NYio HTTP/1.1" 200 OK
Jan 14 07:58:59 vm15330919.example.com uvicorn[1620738]: INFO:     156.246.151.196:0 - "GET /v1/balances/DCaZAAbQMPfJaFwNgzw5sPqZ2E5E7LZh1x5psi15NYio HTTP/1.1" 200 OK
Jan 14 07:58:59 vm15330919.example.com uvicorn[1620739]: INFO:     156.246.151.196:0 - "GET /v1/balances/DCaZAAbQMPfJaFwNgzw5sPqZ2E5E7LZh1x5psi15NYio HTTP/1.1" 200 OK
Jan 14 08:07:34 vm15330919.example.com uvicorn[1620739]: INFO:     156.246.151.196:0 - "GET /v1/receive/DCaZAAbQMPfJaFwNgzw5sPqZ2E5E7LZh1x5psi15NYio HTTP/1.1" 200 OK
Jan 14 08:07:36 vm15330919.example.com uvicorn[1620739]: INFO:     156.246.151.196:0 - "GET /v1/balances/DCaZAAbQMPfJaFwNgzw5sPqZ2E5E7LZh1x5psi15NYio HTTP/1.1" 200 OK
Jan 14 08:07:36 vm15330919.example.com uvicorn[1620739]: INFO:     156.246.151.196:0 - "GET /v1/balances/DCaZAAbQMPfJaFwNgzw5sPqZ2E5E7LZh1x5psi15NYio HTTP/1.1" 200 OK
Jan 14 08:09:49 vm15330919.example.com uvicorn[1620739]: INFO:     156.246.151.196:0 - "GET /v1/receive/DCaZAAbQMPfJaFwNgzw5sPqZ2E5E7LZh1x5psi15NYio HTTP/1.1" 200 OK
Jan 14 08:09:51 vm15330919.example.com uvicorn[1620739]: INFO:     156.246.151.196:0 - "GET /v1/balances/DCaZAAbQMPfJaFwNgzw5sPqZ2E5E7LZh1x5psi15NYio HTTP/1.1" 200 OK
Jan 14 08:09:51 vm15330919.example.com uvicorn[1620739]: INFO:     156.246.151.196:0 - "GET /v1/balances/DCaZAAbQMPfJaFwNgzw5sPqZ2E5E7LZh1x5psi15NYio HTTP/1.1" 200 OK
Jan 14 08:10:26 vm15330919.example.com uvicorn[1620738]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 08:10:28 vm15330919.example.com uvicorn[1620738]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 08:10:28 vm15330919.example.com uvicorn[1620738]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 08:33:14 vm15330919.example.com uvicorn[1620738]: INFO:     156.246.151.196:0 - "GET /v1/receive/DCaZAAbQMPfJaFwNgzw5sPqZ2E5E7LZh1x5psi15NYio HTTP/1.1" 200 OK
Jan 14 08:33:16 vm15330919.example.com uvicorn[1620739]: INFO:     156.246.151.196:0 - "GET /v1/balances/DCaZAAbQMPfJaFwNgzw5sPqZ2E5E7LZh1x5psi15NYio HTTP/1.1" 200 OK
Jan 14 08:33:31 vm15330919.example.com uvicorn[1620738]: INFO:     156.246.151.196:0 - "GET /v1/receive/DCaZAAbQMPfJaFwNgzw5sPqZ2E5E7LZh1x5psi15NYio HTTP/1.1" 200 OK
Jan 14 08:33:33 vm15330919.example.com uvicorn[1620739]: INFO:     156.246.151.196:0 - "GET /v1/balances/DCaZAAbQMPfJaFwNgzw5sPqZ2E5E7LZh1x5psi15NYio HTTP/1.1" 200 OK
Jan 14 08:33:33 vm15330919.example.com uvicorn[1620738]: INFO:     156.246.151.196:0 - "GET /v1/balances/DCaZAAbQMPfJaFwNgzw5sPqZ2E5E7LZh1x5psi15NYio HTTP/1.1" 200 OK
Jan 14 08:40:19 vm15330919.example.com uvicorn[1620739]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 08:40:21 vm15330919.example.com uvicorn[1620739]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 08:40:21 vm15330919.example.com uvicorn[1620739]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 08:50:13 vm15330919.example.com uvicorn[1620739]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 08:50:16 vm15330919.example.com uvicorn[1620739]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 08:50:16 vm15330919.example.com uvicorn[1620739]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 09:06:36 vm15330919.example.com uvicorn[1620739]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 09:06:39 vm15330919.example.com uvicorn[1620739]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 09:06:39 vm15330919.example.com uvicorn[1620739]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 09:27:55 vm15330919.example.com uvicorn[1620739]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 09:27:57 vm15330919.example.com uvicorn[1620739]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 09:27:57 vm15330919.example.com uvicorn[1620738]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 10:06:14 vm15330919.example.com uvicorn[1620738]: INFO:     156.246.151.196:0 - "GET /v1/receive/Atx9FPoB652QY1FR2PB4quBJsdjt9fhHoHL2pMe5yec6JUc HTTP/1.1" 200 OK
Jan 14 10:06:16 vm15330919.example.com uvicorn[1620738]: INFO:     156.246.151.196:0 - "GET /v1/balances/Atx9FPoB652QY1FR2PB4quBJsdjt9fhHoHL2pMe5yec6JUc HTTP/1.1" 200 OK
Jan 14 10:06:16 vm15330919.example.com uvicorn[1620738]: INFO:     156.246.151.196:0 - "GET /v1/balances/Atx9FPoB652QY1FR2PB4quBJsdjt9fhHoHL2pMe5yec6JUc HTTP/1.1" 200 OK
Jan 14 10:07:11 vm15330919.example.com uvicorn[1620738]: INFO:     156.246.151.196:0 - "GET /v1/receive/Atx9FPoB652QY1FR2PB4quBJsdjt9fhHoHL2pMe5yec6JUc HTTP/1.1" 200 OK
Jan 14 10:07:12 vm15330919.example.com uvicorn[1620738]: INFO:     156.246.151.196:0 - "GET /v1/balances/Atx9FPoB652QY1FR2PB4quBJsdjt9fhHoHL2pMe5yec6JUc HTTP/1.1" 200 OK
Jan 14 10:07:12 vm15330919.example.com uvicorn[1620738]: INFO:     156.246.151.196:0 - "GET /v1/balances/Atx9FPoB652QY1FR2PB4quBJsdjt9fhHoHL2pMe5yec6JUc HTTP/1.1" 200 OK
Jan 14 10:29:47 vm15330919.example.com uvicorn[1620739]: INFO:     156.246.151.196:0 - "GET /v1/receive/Atx4SLUk7Fd3H3x8ohzz4mjJr8VdpTZnfy5VFHox9VhQG1Q HTTP/1.1" 200 OK
Jan 14 10:29:50 vm15330919.example.com uvicorn[1620738]: INFO:     156.246.151.196:0 - "GET /v1/balances/Atx4SLUk7Fd3H3x8ohzz4mjJr8VdpTZnfy5VFHox9VhQG1Q HTTP/1.1" 200 OK
Jan 14 10:29:50 vm15330919.example.com uvicorn[1620739]: INFO:     156.246.151.196:0 - "GET /v1/balances/Atx4SLUk7Fd3H3x8ohzz4mjJr8VdpTZnfy5VFHox9VhQG1Q HTTP/1.1" 200 OK
Jan 14 10:40:35 vm15330919.example.com uvicorn[1620738]: INFO:     156.246.151.196:0 - "GET /v1/receive/Atx4SLUk7Fd3H3x8ohzz4mjJr8VdpTZnfy5VFHox9VhQG1Q HTTP/1.1" 200 OK
Jan 14 10:40:37 vm15330919.example.com uvicorn[1620738]: INFO:     156.246.151.196:0 - "GET /v1/balances/Atx4SLUk7Fd3H3x8ohzz4mjJr8VdpTZnfy5VFHox9VhQG1Q HTTP/1.1" 200 OK
Jan 14 10:40:37 vm15330919.example.com uvicorn[1620738]: INFO:     156.246.151.196:0 - "GET /v1/balances/Atx4SLUk7Fd3H3x8ohzz4mjJr8VdpTZnfy5VFHox9VhQG1Q HTTP/1.1" 200 OK
Jan 14 10:41:16 vm15330919.example.com uvicorn[1620738]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 10:41:18 vm15330919.example.com uvicorn[1620738]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 10:41:18 vm15330919.example.com uvicorn[1620738]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 12:06:11 vm15330919.example.com uvicorn[1620739]: INFO:     77.91.123.72:0 - "GET /v1/receive/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 12:06:13 vm15330919.example.com uvicorn[1620738]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 12:06:13 vm15330919.example.com uvicorn[1620739]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 14 12:18:38 vm15330919.example.com uvicorn[1620738]: INFO:     127.0.0.1:40220 - "GET /openapi.json HTTP/1.1" 200 OK
Jan 14 12:18:38 vm15330919.example.com uvicorn[1620738]: INFO:     127.0.0.1:40226 - "GET / HTTP/1.1" 200 OK

```

## JOURNALCTL -u lrb-scanner -n 300

```
Jan 15 11:14:43 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:14:43 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:14:43 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:14:43 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:14:43 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:14:43 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:14:43 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:14:43 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:14:43 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:14:43 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:14:43 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:14:43 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:14:43 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:14:43 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:14:43 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:14:43 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:14:43 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:14:43 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:14:43 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:14:43 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:14:43 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:14:43 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:14:43 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:14:43 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:14:43 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:14:43 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:14:43 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:14:43 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:14:43 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:14:43 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 11:51:02 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 11:51:02 vm15330919.example.com python[1620726]: FROM kv
Jan 15 11:51:02 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 11:51:02 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)

```

## JOURNALCTL -u logos-node@main -n 300

```
Jan 06 13:59:34 vm15330919.example.com systemd[1]: /etc/systemd/system/logos-node@.service:21: System call ~keyctl is not known, ignoring.
Jan 06 13:59:34 vm15330919.example.com systemd[1]: /etc/systemd/system/logos-node@.service.d/10-restart-policy.conf:4: Unknown key name 'StartLimitIntervalSec' in section 'Service', ignoring.
Jan 06 14:00:01 vm15330919.example.com systemd[1]: /etc/systemd/system/logos-node@.service:21: System call ~keyctl is not known, ignoring.
Jan 06 14:00:01 vm15330919.example.com systemd[1]: /etc/systemd/system/logos-node@.service.d/10-restart-policy.conf:4: Unknown key name 'StartLimitIntervalSec' in section 'Service', ignoring.
Jan 06 15:28:41 vm15330919.example.com systemd[1]: /etc/systemd/system/logos-node@.service:21: System call ~keyctl is not known, ignoring.
Jan 06 15:28:41 vm15330919.example.com systemd[1]: /etc/systemd/system/logos-node@.service.d/10-restart-policy.conf:4: Unknown key name 'StartLimitIntervalSec' in section 'Service', ignoring.
Jan 06 16:58:13 vm15330919.example.com systemd[1]: /etc/systemd/system/logos-node@.service:21: System call ~keyctl is not known, ignoring.
Jan 06 16:58:13 vm15330919.example.com systemd[1]: /etc/systemd/system/logos-node@.service.d/10-restart-policy.conf:4: Unknown key name 'StartLimitIntervalSec' in section 'Service', ignoring.
Jan 07 03:41:43 vm15330919.example.com systemd[1]: Stopping logos-node@main.service - LOGOS LRB Node (main)...
Jan 07 03:41:43 vm15330919.example.com systemd[1]: logos-node@main.service: Deactivated successfully.
Jan 07 03:41:43 vm15330919.example.com systemd[1]: Stopped logos-node@main.service - LOGOS LRB Node (main).
Jan 07 03:41:43 vm15330919.example.com systemd[1]: logos-node@main.service: Consumed 1min 23.349s CPU time, 608.7M memory peak, 0B memory swap peak.
Jan 07 03:42:51 vm15330919.example.com systemd[1]: Started logos-node@main.service - LOGOS LRB Node (main).
Jan 07 03:42:52 vm15330919.example.com logos_node[1078567]: 2026-01-07T03:42:52.171495Z  WARN logos_node: archive disabled
Jan 07 03:42:52 vm15330919.example.com logos_node[1078567]: 2026-01-07T03:42:52.171525Z  INFO logos_node: producer start
Jan 07 03:42:52 vm15330919.example.com logos_node[1078567]: 2026-01-07T03:42:52.171530Z  INFO logos_node::producer: producer: local block production is disabled in this build; node operates as follower (ledger + archive + bridge).
Jan 07 03:42:52 vm15330919.example.com logos_node[1078567]: 2026-01-07T03:42:52.171604Z  INFO logos_node: logos_node listening on 0.0.0.0:8080
Jan 08 03:40:58 vm15330919.example.com systemd[1]: Stopping logos-node@main.service - LOGOS LRB Node (main)...
Jan 08 03:40:58 vm15330919.example.com systemd[1]: logos-node@main.service: Deactivated successfully.
Jan 08 03:40:58 vm15330919.example.com systemd[1]: Stopped logos-node@main.service - LOGOS LRB Node (main).
Jan 08 03:40:58 vm15330919.example.com systemd[1]: logos-node@main.service: Consumed 1min 24.063s CPU time.
Jan 08 03:42:04 vm15330919.example.com systemd[1]: Started logos-node@main.service - LOGOS LRB Node (main).
Jan 08 03:42:04 vm15330919.example.com logos_node[1155803]: 2026-01-08T03:42:04.927582Z  WARN logos_node: archive disabled
Jan 08 03:42:04 vm15330919.example.com logos_node[1155803]: 2026-01-08T03:42:04.927613Z  INFO logos_node: producer start
Jan 08 03:42:04 vm15330919.example.com logos_node[1155803]: 2026-01-08T03:42:04.927618Z  INFO logos_node::producer: producer: local block production is disabled in this build; node operates as follower (ledger + archive + bridge).
Jan 08 03:42:04 vm15330919.example.com logos_node[1155803]: 2026-01-08T03:42:04.927693Z  INFO logos_node: logos_node listening on 0.0.0.0:8080
Jan 09 03:40:28 vm15330919.example.com systemd[1]: Stopping logos-node@main.service - LOGOS LRB Node (main)...
Jan 09 03:40:28 vm15330919.example.com systemd[1]: logos-node@main.service: Deactivated successfully.
Jan 09 03:40:28 vm15330919.example.com systemd[1]: Stopped logos-node@main.service - LOGOS LRB Node (main).
Jan 09 03:40:28 vm15330919.example.com systemd[1]: logos-node@main.service: Consumed 1min 29.501s CPU time.
Jan 09 03:41:36 vm15330919.example.com systemd[1]: Started logos-node@main.service - LOGOS LRB Node (main).
Jan 09 03:41:36 vm15330919.example.com logos_node[1231457]: 2026-01-09T03:41:36.756095Z  WARN logos_node: archive disabled
Jan 09 03:41:36 vm15330919.example.com logos_node[1231457]: 2026-01-09T03:41:36.756132Z  INFO logos_node: producer start
Jan 09 03:41:36 vm15330919.example.com logos_node[1231457]: 2026-01-09T03:41:36.756139Z  INFO logos_node::producer: producer: local block production is disabled in this build; node operates as follower (ledger + archive + bridge).
Jan 09 03:41:36 vm15330919.example.com logos_node[1231457]: 2026-01-09T03:41:36.756265Z  INFO logos_node: logos_node listening on 0.0.0.0:8080
Jan 10 03:42:34 vm15330919.example.com systemd[1]: Stopping logos-node@main.service - LOGOS LRB Node (main)...
Jan 10 03:42:34 vm15330919.example.com systemd[1]: logos-node@main.service: Deactivated successfully.
Jan 10 03:42:34 vm15330919.example.com systemd[1]: Stopped logos-node@main.service - LOGOS LRB Node (main).
Jan 10 03:42:34 vm15330919.example.com systemd[1]: logos-node@main.service: Consumed 1min 30.076s CPU time.
Jan 10 03:43:39 vm15330919.example.com systemd[1]: Started logos-node@main.service - LOGOS LRB Node (main).
Jan 10 03:43:40 vm15330919.example.com logos_node[1306682]: 2026-01-10T03:43:40.079748Z  WARN logos_node: archive disabled
Jan 10 03:43:40 vm15330919.example.com logos_node[1306682]: 2026-01-10T03:43:40.079793Z  INFO logos_node: producer start
Jan 10 03:43:40 vm15330919.example.com logos_node[1306682]: 2026-01-10T03:43:40.079798Z  INFO logos_node::producer: producer: local block production is disabled in this build; node operates as follower (ledger + archive + bridge).
Jan 10 03:43:40 vm15330919.example.com logos_node[1306682]: 2026-01-10T03:43:40.079874Z  INFO logos_node: logos_node listening on 0.0.0.0:8080
Jan 11 03:40:27 vm15330919.example.com systemd[1]: Stopping logos-node@main.service - LOGOS LRB Node (main)...
Jan 11 03:40:27 vm15330919.example.com systemd[1]: logos-node@main.service: Deactivated successfully.
Jan 11 03:40:27 vm15330919.example.com systemd[1]: Stopped logos-node@main.service - LOGOS LRB Node (main).
Jan 11 03:40:27 vm15330919.example.com systemd[1]: logos-node@main.service: Consumed 1min 36.315s CPU time.
Jan 11 03:41:29 vm15330919.example.com systemd[1]: Started logos-node@main.service - LOGOS LRB Node (main).
Jan 11 03:41:30 vm15330919.example.com logos_node[1383123]: 2026-01-11T03:41:30.333373Z  WARN logos_node: archive disabled
Jan 11 03:41:30 vm15330919.example.com logos_node[1383123]: 2026-01-11T03:41:30.333409Z  INFO logos_node: producer start
Jan 11 03:41:30 vm15330919.example.com logos_node[1383123]: 2026-01-11T03:41:30.333414Z  INFO logos_node::producer: producer: local block production is disabled in this build; node operates as follower (ledger + archive + bridge).
Jan 11 03:41:30 vm15330919.example.com logos_node[1383123]: 2026-01-11T03:41:30.333484Z  INFO logos_node: logos_node listening on 0.0.0.0:8080
Jan 12 03:40:05 vm15330919.example.com systemd[1]: Stopping logos-node@main.service - LOGOS LRB Node (main)...
Jan 12 03:40:05 vm15330919.example.com systemd[1]: logos-node@main.service: Deactivated successfully.
Jan 12 03:40:05 vm15330919.example.com systemd[1]: Stopped logos-node@main.service - LOGOS LRB Node (main).
Jan 12 03:40:05 vm15330919.example.com systemd[1]: logos-node@main.service: Consumed 1min 18.307s CPU time.
Jan 12 03:41:09 vm15330919.example.com systemd[1]: Started logos-node@main.service - LOGOS LRB Node (main).
Jan 12 03:41:09 vm15330919.example.com logos_node[1460586]: 2026-01-12T03:41:09.965919Z  WARN logos_node: archive disabled
Jan 12 03:41:09 vm15330919.example.com logos_node[1460586]: 2026-01-12T03:41:09.965992Z  INFO logos_node: producer start
Jan 12 03:41:09 vm15330919.example.com logos_node[1460586]: 2026-01-12T03:41:09.966027Z  INFO logos_node::producer: producer: local block production is disabled in this build; node operates as follower (ledger + archive + bridge).
Jan 12 03:41:09 vm15330919.example.com logos_node[1460586]: 2026-01-12T03:41:09.966179Z  INFO logos_node: logos_node listening on 0.0.0.0:8080
Jan 13 03:40:40 vm15330919.example.com systemd[1]: Stopping logos-node@main.service - LOGOS LRB Node (main)...
Jan 13 03:40:40 vm15330919.example.com systemd[1]: logos-node@main.service: Deactivated successfully.
Jan 13 03:40:40 vm15330919.example.com systemd[1]: Stopped logos-node@main.service - LOGOS LRB Node (main).
Jan 13 03:40:40 vm15330919.example.com systemd[1]: logos-node@main.service: Consumed 1min 20.819s CPU time.
Jan 13 03:41:41 vm15330919.example.com systemd[1]: Started logos-node@main.service - LOGOS LRB Node (main).
Jan 13 03:41:42 vm15330919.example.com logos_node[1534305]: 2026-01-13T03:41:42.611148Z  WARN logos_node: archive disabled
Jan 13 03:41:42 vm15330919.example.com logos_node[1534305]: 2026-01-13T03:41:42.611187Z  INFO logos_node: producer start
Jan 13 03:41:42 vm15330919.example.com logos_node[1534305]: 2026-01-13T03:41:42.611192Z  INFO logos_node::producer: producer: local block production is disabled in this build; node operates as follower (ledger + archive + bridge).
Jan 13 03:41:42 vm15330919.example.com logos_node[1534305]: 2026-01-13T03:41:42.611263Z  INFO logos_node: logos_node listening on 0.0.0.0:8080
Jan 14 03:40:28 vm15330919.example.com systemd[1]: Stopping logos-node@main.service - LOGOS LRB Node (main)...
Jan 14 03:40:28 vm15330919.example.com systemd[1]: logos-node@main.service: Deactivated successfully.
Jan 14 03:40:28 vm15330919.example.com systemd[1]: Stopped logos-node@main.service - LOGOS LRB Node (main).
Jan 14 03:40:28 vm15330919.example.com systemd[1]: logos-node@main.service: Consumed 1min 18.975s CPU time, 171.6M memory peak, 0B memory swap peak.
Jan 14 03:41:28 vm15330919.example.com systemd[1]: Started logos-node@main.service - LOGOS LRB Node (main).
Jan 14 03:41:29 vm15330919.example.com logos_node[1610448]: 2026-01-14T03:41:29.603715Z  WARN logos_node: archive disabled
Jan 14 03:41:29 vm15330919.example.com logos_node[1610448]: 2026-01-14T03:41:29.603753Z  INFO logos_node: producer start
Jan 14 03:41:29 vm15330919.example.com logos_node[1610448]: 2026-01-14T03:41:29.603759Z  INFO logos_node::producer: producer: local block production is disabled in this build; node operates as follower (ledger + archive + bridge).
Jan 14 03:41:29 vm15330919.example.com logos_node[1610448]: 2026-01-14T03:41:29.603830Z  INFO logos_node: logos_node listening on 0.0.0.0:8080
Jan 15 03:41:38 vm15330919.example.com systemd[1]: Stopping logos-node@main.service - LOGOS LRB Node (main)...
Jan 15 03:41:38 vm15330919.example.com systemd[1]: logos-node@main.service: Deactivated successfully.
Jan 15 03:41:38 vm15330919.example.com systemd[1]: Stopped logos-node@main.service - LOGOS LRB Node (main).
Jan 15 03:41:38 vm15330919.example.com systemd[1]: logos-node@main.service: Consumed 1min 14.697s CPU time, 168.4M memory peak, 0B memory swap peak.
Jan 15 03:42:43 vm15330919.example.com systemd[1]: Started logos-node@main.service - LOGOS LRB Node (main).
Jan 15 03:42:46 vm15330919.example.com logos_node[1693815]: 2026-01-15T03:42:46.666042Z  WARN logos_node: archive disabled
Jan 15 03:42:46 vm15330919.example.com logos_node[1693815]: 2026-01-15T03:42:46.666082Z  INFO logos_node: producer start
Jan 15 03:42:46 vm15330919.example.com logos_node[1693815]: 2026-01-15T03:42:46.666088Z  INFO logos_node::producer: producer: local block production is disabled in this build; node operates as follower (ledger + archive + bridge).
Jan 15 03:42:46 vm15330919.example.com logos_node[1693815]: 2026-01-15T03:42:46.666162Z  INFO logos_node: logos_node listening on 0.0.0.0:8080

```

## JOURNALCTL -u logos-node -n 300

```
-- No entries --

```

## JOURNALCTL -u lrb-proxy -n 300

```
Jan 06 14:01:07 vm15330919.example.com uvicorn[1017301]: INFO:     127.0.0.1:44554 - "GET /v1/receive/RID_HERE HTTP/1.1" 500 Internal Server Error
Jan 06 14:01:36 vm15330919.example.com uvicorn[1017301]: INFO:     45.159.248.232:0 - "GET /v1/receive/RID_HERE HTTP/1.1" 500 Internal Server Error
Jan 06 14:01:53 vm15330919.example.com uvicorn[1017301]: INFO:     45.159.248.232:0 - "GET /v1/receive/RID_HERE HTTP/1.1" 500 Internal Server Error
Jan 06 14:14:38 vm15330919.example.com uvicorn[1017301]: INFO:     127.0.0.1:48820 - "GET /v1/receive/RID_HERE HTTP/1.1" 500 Internal Server Error
Jan 06 14:14:51 vm15330919.example.com uvicorn[1017302]: INFO:     45.159.248.232:0 - "GET /v1/receive/RID_HERE HTTP/1.1" 500 Internal Server Error
Jan 06 14:23:53 vm15330919.example.com systemd[1]: lrb-proxy.service: Main process exited, code=killed, status=9/KILL
Jan 06 14:23:53 vm15330919.example.com systemd[1]: lrb-proxy.service: Failed with result 'signal'.
Jan 06 14:23:53 vm15330919.example.com systemd[1]: lrb-proxy.service: Consumed 1min 11.330s CPU time, 206.8M memory peak, 0B memory swap peak.
Jan 06 14:23:55 vm15330919.example.com systemd[1]: lrb-proxy.service: Scheduled restart job, restart counter is at 2.
Jan 06 14:23:56 vm15330919.example.com systemd[1]: Started lrb-proxy.service - LOGOS Wallet Proxy (FastAPI on :9090).
Jan 06 14:23:56 vm15330919.example.com uvicorn[1035001]: INFO:     Uvicorn running on http://0.0.0.0:9090 (Press CTRL+C to quit)
Jan 06 14:23:56 vm15330919.example.com uvicorn[1035001]: INFO:     Started parent process [1035001]
Jan 06 14:23:58 vm15330919.example.com uvicorn[1035004]: INFO:     Started server process [1035004]
Jan 06 14:23:58 vm15330919.example.com uvicorn[1035004]: INFO:     Waiting for application startup.
Jan 06 14:23:58 vm15330919.example.com uvicorn[1035004]: INFO:     Application startup complete.
Jan 06 14:23:58 vm15330919.example.com uvicorn[1035005]: INFO:     Started server process [1035005]
Jan 06 14:23:58 vm15330919.example.com uvicorn[1035005]: INFO:     Waiting for application startup.
Jan 06 14:23:58 vm15330919.example.com uvicorn[1035005]: INFO:     Application startup complete.
Jan 14 06:53:02 vm15330919.example.com uvicorn[1035004]: INFO:     Shutting down
Jan 14 06:53:02 vm15330919.example.com systemd[1]: Stopping lrb-proxy.service - LOGOS Wallet Proxy (FastAPI on :9090)...
Jan 14 06:53:02 vm15330919.example.com uvicorn[1035005]: INFO:     Shutting down
Jan 14 06:53:02 vm15330919.example.com uvicorn[1035001]: INFO:     Received SIGTERM, exiting.
Jan 14 06:53:02 vm15330919.example.com uvicorn[1035001]: INFO:     Terminated child process [1035004]
Jan 14 06:53:02 vm15330919.example.com uvicorn[1035001]: INFO:     Terminated child process [1035005]
Jan 14 06:53:02 vm15330919.example.com uvicorn[1035001]: INFO:     Waiting for child process [1035004]
Jan 14 06:53:02 vm15330919.example.com uvicorn[1035004]: INFO:     Waiting for application shutdown.
Jan 14 06:53:02 vm15330919.example.com uvicorn[1035004]: INFO:     Application shutdown complete.
Jan 14 06:53:02 vm15330919.example.com uvicorn[1035004]: INFO:     Finished server process [1035004]
Jan 14 06:53:02 vm15330919.example.com uvicorn[1035005]: INFO:     Waiting for application shutdown.
Jan 14 06:53:02 vm15330919.example.com uvicorn[1035005]: INFO:     Application shutdown complete.
Jan 14 06:53:02 vm15330919.example.com uvicorn[1035005]: INFO:     Finished server process [1035005]
Jan 14 06:53:02 vm15330919.example.com uvicorn[1035001]: INFO:     Waiting for child process [1035005]
Jan 14 06:53:02 vm15330919.example.com uvicorn[1035001]: INFO:     Stopping parent process [1035001]
Jan 14 06:53:02 vm15330919.example.com systemd[1]: lrb-proxy.service: Deactivated successfully.
Jan 14 06:53:02 vm15330919.example.com systemd[1]: Stopped lrb-proxy.service - LOGOS Wallet Proxy (FastAPI on :9090).
Jan 14 06:53:02 vm15330919.example.com systemd[1]: lrb-proxy.service: Consumed 1h 15min 30.728s CPU time, 180.5M memory peak, 0B memory swap peak.
Jan 14 06:53:02 vm15330919.example.com systemd[1]: Started lrb-proxy.service - LOGOS Wallet Proxy (FastAPI on :9090).
Jan 14 06:53:02 vm15330919.example.com uvicorn[1620728]: INFO:     Uvicorn running on http://0.0.0.0:9090 (Press CTRL+C to quit)
Jan 14 06:53:02 vm15330919.example.com uvicorn[1620728]: INFO:     Started parent process [1620728]
Jan 14 06:53:05 vm15330919.example.com uvicorn[1620736]: INFO:     Started server process [1620736]
Jan 14 06:53:05 vm15330919.example.com uvicorn[1620736]: INFO:     Waiting for application startup.
Jan 14 06:53:05 vm15330919.example.com uvicorn[1620736]: INFO:     Application startup complete.
Jan 14 06:53:05 vm15330919.example.com uvicorn[1620735]: INFO:     Started server process [1620735]
Jan 14 06:53:05 vm15330919.example.com uvicorn[1620735]: INFO:     Waiting for application startup.
Jan 14 06:53:05 vm15330919.example.com uvicorn[1620735]: INFO:     Application startup complete.

```

## JOURNALCTL -u logos_wallet_api -n 300

```
-- No entries --

```

## JOURNALCTL -u logos_node_backend -n 300

```
-- No entries --

```

## NGINX LOG TAIL: /var/log/nginx/error.log

```
2026/01/15 02:25:51 [error] 1568902#1568902: *86063 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.71.184.86, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 02:26:57 [error] 1568902#1568902: *86065 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.71.247.8, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 02:27:17 [error] 1568902#1568902: *86067 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.69.50.218, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 02:28:27 [error] 1568902#1568902: *86068 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.68.10.193, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 02:41:39 [error] 1568902#1568902: *86074 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.183, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 02:42:04 [error] 1568902#1568902: *86076 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.98, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 02:43:28 [error] 1568902#1568902: *86077 open() "/opt/logos/www/index.php" failed (2: No such file or directory), client: 162.158.178.212, server: mw-expedition.com, request: "POST /index.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 02:43:28 [error] 1568902#1568902: *86077 open() "/opt/logos/www/admin" failed (2: No such file or directory), client: 162.158.178.212, server: mw-expedition.com, request: "POST /admin HTTP/2.0", host: "logosblockchain.com"
2026/01/15 02:43:38 [error] 1568902#1568902: *86079 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.99, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 02:44:17 [error] 1568902#1568902: *86082 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.217.56, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 02:45:32 [error] 1568902#1568902: *86086 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.99, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 02:45:37 [error] 1568902#1568902: *86087 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.182, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 02:58:30 [error] 1568902#1568902: *86102 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.71.184.87, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 02:59:24 [error] 1568902#1568902: *86104 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 162.158.110.45, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 02:59:29 [error] 1568902#1568902: *86105 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.68.10.192, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 03:00:46 [error] 1568902#1568902: *86106 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.71.184.87, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 03:17:59 [error] 1568902#1568902: *86113 "/opt/logos/www/webui/index.html" is not found (2: No such file or directory), client: 64.62.197.197, server: mw-expedition.com, request: "GET /webui/ HTTP/1.1", host: "45.159.248.232"
2026/01/15 03:18:04 [error] 1568902#1568902: *86115 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.68.10.192, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 03:20:19 [error] 1568902#1568902: *86128 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.68.10.193, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 03:20:24 [error] 1568902#1568902: *86129 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.71.184.87, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 03:21:20 [error] 1568902#1568902: *86136 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.69.151.229, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 03:25:15 [error] 1568902#1568902: *86139 open() "/opt/logos/www/ads.txt" failed (2: No such file or directory), client: 172.68.22.59, server: mw-expedition.com, request: "GET /ads.txt HTTP/2.0", host: "logosblockchain.com"
2026/01/15 03:32:40 [error] 1568902#1568902: *86141 "/opt/logos/www/geoserver/web/index.html" is not found (2: No such file or directory), client: 64.62.197.197, server: mw-expedition.com, request: "GET /geoserver/web/ HTTP/1.1", host: "45.159.248.232"
2026/01/15 03:34:48 [error] 1568902#1568902: *86143 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.71.184.87, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 03:36:14 [error] 1568902#1568902: *86144 open() "/opt/logos/www/.git/config" failed (2: No such file or directory), client: 64.62.197.197, server: mw-expedition.com, request: "GET /.git/config HTTP/1.1", host: "45.159.248.232"
2026/01/15 03:36:25 [error] 1568902#1568902: *86145 open() "/opt/logos/www/airdrop.html" failed (2: No such file or directory), client: 108.162.216.50, server: mw-expedition.com, request: "GET /airdrop.html HTTP/2.0", host: "logosblockchain.com"
2026/01/15 03:37:26 [error] 1568902#1568902: *86146 open() "/opt/logos/www/SDK/webLanguage" failed (2: No such file or directory), client: 5.187.35.158, server: mw-expedition.com, request: "GET /SDK/webLanguage HTTP/1.1", host: "45.159.248.232:443"
2026/01/15 03:37:34 [error] 1568902#1568902: *86148 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.70.248.2, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 03:38:28 [error] 1568902#1568902: *86149 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.71.184.86, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 03:38:33 [error] 1568902#1568902: *86149 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.71.184.86, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 03:44:43 [error] 1568902#1568902: *86150 open() "/opt/logos/www/robots.txt" failed (2: No such file or directory), client: 47.128.18.41, server: mw-expedition.com, request: "GET /robots.txt HTTP/1.1", host: "mw-expedition.com"
2026/01/15 03:50:22 [error] 1568902#1568902: *86153 open() "/opt/logos/www/robots.txt" failed (2: No such file or directory), client: 47.128.62.230, server: mw-expedition.com, request: "GET /robots.txt HTTP/1.1", host: "mw-expedition.com"
2026/01/15 03:53:15 [error] 1568902#1568902: *86157 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.217.101, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 03:55:13 [error] 1568902#1568902: *86159 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.182, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 03:55:26 [error] 1568902#1568902: *86159 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.182, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 03:55:51 [error] 1568902#1568902: *86164 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.98, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 04:11:30 [error] 1568902#1568902: *86170 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.68.10.192, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 04:12:12 [error] 1568902#1568902: *86172 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.71.184.87, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 04:12:12 [error] 1568902#1568902: *86172 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.71.184.87, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 04:13:12 [error] 1568902#1568902: *86173 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.68.10.193, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 04:20:41 [error] 1568902#1568902: *86175 open() "/opt/logos/www/+CSCOL+/Java.jar" failed (2: No such file or directory), client: 152.42.175.85, server: mw-expedition.com, request: "GET /+CSCOL+/Java.jar HTTP/1.1", host: "45.159.248.232"
2026/01/15 04:20:43 [error] 1568902#1568902: *86177 open() "/opt/logos/www/+CSCOL+/a1.jar" failed (2: No such file or directory), client: 152.42.175.85, server: mw-expedition.com, request: "GET /+CSCOL+/a1.jar HTTP/1.1", host: "45.159.248.232"
2026/01/15 04:29:26 [error] 1568902#1568902: *86182 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.68.10.193, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 04:29:31 [error] 1568902#1568902: *86183 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 162.158.94.33, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 04:29:31 [error] 1568902#1568902: *86185 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.71.184.87, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 04:32:02 [error] 1568902#1568902: *86187 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.68.10.193, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 04:33:05 [error] 1568902#1568902: *86189 open() "/opt/logos/www/style.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /style.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/style.php"
2026/01/15 04:33:07 [error] 1568902#1568902: *86189 open() "/opt/logos/www/wp-content/style.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /wp-content/style.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/wp-content/style.php"
2026/01/15 04:33:07 [error] 1568902#1568902: *86189 open() "/opt/logos/www/wp-content/themes/style.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /wp-content/themes/style.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/wp-content/themes/style.php"
2026/01/15 04:33:08 [error] 1568902#1568902: *86189 open() "/opt/logos/www/wp-admin/style.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /wp-admin/style.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/wp-admin/style.php"
2026/01/15 04:33:08 [error] 1568902#1568902: *86189 open() "/opt/logos/www/wp-includes/style.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /wp-includes/style.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/wp-includes/style.php"
2026/01/15 04:33:08 [error] 1568902#1568902: *86189 open() "/opt/logos/www/chosen.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /chosen.php?p= HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/chosen.php?p="
2026/01/15 04:33:09 [error] 1568902#1568902: *86189 open() "/opt/logos/www/file.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /file.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/file.php"
2026/01/15 04:33:09 [error] 1568902#1568902: *86189 open() "/opt/logos/www/flower.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /flower.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/flower.php"
2026/01/15 04:33:09 [error] 1568902#1568902: *86189 open() "/opt/logos/www/gifclass.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /gifclass.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/gifclass.php#888xyz999"
2026/01/15 04:33:10 [error] 1568902#1568902: *86189 open() "/opt/logos/www/bless.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /bless.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/bless.php#888xyz999"
2026/01/15 04:33:10 [error] 1568902#1568902: *86189 open() "/opt/logos/www/class-t.api.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /class-t.api.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/class-t.api.php#888xyz999"
2026/01/15 04:33:10 [error] 1568902#1568902: *86189 open() "/opt/logos/www/blurbs.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /blurbs.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/blurbs.php#888xyz999"
2026/01/15 04:33:11 [error] 1568902#1568902: *86189 open() "/opt/logos/www/akcc.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /akcc.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/akcc.php"
2026/01/15 04:33:11 [error] 1568902#1568902: *86189 open() "/opt/logos/www/abcd.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /abcd.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/abcd.php"
2026/01/15 04:33:11 [error] 1568902#1568902: *86189 open() "/opt/logos/www/shelp.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /shelp.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/shelp.php"
2026/01/15 04:33:12 [error] 1568902#1568902: *86189 open() "/opt/logos/www/cord.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /cord.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/cord.php"
2026/01/15 04:33:12 [error] 1568902#1568902: *86189 open() "/opt/logos/www/dex.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /dex.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/dex.php"
2026/01/15 04:33:12 [error] 1568902#1568902: *86189 open() "/opt/logos/www/wp-admin/admin-ajax.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /wp-admin/admin-ajax.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/wp-admin/admin-ajax.php"
2026/01/15 04:33:12 [error] 1568902#1568902: *86189 open() "/opt/logos/www/file2.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /file2.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/file2.php#tabFM"
2026/01/15 04:33:13 [error] 1568902#1568902: *86189 open() "/opt/logos/www/zwso.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET //zwso.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com//zwso.php"
2026/01/15 04:33:13 [error] 1568902#1568902: *86189 open() "/opt/logos/www/wp-admin/zwso.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /wp-admin/zwso.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/wp-admin/zwso.php"
2026/01/15 04:33:13 [error] 1568902#1568902: *86189 open() "/opt/logos/www/wp-content/plugins/hellopress/wp_mna.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /wp-content/plugins/hellopress/wp_mna.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/wp-content/plugins/hellopress/wp_mna.php"
2026/01/15 04:33:14 [error] 1568902#1568902: *86189 open() "/opt/logos/www/bolt.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /bolt.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/bolt.php"
2026/01/15 04:33:14 [error] 1568902#1568902: *86189 open() "/opt/logos/www/shlo.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /shlo.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/shlo.php#lufix"
2026/01/15 04:33:14 [error] 1568902#1568902: *86189 open() "/opt/logos/www/133.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /133.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/133.php"
2026/01/15 04:33:14 [error] 1568902#1568902: *86189 open() "/opt/logos/www/ahax.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /ahax.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/ahax.php"
2026/01/15 04:33:15 [error] 1568902#1568902: *86189 open() "/opt/logos/www/php8.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /php8.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/php8.php#xleet"
2026/01/15 04:33:15 [error] 1568902#1568902: *86189 open() "/opt/logos/www/lufix1.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /lufix1.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/lufix1.php#lufix"
2026/01/15 04:33:15 [error] 1568902#1568902: *86189 open() "/opt/logos/www/witmm.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /witmm.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/witmm.php#lufix"
2026/01/15 04:33:16 [error] 1568902#1568902: *86189 open() "/opt/logos/www/wp-admin/css/index.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /wp-admin/css/index.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/wp-admin/css/index.php"
2026/01/15 04:33:16 [error] 1568902#1568902: *86189 open() "/opt/logos/www/wp-content/plugins/index.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /wp-content/plugins/index.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/wp-content/plugins/index.php"
2026/01/15 04:33:16 [error] 1568902#1568902: *86189 open() "/opt/logos/www/wp-content/index.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /wp-content/index.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/wp-content/index.php"
2026/01/15 04:33:17 [error] 1568902#1568902: *86189 open() "/opt/logos/www/ioxi-o.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /ioxi-o.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/ioxi-o.php"
2026/01/15 04:33:17 [error] 1568902#1568902: *86189 open() "/opt/logos/www/222.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /222.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/222.php"
2026/01/15 04:33:17 [error] 1568902#1568902: *86189 open() "/opt/logos/www/files.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /files.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/files.php#admin@3tu/T?TJ8v?N"
2026/01/15 04:33:17 [error] 1568902#1568902: *86189 open() "/opt/logos/www/wp-editor.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /wp-editor.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/wp-editor.php#lufix"
2026/01/15 04:33:18 [error] 1568902#1568902: *86189 open() "/opt/logos/www/txets.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /txets.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/txets.php"
2026/01/15 04:33:18 [error] 1568902#1568902: *86189 open() "/opt/logos/www/wp-content/txets.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /wp-content/txets.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/wp-content/txets.php"
2026/01/15 04:33:18 [error] 1568902#1568902: *86189 open() "/opt/logos/www/wp-admin/txets.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /wp-admin/txets.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/wp-admin/txets.php"
2026/01/15 04:33:19 [error] 1568902#1568902: *86189 open() "/opt/logos/www/postnews.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /postnews.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/postnews.php"
2026/01/15 04:33:19 [error] 1568902#1568902: *86189 open() "/opt/logos/www/wp-content/postnews.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /wp-content/postnews.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/wp-content/postnews.php"
2026/01/15 04:33:19 [error] 1568902#1568902: *86189 open() "/opt/logos/www/wp-admin/postnews.php" failed (2: No such file or directory), client: 104.28.246.115, server: mw-expedition.com, request: "GET /wp-admin/postnews.php HTTP/2.0", host: "mw-expedition.com", referrer: "http://mw-expedition.com/wp-admin/postnews.php"
2026/01/15 04:38:52 [error] 1568902#1568902: *86192 open() "/opt/logos/www/SDK/webLanguage" failed (2: No such file or directory), client: 93.123.72.132, server: mw-expedition.com, request: "GET /SDK/webLanguage HTTP/1.1", host: "45.159.248.232:443"
2026/01/15 04:46:10 [error] 1568902#1568902: *86193 open() "/opt/logos/www/SDK/webLanguage" failed (2: No such file or directory), client: 89.42.231.200, server: mw-expedition.com, request: "GET /SDK/webLanguage HTTP/1.1", host: "45.159.248.232:443"
2026/01/15 04:46:41 [error] 1568902#1568902: *86195 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.217.56, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 04:47:03 [error] 1568902#1568902: *86196 open() "/opt/logos/www/robots.txt" failed (2: No such file or directory), client: 216.73.216.102, server: mw-expedition.com, request: "GET /robots.txt HTTP/2.0", host: "mw-expedition.com"
2026/01/15 04:48:32 [error] 1568902#1568902: *86197 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.183, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 04:49:27 [error] 1568902#1568902: *86197 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.183, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 04:50:13 [error] 1568902#1568902: *86199 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.98, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 04:57:08 [error] 1568902#1568902: *86200 open() "/opt/logos/www/index.php" failed (2: No such file or directory), client: 162.158.178.212, server: mw-expedition.com, request: "POST /index.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 04:57:08 [error] 1568902#1568902: *86200 open() "/opt/logos/www/admin" failed (2: No such file or directory), client: 162.158.178.212, server: mw-expedition.com, request: "POST /admin HTTP/2.0", host: "logosblockchain.com"
2026/01/15 05:06:18 [error] 1568902#1568902: *86202 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.70.243.183, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 05:06:33 [error] 1568902#1568902: *86204 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.68.10.193, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 05:09:52 [error] 1568902#1568902: *86206 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.71.184.86, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 05:10:02 [error] 1568902#1568902: *86206 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.71.184.86, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 05:12:59 [error] 1568902#1568902: *86210 open() "/opt/logos/www/index.php" failed (2: No such file or directory), client: 172.71.214.17, server: mw-expedition.com, request: "POST /index.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 05:12:59 [error] 1568902#1568902: *86210 open() "/opt/logos/www/admin" failed (2: No such file or directory), client: 172.71.214.17, server: mw-expedition.com, request: "POST /admin HTTP/2.0", host: "logosblockchain.com"
2026/01/15 05:14:13 [error] 1568902#1568902: *86212 open() "/opt/logos/www/wp-login.php" failed (2: No such file or directory), client: 172.71.152.67, server: mw-expedition.com, request: "GET /wp-login.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 05:25:47 [error] 1568902#1568902: *86214 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.68.10.192, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 05:27:15 [error] 1568902#1568902: *86216 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.71.184.86, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 05:28:40 [error] 1568902#1568902: *86218 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.68.10.193, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 05:28:50 [error] 1568902#1568902: *86220 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.69.50.219, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 05:31:51 [error] 1568902#1568902: *86221 open() "/opt/logos/www/index.php" failed (2: No such file or directory), client: 172.64.217.64, server: mw-expedition.com, request: "POST /index.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 05:31:51 [error] 1568902#1568902: *86221 open() "/opt/logos/www/admin" failed (2: No such file or directory), client: 172.64.217.64, server: mw-expedition.com, request: "POST /admin HTTP/2.0", host: "logosblockchain.com"
2026/01/15 05:45:53 [error] 1568902#1568902: *86228 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 162.158.183.80, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 05:46:45 [error] 1568902#1568902: *86229 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.99, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 05:46:46 [error] 1568902#1568902: *86231 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.217.101, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 05:46:55 [error] 1568902#1568902: *86232 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.217.57, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 05:59:48 [error] 1568902#1568902: *86235 open() "/opt/logos/www/index.php" failed (2: No such file or directory), client: 162.159.98.123, server: mw-expedition.com, request: "POST /index.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 05:59:49 [error] 1568902#1568902: *86235 open() "/opt/logos/www/admin" failed (2: No such file or directory), client: 162.159.98.123, server: mw-expedition.com, request: "POST /admin HTTP/2.0", host: "logosblockchain.com"
2026/01/15 06:01:16 [error] 1568902#1568902: *86237 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.69.151.230, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 06:02:27 [error] 1568902#1568902: *86239 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.68.10.192, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 06:02:27 [error] 1568902#1568902: *86240 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.71.184.87, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 06:02:42 [error] 1568902#1568902: *86242 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.69.50.219, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 06:19:51 [error] 1568902#1568902: *86245 open() "/opt/logos/www/robots.txt" failed (2: No such file or directory), client: 216.73.216.102, server: mw-expedition.com, request: "GET /robots.txt HTTP/2.0", host: "mw-expedition.com"
2026/01/15 06:19:51 [error] 1568902#1568902: *86245 open() "/opt/logos/www/airdrop.html" failed (2: No such file or directory), client: 216.73.216.102, server: mw-expedition.com, request: "GET /airdrop.html HTTP/2.0", host: "mw-expedition.com"
2026/01/15 06:19:56 [error] 1568902#1568902: *86246 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.99, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 06:19:56 [error] 1568902#1568902: *86248 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.71.148.106, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 06:20:45 [error] 1568902#1568902: *86249 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.71.144.154, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 06:22:29 [error] 1568902#1568902: *86253 open() "/opt/logos/www/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 169.150.203.195, server: mw-expedition.com, request: "GET //wp-includes/wlwmanifest.xml HTTP/1.1", host: "mw-expedition.com"
2026/01/15 06:22:29 [error] 1568902#1568902: *86253 open() "/opt/logos/www/xmlrpc.php" failed (2: No such file or directory), client: 169.150.203.195, server: mw-expedition.com, request: "GET //xmlrpc.php?rsd HTTP/1.1", host: "mw-expedition.com"
2026/01/15 06:22:29 [error] 1568902#1568902: *86253 open() "/opt/logos/www/blog/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 169.150.203.195, server: mw-expedition.com, request: "GET //blog/wp-includes/wlwmanifest.xml HTTP/1.1", host: "mw-expedition.com"
2026/01/15 06:22:29 [error] 1568902#1568902: *86253 open() "/opt/logos/www/web/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 169.150.203.195, server: mw-expedition.com, request: "GET //web/wp-includes/wlwmanifest.xml HTTP/1.1", host: "mw-expedition.com"
2026/01/15 06:22:30 [error] 1568902#1568902: *86253 open() "/opt/logos/www/wordpress/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 169.150.203.195, server: mw-expedition.com, request: "GET //wordpress/wp-includes/wlwmanifest.xml HTTP/1.1", host: "mw-expedition.com"
2026/01/15 06:22:30 [error] 1568902#1568902: *86253 open() "/opt/logos/www/website/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 169.150.203.195, server: mw-expedition.com, request: "GET //website/wp-includes/wlwmanifest.xml HTTP/1.1", host: "mw-expedition.com"
2026/01/15 06:22:30 [error] 1568902#1568902: *86253 open() "/opt/logos/www/wp/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 169.150.203.195, server: mw-expedition.com, request: "GET //wp/wp-includes/wlwmanifest.xml HTTP/1.1", host: "mw-expedition.com"
2026/01/15 06:22:30 [error] 1568902#1568902: *86253 open() "/opt/logos/www/news/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 169.150.203.195, server: mw-expedition.com, request: "GET //news/wp-includes/wlwmanifest.xml HTTP/1.1", host: "mw-expedition.com"
2026/01/15 06:22:30 [error] 1568902#1568902: *86253 open() "/opt/logos/www/2018/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 169.150.203.195, server: mw-expedition.com, request: "GET //2018/wp-includes/wlwmanifest.xml HTTP/1.1", host: "mw-expedition.com"
2026/01/15 06:22:30 [error] 1568902#1568902: *86253 open() "/opt/logos/www/2019/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 169.150.203.195, server: mw-expedition.com, request: "GET //2019/wp-includes/wlwmanifest.xml HTTP/1.1", host: "mw-expedition.com"
2026/01/15 06:22:30 [error] 1568902#1568902: *86253 open() "/opt/logos/www/shop/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 169.150.203.195, server: mw-expedition.com, request: "GET //shop/wp-includes/wlwmanifest.xml HTTP/1.1", host: "mw-expedition.com"
2026/01/15 06:22:30 [error] 1568902#1568902: *86253 open() "/opt/logos/www/wp1/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 169.150.203.195, server: mw-expedition.com, request: "GET //wp1/wp-includes/wlwmanifest.xml HTTP/1.1", host: "mw-expedition.com"
2026/01/15 06:22:31 [error] 1568902#1568902: *86253 open() "/opt/logos/www/test/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 169.150.203.195, server: mw-expedition.com, request: "GET //test/wp-includes/wlwmanifest.xml HTTP/1.1", host: "mw-expedition.com"
2026/01/15 06:22:31 [error] 1568902#1568902: *86253 open() "/opt/logos/www/media/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 169.150.203.195, server: mw-expedition.com, request: "GET //media/wp-includes/wlwmanifest.xml HTTP/1.1", host: "mw-expedition.com"
2026/01/15 06:22:31 [error] 1568902#1568902: *86253 open() "/opt/logos/www/wp2/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 169.150.203.195, server: mw-expedition.com, request: "GET //wp2/wp-includes/wlwmanifest.xml HTTP/1.1", host: "mw-expedition.com"
2026/01/15 06:22:31 [error] 1568902#1568902: *86253 open() "/opt/logos/www/site/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 169.150.203.195, server: mw-expedition.com, request: "GET //site/wp-includes/wlwmanifest.xml HTTP/1.1", host: "mw-expedition.com"
2026/01/15 06:22:31 [error] 1568902#1568902: *86253 open() "/opt/logos/www/cms/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 169.150.203.195, server: mw-expedition.com, request: "GET //cms/wp-includes/wlwmanifest.xml HTTP/1.1", host: "mw-expedition.com"
2026/01/15 06:22:31 [error] 1568902#1568902: *86253 open() "/opt/logos/www/sito/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 169.150.203.195, server: mw-expedition.com, request: "GET //sito/wp-includes/wlwmanifest.xml HTTP/1.1", host: "mw-expedition.com"
2026/01/15 06:23:04 [error] 1568902#1568902: *86255 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.183, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 06:23:34 [error] 1568902#1568902: *86256 open() "/opt/logos/www/staking" failed (2: No such file or directory), client: 216.73.216.102, server: mw-expedition.com, request: "GET /staking HTTP/2.0", host: "mw-expedition.com"
2026/01/15 06:26:01 [error] 1568902#1568902: *86258 open() "/opt/logos/www/robots.txt" failed (2: No such file or directory), client: 46.105.40.140, server: mw-expedition.com, request: "GET /robots.txt HTTP/1.1", host: "mw-expedition.com"
2026/01/15 06:38:59 [error] 1568902#1568902: *86263 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.69.50.241, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 06:40:33 [error] 1568902#1568902: *86265 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.98, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 06:40:33 [error] 1568902#1568902: *86266 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.71.184.86, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 06:40:46 [error] 1568902#1568902: *86267 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.70.240.151, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 06:41:11 [error] 1568902#1568902: *86269 open() "/opt/logos/www/index.php" failed (2: No such file or directory), client: 172.71.131.74, server: mw-expedition.com, request: "POST /index.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 06:41:12 [error] 1568902#1568902: *86269 open() "/opt/logos/www/admin" failed (2: No such file or directory), client: 172.71.131.74, server: mw-expedition.com, request: "POST /admin HTTP/2.0", host: "logosblockchain.com"
2026/01/15 06:44:45 [error] 1568902#1568902: *86272 open() "/opt/logos/www/robots.txt" failed (2: No such file or directory), client: 44.248.182.30, server: mw-expedition.com, request: "GET /robots.txt HTTP/2.0", host: "www.mw-expedition.com"
2026/01/15 06:54:03 [error] 1568902#1568902: *86281 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 162.158.183.80, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 06:54:18 [error] 1568902#1568902: *86282 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.182, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 06:57:18 [error] 1568902#1568902: *86283 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.182, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 06:57:41 [error] 1568902#1568902: *86285 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.98, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 07:11:49 [error] 1568902#1568902: *86289 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.182, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 07:12:51 [error] 1568902#1568902: *86290 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.98, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 07:13:24 [error] 1568902#1568902: *86292 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.37, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 07:15:23 [error] 1568902#1568902: *86294 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.183, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 07:17:42 [error] 1568902#1568902: *86296 open() "/opt/logos/www/index.php" failed (2: No such file or directory), client: 162.159.98.122, server: mw-expedition.com, request: "POST /index.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 07:17:42 [error] 1568902#1568902: *86296 open() "/opt/logos/www/admin" failed (2: No such file or directory), client: 162.159.98.122, server: mw-expedition.com, request: "POST /admin HTTP/2.0", host: "logosblockchain.com"
2026/01/15 07:27:32 [error] 1568902#1568902: *86299 open() "/opt/logos/www/robots.txt" failed (2: No such file or directory), client: 192.71.3.222, server: mw-expedition.com, request: "GET /robots.txt HTTP/1.1", host: "mw-expedition.com", referrer: "http://mw-expedition.com/robots.txt"
2026/01/15 07:30:27 [error] 1568902#1568902: *86305 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.71.184.87, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 07:30:57 [error] 1568902#1568902: *86307 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.68.10.43, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 07:31:16 [error] 1568902#1568902: *86308 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.182, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 07:32:55 [error] 1568902#1568902: *86310 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.69.151.230, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 07:43:22 [error] 1568902#1568902: *86314 open() "/opt/logos/www/index.php" failed (2: No such file or directory), client: 172.68.164.8, server: mw-expedition.com, request: "POST /index.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 07:43:22 [error] 1568902#1568902: *86314 open() "/opt/logos/www/admin" failed (2: No such file or directory), client: 172.68.164.8, server: mw-expedition.com, request: "POST /admin HTTP/2.0", host: "logosblockchain.com"
2026/01/15 07:43:36 [error] 1568902#1568902: *86317 open() "/opt/logos/www/onvif/device_service" failed (2: No such file or directory), client: 185.62.203.253, server: mw-expedition.com, request: "POST /onvif/device_service HTTP/1.1", host: "45.159.248.232"
2026/01/15 07:44:33 [error] 1568902#1568902: *86318 open() "/opt/logos/www/robots.txt" failed (2: No such file or directory), client: 216.73.216.102, server: mw-expedition.com, request: "GET /robots.txt HTTP/2.0", host: "mw-expedition.com"
2026/01/15 07:47:41 [error] 1568902#1568902: *86322 open() "/opt/logos/www/server-status" failed (2: No such file or directory), client: 193.32.127.137, server: mw-expedition.com, request: "GET /server-status HTTP/1.1", host: "vm15330919.example.com"
2026/01/15 07:47:46 [error] 1568902#1568902: *86325 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.98, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 07:49:09 [error] 1568902#1568902: *86328 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.217.57, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 07:50:47 [error] 1568902#1568902: *86332 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.99, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 07:51:17 [error] 1568902#1568902: *86333 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.182, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 07:58:08 [error] 1568902#1568902: *86334 open() "/opt/logos/www/robots.txt" failed (2: No such file or directory), client: 172.71.123.212, server: mw-expedition.com, request: "GET /robots.txt HTTP/2.0", host: "logosblockchain.com"
2026/01/15 07:58:27 [error] 1568902#1568902: *86337 open() "/opt/logos/www/index.php" failed (2: No such file or directory), client: 162.158.178.248, server: mw-expedition.com, request: "POST /index.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 07:58:27 [error] 1568902#1568902: *86337 open() "/opt/logos/www/admin" failed (2: No such file or directory), client: 162.158.178.248, server: mw-expedition.com, request: "POST /admin HTTP/2.0", host: "logosblockchain.com"
2026/01/15 08:04:55 [error] 1568902#1568902: *86340 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.98, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 08:07:12 [error] 1568902#1568902: *86344 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.69.151.230, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 08:08:04 [error] 1568902#1568902: *86346 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.71.172.64, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 08:08:47 [error] 1568902#1568902: *86350 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.183, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 08:19:01 [error] 1568902#1568902: *86366 open() "/opt/logos/www/index.php" failed (2: No such file or directory), client: 108.162.227.149, server: mw-expedition.com, request: "POST /index.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 08:19:02 [error] 1568902#1568902: *86366 open() "/opt/logos/www/admin" failed (2: No such file or directory), client: 108.162.227.149, server: mw-expedition.com, request: "POST /admin HTTP/2.0", host: "logosblockchain.com"
2026/01/15 08:21:44 [error] 1568902#1568902: *86369 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.182, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 08:23:55 [error] 1568902#1568902: *86371 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.99, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 08:24:24 [error] 1568902#1568902: *86373 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 162.158.110.44, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 08:24:56 [error] 1568902#1568902: *86374 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.71.144.155, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 08:25:44 [error] 1568902#1568902: *86375 open() "/opt/logos/www/.git/config" failed (2: No such file or directory), client: 216.81.248.30, server: mw-expedition.com, request: "GET /.git/config HTTP/1.1", host: "mw-expedition.com"
2026/01/15 08:31:38 [error] 1568902#1568902: *86380 open() "/opt/logos/www/index.php" failed (2: No such file or directory), client: 104.23.170.106, server: mw-expedition.com, request: "POST /index.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 08:31:39 [error] 1568902#1568902: *86380 open() "/opt/logos/www/admin" failed (2: No such file or directory), client: 104.23.170.106, server: mw-expedition.com, request: "POST /admin HTTP/2.0", host: "logosblockchain.com"
2026/01/15 08:31:51 [error] 1568902#1568902: *86382 open() "/opt/logos/www/index.php" failed (2: No such file or directory), client: 162.158.178.212, server: mw-expedition.com, request: "POST /index.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 08:31:51 [error] 1568902#1568902: *86382 open() "/opt/logos/www/admin" failed (2: No such file or directory), client: 162.158.178.212, server: mw-expedition.com, request: "POST /admin HTTP/2.0", host: "logosblockchain.com"
2026/01/15 08:37:39 [error] 1568902#1568902: *86393 open() "/opt/logos/www/index.php" failed (2: No such file or directory), client: 104.23.175.141, server: mw-expedition.com, request: "POST /index.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 08:37:39 [error] 1568902#1568902: *86393 open() "/opt/logos/www/admin" failed (2: No such file or directory), client: 104.23.175.141, server: mw-expedition.com, request: "POST /admin HTTP/2.0", host: "logosblockchain.com"
2026/01/15 08:38:19 [error] 1568902#1568902: *86395 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.182, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 08:39:42 [error] 1568902#1568902: *86411 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.217.57, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 08:41:05 [error] 1568902#1568902: *86413 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.217.57, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 08:41:10 [error] 1568902#1568902: *86414 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.99, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 08:42:35 [error] 1568902#1568902: *86415 open() "/opt/logos/www/xmlrpc.php" failed (2: No such file or directory), client: 191.6.255.74, server: mw-expedition.com, request: "POST /xmlrpc.php HTTP/1.1", host: "mw-expedition.com"
2026/01/15 08:43:21 [error] 1568902#1568902: *86416 open() "/opt/logos/www/robots.txt" failed (2: No such file or directory), client: 46.105.40.140, server: mw-expedition.com, request: "GET /robots.txt HTTP/1.1", host: "mw-expedition.com"
2026/01/15 08:44:51 [error] 1568902#1568902: *86424 open() "/opt/logos/www/FSnU" failed (2: No such file or directory), client: 50.19.12.17, server: mw-expedition.com, request: "GET /FSnU HTTP/1.1", host: "45.159.248.232"
2026/01/15 08:44:52 [error] 1568902#1568902: *86426 open() "/opt/logos/www/OEpY" failed (2: No such file or directory), client: 50.19.12.17, server: mw-expedition.com, request: "GET /OEpY HTTP/1.1", host: "45.159.248.232"
2026/01/15 08:44:53 [error] 1568902#1568902: *86431 open() "/opt/logos/www/DYQn" failed (2: No such file or directory), client: 50.19.12.17, server: mw-expedition.com, request: "GET /DYQn HTTP/1.1", host: "45.159.248.232"
2026/01/15 08:44:54 [error] 1568902#1568902: *86432 open() "/opt/logos/www/SKGx" failed (2: No such file or directory), client: 50.19.12.17, server: mw-expedition.com, request: "GET /SKGx HTTP/1.1", host: "45.159.248.232"
2026/01/15 08:55:28 [error] 1568902#1568902: *86435 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.183, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 08:56:39 [error] 1568902#1568902: *86437 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 162.158.183.97, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 08:56:48 [error] 1568902#1568902: *86437 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 162.158.183.97, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 08:57:59 [error] 1568902#1568902: *86438 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 162.158.183.98, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 09:03:26 [error] 1568902#1568902: *86441 open() "/opt/logos/www/index.php" failed (2: No such file or directory), client: 162.158.178.248, server: mw-expedition.com, request: "POST /index.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 09:03:27 [error] 1568902#1568902: *86441 open() "/opt/logos/www/admin" failed (2: No such file or directory), client: 162.158.178.248, server: mw-expedition.com, request: "POST /admin HTTP/2.0", host: "logosblockchain.com"
2026/01/15 09:15:24 [error] 1568902#1568902: *86447 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.182, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 09:16:32 [error] 1568902#1568902: *86448 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.182, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 09:16:36 [error] 1568902#1568902: *86449 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 162.158.110.45, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 09:17:19 [error] 1568902#1568902: *86448 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.182, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 09:19:43 [error] 1568902#1568902: *86452 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.223, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "mw-expedition.com"
2026/01/15 09:19:52 [error] 1568902#1568902: *86453 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.222, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "mw-expedition.com"
2026/01/15 09:20:50 [error] 1568902#1568902: *86454 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.222, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "mw-expedition.com"
2026/01/15 09:21:14 [error] 1568902#1568902: *86456 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.19, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "mw-expedition.com"
2026/01/15 09:25:31 [error] 1568902#1568902: *86457 open() "/opt/logos/www/robots.txt" failed (2: No such file or directory), client: 142.44.233.122, server: mw-expedition.com, request: "GET /robots.txt HTTP/2.0", host: "mw-expedition.com"
2026/01/15 09:31:12 [error] 1568902#1568902: *86460 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.183, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 09:31:27 [error] 1568902#1568902: *86460 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.183, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 09:32:11 [error] 1568902#1568902: *86460 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.183, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 09:35:07 [error] 1568902#1568902: *86463 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.71.164.30, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 09:35:43 [error] 1568902#1568902: *86464 open() "/opt/logos/www/index.php" failed (2: No such file or directory), client: 162.159.98.201, server: mw-expedition.com, request: "POST /index.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 09:35:43 [error] 1568902#1568902: *86464 open() "/opt/logos/www/admin" failed (2: No such file or directory), client: 162.159.98.201, server: mw-expedition.com, request: "POST /admin HTTP/2.0", host: "logosblockchain.com"
2026/01/15 09:41:26 [error] 1568902#1568902: *86468 open() "/opt/logos/www/SDK/webLanguage" failed (2: No such file or directory), client: 5.183.209.196, server: mw-expedition.com, request: "GET /SDK/webLanguage HTTP/1.1", host: "45.159.248.232:443"
2026/01/15 09:45:32 [error] 1568902#1568902: *86470 open() "/opt/logos/www/index.php" failed (2: No such file or directory), client: 172.71.218.240, server: mw-expedition.com, request: "POST /index.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 09:45:32 [error] 1568902#1568902: *86470 open() "/opt/logos/www/admin" failed (2: No such file or directory), client: 172.71.218.240, server: mw-expedition.com, request: "POST /admin HTTP/2.0", host: "logosblockchain.com"
2026/01/15 09:49:42 [error] 1568902#1568902: *86473 open() "/opt/logos/www/cdn-cgi/trace" failed (2: No such file or directory), client: 150.241.68.160, server: mw-expedition.com, request: "GET /cdn-cgi/trace HTTP/2.0", host: "cloudflare.com"
2026/01/15 09:50:29 [error] 1568902#1568902: *86475 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.98, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 09:50:44 [error] 1568902#1568902: *86477 open() "/opt/logos/www/graphql" failed (2: No such file or directory), client: 146.148.114.32, server: mw-expedition.com, request: "POST /graphql HTTP/1.1", host: "45.159.248.232"
2026/01/15 09:50:58 [error] 1568902#1568902: *86479 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.183, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 09:50:58 [error] 1568902#1568902: *86479 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.183, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 09:52:35 [error] 1568902#1568902: *86481 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.182, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 09:52:57 [error] 1568902#1568902: *86482 open() "/opt/logos/www/index.php" failed (2: No such file or directory), client: 104.23.175.154, server: mw-expedition.com, request: "POST /index.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 09:52:57 [error] 1568902#1568902: *86482 open() "/opt/logos/www/admin" failed (2: No such file or directory), client: 104.23.175.154, server: mw-expedition.com, request: "POST /admin HTTP/2.0", host: "logosblockchain.com"
2026/01/15 09:59:43 [error] 1568902#1568902: *86485 open() "/opt/logos/www/robots.txt" failed (2: No such file or directory), client: 104.210.140.142, server: mw-expedition.com, request: "GET /robots.txt HTTP/2.0", host: "mw-expedition.com"
2026/01/15 09:59:43 [error] 1568902#1568902: *86485 open() "/opt/logos/www/robots.txt" failed (2: No such file or directory), client: 104.210.140.142, server: mw-expedition.com, request: "GET /robots.txt HTTP/2.0", host: "mw-expedition.com"
2026/01/15 10:09:31 [error] 1568902#1568902: *86487 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.182, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 10:10:10 [error] 1568902#1568902: *86487 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.182, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 10:10:10 [error] 1568902#1568902: *86489 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.98, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 10:10:38 [error] 1568902#1568902: *86489 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.98, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 10:14:55 [error] 1568902#1568902: *86492 open() "/opt/logos/www/index.php" failed (2: No such file or directory), client: 172.69.40.143, server: mw-expedition.com, request: "POST /index.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 10:14:55 [error] 1568902#1568902: *86492 open() "/opt/logos/www/admin" failed (2: No such file or directory), client: 172.69.40.143, server: mw-expedition.com, request: "POST /admin HTTP/2.0", host: "logosblockchain.com"
2026/01/15 10:27:21 [error] 1568902#1568902: *86496 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.71.144.155, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 10:27:40 [error] 1568902#1568902: *86497 open() "/opt/logos/www/index.php" failed (2: No such file or directory), client: 172.69.114.106, server: mw-expedition.com, request: "POST /index.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 10:27:40 [error] 1568902#1568902: *86497 open() "/opt/logos/www/admin" failed (2: No such file or directory), client: 172.69.114.106, server: mw-expedition.com, request: "POST /admin HTTP/2.0", host: "logosblockchain.com"
2026/01/15 10:27:41 [error] 1568902#1568902: *86500 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.182, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 10:28:37 [error] 1568902#1568902: *86502 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.99, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 10:28:51 [error] 1568902#1568902: *86503 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.182, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 10:31:33 [error] 1568902#1568902: *86505 open() "/opt/logos/www/index.php" failed (2: No such file or directory), client: 108.162.245.180, server: mw-expedition.com, request: "POST /index.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 10:31:33 [error] 1568902#1568902: *86505 open() "/opt/logos/www/admin" failed (2: No such file or directory), client: 108.162.245.180, server: mw-expedition.com, request: "POST /admin HTTP/2.0", host: "logosblockchain.com"
2026/01/15 10:44:32 [error] 1568902#1568902: *86508 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.98, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 10:46:06 [error] 1568902#1568902: *86510 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.99, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 10:46:27 [error] 1568902#1568902: *86510 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.99, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 10:47:47 [error] 1568902#1568902: *86513 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.99, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:02:36 [error] 1568902#1568902: *86519 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.182, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:03:54 [error] 1568902#1568902: *86534 open() "/opt/logos/www/staking" failed (2: No such file or directory), client: 192.36.217.48, server: mw-expedition.com, request: "GET /staking HTTP/1.1", host: "mw-expedition.com"
2026/01/15 11:04:03 [error] 1568902#1568902: *86538 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.183, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:05:13 [error] 1568902#1568902: *86540 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.99, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:05:37 [error] 1568902#1568902: *86542 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.71.246.152, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:07:43 [error] 1568902#1568902: *86543 open() "/opt/logos/www/index.php" failed (2: No such file or directory), client: 172.68.211.180, server: mw-expedition.com, request: "POST /index.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:07:44 [error] 1568902#1568902: *86544 open() "/opt/logos/www/admin" failed (2: No such file or directory), client: 172.68.211.140, server: mw-expedition.com, request: "POST /admin HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:21:40 [error] 1568902#1568902: *86551 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.183, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:22:08 [error] 1568902#1568902: *86552 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.71.144.155, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:22:22 [error] 1568902#1568902: *86551 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.183, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:23:10 [error] 1568902#1568902: *86551 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.183, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:32:59 [error] 1568902#1568902: *86554 open() "/opt/logos/www/autodiscover/autodiscover.json" failed (2: No such file or directory), client: 135.237.126.103, server: mw-expedition.com, request: "GET /autodiscover/autodiscover.json?@zdi/Powershell HTTP/1.1", host: "45.159.248.232"
2026/01/15 11:36:56 [error] 1568902#1568902: *86556 open() "/opt/logos/www/wp-includes/ID3/license.txt" failed (2: No such file or directory), client: 104.22.24.202, server: mw-expedition.com, request: "GET //wp-includes/ID3/license.txt HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:36:56 [error] 1568902#1568902: *86556 "/opt/logos/www/feed/index.html" is not found (2: No such file or directory), client: 104.22.24.202, server: mw-expedition.com, request: "GET //feed/ HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:36:56 [error] 1568902#1568902: *86556 open() "/opt/logos/www/xmlrpc.php" failed (2: No such file or directory), client: 104.22.24.202, server: mw-expedition.com, request: "GET //xmlrpc.php?rsd HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:36:56 [error] 1568902#1568902: *86556 open() "/opt/logos/www/blog/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 104.22.24.202, server: mw-expedition.com, request: "GET //blog/wp-includes/wlwmanifest.xml HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:36:57 [error] 1568902#1568902: *86556 open() "/opt/logos/www/web/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 104.22.24.202, server: mw-expedition.com, request: "GET //web/wp-includes/wlwmanifest.xml HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:36:57 [error] 1568902#1568902: *86556 open() "/opt/logos/www/wordpress/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 104.22.24.202, server: mw-expedition.com, request: "GET //wordpress/wp-includes/wlwmanifest.xml HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:36:57 [error] 1568902#1568902: *86556 open() "/opt/logos/www/wp/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 104.22.24.202, server: mw-expedition.com, request: "GET //wp/wp-includes/wlwmanifest.xml HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:36:57 [error] 1568902#1568902: *86556 open() "/opt/logos/www/2020/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 104.22.24.202, server: mw-expedition.com, request: "GET //2020/wp-includes/wlwmanifest.xml HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:36:57 [error] 1568902#1568902: *86556 open() "/opt/logos/www/2019/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 104.22.24.202, server: mw-expedition.com, request: "GET //2019/wp-includes/wlwmanifest.xml HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:36:57 [error] 1568902#1568902: *86556 open() "/opt/logos/www/2021/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 104.22.24.202, server: mw-expedition.com, request: "GET //2021/wp-includes/wlwmanifest.xml HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:36:57 [error] 1568902#1568902: *86556 open() "/opt/logos/www/shop/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 104.22.24.202, server: mw-expedition.com, request: "GET //shop/wp-includes/wlwmanifest.xml HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:36:57 [error] 1568902#1568902: *86556 open() "/opt/logos/www/wp1/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 104.22.24.202, server: mw-expedition.com, request: "GET //wp1/wp-includes/wlwmanifest.xml HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:36:57 [error] 1568902#1568902: *86556 open() "/opt/logos/www/test/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 104.22.24.202, server: mw-expedition.com, request: "GET //test/wp-includes/wlwmanifest.xml HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:36:58 [error] 1568902#1568902: *86556 open() "/opt/logos/www/site/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 104.22.24.202, server: mw-expedition.com, request: "GET //site/wp-includes/wlwmanifest.xml HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:36:58 [error] 1568902#1568902: *86556 open() "/opt/logos/www/cms/wp-includes/wlwmanifest.xml" failed (2: No such file or directory), client: 104.22.24.202, server: mw-expedition.com, request: "GET //cms/wp-includes/wlwmanifest.xml HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:42:22 [error] 1568902#1568902: *86570 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.182, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:42:46 [error] 1568902#1568902: *86571 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 172.71.164.20, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:43:10 [error] 1568902#1568902: *86570 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.182, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:43:23 [error] 1568902#1568902: *86570 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.182, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:57:10 [error] 1568902#1568902: *86574 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.182, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 11:59:35 [error] 1568902#1568902: *86575 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.182, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 12:00:09 [error] 1568902#1568902: *86577 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.217.101, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 12:00:32 [error] 1568902#1568902: *86578 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.217.56, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 12:09:24 [error] 1568902#1568902: *86581 open() "/opt/logos/www/index.php" failed (2: No such file or directory), client: 162.159.113.102, server: mw-expedition.com, request: "POST /index.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 12:09:24 [error] 1568902#1568902: *86581 open() "/opt/logos/www/admin" failed (2: No such file or directory), client: 162.159.113.102, server: mw-expedition.com, request: "POST /admin HTTP/2.0", host: "logosblockchain.com"
2026/01/15 12:16:25 [error] 1568902#1568902: *86584 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.14, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 12:16:40 [error] 1568902#1568902: *86585 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.223.98, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 12:17:23 [error] 1568902#1568902: *86586 open() "/opt/logos/www/wordpress/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.183, server: mw-expedition.com, request: "GET /wordpress/wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"
2026/01/15 12:17:33 [error] 1568902#1568902: *86586 open() "/opt/logos/www/wp-admin/setup-config.php" failed (2: No such file or directory), client: 104.23.221.183, server: mw-expedition.com, request: "GET /wp-admin/setup-config.php HTTP/2.0", host: "logosblockchain.com"

```

## NGINX LOG TAIL: /var/log/nginx/access.log

```
149.50.103.48 - - [15/Jan/2026:07:33:49 +0000] "GET / HTTP/1.1" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46"
104.23.209.154 - - [15/Jan/2026:07:34:46 +0000] "GET / HTTP/1.1" 301 178 "http://logosblockchain.com/" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.71 Safari/534.24"
172.71.191.32 - - [15/Jan/2026:07:34:46 +0000] "GET / HTTP/2.0" 200 54542 "http://logosblockchain.com/" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.71 Safari/534.24"
172.68.164.8 - - [15/Jan/2026:07:43:22 +0000] "POST / HTTP/2.0" 405 568 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
172.68.164.8 - - [15/Jan/2026:07:43:22 +0000] "POST /index.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
172.68.164.8 - - [15/Jan/2026:07:43:22 +0000] "POST /admin HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
172.68.164.8 - - [15/Jan/2026:07:43:22 +0000] "POST /api HTTP/2.0" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
172.68.164.8 - - [15/Jan/2026:07:43:23 +0000] "GET /api/ HTTP/2.0" 404 0 "https://logosblockchain.com:443/api" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
185.62.203.253 - - [15/Jan/2026:07:43:36 +0000] "POST /onvif/device_service HTTP/1.1" 301 178 "-" "-"
185.62.203.253 - - [15/Jan/2026:07:43:36 +0000] "POST /onvif/device_service HTTP/1.1" 404 162 "-" "-"
216.73.216.102 - - [15/Jan/2026:07:44:33 +0000] "GET /robots.txt HTTP/2.0" 404 162 "-" "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; ClaudeBot/1.0; +claudebot@anthropic.com)"
216.73.216.102 - - [15/Jan/2026:07:44:33 +0000] "GET /explorer/explorer.js HTTP/2.0" 200 2957 "-" "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; ClaudeBot/1.0; +claudebot@anthropic.com)"
193.32.127.137 - - [15/Jan/2026:07:47:41 +0000] "\x16\x03\x00\x00i\x01\x00\x00e\x03\x03U\x1C\xA7\xE4random1random2random3random4\x00\x00\x0C\x00/\x00" 400 166 "-" "-"
193.32.127.137 - - [15/Jan/2026:07:47:41 +0000] "GET /server-status HTTP/1.1" 404 162 "-" "Mozilla/5.0 (compatible; Nmap Scripting Engine; https://nmap.org/book/nse.html)"
193.32.127.137 - - [15/Jan/2026:07:47:41 +0000] "GET /server-status HTTP/1.1" 301 178 "-" "Mozilla/5.0 (compatible; Nmap Scripting Engine; https://nmap.org/book/nse.html)"
104.23.223.98 - - [15/Jan/2026:07:47:46 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "https://logosblockchain.com/wp-admin/setup-config.php"
104.23.217.56 - - [15/Jan/2026:07:49:09 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "http://logosblockchain.com/wordpress/wp-admin/setup-config.php"
104.23.217.57 - - [15/Jan/2026:07:49:09 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "http://logosblockchain.com/wordpress/wp-admin/setup-config.php"
216.73.216.102 - - [15/Jan/2026:07:50:05 +0000] "GET /shared/wallet-theme.css HTTP/2.0" 200 7700 "-" "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; ClaudeBot/1.0; +claudebot@anthropic.com)"
216.73.216.102 - - [15/Jan/2026:07:50:35 +0000] "GET /explorer/explorer.css HTTP/2.0" 200 2086 "-" "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; ClaudeBot/1.0; +claudebot@anthropic.com)"
104.23.223.99 - - [15/Jan/2026:07:50:47 +0000] "GET /wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "http://logosblockchain.com/wp-admin/setup-config.php"
104.23.223.99 - - [15/Jan/2026:07:50:47 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "http://logosblockchain.com/wp-admin/setup-config.php"
104.23.221.182 - - [15/Jan/2026:07:51:17 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "https://logosblockchain.com/wordpress/wp-admin/setup-config.php"
172.71.123.212 - - [15/Jan/2026:07:58:08 +0000] "GET /robots.txt HTTP/2.0" 404 162 "-" "Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)"
172.70.91.32 - - [15/Jan/2026:07:58:11 +0000] "GET / HTTP/2.0" 200 54542 "-" "Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)"
162.158.178.213 - - [15/Jan/2026:07:58:27 +0000] "POST / HTTP/2.0" 405 568 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
162.158.178.248 - - [15/Jan/2026:07:58:27 +0000] "POST /index.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
162.158.178.248 - - [15/Jan/2026:07:58:27 +0000] "POST /admin HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
162.158.178.248 - - [15/Jan/2026:07:58:28 +0000] "POST /api HTTP/2.0" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
162.158.178.248 - - [15/Jan/2026:07:58:28 +0000] "GET /api/ HTTP/2.0" 404 0 "https://logosblockchain.com:443/api" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
104.23.223.98 - - [15/Jan/2026:08:04:55 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "http://logosblockchain.com/wordpress/wp-admin/setup-config.php"
104.23.223.98 - - [15/Jan/2026:08:04:55 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "http://logosblockchain.com/wordpress/wp-admin/setup-config.php"
216.180.246.47 - - [15/Jan/2026:08:05:42 +0000] "GET / HTTP/1.0" 301 178 "-" "'Mozilla/5.0 (compatible; GenomeCrawlerd/1.0; +https://www.nokia.com/genomecrawler)'"
216.180.246.47 - - [15/Jan/2026:08:05:54 +0000] "\x16\x03\x01\x00\xEE\x01\x00\x00\xEA\x03\x03\xBD\xBC \xF7ji~N\xA2\x03\x9F\x02%\xFC\x1B\x02\xE7\x02UC\x08\x80\x95\xE7\x83\xC5\xAA\x81\x9B\xC4|\x8A C\xE5y\xBC\x18k\x86\xF1|1\x82\xA2O\x12#\xF8\xA0L\x08\xF3\x8E\xDF\xAA\xD7\xF3\xD4qWV\xB1\x00\xB8\x00&\xCC\xA8\xCC\xA9\xC0/\xC00\xC0+\xC0,\xC0\x13\xC0\x09\xC0\x14\xC0" 400 166 "-" "-"
216.180.246.47 - - [15/Jan/2026:08:06:24 +0000] "GET / HTTP/1.1" 301 178 "-" "'Mozilla/5.0 (compatible; GenomeCrawlerd/1.0; +https://www.nokia.com/genomecrawler)'"
172.69.151.230 - - [15/Jan/2026:08:07:12 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "https://logosblockchain.com/wordpress/wp-admin/setup-config.php"
216.180.246.47 - - [15/Jan/2026:08:07:31 +0000] "GET /manage/account/login HTTP/1.1" 301 178 "-" "'Mozilla/5.0 (compatible; GenomeCrawlerd/1.0; +https://www.nokia.com/genomecrawler)'"
172.71.172.64 - - [15/Jan/2026:08:08:04 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
216.180.246.47 - - [15/Jan/2026:08:08:06 +0000] "GET /admin/index.html HTTP/1.1" 301 178 "-" "'Mozilla/5.0 (compatible; GenomeCrawlerd/1.0; +https://www.nokia.com/genomecrawler)'"
216.180.246.47 - - [15/Jan/2026:08:08:42 +0000] "GET /index.html HTTP/1.1" 301 178 "-" "'Mozilla/5.0 (compatible; GenomeCrawlerd/1.0; +https://www.nokia.com/genomecrawler)'"
104.23.221.182 - - [15/Jan/2026:08:08:46 +0000] "GET /wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "http://logosblockchain.com/wp-admin/setup-config.php"
104.23.221.183 - - [15/Jan/2026:08:08:47 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "http://logosblockchain.com/wp-admin/setup-config.php"
216.180.246.47 - - [15/Jan/2026:08:09:19 +0000] "GET /+CSCOE+/logon.html HTTP/1.1" 301 178 "-" "'Mozilla/5.0 (compatible; GenomeCrawlerd/1.0; +https://www.nokia.com/genomecrawler)'"
216.180.246.47 - - [15/Jan/2026:08:09:55 +0000] "GET /cgi-bin/login.cgi HTTP/1.1" 301 178 "-" "'Mozilla/5.0 (compatible; GenomeCrawlerd/1.0; +https://www.nokia.com/genomecrawler)'"
216.180.246.47 - - [15/Jan/2026:08:10:29 +0000] "GET /login.htm HTTP/1.1" 301 178 "-" "'Mozilla/5.0 (compatible; GenomeCrawlerd/1.0; +https://www.nokia.com/genomecrawler)'"
216.180.246.47 - - [15/Jan/2026:08:11:03 +0000] "GET /login.html HTTP/1.1" 301 178 "-" "'Mozilla/5.0 (compatible; GenomeCrawlerd/1.0; +https://www.nokia.com/genomecrawler)'"
5.183.209.196 - - [15/Jan/2026:08:11:30 +0000] "GET /SDK/webLanguage HTTP/1.1" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46"
216.180.246.47 - - [15/Jan/2026:08:11:41 +0000] "GET /login.jsp HTTP/1.1" 301 178 "-" "'Mozilla/5.0 (compatible; GenomeCrawlerd/1.0; +https://www.nokia.com/genomecrawler)'"
216.180.246.47 - - [15/Jan/2026:08:12:43 +0000] "GET /login HTTP/1.1" 301 178 "-" "'Mozilla/5.0 (compatible; GenomeCrawlerd/1.0; +https://www.nokia.com/genomecrawler)'"
216.180.246.47 - - [15/Jan/2026:08:13:45 +0000] "GET /doc/index.html HTTP/1.1" 301 178 "-" "'Mozilla/5.0 (compatible; GenomeCrawlerd/1.0; +https://www.nokia.com/genomecrawler)'"
216.180.246.47 - - [15/Jan/2026:08:14:39 +0000] "GET /remote/login HTTP/1.1" 301 178 "-" "'Mozilla/5.0 (compatible; GenomeCrawlerd/1.0; +https://www.nokia.com/genomecrawler)'"
216.180.246.47 - - [15/Jan/2026:08:15:39 +0000] "GET //admin/login.asp HTTP/1.1" 301 178 "-" "'Mozilla/5.0 (compatible; GenomeCrawlerd/1.0; +https://www.nokia.com/genomecrawler)'"
216.180.246.47 - - [15/Jan/2026:08:16:17 +0000] "GET /web/ HTTP/1.1" 301 178 "-" "'Mozilla/5.0 (compatible; GenomeCrawlerd/1.0; +https://www.nokia.com/genomecrawler)'"
216.180.246.47 - - [15/Jan/2026:08:17:02 +0000] "GET //webpages/login.html HTTP/1.1" 301 178 "-" "'Mozilla/5.0 (compatible; GenomeCrawlerd/1.0; +https://www.nokia.com/genomecrawler)'"
91.231.89.148 - - [15/Jan/2026:08:18:17 +0000] "GET / HTTP/1.1" 200 54542 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0"
108.162.226.137 - - [15/Jan/2026:08:19:01 +0000] "POST / HTTP/2.0" 405 568 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
108.162.227.149 - - [15/Jan/2026:08:19:01 +0000] "POST /index.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
108.162.227.149 - - [15/Jan/2026:08:19:02 +0000] "POST /admin HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
108.162.227.149 - - [15/Jan/2026:08:19:02 +0000] "POST /api HTTP/2.0" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
108.162.227.149 - - [15/Jan/2026:08:19:02 +0000] "GET /api/ HTTP/2.0" 404 0 "https://logosblockchain.com:443/api" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
91.196.152.15 - - [15/Jan/2026:08:20:40 +0000] "GET /favicon.ico HTTP/1.1" 404 162 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0"
104.23.221.182 - - [15/Jan/2026:08:21:44 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "https://logosblockchain.com/wordpress/wp-admin/setup-config.php"
104.23.223.98 - - [15/Jan/2026:08:23:55 +0000] "GET /wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "http://logosblockchain.com/wp-admin/setup-config.php"
104.23.223.99 - - [15/Jan/2026:08:23:55 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "http://logosblockchain.com/wp-admin/setup-config.php"
162.158.110.44 - - [15/Jan/2026:08:24:23 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "http://logosblockchain.com/wordpress/wp-admin/setup-config.php"
162.158.110.44 - - [15/Jan/2026:08:24:24 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "http://logosblockchain.com/wordpress/wp-admin/setup-config.php"
172.71.144.155 - - [15/Jan/2026:08:24:56 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
216.81.248.30 - - [15/Jan/2026:08:25:44 +0000] "GET /.git/config HTTP/1.1" 404 564 "-" "Mozilla/5.0 (CentOS; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
45.156.128.47 - - [15/Jan/2026:08:30:39 +0000] "GET / HTTP/1.1" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
45.156.128.126 - - [15/Jan/2026:08:30:39 +0000] "GET / HTTP/1.1" 200 54542 "http://45.159.248.232/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
104.23.170.106 - - [15/Jan/2026:08:31:38 +0000] "POST / HTTP/2.0" 405 568 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
104.23.170.106 - - [15/Jan/2026:08:31:38 +0000] "POST /index.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
104.23.170.106 - - [15/Jan/2026:08:31:39 +0000] "POST /admin HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
104.23.170.106 - - [15/Jan/2026:08:31:39 +0000] "POST /api HTTP/2.0" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
104.23.170.106 - - [15/Jan/2026:08:31:39 +0000] "GET /api/ HTTP/2.0" 404 0 "https://logosblockchain.com:443/api" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
162.158.178.212 - - [15/Jan/2026:08:31:51 +0000] "POST / HTTP/2.0" 405 568 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
162.158.178.212 - - [15/Jan/2026:08:31:51 +0000] "POST /index.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
162.158.178.212 - - [15/Jan/2026:08:31:51 +0000] "POST /admin HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
162.158.178.212 - - [15/Jan/2026:08:31:51 +0000] "POST /api HTTP/2.0" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
162.158.178.212 - - [15/Jan/2026:08:31:51 +0000] "GET /api/ HTTP/2.0" 404 0 "https://logosblockchain.com:443/api" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
167.86.107.35 - - [15/Jan/2026:08:32:48 +0000] "GET / HTTP/1.1" 301 178 "-" "Mozilla/5.0"
216.108.237.50 - - [15/Jan/2026:08:35:49 +0000] "POST /cgi-bin/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/bin/sh HTTP/1.1" 400 166 "-" "-"
172.70.111.166 - - [15/Jan/2026:08:37:03 +0000] "GET / HTTP/2.0" 200 54542 "-" "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1"
104.23.190.133 - - [15/Jan/2026:08:37:03 +0000] "GET / HTTP/2.0" 200 54542 "-" "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1"
162.158.155.113 - - [15/Jan/2026:08:37:04 +0000] "GET /styles.v20251124.css HTTP/2.0" 404 162 "https://logosblockchain.com/" "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1"
162.159.119.12 - - [15/Jan/2026:08:37:04 +0000] "GET /styles.v20251124.css HTTP/2.0" 404 162 "https://www.logosblockchain.com/" "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1"
104.23.190.71 - - [15/Jan/2026:08:37:04 +0000] "GET /favicon.ico HTTP/2.0" 404 162 "https://www.logosblockchain.com/" "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1"
104.23.187.49 - - [15/Jan/2026:08:37:04 +0000] "GET /favicon.ico HTTP/2.0" 404 162 "https://logosblockchain.com/" "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1"
104.23.175.155 - - [15/Jan/2026:08:37:38 +0000] "POST / HTTP/2.0" 405 568 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
104.23.175.141 - - [15/Jan/2026:08:37:39 +0000] "POST /index.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
104.23.175.141 - - [15/Jan/2026:08:37:39 +0000] "POST /admin HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
104.23.175.141 - - [15/Jan/2026:08:37:39 +0000] "POST /api HTTP/2.0" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
104.23.175.141 - - [15/Jan/2026:08:37:39 +0000] "GET /api/ HTTP/2.0" 404 0 "https://logosblockchain.com:443/api" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
104.23.221.182 - - [15/Jan/2026:08:38:19 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
147.185.132.3 - - [15/Jan/2026:08:38:31 +0000] "GET / HTTP/1.1" 301 178 "-" "Hello from Palo Alto Networks, find out more about our scans in https://docs-cortex.paloaltonetworks.com/r/1/Cortex-Xpanse/Scanning-activity"
147.185.132.3 - - [15/Jan/2026:08:38:31 +0000] "GET / HTTP/1.1" 200 54542 "http://45.159.248.232:80/" "Hello from Palo Alto Networks, find out more about our scans in https://docs-cortex.paloaltonetworks.com/r/1/Cortex-Xpanse/Scanning-activity"
98.92.66.49 - - [15/Jan/2026:08:39:11 +0000] "\x16\x03\x01\x02\x00\x01\x00\x01\xFC\x03\x03\xCBQQq\xBFd\x93\x01\xBAYA\x92,^vS\xB6\xAB\xEB\x00\x8B\xF5\x9A\xFD:\x180G_\xFD\xE4\xAC \xB7#p\x92\xB6-C\xCA\xE4o\xF3\x9E\xA4@\xD7{\xC6\x8B\xC7\xE0\x86+\x0FI\xA7\xF2mEJ\x85\xED\x0F\x00\x98\x13\x02\x13\x03\x13\x01\x13\x04\xC0,\xC00\x00\x9F\xCC\xA9\xCC\xA8\xCC\xAA\xC0\xAD\xC0\x9F\xC0]\xC0a\xC0S\x00\xA7\xC0+\xC0/\x00\x9E\xC0\xAC\xC0\x9E\xC0\x5C\xC0`\xC0R\x00\xA6\xC0\xAF\xC0\xAE\xC0\xA3\xC0\xA2\xC0$\xC0(\x00k\xC0s\xC0w\x00\xC4\x00m\x00\xC5\xC0#\xC0'\x00g\xC0r\xC0v\x00\xBE\x00l\x00\xBF\xC0" 400 166 "-" "-"
104.23.217.57 - - [15/Jan/2026:08:39:42 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "http://logosblockchain.com/wordpress/wp-admin/setup-config.php"
104.23.217.57 - - [15/Jan/2026:08:39:42 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "http://logosblockchain.com/wordpress/wp-admin/setup-config.php"
104.23.217.57 - - [15/Jan/2026:08:41:05 +0000] "GET /wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "http://logosblockchain.com/wp-admin/setup-config.php"
104.23.217.57 - - [15/Jan/2026:08:41:05 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "http://logosblockchain.com/wp-admin/setup-config.php"
104.23.223.99 - - [15/Jan/2026:08:41:10 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "https://logosblockchain.com/wordpress/wp-admin/setup-config.php"
191.6.255.74 - - [15/Jan/2026:08:42:35 +0000] "POST /xmlrpc.php HTTP/1.1" 404 162 "-" "Mozilla/5.0 (Windows NT 6.2; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/87.0.0.0 Safari/537.36"
46.105.40.140 - - [15/Jan/2026:08:43:21 +0000] "GET /robots.txt HTTP/1.1" 404 162 "-" "Mozilla/5.0 (compatible; MJ12bot/v2.0.4; http://mj12bot.com/)"
46.105.40.140 - - [15/Jan/2026:08:43:21 +0000] "GET / HTTP/1.1" 200 54542 "-" "Mozilla/5.0 (compatible; MJ12bot/v2.0.4; http://mj12bot.com/)"
54.164.233.234 - - [15/Jan/2026:08:43:34 +0000] "GET / HTTP/1.1" 301 178 "-" ""
54.164.233.234 - - [15/Jan/2026:08:43:34 +0000] "GET / HTTP/1.1" 301 178 "-" ""
54.164.233.234 - - [15/Jan/2026:08:43:34 +0000] "GET / HTTP/1.1" 200 54542 "-" ""
54.164.233.234 - - [15/Jan/2026:08:43:35 +0000] "GET / HTTP/1.1" 400 264 "-" ""
54.164.233.234 - - [15/Jan/2026:08:43:35 +0000] "\x16\x03\x01\x02\x00\x01\x00\x01\xFC\x03\x03\xC5\xC0\xCDl?\xFB\x01\xED\x9C\xC0C\x07}jS\x90\x9E\x19\xCD\xDC\xF8\xCC<Z6\xA0\xFF\xBBQ\xC5\xAB\xFD \xB0\xCB$N\xC3\x1E#\xF4\xAF.\xEF\x99d\xE4\xB6\xB2\x92\xB2]\xC0R\x8E\x1C\xA4<]\xBDC\x0F\xB3\xBD\xBC\x00&\x13\x02\x13\x03\x13\x01\x13\x04\xC0,\xC00\xC0+\xC0/\xCC\xA9\xCC\xA8\xC0$\xC0(\xC0#\xC0'\x00\x9F\x00\x9E\x00k\x00g\x00\xFF\x01\x00\x01\x8D\x00\x0B\x00\x04\x03\x00\x01\x02\x00" 400 166 "-" "-"
54.164.233.234 - - [15/Jan/2026:08:43:36 +0000] "GET / HTTP/1.1" 200 54542 "-" ""
50.19.12.17 - - [15/Jan/2026:08:44:51 +0000] "GET /FSnU HTTP/1.1" 301 178 "-" ""
50.19.12.17 - - [15/Jan/2026:08:44:51 +0000] "GET /FSnU HTTP/1.1" 404 162 "-" ""
50.19.12.17 - - [15/Jan/2026:08:44:52 +0000] "GET /OEpY HTTP/1.1" 301 178 "-" ""
50.19.12.17 - - [15/Jan/2026:08:44:52 +0000] "GET /OEpY HTTP/1.1" 404 162 "-" ""
50.19.12.17 - - [15/Jan/2026:08:44:52 +0000] "GET /aBBw HTTP/1.1" 400 264 "-" ""
50.19.12.17 - - [15/Jan/2026:08:44:52 +0000] "GET /VQSc HTTP/1.1" 400 264 "-" ""
50.19.12.17 - - [15/Jan/2026:08:44:53 +0000] "\x16\x03\x01\x02\x00\x01\x00\x01\xFC\x03\x03\xBFL\xB6\x18\xDE\x1C r\x07\x87\x12D\xD0{a\xC7]\x97\xF8\x18`\xB6\xF1\xE6$`\xE1\xB4\xF1\xEB\x80\x19 \x0E\x0E\x05\x1D\xB79@\xF6B\x8F\xE4\xA2\x0FZ\x18\xEF]\x85\xF8\xC5\x93\xC4\xD3\xAE%\x85\xC4\x5CL?\xBFG\x00&\x13\x02\x13\x03\x13\x01\x13\x04\xC0,\xC00\xC0+\xC0/\xCC\xA9\xCC\xA8\xC0$\xC0(\xC0#\xC0'\x00\x9F\x00\x9E\x00k\x00g\x00\xFF\x01\x00\x01\x8D\x00\x0B\x00\x04\x03\x00\x01\x02\x00" 400 166 "-" "-"
50.19.12.17 - - [15/Jan/2026:08:44:53 +0000] "\x16\x03\x01\x02\x00\x01\x00\x01\xFC\x03\x03\xCF\xB5\x22\x1Bm\xCC@p\xD9GH\xEF\xB1=\x8A\xCA^\x17!~>q\xBARA\xA8\x84j\x11\xCE4\xF1 \xDC\xDA\xE5\xE2\xC1VQ&l\x84\xBF\xE1\x1B\x83\x19g\xC2\xA3? " 400 166 "-" "-"
50.19.12.17 - - [15/Jan/2026:08:44:53 +0000] "GET /DYQn HTTP/1.1" 404 162 "-" ""
50.19.12.17 - - [15/Jan/2026:08:44:54 +0000] "GET /SKGx HTTP/1.1" 404 162 "-" ""
104.23.221.182 - - [15/Jan/2026:08:55:28 +0000] "GET /wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "http://logosblockchain.com/wp-admin/setup-config.php"
104.23.221.183 - - [15/Jan/2026:08:55:28 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "http://logosblockchain.com/wp-admin/setup-config.php"
162.158.183.98 - - [15/Jan/2026:08:56:38 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "http://logosblockchain.com/wordpress/wp-admin/setup-config.php"
162.158.183.97 - - [15/Jan/2026:08:56:39 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "http://logosblockchain.com/wordpress/wp-admin/setup-config.php"
162.158.183.97 - - [15/Jan/2026:08:56:48 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "https://logosblockchain.com/wp-admin/setup-config.php"
162.158.183.98 - - [15/Jan/2026:08:57:59 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "https://logosblockchain.com/wordpress/wp-admin/setup-config.php"
185.189.182.234 - - [15/Jan/2026:08:58:44 +0000] "GET /2dVp HTTP/1.1" 400 166 "-" "-"
162.158.178.212 - - [15/Jan/2026:09:03:26 +0000] "POST / HTTP/2.0" 405 568 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
162.158.178.248 - - [15/Jan/2026:09:03:26 +0000] "POST /index.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
162.158.178.248 - - [15/Jan/2026:09:03:27 +0000] "POST /admin HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
162.158.178.248 - - [15/Jan/2026:09:03:27 +0000] "POST /api HTTP/2.0" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
162.158.178.248 - - [15/Jan/2026:09:03:27 +0000] "GET /api/ HTTP/2.0" 404 0 "https://logosblockchain.com:443/api" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
149.50.103.48 - - [15/Jan/2026:09:12:51 +0000] "GET / HTTP/1.1" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46"
104.23.221.183 - - [15/Jan/2026:09:15:24 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "http://logosblockchain.com/wordpress/wp-admin/setup-config.php"
104.23.221.182 - - [15/Jan/2026:09:15:24 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "http://logosblockchain.com/wordpress/wp-admin/setup-config.php"
104.23.221.182 - - [15/Jan/2026:09:16:32 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "https://logosblockchain.com/wordpress/wp-admin/setup-config.php"
162.158.110.45 - - [15/Jan/2026:09:16:36 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
104.23.221.182 - - [15/Jan/2026:09:17:19 +0000] "GET /wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
104.23.221.182 - - [15/Jan/2026:09:17:19 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
104.23.221.222 - - [15/Jan/2026:09:19:43 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
104.23.221.223 - - [15/Jan/2026:09:19:43 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
104.23.221.222 - - [15/Jan/2026:09:19:52 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
104.23.221.222 - - [15/Jan/2026:09:20:50 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "https://mw-expedition.com/wordpress/wp-admin/setup-config.php"
104.23.223.19 - - [15/Jan/2026:09:21:13 +0000] "GET /wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
104.23.223.19 - - [15/Jan/2026:09:21:14 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
142.44.233.122 - - [15/Jan/2026:09:25:31 +0000] "GET /robots.txt HTTP/2.0" 404 162 "-" "Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)"
198.244.240.55 - - [15/Jan/2026:09:25:34 +0000] "GET / HTTP/2.0" 200 54542 "-" "Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)"
104.23.221.182 - - [15/Jan/2026:09:31:12 +0000] "GET /wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "http://logosblockchain.com/wp-admin/setup-config.php"
104.23.221.183 - - [15/Jan/2026:09:31:12 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "http://logosblockchain.com/wp-admin/setup-config.php"
104.23.221.183 - - [15/Jan/2026:09:31:27 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
104.23.221.183 - - [15/Jan/2026:09:32:11 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "https://logosblockchain.com/wordpress/wp-admin/setup-config.php"
172.71.164.20 - - [15/Jan/2026:09:35:07 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
172.71.164.30 - - [15/Jan/2026:09:35:07 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
162.159.98.201 - - [15/Jan/2026:09:35:43 +0000] "POST / HTTP/2.0" 405 568 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
162.159.98.201 - - [15/Jan/2026:09:35:43 +0000] "POST /index.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
162.159.98.201 - - [15/Jan/2026:09:35:43 +0000] "POST /admin HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
162.159.98.201 - - [15/Jan/2026:09:35:43 +0000] "POST /api HTTP/2.0" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
162.159.98.201 - - [15/Jan/2026:09:35:43 +0000] "GET /api/ HTTP/2.0" 404 0 "https://logosblockchain.com:443/api" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
172.64.213.104 - - [15/Jan/2026:09:38:25 +0000] "GET / HTTP/1.1" 301 178 "-" "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
172.70.123.116 - - [15/Jan/2026:09:38:26 +0000] "GET / HTTP/2.0" 200 54542 "http://logosblockchain.com" "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
5.183.209.196 - - [15/Jan/2026:09:41:26 +0000] "GET /SDK/webLanguage HTTP/1.1" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46"
43.166.128.187 - - [15/Jan/2026:09:45:07 +0000] "GET / HTTP/1.1" 400 264 "-" "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
172.71.218.240 - - [15/Jan/2026:09:45:32 +0000] "POST / HTTP/2.0" 405 568 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
172.71.218.240 - - [15/Jan/2026:09:45:32 +0000] "POST /index.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
172.71.218.240 - - [15/Jan/2026:09:45:32 +0000] "POST /admin HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
172.71.218.240 - - [15/Jan/2026:09:45:33 +0000] "POST /api HTTP/2.0" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
172.71.218.240 - - [15/Jan/2026:09:45:33 +0000] "GET /api/ HTTP/2.0" 404 0 "https://logosblockchain.com:443/api" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
20.55.50.10 - - [15/Jan/2026:09:46:32 +0000] "GET /manager/text/list HTTP/1.1" 301 178 "-" "Mozilla/5.0 zgrab/0.x"
150.241.68.160 - - [15/Jan/2026:09:49:42 +0000] "GET /cdn-cgi/trace HTTP/2.0" 404 162 "-" "Mozilla/5.0"
104.23.223.98 - - [15/Jan/2026:09:50:29 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "http://logosblockchain.com/wordpress/wp-admin/setup-config.php"
104.23.223.98 - - [15/Jan/2026:09:50:29 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "http://logosblockchain.com/wordpress/wp-admin/setup-config.php"
146.148.114.32 - - [15/Jan/2026:09:50:44 +0000] "POST /api/graphql HTTP/1.1" 404 0 "-" "fasthttp"
146.148.114.32 - - [15/Jan/2026:09:50:44 +0000] "POST /graphql HTTP/1.1" 404 162 "-" "fasthttp"
104.23.221.183 - - [15/Jan/2026:09:50:58 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "https://logosblockchain.com/wp-admin/setup-config.php"
104.23.221.182 - - [15/Jan/2026:09:50:58 +0000] "GET /wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "http://logosblockchain.com/wp-admin/setup-config.php"
104.23.221.183 - - [15/Jan/2026:09:50:58 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "http://logosblockchain.com/wp-admin/setup-config.php"
104.23.221.182 - - [15/Jan/2026:09:52:35 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "https://logosblockchain.com/wordpress/wp-admin/setup-config.php"
104.23.175.154 - - [15/Jan/2026:09:52:57 +0000] "POST / HTTP/2.0" 405 568 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
104.23.175.154 - - [15/Jan/2026:09:52:57 +0000] "POST /index.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
104.23.175.154 - - [15/Jan/2026:09:52:57 +0000] "POST /admin HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
104.23.175.154 - - [15/Jan/2026:09:52:58 +0000] "POST /api HTTP/2.0" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
104.23.175.154 - - [15/Jan/2026:09:52:58 +0000] "GET /api/ HTTP/2.0" 404 0 "https://logosblockchain.com:443/api" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
94.26.106.113 - - [15/Jan/2026:09:55:39 +0000] "PROPFIND / HTTP/1.1" 405 166 "http://45.159.248.232:443/" "-"
104.210.140.142 - - [15/Jan/2026:09:59:43 +0000] "GET /robots.txt HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36; compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot"
104.210.140.132 - - [15/Jan/2026:09:59:43 +0000] "GET /robots.txt HTTP/1.1" 301 178 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36; compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot"
104.210.140.142 - - [15/Jan/2026:09:59:43 +0000] "GET /robots.txt HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36; compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot"
104.23.221.182 - - [15/Jan/2026:10:09:31 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
104.23.223.99 - - [15/Jan/2026:10:10:10 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
104.23.221.182 - - [15/Jan/2026:10:10:10 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "https://logosblockchain.com/wordpress/wp-admin/setup-config.php"
104.23.223.98 - - [15/Jan/2026:10:10:10 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
62.210.91.123 - - [15/Jan/2026:10:10:36 +0000] "GET / HTTP/1.1" 200 54542 "-" "Mozilla/5.0 (Linux; Android 10; Pixel 4; rv:92.0) Gecko/20100101 Firefox/92.0"
104.23.223.99 - - [15/Jan/2026:10:10:38 +0000] "GET /wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "http://logosblockchain.com/wp-admin/setup-config.php"
104.23.223.98 - - [15/Jan/2026:10:10:38 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "http://logosblockchain.com/wp-admin/setup-config.php"
172.69.40.154 - - [15/Jan/2026:10:14:55 +0000] "POST / HTTP/2.0" 405 568 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
172.69.40.143 - - [15/Jan/2026:10:14:55 +0000] "POST /index.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
172.69.40.143 - - [15/Jan/2026:10:14:55 +0000] "POST /admin HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
172.69.40.143 - - [15/Jan/2026:10:14:55 +0000] "POST /api HTTP/2.0" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
172.69.40.143 - - [15/Jan/2026:10:14:55 +0000] "GET /api/ HTTP/2.0" 404 0 "https://logosblockchain.com:443/api" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
167.86.107.35 - - [15/Jan/2026:10:20:59 +0000] "GET / HTTP/1.1" 301 178 "-" "Mozilla/5.0"
167.86.107.35 - - [15/Jan/2026:10:21:21 +0000] "POST / HTTP/1.1" 301 178 "-" "Mozilla/5.0"
172.71.144.155 - - [15/Jan/2026:10:27:21 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
172.69.114.106 - - [15/Jan/2026:10:27:40 +0000] "POST / HTTP/2.0" 405 568 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
172.69.114.106 - - [15/Jan/2026:10:27:40 +0000] "POST /index.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
172.69.114.106 - - [15/Jan/2026:10:27:40 +0000] "POST /admin HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
104.23.221.182 - - [15/Jan/2026:10:27:40 +0000] "GET /wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
172.69.114.106 - - [15/Jan/2026:10:27:41 +0000] "POST /api HTTP/2.0" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
172.69.114.106 - - [15/Jan/2026:10:27:41 +0000] "GET /api/ HTTP/2.0" 404 0 "https://logosblockchain.com:443/api" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
104.23.221.182 - - [15/Jan/2026:10:27:41 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
104.23.223.98 - - [15/Jan/2026:10:28:36 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "http://logosblockchain.com/wordpress/wp-admin/setup-config.php"
104.23.223.99 - - [15/Jan/2026:10:28:37 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "http://logosblockchain.com/wordpress/wp-admin/setup-config.php"
104.23.221.182 - - [15/Jan/2026:10:28:51 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "https://logosblockchain.com/wp-admin/setup-config.php"
162.159.120.176 - - [15/Jan/2026:10:31:33 +0000] "POST / HTTP/2.0" 405 568 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
108.162.245.180 - - [15/Jan/2026:10:31:33 +0000] "POST /index.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
108.162.245.180 - - [15/Jan/2026:10:31:33 +0000] "POST /admin HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
108.162.245.180 - - [15/Jan/2026:10:31:34 +0000] "POST /api HTTP/2.0" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
108.162.245.180 - - [15/Jan/2026:10:31:34 +0000] "GET /api/ HTTP/2.0" 404 0 "https://logosblockchain.com:443/api" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
149.50.103.48 - - [15/Jan/2026:10:38:23 +0000] "GET / HTTP/1.1" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46"
104.23.223.98 - - [15/Jan/2026:10:44:32 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "https://logosblockchain.com/wordpress/wp-admin/setup-config.php"
104.23.223.98 - - [15/Jan/2026:10:46:06 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "http://logosblockchain.com/wordpress/wp-admin/setup-config.php"
104.23.223.99 - - [15/Jan/2026:10:46:06 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "http://logosblockchain.com/wordpress/wp-admin/setup-config.php"
104.23.223.99 - - [15/Jan/2026:10:46:27 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "https://logosblockchain.com/wp-admin/setup-config.php"
104.23.223.98 - - [15/Jan/2026:10:47:47 +0000] "GET /wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "http://logosblockchain.com/wp-admin/setup-config.php"
104.23.223.99 - - [15/Jan/2026:10:47:47 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "http://logosblockchain.com/wp-admin/setup-config.php"
147.185.133.87 - - [15/Jan/2026:10:50:09 +0000] "GET / HTTP/1.1" 301 178 "-" "Hello from Palo Alto Networks, find out more about our scans in https://docs-cortex.paloaltonetworks.com/r/1/Cortex-Xpanse/Scanning-activity"
147.185.133.87 - - [15/Jan/2026:10:50:09 +0000] "GET / HTTP/1.1" 200 54542 "http://45.159.248.232:80/" "Hello from Palo Alto Networks, find out more about our scans in https://docs-cortex.paloaltonetworks.com/r/1/Cortex-Xpanse/Scanning-activity"
104.23.221.183 - - [15/Jan/2026:11:02:36 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "http://logosblockchain.com/wordpress/wp-admin/setup-config.php"
104.23.221.182 - - [15/Jan/2026:11:02:36 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "http://logosblockchain.com/wordpress/wp-admin/setup-config.php"
192.121.135.97 - - [15/Jan/2026:11:03:54 +0000] "GET / HTTP/1.1" 301 178 "-" "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604"
192.36.207.10 - - [15/Jan/2026:11:03:54 +0000] "GET / HTTP/1.1" 200 54542 "http://mw-expedition.com/" "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604"
192.36.121.172 - - [15/Jan/2026:11:03:54 +0000] "GET /explorer HTTP/1.1" 301 178 "-" "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604"
192.36.226.103 - - [15/Jan/2026:11:03:54 +0000] "GET /explorer/ HTTP/1.1" 200 1960 "https://mw-expedition.com/explorer" "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604"
192.36.217.48 - - [15/Jan/2026:11:03:54 +0000] "GET /staking HTTP/1.1" 404 162 "-" "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604"
192.36.198.147 - - [15/Jan/2026:11:03:54 +0000] "GET /wallet HTTP/1.1" 301 178 "-" "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604"
192.121.135.97 - - [15/Jan/2026:11:03:54 +0000] "GET /wallet/ HTTP/1.1" 200 94 "https://mw-expedition.com/wallet" "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604"
172.71.182.188 - - [15/Jan/2026:11:04:01 +0000] "GET / HTTP/1.1" 301 178 "-" "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
104.23.221.183 - - [15/Jan/2026:11:04:03 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
104.23.223.98 - - [15/Jan/2026:11:05:13 +0000] "GET /wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "http://logosblockchain.com/wp-admin/setup-config.php"
104.23.223.99 - - [15/Jan/2026:11:05:13 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "http://logosblockchain.com/wp-admin/setup-config.php"
172.71.246.152 - - [15/Jan/2026:11:05:37 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "https://logosblockchain.com/wordpress/wp-admin/setup-config.php"
172.68.211.180 - - [15/Jan/2026:11:07:43 +0000] "POST /index.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
172.68.211.140 - - [15/Jan/2026:11:07:44 +0000] "POST /admin HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
172.68.211.140 - - [15/Jan/2026:11:07:44 +0000] "POST /api HTTP/2.0" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
172.68.211.140 - - [15/Jan/2026:11:07:44 +0000] "GET /api/ HTTP/2.0" 404 0 "https://logosblockchain.com:443/api" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
43.130.141.193 - - [15/Jan/2026:11:16:03 +0000] "GET / HTTP/1.1" 301 178 "-" "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
43.130.141.193 - - [15/Jan/2026:11:16:05 +0000] "GET / HTTP/1.1" 200 54542 "http://mw-expedition.com" "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
172.70.38.160 - - [15/Jan/2026:11:18:12 +0000] "GET / HTTP/1.1" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
104.23.211.87 - - [15/Jan/2026:11:18:12 +0000] "GET / HTTP/2.0" 200 54542 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.151 Whale/3.14.134.62 Safari/537.36"
167.86.107.35 - - [15/Jan/2026:11:21:09 +0000] "GET / HTTP/1.1" 301 178 "-" "Mozilla/5.0"
104.23.221.183 - - [15/Jan/2026:11:21:40 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "https://logosblockchain.com/wordpress/wp-admin/setup-config.php"
172.71.144.155 - - [15/Jan/2026:11:22:08 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
104.23.221.182 - - [15/Jan/2026:11:22:22 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "http://logosblockchain.com/wordpress/wp-admin/setup-config.php"
104.23.221.183 - - [15/Jan/2026:11:22:22 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "http://logosblockchain.com/wordpress/wp-admin/setup-config.php"
104.23.221.182 - - [15/Jan/2026:11:23:10 +0000] "GET /wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "http://logosblockchain.com/wp-admin/setup-config.php"
104.23.221.183 - - [15/Jan/2026:11:23:10 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "http://logosblockchain.com/wp-admin/setup-config.php"
135.237.126.103 - - [15/Jan/2026:11:32:59 +0000] "GET /autodiscover/autodiscover.json?@zdi/Powershell HTTP/1.1" 404 162 "-" "Mozilla/5.0 zgrab/0.x"
104.22.1.104 - - [15/Jan/2026:11:36:56 +0000] "GET / HTTP/1.1" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
104.22.24.202 - - [15/Jan/2026:11:36:56 +0000] "GET //wp-includes/ID3/license.txt HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
104.22.24.202 - - [15/Jan/2026:11:36:56 +0000] "GET //feed/ HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
104.22.24.202 - - [15/Jan/2026:11:36:56 +0000] "GET //xmlrpc.php?rsd HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
104.22.24.202 - - [15/Jan/2026:11:36:56 +0000] "GET //blog/wp-includes/wlwmanifest.xml HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
104.22.24.202 - - [15/Jan/2026:11:36:57 +0000] "GET //web/wp-includes/wlwmanifest.xml HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
104.22.24.202 - - [15/Jan/2026:11:36:57 +0000] "GET //wordpress/wp-includes/wlwmanifest.xml HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
104.22.24.202 - - [15/Jan/2026:11:36:57 +0000] "GET //wp/wp-includes/wlwmanifest.xml HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
104.22.24.202 - - [15/Jan/2026:11:36:57 +0000] "GET //2020/wp-includes/wlwmanifest.xml HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
104.22.24.202 - - [15/Jan/2026:11:36:57 +0000] "GET //2019/wp-includes/wlwmanifest.xml HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
104.22.24.202 - - [15/Jan/2026:11:36:57 +0000] "GET //2021/wp-includes/wlwmanifest.xml HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
104.22.24.202 - - [15/Jan/2026:11:36:57 +0000] "GET //shop/wp-includes/wlwmanifest.xml HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
104.22.24.202 - - [15/Jan/2026:11:36:57 +0000] "GET //wp1/wp-includes/wlwmanifest.xml HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
104.22.24.202 - - [15/Jan/2026:11:36:57 +0000] "GET //test/wp-includes/wlwmanifest.xml HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
104.22.24.202 - - [15/Jan/2026:11:36:58 +0000] "GET //site/wp-includes/wlwmanifest.xml HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
104.22.24.202 - - [15/Jan/2026:11:36:58 +0000] "GET //cms/wp-includes/wlwmanifest.xml HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
172.70.175.29 - - [15/Jan/2026:11:37:16 +0000] "GET / HTTP/1.1" 301 178 "-" "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
172.70.38.238 - - [15/Jan/2026:11:37:17 +0000] "GET / HTTP/2.0" 200 54542 "http://www.logosblockchain.com" "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
217.154.69.208 - - [15/Jan/2026:11:37:46 +0000] "POST /cgi-bin/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/bin/sh HTTP/1.1" 400 166 "-" "-"
104.23.221.182 - - [15/Jan/2026:11:42:22 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "https://logosblockchain.com/wp-admin/setup-config.php"
172.71.164.20 - - [15/Jan/2026:11:42:46 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "https://logosblockchain.com/wordpress/wp-admin/setup-config.php"
104.23.221.183 - - [15/Jan/2026:11:43:10 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "http://logosblockchain.com/wordpress/wp-admin/setup-config.php"
104.23.221.182 - - [15/Jan/2026:11:43:10 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "http://logosblockchain.com/wordpress/wp-admin/setup-config.php"
104.23.221.183 - - [15/Jan/2026:11:43:23 +0000] "GET /wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
104.23.221.182 - - [15/Jan/2026:11:43:23 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
104.23.221.182 - - [15/Jan/2026:11:57:10 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "http://logosblockchain.com/wordpress/wp-admin/setup-config.php"
104.23.221.182 - - [15/Jan/2026:11:57:10 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "http://logosblockchain.com/wordpress/wp-admin/setup-config.php"
104.23.221.182 - - [15/Jan/2026:11:59:35 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
104.23.217.57 - - [15/Jan/2026:12:00:08 +0000] "GET /wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
104.23.217.101 - - [15/Jan/2026:12:00:09 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
104.23.217.56 - - [15/Jan/2026:12:00:32 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "https://logosblockchain.com/wordpress/wp-admin/setup-config.php"
149.50.103.48 - - [15/Jan/2026:12:07:39 +0000] "GET / HTTP/1.1" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46"
162.159.113.125 - - [15/Jan/2026:12:09:23 +0000] "POST / HTTP/2.0" 405 568 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
162.159.113.102 - - [15/Jan/2026:12:09:24 +0000] "POST /index.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
162.159.113.102 - - [15/Jan/2026:12:09:24 +0000] "POST /admin HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
162.159.113.102 - - [15/Jan/2026:12:09:24 +0000] "POST /api HTTP/2.0" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
162.159.113.102 - - [15/Jan/2026:12:09:24 +0000] "GET /api/ HTTP/2.0" 404 0 "https://logosblockchain.com:443/api" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
104.23.223.98 - - [15/Jan/2026:12:16:25 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
104.23.223.14 - - [15/Jan/2026:12:16:25 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
104.23.223.98 - - [15/Jan/2026:12:16:40 +0000] "GET /wp-admin/setup-config.php HTTP/1.1" 301 178 "-" "http://logosblockchain.com/wp-admin/setup-config.php"
104.23.223.98 - - [15/Jan/2026:12:16:40 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "http://logosblockchain.com/wp-admin/setup-config.php"
104.23.221.183 - - [15/Jan/2026:12:17:23 +0000] "GET /wordpress/wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "https://logosblockchain.com/wordpress/wp-admin/setup-config.php"
104.23.221.183 - - [15/Jan/2026:12:17:33 +0000] "GET /wp-admin/setup-config.php HTTP/2.0" 404 162 "-" "https://logosblockchain.com/wp-admin/setup-config.php"
20.168.0.45 - - [15/Jan/2026:12:19:30 +0000] "MGLNDD_45.159.248.232_80" 400 166 "-" "-"

```
