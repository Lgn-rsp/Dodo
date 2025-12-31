# LOGOS — Directory Book: /var/www/logos/explorer

_Generated: 2025-12-31T06:43:51Z_

**Part:** 1

---

## STRUCTURE

```text
/var/www/logos/explorer
```

---

## FILES (FULL SOURCE)


### FILE: /var/www/logos/explorer/explorer.css

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

### FILE: /var/www/logos/explorer/explorer.js

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

### FILE: /var/www/logos/explorer/index.html

```
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta http-equiv="Cache-Control" content="no-store"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS LRB — Explorer</title>
  <style>
    :root{
      --bg:#0b0c10;
      --card:#11151a;
      --line:#1e242c;
      --muted:#9aa4af;
      --txt:#e6edf3;
      --btn:#1665c1;
      --btn-b:#3b7ddd;
    }
    *{box-sizing:border-box;margin:0;padding:0}
    body{font-family:system-ui,Segoe UI,Roboto,Arial,sans-serif;background:var(--bg);color:var(--txt);}
    header{padding:12px 16px;background:var(--card);border-bottom:1px solid var(--line);display:flex;flex-wrap:wrap;gap:10px;align-items:center;}
    header h1{font-size:18px;margin-right:12px;}
    header .pill{display:flex;gap:6px;align-items:center;padding:6px 8px;border-radius:999px;border:1px solid var(--line);background:#0b0f14;}
    header input{background:transparent;border:none;outline:none;color:var(--txt);min-width:260px;}
    header button{border:none;border-radius:999px;padding:6px 10px;background:var(--btn);color:#fff;cursor:pointer;font-size:13px;}
    header button:hover{background:var(--btn-b);}
    #jsStat{font-size:12px;margin-left:auto;color:var(--muted);}
    main{max-width:1100px;margin:18px auto;padding:0 12px;}
    section{background:var(--card);border-radius:14px;border:1px solid var(--line);padding:14px 16px;margin-bottom:14px;}
    h3{margin-bottom:10px;font-size:16px;}
    .row{display:flex;gap:10px;align-items:flex-end;flex-wrap:wrap;}
    .row .grow{flex:1 1 auto;min-width:180px;}
    label{font-size:12px;color:var(--muted);display:block;margin-bottom:4px;}
    input[type="text"],input[type="number"]{
      width:100%;padding:6px 8px;border-radius:8px;border:1px solid var(--line);
      background:#05070b;color:var(--txt);font-size:13px;
    }
    button{padding:6px 10px;border-radius:8px;border:1px solid var(--btn-b);background:var(--btn);color:#fff;font-size:13px;cursor:pointer;}
    button:hover{background:var(--btn-b);}
    pre{
      margin-top:10px;
      background:#05070b;
      border-radius:10px;
      border:1px solid #151b23;
      padding:10px;
      font-family:SFMono-Regular,Menlo,Consolas,monospace;
      font-size:12px;
      max-height:320px;
      overflow:auto;
      white-space:pre;
    }
    table{width:100%;border-collapse:collapse;margin-top:10px;font-size:12px;}
    th,td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;}
    th{color:var(--muted);font-weight:500;}
    tbody tr:nth-child(even){background:#0b0f14;}
    .muted{color:var(--muted);font-size:12px;}
  </style>
</head>
<body>
<header>
  <h1>LOGOS LRB — исследователь</h1>
  <div class="pill">
    <input id="q" placeholder="Поиск: RID, высота блока или from:nonce"/>
    <button onclick="search()">Найти</button>
  </div>
  <div id="jsStat">js: загрузка…</div>
</header>

<main>

  <section>
    <h3>Голова</h3>
    <div class="row">
      <div class="grow">
        <button onclick="fetchHead()">GET /head</button>
        <button onclick="toggleAuto()">Автообновление</button>
      </div>
    </div>
    <pre id="out-head"></pre>
  </section>

  <section>
    <h3>Блок</h3>
    <div class="row">
      <div class="grow">
        <label>высота блока (например 1)</label>
        <input id="inp-height" type="number" min="1" placeholder="например 1"/>
      </div>
      <div class="grow">
        <button onclick="fetchBlock()">/block/:height</button>
      </div>
    </div>
    <pre id="out-block"></pre>
  </section>

  <section>
    <h3>Адрес (RID)</h3>
    <div class="row">
      <div class="grow">
        <label>RID (base58)</label>
        <input id="inp-rid" type="text" placeholder="RID"/>
      </div>
      <div class="grow">
        <label>limit</label>
        <input id="inp-limit" type="number" min="1" max="200" value="20"/>
      </div>
      <div class="grow">
        <button onclick="fetchHistory()">GET /history/:rid</button>
      </div>
    </div>
    <div class="muted" style="margin-top:6px;">nonce, from, to, amount, height, ts</div>
    <table>
      <thead>
        <tr>
          <th>nonce</th>
          <th>from</th>
          <th>to</th>
          <th>amount</th>
          <th>height</th>
          <th>ts</th>
        </tr>
      </thead>
      <tbody id="hist-body">
        <tr><td colspan="6" class="muted">нет данных</td></tr>
      </tbody>
    </table>
    <pre id="out-history" style="display:none"></pre>
  </section>

</main>

<script>
(function(){
  const API = location.origin.replace(/\/$/, "") + "/api";
  const $  = s => document.querySelector(s);
  const setStat = (t, ok) => {
    const s = $("#jsStat");
    if (!s) return;
    s.textContent = t;
    s.style.color = ok ? "#0bd464" : "#ff5252";
  };
  const fmtNum = n => Number(n).toLocaleString("ru-RU");
  const fmtTs  = ms => (isFinite(ms) ? new Date(Number(ms)).toLocaleString("ru-RU") : "");

  async function jget(path){
    try {
      const r = await fetch(API + path, { cache: "no-store" });
      if (!r.ok) {
        const text = (await r.text()).slice(0, 200);
        return { error: r.status + " " + text };
      }
      return await r.json();
    } catch (e) {
      return { error: String(e) };
    }
  }

  // HEAD
  let autoTimer = null;
  window.fetchHead = async () => {
    const j = await jget("/head");
    $("#out-head").textContent = JSON.stringify(j, null, 2);
  };

  window.toggleAuto = () => {
    if (autoTimer) {
      clearInterval(autoTimer);
      autoTimer = null;
      setStat("js: автообновление выключено", true);
    } else {
      autoTimer = setInterval(() => window.fetchHead(), 5000);
      setStat("js: автообновление включено", true);
      window.fetchHead();
    }
  };

  // BLOCK
  window.fetchBlock = async () => {
    const h = Number($("#inp-height").value) || 0;
    if (!h) {
      alert("Укажи высоту блока");
      return;
    }
    const j = await jget("/block/" + h);
    $("#out-block").textContent = JSON.stringify(j, null, 2);
  };

  // HISTORY
  function renderRows(arr) {
    const tb = $("#hist-body");
    tb.innerHTML = "";
    if (!arr || arr.length === 0) {
      const tr = document.createElement("tr");
      tr.innerHTML = '<td colspan="6" class="muted">нет записей</td>';
      tb.appendChild(tr);
      return;
    }
    for (const tx of arr) {
      const tr = document.createElement("tr");
      tr.innerHTML =
        `<td>${tx.nonce ?? ""}</td>` +
        `<td>${tx.from ?? ""}</td>` +
        `<td>${tx.to ?? ""}</td>` +
        `<td>${fmtNum(tx.amount ?? 0)}</td>` +
        `<td>${tx.height ?? ""}</td>` +
        `<td>${tx.ts ? fmtTs(tx.ts * 1000) : ""}</td>`;
      tb.appendChild(tr);
    }
  }

  window.fetchHistory = async () => {
    const rid = ($("#inp-rid").value || "").trim();
    if (!rid) {
      alert("Укажи RID");
      return;
    }
    const j = await jget("/history/" + encodeURIComponent(rid));
    $("#out-history").textContent = JSON.stringify(j, null, 2);
    renderRows(j);
  };

  window.search = async () => {
    const q = ($("#q").value || "").trim();
    if (!q) return;

    if (/^\d+$/.test(q)) {
      $("#inp-height").value = q;
      await window.fetchBlock();
      return;
    }

    if (/^[1-9A-HJ-NP-Za-km-z]+$/.test(q) && q.length > 30) {
      $("#inp-rid").value = q;
      await window.fetchHistory();
      return;
    }

    if (q.includes(":")) {
      const [from, nonce] = q.split(":");
      $("#inp-rid").value = from.trim();
      await window.fetchHistory();
      [...document.querySelectorAll("#hist-body tr")].forEach(tr => {
        if (tr.firstChild && tr.firstChild.textContent === (nonce || "").trim()) {
          tr.style.background = "#132235";
        }
      });
      return;
    }

    alert("Не распознан формат запроса. Используй: RID, номер блока или from:nonce");
  };

  setStat("js: готов", true);
})();
</script>
</body>
</html>

```
