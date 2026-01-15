# BOOK 123 — wallet_prod + wallet-proxy + nginx vhost (sanitized)

Собрано: 2026-01-15T11:51:11Z

Секреты/ключи/токены автоматически заменены на: `***`

---

# wallet_prod


## FILE: `/opt/logos/www/wallet_prod/app.html`

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


## FILE: `/opt/logos/www/wallet_prod/app.js`

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


## FILE: `/opt/logos/www/wallet_prod/modules/lgn_send.js`

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


# wallet-proxy


## FILE: `/opt/logos/wallet-proxy/app.py`

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


# nginx vhost (mw-expedition)

