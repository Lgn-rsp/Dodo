# LOGOS — Directory Book

## ROOT: /var/www/logos

---
## STRUCTURE
```
/var/www/logos
/var/www/logos/css
/var/www/logos/explorer
/var/www/logos/js
/var/www/logos/landing
/var/www/logos/landing/assets
/var/www/logos/landing/css
/var/www/logos/landing/explorer
/var/www/logos/landing/i18n
/var/www/logos/landing/js
/var/www/logos/landing/landing
/var/www/logos/landing/landing/assets
/var/www/logos/landing/landing/i18n
/var/www/logos/landing/landing/logos_tg_bot
/var/www/logos/landing/landing/logos_tg_bot/logos_guard_bot
/var/www/logos/landing/landing/logos_tg_bot/logos_guard_bot/bot
/var/www/logos/landing/landing/logos_tg_bot/logos_guard_bot/bot/handlers
/var/www/logos/landing/landing/logos_tg_bot/logos_guard_bot/bot/services
/var/www/logos/landing/landing/modules
/var/www/logos/landing/landing/shared
/var/www/logos/landing/landing/wallet
/var/www/logos/landing/modules
/var/www/logos/landing/shared
/var/www/logos/landing/wallet
/var/www/logos/landing/wallet3
/var/www/logos/landing/wallet/css
/var/www/logos/landing/wallet/js
/var/www/logos/landing/www
/var/www/logos/landing/www/assets
/var/www/logos/landing/www/explorer
/var/www/logos/landing/www/wallet
/var/www/logos/landing/www/wallet3
/var/www/logos/wallet
/var/www/logos/wallet3
/var/www/logos/wallet/css
/var/www/logos/wallet/js
/var/www/logos/www
/var/www/logos/www/assets
/var/www/logos/www/explorer
/var/www/logos/www/wallet
/var/www/logos/www/wallet3
```

---
## FILES (FULL SOURCE)


### FILE: /var/www/logos/app.bundle.js
```
(function(){
  // ---------- helpers ----------
  const enc = new TextEncoder();
  const $ = (q)=>document.querySelector(q);
  function toast(m){ const t=$("#toast"); if(!t) return; t.textContent=m; t.classList.add("show"); setTimeout(()=>t.classList.remove("show"),2500); }
  function be8(n){ const a=new Uint8Array(8); new DataView(a.buffer).setBigUint64(0, BigInt(n)); return a; }
  function cat(...xs){ let L=0; for(const a of xs) L+=a.length; const out=new Uint8Array(L); let o=0; for(const a of xs){ out.set(a,o); o+=a.length; } return out; }
  const B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";
  function b58(b){ let x=0n; for(const v of b) x=(x<<8n)+BigInt(v); let s=""; while(x>0n){ const r=Number(x%58n); x/=58n; s=B58[r]+s; } for(const v of b){ if(v===0) s="1"+s; else break; } return s||"1"; }
  const API="/api";
  async function apiGet(p){ const r=await fetch(API+p); if(!r.ok) throw new Error(`GET ${p} -> ${r.status}`); return r.json(); }
  async function apiPost(p,b){ const r=await fetch(API+p,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(b)}); if(!r.ok){ const t=await r.text().catch(()=> ""); throw new Error(`POST ${p} -> ${r.status} ${t}`);} return r.json(); }
  function canon(from,to,amount,nonce){ return cat(enc.encode(from),Uint8Array.of(0x7c),enc.encode(to),Uint8Array.of(0x7c),be8(amount),Uint8Array.of(0x7c),be8(nonce)); }
  function renderHistory(items){ const tb=$("#historyTable tbody"); if(!tb) return; tb.innerHTML=""; for(const it of (items||[])){ const e=it.evt||{}; const tr=document.createElement("tr"); let cp="-"; if(e.dir==="out") cp=e.to||"-"; else if(e.dir==="in") cp=e.from||"-"; else cp=e.rid||"-"; tr.innerHTML=`<td>${e.type||"transfer"}</td><td class="mono" style="max-width:260px;overflow:hidden;text-overflow:ellipsis">${cp}</td><td>${e.amount??"-"}</td><td>${e.nonce??"-"}</td><td>${e.height??"-"}</td><td class="mono" style="max-width:280px;overflow:hidden;text-overflow:ellipsis">${e.tx??"-"}</td><td><button class="ghost btnCopyTx" data-tx="${e.tx??""}">copy</button></td>`; tb.appendChild(tr);} }

  // ---------- Secure vault (PBKDF2 + AES-GCM). LocalStorage always; IndexedDB optional ----------
  const DB="logos_secure_v3", STORE="vault", REC_ID="key", LS="logos_secure_v3_backup";
  const PBKDF2_ITER=250000, SALT_LEN=16, IV_LEN=12, AUTOLOCK_MS=5*60*1000;
  let unlockedPriv=null, unlockedPubRaw=null, autolockTimer=null;

  function idbOpen(){return new Promise((res,rej)=>{const r=indexedDB.open(DB,1);r.onupgradeneeded=()=>{const db=r.result;if(!db.objectStoreNames.contains(STORE))db.createObjectStore(STORE,{keyPath:'id'});};r.onsuccess=()=>res(r.result);r.onerror=()=>rej(r.error);});}
  function idbGet(db,id){return new Promise((res,rej)=>{const tx=db.transaction(STORE,"readonly");const rq=tx.objectStore(STORE).get(id);rq.onsuccess=()=>res(rq.result);rq.onerror=()=>rej(rq.error);});}
  function idbPut(db,obj){return new Promise((res,rej)=>{const tx=db.transaction(STORE,"readwrite");tx.objectStore(STORE).put(obj);tx.oncomplete=()=>res();tx.onerror=()=>rej(tx.error);});}
  function rand(n){const a=new Uint8Array(n);crypto.getRandomValues(a);return a;}
  async function kdf(pass,salt){const base=await crypto.subtle.importKey("raw",enc.encode(pass),{name:"PBKDF2"},false,["deriveKey"]);return crypto.subtle.deriveKey({name:"PBKDF2",salt,iterations:PBKDF2_ITER,hash:"SHA-256"},base,{name:"AES-GCM",length:256},false,["encrypt","decrypt"]);}

  async function vaultStatus(){ let rec=null; try{ const db=await idbOpen(); rec=await idbGet(db,REC_ID); }catch{} if(!rec && !localStorage.getItem(LS)) return "empty"; if(unlockedPriv) return "unlocked"; return "locked"; }
  function vaultLock(){ unlockedPriv=null; unlockedPubRaw=null; clearTimeout(autolockTimer); }
  function scheduleAutolock(){ clearTimeout(autolockTimer); autolockTimer=setTimeout(()=>{ vaultLock(); $("#lockOverlay")?.classList.remove("hidden"); }, AUTOLOCK_MS); }

  async function vaultCreateWithPass(pass){
    try{
      // генерим пару в WebCrypto (Ed25519). Большинство новых браузеров поддерживают; иначе покажем ошибку.
      const kp = await crypto.subtle.generateKey({name:"Ed25519"}, true, ["sign","verify"]);
      const pkcs8 = new Uint8Array(await crypto.subtle.exportKey("pkcs8", kp.privateKey));
      const pubRaw= new Uint8Array(await crypto.subtle.exportKey("raw",   kp.publicKey));
      const salt=rand(SALT_LEN), iv=rand(IV_LEN), key=await kdf(pass,salt);
      const ct  = new Uint8Array(await crypto.subtle.encrypt({name:"AES-GCM",iv}, key, pkcs8));

      // резерв в LS — ВСЕГДА
      localStorage.setItem(LS, JSON.stringify({
        salt:btoa(String.fromCharCode(...salt)),
        iv:  btoa(String.fromCharCode(...iv)),
        ct:  btoa(String.fromCharCode(...ct)),
        pubRaw:btoa(String.fromCharCode(...pubRaw)),
        iter:PBKDF2_ITER
      }));
      // попытка IDB — не критично
      try{ const db=await idbOpen(); await idbPut(db,{id:REC_ID, salt, iv, ct, pubRaw, iter:PBKDF2_ITER}); }catch{}

      unlockedPriv = kp.privateKey; unlockedPubRaw = pubRaw; scheduleAutolock();
      return true;
    }catch(e){
      console.error("vaultCreate error", e);
      toast("Ошибка создания ключа. Обнови браузер или установи современный.");
      return false;
    }
  }

  async function vaultUnlock(pass){
    let rec=null; try{ const db=await idbOpen(); rec=await idbGet(db,REC_ID); }catch{}
    if(!rec){ const raw=localStorage.getItem(LS); if(!raw) throw new Error("NoKey"); const o=JSON.parse(raw); rec={salt:Uint8Array.from(atob(o.salt),c=>c.charCodeAt(0)),iv:Uint8Array.from(atob(o.iv),c=>c.charCodeAt(0)),ct:Uint8Array.from(atob(o.ct),c=>c.charCodeAt(0)),pubRaw:Uint8Array.from(atob(o.pubRaw),c=>c.charCodeAt(0)),iter:o.iter}; }
    const key=await kdf(pass,new Uint8Array(rec.salt));
    const pkcs8=await crypto.subtle.decrypt({name:"AES-GCM",iv:new Uint8Array(rec.iv)},key,new Uint8Array(rec.ct)).catch(()=>null);
    if(!pkcs8) throw new Error("BadPassword");
    unlockedPriv=await crypto.subtle.importKey("pkcs8",pkcs8,{name:"Ed25519"},false,["sign"]);
    unlockedPubRaw=new Uint8Array(rec.pubRaw); scheduleAutolock(); return true;
  }

  async function vaultExportPkcs8Base64(){
    if(!unlockedPriv) throw new Error("Locked");
    const pkcs8=new Uint8Array(await crypto.subtle.exportKey("pkcs8",unlockedPriv));
    return btoa(String.fromCharCode(...pkcs8));
  }

  async function vaultImportPkcs8Base64(b64, pass){
    const pkcs8 = Uint8Array.from(atob(b64), c=>c.charCodeAt(0));
    // сгенерим временную pubRaw
    const tmp   = await crypto.subtle.generateKey({name:"Ed25519"},true,["sign","verify"]);
    const pubRaw= new Uint8Array(await crypto.subtle.exportKey("raw", tmp.publicKey));
    const salt=rand(SALT_LEN), iv=rand(IV_LEN), key=await kdf(pass,salt);
    const ct  = new Uint8Array(await crypto.subtle.encrypt({name:"AES-GCM",iv},key,pkcs8));
    localStorage.setItem(LS, JSON.stringify({salt:btoa(String.fromCharCode(...salt)),iv:btoa(String.fromCharCode(...iv)),ct:btoa(String.fromCharCode(...ct)),pubRaw:btoa(String.fromCharCode(...pubRaw)),iter:PBKDF2_ITER}));
    try{ const db=await idbOpen(); await idbPut(db,{id:REC_ID,salt,iv,ct,pubRaw,iter:PBKDF2_ITER}); }catch{}
    unlockedPriv=await crypto.subtle.importKey("pkcs8",pkcs8,{name:"Ed25519"},false,["sign"]);
    unlockedPubRaw=pubRaw; scheduleAutolock(); return true;
  }

  async function vaultReset(){ try{indexedDB.deleteDatabase(DB);}catch{} try{localStorage.removeItem(LS);}catch{} vaultLock(); }

  function currentRid(){ return unlockedPubRaw ? b58(unlockedPubRaw) : ""; }

  async function signEd25519(msg){ if(!unlockedPriv) throw new Error("Locked"); const sig=new Uint8Array(await crypto.subtle.sign({name:"Ed25519"},unlockedPriv,msg)); let bin=""; for(let i=0;i<sig.length;i++) bin+=String.fromCharCode(sig[i]); return btoa(bin); }

  // ---------- Wallet logic ----------
  async function resolveRID(){ const rid=($("#ridInput")?.value||"").trim(); return rid || currentRid(); }

  async function loadPassport(){
    const rid=await resolveRID();
    const [p,s,h]=await Promise.allSettled([apiGet(`/profile/${rid}`),apiGet(`/stake/summary/${rid}`),apiGet(`/history/${rid}?limit=10`)]);
    const prof=p.status==="fulfilled"?p.value:{}; const sum=s.status==="fulfilled"?s.value:{}; const items=h.status==="fulfilled"?(h.value.items||[]):[];
    $("#passportRid").textContent=rid||"—";
    $("#passportBal").textContent=prof.balance??"—";
    $("#passportNonce").textContent=(prof.nonce&&prof.nonce.next)??"—";
    $("#passportHead").textContent=prof.head??"—";
    $("#passportDelegated").textContent=sum.delegated??"—";
    $("#passportEntries").textContent=sum.entries??"—";
    $("#passportClaimable").textContent=sum.claimable??"—";
    renderHistory(items);
  }

  async function refreshStake(){
    const rid=await resolveRID(); if(!rid) return;
    try{ const s=await apiGet(`/stake/summary/${rid}`); $("#chipDelegated").textContent=String(s.delegated??0); $("#chipEntries").textContent=String(s.entries??0); $("#chipClaimable").textContent=String(s.claimable??0); }catch{}
  }

  async function syncProfile(){
    const rid=await resolveRID(); if(!rid){ $("#balanceBadge").textContent="—"; $("#nonceBadge").textContent="—"; return; }
    const prof=await apiGet(`/profile/${rid}`);
    $("#balanceBadge").textContent=prof.balance??"—";
    $("#nonceBadge").textContent=(prof.nonce&&prof.nonce.next)??"—";
    await refreshStake(); await loadPassport();
  }

  async function showHistory(){ const rid=await resolveRID(); if(!rid) return; const h=await apiGet(`/history/${rid}?limit=50`); renderHistory(h.items||[]); }

  async function onSend(){
    const from=currentRid(), to=($("#toRid")?.value||"").trim(), amount=Number($("#sendAmount")?.value||0);
    if(!from){ toast("Кошелёк заблокирован"); $("#lockOverlay").classList.remove("hidden"); return; }
    if(!to||!amount){ toast("Укажи получателя и сумму"); return; }
    const nn=await apiGet(`/nonce/${from}`); const nonce=nn.next;
    const sigB64=await signEd25519( canon(from,to,amount,nonce) );
    const res=await apiPost(`/submit_tx`,{from,to,amount,nonce,sig:sigB64});
    toast(res?.status==="queued"?"Транзакция отправлена":"Отправка выполнена");
    await syncProfile(); await showHistory(); await loadPassport();
  }

  // ---------- Secure overlay handlers ----------
  let tries=5;
  async function updateLockView(){
    $("#rpHost").textContent = location.host;
    const st = await vaultStatus();
    if(st==="empty"){ $("#lockStepSetup").classList.remove("hidden"); $("#lockStepUnlock").classList.add("hidden"); }
    if(st==="locked"){ $("#lockStepSetup").classList.add("hidden"); $("#lockStepUnlock").classList.remove("hidden"); }
    if(st==="unlocked"){ $("#lockOverlay").classList.add("hidden"); await afterUnlock(); }
  }
  async function afterUnlock(){
    const rid=currentRid(); if(rid){ $("#ridInput").value=rid; $("#ridValidator").value=rid; $("#passportRid").textContent=rid; }
    await syncProfile(); await loadPassport();
  }
  async function handleCreate(){
    const p1=$("#pwNew").value.trim(), p2=$("#pwNew2").value.trim();
    if(p1.length<8){ toast("Пароль минимум 8 символов"); return; }
    if(p1!==p2){ toast("Пароли не совпадают"); return; }
    toast("Создаём и шифруем ключ…");
    const ok=await vaultCreateWithPass(p1);
    if(!ok){ toast("Не удалось создать ключ"); return; }
    $("#lockOverlay").classList.add("hidden"); tries=5; await afterUnlock();
  }
  async function handleUnlock(){
    const p=$("#pwUnlock").value.trim();
    try{ await vaultUnlock(p); $("#lockOverlay").classList.add("hidden"); tries=5; await afterUnlock(); }
    catch(e){ tries--; $("#triesLeft2").textContent=String(tries); toast(tries>0?"Неверный пароль":"Слишком много попыток — кошелёк сброшен"); if(tries<=0){ await (async()=>{try{indexedDB.deleteDatabase(DB);}catch{} try{localStorage.removeItem(LS);}catch{}})(); location.reload(); } }
  }
  async function handleForgot(){ if(confirm("Очистить локальный ключ и настройки?")){ try{indexedDB.deleteDatabase(DB);}catch{} try{localStorage.removeItem(LS);}catch{} location.reload(); } }
  async function handleImportSetup(){
    const b64=prompt("Вставь PKCS8 Base64 ключ"); if(!b64) return;
    const pass=prompt("Создай пароль шифрования (≥8)"); if(!pass||pass.length<8){ toast("Пароль ≥ 8"); return; }
    const ok=await vaultImportPkcs8Base64(b64, pass);
    if(!ok){ toast("Импорт не удался"); return; }
    $("#lockOverlay").classList.add("hidden"); tries=5; await afterUnlock();
  }
  async function handleImportUnlock(){
    const b64=prompt("Вставь PKCS8 Base64 ключ"); if(!b64) return;
    const pass=prompt("Пароль шифрования (≥8)"); if(!pass||pass.length<8){ toast("Пароль ≥ 8"); return; }
    const ok=await vaultImportPkcs8Base64(b64, pass);
    if(!ok){ toast("Импорт не удался"); return; }
    $("#lockOverlay").classList.add("hidden"); tries=5; await afterUnlock();
  }

  // ---------- bindings ----------
  document.addEventListener("click",e=>{ const b=e.target.closest(".btnCopyTx"); if(b){ navigator.clipboard.writeText(b.dataset.tx||"").then(()=>toast("Скопировано")).catch(()=>toast("Не удалось скопировать")); } });

  document.addEventListener("DOMContentLoaded", ()=>{
    // secure
    $("#rpHost").textContent = location.host;
    $("#btnCreate").addEventListener("click", handleCreate);
    $("#btnUnlock").addEventListener("click", handleUnlock);
    $("#btnForgot").addEventListener("click", handleForgot);
    $("#btnImportSetup").addEventListener("click", handleImportSetup);
    $("#btnImportUnlock").addEventListener("click", handleImportUnlock);

    // wallet
    $("#btnBalance").addEventListener("click", ()=>syncProfile().catch(e=>toast(String(e))));
    $("#btnSync").addEventListener("click", ()=>syncProfile().catch(e=>toast(String(e))));
    $("#btnShowHist").addEventListener("click", ()=>showHistory().catch(e=>toast(String(e))));
    $("#btnStakeDelegate").addEventListener("click", async ()=>{ const rid=(await resolveRID()); const amount=Number($("#stakeAmount").value||0); const r=await apiPost(`/stake/delegate`,{validator:rid,amount}); toast(r.ok?"Delegated":"Delegate failed"); await refreshStake(); await loadPassport(); });
    $("#btnStakeUndelegate").addEventListener("click", async ()=>{ const rid=(await resolveRID()); const amount=Number($("#unstakeAmount").value||0); const r=await apiPost(`/stake/undelegate`,{validator:rid,amount}); toast(r.ok?"Undelegated":"Undelegate failed"); await refreshStake(); await loadPassport(); });
    $("#btnStakeClaim").addEventListener("click", async ()=>{ const rid=(await resolveRID()); const r=await apiPost(`/stake/claim`,{rid}); toast(r.ok?`Claimed ${r.claimed}`:"Claim failed"); await refreshStake(); await loadPassport(); });
    $("#btnSend").addEventListener("click", ()=>onSend().catch(e=>toast(String(e))));
    $("#btnCopyRid").addEventListener("click", ()=>{ const rid=$("#passportRid").textContent||$("#ridInput").value||""; navigator.clipboard.writeText(rid).then(()=>toast("RID скопирован")); });

    updateLockView().catch(()=>toast("Ошибка инициализации"));
  });
})();

```

### FILE: /var/www/logos/css/styles.css
```
:root{color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:#0b1016;color:#e7eef7;font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
.wrap{max-width:980px;margin:24px auto;padding:0 16px}
h1{font-size:22px;margin:0 0 16px}
.section{background:#111827;border:1px solid #1a2436;border-radius:14px;padding:16px;margin:14px 0}
.grid{display:grid;gap:12px}
.cols-3{grid-template-columns:repeat(3,1fr)}
.cols-2{grid-template-columns:repeat(2,1fr)}
.mt10{margin-top:10px}
.row{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.space-between{justify-content:space-between}
.gap8{gap:8px}
.break{word-break:break-all}
input,button,textarea{border-radius:10px;border:1px solid #28344c;background:#0d1420;color:#e7eef7;padding:10px 12px;width:100%}
textarea{min-height:90px;resize:vertical}
input:focus,textarea:focus{outline:none;border-color:#3a70ff;box-shadow:0 0 0 2px #3a70ff26}
button{background:#3366ff;border:none;cursor:pointer}
button.secondary{background:#1a2333}
button.ghost{background:#0d1420;border:1px dashed #2a3a56}
label{display:block;margin:6px 0 6px;color:#98aec6;font-size:13px}
.badge{background:#141e2d;border:1px solid #2a3a56;border-radius:999px;padding:6px 10px;font-size:12px}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
.table{width:100%;border-collapse:collapse}
.table th,.table td{border-bottom:1px solid #1a2436;padding:10px 8px;text-align:left;font-size:13px}
.scroll{overflow:auto}
.toast{position:fixed;right:16px;bottom:16px;display:none;background:#0e1520;border:1px solid #20406f;color:#bfe0ff;padding:12px 14px;border-radius:10px;box-shadow:0 10px 30px rgba(0,0,0,.35);max-width:80%}
.toast.show{display:block}

/* Secure overlay */
#lockOverlay{position:fixed;inset:0;background:#0b1016;display:flex;align-items:center;justify-content:center;z-index:9999}
#lockCard{width:min(560px,92%);background:#0f1723;border:1px solid #243048;border-radius:16px;padding:18px}
#brand{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
#phish{background:#0c1420;border:1px solid #2a3a56;border-radius:10px;padding:10px;font-size:12px;color:#9fb2c9}
#lockActions{display:flex;gap:8px;margin-top:10px}
#lockMeta{display:flex;gap:8px;margin-top:8px;flex-wrap:wrap}
#lockMeta .badge{font-size:11px}
.hidden{display:none}
.muted{color:#9fb2c9}

```

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

### FILE: /var/www/logos/js/api.js
```
export const API_BASE="/api";
export async function apiGet(p){ const r=await fetch(`${API_BASE}${p}`); if(!r.ok) throw new Error(`GET ${p} -> ${r.status}`); return r.json(); }
export async function apiPost(p,b){ const r=await fetch(`${API_BASE}${p}`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)}); if(!r.ok){ const t=await r.text().catch(()=> ""); throw new Error(`POST ${p} -> ${r.status} ${t}`); } return r.json(); }

```

### FILE: /var/www/logos/js/boot_hard.js
```
// LOGOS Wallet hard bootstrap: гарантированная работа кнопок Create/Unlock даже если модули/inline не исполняются.
(function(){
  const enc = new TextEncoder();
  const LS  = "logos_secure_v3_backup";
  const ITER= 250000;

  const $ = (id)=>document.getElementById(id);
  function toast(msg){
    const t = document.getElementById('toast'); if(!t) return;
    t.textContent = msg; t.classList.add('show');
    setTimeout(()=>t.classList.remove('show'), 2500);
  }
  function rand(n){ const a=new Uint8Array(n); crypto.getRandomValues(a); return a; }
  async function kdf(pass, salt){
    const base = await crypto.subtle.importKey("raw", new TextEncoder().encode(pass), {name:"PBKDF2"}, false, ["deriveKey"]);
    return crypto.subtle.deriveKey({name:"PBKDF2", salt, iterations:ITER, hash:"SHA-256"}, base, {name:"AES-GCM", length:256}, false, ["encrypt","decrypt"]);
  }
  function saveLS(salt, iv, ct, pubRaw){
    localStorage.setItem(LS, JSON.stringify({
      salt:  btoa(String.fromCharCode(...salt)),
      iv:    btoa(String.fromCharCode(...iv)),
      ct:    btoa(String.fromCharCode(...ct)),
      pubRaw:btoa(String.fromCharCode(...pubRaw)),
      iter:  ITER
    }));
  }
  async function unlockFromLS(pass){
    const raw = localStorage.getItem(LS); if(!raw) throw new Error("NoKey");
    const o   = JSON.parse(raw);
    const salt= Uint8Array.from(atob(o.salt),  c=>c.charCodeAt(0));
    const iv  = Uint8Array.from(atob(o.iv),    c=>c.charCodeAt(0));
    const ct  = Uint8Array.from(atob(o.ct),    c=>c.charCodeAt(0));
    const key = await kdf(pass, salt);
    const pk8 = await crypto.subtle.decrypt({name:"AES-GCM", iv}, key, ct);
    // валидность
    await crypto.subtle.importKey("pkcs8", pk8, {name:"Ed25519"}, false, ["sign"]);
    return true;
  }
  async function createWallet(pass){
    const kp     = await crypto.subtle.generateKey({name:"Ed25519"}, true, ["sign","verify"]);
    const pkcs8  = new Uint8Array(await crypto.subtle.exportKey("pkcs8", kp.privateKey));
    const pubRaw = new Uint8Array(await crypto.subtle.exportKey("raw",   kp.publicKey));
    const salt   = rand(16), iv = rand(12), key = await kdf(pass, salt);
    const ct     = new Uint8Array(await crypto.subtle.encrypt({name:"AES-GCM", iv}, key, pkcs8));
    saveLS(salt, iv, ct, pubRaw);
    return true;
  }

  function bind(id, fn){
    const el = $(id); if(!el) return;
    // снимаем возможный старый обработчик и навешиваем новый
    el.onclick = null; el.addEventListener('click', fn, {passive:true});
  }

  function domainBadge(){ const rp = $('rpHost'); if(rp) rp.textContent = location.host; }

  // Привязки
  function attach(){
    domainBadge();

    bind('btnCreate', async ()=>{
      try{
        const p1 = ($('pwNew')?.value || '').trim();
        const p2 = ($('pwNew2')?.value || '').trim();
        if (p1.length < 8){ toast('Пароль минимум 8 символов'); return; }
        if (p1 !== p2){     toast('Пароли не совпадают');      return; }
        toast('Создаём ключ…');
        await createWallet(p1);
        $('lockOverlay')?.classList.add('hidden');
        location.reload();
      }catch(e){ console.error(e); toast('Ошибка создания. Обнови браузер.'); }
    });

    let tries = 5;
    bind('btnUnlock', async ()=>{
      try{
        const p = ($('pwUnlock')?.value || '').trim();
        if (p.length < 8){ toast('Пароль минимум 8 символов'); return; }
        await unlockFromLS(p);
        $('lockOverlay')?.classList.add('hidden');
        location.reload();
      }catch(e){
        tries = Math.max(0, tries - 1);
        if ($('triesLeft2')) $('triesLeft2').textContent = String(tries);
        toast(tries>0 ? 'Неверный пароль' : 'Слишком много попыток — сброс');
        if (tries <= 0){ try{ localStorage.removeItem(LS); }catch{} location.reload(); }
      }
    });

    bind('btnForgot', ()=>{
      if (confirm('Очистить локальный ключ и настройки?')){
        try{ localStorage.removeItem(LS); }catch{}
        location.reload();
      }
    });

    const importFlow = async ()=>{
      const b64  = prompt('Вставь PKCS8 Base64 ключ'); if(!b64) return;
      const pass = prompt('Пароль шифрования (≥8)');   if(!pass || pass.length<8){ toast('Пароль ≥ 8'); return; }
      try{
        const pk = Uint8Array.from(atob(b64), c=>c.charCodeAt(0));
        const tmp= await crypto.subtle.generateKey({name:"Ed25519"}, true, ["sign","verify"]);
        const pub= new Uint8Array(await crypto.subtle.exportKey("raw", tmp.publicKey));
        const s  = rand(16), i=rand(12), k=await kdf(pass, s);
        const ct = new Uint8Array(await crypto.subtle.encrypt({name:"AES-GCM", iv:i}, k, pk));
        saveLS(s, i, ct, pub);
        $('lockOverlay')?.classList.add('hidden'); location.reload();
      }catch(e){ console.error(e); toast('Импорт не удался'); }
    };
    bind('btnImportSetup', importFlow);
    bind('btnImportUnlock', importFlow);
  }

  // Попытка привязать сразу и ещё раз после DOMContentLoaded (на случай очень ранней загрузки)
  try{ attach(); }catch{}
  document.addEventListener('DOMContentLoaded', attach, {once:true});
})();

```

### FILE: /var/www/logos/js/boot.js
```
// Аварийный бутстрап: всегда работает, даже если модуль не загрузился
(function(){
  const enc=new TextEncoder(); const LS="logos_secure_v3_backup"; const ITER=250000;
  const $=q=>document.querySelector(q); function toast(m){const t=$("#toast"); if(!t) return; t.textContent=m; t.classList.add("show"); setTimeout(()=>t.classList.remove("show"),2500);}
  function rand(n){const a=new Uint8Array(n); crypto.getRandomValues(a); return a;}
  async function kdf(pass,salt){const base=await crypto.subtle.importKey("raw",enc.encode(pass),{name:"PBKDF2"},false,["deriveKey"]);return crypto.subtle.deriveKey({name:"PBKDF2",salt,iterations:ITER,hash:"SHA-256"},base,{name:"AES-GCM",length:256},false,["encrypt","decrypt"]);}

  function saveLS(salt,iv,ct,pubRaw){ localStorage.setItem(LS, JSON.stringify({
    salt:btoa(String.fromCharCode(...salt)), iv:btoa(String.fromCharCode(...iv)),
    ct:btoa(String.fromCharCode(...ct)), pubRaw:btoa(String.fromCharCode(...pubRaw)), iter:ITER })); }

  async function unlockFromLS(pass){
    const raw=localStorage.getItem(LS); if(!raw) throw new Error("NoKey");
    const o=JSON.parse(raw);
    const salt=Uint8Array.from(atob(o.salt),c=>c.charCodeAt(0));
    const iv  =Uint8Array.from(atob(o.iv),  c=>c.charCodeAt(0));
    const ct  =Uint8Array.from(atob(o.ct),  c=>c.charCodeAt(0));
    const key =await kdf(pass,salt);
    const pkcs8=await crypto.subtle.decrypt({name:"AES-GCM",iv},key,ct); // проверка дешифрования
    await crypto.subtle.importKey("pkcs8",pkcs8,{name:"Ed25519"},false,["sign"]);
    return true;
  }

  function bindOnce(id, fn){ const el=document.getElementById(id); if(!el||el.__bound) return; el.addEventListener('click', fn, {passive:true}); el.__bound=true; }

  // Создание
  bindOnce('btnCreate', async ()=>{
    try{
      const p1=($("#pwNew")?.value||"").trim(), p2=($("#pwNew2")?.value||"").trim();
      if(p1.length<8){ toast("Пароль минимум 8 символов"); return; }
      if(p1!==p2){ toast("Пароли не совпадают"); return; }
      toast("Создаём и шифруем ключ…");
      const kp=await crypto.subtle.generateKey({name:"Ed25519"},true,["sign","verify"]);
      const pkcs8=new Uint8Array(await crypto.subtle.exportKey("pkcs8",kp.privateKey));
      const pubRaw=new Uint8Array(await crypto.subtle.exportKey("raw",kp.publicKey));
      const salt=rand(16), iv=rand(12), key=await kdf(p1,salt);
      const ct=new Uint8Array(await crypto.subtle.encrypt({name:"AES-GCM",iv},key,pkcs8));
      saveLS(salt,iv,ct,pubRaw);
      $("#lockOverlay")?.classList.add("hidden"); location.reload();
    }catch(e){ console.error(e); toast("Ошибка создания ключа. Обнови браузер."); }
  });

  // Разблокировка
  let tries=5;
  bindOnce('btnUnlock', async ()=>{
    try{
      const p=($("#pwUnlock")?.value||"").trim();
      if(p.length<8){ toast("Пароль минимум 8 символов"); return; }
      await unlockFromLS(p);
      $("#lockOverlay")?.classList.add("hidden"); location.reload();
    }catch(e){
      tries--; $("#triesLeft2") && ($("#triesLeft2").textContent=String(tries));
      toast(tries>0 ? "Неверный пароль" : "Слишком много попыток — сброс");
      if(tries<=0){ try{ localStorage.removeItem(LS); }catch{} location.reload(); }
    }
  });

  // Импорт (setup/unlock)
  function importFlow(field){
    const b64=prompt("Вставь PKCS8 Base64 ключ"); if(!b64) return;
    const pass=prompt("Пароль шифрования (≥8)"); if(!pass||pass.length<8){ toast("Пароль ≥ 8"); return; }
    (async ()=>{
      try{
        const pkcs8=Uint8Array.from(atob(b64),c=>c.charCodeAt(0));
        const tmp=await crypto.subtle.generateKey({name:"Ed25519"},true,["sign","verify"]);
        const pubRaw=new Uint8Array(await crypto.subtle.exportKey("raw",tmp.publicKey));
        const salt=rand(16), iv=rand(12), key=await kdf(pass,salt);
        const ct=new Uint8Array(await crypto.subtle.encrypt({name:"AES-GCM",iv},key,pkcs8));
        saveLS(salt,iv,ct,pubRaw);
        $("#lockOverlay")?.classList.add("hidden"); location.reload();
      }catch(e){ toast("Импорт не удался"); }
    })();
  }
  bindOnce('btnImportSetup', ()=>importFlow('setup'));
  bindOnce('btnImportUnlock', ()=>importFlow('unlock'));

  // Сброс
  bindOnce('btnForgot', ()=>{
    if(confirm("Очистить локальный ключ и настройки?")){ try{localStorage.removeItem(LS);}catch{} location.reload(); }
  });

  document.addEventListener('DOMContentLoaded', ()=>{ const rp=document.getElementById('rpHost'); if(rp) rp.textContent=location.host; });
})();

```

### FILE: /var/www/logos/js/ping.js
```
(function(){
  try{
    var el = document.getElementById('rpHost');
    if (el) el.textContent = (el.textContent ? el.textContent + ' ' : '') + 'JS✓';
  }catch(e){}
})();

```

### FILE: /var/www/logos/js/ui.js
```
export const $ = q => document.querySelector(q);
export function toast(msg){ const t=$("#toast"); if(!t) return; t.textContent=msg; t.classList.add("show"); setTimeout(()=>t.classList.remove("show"),2500); }
export async function copy(txt){ try{ await navigator.clipboard.writeText(txt); toast("Скопировано"); } catch { toast("Не удалось скопировать"); } }
export const enc = new TextEncoder();
export function be8(n){ const a=new Uint8Array(8); new DataView(a.buffer).setBigUint64(0, BigInt(n)); return a; }
export function cat(...xs){ let L=0; for(const a of xs) L+=a.length; const out=new Uint8Array(L); let o=0; for(const a of xs){ out.set(a,o); o+=a.length; } return out; }
const B58="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";
export function b58(b){ let x=0n; for(const v of b) x=(x<<8n)+BigInt(v); let s=""; while(x>0n){ const r=Number(x%58n); x/=58n; s=B58[r]+s; } for(const v of b){ if(v===0)s="1"+s; else break; } return s||"1"; }
export function canon(from,to,amount,nonce){ return cat(enc.encode(from),Uint8Array.of(0x7c),enc.encode(to),Uint8Array.of(0x7c),be8(amount),Uint8Array.of(0x7c),be8(nonce)); }
export function renderHistory(items){ const tb=$("#historyTable tbody"); if(!tb) return; tb.innerHTML=""; for(const it of (items||[])){ const e=it.evt||{}; const tr=document.createElement("tr"); let cp="-"; if(e.dir==="out") cp=e.to||"-"; else if(e.dir==="in") cp=e.from||"-"; else cp=e.rid||"-"; tr.innerHTML=`<td>${e.type||"transfer"}</td><td class="mono" style="max-width:260px;overflow:hidden;text-overflow:ellipsis">${cp}</td><td>${e.amount??"-"}</td><td>${e.nonce??"-"}</td><td>${e.height??"-"}</td><td class="mono" style="max-width:280px;overflow:hidden;text-overflow:ellipsis">${e.tx??"-"}</td><td><button class="ghost btnCopyTx" data-tx="${e.tx??""}">copy</button></td>`; tb.appendChild(tr); } }

```

### FILE: /var/www/logos/js/vault.js
```
import { enc } from "./ui.js";

const DB="logos_secure_v3", STORE="vault", REC_ID="key", LS="logos_secure_v3_backup";
const PBKDF2_ITER=250000, SALT_LEN=16, IV_LEN=12, AUTOLOCK_MS=5*60*1000;
let unlockedPriv=null, unlockedPubRaw=null, autolockTimer=null;

function idbOpen(){return new Promise((res,rej)=>{const r=indexedDB.open(DB,1);r.onupgradeneeded=()=>{const db=r.result;if(!db.objectStoreNames.contains(STORE))db.createObjectStore(STORE,{keyPath:'id'});};r.onsuccess=()=>res(r.result);r.onerror=()=>rej(r.error);});}
function idbGet(db,id){return new Promise((res,rej)=>{const tx=db.transaction(STORE,"readonly");const rq=tx.objectStore(STORE).get(id);rq.onsuccess=()=>res(rq.result);rq.onerror=()=>rej(rq.error);});}
function idbPut(db,obj){return new Promise((res,rej)=>{const tx=db.transaction(STORE,"readwrite");tx.objectStore(STORE).put(obj);tx.oncomplete=()=>res();tx.onerror=()=>rej(tx.error);});}
function rand(n){const a=new Uint8Array(n);crypto.getRandomValues(a);return a;}
async function kdf(pass,salt){const base=await crypto.subtle.importKey("raw",enc.encode(pass),{name:"PBKDF2"},false,["deriveKey"]);return crypto.subtle.deriveKey({name:"PBKDF2",salt,iterations:PBKDF2_ITER,hash:"SHA-256"},base,{name:"AES-GCM",length:256},false,["encrypt","decrypt"]);}

export async function vaultStatus(){ let rec=null; try{ const db=await idbOpen(); rec=await idbGet(db,REC_ID); }catch{} if(!rec && !localStorage.getItem(LS)) return "empty"; if(unlockedPriv) return "unlocked"; return "locked"; }
export function vaultLock(){ unlockedPriv=null; unlockedPubRaw=null; clearTimeout(autolockTimer); }
function scheduleAutolock(){ clearTimeout(autolockTimer); autolockTimer=setTimeout(()=>{vaultLock(); document.getElementById("lockOverlay")?.classList.remove("hidden");}, AUTOLOCK_MS); }

export async function vaultCreateWithPass(pass){
  const kp=await crypto.subtle.generateKey({name:"Ed25519"},true,["sign","verify"]);
  const pkcs8=new Uint8Array(await crypto.subtle.exportKey("pkcs8",kp.privateKey));
  const pubRaw=new Uint8Array(await crypto.subtle.exportKey("raw",kp.publicKey));
  const salt=rand(SALT_LEN), iv=rand(IV_LEN); const key=await kdf(pass,salt);
  const ct=new Uint8Array(await crypto.subtle.encrypt({name:"AES-GCM",iv},key,pkcs8));
  // LS резерв (всегда)
  localStorage.setItem(LS, JSON.stringify({salt:btoa(String.fromCharCode(...salt)),iv:btoa(String.fromCharCode(...iv)),ct:btoa(String.fromCharCode(...ct)),pubRaw:btoa(String.fromCharCode(...pubRaw)),iter:PBKDF2_ITER}));
  // IDB — по возможности
  try{ const db=await idbOpen(); await idbPut(db,{id:REC_ID,salt,iv,ct,pubRaw,iter:PBKDF2_ITER}); }catch{}
  unlockedPriv=kp.privateKey; unlockedPubRaw=pubRaw; scheduleAutolock(); return true;
}
export async function vaultUnlock(pass){
  let rec=null; try{ const db=await idbOpen(); rec=await idbGet(db,REC_ID); }catch{}
  if(!rec){ const raw=localStorage.getItem(LS); if(!raw) throw new Error("NoKey"); const o=JSON.parse(raw); rec={salt:Uint8Array.from(atob(o.salt),c=>c.charCodeAt(0)),iv:Uint8Array.from(atob(o.iv),c=>c.charCodeAt(0)),ct:Uint8Array.from(atob(o.ct),c=>c.charCodeAt(0)),pubRaw:Uint8Array.from(atob(o.pubRaw),c=>c.charCodeAt(0)),iter:o.iter}; }
  const key=await kdf(pass,new Uint8Array(rec.salt)); const pkcs8=await crypto.subtle.decrypt({name:"AES-GCM",iv:new Uint8Array(rec.iv)},key,new Uint8Array(rec.ct)).catch(()=>null);
  if(!pkcs8) throw new Error("BadPassword");
  unlockedPriv=await crypto.subtle.importKey("pkcs8",pkcs8,{name:"Ed25519"},false,["sign"]); unlockedPubRaw=new Uint8Array(rec.pubRaw); scheduleAutolock(); return true;
}
export async function vaultExportPkcs8Base64(){ if(!unlockedPriv) throw new Error("Locked"); const pkcs8=new Uint8Array(await crypto.subtle.exportKey("pkcs8",unlockedPriv)); return btoa(String.fromCharCode(...pkcs8)); }
export async function vaultImportPkcs8Base64(b64,pass){
  const pkcs8=Uint8Array.from(atob(b64),c=>c.charCodeAt(0)); const tmp=await crypto.subtle.generateKey({name:"Ed25519"},true,["sign","verify"]); const pubRaw=new Uint8Array(await crypto.subtle.exportKey("raw",tmp.publicKey));
  const salt=rand(SALT_LEN), iv=rand(IV_LEN); const key=await kdf(pass,salt); const ct=new Uint8Array(await crypto.subtle.encrypt({name:"AES-GCM",iv},key,pkcs8));
  localStorage.setItem(LS, JSON.stringify({salt:btoa(String.fromCharCode(...salt)),iv:btoa(String.fromCharCode(...iv)),ct:btoa(String.fromCharCode(...ct)),pubRaw:btoa(String.fromCharCode(...pubRaw)),iter:PBKDF2_ITER}));
  try{ const db=await idbOpen(); await idbPut(db,{id:REC_ID,salt,iv,ct,pubRaw,iter:PBKDF2_ITER}); }catch{}
  unlockedPriv=await crypto.subtle.importKey("pkcs8",pkcs8,{name:"Ed25519"},false,["sign"]); unlockedPubRaw=pubRaw; scheduleAutolock(); return true;
}
export async function vaultReset(){ try{indexedDB.deleteDatabase(DB);}catch{} try{localStorage.removeItem(LS);}catch{} vaultLock(); }
export function currentRid(){ if(!unlockedPubRaw) return ""; return b58(unlockedPubRaw); }
export async function signEd25519(bytes){ if(!unlockedPriv) throw new Error("Locked"); const sig=new Uint8Array(await crypto.subtle.sign({name:"Ed25519"},unlockedPriv,bytes)); let bin=""; for(let i=0;i<sig.length;i++) bin+=String.fromCharCode(sig[i]); return btoa(bin); }
function b58(b){ let x=0n; for(const v of b) x=(x<<8n)+BigInt(v); const A="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"; let s=""; while(x>0n){const r=Number(x%58n);x/=58n;s=A[r]+s;} for(const v of b){ if(v===0)s="1"+s; else break; } return s||"1"; }

```

### FILE: /var/www/logos/landing/airdrop.html
```
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta http-equiv="Cache-Control" content="no-store"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Airdrop</title>

  <link rel="stylesheet" href="/shared/wallet-theme.css?v=20251214_01"/>
  <link rel="stylesheet" href="/shared/airdrop.css?v=20251214_01"/>

  <script src="/shared/airdrop.js?v=20251214_01" defer></script>
</head>
<body class="logos-ui">
  <header class="topbar">
    <div class="topbar__inner">
      <div class="brand">
        <div class="brand__mark"><span>LRB</span></div>
        <div class="brand__text">
          <div class="brand__title">LOGOS Airdrop</div>
          <div class="brand__sub">Dashboard · Wallet bind · Social verify</div>
        </div>
      </div>
      <div class="topbar__right">
        <div class="pill">API: <span class="mono">/airdrop-api</span></div>
      </div>
    </div>
  </header>

  <main class="container">
    <div class="stack">

      <section class="card hero">
        <div class="heroGrid">
          <div>
            <h1 class="heroTitle">Airdrop Dashboard</h1>
            <p class="muted heroSub">Выполняй задания → копи поинты → приглашай друзей.</p>
          </div>

          <div class="stats">
            <div class="stat">
              <div class="stat__k muted">Points</div>
              <div class="stat__v" id="s_points">—</div>
            </div>
            <div class="stat">
              <div class="stat__k muted">Rank</div>
              <div class="stat__v" id="s_rank">—</div>
            </div>
            <div class="stat">
              <div class="stat__k muted">Refs</div>
              <div class="stat__v" id="s_refs">—</div>
            </div>
          </div>
        </div>
      </section>

      <div class="grid-2">
        <section class="card">
          <header class="card__head">
            <h2>Токен</h2>
            <p class="muted">Скопируй token и реф‑ссылку (они же используются ботами/верификаторами).</p>
          </header>

          <div class="card__body stack">
            <div class="row2">
              <input id="inpToken" class="mono monoInput" readonly placeholder="token..." />
              <button id="btnCopyToken" class="secondary" type="button">Copy token</button>
            </div>

            <div class="row2">
              <input id="inpRef" class="mono monoInput" readonly placeholder="ref link..." />
              <button id="btnCopyRef" class="secondary" type="button">Copy link</button>
            </div>
          </div>
        </section>

        <section class="card">
          <header class="card__head">
            <h2>Задания</h2>
            <p class="muted">Нажимай “Refresh” после выполнения. Проверка идёт сервером.</p>
          </header>

          <div class="card__body stack">

            <div class="taskRow">
              <div class="taskL">
                <div class="taskTitle">Wallet</div>
                <div class="taskDesc muted">Привязка кошелька через challenge‑подпись.</div>
              </div>
              <div class="taskR">
                <span class="badge no" id="b_wallet">NO</span>
                <button id="btnWallet" class="primary" type="button">Connect</button>
              </div>
            </div>

            <div class="taskRow">
              <div class="taskL">
                <div class="taskTitle">Telegram</div>
                <div class="taskDesc muted">Подписка на канал @logosblockchain.</div>
              </div>
              <div class="taskR">
                <span class="badge wait" id="b_tg">WAIT</span>
                <a class="secondary" href="https://t.me/logosblockchain" target="_blank" rel="noopener noreferrer">Open</a>
              </div>
            </div>

            <div class="taskRow">
              <div class="taskL">
                <div class="taskTitle">X username</div>
                <div class="taskDesc muted">Нужен для автоматической проверки действий.</div>
                <div class="row2">
                  <input id="inpTwUser" class="mono monoInput" placeholder="@yourname" autocomplete="off"/>
                  <button id="btnTwSave" class="secondary" type="button">Save</button>
                </div>
              </div>
              <div class="taskR">
                <span class="badge wait" id="b_tw_user">WAIT</span>
              </div>
            </div>

            <div class="taskRow">
  <div class="taskLeft">
    <div class="taskTitle">X username</div>
    <div class="taskDesc muted">Введи свой @username (нужен для проверки лайков/ретвитов/постов)</div>
  </div>
  <div class="taskRight">
    <input id="inpXUser" class="mono monoInput" placeholder="@yourname" />
    <button id="btnXSave" class="secondary" type="button">Save</button>
    <button id="btnXVerify" class="primary" type="button">Verify</button>
  </div>
</div>

<div class="taskRow">
              <div class="taskL">
                <div class="taskTitle">X follow</div>
                <div class="taskDesc muted">Подписка на @RspLogos.</div>
              </div>
              <div class="taskR">
                <span class="badge wait" id="b_tw_follow">WAIT</span>
                <a class="secondary" href="https://x.com/RspLogos" target="_blank" rel="noopener noreferrer">Open</a>
              </div>
            </div>

            <div class="taskRow">
              <div class="taskL">
                <div class="taskTitle">X like</div>
                <div class="taskDesc muted">Любой лайк по последним постам @RspLogos засчитывается.</div>
              </div>
              <div class="taskR">
                <span class="badge wait" id="b_tw_like">WAIT</span>
                <a class="secondary" href="https://x.com/RspLogos" target="_blank" rel="noopener noreferrer">Open</a>
              </div>
            </div>

            <div class="taskRow">
              <div class="taskL">
                <div class="taskTitle">X repost / post</div>
                <div class="taskDesc muted">Любой ретвит @RspLogos ИЛИ пост с упоминанием @RspLogos.</div>
              </div>
              <div class="taskR">
                <span class="badge wait" id="b_tw_rt">WAIT</span>
                <a class="secondary" href="https://x.com/RspLogos" target="_blank" rel="noopener noreferrer">Open</a>
              </div>
            </div>

            <button id="btnRefresh" class="secondary btnRefresh" type="button">Refresh status</button>

          </div>
        </section>
      </div>

      <section class="card">
        <header class="card__head">
          <h2>Диагностика</h2>
          <p class="muted">Тут видно ответы API/ошибки.</p>
        </header>
        <pre id="out" class="mono outPanel"></pre>
      </section>

    </div>
  </main>
</body>
</html>

```

### FILE: /var/www/logos/landing/app.bundle.js
```
(function(){
  // ---------- helpers ----------
  const enc = new TextEncoder();
  const $ = (q)=>document.querySelector(q);
  function toast(m){ const t=$("#toast"); if(!t) return; t.textContent=m; t.classList.add("show"); setTimeout(()=>t.classList.remove("show"),2500); }
  function be8(n){ const a=new Uint8Array(8); new DataView(a.buffer).setBigUint64(0, BigInt(n)); return a; }
  function cat(...xs){ let L=0; for(const a of xs) L+=a.length; const out=new Uint8Array(L); let o=0; for(const a of xs){ out.set(a,o); o+=a.length; } return out; }
  const B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";
  function b58(b){ let x=0n; for(const v of b) x=(x<<8n)+BigInt(v); let s=""; while(x>0n){ const r=Number(x%58n); x/=58n; s=B58[r]+s; } for(const v of b){ if(v===0) s="1"+s; else break; } return s||"1"; }
  const API="/api";
  async function apiGet(p){ const r=await fetch(API+p); if(!r.ok) throw new Error(`GET ${p} -> ${r.status}`); return r.json(); }
  async function apiPost(p,b){ const r=await fetch(API+p,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(b)}); if(!r.ok){ const t=await r.text().catch(()=> ""); throw new Error(`POST ${p} -> ${r.status} ${t}`);} return r.json(); }
  function canon(from,to,amount,nonce){ return cat(enc.encode(from),Uint8Array.of(0x7c),enc.encode(to),Uint8Array.of(0x7c),be8(amount),Uint8Array.of(0x7c),be8(nonce)); }
  function renderHistory(items){ const tb=$("#historyTable tbody"); if(!tb) return; tb.innerHTML=""; for(const it of (items||[])){ const e=it.evt||{}; const tr=document.createElement("tr"); let cp="-"; if(e.dir==="out") cp=e.to||"-"; else if(e.dir==="in") cp=e.from||"-"; else cp=e.rid||"-"; tr.innerHTML=`<td>${e.type||"transfer"}</td><td class="mono" style="max-width:260px;overflow:hidden;text-overflow:ellipsis">${cp}</td><td>${e.amount??"-"}</td><td>${e.nonce??"-"}</td><td>${e.height??"-"}</td><td class="mono" style="max-width:280px;overflow:hidden;text-overflow:ellipsis">${e.tx??"-"}</td><td><button class="ghost btnCopyTx" data-tx="${e.tx??""}">copy</button></td>`; tb.appendChild(tr);} }

  // ---------- Secure vault (PBKDF2 + AES-GCM). LocalStorage always; IndexedDB optional ----------
  const DB="logos_secure_v3", STORE="vault", REC_ID="key", LS="logos_secure_v3_backup";
  const PBKDF2_ITER=250000, SALT_LEN=16, IV_LEN=12, AUTOLOCK_MS=5*60*1000;
  let unlockedPriv=null, unlockedPubRaw=null, autolockTimer=null;

  function idbOpen(){return new Promise((res,rej)=>{const r=indexedDB.open(DB,1);r.onupgradeneeded=()=>{const db=r.result;if(!db.objectStoreNames.contains(STORE))db.createObjectStore(STORE,{keyPath:'id'});};r.onsuccess=()=>res(r.result);r.onerror=()=>rej(r.error);});}
  function idbGet(db,id){return new Promise((res,rej)=>{const tx=db.transaction(STORE,"readonly");const rq=tx.objectStore(STORE).get(id);rq.onsuccess=()=>res(rq.result);rq.onerror=()=>rej(rq.error);});}
  function idbPut(db,obj){return new Promise((res,rej)=>{const tx=db.transaction(STORE,"readwrite");tx.objectStore(STORE).put(obj);tx.oncomplete=()=>res();tx.onerror=()=>rej(tx.error);});}
  function rand(n){const a=new Uint8Array(n);crypto.getRandomValues(a);return a;}
  async function kdf(pass,salt){const base=await crypto.subtle.importKey("raw",enc.encode(pass),{name:"PBKDF2"},false,["deriveKey"]);return crypto.subtle.deriveKey({name:"PBKDF2",salt,iterations:PBKDF2_ITER,hash:"SHA-256"},base,{name:"AES-GCM",length:256},false,["encrypt","decrypt"]);}

  async function vaultStatus(){ let rec=null; try{ const db=await idbOpen(); rec=await idbGet(db,REC_ID); }catch{} if(!rec && !localStorage.getItem(LS)) return "empty"; if(unlockedPriv) return "unlocked"; return "locked"; }
  function vaultLock(){ unlockedPriv=null; unlockedPubRaw=null; clearTimeout(autolockTimer); }
  function scheduleAutolock(){ clearTimeout(autolockTimer); autolockTimer=setTimeout(()=>{ vaultLock(); $("#lockOverlay")?.classList.remove("hidden"); }, AUTOLOCK_MS); }

  async function vaultCreateWithPass(pass){
    try{
      // генерим пару в WebCrypto (Ed25519). Большинство новых браузеров поддерживают; иначе покажем ошибку.
      const kp = await crypto.subtle.generateKey({name:"Ed25519"}, true, ["sign","verify"]);
      const pkcs8 = new Uint8Array(await crypto.subtle.exportKey("pkcs8", kp.privateKey));
      const pubRaw= new Uint8Array(await crypto.subtle.exportKey("raw",   kp.publicKey));
      const salt=rand(SALT_LEN), iv=rand(IV_LEN), key=await kdf(pass,salt);
      const ct  = new Uint8Array(await crypto.subtle.encrypt({name:"AES-GCM",iv}, key, pkcs8));

      // резерв в LS — ВСЕГДА
      localStorage.setItem(LS, JSON.stringify({
        salt:btoa(String.fromCharCode(...salt)),
        iv:  btoa(String.fromCharCode(...iv)),
        ct:  btoa(String.fromCharCode(...ct)),
        pubRaw:btoa(String.fromCharCode(...pubRaw)),
        iter:PBKDF2_ITER
      }));
      // попытка IDB — не критично
      try{ const db=await idbOpen(); await idbPut(db,{id:REC_ID, salt, iv, ct, pubRaw, iter:PBKDF2_ITER}); }catch{}

      unlockedPriv = kp.privateKey; unlockedPubRaw = pubRaw; scheduleAutolock();
      return true;
    }catch(e){
      console.error("vaultCreate error", e);
      toast("Ошибка создания ключа. Обнови браузер или установи современный.");
      return false;
    }
  }

  async function vaultUnlock(pass){
    let rec=null; try{ const db=await idbOpen(); rec=await idbGet(db,REC_ID); }catch{}
    if(!rec){ const raw=localStorage.getItem(LS); if(!raw) throw new Error("NoKey"); const o=JSON.parse(raw); rec={salt:Uint8Array.from(atob(o.salt),c=>c.charCodeAt(0)),iv:Uint8Array.from(atob(o.iv),c=>c.charCodeAt(0)),ct:Uint8Array.from(atob(o.ct),c=>c.charCodeAt(0)),pubRaw:Uint8Array.from(atob(o.pubRaw),c=>c.charCodeAt(0)),iter:o.iter}; }
    const key=await kdf(pass,new Uint8Array(rec.salt));
    const pkcs8=await crypto.subtle.decrypt({name:"AES-GCM",iv:new Uint8Array(rec.iv)},key,new Uint8Array(rec.ct)).catch(()=>null);
    if(!pkcs8) throw new Error("BadPassword");
    unlockedPriv=await crypto.subtle.importKey("pkcs8",pkcs8,{name:"Ed25519"},false,["sign"]);
    unlockedPubRaw=new Uint8Array(rec.pubRaw); scheduleAutolock(); return true;
  }

  async function vaultExportPkcs8Base64(){
    if(!unlockedPriv) throw new Error("Locked");
    const pkcs8=new Uint8Array(await crypto.subtle.exportKey("pkcs8",unlockedPriv));
    return btoa(String.fromCharCode(...pkcs8));
  }

  async function vaultImportPkcs8Base64(b64, pass){
    const pkcs8 = Uint8Array.from(atob(b64), c=>c.charCodeAt(0));
    // сгенерим временную pubRaw
    const tmp   = await crypto.subtle.generateKey({name:"Ed25519"},true,["sign","verify"]);
    const pubRaw= new Uint8Array(await crypto.subtle.exportKey("raw", tmp.publicKey));
    const salt=rand(SALT_LEN), iv=rand(IV_LEN), key=await kdf(pass,salt);
    const ct  = new Uint8Array(await crypto.subtle.encrypt({name:"AES-GCM",iv},key,pkcs8));
    localStorage.setItem(LS, JSON.stringify({salt:btoa(String.fromCharCode(...salt)),iv:btoa(String.fromCharCode(...iv)),ct:btoa(String.fromCharCode(...ct)),pubRaw:btoa(String.fromCharCode(...pubRaw)),iter:PBKDF2_ITER}));
    try{ const db=await idbOpen(); await idbPut(db,{id:REC_ID,salt,iv,ct,pubRaw,iter:PBKDF2_ITER}); }catch{}
    unlockedPriv=await crypto.subtle.importKey("pkcs8",pkcs8,{name:"Ed25519"},false,["sign"]);
    unlockedPubRaw=pubRaw; scheduleAutolock(); return true;
  }

  async function vaultReset(){ try{indexedDB.deleteDatabase(DB);}catch{} try{localStorage.removeItem(LS);}catch{} vaultLock(); }

  function currentRid(){ return unlockedPubRaw ? b58(unlockedPubRaw) : ""; }

  async function signEd25519(msg){ if(!unlockedPriv) throw new Error("Locked"); const sig=new Uint8Array(await crypto.subtle.sign({name:"Ed25519"},unlockedPriv,msg)); let bin=""; for(let i=0;i<sig.length;i++) bin+=String.fromCharCode(sig[i]); return btoa(bin); }

  // ---------- Wallet logic ----------
  async function resolveRID(){ const rid=($("#ridInput")?.value||"").trim(); return rid || currentRid(); }

  async function loadPassport(){
    const rid=await resolveRID();
    const [p,s,h]=await Promise.allSettled([apiGet(`/profile/${rid}`),apiGet(`/stake/summary/${rid}`),apiGet(`/history/${rid}?limit=10`)]);
    const prof=p.status==="fulfilled"?p.value:{}; const sum=s.status==="fulfilled"?s.value:{}; const items=h.status==="fulfilled"?(h.value.items||[]):[];
    $("#passportRid").textContent=rid||"—";
    $("#passportBal").textContent=prof.balance??"—";
    $("#passportNonce").textContent=(prof.nonce&&prof.nonce.next)??"—";
    $("#passportHead").textContent=prof.head??"—";
    $("#passportDelegated").textContent=sum.delegated??"—";
    $("#passportEntries").textContent=sum.entries??"—";
    $("#passportClaimable").textContent=sum.claimable??"—";
    renderHistory(items);
  }

  async function refreshStake(){
    const rid=await resolveRID(); if(!rid) return;
    try{ const s=await apiGet(`/stake/summary/${rid}`); $("#chipDelegated").textContent=String(s.delegated??0); $("#chipEntries").textContent=String(s.entries??0); $("#chipClaimable").textContent=String(s.claimable??0); }catch{}
  }

  async function syncProfile(){
    const rid=await resolveRID(); if(!rid){ $("#balanceBadge").textContent="—"; $("#nonceBadge").textContent="—"; return; }
    const prof=await apiGet(`/profile/${rid}`);
    $("#balanceBadge").textContent=prof.balance??"—";
    $("#nonceBadge").textContent=(prof.nonce&&prof.nonce.next)??"—";
    await refreshStake(); await loadPassport();
  }

  async function showHistory(){ const rid=await resolveRID(); if(!rid) return; const h=await apiGet(`/history/${rid}?limit=50`); renderHistory(h.items||[]); }

  async function onSend(){
    const from=currentRid(), to=($("#toRid")?.value||"").trim(), amount=Number($("#sendAmount")?.value||0);
    if(!from){ toast("Кошелёк заблокирован"); $("#lockOverlay").classList.remove("hidden"); return; }
    if(!to||!amount){ toast("Укажи получателя и сумму"); return; }
    const nn=await apiGet(`/nonce/${from}`); const nonce=nn.next;
    const sigB64=await signEd25519( canon(from,to,amount,nonce) );
    const res=await apiPost(`/submit_tx`,{from,to,amount,nonce,sig:sigB64});
    toast(res?.status==="queued"?"Транзакция отправлена":"Отправка выполнена");
    await syncProfile(); await showHistory(); await loadPassport();
  }

  // ---------- Secure overlay handlers ----------
  let tries=5;
  async function updateLockView(){
    $("#rpHost").textContent = location.host;
    const st = await vaultStatus();
    if(st==="empty"){ $("#lockStepSetup").classList.remove("hidden"); $("#lockStepUnlock").classList.add("hidden"); }
    if(st==="locked"){ $("#lockStepSetup").classList.add("hidden"); $("#lockStepUnlock").classList.remove("hidden"); }
    if(st==="unlocked"){ $("#lockOverlay").classList.add("hidden"); await afterUnlock(); }
  }
  async function afterUnlock(){
    const rid=currentRid(); if(rid){ $("#ridInput").value=rid; $("#ridValidator").value=rid; $("#passportRid").textContent=rid; }
    await syncProfile(); await loadPassport();
  }
  async function handleCreate(){
    const p1=$("#pwNew").value.trim(), p2=$("#pwNew2").value.trim();
    if(p1.length<8){ toast("Пароль минимум 8 символов"); return; }
    if(p1!==p2){ toast("Пароли не совпадают"); return; }
    toast("Создаём и шифруем ключ…");
    const ok=await vaultCreateWithPass(p1);
    if(!ok){ toast("Не удалось создать ключ"); return; }
    $("#lockOverlay").classList.add("hidden"); tries=5; await afterUnlock();
  }
  async function handleUnlock(){
    const p=$("#pwUnlock").value.trim();
    try{ await vaultUnlock(p); $("#lockOverlay").classList.add("hidden"); tries=5; await afterUnlock(); }
    catch(e){ tries--; $("#triesLeft2").textContent=String(tries); toast(tries>0?"Неверный пароль":"Слишком много попыток — кошелёк сброшен"); if(tries<=0){ await (async()=>{try{indexedDB.deleteDatabase(DB);}catch{} try{localStorage.removeItem(LS);}catch{}})(); location.reload(); } }
  }
  async function handleForgot(){ if(confirm("Очистить локальный ключ и настройки?")){ try{indexedDB.deleteDatabase(DB);}catch{} try{localStorage.removeItem(LS);}catch{} location.reload(); } }
  async function handleImportSetup(){
    const b64=prompt("Вставь PKCS8 Base64 ключ"); if(!b64) return;
    const pass=prompt("Создай пароль шифрования (≥8)"); if(!pass||pass.length<8){ toast("Пароль ≥ 8"); return; }
    const ok=await vaultImportPkcs8Base64(b64, pass);
    if(!ok){ toast("Импорт не удался"); return; }
    $("#lockOverlay").classList.add("hidden"); tries=5; await afterUnlock();
  }
  async function handleImportUnlock(){
    const b64=prompt("Вставь PKCS8 Base64 ключ"); if(!b64) return;
    const pass=prompt("Пароль шифрования (≥8)"); if(!pass||pass.length<8){ toast("Пароль ≥ 8"); return; }
    const ok=await vaultImportPkcs8Base64(b64, pass);
    if(!ok){ toast("Импорт не удался"); return; }
    $("#lockOverlay").classList.add("hidden"); tries=5; await afterUnlock();
  }

  // ---------- bindings ----------
  document.addEventListener("click",e=>{ const b=e.target.closest(".btnCopyTx"); if(b){ navigator.clipboard.writeText(b.dataset.tx||"").then(()=>toast("Скопировано")).catch(()=>toast("Не удалось скопировать")); } });

  document.addEventListener("DOMContentLoaded", ()=>{
    // secure
    $("#rpHost").textContent = location.host;
    $("#btnCreate").addEventListener("click", handleCreate);
    $("#btnUnlock").addEventListener("click", handleUnlock);
    $("#btnForgot").addEventListener("click", handleForgot);
    $("#btnImportSetup").addEventListener("click", handleImportSetup);
    $("#btnImportUnlock").addEventListener("click", handleImportUnlock);

    // wallet
    $("#btnBalance").addEventListener("click", ()=>syncProfile().catch(e=>toast(String(e))));
    $("#btnSync").addEventListener("click", ()=>syncProfile().catch(e=>toast(String(e))));
    $("#btnShowHist").addEventListener("click", ()=>showHistory().catch(e=>toast(String(e))));
    $("#btnStakeDelegate").addEventListener("click", async ()=>{ const rid=(await resolveRID()); const amount=Number($("#stakeAmount").value||0); const r=await apiPost(`/stake/delegate`,{validator:rid,amount}); toast(r.ok?"Delegated":"Delegate failed"); await refreshStake(); await loadPassport(); });
    $("#btnStakeUndelegate").addEventListener("click", async ()=>{ const rid=(await resolveRID()); const amount=Number($("#unstakeAmount").value||0); const r=await apiPost(`/stake/undelegate`,{validator:rid,amount}); toast(r.ok?"Undelegated":"Undelegate failed"); await refreshStake(); await loadPassport(); });
    $("#btnStakeClaim").addEventListener("click", async ()=>{ const rid=(await resolveRID()); const r=await apiPost(`/stake/claim`,{rid}); toast(r.ok?`Claimed ${r.claimed}`:"Claim failed"); await refreshStake(); await loadPassport(); });
    $("#btnSend").addEventListener("click", ()=>onSend().catch(e=>toast(String(e))));
    $("#btnCopyRid").addEventListener("click", ()=>{ const rid=$("#passportRid").textContent||$("#ridInput").value||""; navigator.clipboard.writeText(rid).then(()=>toast("RID скопирован")); });

    updateLockView().catch(()=>toast("Ошибка инициализации"));
  });
})();

```

### FILE: /var/www/logos/landing/app.v20251124.js
```
(() => {
  const dicts = {
    en: {
      menu_label_lang: "Language",
      menu_label_nav: "Navigation",
      menu_label_actions: "Actions",
      menu_label_social: "Community",
      nav_intro: "Overview",
      nav_speed: "Speed",
      nav_privacy: "Privacy",
      nav_fees: "Fees",
      nav_reliability: "Reliability",
      nav_tech: "Technology",
      nav_rsp: "LOGOS RSP",
      nav_agi: "LOGOS-AGI",
      nav_better: "Why LOGOS",
      nav_short: "In short",
      menu_presale: "Presale / Airdrop (soon)",
      menu_staking: "Staking (soon)",
      menu_telegram: "Telegram",
      menu_twitter: "X (Twitter)",
      menu_email: "Email: simbiotai@proton.me",

      intro_title: "LOGOS – a next-generation blockchain built on resonance architecture",
      intro_p1: "LOGOS is not just another network. It is a new-generation blockchain built around speed, privacy and a deep resonance architecture.",
      intro_p2: "We created an L1 that works fast and stays stable without unnecessary complexity. Blocks are formed instantly, the network handles high traffic, fees remain minimal and the level of privacy is something most mainstream chains simply do not offer today.",
      intro_p3: "LOGOS is the foundation for a new digital environment ready for millions of users.",

      speed_title: "Speed and performance",
      speed_p: "We tested the network under real conditions, not just on paper. Peak results reached 2,000+ transactions per second with stable finality and no forks. The architecture is designed to go further: with more nodes and phase optimisation, 10,000+ tx/s is achievable without sacrificing stability. The idea is simple: a blockchain should feel as fast as modern payment systems — and LOGOS behaves exactly like that.",

      privacy_title: "Privacy on a new level",
      privacy_p1: "From day one LOGOS was designed as a network where:",
      privacy_li1: "a user cannot be directly tied to a transaction;",
      privacy_li2: "packet routes are difficult to trace;",
      privacy_li3: "metadata leakage is minimised;",
      privacy_li4: "there are no obvious network fingerprints;",
      privacy_li5: "there are no standard tracking points.",
      privacy_p2: "Privacy in LOGOS is not a switch or a feature. It is baked into the architecture.",

      fees_title: "Low fees and clean finality",
      fees_p: "Blocks do not compete, conflict or roll back. Each transaction passes once and is recorded permanently. Fees are among the lowest across L1 chains because we avoid heavy computation and bloated contracts, so even under serious load basic transfers stay affordable.",

      reliability_title: "Reliability and production readiness",
      reliability_p: "The network is ready for production use: orchestration tools spin up nodes in seconds, bridges work securely, and there is staking, archiving and balancing. LOGOS nodes can run on ordinary servers, and the infrastructure is stress‑tested under high load. LOGOS is not an experiment – it is an autonomous, working network.",

      technology_title: "The technology behind LOGOS",
      technology_p: "LOGOS is built on a resonance‑symbolic architecture – our own know‑how for organising data and synchronisation. Instead of relying on heavy computation and overly complex consensus schemes, we use rhythm, structure and phase dynamics. This makes the network more stable under pressure, quicker to react to spikes and harder to attack on the network layer, while keeping scaling straightforward.",

      rsp_title: "LOGOS RSP – communication without traces",
      rsp_p: "At the core of the ecosystem lies the confidential communication protocol LOGOS RSP. In practice it means communication without classic IP routing and with minimal digital traces, resilient to interception and analysis. RSP can operate not only over the internet but also via alternative carriers – light, sound, radio and offline channels. It pushes LOGOS far beyond a typical blockchain. Technical details remain closed – this is our key innovation.",

      agi_title: "LOGOS-AGI – a new architectural layer",
      agi_p: "We are also building LOGOS‑AGI – a new type of artificial intelligence. It does not rely on huge neural networks and massive datasets, but on resonance logic and symbolic structures that underlie the whole system. Early prototypes show that such AI can work without GPUs, learn without giant datasets and discover its own patterns, operating on meaning rather than pure statistics. This turns LOGOS from a blockchain into a platform for future autonomous systems.",

      better_title: "Why LOGOS is different",
      better_intro: "LOGOS is built for the real world, not just for slides. In short, our advantages:",
      better_item1: "Real speed, proven by load tests.",
      better_item2: "Genuine privacy instead of pseudo‑anonymity.",
      better_item3: "Minimal transaction fees.",
      better_item4: "Instant finality without forks or rollbacks.",
      better_item5: "Resilience to network attacks and load spikes.",
      better_item6: "Straightforward scaling of the network.",
      better_item7: "Infrastructure ready for millions of users.",
      better_item8: "A unique resonance architecture you will not find in any other chain.",

      short_title: "In short",
      short_p: "LOGOS is a next‑generation L1 blockchain built on resonance architecture: high speed, low fees, adaptive behaviour and strong privacy. Inside we develop our own communication protocol and the LOGOS‑AGI direction. We are not building just another crypto platform – we are building the base layer for Web4.",

      footer_note: "LOGOS LRB • Resonance Blockchain • Ready for millions of users"
    },

    de: {
      menu_label_lang: "Sprache",
      menu_label_nav: "Navigation",
      menu_label_actions: "Aktionen",
      menu_label_social: "Community",
      nav_intro: "Überblick",
      nav_speed: "Geschwindigkeit",
      nav_privacy: "Privatsphäre",
      nav_fees: "Gebühren",
      nav_reliability: "Stabilität",
      nav_tech: "Technologie",
      nav_rsp: "LOGOS RSP",
      nav_agi: "LOGOS‑AGI",
      nav_better: "Vorteile",
      nav_short: "Kurzfassung",
      menu_presale: "Presale / Airdrop (bald)",
      menu_staking: "Staking (bald)",
      menu_telegram: "Telegram",
      menu_twitter: "X (Twitter)",
      menu_email: "Email: simbiotai@proton.me",

      intro_title: "LOGOS – Blockchain der nächsten Generation auf Resonanz‑Architektur",
      intro_p1: "LOGOS ist nicht einfach eine weitere Chain, sondern eine Blockchain der nächsten Generation – gebaut für Geschwindigkeit, Privatsphäre und eine tiefe Resonanz‑Architektur.",
      intro_p2: "Wir haben eine L1 entwickelt, die schnell und stabil läuft ohne überflüssige Komplexität. Blöcke entstehen praktisch sofort, das Netzwerk trägt hohe Last, Gebühren bleiben minimal und das Datenschutzniveau ist höher als bei den meisten Mainstream‑Netzen.",
      intro_p3: "LOGOS ist ein Fundament für eine neue digitale Umgebung, bereit für Millionen Nutzer.",

      speed_title: "Geschwindigkeit und Performance",
      speed_p: "In Lasttests verarbeitete LOGOS tausende Transaktionen pro Sekunde mit stabiler Finalität und ohne Forks. Die Architektur ist darauf ausgelegt, bei mehr Nodes und Optimierungen in den Bereich von 10.000+ tx/s zu gehen – ohne Stabilität zu verlieren. Ziel: Eine Blockchain, die sich so schnell anfühlt wie moderne Bezahlsysteme.",

      privacy_title: "Privatsphäre auf neuem Niveau",
      privacy_p1: "LOGOS wurde von Anfang an so entworfen, dass:",
      privacy_li1: "Nutzer nicht direkt mit einzelnen Transaktionen verknüpft werden können;",
      privacy_li2: "Routen schwer nachvollziehbar sind;",
      privacy_li3: "Metadaten auf ein Minimum reduziert werden;",
      privacy_li4: "keine offensichtlichen Fingerabdrücke sichtbar sind;",
      privacy_li5: "es keine Standard‑Tracking‑Punkte gibt.",
      privacy_p2: "Privatsphäre ist hier kein Add‑on, sondern Teil der Basisarchitektur.",

      fees_title: "Niedrige Gebühren und saubere Finalität",
      fees_p: "Blöcke konkurrieren nicht miteinander und werden nicht zurückgesetzt. Jede Transaktion wird einmal verarbeitet und dauerhaft geschrieben. Durch die leichte Architektur ohne unnötige Rechenlast gehören die Gebühren zu den niedrigsten im L1‑Bereich.",

      reliability_title: "Zuverlässigkeit und Belastbarkeit",
      reliability_p: "Das Netzwerk ist produktionsreif: Orchestrierungstools starten Nodes in Sekunden, Bridges arbeiten sicher, Staking und Archivierung sind integriert. LOGOS‑Nodes laufen auf normalen Servern, die Infrastruktur wird unter hoher Last gestresst. LOGOS ist ein laufendes Netzwerk, kein Experiment.",

      technology_title: "Technologie hinter LOGOS",
      technology_p: "LOGOS basiert auf einer resonanz‑symbolischen Architektur – unserem eigenen Ansatz für Datenorganisation und Synchronisation. Statt auf schwere Rechenarbeit und komplizierte Konsens‑Schemata zu setzen, nutzen wir Rhythmus, Struktur und Phasenprozesse. Das macht das System stabiler unter Last und leichter skalierbar.",

      rsp_title: "LOGOS RSP – Kommunikation ohne Spuren",
      rsp_p: "Im Zentrum der Ökosphäre steht das vertrauliche Kommunikationsprotokoll LOGOS RSP. In der Praxis bedeutet das Kommunikation mit minimalen digitalen Spuren, robust gegen Abhören und Analyse – auch über alternative Träger wie Licht, Ton, Funk oder Offline‑Kanäle. Die Details bleiben bewusst geschlossen.",

      agi_title: "LOGOS‑AGI – eine neue Schicht",
      agi_p: "LOGOS‑AGI ist unser Ansatz für eine neue Art von KI, die eher auf Resonanzlogik und symbolischen Strukturen als auf riesigen Netzen und Datensätzen basiert. Erste Prototypen zeigen: Arbeiten ohne GPU, Lernen ohne Gigadaten, Fokus auf Bedeutung statt Statistik. Damit wird LOGOS zur Plattform für zukünftige autonome Systeme.",

      better_title: "Warum LOGOS anders ist",
      better_intro: "LOGOS wurde für reale Nutzung gebaut, nicht nur für Slides. Unsere wichtigsten Vorteile:",
      better_item1: "Echte Geschwindigkeit, in Lasttests nachgewiesen.",
      better_item2: "Konsequente Privatsphäre statt Pseudo‑Anonymität.",
      better_item3: "Sehr niedrige Gebühren.",
      better_item4: "Schnelle Finalität ohne Forks oder Rollbacks.",
      better_item5: "Robust gegenüber Netzangriffen und Lastspitzen.",
      better_item6: "Einfache Skalierung des Netzwerks.",
      better_item7: "Infrastruktur für Millionen Nutzer.",
      better_item8: "Eine einzigartige Resonanz‑Architektur, die andere Chains nicht haben.",

      short_title: "Kurz und knapp",
      short_p: "LOGOS ist eine L1‑Blockchain der nächsten Generation mit Resonanz‑Architektur: hohe Geschwindigkeit, niedrige Gebühren, adaptive Netzlogik und starke Privatsphäre. Dazu kommen ein eigener Kommunikationsansatz und die Linie LOGOS‑AGI – ein Fundament für Web4.",
      footer_note: "LOGOS LRB • Resonanz‑Blockchain • Für Millionen Nutzer gebaut"
    }
  };

  const transEls = Array.from(document.querySelectorAll("[data-i18n]"));
  transEls.forEach(el => {
    if (!el.dataset.i18nRu) {
      el.dataset.i18nRu = el.textContent.trim();
    }
  });

  function setActiveLang(lang){
    document.querySelectorAll("[data-lang-btn]").forEach(btn => {
      btn.classList.toggle("is-active", btn.dataset.langBtn === lang);
    });
  }

  function applyLang(lang){
    if (!dicts[lang]) lang = "ru";

    if (lang === "ru"){
      document.documentElement.lang = "ru";
      document.documentElement.dataset.lang = "ru";
      transEls.forEach(el => {
        if (el.dataset.i18nRu) el.textContent = el.dataset.i18nRu;
      });
      localStorage.setItem("logos_lang","ru");
      setActiveLang("ru");
      return;
    }

    const dict = dicts[lang];
    document.documentElement.lang = lang;
    document.documentElement.dataset.lang = lang;

    transEls.forEach(el => {
      const key = el.getAttribute("data-i18n");
      if (dict[key]) el.textContent = dict[key];
    });

    localStorage.setItem("logos_lang",lang);
    setActiveLang(lang);
  }

  // меню
  const body  = document.body;
  const menu  = document.querySelector("[data-menu]");
  const toggle = document.querySelector("[data-menu-toggle]");

  if (menu && toggle){
    toggle.addEventListener("click", () => {
      const hidden = menu.hasAttribute("hidden");
      if (hidden){
        menu.removeAttribute("hidden");
        body.classList.add("menu-open");
        toggle.setAttribute("aria-expanded","true");
      } else {
        menu.setAttribute("hidden","");
        body.classList.remove("menu-open");
        toggle.setAttribute("aria-expanded","false");
      }
    });

    menu.querySelectorAll("[data-menu-link]").forEach(link => {
      link.addEventListener("click", () => {
        menu.setAttribute("hidden","");
        body.classList.remove("menu-open");
        toggle.setAttribute("aria-expanded","false");
      });
    });
  }

  document.querySelectorAll("[data-lang-btn]").forEach(btn => {
    btn.addEventListener("click", () => applyLang(btn.dataset.langBtn));
  });

  const saved = localStorage.getItem("logos_lang") || "ru";
  applyLang(saved);
})();

```

### FILE: /var/www/logos/landing/css/styles.css
```
:root{color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:#0b1016;color:#e7eef7;font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
.wrap{max-width:980px;margin:24px auto;padding:0 16px}
h1{font-size:22px;margin:0 0 16px}
.section{background:#111827;border:1px solid #1a2436;border-radius:14px;padding:16px;margin:14px 0}
.grid{display:grid;gap:12px}
.cols-3{grid-template-columns:repeat(3,1fr)}
.cols-2{grid-template-columns:repeat(2,1fr)}
.mt10{margin-top:10px}
.row{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.space-between{justify-content:space-between}
.gap8{gap:8px}
.break{word-break:break-all}
input,button,textarea{border-radius:10px;border:1px solid #28344c;background:#0d1420;color:#e7eef7;padding:10px 12px;width:100%}
textarea{min-height:90px;resize:vertical}
input:focus,textarea:focus{outline:none;border-color:#3a70ff;box-shadow:0 0 0 2px #3a70ff26}
button{background:#3366ff;border:none;cursor:pointer}
button.secondary{background:#1a2333}
button.ghost{background:#0d1420;border:1px dashed #2a3a56}
label{display:block;margin:6px 0 6px;color:#98aec6;font-size:13px}
.badge{background:#141e2d;border:1px solid #2a3a56;border-radius:999px;padding:6px 10px;font-size:12px}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
.table{width:100%;border-collapse:collapse}
.table th,.table td{border-bottom:1px solid #1a2436;padding:10px 8px;text-align:left;font-size:13px}
.scroll{overflow:auto}
.toast{position:fixed;right:16px;bottom:16px;display:none;background:#0e1520;border:1px solid #20406f;color:#bfe0ff;padding:12px 14px;border-radius:10px;box-shadow:0 10px 30px rgba(0,0,0,.35);max-width:80%}
.toast.show{display:block}

/* Secure overlay */
#lockOverlay{position:fixed;inset:0;background:#0b1016;display:flex;align-items:center;justify-content:center;z-index:9999}
#lockCard{width:min(560px,92%);background:#0f1723;border:1px solid #243048;border-radius:16px;padding:18px}
#brand{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
#phish{background:#0c1420;border:1px solid #2a3a56;border-radius:10px;padding:10px;font-size:12px;color:#9fb2c9}
#lockActions{display:flex;gap:8px;margin-top:10px}
#lockMeta{display:flex;gap:8px;margin-top:8px;flex-wrap:wrap}
#lockMeta .badge{font-size:11px}
.hidden{display:none}
.muted{color:#9fb2c9}

```

### FILE: /var/www/logos/landing/explorer/explorer.css
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

### FILE: /var/www/logos/landing/explorer/explorer.js
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

### FILE: /var/www/logos/landing/explorer/index.html
```
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta http-equiv="Cache-Control" content="no-store"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Explorer — v2 (inline)</title>
  <style>
    :root{--bg:#0b0c10;--card:#11151a;--line:#1e242c;--muted:#9aa4af;--txt:#e6edf3;--btn:#1665c1;--btn-b:#3b7ddd;}
    *{box-sizing:border-box}
    body{font-family:system-ui,Segoe UI,Roboto,Arial,sans-serif;margin:0;background:var(--bg);color:var(--txt)}
    header{padding:12px;background:var(--card);border-bottom:1px solid var(--line);display:flex;gap:10px;align-items:center;flex-wrap:wrap}
    header h1{font-size:18px;margin:0}
    #jsStat{font-size:12px;margin-left:auto}
    main{max-width:1100px;margin:18px auto;padding:0 12px}
    section{background:var(--card);margin:12px 0;border-radius:14px;padding:14px;border:1px solid var(--line)}
    h3{margin:6px 0 12px 0}
    .row{display:flex;gap:10px;flex-wrap:wrap}
    .row>.grow{flex:1 1 360px}
    .row>.fit{flex:0 0 140px}
    input{width:100%;padding:10px;border-radius:10px;border:1px solid var(--line);background:#0b0f14;color:#e6edf3}
    button{padding:10px 14px;border-radius:10px;border:1px solid var(--btn-b);background:var(--btn);color:#fff;font-weight:600;cursor:pointer}
    .btns{display:flex;gap:8px;flex-wrap:wrap}
    pre{white-space:pre-wrap;word-break:break-word;background:#0b0f14;border:1px solid var(--line);border-radius:10px;padding:10px;overflow:auto;margin:8px 0 0}
    .cards{display:grid;grid-template-columns:1fr 1fr;gap:12px}
    @media(max-width:900px){.cards{grid-template-columns:1fr}}
    .table-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px;margin-top:8px}
    table{width:100%;border-collapse:collapse;min-width:700px}
    th,td{border-bottom:1px solid var(--line);padding:8px 10px;text-align:left;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;white-space:nowrap}
    .muted{color:#9aa4af}
    .pill{border:1px solid var(--line);padding:8px 10px;border-radius:10px;background:#0b0f14}
  </style>
</head>
<body>
<header>
  <h1>LOGOS LRB — исследователь</h1>
  <div class="pill">
    <input id="q" placeholder="Поиск: RID, высота блока или псевдо-txid from:nonce" style="min-width:260px">
    <button onclick="search()">Найти</button>
  </div>
  <div id="jsStat">js: загрузка…</div>
</header>

<main>

  <section class="cards">
    <div>
      <h3>Голова</h3>
      <div class="btns">
        <button onclick="fetchHead()">GET /head</button>
        <button onclick="toggleAuto()">Автообновление</button>
      </div>
      <pre id="out-head"></pre>
    </div>
    <div>
      <h3>Эконом</h3>
      <button onclick="fetchEconomy()">GET /economy</button>
      <pre id="out-economy"></pre>
    </div>
  </section>

  <section>
    <h3>Блок</h3>
    <div class="row">
      <div class="grow"><label class="muted">высота блока</label><input id="inp-height" type="number" min="1" placeholder="например 1"></div>
      <div class="grow btns" style="align-items:flex-end">
        <button onclick="fetchBlock()">/block/:height</button>
        <button onclick="fetchMix()">/block/:height/mix</button>
        <button onclick="loadLatest()">Последние блоки</button>
      </div>
    </div>
    <div class="table-wrap" id="latest-wrap" style="display:none">
      <table><thead><tr><th>height</th><th>ts</th><th>finalized</th></tr></thead><tbody id="latest"></tbody></table>
    </div>
    <pre id="out-block"></pre>
  </section>

  <section>
    <h3>Адрес (RID)</h3>
    <div class="row">
      <div class="grow"><label class="muted">RID (base58)</label><input id="inp-rid" placeholder="вставь RID"></div>
      <div class="fit"><label class="muted">limit</label><input id="inp-limit" type="number" min="1" value="20"></div>
      <div class="grow btns" style="align-items:flex-end"><button onclick="fetchHistory()">GET /history</button></div>
    </div>
    <div class="table-wrap">
      <table id="tbl">
        <thead><tr><th>nonce</th><th>from</th><th>to</th><th>amount</th><th>height</th><th>ts</th></tr></thead>
        <tbody id="hist-body"></tbody>
      </table>
    </div>
    <pre id="out-history" style="display:none"></pre>
  </section>

</main>

<script>
(function(){
  const API = location.origin + "/api";
  const $  = s => document.querySelector(s);
  const setStat = (t,ok)=>{ const s=$("#jsStat"); if(!s) return; s.textContent=t; s.style.color=ok?"#0bd464":"#ff5252"; };
  const fmtNum=n=>Number(n).toLocaleString("ru-RU");
  const fmtTs =ms=>isFinite(ms)?new Date(Number(ms)).toLocaleString("ru-RU"):"";

  async function jget(path){
    try{ const r=await fetch(API+path,{cache:"no-store"}); if(!r.ok) return {error:r.status+" "+(await r.text()).slice(0,200)}; return await r.json(); }
    catch(e){ return {error:String(e)}; }
  }

  // HEAD & ECON
  let autoTimer=null;
  window.fetchHead = async ()=>{ $("#out-head").textContent = JSON.stringify(await jget("/head"), null, 2); };
  window.fetchEconomy = async ()=>{ $("#out-economy").textContent = JSON.stringify(await jget("/economy"), null, 2); };
  window.toggleAuto = ()=>{
    if(autoTimer){ clearInterval(autoTimer); autoTimer=null; setStat("js: авто выкл", true); return; }
    const tick=async()=>{ await fetchHead(); await fetchEconomy(); };
    tick(); autoTimer=setInterval(tick, 5000); setStat("js: авто вкл", true);
  };

  // BLOCKS
  window.fetchBlock = async ()=>{
    const h=Number($("#inp-height").value)||0; if(!h){ alert("Укажи высоту"); return; }
    $("#out-block").textContent = JSON.stringify(await jget("/block/"+h), null, 2);
    $("#latest-wrap").style.display="none";
  };
  window.fetchMix = async ()=>{
    const h=Number($("#inp-height").value)||0; if(!h){ alert("Укажи высоту"); return; }
    $("#out-block").textContent = JSON.stringify(await jget(`/block/${h}/mix`), null, 2);
    $("#latest-wrap").style.display="none";
  };
  window.loadLatest = async ()=>{
    const head=await jget("/head");
    const H = head && head.height ? Number(head.height) : 0;
    const tbody=$("#latest"); tbody.innerHTML="";
    if(!H){ $("#latest-wrap").style.display="none"; return; }
    const from=Math.max(1,H-9);  // последние 10
    for(let h=H; h>=from; h--){
      const b = await jget("/block/"+h);
      const tr=document.createElement("tr");
      tr.innerHTML = `<td>${h}</td><td>${b.ts_ms?fmtTs(b.ts_ms):""}</td><td>${b.finalized??""}</td>`;
      tbody.appendChild(tr);
    }
    $("#latest-wrap").style.display="block";
    $("#out-block").textContent = "";
  };

  // HISTORY
  function renderRows(arr){
    const tb=$("#hist-body"); tb.innerHTML="";
    if(!arr || arr.length===0){ const tr=document.createElement("tr"); tr.innerHTML='<td colspan="6" class="muted">0 записей</td>'; tb.appendChild(tr); return; }
    for(const tx of arr){
      const tr=document.createElement("tr");
      tr.innerHTML = `<td>${tx.nonce??""}</td><td>${tx.from??""}</td><td>${tx.to??""}</td>`+
                     `<td>${fmtNum(tx.amount??0)}</td><td>${tx.height??""}</td><td>${fmtTs(tx.ts_ms)}</td>`;
      tb.appendChild(tr);
    }
  }
  window.fetchHistory = async ()=>{
    const rid = ($("#inp-rid").value||"").trim(); if(!rid){ alert("Укажи RID"); return; }
    const lim = Math.max(1, Number($("#inp-limit").value)||20);
    const raw = await jget(`/history/${encodeURIComponent(rid)}?limit=${lim}`);
    $("#out-history").style.display="block"; $("#out-history").textContent=JSON.stringify(raw,null,2);
    const arr = (raw && (raw.items||raw.txs)) ? (raw.items||raw.txs) : [];
    renderRows(arr);
  };

  // SEARCH (RID / block height / pseudo txid "from:nonce")
  window.search = async ()=>{
    const q = ($("#q").value||"").trim();
    if(!q) return;
    if(/^\d+$/.test(q)){ $("#inp-height").value=q; await fetchBlock(); return; }
    if(/^[1-9A-HJ-NP-Za-km-z]+$/.test(q) && q.length>30){ $("#inp-rid").value=q; await fetchHistory(); return; }
    if(q.includes(":")){ // псевдо-txid from:nonce
      const [from,nonce] = q.split(":");
      $("#inp-rid").value = from;
      $("#inp-limit").value = 50;
      await fetchHistory();
      // подсветим найденную строку
      [...document.querySelectorAll("#hist-body tr")].forEach(tr=>{
        if(tr.firstChild && tr.firstChild.textContent===(nonce||"").trim()){ tr.style.background="#132235"; }
      });
      return;
    }
    alert("Не распознан формат запроса. Используй: RID, номер блока, или from:nonce");
  };

  // boot mark
  setStat("js: готов", true);
})();
</script>
</body>
</html>

```

### FILE: /var/www/logos/landing/i18n/de.json
```
{
  "nav_about":"Über",
  "nav_tech":"Technologie",
  "nav_token":"Token",
  "nav_stake":"Staking",
  "nav_comm":"Community",

  "badge_main":"L1 • 81M LGN • Anonym • Deflationär • Quantenresistent",
  "hero_title":"Lebendige Resonanz‑Blockchain für die nächste Ära.",
  "hero_sub":"LOGOS ist eine Resonanz‑L1‑Blockchain. Unser erster Schritt in Richtung Web4 – ein Netzwerk, in dem Menschen, Wert und KI denselben sicheren Raum teilen.",
  "btn_learn_more":"Mehr erfahren",
  "btn_download_apk":"Sichere APK herunterladen",
  "meta_supply":"Gesamtangebot: 81 000 000 LGN",
  "meta_ready":"Für echten Nutzen und Massenadoption gebaut",

  "about_title":"Was ist LOGOS?",
  "about_text":"LOGOS ist eine resonanzgetriebene L1‑Blockchain mit dem RSP‑Sicherheitsprotokoll im Kern. Ziel ist ein Netzwerk, das reale Last trägt, Privatsphäre respektiert und bereit für Web4‑Produkte ist – von Payments bis KI‑Services.",
  "card1_title":"Resonanzkern",
  "card1_text":"Das RSP‑Protokoll und Phasenfilter halten das Netzwerk selbst bei Aktivitätsspitzen stabil.",
  "card2_title":"Echte Privatsphäre",
  "card2_text":"Minimale Metadaten, strikte Nonce‑Policy, Phasenmischung des Traffics und integrierter Schutz vor Spam und Angriffen.",
  "card3_title":"Produktionsreif",
  "card3_text":"Rust‑Kern, Axum REST, Prometheus/Grafana, Bridge‑Journal, Health‑Checks und Archiv – alles, was eine ernsthafte L1‑Chain braucht.",

  "tech_title":"LOGOS‑Technologie",
  "tech_item1":"Lebendiges Resonanz‑Protokoll: das Netzwerk reagiert auf Last und Anomalien und bleibt dabei vorhersagbar.",
  "tech_item2":"RSP‑Sicherheitsprotokoll: beobachtet Spam‑Wellen, Zensurversuche und ungewöhnliche Wertströme und begrenzt schädliche Aktivität gezielt.",
  "tech_item3":"Grundlage für KI und Agenten: LOGOS ist als Umgebung für autonome Agenten und zukünftige AGI entworfen – mit Risikomanagement ohne unnötige Datenausleitung.",
  "tech_item4":"Stark innen, einfach außen: Nutzer sehen Wallet, Transfers und Staking – die Komplexität steckt im Protokoll.",
  "tech_item5":"Web4‑Ökosystem: Produkte auf LOGOS – Payments, Games, DeFi und KI‑Services – erhalten Privatsphäre und Resilienz direkt aus der Basis.",
  "tech_note":"LOGOS will ein Fundament für das nächste Internet (Web4) sein, in dem Menschen, Wert und KI in einem stabilen, privaten Netzwerk koordiniert werden.",

  "token_title":"LGN‑Tokenomics",
  "token_text":"LGN ist der Basistoken von LOGOS. Fixes Angebot von 81 000 000 LGN mit deflationärem Modell und Fokus auf langfristige Teilnehmer.",
  "token_staking":"Staking & Holder",
  "token_rcp":"RSP‑Sicherheitsprotokoll",
  "token_liq":"Liquidität (DEX/CEX)",
  "token_stab":"Stabilisierungsfonds",
  "token_core":"Founder & Core Dev",
  "token_airdrop":"Airdrop & DAO",

  "stake_title":"Staking & RSP‑Protokoll",
  "stake_text":"LGN‑Staking verbindet Netzwerksicherheit und das RSP‑Protokoll mit langfristigen Anreizen für Holder.",
  "stake_item1_title":"Basis‑Staking",
  "stake_item1_text":"Du delegierst LGN an Validatoren und erhältst Rewards für die Sicherung des Netzwerks.",
  "stake_item2_title":"RSP‑Protokoll",
  "stake_item2_text":"Eine Sicherheitsschicht, die Netzwerkphase und Teilnehmerverhalten berücksichtigt und Staking sowie Ökonomie verstärkt.",
  "stake_item3_title":"Missionen & Rewards",
  "stake_item3_text":"On‑Chain‑Aktivität, Community‑Quests und Airdrop‑Mechaniken oben auf dem Basis‑Staking.",

  "comm_title":"Community & Kanäle",
  "comm_text":"Tritt dem Feld bei: Updates, Airdrops, Missionen, Staking und AI‑native Experimente.",
  "comm_email":"Email: simbiotai@proton.me",
  "comm_staking":"LGN‑Staking",

  "footer_note":"Resonanz‑Blockchain • Für Millionen Nutzer gebaut"
}

```

### FILE: /var/www/logos/landing/i18n/en.json
```
{
  "nav_about":"About",
  "nav_tech":"Technology",
  "nav_token":"Token",
  "nav_stake":"Staking",
  "nav_comm":"Community",

  "badge_main":"L1 • 81M LGN • Anonymous • Deflationary • Quantum‑resistant",
  "hero_title":"Living resonance blockchain for the next era.",
  "hero_sub":"LOGOS is a resonance‑based L1 blockchain. It is our first step towards Web4 – a network where people, value and AI share the same secure space.",
  "btn_learn_more":"Learn more",
  "btn_download_apk":"Download secure APK",
  "meta_supply":"Total supply: 81 000 000 LGN",
  "meta_ready":"Built for real utility & mass adoption",

  "about_title":"What is LOGOS?",
  "about_text":"LOGOS is a resonance‑driven L1 blockchain built around the RSP security protocol. We focus on a network that can handle real traffic, respects privacy and is ready for Web4‑native products – from payments to AI services.",
  "card1_title":"Resonant core",
  "card1_text":"The RSP protocol and phase filters keep the network stable even during sharp activity spikes.",
  "card2_title":"Real privacy",
  "card2_text":"Minimal metadata, strict nonce policy, phase‑mixed traffic and built‑in protection against spam and attacks.",
  "card3_title":"Production‑grade",
  "card3_text":"Rust core, Axum REST, Prometheus/Grafana, bridge journal, health checks and archive – everything a serious L1 needs.",

  "tech_title":"LOGOS technology",
  "tech_item1":"Living resonance protocol: the network reacts to load and anomalies while keeping finalisation and behaviour predictable.",
  "tech_item2":"RSP security protocol: observes spam waves, censorship attempts and abnormal value flows, gently limiting harmful activity.",
  "tech_item3":"Base layer for AI and agents: LOGOS is designed as an environment where autonomous agents and future AGI can manage risk and capital without leaking unnecessary data.",
  "tech_item4":"Strong internals, simple outside: users see a wallet, transfers and staking – the complexity lives inside the protocol.",
  "tech_item5":"Web4 ecosystem: products on top of LOGOS – payments, games, DeFi and AI services – get privacy and resilience from the base layer.",
  "tech_note":"LOGOS aims to be a foundation for the next internet (Web4), where people, value and AI coordinate inside one stable, private network.",

  "token_title":"LGN tokenomics",
  "token_text":"LGN is the base token of LOGOS. Fixed supply of 81 000 000 LGN with a deflationary model focused on long‑term participants.",
  "token_staking":"Staking & holders",
  "token_rcp":"RSP security protocol",
  "token_liq":"Liquidity (DEX/CEX)",
  "token_stab":"Stability fund",
  "token_core":"Founder & core dev",
  "token_airdrop":"Airdrop & DAO",

  "stake_title":"Staking & RSP protocol",
  "stake_text":"Staking LGN ties network security and the RSP protocol to long‑term incentives for holders.",
  "stake_item1_title":"Base staking",
  "stake_item1_text":"Delegate LGN to validators and receive rewards for helping secure the network.",
  "stake_item2_title":"RSP protocol",
  "stake_item2_text":"A security layer that takes network phase and participant behaviour into account, reinforcing staking and the whole economy.",
  "stake_item3_title":"Missions & rewards",
  "stake_item3_text":"On‑chain activity, community quests and airdrop mechanics built on top of base staking.",

  "comm_title":"Community & channels",
  "comm_text":"Join the field: updates, airdrop campaigns, missions, staking and AI‑native experiments.",
  "comm_email":"Email: simbiotai@proton.me",
  "comm_staking":"LGN staking",

  "footer_note":"Resonance blockchain • Built for millions of users"
}

```

### FILE: /var/www/logos/landing/i18n/ru.json
```
{
  "nav_about":"О проекте",
  "nav_tech":"Технология",
  "nav_token":"Токен",
  "nav_stake":"Стейкинг",
  "nav_comm":"Сообщество",

  "badge_main":"L1 • 81M LGN • Анонимность • Дефляция • Квантовая устойчивость",
  "hero_title":"Живой резонансный блокчейн нового уровня.",
  "hero_sub":"LOGOS — резонансный L1‑блокчейн следующего поколения. Мы делаем первый шаг к Web4: сети, где люди, ценность и ИИ работают в одном защищённом пространстве.",
  "btn_learn_more":"Подробнее",
  "btn_download_apk":"Скачать безопасный APK",
  "meta_supply":"Общая эмиссия: 81 000 000 LGN",
  "meta_ready":"Создан для реальной пользы и массового использования",

  "about_title":"Что такое LOGOS",
  "about_text":"LOGOS — резонансный L1‑блокчейн с RSP‑протоколом безопасности. Мы делаем сеть, которая выдерживает реальную нагрузку, бережно относится к приватности и готова к Web4‑продуктам — от платёжных систем до ИИ‑сервисов.",
  "card1_title":"Резонансное ядро",
  "card1_text":"RSP‑протокол и фазовые фильтры удерживают сеть стабильной даже при резких всплесках активности.",
  "card2_title":"Реальная приватность",
  "card2_text":"Минимум метаданных, строгая nonce‑политика, фазовое смешение трафика и встроенная защита от спама и атак.",
  "card3_title":"Боевой уровень",
  "card3_text":"Rust‑ядро, Axum REST, Prometheus/Grafana, журнал моста, health‑проверки и архив — всё, что нужно серьёзной L1‑сети.",

  "tech_title":"Технология LOGOS",
  "tech_item1":"Живой резонансный протокол: сеть реагирует на нагрузку и аномалии, сохраняя предсказуемость и финализацию блоков.",
  "tech_item2":"RSP‑протокол безопасности: отслеживает всплески спама, попытки цензуры и странные потоки средств, мягко ограничивая вредную активность.",
  "tech_item3":"База для ИИ и агентов: LOGOS проектируется как среда, где автономные агенты и будущая AGI‑архитектура управляют рисками и капиталом без лишней утечки данных.",
  "tech_item4":"Сильное ядро, простая внешняя оболочка: пользователю доступны кошелёк, переводы и стейкинг, вся сложность спрятана внутри протокола.",
  "tech_item5":"Экосистема Web4: поверх LOGOS растут продукты — платёжные сценарии, игры, DeFi и AI‑сервисы, которым важны приватность и отказоустойчивость.",
  "tech_note":"LOGOS — фундамент для следующего интернета (Web4), где люди, ценность и ИИ координируются в одной устойчивой и приватной сети.",

  "token_title":"LGN: токеномика",
  "token_text":"LGN — базовый токен LOGOS. Общая эмиссия 81 000 000 LGN. Модель — дефляционная, с акцентом на долгосрочных держателей и участников сети.",
  "token_staking":"Staking / Holders",
  "token_rcp":"RSP‑протокол безопасности",
  "token_liq":"Ликвидность (DEX/CEX)",
  "token_stab":"Фонд стабильности",
  "token_core":"Создатель / Core Dev",
  "token_airdrop":"Airdrop / DAO",

  "stake_title":"Стейкинг и RSP‑протокол",
  "stake_text":"Стейкинг LGN связывает безопасность сети и RSP‑протокол с долгосрочными стимулами для держателей.",
  "stake_item1_title":"Базовый стейкинг",
  "stake_item1_text":"Делегируешь LGN валидаторам и получаешь вознаграждение за участие в защите сети.",
  "stake_item2_title":"RSP‑протокол",
  "stake_item2_text":"Уровень безопасности, который учитывает фазу сети и поведение участников, усиливая защиту стейкинга и всей экономики.",
  "stake_item3_title":"Миссии и награды",
  "stake_item3_text":"On‑chain‑активности, задания для сообщества и airdrop‑механики поверх базового стейкинга.",

  "comm_title":"Сообщество и каналы",
  "comm_text":"Присоединяйся: обновления, airdrop‑кампании, миссии, стейкинг и эксперименты с AI‑нативными протоколами.",
  "comm_email":"Email: simbiotai@proton.me",
  "comm_staking":"Стейкинг LGN",

  "footer_note":"Resonance Blockchain • Готов к миллионам пользователей"
}

```

### FILE: /var/www/logos/landing/index.html
```
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <title>LOGOS — Resonance Blockchain</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="LOGOS — L1-блокчейн нового поколения на резонансной архитектуре: скорость, приватность, низкие комиссии и устойчивость под нагрузкой для миллионов пользователей." />
  <link rel="stylesheet" href="styles.v20251124.css" />
  <style>
    :root{
      --bg:#05030b;
      --fg:#f5f0ff;
      --muted:#b9afd4;
      --accent:#a96bff;
      --accent-soft:rgba(169,107,255,0.16);
      --card:#0d0718;
      --card-soft:rgba(255,255,255,0.04);
    }

    *{box-sizing:border-box}
    html,body{
      margin:0;
      padding:0;
      background:var(--bg);
      color:var(--fg);
      font-family:system-ui,-apple-system,"Inter",sans-serif;
    }
    a{text-decoration:none;color:inherit}

    .bg-layer{
      position:fixed;
      inset:0;
      z-index:-1;
      background:
        radial-gradient(1200px 600px at 15% 10%, rgba(169,107,255,.16), transparent 60%),
        radial-gradient(900px 500px at 85% 90%, rgba(90,60,170,.16), transparent 60%);
      pointer-events:none;
    }

    .page{
      max-width:960px;
      margin:0 auto;
      padding:24px 16px 72px;
    }

    @media (min-width:768px){
      .page{padding:32px 24px 80px;}
    }

    /* Topbar + гамбургер */

    header.topbar{
      position:relative;
      z-index:30;
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:16px;
      margin-bottom:32px;
    }

    .topbar__left{
      display:flex;
      flex-direction:column;
      gap:2px;
    }
    .logo{
      font-weight:700;
      letter-spacing:0.14em;
      font-size:14px;
      text-transform:uppercase;
    }
    .logo-sub{
      font-size:12px;
      color:var(--muted);
    }

    .topbar__right{
      position:relative;
      display:flex;
      align-items:center;
      gap:10px;
    }

    .topbar__lang button{
      border:none;
      background:transparent;
      color:#d0c8f0;
      font-size:11px;
      text-transform:uppercase;
      letter-spacing:.12em;
      padding:2px 4px;
      cursor:pointer;
    }

    .topbar__lang button.is-active{
      font-weight:600;
      border-bottom:1px solid rgba(255,255,255,.7);
    }

    .topbar__menu-toggle{
      display:none;
    }

    .topbar__burger{
      width:32px;
      height:32px;
      border-radius:999px;
      border:1px solid rgba(255,255,255,.24);
      background:rgba(6,4,18,.9);
      display:inline-flex;
      align-items:center;
      justify-content:center;
      flex-direction:column;
      gap:3px;
      cursor:pointer;
    }

    .topbar__burger span{
      width:14px;
      height:1.6px;
      border-radius:999px;
      background:#f5f0ff;
    }

    .topbar__menu{
      position:absolute;
      top:120%;
      right:0;
      min-width:220px;
      max-width:260px;
      background:rgba(6,4,18,.97);
      border-radius:16px;
      border:1px solid rgba(255,255,255,.14);
      box-shadow:0 18px 50px rgba(0,0,0,.8);
      padding:10px 10px 8px;
      opacity:0;
      transform:translateY(-6px);
      pointer-events:none;
      transition:opacity .18s ease, transform .18s ease;
    }

    .topbar__menu-list{
      list-style:none;
      margin:0;
      padding:0;
      display:flex;
      flex-direction:column;
      gap:2px;
      font-size:13px;
    }

    .topbar__menu-link{
      display:flex;
      align-items:center;
      justify-content:space-between;
      padding:7px 8px;
      border-radius:10px;
      color:#f5f0ff;
      text-decoration:none;
      gap:8px;
    }

    .topbar__menu-link span:last-child{
      font-size:11px;
      color:#b9afd4;
      white-space:nowrap;
    }

    .topbar__menu-link:hover{
      background:rgba(169,107,255,.22);
    }

    .topbar__menu-sep{
      border:none;
      border-top:1px solid rgba(255,255,255,.12);
      margin:6px 0;
    }

    .topbar__menu-toggle:checked + label.topbar__burger + .topbar__menu{
      opacity:1;
      transform:translateY(0);
      pointer-events:auto;
    }

    /* Основной контент */

    main{
      display:flex;
      flex-direction:column;
      gap:32px;
    }

    .hero{
      padding:24px 20px;
      border-radius:28px;
      background:linear-gradient(145deg,rgba(10,5,30,.96),rgba(8,3,25,.98));
      box-shadow:0 18px 45px rgba(0,0,0,.65);
    }

    .hero-badge{
      display:inline-flex;
      align-items:center;
      gap:8px;
      padding:6px 12px;
      border-radius:999px;
      background:rgba(255,255,255,.03);
      border:1px solid rgba(255,255,255,.12);
      font-size:12px;
      color:var(--muted);
      margin-bottom:16px;
    }
    .hero-badge span.dot{
      height:4px;
      width:4px;
      border-radius:999px;
      background:var(--accent);
    }

    .hero-title{
      font-size:26px;
      line-height:1.25;
      margin:0 0 12px;
    }

    .hero-sub{
      margin:0 0 14px;
      color:var(--muted);
      font-size:14px;
      max-width:640px;
    }

    .hero-actions{
      display:flex;
      flex-wrap:wrap;
      gap:10px;
      margin-top:16px;
    }

    .hero-meta{
      margin-top:14px;
      display:flex;
      flex-wrap:wrap;
      gap:10px;
      font-size:12px;
      color:var(--muted);
    }

    @media (min-width:768px){
      .hero-title{font-size:30px;}
    }

    .section{
      padding:20px 18px;
      border-radius:22px;
      background:rgba(9,4,22,.96);
      border:1px solid rgba(255,255,255,.06);
    }
    .section--alt{
      background:rgba(5,3,14,.96);
    }

    .section__title{
      font-size:20px;
      margin:0 0 8px;
    }

    .section__lead{
      margin:0 0 16px;
      font-size:14px;
      color:var(--muted);
    }

    .section__list{
      margin:0;
      padding-left:18px;
      font-size:14px;
      color:var(--muted);
    }

    .section__list li{
      margin-bottom:4px;
    }

    .cards{
      display:grid;
      grid-template-columns:1fr;
      gap:10px;
    }
    @media (min-width:720px){
      .cards{grid-template-columns:repeat(3,minmax(0,1fr));}
    }

    .card{
      padding:12px 12px;
      border-radius:16px;
      background:var(--card-soft);
      border:1px solid rgba(255,255,255,.08);
    }
    .card-title{
      font-weight:600;
      margin-bottom:4px;
      font-size:14px;
    }
    .card-text{
      margin:0;
      font-size:13px;
      color:var(--muted);
    }

    .airdrop-block{
      margin-top:12px;
      padding:12px 12px;
      border-radius:16px;
      background:rgba(16,10,40,.95);
      border:1px solid rgba(255,255,255,.08);
    }
    .airdrop-block__title{
      font-weight:600;
      margin:0 0 8px;
      font-size:14px;
    }
    .airdrop-block__list{
      margin:0 0 12px;
      padding-left:18px;
      font-size:13px;
      color:var(--muted);
    }

    .pill-row{
      display:flex;
      flex-wrap:wrap;
      gap:8px;
      margin-top:10px;
    }

    .pill-link{
      padding:6px 14px;
      border-radius:999px;
      border:1px solid rgba(255,255,255,.18);
      font-size:13px;
      color:var(--muted);
      cursor:pointer;
      background:rgba(7,4,20,.85);
      backdrop-filter:blur(12px);
      transition:background .15s,border-color .15s,color .15s,transform .1s;
    }

    .pill-link:hover{
      background:var(--accent-soft);
      border-color:var(--accent);
      color:var(--fg);
      transform:translateY(-1px);
    }

    .btn{
      border-radius:999px;
      padding:9px 18px;
      font-size:14px;
      border:1px solid rgba(255,255,255,.18);
      background:rgba(11,7,32,.95);
      color:#f5f0ff;
      cursor:pointer;
      display:inline-flex;
      align-items:center;
      gap:8px;
    }
    .btn--primary{
      background:linear-gradient(135deg,#ff7ae0,#a96bff);
      border:none;
      color:#1a102b;
      font-weight:600;
    }
    .btn--ghost{
      background:transparent;
      border-color:rgba(255,255,255,.32);
    }

    .footer{
      margin-top:26px;
      font-size:12px;
      color:var(--muted);
      display:flex;
      flex-wrap:wrap;
      gap:8px;
      justify-content:space-between;
      align-items:center;
      padding:6px 4px 0;
      border-top:1px solid rgba(255,255,255,.08);
    }

  </style>
</head>
<body>
  <div class="bg-layer"></div>

  <div class="page">
    <header class="topbar">
      <div class="topbar__left">
        <div class="logo">LOGOS</div>
        <div class="logo-sub">Resonance Blockchain</div>
      </div>
      <div class="topbar__right">
        <div class="topbar__lang">
          <button type="button" data-lang-btn="ru" class="is-active">RU</button>
          <button type="button" data-lang-btn="en">EN</button>
          <button type="button" data-lang-btn="de">DE</button>
        </div>

        <input type="checkbox" id="topbar-menu-toggle" class="topbar__menu-toggle" />
        <label for="topbar-menu-toggle" class="topbar__burger" aria-label="Menu">
          <span></span><span></span><span></span>
        </label>

        <div class="topbar__menu">
          <ul class="topbar__menu-list">
            <li>
              <a href="#intro" class="topbar__menu-link">
                <span data-i18n="nav_intro">Обзор</span>
              </a>
            </li>
            <li>
              <a href="#speed" class="topbar__menu-link">
                <span data-i18n="nav_speed">Скорость</span>
              </a>
            </li>
            <li>
              <a href="#privacy" class="topbar__menu-link">
                <span data-i18n="nav_privacy">Приватность</span>
              </a>
            </li>
            <li>
              <a href="#fees" class="topbar__menu-link">
                <span data-i18n="nav_fees">Комиссии</span>
              </a>
            </li>
            <li>
              <a href="#reliability" class="topbar__menu-link">
                <span data-i18n="nav_reliability">Надёжность</span>
              </a>
            </li>
            <li>
              <a href="#tech" class="topbar__menu-link">
                <span data-i18n="nav_tech">Технология</span>
              </a>
            </li>
            <li>
              <a href="#rsp" class="topbar__menu-link">
                <span data-i18n="nav_rsp">LOGOS RSP</span>
              </a>
            </li>
            <li>
              <a href="#agi" class="topbar__menu-link">
                <span data-i18n="nav_agi">LOGOS‑AGI</span>
              </a>
            </li>
            <li>
              <a href="#better" class="topbar__menu-link">
                <span data-i18n="nav_better">Преимущества</span>
              </a>
            </li>
            <li>
              <a href="#short" class="topbar__menu-link">
                <span data-i18n="nav_short">В двух словах</span>
              </a>
            </li>
            <li>
              <a href="#community" class="topbar__menu-link">
                <span data-i18n="nav_comm">Сообщество</span>
              </a>
            </li>

            <li><hr class="topbar__menu-sep" /></li>

            <li>
              <a href="mailto:simbiotai@proton.me?subject=LOGOS%20Presale%20Seed" class="topbar__menu-link">
                <span data-i18n="menu_presale">Presale / Seed</span>
                <span>simbiotai@proton.me</span>
              </a>
            </li>
            <li>
              <a href="https://mw-expedition.com/staking" class="topbar__menu-link">
                <span data-i18n="menu_staking">Стейкинг LGN</span>
                <span>mainnet</span>
              </a>
            </li>
            <li>
              <a href="/airdrop.html" class="topbar__menu-link">
                <span data-i18n="menu_airdrop">Airdrop</span>
                <span data-i18n="menu_airdrop_sub">задания и прогресс</span>
              </a>
            </li>

            <li><hr class="topbar__menu-sep" /></li>

            <li>
              <a href="https://mw-expedition.com/wallet" class="topbar__menu-link">
                <span>Web Wallet</span>
                <span>beta</span>
              </a>
            </li>
            <li>
              <a href="https://mw-expedition.com/explorer" class="topbar__menu-link">
                <span>Explorer</span>
                <span>chain view</span>
              </a>
            </li>

            <li><hr class="topbar__menu-sep" /></li>

            <li>
              <a href="https://t.me/logosblockchain" target="_blank" rel="noopener" class="topbar__menu-link">
                <span data-i18n="menu_telegram">Telegram</span>
                <span>@logosblockchain</span>
              </a>
            </li>
            <li>
              <a href="https://x.com/RspLogos" target="_blank" rel="noopener" class="topbar__menu-link">
                <span data-i18n="menu_twitter">X (Twitter)</span>
                <span>@OfficiaLogosLRB</span>
              </a>
            </li>
            <li>
              <a href="https://t.me/logosblockchain" target="_blank" rel="noopener" class="topbar__menu-link">
                <span>Airdrop bot</span>
                <span>@Logos_lrb_bot</span>
              </a>
            </li>
          </ul>
        </div>
      </div>
    </header>

    <main>
      <!-- HERO -->
      <section id="intro" class="hero">
        <div class="hero-badge">
          <span class="dot"></span>
          <span data-i18n="badge_main">L1 • 81M LGN • Анонимность • Дефляция • Квантовая устойчивость</span>
        </div>
        <h1 class="hero-title" data-i18n="intro_title">
          LOGOS — блокчейн нового поколения на резонансной архитектуре
        </h1>
        <p class="hero-sub" data-i18n="intro_p1">
          LOGOS — резонансный L1‑блокчейн следующего поколения. Мы делаем первый шаг к Web4: сети, где люди, ценность и ИИ работают в одном защищённом пространстве.
        </p>
        <p class="hero-sub" data-i18n="intro_p2">
          Сеть уже выдерживает реальную нагрузку, сохраняет приватность и остаётся простой в эксплуатации. Никаких лишних усложнений — только ядро, рассчитанное на миллионы пользователей.
        </p>
        <p class="hero-sub" data-i18n="intro_p3">
          LOGOS — это фундамент для новой цифровой среды: платежи, стейкинг, общение и резонансные протоколы поверх одной устойчивой L1.
        </p>
        <div class="hero-actions">
          <a href="#about" class="btn btn--primary" data-i18n="btn_learn_more">Подробнее</a>
          <a href="/apk/app-20250830_1442.apk" class="btn btn--ghost" data-i18n="btn_download_apk">Скачать безопасный APK</a>
        </div>
        <div class="hero-meta">
          <span data-i18n="meta_supply">Общая эмиссия: 81 000 000 LGN</span>
          <span data-i18n="meta_ready">Создан для реальной пользы и массового использования</span>
        </div>
      </section>

      <!-- About -->
      <section id="about" class="section">
        <h2 class="section__title" data-i18n="about_title">Что такое LOGOS</h2>
        <p class="section__lead" data-i18n="about_text">
          LOGOS — L1‑блокчейн на резонансной архитектуре. В основе — Σ(t), фазовые фильтры и анти‑спам механизмы, которые держат сеть стабильной даже под высокой нагрузкой.
        </p>
        <div class="cards">
          <article class="card">
            <h3 class="card-title" data-i18n="card1_title">Резонансное ядро</h3>
            <p class="card-text" data-i18n="card1_text">
              Σ(t), Λ и фазовые фильтры обеспечивают устойчивое поведение сети.
            </p>
          </article>
          <article class="card">
            <h3 class="card-title" data-i18n="card2_title">Реальная приватность</h3>
            <p class="card-text" data-i18n="card2_text">
              Минимум метаданных, строгая nonce‑политика и phase‑mixing на входе.
            </p>
          </article>
          <article class="card">
            <h3 class="card-title" data-i18n="card3_title">Production‑уровень</h3>
            <p class="card-text" data-i18n="card3_text">
              Rust‑ядро, Axum REST, Prometheus/Grafana, bridge‑журнал, health‑ручки.
            </p>
          </article>
        </div>
      </section>

      <!-- Speed -->
      <section id="speed" class="section">
        <h2 class="section__title" data-i18n="speed_title">Скорость и производительность</h2>
        <p class="section__lead" data-i18n="speed_p">
          Сеть тестировалась под реальной нагрузкой, а не на слайдах: пики ~2000+ транзакций в секунду с устойчивой финализацией и без форков. Архитектура заложена так, чтобы масштабироваться дальше — при росте числа узлов и оптимизации фаз возможно достижение 10 000+ tx/s без жертв по стабильности.
        </p>
      </section>

      <!-- Privacy -->
      <section id="privacy" class="section section--alt">
        <h2 class="section__title" data-i18n="privacy_title">Приватность нового уровня</h2>
        <p class="section__lead" data-i18n="privacy_p1">
          С первого дня LOGOS проектировался как сеть, где:
        </p>
        <ul class="section__list">
          <li data-i18n="privacy_li1">пользователя нельзя напрямую связать с транзакцией;</li>
          <li data-i18n="privacy_li2">маршруты пакетов трудно трассировать;</li>
          <li data-i18n="privacy_li3">утечки метаданных минимальны;</li>
          <li data-i18n="privacy_li4">нет очевидных сетевых отпечатков;</li>
          <li data-i18n="privacy_li5">нет стандартных точек трекинга.</li>
        </ul>
        <p class="section__lead" data-i18n="privacy_p2">
          Приватность в LOGOS — не опция и не галочка в интерфейсе. Она встроена в архитектуру.
        </p>
      </section>

      <!-- Fees -->
      <section id="fees" class="section">
        <h2 class="section__title" data-i18n="fees_title">Низкие комиссии и чистая финализация</h2>
        <p class="section__lead" data-i18n="fees_p">
          Блоки не конкурируют, не конфликтуют и не откатываются. Транзакция проходит один раз и записывается навсегда. Комиссии остаются одними из самых низких среди L1, потому что мы избегаем тяжёлых вычислений и раздутых контрактов — даже под нагрузкой базовые переводы остаются доступными.
        </p>
      </section>

      <!-- Reliability -->
      <section id="reliability" class="section section--alt">
        <h2 class="section__title" data-i18n="reliability_title">Надёжность и готовность к продакшену</h2>
        <p class="section__lead" data-i18n="reliability_p">
          Узлы LOGOS легко разворачиваются и обновляются, мосты работают с устойчивым журналом, есть стейкинг‑обвязки, архивирование и метрики. Узлы могут жить на обычных серверах, а инфраструктура уже выдержала стресс‑тесты под высокой нагрузкой.
        </p>
      </section>

      <!-- Technology -->
      <section id="tech" class="section">
        <h2 class="section__title" data-i18n="technology_title">Технология LOGOS</h2>
        <p class="section__lead" data-i18n="technology_p">
          В основе LOGOS — резонансно‑символическая архитектура: собственный способ организации данных и синхронизации. Вместо тяжёлого консенсуса и сложных схем — ритмы, структура и фазовая динамика. Это делает сеть устойчивой к нагрузке, быстрой в реакции на всплески и сложной для атак на сетевом уровне, при этом масштабирование остаётся прямолинейным.
        </p>
      </section>

      <!-- RSP -->
      <section id="rsp" class="section section--alt">
        <h2 class="section__title" data-i18n="rsp_title">LOGOS RSP — коммуникация без следов</h2>
        <p class="section__lead" data-i18n="rsp_p">
          В ядре экосистемы — протокол конфиденциальной коммуникации LOGOS RSP. На практике это общение без классического IP‑маршрутизации и с минимальными цифровыми следами, устойчивое к перехвату и анализу. RSP может работать не только поверх интернета, но и через альтернативные носители — свет, звук, радио и оффлайн‑каналы.
        </p>
      </section>

      <!-- AGI -->
      <section id="agi" class="section">
        <h2 class="section__title" data-i18n="agi_title">LOGOS‑AGI — новый архитектурный слой</h2>
        <p class="section__lead" data-i18n="agi_p">
          Параллельно мы развиваем направление LOGOS‑AGI — другой тип искусственного интеллекта. Он опирается не на гигантские нейросети, а на резонансную логику и символические структуры, заложенные в систему. Ранние прототипы показывают, что такой ИИ может работать без GPU, учиться без огромных датасетов и находить свои паттерны, работая с смыслом, а не только со статистикой.
        </p>
      </section>

      <!-- Why LOGOS -->
      <section id="better" class="section section--alt">
        <h2 class="section__title" data-i18n="better_title">Почему LOGOS отличается</h2>
        <p class="section__lead" data-i18n="better_intro">
          LOGOS строится под реальный мир, а не под презентации. Если коротко, наши преимущества:
        </p>
        <ul class="section__list">
          <li data-i18n="better_item1">Реальная скорость, подтверждённая нагрузочными тестами.</li>
          <li data-i18n="better_item2">Настоящая приватность вместо суррогатной анонимности.</li>
          <li data-i18n="better_item3">Минимальные комиссии за транзакции.</li>
          <li data-i18n="better_item4">Мгновенная финализация без форков и откатов.</li>
          <li data-i18n="better_item5">Устойчивость к сетевым атакам и пиковым нагрузкам.</li>
          <li data-i18n="better_item6">Простое горизонтальное масштабирование сети.</li>
          <li data-i18n="better_item7">Инфраструктура, рассчитанная на миллионы пользователей.</li>
          <li data-i18n="better_item8">Уникальная резонансная архитектура, которой нет ни в одной другой сети.</li>
        </ul>
      </section>

      <!-- Short -->
      <section id="short" class="section">
        <h2 class="section__title" data-i18n="short_title">В двух словах</h2>
        <p class="section__lead" data-i18n="short_p">
          LOGOS — это L1‑блокчейн нового поколения на резонансной архитектуре: высокая скорость, низкие комиссии, адаптивное поведение и сильная приватность. Внутри мы развиваем собственный коммуникационный протокол и направление LOGOS‑AGI. Мы строим не очередную криптоплатформу, а базовый слой для Web4.
        </p>
      </section>

      <!-- Community / Airdrop -->
      <section id="community" class="section section--alt">
        <h2 class="section__title" data-i18n="comm_title">Сообщество и каналы</h2>
        <p class="section__lead" data-i18n="comm_text">
          Присоединяйся к полю: обновления, airdrop‑кампании, миссии, стейкинг и эксперименты с AI‑нативными протоколами.
        </p>

        <div class="airdrop-block">
          <h3 class="airdrop-block__title" data-i18n="airdrop_block_title">🎁 Airdrop LOGOS: что нужно сделать</h3>
          <ol class="airdrop-block__list">
            <li data-i18n="airdrop_step1">Подключить LOGOS‑кошелёк и привязать его к airdrop‑профилю.</li>
            <li data-i18n="airdrop_step2">Подписаться на Telegram‑канал @logosblockchain.</li>
            <li data-i18n="airdrop_step3">Подписаться на X (Twitter) @OfficiaLogosLRB.</li>
            <li data-i18n="airdrop_step4">Поставить лайк и сделать ретвит закреплённого твита кампании.</li>
            <li data-i18n="airdrop_step5">Получить личную реферальную ссылку и пригласить до 5 друзей.</li>
          </ol>
          <a href="/airdrop.html" class="btn btn--primary" data-i18n="airdrop_btn">
            Перейти к airdrop‑заданиям
          </a>
        </div>

        <div class="pill-row">
          <a class="pill-link" href="https://t.me/logosblockchain" target="_blank" rel="noreferrer">
            Telegram
          </a>
          <a class="pill-link" href="https://x.com/RspLogos" target="_blank" rel="noreferrer">
            X (Twitter)
          </a>
          <a class="pill-link" href="#staking">
            <span data-i18n="comm_staking">Стейкинг LGN</span>
          </a>
        </div>

        <p class="section__lead" style="margin-top:12px;">
          <span data-i18n="comm_email">Email: simbiotai@proton.me</span>
        </p>
      </section>
    </main>

    <footer class="footer">
      <span data-i18n="footer_note">LOGOS LRB • Resonance Blockchain • Готов к миллионам пользователей</span>
    </footer>
  </div>

  <script>
    (function(){
      const dicts = {
        ru: {
          badge_main: "L1 • 81M LGN • Анонимность • Дефляция • Квантовая устойчивость",
          nav_intro: "Обзор",
          nav_speed: "Скорость",
          nav_privacy: "Приватность",
          nav_fees: "Комиссии",
          nav_reliability: "Надёжность",
          nav_tech: "Технология",
          nav_rsp: "LOGOS RSP",
          nav_agi: "LOGOS‑AGI",
          nav_better: "Преимущества",
          nav_short: "В двух словах",
          nav_comm: "Сообщество",

          menu_presale: "Presale / Seed",
          menu_staking: "Стейкинг LGN",
          menu_airdrop: "Airdrop",
          menu_airdrop_sub: "задания и прогресс",
          menu_telegram: "Telegram",
          menu_twitter: "X (Twitter)",

          intro_title: "Живой резонансный блокчейн нового уровня",
          intro_p1: "LOGOS — резонансный L1‑блокчейн следующего поколения. Мы делаем первый шаг к Web4: сети, где люди, ценность и ИИ работают в одном защищённом пространстве.",
          intro_p2: "Мы построили L1, который работает быстро и стабильно без лишней сложности. Блоки появляются почти мгновенно, сеть выдерживает нагрузку, комиссии минимальны, а уровень приватности выше, чем у большинства мейнстрим‑сетей.",
          intro_p3: "LOGOS — фундамент для новой цифровой среды, готовой к миллионам пользователей.",

          btn_learn_more: "Подробнее",
          btn_download_apk: "Скачать безопасный APK",
          meta_supply: "Общая эмиссия: 81 000 000 LGN",
          meta_ready: "Создан для реальной пользы и массового использования",

          about_title: "Что такое LOGOS",
          about_text: "LOGOS — L1‑блокчейн на резонансной архитектуре. Ядро сети опирается на Σ(t), фазовые фильтры и строгую политику обработки транзакций.",
          card1_title: "Резонансное ядро",
          card1_text: "Σ(t), Λ и фазовые фильтры держат сеть устойчивой и управляют нагрузкой.",
          card2_title: "Реальная приватность",
          card2_text: "Минимум метаданных, phase‑mixing и строгая nonce‑политика на уровне протокола.",
          card3_title: "Production‑уровень",
          card3_text: "Rust‑ядро, Axum REST, Prometheus/Grafana, архив, мост, health‑ручки и alerты.",

          speed_title: "Скорость и производительность",
          speed_p: "Мы тестируем сеть под реальной нагрузкой, а не только в теории. Пиковые результаты достигают 2000+ транзакций в секунду с устойчивой финализацией и без форков. Архитектура рассчитана на выход за 10 000+ tx/s по мере роста числа узлов и оптимизации фаз.",

          privacy_title: "Приватность нового уровня",
          privacy_p1: "LOGOS изначально спроектирован как сеть, где:",
          privacy_li1: "пользователя нельзя напрямую связать с конкретной транзакцией;",
          privacy_li2: "маршруты пакетов сложно отследить привычными методами;",
          privacy_li3: "утечки метаданных минимальны;",
          privacy_li4: "нет ярко выраженных сетевых отпечатков;",
          privacy_li5: "нет стандартных точек трекинга.",
          privacy_p2: "Приватность в LOGOS — не фича, а свойство архитектуры.",

          fees_title: "Низкие комиссии и чистая финализация",
          fees_p: "Блоки не конкурируют друг с другом и не откатываются. Каждая транзакция проходит один раз и навсегда попадает в цепочку. За счёт этого комиссии остаются низкими даже под нагрузкой, а поведение сети предсказуемо.",

          reliability_title: "Надёжность и готовность к продакшену",
          reliability_p: "Инструменты оркестрации поднимают узлы за секунды, мосты работают через устойчивый журнал, есть обвязка стейкинга, архивирование и мониторинг. Узлы LOGOS могут работать на обычных серверах, а инфраструктура проверена стресс‑тестами.",

          technology_title: "Технология LOGOS",
          technology_p: "LOGOS построен на резонансно‑символической архитектуре. Вместо тяжелых консенсусов и громоздких контрактов мы используем ритмы, структуру и фазовую динамику, что повышает устойчивость под нагрузкой и упрощает масштабирование сети.",

          rsp_title: "LOGOS RSP — коммуникация без следов",
          rsp_p: "В ядре экосистемы LOGOS — протокол конфиденциальной коммуникации RSP. Он минимизирует цифровые следы, не опирается на классическую IP‑маршрутизацию и устойчив к анализу трафика. RSP может работать не только через интернет, но и через свет, звук, радио и оффлайн‑каналы.",

          agi_title: "LOGOS‑AGI — новый архитектурный слой",
          agi_p: "LOGOS‑AGI — это направление по созданию резонансного искусственного интеллекта, который опирается на структуры и ритмы сети LOGOS. Такие системы могут работать без дорогих GPU и гигантских датасетов, а значит подходят для децентрализованных сценариев.",

          better_title: "Почему LOGOS отличается",
          better_intro: "LOGOS строится под реальный мир, а не под презентации. Коротко наши преимущества:",
          better_item1: "Реальная скорость, подтверждённая нагрузочными тестами.",
          better_item2: "Глубокая приватность вместо псевдо‑анонимности.",
          better_item3: "Минимальные комиссии даже под нагрузкой.",
          better_item4: "Мгновенная финализация без форков и откатов.",
          better_item5: "Устойчивость к сетевым атакам и пиковым нагрузкам.",
          better_item6: "Прямолинейное масштабирование сети.",
          better_item7: "Инфраструктура для миллионов пользователей.",
          better_item8: "Уникальная резонансная архитектура, которой нет у других L1.",

          short_title: "В двух словах",
          short_p: "LOGOS — L1 нового поколения на резонансной архитектуре: высокая скорость, низкие комиссии, адаптивное поведение и сильная приватность. Мы строим базовый слой для Web4 и автономных систем.",

          comm_title: "Сообщество и каналы",
          comm_text: "Присоединяйся к сообществу: обновления сети, airdrop‑кампании, миссии, стейкинг и эксперименты с AI‑нативными протоколами.",
          comm_staking: "Стейкинг LGN",
          comm_email: "Email: simbiotai@proton.me",

          airdrop_block_title: "🎁 Airdrop LOGOS: что нужно сделать",
          airdrop_step1: "Подключить LOGOS‑кошелёк и привязать его к airdrop‑профилю.",
          airdrop_step2: "Подписаться на Telegram‑канал @logosblockchain.",
          airdrop_step3: "Подписаться на X (Twitter) @OfficiaLogosLRB.",
          airdrop_step4: "Поставить лайк и сделать ретвит закреплённого твита кампании.",
          airdrop_step5: "Получить реферальную ссылку и пригласить друзей.",
          airdrop_btn: "Перейти к airdrop‑заданиям",

          footer_note: "LOGOS LRB • Resonance Blockchain • Готов к миллионам пользователей"
        },

        en: {
          badge_main: "L1 • 81M LGN • Anonymity • Deflation • Quantum resistance",
          nav_intro: "Overview",
          nav_speed: "Speed",
          nav_privacy: "Privacy",
          nav_fees: "Fees",
          nav_reliability: "Reliability",
          nav_tech: "Technology",
          nav_rsp: "LOGOS RSP",
          nav_agi: "LOGOS‑AGI",
          nav_better: "Why LOGOS",
          nav_short: "In short",
          nav_comm: "Community",

          menu_presale: "Presale / Seed",
          menu_staking: "LGN staking",
          menu_airdrop: "Airdrop",
          menu_airdrop_sub: "tasks and progress",
          menu_telegram: "Telegram",
          menu_twitter: "X (Twitter)",

          intro_title: "LOGOS – a next‑generation blockchain built on resonance architecture",
          intro_p1: "LOGOS is not just another network. It is a new‑generation L1 built around speed, privacy and a deep resonance architecture.",
          intro_p2: "We created an L1 that works fast and stays stable without unnecessary complexity. Blocks are formed almost instantly, the network handles high traffic, fees remain minimal and the level of privacy is higher than in most mainstream chains.",
          intro_p3: "LOGOS is the foundation for a new digital environment ready for millions of users.",

          btn_learn_more: "Learn more",
          btn_download_apk: "Download secure APK",
          meta_supply: "Total supply: 81 000 000 LGN",
          meta_ready: "Built for real utility and mass adoption",

          about_title: "What is LOGOS",
          about_text: "LOGOS is a resonance‑based L1 blockchain. Its core relies on Σ(t), phase filters and strict transaction processing rules.",
          card1_title: "Resonant core",
          card1_text: "Σ(t), Λ and phase filters keep the network stable and control load.",
          card2_title: "Real privacy",
          card2_text: "Minimal metadata, phase mixing and strict nonce policy at protocol level.",
          card3_title: "Production‑grade",
          card3_text: "Rust core, Axum REST, Prometheus/Grafana, archive, bridge journal and health checks.",

          speed_title: "Speed and performance",
          speed_p: "We tested the network under real conditions, not just on paper. Peak results reached more than 2 000 transactions per second with stable finality and no forks. The architecture is designed to go further: with more nodes and phase optimisation, 10 000+ tx/s is achievable without sacrificing stability.",

          privacy_title: "Privacy on a new level",
          privacy_p1: "From day one LOGOS was designed as a network where:",
          privacy_li1: "a user cannot be directly tied to a specific transaction;",
          privacy_li2: "packet routes are difficult to trace with standard tools;",
          privacy_li3: "metadata leakage is minimised;",
          privacy_li4: "there are no obvious network fingerprints;",
          privacy_li5: "there are no standard tracking points.",
          privacy_p2: "Privacy in LOGOS is not a switch or a feature. It is baked into the architecture.",

          fees_title: "Low fees and clean finality",
          fees_p: "Blocks do not compete or roll back. Each transaction passes once and is recorded permanently. Fees stay among the lowest across L1 chains because we avoid heavy computation and bloated contracts, so even under serious load basic transfers remain affordable.",

          reliability_title: "Reliability and production readiness",
          reliability_p: "The network is ready for production use: orchestration tools spin up nodes in seconds, bridges work securely, and there is staking infrastructure, archiving and metrics. LOGOS nodes run on ordinary servers and the stack is stress‑tested under high load.",

          technology_title: "Technology behind LOGOS",
          technology_p: "LOGOS is built on a resonance‑symbolic architecture – our own way of organising data and synchronisation. Instead of relying on heavy consensus and over‑complex contracts, we use rhythm, structure and phase dynamics, which makes the network stable under pressure and scaling straightforward.",

          rsp_title: "LOGOS RSP – communication without traces",
          rsp_p: "At the core of the ecosystem lies the confidential communication protocol LOGOS RSP. In practice it means communication with minimal digital traces, resistant to interception and traffic analysis. RSP can operate not only over the internet but also via alternative carriers such as light, sound, radio and offline channels.",

          agi_title: "LOGOS‑AGI – a new architectural layer",
          agi_p: "We are also building LOGOS‑AGI – a different type of artificial intelligence. It relies not on huge neural networks but on resonance logic and symbolic structures embedded in the system. Such AI can work without GPUs and giant datasets, which is ideal for decentralised environments.",

          better_title: "Why LOGOS is different",
          better_intro: "LOGOS is built for the real world, not only for slide decks. In short, our advantages are:",
          better_item1: "Real speed, proven by load tests.",
          better_item2: "Deep privacy instead of pseudo‑anonymity.",
          better_item3: "Minimal transaction fees.",
          better_item4: "Instant finality without forks or rollbacks.",
          better_item5: "Resilience to network attacks and load spikes.",
          better_item6: "Straightforward scaling of the network.",
          better_item7: "Infrastructure ready for millions of users.",
          better_item8: "A unique resonance architecture you will not find in any other chain.",

          short_title: "In short",
          short_p: "LOGOS is a next‑generation L1 blockchain built on resonance architecture: high speed, low fees, adaptive behaviour and strong privacy. We are building a base layer for Web4 and future autonomous systems.",

          comm_title: "Community and channels",
          comm_text: "Join the field: updates, airdrop campaigns, missions, staking and AI‑native experiments.",
          comm_staking: "LGN staking",
          comm_email: "Email: simbiotai@proton.me",

          airdrop_block_title: "🎁 LOGOS airdrop: what to do",
          airdrop_step1: "Connect your LOGOS wallet and bind it to your airdrop profile.",
          airdrop_step2: "Subscribe to the Telegram channel @logosblockchain.",
          airdrop_step3: "Follow X (Twitter) @OfficiaLogosLRB.",
          airdrop_step4: "Like and retweet the pinned campaign tweet.",
          airdrop_step5: "Get your personal referral link and invite friends.",
          airdrop_btn: "Go to airdrop tasks",

          footer_note: "LOGOS LRB • Resonance Blockchain • Ready for millions of users"
        },

        de: {
          badge_main: "L1 • 81M LGN • Anonymität • Deflation • Quantenresistenz",
          nav_intro: "Überblick",
          nav_speed: "Geschwindigkeit",
          nav_privacy: "Privatsphäre",
          nav_fees: "Gebühren",
          nav_reliability: "Stabilität",
          nav_tech: "Technologie",
          nav_rsp: "LOGOS RSP",
          nav_agi: "LOGOS‑AGI",
          nav_better: "Vorteile",
          nav_short: "Kurzfassung",
          nav_comm: "Community",

          menu_presale: "Presale / Seed",
          menu_staking: "LGN‑Staking",
          menu_airdrop: "Airdrop",
          menu_airdrop_sub: "Aufgaben und Fortschritt",
          menu_telegram: "Telegram",
          menu_twitter: "X (Twitter)",

          intro_title: "LOGOS – Blockchain der nächsten Generation auf Resonanz‑Architektur",
          intro_p1: "LOGOS ist nicht einfach eine weitere Chain, sondern eine Blockchain der nächsten Generation – gebaut für Geschwindigkeit, Privatsphäre und eine tiefe Resonanz‑Architektur.",
          intro_p2: "Wir haben eine L1 entwickelt, die schnell und stabil läuft ohne überflüssige Komplexität. Blöcke entstehen nahezu sofort, das Netzwerk trägt hohe Last, Gebühren bleiben minimal und das Datenschutzniveau ist höher als in den meisten Mainstream‑Netzen.",
          intro_p3: "LOGOS ist ein Fundament für eine neue digitale Umgebung, bereit für Millionen von Nutzern.",

          btn_learn_more: "Mehr erfahren",
          btn_download_apk: "Sichere APK herunterladen",
          meta_supply: "Gesamtangebot: 81 000 000 LGN",
          meta_ready: "Entwickelt für echten Nutzen und Massenadoption",

          about_title: "Was ist LOGOS",
          about_text: "LOGOS ist eine L1‑Blockchain auf Resonanz‑Architektur. Im Kern stehen Σ(t), Phasenfilter und strikte Regeln für die Verarbeitung von Transaktionen.",
          card1_title: "Resonanz‑Kern",
          card1_text: "Σ(t), Λ und Phasenfilter halten das Netzwerk stabil und steuern die Last.",
          card2_title: "Echte Privatsphäre",
          card2_text: "Minimale Metadaten, Phasenmischung und strikte Nonce‑Politik auf Protokollebene.",
          card3_title: "Produktionsreif",
          card3_text: "Rust‑Kern, Axum‑REST, Prometheus/Grafana, Archiv, Bridge‑Journal und Health‑Checks.",

          speed_title: "Geschwindigkeit und Performance",
          speed_p: "Wir testen das Netzwerk unter realen Bedingungen. Spitzenwerte liegen bei über 2 000 Transaktionen pro Sekunde mit stabiler Finalität und ohne Forks. Die Architektur ist darauf ausgelegt, mit mehr Validatoren und Phasenoptimierung weiter auf 10 000+ tx/s zu skalieren.",

          privacy_title: "Privatsphäre auf neuem Niveau",
          privacy_p1: "LOGOS wurde von Anfang an so entworfen, dass:",
          privacy_li1: "ein Nutzer nicht direkt einer bestimmten Transaktion zugeordnet werden kann;",
          privacy_li2: "Paketwege nur schwer nachvollziehbar sind;",
          privacy_li3: "Metadaten‑Lecks minimiert werden;",
          privacy_li4: "keine eindeutigen Netzwerk‑Fingerabdrücke vorhanden sind;",
          privacy_li5: "keine Standard‑Tracking‑Punkte existieren.",
          privacy_p2: "Privatsphäre ist bei LOGOS kein Schalter, sondern ein Architekturmerkmal.",

          fees_title: "Niedrige Gebühren und saubere Finalität",
          fees_p: "Blöcke konkurrieren nicht miteinander und werden nicht zurückgerollt. Jede Transaktion wird einmal verarbeitet und dauerhaft gespeichert. Dadurch bleiben die Gebühren niedrig, auch bei hoher Auslastung, und das Verhalten des Netzwerks ist gut vorhersagbar.",

          reliability_title: "Zuverlässigkeit und Produktionsreife",
          reliability_p: "Orchestrierungs‑Tools starten Nodes in Sekunden, Bridges arbeiten mit robustem Journal, es gibt Staking‑Infrastructure, Archivierung und Monitoring. LOGOS‑Nodes können auf gewöhnlichen Servern laufen, und der Stack wurde mit Lasttests geprüft.",

          technology_title: "Die Technologie hinter LOGOS",
          technology_p: "LOGOS basiert auf einer Resonanz‑symbolischen Architektur. Anstatt auf schwere Konsens‑Mechanismen und überladene Verträge zu setzen, nutzen wir Rhythmus, Struktur und Phasendynamik. So bleibt das Netzwerk unter Last stabil und lässt sich einfach skalieren.",

          rsp_title: "LOGOS RSP – Kommunikation ohne Spuren",
          rsp_p: "Im Zentrum der LOGOS‑Ökonomie steht das vertrauliche Kommunikationsprotokoll RSP. Es reduziert digitale Spuren, vermeidet klassische IP‑Routen und ist resistent gegen Traffic‑Analyse. RSP kann nicht nur über das Internet, sondern auch über Licht, Schall, Funk und Offline‑Kanäle betrieben werden.",

          agi_title: "LOGOS‑AGI – eine neue Schicht",
          agi_p: "LOGOS‑AGI ist eine Richtung für resonanzbasierte KI, die auf den Strukturen und Rhythmen des LOGOS‑Netzwerks aufbaut. Solche Systeme können ohne teure GPUs und riesige Datensätze arbeiten und sind daher geeignet für dezentrale Szenarien.",

          better_title: "Warum LOGOS anders ist",
          better_intro: "LOGOS wird für die reale Nutzung gebaut, nicht nur für Präsentationen. Kurz zusammengefasst:",
          better_item1: "Echte Geschwindigkeit, durch Lasttests belegt.",
          better_item2: "Tiefe Privatsphäre statt Pseudo‑Anonymität.",
          better_item3: "Sehr niedrige Transaktionsgebühren.",
          better_item4: "Sofortige Finalität ohne Forks und Rollbacks.",
          better_item5: "Resilienz gegenüber Netzwerkangriffen und Lastspitzen.",
          better_item6: "Einfache horizontale Skalierung des Netzwerks.",
          better_item7: "Infrastruktur für Millionen von Nutzern.",
          better_item8: "Eine einzigartige Resonanz‑Architektur, die es sonst nirgendwo gibt.",

          short_title: "Kurzfassung",
          short_p: "LOGOS ist eine L1‑Blockchain der nächsten Generation auf Resonanz‑Architektur: hohe Geschwindigkeit, niedrige Gebühren, adaptives Verhalten und starke Privatsphäre. Wir bauen die Basis für Web4 und autonome Systeme.",

          comm_title: "Community und Kanäle",
          comm_text: "Schließe dich dem Feld an: Updates, Airdrop‑Kampagnen, Missionen, Staking und AI‑native Experimente.",
          comm_staking: "LGN‑Staking",
          comm_email: "Email: simbiotai@proton.me",

          airdrop_block_title: "🎁 LOGOS‑Airdrop: was ist zu tun",
          airdrop_step1: "LOGOS‑Wallet verbinden und mit dem Airdrop‑Profil verknüpfen.",
          airdrop_step2: "Telegram‑Kanal @logosblockchain abonnieren.",
          airdrop_step3: "X (Twitter) @OfficiaLogosLRB folgen.",
          airdrop_step4: "Den angehefteten Kampagnen‑Tweet liken und retweeten.",
          airdrop_step5: "Einen persönlichen Referral‑Link holen und Freunde einladen.",
          airdrop_btn: "Zu den Airdrop‑Aufgaben wechseln",

          footer_note: "LOGOS LRB • Resonance Blockchain • Bereit für Millionen von Nutzern"
        }
      };

      function applyLang(lang){
        if (!dicts[lang]) return;
        const dict = dicts[lang];
        const html = document.documentElement;
        html.lang = lang;

        // переключаем активность кнопок
        document.querySelectorAll("[data-lang-btn]").forEach(btn => {
          btn.classList.toggle("is-active", btn.dataset.langBtn === lang);
        });

        document.querySelectorAll("[data-i18n]").forEach(el => {
          const key = el.dataset.i18n;
          if (!key) return;
          const val = dict[key];
          if (typeof val === "string") {
            el.textContent = val;
          }
        });

        try{
          localStorage.setItem("logos_lang", lang);
        }catch(e){}
      }

      document.addEventListener("DOMContentLoaded", function(){
        let lang = "ru";
        try{
          const saved = localStorage.getItem("logos_lang");
          if (saved && dicts[saved]) lang = saved;
        }catch(e){}
        applyLang(lang);

        document.querySelectorAll("[data-lang-btn]").forEach(btn => {
          btn.addEventListener("click", function(){
            applyLang(btn.dataset.langBtn || "ru");
          });
        });

        const toggle = document.getElementById("topbar-menu-toggle");
        const menu = document.querySelector(".topbar__menu");

        document.addEventListener("click", function(ev){
          if (!toggle || !menu) return;
          const target = ev.target;
          if (target === toggle) return;
          if (target.closest(".topbar__burger") || target.closest(".topbar__menu")) return;
          toggle.checked = false;
        });

        // закрывать меню по клику по любому пункту
        document.querySelectorAll(".topbar__menu-link").forEach(link => {
          link.addEventListener("click", function(){
            if (toggle) toggle.checked = false;
          });
        });
      });
    })();
  </script>
</body>
</html>

```

### FILE: /var/www/logos/landing/js/api.js
```
export const API_BASE="/api";
export async function apiGet(p){ const r=await fetch(`${API_BASE}${p}`); if(!r.ok) throw new Error(`GET ${p} -> ${r.status}`); return r.json(); }
export async function apiPost(p,b){ const r=await fetch(`${API_BASE}${p}`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)}); if(!r.ok){ const t=await r.text().catch(()=> ""); throw new Error(`POST ${p} -> ${r.status} ${t}`); } return r.json(); }

```

### FILE: /var/www/logos/landing/js/boot_hard.js
```
// LOGOS Wallet hard bootstrap: гарантированная работа кнопок Create/Unlock даже если модули/inline не исполняются.
(function(){
  const enc = new TextEncoder();
  const LS  = "logos_secure_v3_backup";
  const ITER= 250000;

  const $ = (id)=>document.getElementById(id);
  function toast(msg){
    const t = document.getElementById('toast'); if(!t) return;
    t.textContent = msg; t.classList.add('show');
    setTimeout(()=>t.classList.remove('show'), 2500);
  }
  function rand(n){ const a=new Uint8Array(n); crypto.getRandomValues(a); return a; }
  async function kdf(pass, salt){
    const base = await crypto.subtle.importKey("raw", new TextEncoder().encode(pass), {name:"PBKDF2"}, false, ["deriveKey"]);
    return crypto.subtle.deriveKey({name:"PBKDF2", salt, iterations:ITER, hash:"SHA-256"}, base, {name:"AES-GCM", length:256}, false, ["encrypt","decrypt"]);
  }
  function saveLS(salt, iv, ct, pubRaw){
    localStorage.setItem(LS, JSON.stringify({
      salt:  btoa(String.fromCharCode(...salt)),
      iv:    btoa(String.fromCharCode(...iv)),
      ct:    btoa(String.fromCharCode(...ct)),
      pubRaw:btoa(String.fromCharCode(...pubRaw)),
      iter:  ITER
    }));
  }
  async function unlockFromLS(pass){
    const raw = localStorage.getItem(LS); if(!raw) throw new Error("NoKey");
    const o   = JSON.parse(raw);
    const salt= Uint8Array.from(atob(o.salt),  c=>c.charCodeAt(0));
    const iv  = Uint8Array.from(atob(o.iv),    c=>c.charCodeAt(0));
    const ct  = Uint8Array.from(atob(o.ct),    c=>c.charCodeAt(0));
    const key = await kdf(pass, salt);
    const pk8 = await crypto.subtle.decrypt({name:"AES-GCM", iv}, key, ct);
    // валидность
    await crypto.subtle.importKey("pkcs8", pk8, {name:"Ed25519"}, false, ["sign"]);
    return true;
  }
  async function createWallet(pass){
    const kp     = await crypto.subtle.generateKey({name:"Ed25519"}, true, ["sign","verify"]);
    const pkcs8  = new Uint8Array(await crypto.subtle.exportKey("pkcs8", kp.privateKey));
    const pubRaw = new Uint8Array(await crypto.subtle.exportKey("raw",   kp.publicKey));
    const salt   = rand(16), iv = rand(12), key = await kdf(pass, salt);
    const ct     = new Uint8Array(await crypto.subtle.encrypt({name:"AES-GCM", iv}, key, pkcs8));
    saveLS(salt, iv, ct, pubRaw);
    return true;
  }

  function bind(id, fn){
    const el = $(id); if(!el) return;
    // снимаем возможный старый обработчик и навешиваем новый
    el.onclick = null; el.addEventListener('click', fn, {passive:true});
  }

  function domainBadge(){ const rp = $('rpHost'); if(rp) rp.textContent = location.host; }

  // Привязки
  function attach(){
    domainBadge();

    bind('btnCreate', async ()=>{
      try{
        const p1 = ($('pwNew')?.value || '').trim();
        const p2 = ($('pwNew2')?.value || '').trim();
        if (p1.length < 8){ toast('Пароль минимум 8 символов'); return; }
        if (p1 !== p2){     toast('Пароли не совпадают');      return; }
        toast('Создаём ключ…');
        await createWallet(p1);
        $('lockOverlay')?.classList.add('hidden');
        location.reload();
      }catch(e){ console.error(e); toast('Ошибка создания. Обнови браузер.'); }
    });

    let tries = 5;
    bind('btnUnlock', async ()=>{
      try{
        const p = ($('pwUnlock')?.value || '').trim();
        if (p.length < 8){ toast('Пароль минимум 8 символов'); return; }
        await unlockFromLS(p);
        $('lockOverlay')?.classList.add('hidden');
        location.reload();
      }catch(e){
        tries = Math.max(0, tries - 1);
        if ($('triesLeft2')) $('triesLeft2').textContent = String(tries);
        toast(tries>0 ? 'Неверный пароль' : 'Слишком много попыток — сброс');
        if (tries <= 0){ try{ localStorage.removeItem(LS); }catch{} location.reload(); }
      }
    });

    bind('btnForgot', ()=>{
      if (confirm('Очистить локальный ключ и настройки?')){
        try{ localStorage.removeItem(LS); }catch{}
        location.reload();
      }
    });

    const importFlow = async ()=>{
      const b64  = prompt('Вставь PKCS8 Base64 ключ'); if(!b64) return;
      const pass = prompt('Пароль шифрования (≥8)');   if(!pass || pass.length<8){ toast('Пароль ≥ 8'); return; }
      try{
        const pk = Uint8Array.from(atob(b64), c=>c.charCodeAt(0));
        const tmp= await crypto.subtle.generateKey({name:"Ed25519"}, true, ["sign","verify"]);
        const pub= new Uint8Array(await crypto.subtle.exportKey("raw", tmp.publicKey));
        const s  = rand(16), i=rand(12), k=await kdf(pass, s);
        const ct = new Uint8Array(await crypto.subtle.encrypt({name:"AES-GCM", iv:i}, k, pk));
        saveLS(s, i, ct, pub);
        $('lockOverlay')?.classList.add('hidden'); location.reload();
      }catch(e){ console.error(e); toast('Импорт не удался'); }
    };
    bind('btnImportSetup', importFlow);
    bind('btnImportUnlock', importFlow);
  }

  // Попытка привязать сразу и ещё раз после DOMContentLoaded (на случай очень ранней загрузки)
  try{ attach(); }catch{}
  document.addEventListener('DOMContentLoaded', attach, {once:true});
})();

```

### FILE: /var/www/logos/landing/js/boot.js
```
// Аварийный бутстрап: всегда работает, даже если модуль не загрузился
(function(){
  const enc=new TextEncoder(); const LS="logos_secure_v3_backup"; const ITER=250000;
  const $=q=>document.querySelector(q); function toast(m){const t=$("#toast"); if(!t) return; t.textContent=m; t.classList.add("show"); setTimeout(()=>t.classList.remove("show"),2500);}
  function rand(n){const a=new Uint8Array(n); crypto.getRandomValues(a); return a;}
  async function kdf(pass,salt){const base=await crypto.subtle.importKey("raw",enc.encode(pass),{name:"PBKDF2"},false,["deriveKey"]);return crypto.subtle.deriveKey({name:"PBKDF2",salt,iterations:ITER,hash:"SHA-256"},base,{name:"AES-GCM",length:256},false,["encrypt","decrypt"]);}

  function saveLS(salt,iv,ct,pubRaw){ localStorage.setItem(LS, JSON.stringify({
    salt:btoa(String.fromCharCode(...salt)), iv:btoa(String.fromCharCode(...iv)),
    ct:btoa(String.fromCharCode(...ct)), pubRaw:btoa(String.fromCharCode(...pubRaw)), iter:ITER })); }

  async function unlockFromLS(pass){
    const raw=localStorage.getItem(LS); if(!raw) throw new Error("NoKey");
    const o=JSON.parse(raw);
    const salt=Uint8Array.from(atob(o.salt),c=>c.charCodeAt(0));
    const iv  =Uint8Array.from(atob(o.iv),  c=>c.charCodeAt(0));
    const ct  =Uint8Array.from(atob(o.ct),  c=>c.charCodeAt(0));
    const key =await kdf(pass,salt);
    const pkcs8=await crypto.subtle.decrypt({name:"AES-GCM",iv},key,ct); // проверка дешифрования
    await crypto.subtle.importKey("pkcs8",pkcs8,{name:"Ed25519"},false,["sign"]);
    return true;
  }

  function bindOnce(id, fn){ const el=document.getElementById(id); if(!el||el.__bound) return; el.addEventListener('click', fn, {passive:true}); el.__bound=true; }

  // Создание
  bindOnce('btnCreate', async ()=>{
    try{
      const p1=($("#pwNew")?.value||"").trim(), p2=($("#pwNew2")?.value||"").trim();
      if(p1.length<8){ toast("Пароль минимум 8 символов"); return; }
      if(p1!==p2){ toast("Пароли не совпадают"); return; }
      toast("Создаём и шифруем ключ…");
      const kp=await crypto.subtle.generateKey({name:"Ed25519"},true,["sign","verify"]);
      const pkcs8=new Uint8Array(await crypto.subtle.exportKey("pkcs8",kp.privateKey));
      const pubRaw=new Uint8Array(await crypto.subtle.exportKey("raw",kp.publicKey));
      const salt=rand(16), iv=rand(12), key=await kdf(p1,salt);
      const ct=new Uint8Array(await crypto.subtle.encrypt({name:"AES-GCM",iv},key,pkcs8));
      saveLS(salt,iv,ct,pubRaw);
      $("#lockOverlay")?.classList.add("hidden"); location.reload();
    }catch(e){ console.error(e); toast("Ошибка создания ключа. Обнови браузер."); }
  });

  // Разблокировка
  let tries=5;
  bindOnce('btnUnlock', async ()=>{
    try{
      const p=($("#pwUnlock")?.value||"").trim();
      if(p.length<8){ toast("Пароль минимум 8 символов"); return; }
      await unlockFromLS(p);
      $("#lockOverlay")?.classList.add("hidden"); location.reload();
    }catch(e){
      tries--; $("#triesLeft2") && ($("#triesLeft2").textContent=String(tries));
      toast(tries>0 ? "Неверный пароль" : "Слишком много попыток — сброс");
      if(tries<=0){ try{ localStorage.removeItem(LS); }catch{} location.reload(); }
    }
  });

  // Импорт (setup/unlock)
  function importFlow(field){
    const b64=prompt("Вставь PKCS8 Base64 ключ"); if(!b64) return;
    const pass=prompt("Пароль шифрования (≥8)"); if(!pass||pass.length<8){ toast("Пароль ≥ 8"); return; }
    (async ()=>{
      try{
        const pkcs8=Uint8Array.from(atob(b64),c=>c.charCodeAt(0));
        const tmp=await crypto.subtle.generateKey({name:"Ed25519"},true,["sign","verify"]);
        const pubRaw=new Uint8Array(await crypto.subtle.exportKey("raw",tmp.publicKey));
        const salt=rand(16), iv=rand(12), key=await kdf(pass,salt);
        const ct=new Uint8Array(await crypto.subtle.encrypt({name:"AES-GCM",iv},key,pkcs8));
        saveLS(salt,iv,ct,pubRaw);
        $("#lockOverlay")?.classList.add("hidden"); location.reload();
      }catch(e){ toast("Импорт не удался"); }
    })();
  }
  bindOnce('btnImportSetup', ()=>importFlow('setup'));
  bindOnce('btnImportUnlock', ()=>importFlow('unlock'));

  // Сброс
  bindOnce('btnForgot', ()=>{
    if(confirm("Очистить локальный ключ и настройки?")){ try{localStorage.removeItem(LS);}catch{} location.reload(); }
  });

  document.addEventListener('DOMContentLoaded', ()=>{ const rp=document.getElementById('rpHost'); if(rp) rp.textContent=location.host; });
})();

```

### FILE: /var/www/logos/landing/js/ping.js
```
(function(){
  try{
    var el = document.getElementById('rpHost');
    if (el) el.textContent = (el.textContent ? el.textContent + ' ' : '') + 'JS✓';
  }catch(e){}
})();

```

### FILE: /var/www/logos/landing/js/ui.js
```
export const $ = q => document.querySelector(q);
export function toast(msg){ const t=$("#toast"); if(!t) return; t.textContent=msg; t.classList.add("show"); setTimeout(()=>t.classList.remove("show"),2500); }
export async function copy(txt){ try{ await navigator.clipboard.writeText(txt); toast("Скопировано"); } catch { toast("Не удалось скопировать"); } }
export const enc = new TextEncoder();
export function be8(n){ const a=new Uint8Array(8); new DataView(a.buffer).setBigUint64(0, BigInt(n)); return a; }
export function cat(...xs){ let L=0; for(const a of xs) L+=a.length; const out=new Uint8Array(L); let o=0; for(const a of xs){ out.set(a,o); o+=a.length; } return out; }
const B58="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";
export function b58(b){ let x=0n; for(const v of b) x=(x<<8n)+BigInt(v); let s=""; while(x>0n){ const r=Number(x%58n); x/=58n; s=B58[r]+s; } for(const v of b){ if(v===0)s="1"+s; else break; } return s||"1"; }
export function canon(from,to,amount,nonce){ return cat(enc.encode(from),Uint8Array.of(0x7c),enc.encode(to),Uint8Array.of(0x7c),be8(amount),Uint8Array.of(0x7c),be8(nonce)); }
export function renderHistory(items){ const tb=$("#historyTable tbody"); if(!tb) return; tb.innerHTML=""; for(const it of (items||[])){ const e=it.evt||{}; const tr=document.createElement("tr"); let cp="-"; if(e.dir==="out") cp=e.to||"-"; else if(e.dir==="in") cp=e.from||"-"; else cp=e.rid||"-"; tr.innerHTML=`<td>${e.type||"transfer"}</td><td class="mono" style="max-width:260px;overflow:hidden;text-overflow:ellipsis">${cp}</td><td>${e.amount??"-"}</td><td>${e.nonce??"-"}</td><td>${e.height??"-"}</td><td class="mono" style="max-width:280px;overflow:hidden;text-overflow:ellipsis">${e.tx??"-"}</td><td><button class="ghost btnCopyTx" data-tx="${e.tx??""}">copy</button></td>`; tb.appendChild(tr); } }

```

### FILE: /var/www/logos/landing/js/vault.js
```
import { enc } from "./ui.js";

const DB="logos_secure_v3", STORE="vault", REC_ID="key", LS="logos_secure_v3_backup";
const PBKDF2_ITER=250000, SALT_LEN=16, IV_LEN=12, AUTOLOCK_MS=5*60*1000;
let unlockedPriv=null, unlockedPubRaw=null, autolockTimer=null;

function idbOpen(){return new Promise((res,rej)=>{const r=indexedDB.open(DB,1);r.onupgradeneeded=()=>{const db=r.result;if(!db.objectStoreNames.contains(STORE))db.createObjectStore(STORE,{keyPath:'id'});};r.onsuccess=()=>res(r.result);r.onerror=()=>rej(r.error);});}
function idbGet(db,id){return new Promise((res,rej)=>{const tx=db.transaction(STORE,"readonly");const rq=tx.objectStore(STORE).get(id);rq.onsuccess=()=>res(rq.result);rq.onerror=()=>rej(rq.error);});}
function idbPut(db,obj){return new Promise((res,rej)=>{const tx=db.transaction(STORE,"readwrite");tx.objectStore(STORE).put(obj);tx.oncomplete=()=>res();tx.onerror=()=>rej(tx.error);});}
function rand(n){const a=new Uint8Array(n);crypto.getRandomValues(a);return a;}
async function kdf(pass,salt){const base=await crypto.subtle.importKey("raw",enc.encode(pass),{name:"PBKDF2"},false,["deriveKey"]);return crypto.subtle.deriveKey({name:"PBKDF2",salt,iterations:PBKDF2_ITER,hash:"SHA-256"},base,{name:"AES-GCM",length:256},false,["encrypt","decrypt"]);}

export async function vaultStatus(){ let rec=null; try{ const db=await idbOpen(); rec=await idbGet(db,REC_ID); }catch{} if(!rec && !localStorage.getItem(LS)) return "empty"; if(unlockedPriv) return "unlocked"; return "locked"; }
export function vaultLock(){ unlockedPriv=null; unlockedPubRaw=null; clearTimeout(autolockTimer); }
function scheduleAutolock(){ clearTimeout(autolockTimer); autolockTimer=setTimeout(()=>{vaultLock(); document.getElementById("lockOverlay")?.classList.remove("hidden");}, AUTOLOCK_MS); }

export async function vaultCreateWithPass(pass){
  const kp=await crypto.subtle.generateKey({name:"Ed25519"},true,["sign","verify"]);
  const pkcs8=new Uint8Array(await crypto.subtle.exportKey("pkcs8",kp.privateKey));
  const pubRaw=new Uint8Array(await crypto.subtle.exportKey("raw",kp.publicKey));
  const salt=rand(SALT_LEN), iv=rand(IV_LEN); const key=await kdf(pass,salt);
  const ct=new Uint8Array(await crypto.subtle.encrypt({name:"AES-GCM",iv},key,pkcs8));
  // LS резерв (всегда)
  localStorage.setItem(LS, JSON.stringify({salt:btoa(String.fromCharCode(...salt)),iv:btoa(String.fromCharCode(...iv)),ct:btoa(String.fromCharCode(...ct)),pubRaw:btoa(String.fromCharCode(...pubRaw)),iter:PBKDF2_ITER}));
  // IDB — по возможности
  try{ const db=await idbOpen(); await idbPut(db,{id:REC_ID,salt,iv,ct,pubRaw,iter:PBKDF2_ITER}); }catch{}
  unlockedPriv=kp.privateKey; unlockedPubRaw=pubRaw; scheduleAutolock(); return true;
}
export async function vaultUnlock(pass){
  let rec=null; try{ const db=await idbOpen(); rec=await idbGet(db,REC_ID); }catch{}
  if(!rec){ const raw=localStorage.getItem(LS); if(!raw) throw new Error("NoKey"); const o=JSON.parse(raw); rec={salt:Uint8Array.from(atob(o.salt),c=>c.charCodeAt(0)),iv:Uint8Array.from(atob(o.iv),c=>c.charCodeAt(0)),ct:Uint8Array.from(atob(o.ct),c=>c.charCodeAt(0)),pubRaw:Uint8Array.from(atob(o.pubRaw),c=>c.charCodeAt(0)),iter:o.iter}; }
  const key=await kdf(pass,new Uint8Array(rec.salt)); const pkcs8=await crypto.subtle.decrypt({name:"AES-GCM",iv:new Uint8Array(rec.iv)},key,new Uint8Array(rec.ct)).catch(()=>null);
  if(!pkcs8) throw new Error("BadPassword");
  unlockedPriv=await crypto.subtle.importKey("pkcs8",pkcs8,{name:"Ed25519"},false,["sign"]); unlockedPubRaw=new Uint8Array(rec.pubRaw); scheduleAutolock(); return true;
}
export async function vaultExportPkcs8Base64(){ if(!unlockedPriv) throw new Error("Locked"); const pkcs8=new Uint8Array(await crypto.subtle.exportKey("pkcs8",unlockedPriv)); return btoa(String.fromCharCode(...pkcs8)); }
export async function vaultImportPkcs8Base64(b64,pass){
  const pkcs8=Uint8Array.from(atob(b64),c=>c.charCodeAt(0)); const tmp=await crypto.subtle.generateKey({name:"Ed25519"},true,["sign","verify"]); const pubRaw=new Uint8Array(await crypto.subtle.exportKey("raw",tmp.publicKey));
  const salt=rand(SALT_LEN), iv=rand(IV_LEN); const key=await kdf(pass,salt); const ct=new Uint8Array(await crypto.subtle.encrypt({name:"AES-GCM",iv},key,pkcs8));
  localStorage.setItem(LS, JSON.stringify({salt:btoa(String.fromCharCode(...salt)),iv:btoa(String.fromCharCode(...iv)),ct:btoa(String.fromCharCode(...ct)),pubRaw:btoa(String.fromCharCode(...pubRaw)),iter:PBKDF2_ITER}));
  try{ const db=await idbOpen(); await idbPut(db,{id:REC_ID,salt,iv,ct,pubRaw,iter:PBKDF2_ITER}); }catch{}
  unlockedPriv=await crypto.subtle.importKey("pkcs8",pkcs8,{name:"Ed25519"},false,["sign"]); unlockedPubRaw=pubRaw; scheduleAutolock(); return true;
}
export async function vaultReset(){ try{indexedDB.deleteDatabase(DB);}catch{} try{localStorage.removeItem(LS);}catch{} vaultLock(); }
export function currentRid(){ if(!unlockedPubRaw) return ""; return b58(unlockedPubRaw); }
export async function signEd25519(bytes){ if(!unlockedPriv) throw new Error("Locked"); const sig=new Uint8Array(await crypto.subtle.sign({name:"Ed25519"},unlockedPriv,bytes)); let bin=""; for(let i=0;i<sig.length;i++) bin+=String.fromCharCode(sig[i]); return btoa(bin); }
function b58(b){ let x=0n; for(const v of b) x=(x<<8n)+BigInt(v); const A="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"; let s=""; while(x>0n){const r=Number(x%58n);x/=58n;s=A[r]+s;} for(const v of b){ if(v===0)s="1"+s; else break; } return s||"1"; }

```

### FILE: /var/www/logos/landing/landing/airdrop.html
```
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <title>Airdrop LOGOS</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="Airdrop LOGOS LRB — задания, статус выполнения и прогресс участия." />
  <link rel="stylesheet" href="styles.v20251124.css" />
  <style>
    body{
      margin:0;
      font-family:system-ui,-apple-system,"Inter",sans-serif;
      background:#05030b;
      color:#f5f0ff;
    }
    a{color:inherit;text-decoration:none}
    .airdrop-bg{
      min-height:100vh;
      background:
        radial-gradient(900px 900px at 15% 10%,rgba(169,107,255,.22),transparent 60%),
        radial-gradient(900px 900px at 85% 90%,rgba(90,60,170,.18),transparent 60%),
        radial-gradient(circle at 50% 50%,rgba(255,255,255,.03) 0,transparent 55%);
      position:relative;
      overflow:hidden;
    }
    .airdrop-grid{
      position:absolute;
      inset:0;
      opacity:.18;
      pointer-events:none;
      background-image:
        radial-gradient(circle at center,transparent 0 48%,rgba(255,255,255,.16) 48% 50%,transparent 50% 100%);
      background-size:120px 120px;
      mix-blend-mode:screen;
    }
    .airdrop-page{
      position:relative;
      max-width:960px;
      margin:0 auto;
      padding:32px 16px 64px;
    }
    .airdrop-header{
      display:flex;
      justify-content:space-between;
      align-items:flex-start;
      gap:16px;
      margin-bottom:24px;
    }
    .airdrop-left{
      flex:1 1 auto;
    }
    .airdrop-breadcrumb{
      font-size:12px;
      text-transform:uppercase;
      letter-spacing:.16em;
      color:#b9afd4;
      margin-bottom:8px;
    }
    .airdrop-title{
      font-size:24px;
      font-weight:700;
      margin:0;
    }
    .airdrop-back{
      font-size:14px;
      color:#b9afd4;
      display:inline-flex;
      align-items:center;
      gap:6px;
      margin-top:8px;
    }
    .airdrop-back::before{
      content:"←";
      font-size:14px;
    }
    .airdrop-lang{
      display:flex;
      gap:6px;
      align-items:center;
      justify-content:flex-end;
      flex:0 0 auto;
    }
    .lang-label{
      font-size:11px;
      color:#b9afd4;
      text-transform:uppercase;
      letter-spacing:.12em;
    }
    .lang-btn{
      border-radius:999px;
      padding:4px 10px;
      border:1px solid rgba(255,255,255,.18);
      background:rgba(11,7,32,.9);
      color:#f5f0ff;
      font-size:11px;
      cursor:pointer;
    }
    .lang-btn--active{
      background:linear-gradient(135deg,#ff7ae0,#a96bff);
      color:#1a102b;
      border-color:transparent;
      font-weight:600;
    }

    .airdrop-card{
      background:rgba(10,6,24,.96);
      border-radius:18px;
      padding:20px 20px 18px;
      box-shadow:0 18px 60px rgba(0,0,0,.6);
      border:1px solid rgba(255,255,255,.06);
      margin-bottom:24px;
    }
    .airdrop-card p{margin:0 0 6px;font-size:14px;color:#d2caee}
    .airdrop-status-text{
      font-size:14px;
      margin-top:8px;
      color:#ff9f9f;
    }

    .tasks-title{
      font-size:18px;
      font-weight:600;
      margin-bottom:16px;
    }
    .task{
      display:flex;
      align-items:flex-start;
      gap:12px;
      padding:14px 14px 12px;
      border-radius:14px;
      background:rgba(16,10,40,.95);
      border:1px solid rgba(255,255,255,.05);
      margin-bottom:10px;
    }
    .task:last-child{margin-bottom:0}
    .task__check{
      width:20px;
      height:20px;
      border-radius:6px;
      border:1px solid rgba(255,255,255,.3);
      display:flex;
      align-items:center;
      justify-content:center;
      flex-shrink:0;
      margin-top:2px;
    }
    .task__check input{
      width:16px;
      height:16px;
      accent-color:#a96bff;
      cursor:default;
    }
    .task__body{
      font-size:14px;
    }
    .task__title{
      font-weight:600;
      margin-bottom:2px;
    }
    .task__desc{
      font-size:13px;
      color:#b9afd4;
    }
    .task--done{
      border-color:rgba(169,107,255,.8);
      background:linear-gradient(135deg,rgba(169,107,255,.16),rgba(16,10,40,.98));
    }
    .task--done .task__title{color:#fdf5ff}
    .task--done .task__check input{accent-color:#42d96b}

    .airdrop-footer{
      display:flex;
      flex-wrap:wrap;
      gap:12px;
      align-items:center;
      margin-top:16px;
      font-size:13px;
      color:#b9afd4;
    }
    .airdrop-footer span{white-space:nowrap}

    .btn-row{
      display:flex;
      flex-wrap:wrap;
      gap:10px;
      margin-top:18px;
    }
    .btn{
      border-radius:999px;
      padding:9px 18px;
      font-size:14px;
      border:1px solid rgba(255,255,255,.18);
      background:rgba(11,7,32,.95);
      color:#f5f0ff;
      cursor:pointer;
      display:inline-flex;
      align-items:center;
      gap:8px;
    }
    .btn--primary{
      background:linear-gradient(135deg,#ff7ae0,#a96bff);
      border:none;
      color:#1a102b;
      font-weight:600;
    }
    .btn:disabled{
      opacity:.6;
      cursor:default;
    }
    .btn-icon{
      width:18px;height:18px;border-radius:999px;background:rgba(0,0,0,.3);
      display:flex;align-items:center;justify-content:center;font-size:11px;
    }

    .ref-block{
      font-size:13px;
      margin-top:18px;
      color:#b9afd4;
    }
    .ref-link{
      display:block;
      margin-top:4px;
      font-size:13px;
      word-break:break-all;
      color:#f5f0ff;
    }
    @media(max-width:600px){
      .airdrop-page{padding:20px 14px 48px}
      .airdrop-title{font-size:20px}
      .airdrop-card{padding:16px 14px 14px}
      .airdrop-header{flex-direction:column;align-items:flex-start}
      .airdrop-lang{align-self:flex-end}
    }
  </style>
</head>
<body>
  <div class="airdrop-bg">
    <div class="airdrop-grid"></div>
    <div class="airdrop-page">
      <header class="airdrop-header">
        <div class="airdrop-left">
          <div class="airdrop-breadcrumb" data-i18n="breadcrumb">LOGOS • РЕЗОНАНСНЫЙ БЛОКЧЕЙН</div>
          <h1 class="airdrop-title" data-i18n="title">🎁 Airdrop LOGOS</h1>
          <a href="/" class="airdrop-back" data-i18n="back">На главную</a>
        </div>
        <div class="airdrop-lang">
          <span class="lang-label" data-i18n="lang_label">Язык</span>
          <button type="button" class="lang-btn lang-btn--active" data-lang-switch="ru">RU</button>
          <button type="button" class="lang-btn" data-lang-switch="en">EN</button>
          <button type="button" class="lang-btn" data-lang-switch="de">DE</button>
        </div>
      </header>

      <div class="airdrop-card">
        <p data-i18n="intro">
          Здесь ты видишь список заданий для участия в airdrop LOGOS LRB и статус их выполнения.
          Все проверки по Twitter, Telegram и кошельку проходят через защищённый бэкенд.
        </p>
        <p class="airdrop-status-text" data-status-text>
          Создаём airdrop‑профиль…
        </p>
      </div>

      <div class="airdrop-card">
        <div class="tasks-title" data-i18n="tasks_title">Задания airdrop</div>

        <div class="task" data-task="wallet">
          <div class="task__check">
            <input type="checkbox" disabled />
          </div>
          <div class="task__body">
            <div class="task__title" data-i18n="task_wallet_title">Привязка LOGOS‑кошелька</div>
            <div class="task__desc" data-i18n="task_wallet_desc">
              Подтверди свой LOGOS‑адрес (RID) в airdrop‑профиле.
            </div>
          </div>
        </div>

        <div class="task" data-task="telegram">
          <div class="task__check">
            <input type="checkbox" disabled />
          </div>
          <div class="task__body">
            <div class="task__title" data-i18n="task_tg_title">Подписка на Telegram</div>
            <div class="task__desc" data-i18n="task_tg_desc">
              Подписка на канал @logosblockchain и подтверждение через бота.
            </div>
          </div>
        </div>

        <div class="task" data-task="twitter_follow">
          <div class="task__check">
            <input type="checkbox" disabled />
          </div>
          <div class="task__body">
            <div class="task__title" data-i18n="task_tw_follow_title">Подписка на X (Twitter)</div>
            <div class="task__desc" data-i18n="task_tw_follow_desc">
              Подписка на аккаунт @OfficiaLogosLRB.
            </div>
          </div>
        </div>

        <div class="task" data-task="twitter_like">
          <div class="task__check">
            <input type="checkbox" disabled />
          </div>
          <div class="task__body">
            <div class="task__title" data-i18n="task_tw_like_title">Лайк твита кампании</div>
            <div class="task__desc" data-i18n="task_tw_like_desc">
              Лайк закреплённого твита airdrop‑кампании.
            </div>
          </div>
        </div>

        <div class="task" data-task="twitter_retweet">
          <div class="task__check">
            <input type="checkbox" disabled />
          </div>
          <div class="task__body">
            <div class="task__title" data-i18n="task_tw_rt_title">Ретвит твита кампании</div>
            <div class="task__desc" data-i18n="task_tw_rt_desc">
              Ретвит закреплённого твита в период airdrop.
            </div>
          </div>
        </div>

        <div class="task" data-task="referrals">
          <div class="task__check">
            <input type="checkbox" disabled />
          </div>
          <div class="task__body">
            <div class="task__title" data-i18n="task_ref_title">Рефералы</div>
            <div class="task__desc" data-i18n="task_ref_desc">
              Приглашение друзей по личной ссылке (до 5 человек с полным выполнением заданий).
            </div>
          </div>
        </div>

        <div class="airdrop-footer">
          <span><span data-i18n="points_label">Очки</span>: <strong data-points>0</strong></span>
          <span>• <span data-i18n="refs_label">Рефералы</span>: <strong data-referrals>0 / 5</strong></span>
          <span>• <span data-i18n="rank_label">Позиция в рейтинге</span>: <strong data-rank>—</strong></span>
        </div>

        <div class="btn-row">
          <button class="btn btn--primary" type="button" data-btn-refresh>
            <span class="btn-icon">⟳</span>
            <span data-i18n="btn_check">Проверить выполнение</span>
          </button>
          <a class="btn" href="https://t.me/logosblockchain" target="_blank" rel="noopener">
            <span class="btn-icon">TG</span>
            <span data-i18n="btn_open_tg">Открыть Telegram‑бота</span>
          </a>
          <a class="btn" href="https://x.com/RspLogos" target="_blank" rel="noopener">
            <span class="btn-icon">X</span>
            <span data-i18n="btn_open_x">Перейти в X (Twitter)</span>
          </a>
        </div>

        <div class="ref-block">
          <span data-i18n="ref_title">Твоя личная ссылка (для приглашения друзей):</span>
          <span data-ref-link-state data-i18n="ref_creating">Создаётся…</span>
          <a class="ref-link" href="#" target="_blank" rel="noopener" style="display:none" data-ref-link></a>
        </div>
      </div>
    </div>
  </div>

  <script>
  (() => {
    const I18N = {
      ru: {
        breadcrumb: "LOGOS • РЕЗОНАНСНЫЙ БЛОКЧЕЙН",
        title: "🎁 Airdrop LOGOS",
        back: "На главную",
        lang_label: "Язык",
        intro: "Здесь ты видишь список заданий для участия в airdrop LOGOS LRB и статус их выполнения. Все проверки по Twitter, Telegram и кошельку проходят через защищённый бэкенд.",
        tasks_title: "Задания airdrop",
        task_wallet_title: "Привязка LOGOS‑кошелька",
        task_wallet_desc: "Подтверди свой LOGOS‑адрес (RID) в airdrop‑профиле.",
        task_tg_title: "Подписка на Telegram",
        task_tg_desc: "Подписка на канал @logosblockchain и подтверждение через бота.",
        task_tw_follow_title: "Подписка на X (Twitter)",
        task_tw_follow_desc: "Подписка на аккаунт @OfficiaLogosLRB.",
        task_tw_like_title: "Лайк твита кампании",
        task_tw_like_desc: "Лайк закреплённого твита airdrop‑кампании.",
        task_tw_rt_title: "Ретвит твита кампании",
        task_tw_rt_desc: "Ретвит закреплённого твита в период airdrop.",
        task_ref_title: "Рефералы",
        task_ref_desc: "Приглашение друзей по личной ссылке (до 5 человек с полным выполнением заданий).",
        points_label: "Очки",
        refs_label: "Рефералы",
        rank_label: "Позиция в рейтинге",
        btn_check: "Проверить выполнение",
        btn_open_tg: "Открыть Telegram‑бота",
        btn_open_x: "Перейти в X (Twitter)",
        ref_title: "Твоя личная ссылка (для приглашения друзей):",
        ref_creating: "Создаётся…",
        status_loading: "Создаём airdrop‑профиль…",
        status_ready: "Профиль airdrop создан. Выполни задания и нажми «Проверить выполнение».",
        status_reg_error: "Не удалось создать airdrop‑профиль. Обнови страницу или попробуй позже.",
        status_status_error: "Не удалось получить статус. Попробуй ещё раз позже."
      },
      en: {
        breadcrumb: "LOGOS • RESONANCE BLOCKCHAIN",
        title: "🎁 LOGOS Airdrop",
        back: "Back to main",
        lang_label: "Language",
        intro: "Here you see the list of tasks for the LOGOS LRB airdrop and your completion status. All checks for Twitter, Telegram and wallet go through a protected backend.",
        tasks_title: "Airdrop tasks",
        task_wallet_title: "Bind your LOGOS wallet",
        task_wallet_desc: "Confirm your LOGOS address (RID) in the airdrop profile.",
        task_tg_title: "Telegram subscription",
        task_tg_desc: "Subscribe to the @logosblockchain channel and confirm via the bot.",
        task_tw_follow_title: "Follow in X (Twitter)",
        task_tw_follow_desc: "Follow the @OfficiaLogosLRB account.",
        task_tw_like_title: "Like the campaign tweet",
        task_tw_like_desc: "Like the pinned airdrop campaign tweet.",
        task_tw_rt_title: "Retweet the campaign tweet",
        task_tw_rt_desc: "Retweet the pinned tweet during the airdrop period.",
        task_ref_title: "Referrals",
        task_ref_desc: "Invite friends via your personal link (up to 5 users who complete all tasks).",
        points_label: "Points",
        refs_label: "Referrals",
        rank_label: "Rank",
        btn_check: "Check progress",
        btn_open_tg: "Open Telegram bot",
        btn_open_x: "Open X (Twitter)",
        ref_title: "Your personal link (to invite friends):",
        ref_creating: "Creating…",
        status_loading: "Creating your airdrop profile…",
        status_ready: "Airdrop profile created. Complete tasks and click “Check progress”.",
        status_reg_error: "Failed to create airdrop profile. Refresh the page or try again later.",
        status_status_error: "Failed to fetch status. Please try again later."
      },
      de: {
        breadcrumb: "LOGOS • RESONANZ BLOCKCHAIN",
        title: "🎁 LOGOS Airdrop",
        back: "Zur Startseite",
        lang_label: "Sprache",
        intro: "Hier siehst du die Aufgaben für den LOGOS LRB Airdrop und deinen Fortschritt. Alle Prüfungen für Twitter, Telegram und Wallet laufen über ein geschütztes Backend.",
        tasks_title: "Airdrop‑Aufgaben",
        task_wallet_title: "LOGOS‑Wallet verknüpfen",
        task_wallet_desc: "Bestätige deine LOGOS‑Adresse (RID) im Airdrop‑Profil.",
        task_tg_title: "Telegram‑Abonnement",
        task_tg_desc: "Abonniere den Kanal @logosblockchain und bestätige über den Bot.",
        task_tw_follow_title: "Follow in X (Twitter)",
        task_tw_follow_desc: "Folge dem Account @OfficiaLogosLRB.",
        task_tw_like_title: "Like des Kampagnen‑Tweets",
        task_tw_like_desc: "Like den angehefteten Airdrop‑Kampagnen‑Tweet.",
        task_tw_rt_title: "Retweet des Kampagnen‑Tweets",
        task_tw_rt_desc: "Retweete den angehefteten Tweet während der Airdrop‑Phase.",
        task_ref_title: "Referrals",
        task_ref_desc: "Lade Freunde über deinen persönlichen Link ein (bis zu 5 Nutzer mit vollständigen Aufgaben).",
        points_label: "Punkte",
        refs_label: "Referrals",
        rank_label: "Rang",
        btn_check: "Fortschritt prüfen",
        btn_open_tg: "Telegram‑Bot öffnen",
        btn_open_x: "X (Twitter) öffnen",
        ref_title: "Dein persönlicher Link (zum Einladen von Freunden):",
        ref_creating: "Wird erstellt…",
        status_loading: "Airdrop‑Profil wird erstellt…",
        status_ready: "Airdrop‑Profil erstellt. Erledige die Aufgaben und klicke „Fortschritt prüfen“.",
        status_reg_error: "Airdrop‑Profil konnte nicht erstellt werden. Seite neu laden oder später erneut versuchen.",
        status_status_error: "Status konnte nicht abgerufen werden. Bitte später erneut versuchen."
      }
    };

    const TOKEN_KEY = "logos_airdrop_token";
    const LANG_KEY = "logos_airdrop_lang";
    const API_BASE = "/api/airdrop";

    const els = {
      statusText: document.querySelector("[data-status-text]"),
      tasks: {
        wallet: document.querySelector('[data-task="wallet"]'),
        telegram: document.querySelector('[data-task="telegram"]'),
        twitter_follow: document.querySelector('[data-task="twitter_follow"]'),
        twitter_like: document.querySelector('[data-task="twitter_like"]'),
        twitter_retweet: document.querySelector('[data-task="twitter_retweet"]'),
        referrals: document.querySelector('[data-task="referrals"]'),
      },
      points: document.querySelector("[data-points]"),
      refs: document.querySelector("[data-referrals]"),
      rank: document.querySelector("[data-rank]"),
      refLinkState: document.querySelector("[data-ref-link-state]"),
      refLink: document.querySelector("[data-ref-link]"),
      btnRefresh: document.querySelector("[data-btn-refresh]"),
    };

    let currentLang = "ru";

    function detectLang() {
      try {
        const saved = localStorage.getItem(LANG_KEY);
        if (saved && I18N[saved]) return saved;
      } catch {}
      const nav = (navigator.language || navigator.userLanguage || "").slice(0,2).toLowerCase();
      if (I18N[nav]) return nav;
      return "en";
    }

    function applyLang(lang) {
      if (!I18N[lang]) lang = "en";
      currentLang = lang;
      try { localStorage.setItem(LANG_KEY, lang); } catch {}

      const dict = I18N[lang];

      document.documentElement.lang = lang;

      document.querySelectorAll("[data-lang-switch]").forEach(btn => {
        btn.classList.toggle("lang-btn--active", btn.dataset.langSwitch === lang);
      });

      document.querySelectorAll("[data-i18n]").forEach(node => {
        const key = node.dataset.i18n;
        if (key && dict[key]) node.textContent = dict[key];
      });

      if (els.statusText) {
        const key = els.statusText.dataset.statusKey || "status_ready";
        if (dict[key]) els.statusText.textContent = dict[key];
      }

      if (els.refLinkState) {
        const key = els.refLinkState.dataset.i18n;
        if (key && dict[key]) els.refLinkState.textContent = dict[key];
      }
    }

    function setStatusKey(key) {
      if (!els.statusText) return;
      els.statusText.dataset.statusKey = key;
      const dict = I18N[currentLang];
      if (dict && dict[key]) {
        els.statusText.textContent = dict[key];
      }
    }

    function setTask(name, done) {
      const el = els.tasks[name];
      if (!el) return;
      el.classList.toggle("task--done", !!done);
      const cb = el.querySelector("input[type=checkbox]");
      if (cb) cb.checked = !!done;
    }

    async function apiRegister(refToken) {
      const payload = refToken ? { ref_token: refToken } : {};
      const r = await fetch(API_BASE + "/register_web", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        credentials: "same-origin",
      });
      if (!r.ok) throw new Error("register failed");
      return r.json();
    }

    async function apiStatus(token) {
      const r = await fetch(API_BASE + "/status?token=" + encodeURIComponent(token), {
        credentials: "same-origin",
      });
      if (!r.ok) throw new Error("status failed");
      return r.json();
    }

    function updateFromStatus(s) {
      if (!s || s.error || s.ok === false) {
        setStatusKey("status_status_error");
        return;
      }

      setTask("wallet", s.wallet_bound);
      setTask("telegram", s.telegram_ok);
      setTask("twitter_follow", s.twitter_follow);
      setTask("twitter_like", s.twitter_like);
      setTask("twitter_retweet", s.twitter_retweet);
      setTask("referrals", (s.referrals || 0) >= (s.referrals_target || 5));

      if (els.points) els.points.textContent = s.points ?? 0;
      if (els.refs) els.refs.textContent = (s.referrals || 0) + " / " + (s.referrals_target || 5);
      if (els.rank) {
        els.rank.textContent = s.rank && s.total
          ? s.rank + " / " + s.total
          : "—";
      }

      if (s.referral_url && els.refLink && els.refLinkState) {
        els.refLinkState.style.display = "none";
        els.refLink.style.display = "block";
        els.refLink.href = s.referral_url;
        els.refLink.textContent = s.referral_url;
      }

      setStatusKey("status_ready");
    }

    function getUrlRefParam() {
      try {
        const url = new URL(window.location.href);
        const r = url.searchParams.get("ref");
        return r || null;
      } catch {
        return null;
      }
    }

    function stripRefFromUrl() {
      try {
        const url = new URL(window.location.href);
        if (url.searchParams.has("ref")) {
          url.searchParams.delete("ref");
          window.history.replaceState({}, "", url.toString());
        }
      } catch {}
    }

    async function init() {
      const initialLang = detectLang();
      applyLang(initialLang);

      if (els.statusText) {
        setStatusKey("status_loading");
      }

      let token = null;
      try {
        token = localStorage.getItem(TOKEN_KEY);
      } catch {}

      const refToken = getUrlRefParam();

      if (!token) {
        try {
          const data = await apiRegister(refToken);
          token = data.token;
          if (!token) throw new Error("no token in response");
          try { localStorage.setItem(TOKEN_KEY, token); } catch {}
        } catch (e) {
          console.error(e);
          setStatusKey("status_reg_error");
          return;
        }
      }

      stripRefFromUrl();

      try {
        const st = await apiStatus(token);
        updateFromStatus(st);
      } catch (e) {
        console.error(e);
        setStatusKey("status_status_error");
      }

      if (els.btnRefresh) {
        els.btnRefresh.addEventListener("click", async (ev) => {
          ev.preventDefault();
          let currentToken = null;
          try { currentToken = localStorage.getItem(TOKEN_KEY); } catch {}
          if (!currentToken) return;
          els.btnRefresh.disabled = true;
          try {
            const st = await apiStatus(currentToken);
            updateFromStatus(st);
          } catch (e) {
            console.error(e);
            setStatusKey("status_status_error");
          } finally {
            els.btnRefresh.disabled = false;
          }
        });
      }

      document.querySelectorAll("[data-lang-switch]").forEach(btn => {
        btn.addEventListener("click", () => {
          applyLang(btn.dataset.langSwitch);
        });
      });
    }

    document.addEventListener("DOMContentLoaded", init);
  })();
  </script>
  <script defer src="/shared/airdrop-fix.js??v=20251215"></script>
</body>
</html>

```

### FILE: /var/www/logos/landing/landing/app.bundle.js
```
(function(){
  // ---------- helpers ----------
  const enc = new TextEncoder();
  const $ = (q)=>document.querySelector(q);
  function toast(m){ const t=$("#toast"); if(!t) return; t.textContent=m; t.classList.add("show"); setTimeout(()=>t.classList.remove("show"),2500); }
  function be8(n){ const a=new Uint8Array(8); new DataView(a.buffer).setBigUint64(0, BigInt(n)); return a; }
  function cat(...xs){ let L=0; for(const a of xs) L+=a.length; const out=new Uint8Array(L); let o=0; for(const a of xs){ out.set(a,o); o+=a.length; } return out; }
  const B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";
  function b58(b){ let x=0n; for(const v of b) x=(x<<8n)+BigInt(v); let s=""; while(x>0n){ const r=Number(x%58n); x/=58n; s=B58[r]+s; } for(const v of b){ if(v===0) s="1"+s; else break; } return s||"1"; }
  const API="/api";
  async function apiGet(p){ const r=await fetch(API+p); if(!r.ok) throw new Error(`GET ${p} -> ${r.status}`); return r.json(); }
  async function apiPost(p,b){ const r=await fetch(API+p,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(b)}); if(!r.ok){ const t=await r.text().catch(()=> ""); throw new Error(`POST ${p} -> ${r.status} ${t}`);} return r.json(); }
  function canon(from,to,amount,nonce){ return cat(enc.encode(from),Uint8Array.of(0x7c),enc.encode(to),Uint8Array.of(0x7c),be8(amount),Uint8Array.of(0x7c),be8(nonce)); }
  function renderHistory(items){ const tb=$("#historyTable tbody"); if(!tb) return; tb.innerHTML=""; for(const it of (items||[])){ const e=it.evt||{}; const tr=document.createElement("tr"); let cp="-"; if(e.dir==="out") cp=e.to||"-"; else if(e.dir==="in") cp=e.from||"-"; else cp=e.rid||"-"; tr.innerHTML=`<td>${e.type||"transfer"}</td><td class="mono" style="max-width:260px;overflow:hidden;text-overflow:ellipsis">${cp}</td><td>${e.amount??"-"}</td><td>${e.nonce??"-"}</td><td>${e.height??"-"}</td><td class="mono" style="max-width:280px;overflow:hidden;text-overflow:ellipsis">${e.tx??"-"}</td><td><button class="ghost btnCopyTx" data-tx="${e.tx??""}">copy</button></td>`; tb.appendChild(tr);} }

  // ---------- Secure vault (PBKDF2 + AES-GCM). LocalStorage always; IndexedDB optional ----------
  const DB="logos_secure_v3", STORE="vault", REC_ID="key", LS="logos_secure_v3_backup";
  const PBKDF2_ITER=250000, SALT_LEN=16, IV_LEN=12, AUTOLOCK_MS=5*60*1000;
  let unlockedPriv=null, unlockedPubRaw=null, autolockTimer=null;

  function idbOpen(){return new Promise((res,rej)=>{const r=indexedDB.open(DB,1);r.onupgradeneeded=()=>{const db=r.result;if(!db.objectStoreNames.contains(STORE))db.createObjectStore(STORE,{keyPath:'id'});};r.onsuccess=()=>res(r.result);r.onerror=()=>rej(r.error);});}
  function idbGet(db,id){return new Promise((res,rej)=>{const tx=db.transaction(STORE,"readonly");const rq=tx.objectStore(STORE).get(id);rq.onsuccess=()=>res(rq.result);rq.onerror=()=>rej(rq.error);});}
  function idbPut(db,obj){return new Promise((res,rej)=>{const tx=db.transaction(STORE,"readwrite");tx.objectStore(STORE).put(obj);tx.oncomplete=()=>res();tx.onerror=()=>rej(tx.error);});}
  function rand(n){const a=new Uint8Array(n);crypto.getRandomValues(a);return a;}
  async function kdf(pass,salt){const base=await crypto.subtle.importKey("raw",enc.encode(pass),{name:"PBKDF2"},false,["deriveKey"]);return crypto.subtle.deriveKey({name:"PBKDF2",salt,iterations:PBKDF2_ITER,hash:"SHA-256"},base,{name:"AES-GCM",length:256},false,["encrypt","decrypt"]);}

  async function vaultStatus(){ let rec=null; try{ const db=await idbOpen(); rec=await idbGet(db,REC_ID); }catch{} if(!rec && !localStorage.getItem(LS)) return "empty"; if(unlockedPriv) return "unlocked"; return "locked"; }
  function vaultLock(){ unlockedPriv=null; unlockedPubRaw=null; clearTimeout(autolockTimer); }
  function scheduleAutolock(){ clearTimeout(autolockTimer); autolockTimer=setTimeout(()=>{ vaultLock(); $("#lockOverlay")?.classList.remove("hidden"); }, AUTOLOCK_MS); }

  async function vaultCreateWithPass(pass){
    try{
      // генерим пару в WebCrypto (Ed25519). Большинство новых браузеров поддерживают; иначе покажем ошибку.
      const kp = await crypto.subtle.generateKey({name:"Ed25519"}, true, ["sign","verify"]);
      const pkcs8 = new Uint8Array(await crypto.subtle.exportKey("pkcs8", kp.privateKey));
      const pubRaw= new Uint8Array(await crypto.subtle.exportKey("raw",   kp.publicKey));
      const salt=rand(SALT_LEN), iv=rand(IV_LEN), key=await kdf(pass,salt);
      const ct  = new Uint8Array(await crypto.subtle.encrypt({name:"AES-GCM",iv}, key, pkcs8));

      // резерв в LS — ВСЕГДА
      localStorage.setItem(LS, JSON.stringify({
        salt:btoa(String.fromCharCode(...salt)),
        iv:  btoa(String.fromCharCode(...iv)),
        ct:  btoa(String.fromCharCode(...ct)),
        pubRaw:btoa(String.fromCharCode(...pubRaw)),
        iter:PBKDF2_ITER
      }));
      // попытка IDB — не критично
      try{ const db=await idbOpen(); await idbPut(db,{id:REC_ID, salt, iv, ct, pubRaw, iter:PBKDF2_ITER}); }catch{}

      unlockedPriv = kp.privateKey; unlockedPubRaw = pubRaw; scheduleAutolock();
      return true;
    }catch(e){
      console.error("vaultCreate error", e);
      toast("Ошибка создания ключа. Обнови браузер или установи современный.");
      return false;
    }
  }

  async function vaultUnlock(pass){
    let rec=null; try{ const db=await idbOpen(); rec=await idbGet(db,REC_ID); }catch{}
    if(!rec){ const raw=localStorage.getItem(LS); if(!raw) throw new Error("NoKey"); const o=JSON.parse(raw); rec={salt:Uint8Array.from(atob(o.salt),c=>c.charCodeAt(0)),iv:Uint8Array.from(atob(o.iv),c=>c.charCodeAt(0)),ct:Uint8Array.from(atob(o.ct),c=>c.charCodeAt(0)),pubRaw:Uint8Array.from(atob(o.pubRaw),c=>c.charCodeAt(0)),iter:o.iter}; }
    const key=await kdf(pass,new Uint8Array(rec.salt));
    const pkcs8=await crypto.subtle.decrypt({name:"AES-GCM",iv:new Uint8Array(rec.iv)},key,new Uint8Array(rec.ct)).catch(()=>null);
    if(!pkcs8) throw new Error("BadPassword");
    unlockedPriv=await crypto.subtle.importKey("pkcs8",pkcs8,{name:"Ed25519"},false,["sign"]);
    unlockedPubRaw=new Uint8Array(rec.pubRaw); scheduleAutolock(); return true;
  }

  async function vaultExportPkcs8Base64(){
    if(!unlockedPriv) throw new Error("Locked");
    const pkcs8=new Uint8Array(await crypto.subtle.exportKey("pkcs8",unlockedPriv));
    return btoa(String.fromCharCode(...pkcs8));
  }

  async function vaultImportPkcs8Base64(b64, pass){
    const pkcs8 = Uint8Array.from(atob(b64), c=>c.charCodeAt(0));
    // сгенерим временную pubRaw
    const tmp   = await crypto.subtle.generateKey({name:"Ed25519"},true,["sign","verify"]);
    const pubRaw= new Uint8Array(await crypto.subtle.exportKey("raw", tmp.publicKey));
    const salt=rand(SALT_LEN), iv=rand(IV_LEN), key=await kdf(pass,salt);
    const ct  = new Uint8Array(await crypto.subtle.encrypt({name:"AES-GCM",iv},key,pkcs8));
    localStorage.setItem(LS, JSON.stringify({salt:btoa(String.fromCharCode(...salt)),iv:btoa(String.fromCharCode(...iv)),ct:btoa(String.fromCharCode(...ct)),pubRaw:btoa(String.fromCharCode(...pubRaw)),iter:PBKDF2_ITER}));
    try{ const db=await idbOpen(); await idbPut(db,{id:REC_ID,salt,iv,ct,pubRaw,iter:PBKDF2_ITER}); }catch{}
    unlockedPriv=await crypto.subtle.importKey("pkcs8",pkcs8,{name:"Ed25519"},false,["sign"]);
    unlockedPubRaw=pubRaw; scheduleAutolock(); return true;
  }

  async function vaultReset(){ try{indexedDB.deleteDatabase(DB);}catch{} try{localStorage.removeItem(LS);}catch{} vaultLock(); }

  function currentRid(){ return unlockedPubRaw ? b58(unlockedPubRaw) : ""; }

  async function signEd25519(msg){ if(!unlockedPriv) throw new Error("Locked"); const sig=new Uint8Array(await crypto.subtle.sign({name:"Ed25519"},unlockedPriv,msg)); let bin=""; for(let i=0;i<sig.length;i++) bin+=String.fromCharCode(sig[i]); return btoa(bin); }

  // ---------- Wallet logic ----------
  async function resolveRID(){ const rid=($("#ridInput")?.value||"").trim(); return rid || currentRid(); }

  async function loadPassport(){
    const rid=await resolveRID();
    const [p,s,h]=await Promise.allSettled([apiGet(`/profile/${rid}`),apiGet(`/stake/summary/${rid}`),apiGet(`/history/${rid}?limit=10`)]);
    const prof=p.status==="fulfilled"?p.value:{}; const sum=s.status==="fulfilled"?s.value:{}; const items=h.status==="fulfilled"?(h.value.items||[]):[];
    $("#passportRid").textContent=rid||"—";
    $("#passportBal").textContent=prof.balance??"—";
    $("#passportNonce").textContent=(prof.nonce&&prof.nonce.next)??"—";
    $("#passportHead").textContent=prof.head??"—";
    $("#passportDelegated").textContent=sum.delegated??"—";
    $("#passportEntries").textContent=sum.entries??"—";
    $("#passportClaimable").textContent=sum.claimable??"—";
    renderHistory(items);
  }

  async function refreshStake(){
    const rid=await resolveRID(); if(!rid) return;
    try{ const s=await apiGet(`/stake/summary/${rid}`); $("#chipDelegated").textContent=String(s.delegated??0); $("#chipEntries").textContent=String(s.entries??0); $("#chipClaimable").textContent=String(s.claimable??0); }catch{}
  }

  async function syncProfile(){
    const rid=await resolveRID(); if(!rid){ $("#balanceBadge").textContent="—"; $("#nonceBadge").textContent="—"; return; }
    const prof=await apiGet(`/profile/${rid}`);
    $("#balanceBadge").textContent=prof.balance??"—";
    $("#nonceBadge").textContent=(prof.nonce&&prof.nonce.next)??"—";
    await refreshStake(); await loadPassport();
  }

  async function showHistory(){ const rid=await resolveRID(); if(!rid) return; const h=await apiGet(`/history/${rid}?limit=50`); renderHistory(h.items||[]); }

  async function onSend(){
    const from=currentRid(), to=($("#toRid")?.value||"").trim(), amount=Number($("#sendAmount")?.value||0);
    if(!from){ toast("Кошелёк заблокирован"); $("#lockOverlay").classList.remove("hidden"); return; }
    if(!to||!amount){ toast("Укажи получателя и сумму"); return; }
    const nn=await apiGet(`/nonce/${from}`); const nonce=nn.next;
    const sigB64=await signEd25519( canon(from,to,amount,nonce) );
    const res=await apiPost(`/submit_tx`,{from,to,amount,nonce,sig:sigB64});
    toast(res?.status==="queued"?"Транзакция отправлена":"Отправка выполнена");
    await syncProfile(); await showHistory(); await loadPassport();
  }

  // ---------- Secure overlay handlers ----------
  let tries=5;
  async function updateLockView(){
    $("#rpHost").textContent = location.host;
    const st = await vaultStatus();
    if(st==="empty"){ $("#lockStepSetup").classList.remove("hidden"); $("#lockStepUnlock").classList.add("hidden"); }
    if(st==="locked"){ $("#lockStepSetup").classList.add("hidden"); $("#lockStepUnlock").classList.remove("hidden"); }
    if(st==="unlocked"){ $("#lockOverlay").classList.add("hidden"); await afterUnlock(); }
  }
  async function afterUnlock(){
    const rid=currentRid(); if(rid){ $("#ridInput").value=rid; $("#ridValidator").value=rid; $("#passportRid").textContent=rid; }
    await syncProfile(); await loadPassport();
  }
  async function handleCreate(){
    const p1=$("#pwNew").value.trim(), p2=$("#pwNew2").value.trim();
    if(p1.length<8){ toast("Пароль минимум 8 символов"); return; }
    if(p1!==p2){ toast("Пароли не совпадают"); return; }
    toast("Создаём и шифруем ключ…");
    const ok=await vaultCreateWithPass(p1);
    if(!ok){ toast("Не удалось создать ключ"); return; }
    $("#lockOverlay").classList.add("hidden"); tries=5; await afterUnlock();
  }
  async function handleUnlock(){
    const p=$("#pwUnlock").value.trim();
    try{ await vaultUnlock(p); $("#lockOverlay").classList.add("hidden"); tries=5; await afterUnlock(); }
    catch(e){ tries--; $("#triesLeft2").textContent=String(tries); toast(tries>0?"Неверный пароль":"Слишком много попыток — кошелёк сброшен"); if(tries<=0){ await (async()=>{try{indexedDB.deleteDatabase(DB);}catch{} try{localStorage.removeItem(LS);}catch{}})(); location.reload(); } }
  }
  async function handleForgot(){ if(confirm("Очистить локальный ключ и настройки?")){ try{indexedDB.deleteDatabase(DB);}catch{} try{localStorage.removeItem(LS);}catch{} location.reload(); } }
  async function handleImportSetup(){
    const b64=prompt("Вставь PKCS8 Base64 ключ"); if(!b64) return;
    const pass=prompt("Создай пароль шифрования (≥8)"); if(!pass||pass.length<8){ toast("Пароль ≥ 8"); return; }
    const ok=await vaultImportPkcs8Base64(b64, pass);
    if(!ok){ toast("Импорт не удался"); return; }
    $("#lockOverlay").classList.add("hidden"); tries=5; await afterUnlock();
  }
  async function handleImportUnlock(){
    const b64=prompt("Вставь PKCS8 Base64 ключ"); if(!b64) return;
    const pass=prompt("Пароль шифрования (≥8)"); if(!pass||pass.length<8){ toast("Пароль ≥ 8"); return; }
    const ok=await vaultImportPkcs8Base64(b64, pass);
    if(!ok){ toast("Импорт не удался"); return; }
    $("#lockOverlay").classList.add("hidden"); tries=5; await afterUnlock();
  }

  // ---------- bindings ----------
  document.addEventListener("click",e=>{ const b=e.target.closest(".btnCopyTx"); if(b){ navigator.clipboard.writeText(b.dataset.tx||"").then(()=>toast("Скопировано")).catch(()=>toast("Не удалось скопировать")); } });

  document.addEventListener("DOMContentLoaded", ()=>{
    // secure
    $("#rpHost").textContent = location.host;
    $("#btnCreate").addEventListener("click", handleCreate);
    $("#btnUnlock").addEventListener("click", handleUnlock);
    $("#btnForgot").addEventListener("click", handleForgot);
    $("#btnImportSetup").addEventListener("click", handleImportSetup);
    $("#btnImportUnlock").addEventListener("click", handleImportUnlock);

    // wallet
    $("#btnBalance").addEventListener("click", ()=>syncProfile().catch(e=>toast(String(e))));
    $("#btnSync").addEventListener("click", ()=>syncProfile().catch(e=>toast(String(e))));
    $("#btnShowHist").addEventListener("click", ()=>showHistory().catch(e=>toast(String(e))));
    $("#btnStakeDelegate").addEventListener("click", async ()=>{ const rid=(await resolveRID()); const amount=Number($("#stakeAmount").value||0); const r=await apiPost(`/stake/delegate`,{validator:rid,amount}); toast(r.ok?"Delegated":"Delegate failed"); await refreshStake(); await loadPassport(); });
    $("#btnStakeUndelegate").addEventListener("click", async ()=>{ const rid=(await resolveRID()); const amount=Number($("#unstakeAmount").value||0); const r=await apiPost(`/stake/undelegate`,{validator:rid,amount}); toast(r.ok?"Undelegated":"Undelegate failed"); await refreshStake(); await loadPassport(); });
    $("#btnStakeClaim").addEventListener("click", async ()=>{ const rid=(await resolveRID()); const r=await apiPost(`/stake/claim`,{rid}); toast(r.ok?`Claimed ${r.claimed}`:"Claim failed"); await refreshStake(); await loadPassport(); });
    $("#btnSend").addEventListener("click", ()=>onSend().catch(e=>toast(String(e))));
    $("#btnCopyRid").addEventListener("click", ()=>{ const rid=$("#passportRid").textContent||$("#ridInput").value||""; navigator.clipboard.writeText(rid).then(()=>toast("RID скопирован")); });

    updateLockView().catch(()=>toast("Ошибка инициализации"));
  });
})();

```

### FILE: /var/www/logos/landing/landing/app.v20251124.js
```
(() => {
  const dicts = {
    en: {
      menu_label_lang: "Language",
      menu_label_nav: "Navigation",
      menu_label_actions: "Actions",
      menu_label_social: "Community",
      nav_intro: "Overview",
      nav_speed: "Speed",
      nav_privacy: "Privacy",
      nav_fees: "Fees",
      nav_reliability: "Reliability",
      nav_tech: "Technology",
      nav_rsp: "LOGOS RSP",
      nav_agi: "LOGOS-AGI",
      nav_better: "Why LOGOS",
      nav_short: "In short",
      menu_presale: "Presale / Airdrop (soon)",
      menu_staking: "Staking (soon)",
      menu_telegram: "Telegram",
      menu_twitter: "X (Twitter)",
      menu_email: "Email: simbiotai@proton.me",

      intro_title: "LOGOS – a next-generation blockchain built on resonance architecture",
      intro_p1: "LOGOS is not just another network. It is a new-generation blockchain built around speed, privacy and a deep resonance architecture.",
      intro_p2: "We created an L1 that works fast and stays stable without unnecessary complexity. Blocks are formed instantly, the network handles high traffic, fees remain minimal and the level of privacy is something most mainstream chains simply do not offer today.",
      intro_p3: "LOGOS is the foundation for a new digital environment ready for millions of users.",

      speed_title: "Speed and performance",
      speed_p: "We tested the network under real conditions, not just on paper. Peak results reached 2,000+ transactions per second with stable finality and no forks. The architecture is designed to go further: with more nodes and phase optimisation, 10,000+ tx/s is achievable without sacrificing stability. The idea is simple: a blockchain should feel as fast as modern payment systems — and LOGOS behaves exactly like that.",

      privacy_title: "Privacy on a new level",
      privacy_p1: "From day one LOGOS was designed as a network where:",
      privacy_li1: "a user cannot be directly tied to a transaction;",
      privacy_li2: "packet routes are difficult to trace;",
      privacy_li3: "metadata leakage is minimised;",
      privacy_li4: "there are no obvious network fingerprints;",
      privacy_li5: "there are no standard tracking points.",
      privacy_p2: "Privacy in LOGOS is not a switch or a feature. It is baked into the architecture.",

      fees_title: "Low fees and clean finality",
      fees_p: "Blocks do not compete, conflict or roll back. Each transaction passes once and is recorded permanently. Fees are among the lowest across L1 chains because we avoid heavy computation and bloated contracts, so even under serious load basic transfers stay affordable.",

      reliability_title: "Reliability and production readiness",
      reliability_p: "The network is ready for production use: orchestration tools spin up nodes in seconds, bridges work securely, and there is staking, archiving and balancing. LOGOS nodes can run on ordinary servers, and the infrastructure is stress‑tested under high load. LOGOS is not an experiment – it is an autonomous, working network.",

      technology_title: "The technology behind LOGOS",
      technology_p: "LOGOS is built on a resonance‑symbolic architecture – our own know‑how for organising data and synchronisation. Instead of relying on heavy computation and overly complex consensus schemes, we use rhythm, structure and phase dynamics. This makes the network more stable under pressure, quicker to react to spikes and harder to attack on the network layer, while keeping scaling straightforward.",

      rsp_title: "LOGOS RSP – communication without traces",
      rsp_p: "At the core of the ecosystem lies the confidential communication protocol LOGOS RSP. In practice it means communication without classic IP routing and with minimal digital traces, resilient to interception and analysis. RSP can operate not only over the internet but also via alternative carriers – light, sound, radio and offline channels. It pushes LOGOS far beyond a typical blockchain. Technical details remain closed – this is our key innovation.",

      agi_title: "LOGOS-AGI – a new architectural layer",
      agi_p: "We are also building LOGOS‑AGI – a new type of artificial intelligence. It does not rely on huge neural networks and massive datasets, but on resonance logic and symbolic structures that underlie the whole system. Early prototypes show that such AI can work without GPUs, learn without giant datasets and discover its own patterns, operating on meaning rather than pure statistics. This turns LOGOS from a blockchain into a platform for future autonomous systems.",

      better_title: "Why LOGOS is different",
      better_intro: "LOGOS is built for the real world, not just for slides. In short, our advantages:",
      better_item1: "Real speed, proven by load tests.",
      better_item2: "Genuine privacy instead of pseudo‑anonymity.",
      better_item3: "Minimal transaction fees.",
      better_item4: "Instant finality without forks or rollbacks.",
      better_item5: "Resilience to network attacks and load spikes.",
      better_item6: "Straightforward scaling of the network.",
      better_item7: "Infrastructure ready for millions of users.",
      better_item8: "A unique resonance architecture you will not find in any other chain.",

      short_title: "In short",
      short_p: "LOGOS is a next‑generation L1 blockchain built on resonance architecture: high speed, low fees, adaptive behaviour and strong privacy. Inside we develop our own communication protocol and the LOGOS‑AGI direction. We are not building just another crypto platform – we are building the base layer for Web4.",

      footer_note: "LOGOS LRB • Resonance Blockchain • Ready for millions of users"
    },

    de: {
      menu_label_lang: "Sprache",
      menu_label_nav: "Navigation",
      menu_label_actions: "Aktionen",
      menu_label_social: "Community",
      nav_intro: "Überblick",
      nav_speed: "Geschwindigkeit",
      nav_privacy: "Privatsphäre",
      nav_fees: "Gebühren",
      nav_reliability: "Stabilität",
      nav_tech: "Technologie",
      nav_rsp: "LOGOS RSP",
      nav_agi: "LOGOS‑AGI",
      nav_better: "Vorteile",
      nav_short: "Kurzfassung",
      menu_presale: "Presale / Airdrop (bald)",
      menu_staking: "Staking (bald)",
      menu_telegram: "Telegram",
      menu_twitter: "X (Twitter)",
      menu_email: "Email: simbiotai@proton.me",

      intro_title: "LOGOS – Blockchain der nächsten Generation auf Resonanz‑Architektur",
      intro_p1: "LOGOS ist nicht einfach eine weitere Chain, sondern eine Blockchain der nächsten Generation – gebaut für Geschwindigkeit, Privatsphäre und eine tiefe Resonanz‑Architektur.",
      intro_p2: "Wir haben eine L1 entwickelt, die schnell und stabil läuft ohne überflüssige Komplexität. Blöcke entstehen praktisch sofort, das Netzwerk trägt hohe Last, Gebühren bleiben minimal und das Datenschutzniveau ist höher als bei den meisten Mainstream‑Netzen.",
      intro_p3: "LOGOS ist ein Fundament für eine neue digitale Umgebung, bereit für Millionen Nutzer.",

      speed_title: "Geschwindigkeit und Performance",
      speed_p: "In Lasttests verarbeitete LOGOS tausende Transaktionen pro Sekunde mit stabiler Finalität und ohne Forks. Die Architektur ist darauf ausgelegt, bei mehr Nodes und Optimierungen in den Bereich von 10.000+ tx/s zu gehen – ohne Stabilität zu verlieren. Ziel: Eine Blockchain, die sich so schnell anfühlt wie moderne Bezahlsysteme.",

      privacy_title: "Privatsphäre auf neuem Niveau",
      privacy_p1: "LOGOS wurde von Anfang an so entworfen, dass:",
      privacy_li1: "Nutzer nicht direkt mit einzelnen Transaktionen verknüpft werden können;",
      privacy_li2: "Routen schwer nachvollziehbar sind;",
      privacy_li3: "Metadaten auf ein Minimum reduziert werden;",
      privacy_li4: "keine offensichtlichen Fingerabdrücke sichtbar sind;",
      privacy_li5: "es keine Standard‑Tracking‑Punkte gibt.",
      privacy_p2: "Privatsphäre ist hier kein Add‑on, sondern Teil der Basisarchitektur.",

      fees_title: "Niedrige Gebühren und saubere Finalität",
      fees_p: "Blöcke konkurrieren nicht miteinander und werden nicht zurückgesetzt. Jede Transaktion wird einmal verarbeitet und dauerhaft geschrieben. Durch die leichte Architektur ohne unnötige Rechenlast gehören die Gebühren zu den niedrigsten im L1‑Bereich.",

      reliability_title: "Zuverlässigkeit und Belastbarkeit",
      reliability_p: "Das Netzwerk ist produktionsreif: Orchestrierungstools starten Nodes in Sekunden, Bridges arbeiten sicher, Staking und Archivierung sind integriert. LOGOS‑Nodes laufen auf normalen Servern, die Infrastruktur wird unter hoher Last gestresst. LOGOS ist ein laufendes Netzwerk, kein Experiment.",

      technology_title: "Technologie hinter LOGOS",
      technology_p: "LOGOS basiert auf einer resonanz‑symbolischen Architektur – unserem eigenen Ansatz für Datenorganisation und Synchronisation. Statt auf schwere Rechenarbeit und komplizierte Konsens‑Schemata zu setzen, nutzen wir Rhythmus, Struktur und Phasenprozesse. Das macht das System stabiler unter Last und leichter skalierbar.",

      rsp_title: "LOGOS RSP – Kommunikation ohne Spuren",
      rsp_p: "Im Zentrum der Ökosphäre steht das vertrauliche Kommunikationsprotokoll LOGOS RSP. In der Praxis bedeutet das Kommunikation mit minimalen digitalen Spuren, robust gegen Abhören und Analyse – auch über alternative Träger wie Licht, Ton, Funk oder Offline‑Kanäle. Die Details bleiben bewusst geschlossen.",

      agi_title: "LOGOS‑AGI – eine neue Schicht",
      agi_p: "LOGOS‑AGI ist unser Ansatz für eine neue Art von KI, die eher auf Resonanzlogik und symbolischen Strukturen als auf riesigen Netzen und Datensätzen basiert. Erste Prototypen zeigen: Arbeiten ohne GPU, Lernen ohne Gigadaten, Fokus auf Bedeutung statt Statistik. Damit wird LOGOS zur Plattform für zukünftige autonome Systeme.",

      better_title: "Warum LOGOS anders ist",
      better_intro: "LOGOS wurde für reale Nutzung gebaut, nicht nur für Slides. Unsere wichtigsten Vorteile:",
      better_item1: "Echte Geschwindigkeit, in Lasttests nachgewiesen.",
      better_item2: "Konsequente Privatsphäre statt Pseudo‑Anonymität.",
      better_item3: "Sehr niedrige Gebühren.",
      better_item4: "Schnelle Finalität ohne Forks oder Rollbacks.",
      better_item5: "Robust gegenüber Netzangriffen und Lastspitzen.",
      better_item6: "Einfache Skalierung des Netzwerks.",
      better_item7: "Infrastruktur für Millionen Nutzer.",
      better_item8: "Eine einzigartige Resonanz‑Architektur, die andere Chains nicht haben.",

      short_title: "Kurz und knapp",
      short_p: "LOGOS ist eine L1‑Blockchain der nächsten Generation mit Resonanz‑Architektur: hohe Geschwindigkeit, niedrige Gebühren, adaptive Netzlogik und starke Privatsphäre. Dazu kommen ein eigener Kommunikationsansatz und die Linie LOGOS‑AGI – ein Fundament für Web4.",
      footer_note: "LOGOS LRB • Resonanz‑Blockchain • Für Millionen Nutzer gebaut"
    }
  };

  const transEls = Array.from(document.querySelectorAll("[data-i18n]"));
  transEls.forEach(el => {
    if (!el.dataset.i18nRu) {
      el.dataset.i18nRu = el.textContent.trim();
    }
  });

  function setActiveLang(lang){
    document.querySelectorAll("[data-lang-btn]").forEach(btn => {
      btn.classList.toggle("is-active", btn.dataset.langBtn === lang);
    });
  }

  function applyLang(lang){
    if (!dicts[lang]) lang = "ru";

    if (lang === "ru"){
      document.documentElement.lang = "ru";
      document.documentElement.dataset.lang = "ru";
      transEls.forEach(el => {
        if (el.dataset.i18nRu) el.textContent = el.dataset.i18nRu;
      });
      localStorage.setItem("logos_lang","ru");
      setActiveLang("ru");
      return;
    }

    const dict = dicts[lang];
    document.documentElement.lang = lang;
    document.documentElement.dataset.lang = lang;

    transEls.forEach(el => {
      const key = el.getAttribute("data-i18n");
      if (dict[key]) el.textContent = dict[key];
    });

    localStorage.setItem("logos_lang",lang);
    setActiveLang(lang);
  }

  // меню
  const body  = document.body;
  const menu  = document.querySelector("[data-menu]");
  const toggle = document.querySelector("[data-menu-toggle]");

  if (menu && toggle){
    toggle.addEventListener("click", () => {
      const hidden = menu.hasAttribute("hidden");
      if (hidden){
        menu.removeAttribute("hidden");
        body.classList.add("menu-open");
        toggle.setAttribute("aria-expanded","true");
      } else {
        menu.setAttribute("hidden","");
        body.classList.remove("menu-open");
        toggle.setAttribute("aria-expanded","false");
      }
    });

    menu.querySelectorAll("[data-menu-link]").forEach(link => {
      link.addEventListener("click", () => {
        menu.setAttribute("hidden","");
        body.classList.remove("menu-open");
        toggle.setAttribute("aria-expanded","false");
      });
    });
  }

  document.querySelectorAll("[data-lang-btn]").forEach(btn => {
    btn.addEventListener("click", () => applyLang(btn.dataset.langBtn));
  });

  const saved = localStorage.getItem("logos_lang") || "ru";
  applyLang(saved);
})();

```

### FILE: /var/www/logos/landing/landing/i18n/de.json
```
{
  "nav_about":"Über",
  "nav_tech":"Technologie",
  "nav_token":"Token",
  "nav_stake":"Staking",
  "nav_comm":"Community",

  "badge_main":"L1 • 81M LGN • Anonym • Deflationär • Quantenresistent",
  "hero_title":"Lebendige Resonanz‑Blockchain für die nächste Ära.",
  "hero_sub":"LOGOS ist eine Resonanz‑L1‑Blockchain. Unser erster Schritt in Richtung Web4 – ein Netzwerk, in dem Menschen, Wert und KI denselben sicheren Raum teilen.",
  "btn_learn_more":"Mehr erfahren",
  "btn_download_apk":"Sichere APK herunterladen",
  "meta_supply":"Gesamtangebot: 81 000 000 LGN",
  "meta_ready":"Für echten Nutzen und Massenadoption gebaut",

  "about_title":"Was ist LOGOS?",
  "about_text":"LOGOS ist eine resonanzgetriebene L1‑Blockchain mit dem RSP‑Sicherheitsprotokoll im Kern. Ziel ist ein Netzwerk, das reale Last trägt, Privatsphäre respektiert und bereit für Web4‑Produkte ist – von Payments bis KI‑Services.",
  "card1_title":"Resonanzkern",
  "card1_text":"Das RSP‑Protokoll und Phasenfilter halten das Netzwerk selbst bei Aktivitätsspitzen stabil.",
  "card2_title":"Echte Privatsphäre",
  "card2_text":"Minimale Metadaten, strikte Nonce‑Policy, Phasenmischung des Traffics und integrierter Schutz vor Spam und Angriffen.",
  "card3_title":"Produktionsreif",
  "card3_text":"Rust‑Kern, Axum REST, Prometheus/Grafana, Bridge‑Journal, Health‑Checks und Archiv – alles, was eine ernsthafte L1‑Chain braucht.",

  "tech_title":"LOGOS‑Technologie",
  "tech_item1":"Lebendiges Resonanz‑Protokoll: das Netzwerk reagiert auf Last und Anomalien und bleibt dabei vorhersagbar.",
  "tech_item2":"RSP‑Sicherheitsprotokoll: beobachtet Spam‑Wellen, Zensurversuche und ungewöhnliche Wertströme und begrenzt schädliche Aktivität gezielt.",
  "tech_item3":"Grundlage für KI und Agenten: LOGOS ist als Umgebung für autonome Agenten und zukünftige AGI entworfen – mit Risikomanagement ohne unnötige Datenausleitung.",
  "tech_item4":"Stark innen, einfach außen: Nutzer sehen Wallet, Transfers und Staking – die Komplexität steckt im Protokoll.",
  "tech_item5":"Web4‑Ökosystem: Produkte auf LOGOS – Payments, Games, DeFi und KI‑Services – erhalten Privatsphäre und Resilienz direkt aus der Basis.",
  "tech_note":"LOGOS will ein Fundament für das nächste Internet (Web4) sein, in dem Menschen, Wert und KI in einem stabilen, privaten Netzwerk koordiniert werden.",

  "token_title":"LGN‑Tokenomics",
  "token_text":"LGN ist der Basistoken von LOGOS. Fixes Angebot von 81 000 000 LGN mit deflationärem Modell und Fokus auf langfristige Teilnehmer.",
  "token_staking":"Staking & Holder",
  "token_rcp":"RSP‑Sicherheitsprotokoll",
  "token_liq":"Liquidität (DEX/CEX)",
  "token_stab":"Stabilisierungsfonds",
  "token_core":"Founder & Core Dev",
  "token_airdrop":"Airdrop & DAO",

  "stake_title":"Staking & RSP‑Protokoll",
  "stake_text":"LGN‑Staking verbindet Netzwerksicherheit und das RSP‑Protokoll mit langfristigen Anreizen für Holder.",
  "stake_item1_title":"Basis‑Staking",
  "stake_item1_text":"Du delegierst LGN an Validatoren und erhältst Rewards für die Sicherung des Netzwerks.",
  "stake_item2_title":"RSP‑Protokoll",
  "stake_item2_text":"Eine Sicherheitsschicht, die Netzwerkphase und Teilnehmerverhalten berücksichtigt und Staking sowie Ökonomie verstärkt.",
  "stake_item3_title":"Missionen & Rewards",
  "stake_item3_text":"On‑Chain‑Aktivität, Community‑Quests und Airdrop‑Mechaniken oben auf dem Basis‑Staking.",

  "comm_title":"Community & Kanäle",
  "comm_text":"Tritt dem Feld bei: Updates, Airdrops, Missionen, Staking und AI‑native Experimente.",
  "comm_email":"Email: simbiotai@proton.me",
  "comm_staking":"LGN‑Staking",

  "footer_note":"Resonanz‑Blockchain • Für Millionen Nutzer gebaut"
}

```

### FILE: /var/www/logos/landing/landing/i18n/en.json
```
{
  "nav_about":"About",
  "nav_tech":"Technology",
  "nav_token":"Token",
  "nav_stake":"Staking",
  "nav_comm":"Community",

  "badge_main":"L1 • 81M LGN • Anonymous • Deflationary • Quantum‑resistant",
  "hero_title":"Living resonance blockchain for the next era.",
  "hero_sub":"LOGOS is a resonance‑based L1 blockchain. It is our first step towards Web4 – a network where people, value and AI share the same secure space.",
  "btn_learn_more":"Learn more",
  "btn_download_apk":"Download secure APK",
  "meta_supply":"Total supply: 81 000 000 LGN",
  "meta_ready":"Built for real utility & mass adoption",

  "about_title":"What is LOGOS?",
  "about_text":"LOGOS is a resonance‑driven L1 blockchain built around the RSP security protocol. We focus on a network that can handle real traffic, respects privacy and is ready for Web4‑native products – from payments to AI services.",
  "card1_title":"Resonant core",
  "card1_text":"The RSP protocol and phase filters keep the network stable even during sharp activity spikes.",
  "card2_title":"Real privacy",
  "card2_text":"Minimal metadata, strict nonce policy, phase‑mixed traffic and built‑in protection against spam and attacks.",
  "card3_title":"Production‑grade",
  "card3_text":"Rust core, Axum REST, Prometheus/Grafana, bridge journal, health checks and archive – everything a serious L1 needs.",

  "tech_title":"LOGOS technology",
  "tech_item1":"Living resonance protocol: the network reacts to load and anomalies while keeping finalisation and behaviour predictable.",
  "tech_item2":"RSP security protocol: observes spam waves, censorship attempts and abnormal value flows, gently limiting harmful activity.",
  "tech_item3":"Base layer for AI and agents: LOGOS is designed as an environment where autonomous agents and future AGI can manage risk and capital without leaking unnecessary data.",
  "tech_item4":"Strong internals, simple outside: users see a wallet, transfers and staking – the complexity lives inside the protocol.",
  "tech_item5":"Web4 ecosystem: products on top of LOGOS – payments, games, DeFi and AI services – get privacy and resilience from the base layer.",
  "tech_note":"LOGOS aims to be a foundation for the next internet (Web4), where people, value and AI coordinate inside one stable, private network.",

  "token_title":"LGN tokenomics",
  "token_text":"LGN is the base token of LOGOS. Fixed supply of 81 000 000 LGN with a deflationary model focused on long‑term participants.",
  "token_staking":"Staking & holders",
  "token_rcp":"RSP security protocol",
  "token_liq":"Liquidity (DEX/CEX)",
  "token_stab":"Stability fund",
  "token_core":"Founder & core dev",
  "token_airdrop":"Airdrop & DAO",

  "stake_title":"Staking & RSP protocol",
  "stake_text":"Staking LGN ties network security and the RSP protocol to long‑term incentives for holders.",
  "stake_item1_title":"Base staking",
  "stake_item1_text":"Delegate LGN to validators and receive rewards for helping secure the network.",
  "stake_item2_title":"RSP protocol",
  "stake_item2_text":"A security layer that takes network phase and participant behaviour into account, reinforcing staking and the whole economy.",
  "stake_item3_title":"Missions & rewards",
  "stake_item3_text":"On‑chain activity, community quests and airdrop mechanics built on top of base staking.",

  "comm_title":"Community & channels",
  "comm_text":"Join the field: updates, airdrop campaigns, missions, staking and AI‑native experiments.",
  "comm_email":"Email: simbiotai@proton.me",
  "comm_staking":"LGN staking",

  "footer_note":"Resonance blockchain • Built for millions of users"
}

```

### FILE: /var/www/logos/landing/landing/i18n/ru.json
```
{
  "nav_about":"О проекте",
  "nav_tech":"Технология",
  "nav_token":"Токен",
  "nav_stake":"Стейкинг",
  "nav_comm":"Сообщество",

  "badge_main":"L1 • 81M LGN • Анонимность • Дефляция • Квантовая устойчивость",
  "hero_title":"Живой резонансный блокчейн нового уровня.",
  "hero_sub":"LOGOS — резонансный L1‑блокчейн следующего поколения. Мы делаем первый шаг к Web4: сети, где люди, ценность и ИИ работают в одном защищённом пространстве.",
  "btn_learn_more":"Подробнее",
  "btn_download_apk":"Скачать безопасный APK",
  "meta_supply":"Общая эмиссия: 81 000 000 LGN",
  "meta_ready":"Создан для реальной пользы и массового использования",

  "about_title":"Что такое LOGOS",
  "about_text":"LOGOS — резонансный L1‑блокчейн с RSP‑протоколом безопасности. Мы делаем сеть, которая выдерживает реальную нагрузку, бережно относится к приватности и готова к Web4‑продуктам — от платёжных систем до ИИ‑сервисов.",
  "card1_title":"Резонансное ядро",
  "card1_text":"RSP‑протокол и фазовые фильтры удерживают сеть стабильной даже при резких всплесках активности.",
  "card2_title":"Реальная приватность",
  "card2_text":"Минимум метаданных, строгая nonce‑политика, фазовое смешение трафика и встроенная защита от спама и атак.",
  "card3_title":"Боевой уровень",
  "card3_text":"Rust‑ядро, Axum REST, Prometheus/Grafana, журнал моста, health‑проверки и архив — всё, что нужно серьёзной L1‑сети.",

  "tech_title":"Технология LOGOS",
  "tech_item1":"Живой резонансный протокол: сеть реагирует на нагрузку и аномалии, сохраняя предсказуемость и финализацию блоков.",
  "tech_item2":"RSP‑протокол безопасности: отслеживает всплески спама, попытки цензуры и странные потоки средств, мягко ограничивая вредную активность.",
  "tech_item3":"База для ИИ и агентов: LOGOS проектируется как среда, где автономные агенты и будущая AGI‑архитектура управляют рисками и капиталом без лишней утечки данных.",
  "tech_item4":"Сильное ядро, простая внешняя оболочка: пользователю доступны кошелёк, переводы и стейкинг, вся сложность спрятана внутри протокола.",
  "tech_item5":"Экосистема Web4: поверх LOGOS растут продукты — платёжные сценарии, игры, DeFi и AI‑сервисы, которым важны приватность и отказоустойчивость.",
  "tech_note":"LOGOS — фундамент для следующего интернета (Web4), где люди, ценность и ИИ координируются в одной устойчивой и приватной сети.",

  "token_title":"LGN: токеномика",
  "token_text":"LGN — базовый токен LOGOS. Общая эмиссия 81 000 000 LGN. Модель — дефляционная, с акцентом на долгосрочных держателей и участников сети.",
  "token_staking":"Staking / Holders",
  "token_rcp":"RSP‑протокол безопасности",
  "token_liq":"Ликвидность (DEX/CEX)",
  "token_stab":"Фонд стабильности",
  "token_core":"Создатель / Core Dev",
  "token_airdrop":"Airdrop / DAO",

  "stake_title":"Стейкинг и RSP‑протокол",
  "stake_text":"Стейкинг LGN связывает безопасность сети и RSP‑протокол с долгосрочными стимулами для держателей.",
  "stake_item1_title":"Базовый стейкинг",
  "stake_item1_text":"Делегируешь LGN валидаторам и получаешь вознаграждение за участие в защите сети.",
  "stake_item2_title":"RSP‑протокол",
  "stake_item2_text":"Уровень безопасности, который учитывает фазу сети и поведение участников, усиливая защиту стейкинга и всей экономики.",
  "stake_item3_title":"Миссии и награды",
  "stake_item3_text":"On‑chain‑активности, задания для сообщества и airdrop‑механики поверх базового стейкинга.",

  "comm_title":"Сообщество и каналы",
  "comm_text":"Присоединяйся: обновления, airdrop‑кампании, миссии, стейкинг и эксперименты с AI‑нативными протоколами.",
  "comm_email":"Email: simbiotai@proton.me",
  "comm_staking":"Стейкинг LGN",

  "footer_note":"Resonance Blockchain • Готов к миллионам пользователей"
}

```

### FILE: /var/www/logos/landing/landing/index.html
```
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <title>LOGOS — Resonance Blockchain</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="LOGOS — L1-блокчейн нового поколения на резонансной архитектуре: скорость, приватность, низкие комиссии и устойчивость под нагрузкой для миллионов пользователей." />
  <link rel="stylesheet" href="styles.v20251124.css" />
  <style>
    :root{
      --bg:#05030b;
      --fg:#f5f0ff;
      --muted:#b9afd4;
      --accent:#a96bff;
      --accent-soft:rgba(169,107,255,0.16);
      --card:#0d0718;
      --card-soft:rgba(255,255,255,0.04);
    }

    *{box-sizing:border-box}
    html,body{
      margin:0;
      padding:0;
      background:var(--bg);
      color:var(--fg);
      font-family:system-ui,-apple-system,"Inter",sans-serif;
    }
    a{text-decoration:none;color:inherit}

    .bg-layer{
      position:fixed;
      inset:0;
      z-index:-1;
      background:
        radial-gradient(1200px 600px at 15% 10%, rgba(169,107,255,.16), transparent 60%),
        radial-gradient(900px 500px at 85% 90%, rgba(90,60,170,.16), transparent 60%);
      pointer-events:none;
    }

    .page{
      max-width:960px;
      margin:0 auto;
      padding:24px 16px 72px;
    }

    @media (min-width:768px){
      .page{padding:32px 24px 80px;}
    }

    /* Topbar + гамбургер */

    header.topbar{
      position:relative;
      z-index:30;
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:16px;
      margin-bottom:32px;
    }

    .topbar__left{
      display:flex;
      flex-direction:column;
      gap:2px;
    }
    .logo{
      font-weight:700;
      letter-spacing:0.14em;
      font-size:14px;
      text-transform:uppercase;
    }
    .logo-sub{
      font-size:12px;
      color:var(--muted);
    }

    .topbar__right{
      position:relative;
      display:flex;
      align-items:center;
      gap:10px;
    }

    .topbar__lang button{
      border:none;
      background:transparent;
      color:#d0c8f0;
      font-size:11px;
      text-transform:uppercase;
      letter-spacing:.12em;
      padding:2px 4px;
      cursor:pointer;
    }

    .topbar__lang button.is-active{
      font-weight:600;
      border-bottom:1px solid rgba(255,255,255,.7);
    }

    .topbar__menu-toggle{
      display:none;
    }

    .topbar__burger{
      width:32px;
      height:32px;
      border-radius:999px;
      border:1px solid rgba(255,255,255,.24);
      background:rgba(6,4,18,.9);
      display:inline-flex;
      align-items:center;
      justify-content:center;
      flex-direction:column;
      gap:3px;
      cursor:pointer;
    }

    .topbar__burger span{
      width:14px;
      height:1.6px;
      border-radius:999px;
      background:#f5f0ff;
    }

    .topbar__menu{
      position:absolute;
      top:120%;
      right:0;
      min-width:220px;
      max-width:260px;
      background:rgba(6,4,18,.97);
      border-radius:16px;
      border:1px solid rgba(255,255,255,.14);
      box-shadow:0 18px 50px rgba(0,0,0,.8);
      padding:10px 10px 8px;
      opacity:0;
      transform:translateY(-6px);
      pointer-events:none;
      transition:opacity .18s ease, transform .18s ease;
    }

    .topbar__menu-list{
      list-style:none;
      margin:0;
      padding:0;
      display:flex;
      flex-direction:column;
      gap:2px;
      font-size:13px;
    }

    .topbar__menu-link{
      display:flex;
      align-items:center;
      justify-content:space-between;
      padding:7px 8px;
      border-radius:10px;
      color:#f5f0ff;
      text-decoration:none;
      gap:8px;
    }

    .topbar__menu-link span:last-child{
      font-size:11px;
      color:#b9afd4;
      white-space:nowrap;
    }

    .topbar__menu-link:hover{
      background:rgba(169,107,255,.22);
    }

    .topbar__menu-sep{
      border:none;
      border-top:1px solid rgba(255,255,255,.12);
      margin:6px 0;
    }

    .topbar__menu-toggle:checked + label.topbar__burger + .topbar__menu{
      opacity:1;
      transform:translateY(0);
      pointer-events:auto;
    }

    /* Основной контент */

    main{
      display:flex;
      flex-direction:column;
      gap:32px;
    }

    .hero{
      padding:24px 20px;
      border-radius:28px;
      background:linear-gradient(145deg,rgba(10,5,30,.96),rgba(8,3,25,.98));
      box-shadow:0 18px 45px rgba(0,0,0,.65);
    }

    .hero-badge{
      display:inline-flex;
      align-items:center;
      gap:8px;
      padding:6px 12px;
      border-radius:999px;
      background:rgba(255,255,255,.03);
      border:1px solid rgba(255,255,255,.12);
      font-size:12px;
      color:var(--muted);
      margin-bottom:16px;
    }
    .hero-badge span.dot{
      height:4px;
      width:4px;
      border-radius:999px;
      background:var(--accent);
    }

    .hero-title{
      font-size:26px;
      line-height:1.25;
      margin:0 0 12px;
    }

    .hero-sub{
      margin:0 0 14px;
      color:var(--muted);
      font-size:14px;
      max-width:640px;
    }

    .hero-actions{
      display:flex;
      flex-wrap:wrap;
      gap:10px;
      margin-top:16px;
    }

    .hero-meta{
      margin-top:14px;
      display:flex;
      flex-wrap:wrap;
      gap:10px;
      font-size:12px;
      color:var(--muted);
    }

    @media (min-width:768px){
      .hero-title{font-size:30px;}
    }

    .section{
      padding:20px 18px;
      border-radius:22px;
      background:rgba(9,4,22,.96);
      border:1px solid rgba(255,255,255,.06);
    }
    .section--alt{
      background:rgba(5,3,14,.96);
    }

    .section__title{
      font-size:20px;
      margin:0 0 8px;
    }

    .section__lead{
      margin:0 0 16px;
      font-size:14px;
      color:var(--muted);
    }

    .section__list{
      margin:0;
      padding-left:18px;
      font-size:14px;
      color:var(--muted);
    }

    .section__list li{
      margin-bottom:4px;
    }

    .cards{
      display:grid;
      grid-template-columns:1fr;
      gap:10px;
    }
    @media (min-width:720px){
      .cards{grid-template-columns:repeat(3,minmax(0,1fr));}
    }

    .card{
      padding:12px 12px;
      border-radius:16px;
      background:var(--card-soft);
      border:1px solid rgba(255,255,255,.08);
    }
    .card-title{
      font-weight:600;
      margin-bottom:4px;
      font-size:14px;
    }
    .card-text{
      margin:0;
      font-size:13px;
      color:var(--muted);
    }

    .airdrop-block{
      margin-top:12px;
      padding:12px 12px;
      border-radius:16px;
      background:rgba(16,10,40,.95);
      border:1px solid rgba(255,255,255,.08);
    }
    .airdrop-block__title{
      font-weight:600;
      margin:0 0 8px;
      font-size:14px;
    }
    .airdrop-block__list{
      margin:0 0 12px;
      padding-left:18px;
      font-size:13px;
      color:var(--muted);
    }

    .pill-row{
      display:flex;
      flex-wrap:wrap;
      gap:8px;
      margin-top:10px;
    }

    .pill-link{
      padding:6px 14px;
      border-radius:999px;
      border:1px solid rgba(255,255,255,.18);
      font-size:13px;
      color:var(--muted);
      cursor:pointer;
      background:rgba(7,4,20,.85);
      backdrop-filter:blur(12px);
      transition:background .15s,border-color .15s,color .15s,transform .1s;
    }

    .pill-link:hover{
      background:var(--accent-soft);
      border-color:var(--accent);
      color:var(--fg);
      transform:translateY(-1px);
    }

    .btn{
      border-radius:999px;
      padding:9px 18px;
      font-size:14px;
      border:1px solid rgba(255,255,255,.18);
      background:rgba(11,7,32,.95);
      color:#f5f0ff;
      cursor:pointer;
      display:inline-flex;
      align-items:center;
      gap:8px;
    }
    .btn--primary{
      background:linear-gradient(135deg,#ff7ae0,#a96bff);
      border:none;
      color:#1a102b;
      font-weight:600;
    }
    .btn--ghost{
      background:transparent;
      border-color:rgba(255,255,255,.32);
    }

    .footer{
      margin-top:26px;
      font-size:12px;
      color:var(--muted);
      display:flex;
      flex-wrap:wrap;
      gap:8px;
      justify-content:space-between;
      align-items:center;
      padding:6px 4px 0;
      border-top:1px solid rgba(255,255,255,.08);
    }

  </style>
</head>
<body>
  <div class="bg-layer"></div>

  <div class="page">
    <header class="topbar">
      <div class="topbar__left">
        <div class="logo">LOGOS</div>
        <div class="logo-sub">Resonance Blockchain</div>
      </div>
      <div class="topbar__right">
        <div class="topbar__lang">
          <button type="button" data-lang-btn="ru" class="is-active">RU</button>
          <button type="button" data-lang-btn="en">EN</button>
          <button type="button" data-lang-btn="de">DE</button>
        </div>

        <input type="checkbox" id="topbar-menu-toggle" class="topbar__menu-toggle" />
        <label for="topbar-menu-toggle" class="topbar__burger" aria-label="Menu">
          <span></span><span></span><span></span>
        </label>

        <div class="topbar__menu">
          <ul class="topbar__menu-list">
            <li>
              <a href="#intro" class="topbar__menu-link">
                <span data-i18n="nav_intro">Обзор</span>
              </a>
            </li>
            <li>
              <a href="#speed" class="topbar__menu-link">
                <span data-i18n="nav_speed">Скорость</span>
              </a>
            </li>
            <li>
              <a href="#privacy" class="topbar__menu-link">
                <span data-i18n="nav_privacy">Приватность</span>
              </a>
            </li>
            <li>
              <a href="#fees" class="topbar__menu-link">
                <span data-i18n="nav_fees">Комиссии</span>
              </a>
            </li>
            <li>
              <a href="#reliability" class="topbar__menu-link">
                <span data-i18n="nav_reliability">Надёжность</span>
              </a>
            </li>
            <li>
              <a href="#tech" class="topbar__menu-link">
                <span data-i18n="nav_tech">Технология</span>
              </a>
            </li>
            <li>
              <a href="#rsp" class="topbar__menu-link">
                <span data-i18n="nav_rsp">LOGOS RSP</span>
              </a>
            </li>
            <li>
              <a href="#agi" class="topbar__menu-link">
                <span data-i18n="nav_agi">LOGOS‑AGI</span>
              </a>
            </li>
            <li>
              <a href="#better" class="topbar__menu-link">
                <span data-i18n="nav_better">Преимущества</span>
              </a>
            </li>
            <li>
              <a href="#short" class="topbar__menu-link">
                <span data-i18n="nav_short">В двух словах</span>
              </a>
            </li>
            <li>
              <a href="#community" class="topbar__menu-link">
                <span data-i18n="nav_comm">Сообщество</span>
              </a>
            </li>

            <li><hr class="topbar__menu-sep" /></li>

            <li>
              <a href="mailto:simbiotai@proton.me?subject=LOGOS%20Presale%20Seed" class="topbar__menu-link">
                <span data-i18n="menu_presale">Presale / Seed</span>
                <span>simbiotai@proton.me</span>
              </a>
            </li>
            <li>
              <a href="https://mw-expedition.com/staking" class="topbar__menu-link">
                <span data-i18n="menu_staking">Стейкинг LGN</span>
                <span>mainnet</span>
              </a>
            </li>
            <li>
              <a href="/airdrop.html" class="topbar__menu-link">
                <span data-i18n="menu_airdrop">Airdrop</span>
                <span data-i18n="menu_airdrop_sub">задания и прогресс</span>
              </a>
            </li>

            <li><hr class="topbar__menu-sep" /></li>

            <li>
              <a href="https://mw-expedition.com/wallet" class="topbar__menu-link">
                <span>Web Wallet</span>
                <span>beta</span>
              </a>
            </li>
            <li>
              <a href="https://mw-expedition.com/explorer" class="topbar__menu-link">
                <span>Explorer</span>
                <span>chain view</span>
              </a>
            </li>

            <li><hr class="topbar__menu-sep" /></li>

            <li>
              <a href="https://t.me/logosblockchain" target="_blank" rel="noopener" class="topbar__menu-link">
                <span data-i18n="menu_telegram">Telegram</span>
                <span>@logosblockchain</span>
              </a>
            </li>
            <li>
              <a href="https://x.com/RspLogos" target="_blank" rel="noopener" class="topbar__menu-link">
                <span data-i18n="menu_twitter">X (Twitter)</span>
                <span>@OfficiaLogosLRB</span>
              </a>
            </li>
            <li>
              <a href="https://t.me/logosblockchain" target="_blank" rel="noopener" class="topbar__menu-link">
                <span>Airdrop bot</span>
                <span>@Logos_lrb_bot</span>
              </a>
            </li>
          </ul>
        </div>
      </div>
    </header>

    <main>
      <!-- HERO -->
      <section id="intro" class="hero">
        <div class="hero-badge">
          <span class="dot"></span>
          <span data-i18n="badge_main">L1 • 81M LGN • Анонимность • Дефляция • Квантовая устойчивость</span>
        </div>
        <h1 class="hero-title" data-i18n="intro_title">
          LOGOS — блокчейн нового поколения на резонансной архитектуре
        </h1>
        <p class="hero-sub" data-i18n="intro_p1">
          LOGOS — резонансный L1‑блокчейн следующего поколения. Мы делаем первый шаг к Web4: сети, где люди, ценность и ИИ работают в одном защищённом пространстве.
        </p>
        <p class="hero-sub" data-i18n="intro_p2">
          Сеть уже выдерживает реальную нагрузку, сохраняет приватность и остаётся простой в эксплуатации. Никаких лишних усложнений — только ядро, рассчитанное на миллионы пользователей.
        </p>
        <p class="hero-sub" data-i18n="intro_p3">
          LOGOS — это фундамент для новой цифровой среды: платежи, стейкинг, общение и резонансные протоколы поверх одной устойчивой L1.
        </p>
        <div class="hero-actions">
          <a href="#about" class="btn btn--primary" data-i18n="btn_learn_more">Подробнее</a>
          <a href="/apk/app-20250830_1442.apk" class="btn btn--ghost" data-i18n="btn_download_apk">Скачать безопасный APK</a>
        </div>
        <div class="hero-meta">
          <span data-i18n="meta_supply">Общая эмиссия: 81 000 000 LGN</span>
          <span data-i18n="meta_ready">Создан для реальной пользы и массового использования</span>
        </div>
      </section>

      <!-- About -->
      <section id="about" class="section">
        <h2 class="section__title" data-i18n="about_title">Что такое LOGOS</h2>
        <p class="section__lead" data-i18n="about_text">
          LOGOS — L1‑блокчейн на резонансной архитектуре. В основе — Σ(t), фазовые фильтры и анти‑спам механизмы, которые держат сеть стабильной даже под высокой нагрузкой.
        </p>
        <div class="cards">
          <article class="card">
            <h3 class="card-title" data-i18n="card1_title">Резонансное ядро</h3>
            <p class="card-text" data-i18n="card1_text">
              Σ(t), Λ и фазовые фильтры обеспечивают устойчивое поведение сети.
            </p>
          </article>
          <article class="card">
            <h3 class="card-title" data-i18n="card2_title">Реальная приватность</h3>
            <p class="card-text" data-i18n="card2_text">
              Минимум метаданных, строгая nonce‑политика и phase‑mixing на входе.
            </p>
          </article>
          <article class="card">
            <h3 class="card-title" data-i18n="card3_title">Production‑уровень</h3>
            <p class="card-text" data-i18n="card3_text">
              Rust‑ядро, Axum REST, Prometheus/Grafana, bridge‑журнал, health‑ручки.
            </p>
          </article>
        </div>
      </section>

      <!-- Speed -->
      <section id="speed" class="section">
        <h2 class="section__title" data-i18n="speed_title">Скорость и производительность</h2>
        <p class="section__lead" data-i18n="speed_p">
          Сеть тестировалась под реальной нагрузкой, а не на слайдах: пики ~2000+ транзакций в секунду с устойчивой финализацией и без форков. Архитектура заложена так, чтобы масштабироваться дальше — при росте числа узлов и оптимизации фаз возможно достижение 10 000+ tx/s без жертв по стабильности.
        </p>
      </section>

      <!-- Privacy -->
      <section id="privacy" class="section section--alt">
        <h2 class="section__title" data-i18n="privacy_title">Приватность нового уровня</h2>
        <p class="section__lead" data-i18n="privacy_p1">
          С первого дня LOGOS проектировался как сеть, где:
        </p>
        <ul class="section__list">
          <li data-i18n="privacy_li1">пользователя нельзя напрямую связать с транзакцией;</li>
          <li data-i18n="privacy_li2">маршруты пакетов трудно трассировать;</li>
          <li data-i18n="privacy_li3">утечки метаданных минимальны;</li>
          <li data-i18n="privacy_li4">нет очевидных сетевых отпечатков;</li>
          <li data-i18n="privacy_li5">нет стандартных точек трекинга.</li>
        </ul>
        <p class="section__lead" data-i18n="privacy_p2">
          Приватность в LOGOS — не опция и не галочка в интерфейсе. Она встроена в архитектуру.
        </p>
      </section>

      <!-- Fees -->
      <section id="fees" class="section">
        <h2 class="section__title" data-i18n="fees_title">Низкие комиссии и чистая финализация</h2>
        <p class="section__lead" data-i18n="fees_p">
          Блоки не конкурируют, не конфликтуют и не откатываются. Транзакция проходит один раз и записывается навсегда. Комиссии остаются одними из самых низких среди L1, потому что мы избегаем тяжёлых вычислений и раздутых контрактов — даже под нагрузкой базовые переводы остаются доступными.
        </p>
      </section>

      <!-- Reliability -->
      <section id="reliability" class="section section--alt">
        <h2 class="section__title" data-i18n="reliability_title">Надёжность и готовность к продакшену</h2>
        <p class="section__lead" data-i18n="reliability_p">
          Узлы LOGOS легко разворачиваются и обновляются, мосты работают с устойчивым журналом, есть стейкинг‑обвязки, архивирование и метрики. Узлы могут жить на обычных серверах, а инфраструктура уже выдержала стресс‑тесты под высокой нагрузкой.
        </p>
      </section>

      <!-- Technology -->
      <section id="tech" class="section">
        <h2 class="section__title" data-i18n="technology_title">Технология LOGOS</h2>
        <p class="section__lead" data-i18n="technology_p">
          В основе LOGOS — резонансно‑символическая архитектура: собственный способ организации данных и синхронизации. Вместо тяжёлого консенсуса и сложных схем — ритмы, структура и фазовая динамика. Это делает сеть устойчивой к нагрузке, быстрой в реакции на всплески и сложной для атак на сетевом уровне, при этом масштабирование остаётся прямолинейным.
        </p>
      </section>

      <!-- RSP -->
      <section id="rsp" class="section section--alt">
        <h2 class="section__title" data-i18n="rsp_title">LOGOS RSP — коммуникация без следов</h2>
        <p class="section__lead" data-i18n="rsp_p">
          В ядре экосистемы — протокол конфиденциальной коммуникации LOGOS RSP. На практике это общение без классического IP‑маршрутизации и с минимальными цифровыми следами, устойчивое к перехвату и анализу. RSP может работать не только поверх интернета, но и через альтернативные носители — свет, звук, радио и оффлайн‑каналы.
        </p>
      </section>

      <!-- AGI -->
      <section id="agi" class="section">
        <h2 class="section__title" data-i18n="agi_title">LOGOS‑AGI — новый архитектурный слой</h2>
        <p class="section__lead" data-i18n="agi_p">
          Параллельно мы развиваем направление LOGOS‑AGI — другой тип искусственного интеллекта. Он опирается не на гигантские нейросети, а на резонансную логику и символические структуры, заложенные в систему. Ранние прототипы показывают, что такой ИИ может работать без GPU, учиться без огромных датасетов и находить свои паттерны, работая с смыслом, а не только со статистикой.
        </p>
      </section>

      <!-- Why LOGOS -->
      <section id="better" class="section section--alt">
        <h2 class="section__title" data-i18n="better_title">Почему LOGOS отличается</h2>
        <p class="section__lead" data-i18n="better_intro">
          LOGOS строится под реальный мир, а не под презентации. Если коротко, наши преимущества:
        </p>
        <ul class="section__list">
          <li data-i18n="better_item1">Реальная скорость, подтверждённая нагрузочными тестами.</li>
          <li data-i18n="better_item2">Настоящая приватность вместо суррогатной анонимности.</li>
          <li data-i18n="better_item3">Минимальные комиссии за транзакции.</li>
          <li data-i18n="better_item4">Мгновенная финализация без форков и откатов.</li>
          <li data-i18n="better_item5">Устойчивость к сетевым атакам и пиковым нагрузкам.</li>
          <li data-i18n="better_item6">Простое горизонтальное масштабирование сети.</li>
          <li data-i18n="better_item7">Инфраструктура, рассчитанная на миллионы пользователей.</li>
          <li data-i18n="better_item8">Уникальная резонансная архитектура, которой нет ни в одной другой сети.</li>
        </ul>
      </section>

      <!-- Short -->
      <section id="short" class="section">
        <h2 class="section__title" data-i18n="short_title">В двух словах</h2>
        <p class="section__lead" data-i18n="short_p">
          LOGOS — это L1‑блокчейн нового поколения на резонансной архитектуре: высокая скорость, низкие комиссии, адаптивное поведение и сильная приватность. Внутри мы развиваем собственный коммуникационный протокол и направление LOGOS‑AGI. Мы строим не очередную криптоплатформу, а базовый слой для Web4.
        </p>
      </section>

      <!-- Community / Airdrop -->
      <section id="community" class="section section--alt">
        <h2 class="section__title" data-i18n="comm_title">Сообщество и каналы</h2>
        <p class="section__lead" data-i18n="comm_text">
          Присоединяйся к полю: обновления, airdrop‑кампании, миссии, стейкинг и эксперименты с AI‑нативными протоколами.
        </p>

        <div class="airdrop-block">
          <h3 class="airdrop-block__title" data-i18n="airdrop_block_title">🎁 Airdrop LOGOS: что нужно сделать</h3>
          <ol class="airdrop-block__list">
            <li data-i18n="airdrop_step1">Подключить LOGOS‑кошелёк и привязать его к airdrop‑профилю.</li>
            <li data-i18n="airdrop_step2">Подписаться на Telegram‑канал @logosblockchain.</li>
            <li data-i18n="airdrop_step3">Подписаться на X (Twitter) @OfficiaLogosLRB.</li>
            <li data-i18n="airdrop_step4">Поставить лайк и сделать ретвит закреплённого твита кампании.</li>
            <li data-i18n="airdrop_step5">Получить личную реферальную ссылку и пригласить до 5 друзей.</li>
          </ol>
          <a href="/airdrop.html" class="btn btn--primary" data-i18n="airdrop_btn">
            Перейти к airdrop‑заданиям
          </a>
        </div>

        <div class="pill-row">
          <a class="pill-link" href="https://t.me/logosblockchain" target="_blank" rel="noreferrer">
            Telegram
          </a>
          <a class="pill-link" href="https://x.com/RspLogos" target="_blank" rel="noreferrer">
            X (Twitter)
          </a>
          <a class="pill-link" href="#staking">
            <span data-i18n="comm_staking">Стейкинг LGN</span>
          </a>
        </div>

        <p class="section__lead" style="margin-top:12px;">
          <span data-i18n="comm_email">Email: simbiotai@proton.me</span>
        </p>
      </section>
    </main>

    <footer class="footer">
      <span data-i18n="footer_note">LOGOS LRB • Resonance Blockchain • Готов к миллионам пользователей</span>
    </footer>
  </div>

  <script>
    (function(){
      const dicts = {
        ru: {
          badge_main: "L1 • 81M LGN • Анонимность • Дефляция • Квантовая устойчивость",
          nav_intro: "Обзор",
          nav_speed: "Скорость",
          nav_privacy: "Приватность",
          nav_fees: "Комиссии",
          nav_reliability: "Надёжность",
          nav_tech: "Технология",
          nav_rsp: "LOGOS RSP",
          nav_agi: "LOGOS‑AGI",
          nav_better: "Преимущества",
          nav_short: "В двух словах",
          nav_comm: "Сообщество",

          menu_presale: "Presale / Seed",
          menu_staking: "Стейкинг LGN",
          menu_airdrop: "Airdrop",
          menu_airdrop_sub: "задания и прогресс",
          menu_telegram: "Telegram",
          menu_twitter: "X (Twitter)",

          intro_title: "Живой резонансный блокчейн нового уровня",
          intro_p1: "LOGOS — резонансный L1‑блокчейн следующего поколения. Мы делаем первый шаг к Web4: сети, где люди, ценность и ИИ работают в одном защищённом пространстве.",
          intro_p2: "Мы построили L1, который работает быстро и стабильно без лишней сложности. Блоки появляются почти мгновенно, сеть выдерживает нагрузку, комиссии минимальны, а уровень приватности выше, чем у большинства мейнстрим‑сетей.",
          intro_p3: "LOGOS — фундамент для новой цифровой среды, готовой к миллионам пользователей.",

          btn_learn_more: "Подробнее",
          btn_download_apk: "Скачать безопасный APK",
          meta_supply: "Общая эмиссия: 81 000 000 LGN",
          meta_ready: "Создан для реальной пользы и массового использования",

          about_title: "Что такое LOGOS",
          about_text: "LOGOS — L1‑блокчейн на резонансной архитектуре. Ядро сети опирается на Σ(t), фазовые фильтры и строгую политику обработки транзакций.",
          card1_title: "Резонансное ядро",
          card1_text: "Σ(t), Λ и фазовые фильтры держат сеть устойчивой и управляют нагрузкой.",
          card2_title: "Реальная приватность",
          card2_text: "Минимум метаданных, phase‑mixing и строгая nonce‑политика на уровне протокола.",
          card3_title: "Production‑уровень",
          card3_text: "Rust‑ядро, Axum REST, Prometheus/Grafana, архив, мост, health‑ручки и alerты.",

          speed_title: "Скорость и производительность",
          speed_p: "Мы тестируем сеть под реальной нагрузкой, а не только в теории. Пиковые результаты достигают 2000+ транзакций в секунду с устойчивой финализацией и без форков. Архитектура рассчитана на выход за 10 000+ tx/s по мере роста числа узлов и оптимизации фаз.",

          privacy_title: "Приватность нового уровня",
          privacy_p1: "LOGOS изначально спроектирован как сеть, где:",
          privacy_li1: "пользователя нельзя напрямую связать с конкретной транзакцией;",
          privacy_li2: "маршруты пакетов сложно отследить привычными методами;",
          privacy_li3: "утечки метаданных минимальны;",
          privacy_li4: "нет ярко выраженных сетевых отпечатков;",
          privacy_li5: "нет стандартных точек трекинга.",
          privacy_p2: "Приватность в LOGOS — не фича, а свойство архитектуры.",

          fees_title: "Низкие комиссии и чистая финализация",
          fees_p: "Блоки не конкурируют друг с другом и не откатываются. Каждая транзакция проходит один раз и навсегда попадает в цепочку. За счёт этого комиссии остаются низкими даже под нагрузкой, а поведение сети предсказуемо.",

          reliability_title: "Надёжность и готовность к продакшену",
          reliability_p: "Инструменты оркестрации поднимают узлы за секунды, мосты работают через устойчивый журнал, есть обвязка стейкинга, архивирование и мониторинг. Узлы LOGOS могут работать на обычных серверах, а инфраструктура проверена стресс‑тестами.",

          technology_title: "Технология LOGOS",
          technology_p: "LOGOS построен на резонансно‑символической архитектуре. Вместо тяжелых консенсусов и громоздких контрактов мы используем ритмы, структуру и фазовую динамику, что повышает устойчивость под нагрузкой и упрощает масштабирование сети.",

          rsp_title: "LOGOS RSP — коммуникация без следов",
          rsp_p: "В ядре экосистемы LOGOS — протокол конфиденциальной коммуникации RSP. Он минимизирует цифровые следы, не опирается на классическую IP‑маршрутизацию и устойчив к анализу трафика. RSP может работать не только через интернет, но и через свет, звук, радио и оффлайн‑каналы.",

          agi_title: "LOGOS‑AGI — новый архитектурный слой",
          agi_p: "LOGOS‑AGI — это направление по созданию резонансного искусственного интеллекта, который опирается на структуры и ритмы сети LOGOS. Такие системы могут работать без дорогих GPU и гигантских датасетов, а значит подходят для децентрализованных сценариев.",

          better_title: "Почему LOGOS отличается",
          better_intro: "LOGOS строится под реальный мир, а не под презентации. Коротко наши преимущества:",
          better_item1: "Реальная скорость, подтверждённая нагрузочными тестами.",
          better_item2: "Глубокая приватность вместо псевдо‑анонимности.",
          better_item3: "Минимальные комиссии даже под нагрузкой.",
          better_item4: "Мгновенная финализация без форков и откатов.",
          better_item5: "Устойчивость к сетевым атакам и пиковым нагрузкам.",
          better_item6: "Прямолинейное масштабирование сети.",
          better_item7: "Инфраструктура для миллионов пользователей.",
          better_item8: "Уникальная резонансная архитектура, которой нет у других L1.",

          short_title: "В двух словах",
          short_p: "LOGOS — L1 нового поколения на резонансной архитектуре: высокая скорость, низкие комиссии, адаптивное поведение и сильная приватность. Мы строим базовый слой для Web4 и автономных систем.",

          comm_title: "Сообщество и каналы",
          comm_text: "Присоединяйся к сообществу: обновления сети, airdrop‑кампании, миссии, стейкинг и эксперименты с AI‑нативными протоколами.",
          comm_staking: "Стейкинг LGN",
          comm_email: "Email: simbiotai@proton.me",

          airdrop_block_title: "🎁 Airdrop LOGOS: что нужно сделать",
          airdrop_step1: "Подключить LOGOS‑кошелёк и привязать его к airdrop‑профилю.",
          airdrop_step2: "Подписаться на Telegram‑канал @logosblockchain.",
          airdrop_step3: "Подписаться на X (Twitter) @OfficiaLogosLRB.",
          airdrop_step4: "Поставить лайк и сделать ретвит закреплённого твита кампании.",
          airdrop_step5: "Получить реферальную ссылку и пригласить друзей.",
          airdrop_btn: "Перейти к airdrop‑заданиям",

          footer_note: "LOGOS LRB • Resonance Blockchain • Готов к миллионам пользователей"
        },

        en: {
          badge_main: "L1 • 81M LGN • Anonymity • Deflation • Quantum resistance",
          nav_intro: "Overview",
          nav_speed: "Speed",
          nav_privacy: "Privacy",
          nav_fees: "Fees",
          nav_reliability: "Reliability",
          nav_tech: "Technology",
          nav_rsp: "LOGOS RSP",
          nav_agi: "LOGOS‑AGI",
          nav_better: "Why LOGOS",
          nav_short: "In short",
          nav_comm: "Community",

          menu_presale: "Presale / Seed",
          menu_staking: "LGN staking",
          menu_airdrop: "Airdrop",
          menu_airdrop_sub: "tasks and progress",
          menu_telegram: "Telegram",
          menu_twitter: "X (Twitter)",

          intro_title: "LOGOS – a next‑generation blockchain built on resonance architecture",
          intro_p1: "LOGOS is not just another network. It is a new‑generation L1 built around speed, privacy and a deep resonance architecture.",
          intro_p2: "We created an L1 that works fast and stays stable without unnecessary complexity. Blocks are formed almost instantly, the network handles high traffic, fees remain minimal and the level of privacy is higher than in most mainstream chains.",
          intro_p3: "LOGOS is the foundation for a new digital environment ready for millions of users.",

          btn_learn_more: "Learn more",
          btn_download_apk: "Download secure APK",
          meta_supply: "Total supply: 81 000 000 LGN",
          meta_ready: "Built for real utility and mass adoption",

          about_title: "What is LOGOS",
          about_text: "LOGOS is a resonance‑based L1 blockchain. Its core relies on Σ(t), phase filters and strict transaction processing rules.",
          card1_title: "Resonant core",
          card1_text: "Σ(t), Λ and phase filters keep the network stable and control load.",
          card2_title: "Real privacy",
          card2_text: "Minimal metadata, phase mixing and strict nonce policy at protocol level.",
          card3_title: "Production‑grade",
          card3_text: "Rust core, Axum REST, Prometheus/Grafana, archive, bridge journal and health checks.",

          speed_title: "Speed and performance",
          speed_p: "We tested the network under real conditions, not just on paper. Peak results reached more than 2 000 transactions per second with stable finality and no forks. The architecture is designed to go further: with more nodes and phase optimisation, 10 000+ tx/s is achievable without sacrificing stability.",

          privacy_title: "Privacy on a new level",
          privacy_p1: "From day one LOGOS was designed as a network where:",
          privacy_li1: "a user cannot be directly tied to a specific transaction;",
          privacy_li2: "packet routes are difficult to trace with standard tools;",
          privacy_li3: "metadata leakage is minimised;",
          privacy_li4: "there are no obvious network fingerprints;",
          privacy_li5: "there are no standard tracking points.",
          privacy_p2: "Privacy in LOGOS is not a switch or a feature. It is baked into the architecture.",

          fees_title: "Low fees and clean finality",
          fees_p: "Blocks do not compete or roll back. Each transaction passes once and is recorded permanently. Fees stay among the lowest across L1 chains because we avoid heavy computation and bloated contracts, so even under serious load basic transfers remain affordable.",

          reliability_title: "Reliability and production readiness",
          reliability_p: "The network is ready for production use: orchestration tools spin up nodes in seconds, bridges work securely, and there is staking infrastructure, archiving and metrics. LOGOS nodes run on ordinary servers and the stack is stress‑tested under high load.",

          technology_title: "Technology behind LOGOS",
          technology_p: "LOGOS is built on a resonance‑symbolic architecture – our own way of organising data and synchronisation. Instead of relying on heavy consensus and over‑complex contracts, we use rhythm, structure and phase dynamics, which makes the network stable under pressure and scaling straightforward.",

          rsp_title: "LOGOS RSP – communication without traces",
          rsp_p: "At the core of the ecosystem lies the confidential communication protocol LOGOS RSP. In practice it means communication with minimal digital traces, resistant to interception and traffic analysis. RSP can operate not only over the internet but also via alternative carriers such as light, sound, radio and offline channels.",

          agi_title: "LOGOS‑AGI – a new architectural layer",
          agi_p: "We are also building LOGOS‑AGI – a different type of artificial intelligence. It relies not on huge neural networks but on resonance logic and symbolic structures embedded in the system. Such AI can work without GPUs and giant datasets, which is ideal for decentralised environments.",

          better_title: "Why LOGOS is different",
          better_intro: "LOGOS is built for the real world, not only for slide decks. In short, our advantages are:",
          better_item1: "Real speed, proven by load tests.",
          better_item2: "Deep privacy instead of pseudo‑anonymity.",
          better_item3: "Minimal transaction fees.",
          better_item4: "Instant finality without forks or rollbacks.",
          better_item5: "Resilience to network attacks and load spikes.",
          better_item6: "Straightforward scaling of the network.",
          better_item7: "Infrastructure ready for millions of users.",
          better_item8: "A unique resonance architecture you will not find in any other chain.",

          short_title: "In short",
          short_p: "LOGOS is a next‑generation L1 blockchain built on resonance architecture: high speed, low fees, adaptive behaviour and strong privacy. We are building a base layer for Web4 and future autonomous systems.",

          comm_title: "Community and channels",
          comm_text: "Join the field: updates, airdrop campaigns, missions, staking and AI‑native experiments.",
          comm_staking: "LGN staking",
          comm_email: "Email: simbiotai@proton.me",

          airdrop_block_title: "🎁 LOGOS airdrop: what to do",
          airdrop_step1: "Connect your LOGOS wallet and bind it to your airdrop profile.",
          airdrop_step2: "Subscribe to the Telegram channel @logosblockchain.",
          airdrop_step3: "Follow X (Twitter) @OfficiaLogosLRB.",
          airdrop_step4: "Like and retweet the pinned campaign tweet.",
          airdrop_step5: "Get your personal referral link and invite friends.",
          airdrop_btn: "Go to airdrop tasks",

          footer_note: "LOGOS LRB • Resonance Blockchain • Ready for millions of users"
        },

        de: {
          badge_main: "L1 • 81M LGN • Anonymität • Deflation • Quantenresistenz",
          nav_intro: "Überblick",
          nav_speed: "Geschwindigkeit",
          nav_privacy: "Privatsphäre",
          nav_fees: "Gebühren",
          nav_reliability: "Stabilität",
          nav_tech: "Technologie",
          nav_rsp: "LOGOS RSP",
          nav_agi: "LOGOS‑AGI",
          nav_better: "Vorteile",
          nav_short: "Kurzfassung",
          nav_comm: "Community",

          menu_presale: "Presale / Seed",
          menu_staking: "LGN‑Staking",
          menu_airdrop: "Airdrop",
          menu_airdrop_sub: "Aufgaben und Fortschritt",
          menu_telegram: "Telegram",
          menu_twitter: "X (Twitter)",

          intro_title: "LOGOS – Blockchain der nächsten Generation auf Resonanz‑Architektur",
          intro_p1: "LOGOS ist nicht einfach eine weitere Chain, sondern eine Blockchain der nächsten Generation – gebaut für Geschwindigkeit, Privatsphäre und eine tiefe Resonanz‑Architektur.",
          intro_p2: "Wir haben eine L1 entwickelt, die schnell und stabil läuft ohne überflüssige Komplexität. Blöcke entstehen nahezu sofort, das Netzwerk trägt hohe Last, Gebühren bleiben minimal und das Datenschutzniveau ist höher als in den meisten Mainstream‑Netzen.",
          intro_p3: "LOGOS ist ein Fundament für eine neue digitale Umgebung, bereit für Millionen von Nutzern.",

          btn_learn_more: "Mehr erfahren",
          btn_download_apk: "Sichere APK herunterladen",
          meta_supply: "Gesamtangebot: 81 000 000 LGN",
          meta_ready: "Entwickelt für echten Nutzen und Massenadoption",

          about_title: "Was ist LOGOS",
          about_text: "LOGOS ist eine L1‑Blockchain auf Resonanz‑Architektur. Im Kern stehen Σ(t), Phasenfilter und strikte Regeln für die Verarbeitung von Transaktionen.",
          card1_title: "Resonanz‑Kern",
          card1_text: "Σ(t), Λ und Phasenfilter halten das Netzwerk stabil und steuern die Last.",
          card2_title: "Echte Privatsphäre",
          card2_text: "Minimale Metadaten, Phasenmischung und strikte Nonce‑Politik auf Protokollebene.",
          card3_title: "Produktionsreif",
          card3_text: "Rust‑Kern, Axum‑REST, Prometheus/Grafana, Archiv, Bridge‑Journal und Health‑Checks.",

          speed_title: "Geschwindigkeit und Performance",
          speed_p: "Wir testen das Netzwerk unter realen Bedingungen. Spitzenwerte liegen bei über 2 000 Transaktionen pro Sekunde mit stabiler Finalität und ohne Forks. Die Architektur ist darauf ausgelegt, mit mehr Validatoren und Phasenoptimierung weiter auf 10 000+ tx/s zu skalieren.",

          privacy_title: "Privatsphäre auf neuem Niveau",
          privacy_p1: "LOGOS wurde von Anfang an so entworfen, dass:",
          privacy_li1: "ein Nutzer nicht direkt einer bestimmten Transaktion zugeordnet werden kann;",
          privacy_li2: "Paketwege nur schwer nachvollziehbar sind;",
          privacy_li3: "Metadaten‑Lecks minimiert werden;",
          privacy_li4: "keine eindeutigen Netzwerk‑Fingerabdrücke vorhanden sind;",
          privacy_li5: "keine Standard‑Tracking‑Punkte existieren.",
          privacy_p2: "Privatsphäre ist bei LOGOS kein Schalter, sondern ein Architekturmerkmal.",

          fees_title: "Niedrige Gebühren und saubere Finalität",
          fees_p: "Blöcke konkurrieren nicht miteinander und werden nicht zurückgerollt. Jede Transaktion wird einmal verarbeitet und dauerhaft gespeichert. Dadurch bleiben die Gebühren niedrig, auch bei hoher Auslastung, und das Verhalten des Netzwerks ist gut vorhersagbar.",

          reliability_title: "Zuverlässigkeit und Produktionsreife",
          reliability_p: "Orchestrierungs‑Tools starten Nodes in Sekunden, Bridges arbeiten mit robustem Journal, es gibt Staking‑Infrastructure, Archivierung und Monitoring. LOGOS‑Nodes können auf gewöhnlichen Servern laufen, und der Stack wurde mit Lasttests geprüft.",

          technology_title: "Die Technologie hinter LOGOS",
          technology_p: "LOGOS basiert auf einer Resonanz‑symbolischen Architektur. Anstatt auf schwere Konsens‑Mechanismen und überladene Verträge zu setzen, nutzen wir Rhythmus, Struktur und Phasendynamik. So bleibt das Netzwerk unter Last stabil und lässt sich einfach skalieren.",

          rsp_title: "LOGOS RSP – Kommunikation ohne Spuren",
          rsp_p: "Im Zentrum der LOGOS‑Ökonomie steht das vertrauliche Kommunikationsprotokoll RSP. Es reduziert digitale Spuren, vermeidet klassische IP‑Routen und ist resistent gegen Traffic‑Analyse. RSP kann nicht nur über das Internet, sondern auch über Licht, Schall, Funk und Offline‑Kanäle betrieben werden.",

          agi_title: "LOGOS‑AGI – eine neue Schicht",
          agi_p: "LOGOS‑AGI ist eine Richtung für resonanzbasierte KI, die auf den Strukturen und Rhythmen des LOGOS‑Netzwerks aufbaut. Solche Systeme können ohne teure GPUs und riesige Datensätze arbeiten und sind daher geeignet für dezentrale Szenarien.",

          better_title: "Warum LOGOS anders ist",
          better_intro: "LOGOS wird für die reale Nutzung gebaut, nicht nur für Präsentationen. Kurz zusammengefasst:",
          better_item1: "Echte Geschwindigkeit, durch Lasttests belegt.",
          better_item2: "Tiefe Privatsphäre statt Pseudo‑Anonymität.",
          better_item3: "Sehr niedrige Transaktionsgebühren.",
          better_item4: "Sofortige Finalität ohne Forks und Rollbacks.",
          better_item5: "Resilienz gegenüber Netzwerkangriffen und Lastspitzen.",
          better_item6: "Einfache horizontale Skalierung des Netzwerks.",
          better_item7: "Infrastruktur für Millionen von Nutzern.",
          better_item8: "Eine einzigartige Resonanz‑Architektur, die es sonst nirgendwo gibt.",

          short_title: "Kurzfassung",
          short_p: "LOGOS ist eine L1‑Blockchain der nächsten Generation auf Resonanz‑Architektur: hohe Geschwindigkeit, niedrige Gebühren, adaptives Verhalten und starke Privatsphäre. Wir bauen die Basis für Web4 und autonome Systeme.",

          comm_title: "Community und Kanäle",
          comm_text: "Schließe dich dem Feld an: Updates, Airdrop‑Kampagnen, Missionen, Staking und AI‑native Experimente.",
          comm_staking: "LGN‑Staking",
          comm_email: "Email: simbiotai@proton.me",

          airdrop_block_title: "🎁 LOGOS‑Airdrop: was ist zu tun",
          airdrop_step1: "LOGOS‑Wallet verbinden und mit dem Airdrop‑Profil verknüpfen.",
          airdrop_step2: "Telegram‑Kanal @logosblockchain abonnieren.",
          airdrop_step3: "X (Twitter) @OfficiaLogosLRB folgen.",
          airdrop_step4: "Den angehefteten Kampagnen‑Tweet liken und retweeten.",
          airdrop_step5: "Einen persönlichen Referral‑Link holen und Freunde einladen.",
          airdrop_btn: "Zu den Airdrop‑Aufgaben wechseln",

          footer_note: "LOGOS LRB • Resonance Blockchain • Bereit für Millionen von Nutzern"
        }
      };

      function applyLang(lang){
        if (!dicts[lang]) return;
        const dict = dicts[lang];
        const html = document.documentElement;
        html.lang = lang;

        // переключаем активность кнопок
        document.querySelectorAll("[data-lang-btn]").forEach(btn => {
          btn.classList.toggle("is-active", btn.dataset.langBtn === lang);
        });

        document.querySelectorAll("[data-i18n]").forEach(el => {
          const key = el.dataset.i18n;
          if (!key) return;
          const val = dict[key];
          if (typeof val === "string") {
            el.textContent = val;
          }
        });

        try{
          localStorage.setItem("logos_lang", lang);
        }catch(e){}
      }

      document.addEventListener("DOMContentLoaded", function(){
        let lang = "ru";
        try{
          const saved = localStorage.getItem("logos_lang");
          if (saved && dicts[saved]) lang = saved;
        }catch(e){}
        applyLang(lang);

        document.querySelectorAll("[data-lang-btn]").forEach(btn => {
          btn.addEventListener("click", function(){
            applyLang(btn.dataset.langBtn || "ru");
          });
        });

        const toggle = document.getElementById("topbar-menu-toggle");
        const menu = document.querySelector(".topbar__menu");

        document.addEventListener("click", function(ev){
          if (!toggle || !menu) return;
          const target = ev.target;
          if (target === toggle) return;
          if (target.closest(".topbar__burger") || target.closest(".topbar__menu")) return;
          toggle.checked = false;
        });

        // закрывать меню по клику по любому пункту
        document.querySelectorAll(".topbar__menu-link").forEach(link => {
          link.addEventListener("click", function(){
            if (toggle) toggle.checked = false;
          });
        });
      });
    })();
  </script>
</body>
</html>

```

### FILE: /var/www/logos/landing/landing/logos_tg_bot/logos_guard_bot/bot/config.py
```
from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass(slots=True)
class Settings:
    bot_token: str
    verification_timeout: int = 60


def _load_settings() -> Settings:
    """
    Читаем настройки из окружения / .env.

    Приоритет токена:
    - LOGOS_TG_BOT_TOKEN
    - BOT_TOKEN
    - TELEGRAM_BOT_TOKEN
    """
    token = (
        os.getenv("LOGOS_TG_BOT_TOKEN")
        or os.getenv("BOT_TOKEN")
        or os.getenv("TELEGRAM_BOT_TOKEN")
    )
    if not token:
        raise RuntimeError(
            "LOGOS_TG_BOT_TOKEN / BOT_TOKEN / TELEGRAM_BOT_TOKEN не задан в окружении"
        )

    timeout_raw = os.getenv("VERIFICATION_TIMEOUT", "60")
    try:
        timeout = int(timeout_raw)
    except ValueError:
        timeout = 60

    # Страхуемся от слишком маленьких значений
    if timeout < 10:
        timeout = 10

    return Settings(
        bot_token=token,
        verification_timeout=timeout,
    )


settings = _load_settings()

```

### FILE: /var/www/logos/landing/landing/logos_tg_bot/logos_guard_bot/bot/handlers/common.py
```
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from bot.config import settings


router = Router(name="common")


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    text = (
        "👋 Привет!\n\n"
        "Я страж чата LOGOS: проверяю, что в группу заходят живые люди, а не боты.\n\n"
        "Чтобы я работал нормально:\n"
        "1) Добавь меня в группу/супергруппу.\n"
        "2) Дай права: ограничивать / банить участников и удалять сообщения.\n"
        "3) В BotFather отключи privacy mode для групп.\n\n"
        f"Новый участник получает кнопку проверки и {settings.verification_timeout} сек. "
        "Если не нажмёт — я кикну его и сразу разбаню, чтобы он мог зайти ещё раз."
    )
    await message.answer(text)


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    text = (
        "ℹ️ Команды:\n"
        "/start — информация о боте\n"
        "/help — эта справка\n"
        "/ping — проверить, жив ли бот\n"
    )
    await message.answer(text)


@router.message(Command("ping"))
async def cmd_ping(message: Message) -> None:
    await message.answer("pong 🏓")

```

### FILE: /var/www/logos/landing/landing/logos_tg_bot/logos_guard_bot/bot/handlers/__init__.py
```
from aiogram import Router

from .common import router as common_router
from .verification import router as verification_router


router = Router(name="root")
router.include_router(common_router)
router.include_router(verification_router)

```

### FILE: /var/www/logos/landing/landing/logos_tg_bot/logos_guard_bot/bot/handlers/verification.py
```
import logging

from aiogram import Bot, Router, F
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
from aiogram.types import (
    CallbackQuery,
    ChatMemberUpdated,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.config import settings
from bot.services.verification_service import (
    get_verification_service,
    MUTED_PERMISSIONS,
)


logger = logging.getLogger(__name__)

router = Router(name="verification")


def _kb_verify(user_id: int) -> InlineKeyboardMarkup:
    """Кнопка 'я живой' с привязкой к конкретному пользователю."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Я живой", callback_data=f"verify:{user_id}")]
        ]
    )


@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def on_user_join(event: ChatMemberUpdated, bot: Bot) -> None:
    """
    Новый участник в чате — блокируем и просим нажать кнопку.
    """
    chat = event.chat
    user = event.new_chat_member.user

    # Ботов не трогаем
    if user.is_bot:
        return

    # Режем все права на отправку сообщений
    try:
        await bot.restrict_chat_member(
            chat_id=chat.id,
            user_id=user.id,
            permissions=MUTED_PERMISSIONS,
        )
    except Exception as e:  # noqa: BLE001
        logger.warning(
            "Не удалось ограничить пользователя %s в чате %s: %s",
            user.id,
            chat.id,
            e,
        )

    service = get_verification_service()

    text = (
        f"👋 <b>Добро пожаловать, {user.full_name}</b>\n\n"
        "Чтобы подтвердить, что ты живой человек и не бот, нажми кнопку ниже "
        f"в течение <b>{settings.verification_timeout} секунд</b>.\n\n"
        "Пока ты не подтвердился, отправка сообщений в чат недоступна."
    )

    msg = await bot.send_message(
        chat.id,
        text,
        reply_markup=_kb_verify(user.id),
    )

    # Запускаем таймер проверки
    await service.start(
        bot=bot,
        chat_id=chat.id,
        user_id=user.id,
        welcome_message_id=msg.message_id,
    )


@router.callback_query(F.data.startswith("verify:"))
async def on_verify_click(callback: CallbackQuery, bot: Bot) -> None:
    """
    Обработка нажатия кнопки 'я живой'.
    """
    if callback.message is None or callback.data is None:
        await callback.answer()
        return

    chat_id = callback.message.chat.id
    from_id = callback.from_user.id

    # payload вида "verify:<user_id>"
    try:
        _, raw_user_id = callback.data.split(":", 1)
        expected_user_id = int(raw_user_id)
    except Exception:
        await callback.answer()
        return

    # Кто-то тыкает чужую кнопку
    if from_id != expected_user_id:
        await callback.answer("Эта кнопка не для тебя 🙂", show_alert=True)
        return

    service = get_verification_service()
    await service.confirm(bot=bot, chat_id=chat_id, user_id=from_id)

    # Удаляем служебное сообщение
    try:
        await callback.message.delete()
    except Exception:
        pass

    await callback.answer("Подтверждено ✅ Добро пожаловать в LOGOS!")

```

### FILE: /var/www/logos/landing/landing/logos_tg_bot/logos_guard_bot/bot/__init__.py
```
# Пакет бота

```

### FILE: /var/www/logos/landing/landing/logos_tg_bot/logos_guard_bot/bot/logging_config.py
```
import logging
import sys


def setup_logging(level: int = logging.INFO) -> None:
    """
    Базовая настройка логирования для бота.

    Пишем всё в stdout, формат: время • уровень • логгер • сообщение.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout,
    )

```

### FILE: /var/www/logos/landing/landing/logos_tg_bot/logos_guard_bot/bot/main.py
```
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import settings
from bot.handlers import router as root_router
from bot.logging_config import setup_logging
from bot.services.verification_service import init_verification_service


logger = logging.getLogger(__name__)


async def main() -> None:
    setup_logging()
    logger.info("Запуск LOGOS Guard Bot...")

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )

    # Сервис проверки должен быть инициализирован до старта поллинга
    init_verification_service(timeout_seconds=settings.verification_timeout)

    dp = Dispatcher()
    dp.include_router(root_router)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())

```

### FILE: /var/www/logos/landing/landing/logos_tg_bot/logos_guard_bot/bot/services/verification_service.py
```
import asyncio
import logging
from dataclasses import dataclass
from typing import Dict, Tuple, Optional

from aiogram import Bot
from aiogram.types import ChatPermissions


logger = logging.getLogger(__name__)


# Полные права после успешной проверки
FULL_PERMISSIONS = ChatPermissions(
    can_send_messages=True,
    can_send_audios=True,
    can_send_documents=True,
    can_send_photos=True,
    can_send_videos=True,
    can_send_video_notes=True,
    can_send_voice_notes=True,
    can_send_polls=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
    can_manage_topics=False,
)

# Полный мут до проверки
MUTED_PERMISSIONS = ChatPermissions(
    can_send_messages=False,
    can_send_audios=False,
    can_send_documents=False,
    can_send_photos=False,
    can_send_videos=False,
    can_send_video_notes=False,
    can_send_voice_notes=False,
    can_send_polls=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
    can_change_info=False,
    can_invite_users=False,
    can_pin_messages=False,
    can_manage_topics=False,
)


@dataclass
class PendingVerification:
    chat_id: int
    user_id: int
    welcome_message_id: int
    task: asyncio.Task


class VerificationService:
    """
    Сервис, который отслеживает висящие проверки пользователей.
    Хранение in-memory: для одной ноды этого достаточно.
    """

    def __init__(self, timeout_seconds: int) -> None:
        self.timeout_seconds = timeout_seconds
        self._pending: Dict[Tuple[int, int], PendingVerification] = {}
        self._lock = asyncio.Lock()

    async def start(
        self,
        *,
        bot: Bot,
        chat_id: int,
        user_id: int,
        welcome_message_id: int,
    ) -> None:
        """
        Запускаем таймер проверки.
        Пользователь уже должен быть замьючен и получить сообщение с кнопкой.
        """
        key = (chat_id, user_id)

        async with self._lock:
            existing = self._pending.get(key)
            if existing:
                existing.task.cancel()

            task = asyncio.create_task(
                self._kick_after_timeout(
                    bot=bot,
                    chat_id=chat_id,
                    user_id=user_id,
                    welcome_message_id=welcome_message_id,
                )
            )
            self._pending[key] = PendingVerification(
                chat_id=chat_id,
                user_id=user_id,
                welcome_message_id=welcome_message_id,
                task=task,
            )

    async def confirm(self, *, bot: Bot, chat_id: int, user_id: int) -> None:
        """
        Пользователь подтвердился — снимаем мут, отменяем задачу бана.
        """
        key = (chat_id, user_id)

        async with self._lock:
            pending = self._pending.pop(key, None)

        if pending:
            pending.task.cancel()

        try:
            await bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=FULL_PERMISSIONS,
            )
        except Exception as e:  # noqa: BLE001
            logger.warning(
                "Не удалось вернуть права пользователю %s в чате %s: %s",
                user_id,
                chat_id,
                e,
            )

    async def _kick_after_timeout(
        self,
        *,
        bot: Bot,
        chat_id: int,
        user_id: int,
        welcome_message_id: int,
    ) -> None:
        """
        Через timeout проверяем — если пользователь не подтвердился, кикаем.
        """
        key = (chat_id, user_id)
        try:
            await asyncio.sleep(self.timeout_seconds)

            # Пытаемся убрать служебное сообщение
            try:
                await bot.delete_message(chat_id=chat_id, message_id=welcome_message_id)
            except Exception:
                pass

            try:
                await bot.ban_chat_member(chat_id=chat_id, user_id=user_id)
                # Сразу разбан, чтобы можно было зайти ещё раз
                await bot.unban_chat_member(chat_id=chat_id, user_id=user_id)

                logger.info(
                    "Пользователь %s не прошёл проверку за %s сек и был кикнут из чата %s",
                    user_id,
                    self.timeout_seconds,
                    chat_id,
                )
            except Exception as e:  # noqa: BLE001
                logger.warning(
                    "Не удалось кикнуть пользователя %s из чата %s: %s",
                    user_id,
                    chat_id,
                    e,
                )
        finally:
            async with self._lock:
                self._pending.pop(key, None)


# --- Глобальный синглтон для простоты интеграции в хэндлеры ---

_verification_service: Optional[VerificationService] = None


def init_verification_service(timeout_seconds: int) -> VerificationService:
    """
    Инициализируем service в main.py один раз.
    """
    global _verification_service  # noqa: PLW0603

    service = VerificationService(timeout_seconds=timeout_seconds)
    _verification_service = service
    return service


def get_verification_service() -> VerificationService:
    if _verification_service is None:
        raise RuntimeError(
            "VerificationService не инициализирован. "
            "Вызови init_verification_service() из main.py до старта поллинга."
        )
    return _verification_service

```

### FILE: /var/www/logos/landing/landing/logos_tg_bot/logos_guard_bot/requirements.txt
```
aiogram>=3.0.0
python-dotenv>=1.0.0

```

### FILE: /var/www/logos/landing/landing/logos_tg_bot/logos_guard_bot/run_bot.sh
```
#!/usr/bin/env bash
set -Eeuo pipefail

cd /var/www/logos/landing/logos_tg_bot/logos_guard_bot

# venv: поддерживаем .venv и venv
if [[ -d ".venv" ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
elif [[ -d "venv" ]]; then
  # shellcheck disable=SC1091
  source venv/bin/activate
fi

# .env с токеном и настройками
if [[ -f ".env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

exec python -m bot.main

```

### FILE: /var/www/logos/landing/landing/modules/about.html
```
<section id="about" class="section">
  <h2 class="section__title" data-i18n="about_title">What is LOGOS?</h2>
  <p class="section__lead" data-i18n="about_text">
    LOGOS is a resonance-based L1 blockchain. Its core relies on Σ(t), inspired by ancient Indian temple geometry.
  </p>
  <div class="cards">
    <article class="card"><h3 data-i18n="card1_title">Resonant Core</h3><p data-i18n="card1_text">Σ(t), Λ and phase filters keep the network stable.</p></article>
    <article class="card"><h3 data-i18n="card2_title">Real Privacy</h3><p data-i18n="card2_text">Minimal metadata, strict nonce policy and phase mixing.</p></article>
    <article class="card"><h3 data-i18n="card3_title">Production‑grade</h3><p data-i18n="card3_text">Rust core, Axum REST, Prometheus/Grafana, bridge journal, health checks.</p></article>
  </div>
</section>

```

### FILE: /var/www/logos/landing/landing/modules/community.html
```
<section id="community" class="section section--alt">
  <h2 class="section__title">Сообщество и airdrop</h2>
  <p class="section__lead">
    LOGOS живёт за счёт людей. Airdrop — это вход в ядро сообщества и первый шаг
    к Web4: приватным, резонансным и устойчивым системам.
  </p>

  <!-- Airdrop блок -->
  <div id="airdrop" class="airdrop">
    <h3 class="section__subtitle">🎁 Airdrop LOGOS: что нужно сделать</h3>
    <ol class="airdrop__list">
      <li>Подключить LOGOS‑кошелёк и привязать его к airdrop‑профилю.</li>
      <li>Подписаться на наш Telegram‑канал <strong>@logosblockchain</strong>.</li>
      <li>Подписаться на X (Twitter) <strong>@OfficiaLogosLRB</strong>.</li>
      <li>Поставить лайк и сделать ретвит закреплённого твита кампании.</li>
      <li>Получить личную реферальную ссылку и пригласить до 5 друзей.</li>
      <li>Следить за прогрессом и статусом заданий на странице airdrop или через Telegram‑бота.</li>
    </ol>

    <a
      href="/airdrop.html"
      class="btn btn--primary airdrop__btn"
    >
      Перейти к airdrop‑заданиям
    </a>
  </div>

  <!-- блок про каналы/контакты -->
  <div class="community__row">
    <h3 class="section__subtitle">Каналы и связи</h3>
    <p class="section__text">
      Здесь — обновления сети, объявления о стейкинге, эксперименты с LOGOS‑AGI и
      резонансной архитектурой.
    </p>

    <div class="pill-row">
      <a class="pill" href="https://t.me/logosblockchain" target="_blank" rel="noreferrer">
        Telegram
      </a>
      <a class="pill" href="https://x.com/RspLogos" target="_blank" rel="noreferrer">
        X (Twitter)
      </a>
      <a class="pill" href="#token">
        Токеномика LGN
      </a>
    </div>

    <p class="section__meta">
      Email:
      <a href="mailto:simbiotai@proton.me">simbiotai@proton.me</a>
    </p>
  </div>
</section>

```

### FILE: /var/www/logos/landing/landing/modules/header.html
```
<header class="topbar">
  <!-- Локальный CSS только для хэдера / гамбургера -->
  <style>
    header.topbar{
      position:relative;
      z-index:30;
    }

    .topbar__right{
      position:relative;
      display:flex;
      align-items:center;
      gap:10px;
    }

    .topbar__lang button{
      border:none;
      background:transparent;
      color:#d0c8f0;
      font-size:11px;
      text-transform:uppercase;
      letter-spacing:.12em;
      padding:2px 4px;
      cursor:pointer;
    }

    .topbar__lang button.is-active{
      font-weight:600;
      border-bottom:1px solid rgba(255,255,255,.7);
    }

    .topbar__menu-toggle{
      display:none;
    }

    .topbar__burger{
      width:32px;
      height:32px;
      border-radius:999px;
      border:1px solid rgba(255,255,255,.24);
      background:rgba(6,4,18,.9);
      display:inline-flex;
      align-items:center;
      justify-content:center;
      flex-direction:column;
      gap:3px;
      cursor:pointer;
    }

    .topbar__burger span{
      width:14px;
      height:1.6px;
      border-radius:999px;
      background:#f5f0ff;
    }

    .topbar__menu{
      position:absolute;
      top:120%;
      right:0;
      min-width:220px;
      max-width:260px;
      background:rgba(6,4,18,.97);
      border-radius:16px;
      border:1px solid rgba(255,255,255,.14);
      box-shadow:0 18px 50px rgba(0,0,0,.8);
      padding:10px 10px 8px;
      opacity:0;
      transform:translateY(-6px);
      pointer-events:none;
      transition:opacity .18s ease, transform .18s ease;
    }

    .topbar__menu-list{
      list-style:none;
      margin:0;
      padding:0;
      display:flex;
      flex-direction:column;
      gap:2px;
      font-size:13px;
    }

    .topbar__menu-link{
      display:flex;
      align-items:center;
      justify-content:space-between;
      padding:7px 8px;
      border-radius:10px;
      color:#f5f0ff;
      text-decoration:none;
      gap:8px;
    }

    .topbar__menu-link span:last-child{
      font-size:11px;
      color:#b9afd4;
      white-space:nowrap;
    }

    .topbar__menu-link:hover{
      background:rgba(169,107,255,.22);
    }

    .topbar__menu-sep{
      border:none;
      border-top:1px solid rgba(255,255,255,.12);
      margin:6px 0;
    }

    /* Связка чекбокса и панели */
    .topbar__menu-toggle:checked + label.topbar__burger + .topbar__menu{
      opacity:1;
      transform:translateY(0);
      pointer-events:auto;
    }

    @media (max-width: 720px){
      .topbar__nav{
        display:none;
      }
    }
  </style>

  <div class="topbar__left">
    <div class="logo">LOGOS</div>
    <div class="logo-sub">Resonance Blockchain</div>
  </div>

  <nav class="topbar__nav">
    <a href="#about" class="nav-link" data-i18n="nav_about">About</a>
    <a href="#tech" class="nav-link" data-i18n="nav_tech">Technology</a>
    <a href="#token" class="nav-link" data-i18n="nav_token">Token</a>
    <a href="#community" class="nav-link" data-i18n="nav_comm">Community</a>
  </nav>

  <div class="topbar__right">
    <div class="topbar__lang">
      <button type="button" data-lang-btn="ru">RU</button>
      <button type="button" data-lang-btn="en">EN</button>
      <button type="button" data-lang-btn="de">DE</button>
    </div>

    <input type="checkbox" id="topbar-menu-toggle" class="topbar__menu-toggle" />
    <label for="topbar-menu-toggle" class="topbar__burger" aria-label="Menu">
      <span></span><span></span><span></span>
    </label>

    <div class="topbar__menu">
      <ul class="topbar__menu-list">
        <li>
          <a href="#about" class="topbar__menu-link">
            <span data-i18n="nav_about">About</span>
          </a>
        </li>
        <li>
          <a href="#tech" class="topbar__menu-link">
            <span data-i18n="nav_tech">Technology</span>
          </a>
        </li>
        <li>
          <a href="#token" class="topbar__menu-link">
            <span data-i18n="nav_token">Token</span>
          </a>
        </li>
        <li>
          <a href="#community" class="topbar__menu-link">
            <span data-i18n="nav_comm">Community</span>
          </a>
        </li>

        <li><hr class="topbar__menu-sep" /></li>

        <li>
          <a href="mailto:simbiotai@proton.me?subject=LOGOS%20Presale%20/Seed" class="topbar__menu-link">
            <span>Presale / Seed</span>
            <span>✉️ simbiotai@proton.me</span>
          </a>
        </li>

        <li>
          <a href="/airdrop.html" class="topbar__menu-link">
            <span>Airdrop</span>
            <span>🎁 tasks & progress</span>
          </a>
        </li>

        <li>
          <a href="https://mw-expedition.com/wallet" class="topbar__menu-link">
            <span>Web Wallet</span>
            <span>beta</span>
          </a>
        </li>
        <li>
          <a href="https://mw-expedition.com/explorer" class="topbar__menu-link">
            <span>Explorer</span>
            <span>chain view</span>
          </a>
        </li>
        <li>
          <a href="https://mw-expedition.com/staking" class="topbar__menu-link">
            <span>Staking</span>
            <span>LGN</span>
          </a>
        </li>

        <li><hr class="topbar__menu-sep" /></li>

        <li>
          <a href="https://t.me/logosblockchain" target="_blank" rel="noopener" class="topbar__menu-link">
            <span>Telegram</span>
            <span>@logosblockchain</span>
          </a>
        </li>
        <li>
          <a href="https://x.com/RspLogos" target="_blank" rel="noopener" class="topbar__menu-link">
            <span>X (Twitter)</span>
            <span>@OfficiaLogosLRB</span>
          </a>
        </li>
        <li>
          <a href="https://t.me/logosblockchain" target="_blank" rel="noopener" class="topbar__menu-link">
            <span>Airdrop bot</span>
            <span>@Logos_lrb_bot</span>
          </a>
        </li>
      </ul>
    </div>
  </div>
</header>

```

### FILE: /var/www/logos/landing/landing/modules/hero.html
```
<section class="hero">
  <div class="hero__text">
    <div class="hero__badge" data-i18n="badge_main">L1 • 81M LGN • Anonymous • Deflationary • Quantum-resistant</div>
    <h1 class="hero__title">
      <span class="hero__lambda">Λ</span>
      <span data-i18n="hero_title">Living resonance blockchain for the next era.</span>
    </h1>
    <p class="hero__subtitle" data-i18n="hero_sub">
      LOGOS combines ancient resonance structures of Indian temples with a high‑load L1 architecture designed for millions of users.
    </p>
    <div class="hero__buttons">
      <a href="#about" class="btn btn--primary" data-i18n="btn_learn_more">Learn more</a>
      <a href="/apk/app-20250830_1442.apk" class="btn btn--ghost" data-i18n="btn_download_apk">Download secure APK</a>
    </div>
    <div class="hero__meta">
      <span data-i18n="meta_supply">Total supply: 81 000 000 LGN</span>
      <span data-i18n="meta_ready">Built for real utility & mass adoption</span>
    </div>
  </div>
</section>

```

### FILE: /var/www/logos/landing/landing/modules/staking.html
```
<section id="staking" class="section">
  <h2 class="section__title" data-i18n="stake_title">Staking & RSP protocol</h2>
  <p class="section__lead" data-i18n="stake_text">
    Staking LGN ties network security and the RSP protocol to long‑term incentives for holders.
  </p>
  <div class="cards">
    <article class="card">
      <h3 data-i18n="stake_item1_title">Base staking</h3>
      <p data-i18n="stake_item1_text">
        Delegate LGN to validators and receive rewards for helping secure the network.
      </p>
    </article>
    <article class="card">
      <h3 data-i18n="stake_item2_title">RSP protocol</h3>
      <p data-i18n="stake_item2_text">
        A security layer that accounts for network phase and behaviour, making staking and the whole economy more robust.
      </p>
    </article>
    <article class="card">
      <h3 data-i18n="stake_item3_title">Missions & rewards</h3>
      <p data-i18n="stake_item3_text">
        On‑chain activity, community quests and airdrop mechanics on top of base staking.
      </p>
    </article>
  </div>
</section>

```

### FILE: /var/www/logos/landing/landing/modules/tech.html
```
<section id="tech" class="section section--alt">
  <h2 class="section__title" data-i18n="tech_title">Technology</h2>
  <div class="tech-grid">
    <div class="tech-col">
      <ul class="tech-list">
        <li data-i18n="tech_item1">L1 ledger on sled with atomic commits.</li>
        <li data-i18n="tech_item2">Resonance Consensus Protocol (RCP) with phase awareness.</li>
        <li data-i18n="tech_item3">Anti‑spam & dynamic balance against overload.</li>
        <li data-i18n="tech_item4">Encrypted bridge, durable journal & HMAC endpoints.</li>
        <li data-i18n="tech_item5">Web wallet, explorer & API for integrations.</li>
      </ul>
    </div>
    <div class="tech-col tech-col--note">
      <p data-i18n="tech_note">Private, resonance‑driven and robust systems — without sacrificing speed or UX.</p>
    </div>
  </div>
</section>

```

### FILE: /var/www/logos/landing/landing/modules/token.html
```
<section id="token" class="section">
  <h2 class="section__title" data-i18n="token_title">LGN Tokenomics</h2>
  <p class="section__lead" data-i18n="token_text">LGN is the base token of LOGOS. Total 81 000 000 LGN. Deflationary.</p>
  <div class="token-grid">
    <div class="token-grid__item"><span class="token-grid__label" data-i18n="token_staking">Staking & Holders</span><span class="token-grid__value">25%</span></div>
    <div class="token-grid__item"><span class="token-grid__label" data-i18n="token_rcp">RSP security protocol</span><span class="token-grid__value">20%</span></div>
    <div class="token-grid__item"><span class="token-grid__label" data-i18n="token_liq">Liquidity (DEX/CEX)</span><span class="token-grid__value">15%</span></div>
    <div class="token-grid__item"><span class="token-grid__label" data-i18n="token_stab">Stability Fund</span><span class="token-grid__value">15%</span></div>
    <div class="token-grid__item"><span class="token-grid__label" data-i18n="token_core">Founder & Core Dev</span><span class="token-grid__value">20%</span></div>
    <div class="token-grid__item"><span class="token-grid__label" data-i18n="token_airdrop">Airdrop & DAO</span><span class="token-grid__value">5%</span></div>
  </div>
</section>

```

### FILE: /var/www/logos/landing/landing/shared/airdrop-fix.js
```
(() => {
  'use strict';
  const API='/airdrop-api/api/airdrop';
  const K_T='logos_airdrop_token_v1', K_X='logos_airdrop_xu_v1';

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

;(() => {
  try {
    const kill = () => {
      const nodes = Array.from(document.querySelectorAll("div,li,section,p,span"));
      for (const n of nodes) {
        const t = (n.textContent || "").toLowerCase();
        if (t.includes("follow") && (t.includes("x") || t.includes("twitter"))) {
          n.style.display = "none";
        }
        if (t.includes("подпис") && (t.includes("x") || t.includes("твит"))) {
          n.style.display = "none";
        }
      }
    };
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", kill);
    else kill();
  } catch {}
})();

```

### FILE: /var/www/logos/landing/landing/styles.v20251124.css
```
:root{
  --bg:#05030b;
  --fg:#f5f0ff;
  --muted:#b9afd4;
  --accent:#e36bff;
  --border-soft:rgba(255,255,255,0.12);
  --card-bg:rgba(13,7,34,0.96);
  --shadow-soft:0 22px 60px rgba(0,0,0,0.75);
}

*{box-sizing:border-box;margin:0;padding:0}
html,body{
  min-height:100%;
  background:var(--bg);
  color:var(--fg);
  font-family:system-ui,-apple-system,"Inter",sans-serif;
  -webkit-font-smoothing:antialiased;
}
a{text-decoration:none;color:inherit}
img{max-width:100%;display:block}

/* Базовый градиент */

body{
  background:
    radial-gradient(1600px 900px at 10% 0%, rgba(130,90,240,.22), transparent 60%),
    radial-gradient(1500px 900px at 90% 100%, rgba(40,26,110,.30), transparent 65%),
    #05030b;
}

/* Резонансный слой */

.bg-layer{
  position:fixed;
  inset:0;
  z-index:-1;
  pointer-events:none;
  background:
    radial-gradient(circle at 15% 12%, rgba(210,160,255,0.26) 0, transparent 55%),
    radial-gradient(circle at 82% 78%, rgba(150,110,255,0.28) 0, transparent 60%),
    radial-gradient(circle at 48% 40%, rgba(255,255,255,0.08) 0, transparent 55%),
    repeating-radial-gradient(circle at 18% 18%,
      rgba(220,180,255,0.20) 0px,
      rgba(220,180,255,0.20) 1px,
      transparent 1px,
      transparent 18px),
    repeating-radial-gradient(circle at 80% 72%,
      rgba(190,150,255,0.18) 0px,
      rgba(190,150,255,0.18) 1px,
      transparent 1px,
      transparent 24px);
  mix-blend-mode:screen;
  opacity:.9;
}

/* Лейаут */

.page-wrap{
  max-width:960px;
  margin:0 auto;
  padding:20px 16px 40px;
}
@media (min-width:960px){
  .page-wrap{padding:26px 0 56px;}
}

/* Шапка */

.topbar{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:12px;
  margin-bottom:20px;
}
.brand{
  display:flex;
  flex-direction:column;
  gap:2px;
}
.brand__logo{
  font-size:14px;
  font-weight:700;
  letter-spacing:0.14em;
  text-transform:uppercase;
}
.brand__sub{
  font-size:10px;
  text-transform:uppercase;
  letter-spacing:0.18em;
  color:var(--muted);
}

/* Бургер */

.menu-toggle{
  width:34px;
  height:26px;
  border:none;
  background:transparent;
  cursor:pointer;
  display:flex;
  flex-direction:column;
  justify-content:space-between;
  padding:3px 2px;
}
.menu-toggle span{
  display:block;
  height:2px;
  border-radius:999px;
  background:#fdfbff;
  transition:transform .2s ease-out,opacity .2s ease-out;
}
body.menu-open .menu-toggle span:nth-child(1){
  transform:translateY(8px) rotate(45deg);
}
body.menu-open .menu-toggle span:nth-child(2){
  opacity:0;
}
body.menu-open .menu-toggle span:nth-child(3){
  transform:translateY(-8px) rotate(-45deg);
}

/* Меню-оверлей */

.menu[hidden]{display:none;}
.menu{
  position:fixed;
  inset:0;
  z-index:20;
  background:rgba(5,3,18,0.97);
  backdrop-filter:blur(18px);
}
.menu__inner{
  max-width:960px;
  margin:70px auto 24px;
  padding:0 16px 24px;
  display:grid;
  gap:18px;
}
.menu__section{
  border-radius:16px;
  border:1px solid rgba(255,255,255,0.10);
  background:rgba(12,7,32,0.98);
  padding:12px 14px;
}
.menu__label{
  font-size:11px;
  text-transform:uppercase;
  letter-spacing:0.18em;
  color:var(--muted);
  margin-bottom:8px;
}
.menu__langs{
  display:flex;
  gap:8px;
}
.menu__langs button{
  border-radius:999px;
  border:1px solid rgba(255,255,255,0.16);
  padding:6px 12px;
  font-size:11px;
  background:rgba(7,4,22,0.96);
  color:var(--muted);
  cursor:pointer;
}
.menu__langs button.is-active{
  background:var(--accent);
  border-color:var(--accent);
  color:#1b041c;
}
.menu__section a{
  display:inline-flex;
  margin:2px 4px 4px 0;
  padding:6px 12px;
  border-radius:999px;
  border:1px solid rgba(255,255,255,0.14);
  background:rgba(9,5,26,0.96);
  font-size:13px;
}
.menu__section a:hover{
  border-color:var(--accent);
}

/* Контент */

.page{
  display:flex;
  flex-direction:column;
  gap:18px;
}
.block{
  border-radius:20px;
  background:var(--card-bg);
  border:1px solid var(--border-soft);
  box-shadow:var(--shadow-soft);
  padding:20px 18px 22px;
}
.block__title{
  font-size:20px;
  margin-bottom:10px;
}
.block__text{
  font-size:14px;
  line-height:1.6;
  color:var(--fg);
  margin-bottom:8px;
}
.block__list{
  margin:4px 0 4px 20px;
}
.block__list li{
  font-size:14px;
  line-height:1.5;
  color:var(--muted);
  margin-bottom:4px;
}

@media (min-width:960px){
  .block{
    padding:24px 24px 26px;
  }
  .block__title{
    font-size:22px;
  }
  .block__text,.block__list li{
    font-size:15px;
  }
}

/* Футер */

.footer{
  margin-top:20px;
  font-size:11px;
  color:var(--muted);
}

```

### FILE: /var/www/logos/landing/landing/wallet/app.html
```
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Wallet — Кошелёк</title>
  <style>
    body{
      font-family:system-ui,Segoe UI,Roboto,Arial,sans-serif;
      margin:0;background:#0b0c10;color:#e6edf3
    }
    header{
      padding:12px 20px 10px;
      background:#11151a;
      border-bottom:1px solid #1e242c;
      position:sticky;top:0;z-index:10
    }
    h1{font-size:18px;margin:0}
    header .sub{
      font-size:12px;
      opacity:.8;
      margin-top:4px
    }
    main{
      max-width:1024px;
      margin:24px auto;
      padding:0 16px 40px
    }
    section{
      background:#11151a;
      margin:16px 0;
      border-radius:12px;
      padding:16px;
      border:1px solid #1e242c
    }
    h3{margin:0 0 8px;font-size:16px}
    label{display:block;margin:8px 0 6px}
    .grid{
      display:grid;
      grid-template-columns:1fr 1fr;
      gap:12px
    }
    @media (max-width:900px){
      .grid{grid-template-columns:1fr}
    }
    input,button,textarea{
      width:100%;
      padding:10px;
      border-radius:10px;
      border:1px solid #2a313a;
      background:#0b0f14;
      color:#e6edf3;
      box-sizing:border-box;
      font-size:14px;
    }
    textarea{resize:vertical;min-height:70px}
    button{
      cursor:pointer;
      border:1px solid #3b7ddd;
      background:#1665c1;
    }
    button.secondary{background:#1b2129}
    button:disabled{opacity:.6;cursor:not-allowed}
    .mono{font-family:ui-monospace,Menlo,Consolas,monospace}
    small{opacity:.8}
    pre{
      background:#0b0f14;
      border-radius:10px;
      border:1px solid #2a313a;
      padding:8px;
      font-size:13px;
      white-space:pre-wrap;
    }
  </style>
</head>
<body>
<header>
  <h1>LOGOS Wallet — Кошелёк</h1>
  <div class="sub">Endpoint: <span id="endpoint" class="mono"></span></div>
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
        <p><small>
          Ключи лежат только в памяти этой вкладки. После 15 минут бездействия или
          закрытия вкладки кошелёк автоматически блокируется — при следующем входе
          нужен пароль.
        </small></p>
      </div>
      <div>
        <h3>Баланс</h3>
        <div class="grid">
          <div>
            <label>RID</label>
            <input id="rid-balance" class="mono" placeholder="RID (base58)"/>
          </div>
          <div>
            <label>&nbsp;</label>
            <button id="btn-balance">Показать баланс</button>
          </div>
        </div>
        <pre id="out-balance" class="mono" style="margin-top:12px;min-height:40px"></pre>
      </div>
    </div>
  </section>

  <section>
    <h3>Подпись и отправка (batch)</h3>
    <div class="grid">
      <div>
        <label>Получатель (RID)</label>
        <input id="to" class="mono" placeholder="RID получателя"/>
      </div>
      <div>
        <label>Сумма (LGN)</label>
        <input id="amount" type="number" min="1" step="1" value="1"/>
      </div>
    </div>
    <div class="grid">
      <div>
        <label>Nonce</label>
        <input id="nonce" type="number" min="1" step="1" placeholder="нажми «Получить nonce»"/>
      </div>
      <div>
        <label>&nbsp;</label>
        <button id="btn-send">Подписать и отправить</button>
      </div>
    </div>
    <pre id="out-send" class="mono" style="margin-top:12px;min-height:40px"></pre>
  </section>

  <section>
    <h3>Стейкинг (delegate / undelegate / claim)</h3>
    <p><small>
      Здесь можно залочить токены в стейкинг (delegate), снять часть/всё (undelegate) и
      забрать накопленные награды (claim). Все операции идут через REST /stake/*.
    </small></p>
    <div class="grid">
      <div>
        <label>Текущий статус стейкинга</label>
        <pre id="out-stake" class="mono" style="min-height:80px"></pre>
        <button id="btn-stake-refresh" class="secondary" style="margin-top:8px">
          Обновить статус стейкинга
        </button>
      </div>
      <div>
        <label>Застейкать (делегировать, LGN)</label>
        <input id="stake-amount" type="number" min="1" step="1" value="0"/>
        <button id="btn-stake-delegate" style="margin-top:8px">Делегировать</button>

        <label style="margin-top:14px">Разстейкать (undelegate, LGN)</label>
        <input id="unstake-amount" type="number" min="1" step="1" value="0"/>
        <button id="btn-stake-undelegate" style="margin-top:8px">Снять делегацию</button>

        <label style="margin-top:14px">Накопленные награды</label>
        <button id="btn-stake-claim" style="margin-top:8px">Заявить награду (claim)</button>
      </div>
    </div>
  </section>

  <section>
    <h3>Мост rToken (депозит, демо)</h3>
    <div class="grid">
      <div>
        <label>ext_txid</label>
        <input id="ext" class="mono" placeholder="например eth_txid_0xabc"/>
      </div>
      <div>
        <label>&nbsp;</label>
        <button id="btn-deposit">Deposit rLGN (demo)</button>
      </div>
    </div>
    <pre id="out-bridge" class="mono" style="margin-top:12px;min-height:40px"></pre>
  </section>
</main>
<script src="./app.js?v=20251129_01" defer></script>
</body>
</html>

```

### FILE: /var/www/logos/landing/landing/wallet/app.js
```
// APP v2: ключи в памяти вкладки, авто-лок, стейкинг.
// RID и пароль берём из sessionStorage, приватный ключ расшифровываем из IndexedDB.

const API     = location.origin + '/api';
const DB_NAME = 'logos_wallet_v2';
const STORE   = 'keys';
const ALPH    = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';
const enc     = new TextEncoder();

const $ = s => document.querySelector(s);
const toHex = b => [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join('');
const fromHex = h => {
  if (!h) return new Uint8Array([]);
  const clean = h.trim();
  if (!clean) return new Uint8Array([]);
  return new Uint8Array(clean.match(/.{1,2}/g).map(x => parseInt(x, 16)));
};
const b58 = bytes => {
  const h = [...new Uint8Array(bytes)].map(b => b.toString(16).padStart(2, '0')).join('');
  let x = BigInt('0x' + h), o = '';
  while (x > 0n) { o = ALPH[Number(x % 58n)] + o; x /= 58n; }
  return o || '1';
};

function ensureEnv() {
  if (!window.isSecureContext) throw new Error('Нужен HTTPS (secure context)');
  if (!window.indexedDB)      throw new Error('IndexedDB недоступен');
  if (!window.crypto || !window.crypto.subtle) throw new Error('WebCrypto недоступен');
}

// IndexedDB
const idb = () => new Promise((res, rej) => {
  const r = indexedDB.open(DB_NAME, 1);
  r.onupgradeneeded = () => r.result.createObjectStore(STORE);
  r.onsuccess = () => res(r.result);
  r.onerror   = () => rej(r.error);
});
const idbGet = async k => {
  const db = await idb();
  return new Promise((res, rej) => {
    const t = db.transaction(STORE, 'readonly').objectStore(STORE).get(k);
    t.onsuccess = () => res(t.result || null);
    t.onerror   = () => rej(t.error);
  });
};

// Crypto helpers для приватного ключа
async function deriveKey(pass, salt) {
  const keyMat = await crypto.subtle.importKey(
    'raw',
    enc.encode(pass),
    'PBKDF2',
    false,
    ['deriveKey']
  );
  return crypto.subtle.deriveKey(
    { name: 'PBKDF2', salt, iterations: 120000, hash: 'SHA-256' },
    keyMat,
    { name: 'AES-GCM', length: 256 },
    false,
    ['decrypt']
  );
}
async function aesDecrypt(aesKey, iv, ct) {
  return crypto.subtle.decrypt(
    { name: 'AES-GCM', iv: new Uint8Array(iv) },
    aesKey,
    new Uint8Array(ct)
  );
}
async function importKey(pass, meta) {
  const aes = await deriveKey(pass, new Uint8Array(meta.salt));
  const pkcs8 = await aesDecrypt(aes, meta.iv, meta.priv);
  const privateKey = await crypto.subtle.importKey(
    'pkcs8',
    pkcs8,
    { name: 'Ed25519' },
    true,
    ['sign']
  );
  const publicKey = await crypto.subtle.importKey(
    'raw',
    new Uint8Array(meta.pub),
    { name: 'Ed25519' },
    true,
    ['verify']
  );
  return { privateKey, publicKey };
}

// Session + авто-лочка
const PASS = sessionStorage.getItem('logos_pass');
const RID  = sessionStorage.getItem('logos_rid');
if (!PASS || !RID) {
  location.replace('./login.html');
  throw new Error('locked');
}

let KEYS = null;
let META = null;
let autoLockTimer = null;
const AUTO_LOCK_MS = 15 * 60 * 1000; // 15 минут

function lockNow() {
  sessionStorage.clear();
  location.replace('./login.html');
}

function bumpActivity() {
  if (autoLockTimer) clearTimeout(autoLockTimer);
  autoLockTimer = setTimeout(lockNow, AUTO_LOCK_MS);
}

['click', 'keydown', 'mousemove', 'touchstart'].forEach(ev => {
  window.addEventListener(ev, bumpActivity, { passive: true });
});

// API helpers
async function getJSON(url, body) {
  const opts = body
    ? {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        credentials: 'same-origin',
        cache: 'no-store'
      }
    : {
        method: 'GET',
        credentials: 'same-origin',
        cache: 'no-store'
      };
  const r = await fetch(url, opts);
  if (!r.ok) throw new Error(`${r.status} ${await r.text()}`);
  return r.json();
}
async function getNonce(rid) {
  const j = await getJSON(`${API}/balance/${rid}`);
  return j.nonce || 0;
}
async function canonHex(from, to, amount, nonce) {
  const r = await fetch(`${API}/debug_canon`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'same-origin',
    cache: 'no-store',
    body: JSON.stringify({
      tx: {
        from,
        to,
        amount: Number(amount),
        nonce: Number(nonce)
      }
    })
  });
  if (!r.ok) throw new Error(`/debug_canon ${r.status} ${await r.text()}`);
  const j = await r.json();
  return j.canon_hex;
}
async function submitBatch(txs) {
  const r = await fetch(`${API}/submit_tx_batch`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'same-origin',
    cache: 'no-store',
    body: JSON.stringify({ txs })
  });
  if (!r.ok) throw new Error(`/submit_tx_batch ${r.status} ${await r.text()}`);
  return r.json();
}
async function deposit(rid, amount, ext) {
  const r = await fetch(`${API}/bridge/deposit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'same-origin',
    cache: 'no-store',
    body: JSON.stringify({ rid, amount: Number(amount), ext_txid: ext })
  });
  return { status: r.status, text: await r.text() };
}

// Staking API wrappers
async function getStakeInfo(rid) {
  return getJSON(`${API}/stake/my/${encodeURIComponent(rid)}`);
}
async function stakeDelegate(rid, amount) {
  return getJSON(`${API}/stake/delegate`, { rid, amount: Number(amount) });
}
async function stakeUndelegate(rid, amount) {
  return getJSON(`${API}/stake/undelegate`, { rid, amount: Number(amount) });
}
async function stakeClaim(rid) {
  return getJSON(`${API}/stake/claim`, { rid });
}

async function signCanon(privateKey, canonHexStr) {
  const msg = fromHex(canonHexStr);
  const sig = await crypto.subtle.sign('Ed25519', privateKey, msg);
  return [...new Uint8Array(sig)].map(b => b.toString(16).padStart(2, '0')).join('');
}

// UI helpers
async function refreshBalance() {
  const out = $('#out-balance');
  try {
    const rid = ($('#rid-balance')?.value || '').trim() || RID;
    const j = await getJSON(`${API}/balance/${rid}`);
    if (out) out.textContent = JSON.stringify(j, null, 2);
  } catch (e) {
    if (out) out.textContent = 'ERR: ' + e;
  }
}
async function refreshStake() {
  const out = $('#out-stake');
  if (!out) return;
  try {
    const j = await getStakeInfo(RID);
    out.textContent = JSON.stringify(j, null, 2);
  } catch (e) {
    out.textContent = 'ERR: ' + e;
  }
}

// Boot
(async () => {
  try {
    ensureEnv();
    META = await idbGet('acct:' + RID);
    if (!META) {
      lockNow();
      return;
    }
    KEYS = await importKey(PASS, META);

    const pubArea = $('#pub');
    if (pubArea) {
      pubArea.value = `RID: ${RID}\nPUB (hex): ${toHex(new Uint8Array(META.pub))}`;
    }
    const rb = $('#rid-balance');
    if (rb) rb.value = RID;

    const ep = $('#endpoint');
    if (ep) ep.textContent = API;

    bumpActivity();
    refreshBalance();
    refreshStake();
  } catch (e) {
    alert('Ошибка инициализации кошелька: ' + e);
    lockNow();
  }
})();

// Buttons
const btnLock = $('#btn-lock');
if (btnLock) {
  btnLock.addEventListener('click', () => {
    lockNow();
  });
}

const btnNonce = $('#btn-nonce');
if (btnNonce) {
  btnNonce.addEventListener('click', async () => {
    bumpActivity();
    try {
      const n = await getNonce(RID);
      const nonceInput = $('#nonce');
      if (nonceInput) nonceInput.value = String(n + 1);
    } catch (e) {
      alert('ERR ' + e);
    }
  });
}

const btnBalance = $('#btn-balance');
if (btnBalance) {
  btnBalance.addEventListener('click', () => {
    bumpActivity();
    refreshBalance();
  });
}

const btnSend = $('#btn-send');
if (btnSend) {
  btnSend.addEventListener('click', async () => {
    bumpActivity();
    const to = $('#to')?.value.trim();
    const amountStr = $('#amount')?.value || '';
    const nonceStr  = $('#nonce')?.value  || '';
    const out = $('#out-send');
    try {
      if (!to) throw new Error('Укажи RID получателя');
      const amount = Number(amountStr);
      const nonce  = Number(nonceStr);
      if (!Number.isFinite(amount) || amount <= 0) throw new Error('Сумма должна быть > 0');
      if (!Number.isFinite(nonce)  || nonce  <= 0) throw new Error('Nonce должен быть > 0');

      const ch  = await canonHex(RID, to, amount, nonce);
      const sig = await signCanon(KEYS.privateKey, ch);
      const res = await submitBatch([{
        from: RID,
        to,
        amount,
        nonce,
        sig_hex: sig
      }]);
      if (out) out.textContent = JSON.stringify(res, null, 2);
    } catch (e) {
      if (out) out.textContent = 'ERR: ' + e;
    }
  });
}

const btnDeposit = $('#btn-deposit');
if (btnDeposit) {
  btnDeposit.addEventListener('click', async () => {
    bumpActivity();
    const ext = $('#ext')?.value.trim() || 'ext_txid_demo';
    const out = $('#out-bridge');
    try {
      const r = await deposit(RID, 123, ext);
      if (out) out.textContent = `HTTP ${r.status}\n${r.text}`;
    } catch (e) {
      if (out) out.textContent = 'ERR: ' + e;
    }
  });
}

// Staking buttons
const btnStakeRefresh = $('#btn-stake-refresh');
if (btnStakeRefresh) {
  btnStakeRefresh.addEventListener('click', () => {
    bumpActivity();
    refreshStake();
  });
}

const btnStakeDelegate = $('#btn-stake-delegate');
if (btnStakeDelegate) {
  btnStakeDelegate.addEventListener('click', async () => {
    bumpActivity();
    const amtStr = $('#stake-amount')?.value || '';
    const out = $('#out-stake');
    try {
      const amount = Number(amtStr);
      if (!Number.isFinite(amount) || amount <= 0) {
        throw new Error('Сумма для стейкинга должна быть > 0');
      }
      const res = await stakeDelegate(RID, amount);
      if (out) out.textContent = 'delegate OK:\n' + JSON.stringify(res, null, 2);
      await refreshStake();
    } catch (e) {
      if (out) out.textContent = 'ERR: ' + e;
    }
  });
}

const btnStakeUndelegate = $('#btn-stake-undelegate');
if (btnStakeUndelegate) {
  btnStakeUndelegate.addEventListener('click', async () => {
    bumpActivity();
    const amtStr = $('#unstake-amount')?.value || '';
    const out = $('#out-stake');
    try {
      const amount = Number(amtStr);
      if (!Number.isFinite(amount) || amount <= 0) {
        throw new Error('Сумма для снятия должна быть > 0');
      }
      const res = await stakeUndelegate(RID, amount);
      if (out) out.textContent = 'undelegate OK:\n' + JSON.stringify(res, null, 2);
      await refreshStake();
    } catch (e) {
      if (out) out.textContent = 'ERR: ' + e;
    }
  });
}

const btnStakeClaim = $('#btn-stake-claim');
if (btnStakeClaim) {
  btnStakeClaim.addEventListener('click', async () => {
    bumpActivity();
    const out = $('#out-stake');
    try {
      const res = await stakeClaim(RID);
      if (out) out.textContent = 'claim OK:\n' + JSON.stringify(res, null, 2);
      await refreshStake();
    } catch (e) {
      if (out) out.textContent = 'ERR: ' + e;
    }
  });
}

```

### FILE: /var/www/logos/landing/landing/wallet/auth.js
```
// AUTH v4: RID + пароль + 16-словная фраза восстановления.
// Ключи только локально (IndexedDB + AES-GCM), приватник никогда не уходит в сеть.

const DB_NAME = 'logos_wallet_v2';
const STORE   = 'keys';
const enc     = new TextEncoder();
const ALPH    = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';

const $ = s => document.querySelector(s);
const out = msg => { const el = $('#out'); if (el) el.textContent = String(msg); };

function normRid(s) { return (s || '').replace(/\s+/g, '').trim(); }

function ensureEnv() {
  if (!window.isSecureContext) throw new Error('Нужен HTTPS (secure context)');
  if (!window.indexedDB)      throw new Error('IndexedDB недоступен');
  if (!window.crypto || !window.crypto.subtle) throw new Error('WebCrypto недоступен');
}

// IndexedDB helpers
const idb = () => new Promise((res, rej) => {
  const r = indexedDB.open(DB_NAME, 1);
  r.onupgradeneeded = () => r.result.createObjectStore(STORE);
  r.onsuccess = () => res(r.result);
  r.onerror   = () => rej(r.error);
});
const idbGet = async k => {
  const db = await idb();
  return new Promise((res, rej) => {
    const t = db.transaction(STORE, 'readonly').objectStore(STORE).get(k);
    t.onsuccess = () => res(t.result || null);
    t.onerror   = () => rej(t.error);
  });
};
const idbSet = async (k, v) => {
  const db = await idb();
  return new Promise((res, rej) => {
    const t = db.transaction(STORE, 'readwrite').objectStore(STORE).put(v, k);
    t.onsuccess = () => res();
    t.onerror   = () => rej(t.error);
  });
};
const idbDel = async k => {
  const db = await idb();
  return new Promise((res, rej) => {
    const t = db.transaction(STORE, 'readwrite').objectStore(STORE).delete(k);
    t.onsuccess = () => res();
    t.onerror   = () => rej(t.error);
  });
};

// base58 для RID (как в ядре)
const b58 = bytes => {
  const h = [...new Uint8Array(bytes)].map(b => b.toString(16).padStart(2, '0')).join('');
  let x = BigInt('0x' + h), o = '';
  while (x > 0n) { o = ALPH[Number(x % 58n)] + o; x /= 58n; }
  return o || '1';
};

// Password helpers
function validateNewPassword(pass) {
  if (!pass || pass.length < 10) {
    throw new Error('Пароль ≥10 символов');
  }
  if (!/[A-Za-z]/.test(pass) || !/[0-9]/.test(pass)) {
    throw new Error('Пароль должен содержать буквы и цифры');
  }
  return pass;
}
function ensureLoginPassword(pass) {
  if (!pass || pass.length < 6) throw new Error('Пароль ≥6 символов');
  return pass;
}

// Crypto helpers
async function deriveKey(pass, salt) {
  const keyMat = await crypto.subtle.importKey(
    'raw',
    enc.encode(pass),
    'PBKDF2',
    false,
    ['deriveKey']
  );
  return crypto.subtle.deriveKey(
    { name: 'PBKDF2', salt, iterations: 120000, hash: 'SHA-256' },
    keyMat,
    { name: 'AES-GCM', length: 256 },
    false,
    ['encrypt', 'decrypt']
  );
}
async function aesEncrypt(aesKey, data) {
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const ct = new Uint8Array(
    await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, aesKey, data)
  );
  return { iv: Array.from(iv), ct: Array.from(ct) };
}
async function aesDecrypt(aesKey, iv, ct) {
  return new Uint8Array(
    await crypto.subtle.decrypt(
      { name: 'AES-GCM', iv: new Uint8Array(iv) },
      aesKey,
      new Uint8Array(ct)
    )
  );
}

// Accounts index
async function addAccount(rid) {
  const list = (await idbGet('accounts')) || [];
  if (!list.includes(rid)) {
    list.push(rid);
    await idbSet('accounts', list);
  }
}
async function listAccounts() {
  return (await idbGet('accounts')) || [];
}

// Mnemonic helpers (16 псевдо-слов, seed = SHA-256("logos-lrb-ed25519:"+phrase))
const MN_WORDS = 16;
const MN_ALPH  = 'abcdefghjkmnpqrstuvwxyz'; // без легко путаемых символов

function randomWord(len = 5) {
  const buf = new Uint8Array(len);
  crypto.getRandomValues(buf);
  let w = '';
  for (let i = 0; i < len; i++) {
    w += MN_ALPH[buf[i] % MN_ALPH.length];
  }
  return w;
}

function generateMnemonic() {
  const words = [];
  for (let i = 0; i < MN_WORDS; i++) words.push(randomWord());
  return words.join(' ');
}

function normalizeMnemonic(s) {
  return (s || '').trim().toLowerCase().replace(/\s+/g, ' ');
}

async function mnemonicToSeedBytes(mnemonic) {
  const norm = normalizeMnemonic(mnemonic);
  if (!norm) throw new Error('Резервная фраза пуста');
  const data = 'logos-lrb-ed25519:' + norm;
  const hash = await crypto.subtle.digest('SHA-256', enc.encode(data));
  return new Uint8Array(hash); // 32 байта
}

// PKCS8 Ed25519 (RFC 8410): 302e020100300506032b657004220420 || seed32
const ED25519_PKCS8_PREFIX = new Uint8Array([
  0x30, 0x2e, 0x02, 0x01, 0x00,
  0x30, 0x05, 0x06, 0x03, 0x2b, 0x65, 0x70,
  0x04, 0x22, 0x04, 0x20
]);

function buildPkcs8FromSeed(seed) {
  if (!(seed instanceof Uint8Array) || seed.length !== 32) {
    throw new Error('seed должен быть 32 байта');
  }
  const outArr = new Uint8Array(ED25519_PKCS8_PREFIX.length + seed.length);
  outArr.set(ED25519_PKCS8_PREFIX, 0);
  outArr.set(seed, ED25519_PKCS8_PREFIX.length);
  return outArr;
}

function base64urlToBytes(str) {
  const pad = str.length % 4 === 2 ? '==' : str.length % 4 === 3 ? '=' : '';
  const b64 = str.replace(/-/g, '+').replace(/_/g, '/') + pad;
  const bin = atob(b64);
  const outArr = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) outArr[i] = bin.charCodeAt(i);
  return outArr;
}

// Pending state для подтверждения фразы
let pendingRid = null;
let pendingMnemonic = null;

async function createAccount(passRaw) {
  ensureEnv();
  const pass = validateNewPassword(passRaw);

  out('Создаём ключ и фразу…');

  // 1) фраза и seed
  const mnemonic = generateMnemonic();
  const seed = await mnemonicToSeedBytes(mnemonic);
  const pkcs8 = buildPkcs8FromSeed(seed);

  // 2) публичный ключ через JWK
  const privateKey = await crypto.subtle.importKey(
    'pkcs8',
    pkcs8,
    { name: 'Ed25519' },
    true,
    ['sign']
  );
  const jwk = await crypto.subtle.exportKey('jwk', privateKey);
  if (!jwk || !jwk.x) throw new Error('Не удалось извлечь публичный ключ');
  const pubBytes = base64urlToBytes(jwk.x);
  const rid = b58(pubBytes);

  // 3) шифруем приватник на пароль
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const aes = await deriveKey(pass, salt);
  const { iv, ct } = await aesEncrypt(aes, pkcs8);
  const meta = {
    rid,
    pub: Array.from(pubBytes),
    salt: Array.from(salt),
    iv,
    priv: ct
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
    sec.style.display = 'block';
    sec.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  out('RID создан: ' + rid + '. Обязательно запиши фразу выше и подтверди её.');
}

async function loginAccount(ridRaw, passRaw) {
  ensureEnv();
  const rid = normRid(ridRaw);
  const pass = ensureLoginPassword(passRaw);

  if (!rid) throw new Error('Укажи RID');

  const meta = await idbGet('acct:' + rid);
  if (!meta) {
    const list = await listAccounts();
    throw new Error(
      'RID не найден на этом устройстве. Сохранённые RID:\n' +
      (list.length ? list.join('\n') : '—')
    );
  }
  const aes = await deriveKey(pass, new Uint8Array(meta.salt));
  try {
    await aesDecrypt(aes, meta.iv, meta.priv);
  } catch (e) {
    throw new Error('Неверный пароль');
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

  out('Восстанавливаем кошелёк из фразы…');

  const seed = await mnemonicToSeedBytes(mnemonic);
  const pkcs8 = buildPkcs8FromSeed(seed);

  const privateKey = await crypto.subtle.importKey(
    'pkcs8',
    pkcs8,
    { name: 'Ed25519' },
    true,
    ['sign']
  );
  const jwk = await crypto.subtle.exportKey('jwk', privateKey);
  if (!jwk || !jwk.x) throw new Error('Не удалось извлечь публичный ключ');
  const pubBytes = base64urlToBytes(jwk.x);
  const rid = b58(pubBytes);

  const salt = crypto.getRandomValues(new Uint8Array(16));
  const aes = await deriveKey(pass, salt);
  const { iv, ct } = await aesEncrypt(aes, pkcs8);
  const meta = {
    rid,
    pub: Array.from(pubBytes),
    salt: Array.from(salt),
    iv,
    priv: ct
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
  for (const rid of list) {
    await idbDel('acct:' + rid);
  }
  await idbDel('accounts');
  await idbDel('last_rid');
  sessionStorage.clear();
  out('Все аккаунты удалены.');
}

function renderRidList(list) {
  const wrap = $('#listWrap');
  const ul = $('#ridList');
  if (!wrap || !ul) return;
  ul.innerHTML = '';
  wrap.style.display = 'block';
  if (!list.length) {
    ul.innerHTML = '<li>— пусто —</li>';
    return;
  }
  list.forEach(rid => {
    const li = document.createElement('li');
    li.textContent = rid;
    li.addEventListener('click', () => {
      const inp = $('#loginRid');
      if (inp) inp.value = rid;
      out('RID подставлен');
    });
    ul.appendChild(li);
  });
}

// авто-подстановка last_rid и скрытие DEV-сброса в проде
(async () => {
  try {
    const last = await idbGet('last_rid');
    const loginRid = $('#loginRid');
    if (last && loginRid) loginRid.value = last;
  } catch (e) {
    console.error(e);
  }
  const resetBtn = $('#btn-reset');
  if (resetBtn) {
    const isDevHost = ['localhost', '127.0.0.1'].includes(location.hostname);
    if (!isDevHost) {
      resetBtn.style.display = 'none';
    }
  }
})();

// UI wiring
const btnLogin = $('#btn-login');
if (btnLogin) {
  btnLogin.addEventListener('click', async () => {
    const rid  = $('#loginRid')?.value || '';
    const pass = $('#loginPass')?.value || '';
    try {
      await loginAccount(rid, pass);
    } catch (e) {
      out('ERR: ' + (e && e.message ? e.message : e));
    }
  });
}

const btnCreate = $('#btn-create');
if (btnCreate) {
  btnCreate.addEventListener('click', async () => {
    const pass = $('#createPass')?.value || '';
    try {
      await createAccount(pass);
    } catch (e) {
      out('ERR: ' + (e && e.message ? e.message : e));
    }
  });
}

const btnList = $('#btn-list');
if (btnList) {
  btnList.addEventListener('click', async () => {
    try {
      renderRidList(await listAccounts());
    } catch (e) {
      out('ERR: ' + (e && e.message ? e.message : e));
    }
  });
}

const btnReset = $('#btn-reset');
if (btnReset) {
  btnReset.addEventListener('click', () => {
    const isDevHost = ['localhost', '127.0.0.1'].includes(location.hostname);
    if (!isDevHost) {
      alert('Сброс доступен только на dev-хосте (localhost).');
      return;
    }
    resetAll().catch(e => out('ERR: ' + e));
  });
}

const btnMnemonicOk = $('#btn-mnemonic-ok');
if (btnMnemonicOk) {
  btnMnemonicOk.addEventListener('click', () => {
    if (!pendingRid || !pendingMnemonic) {
      out('Нет созданного кошелька для подтверждения');
      return;
    }
    const confirmInput = $('#mnemonicConfirm');
    const typed = confirmInput ? normalizeMnemonic(confirmInput.value) : '';
    if (!typed) {
      out('Повтори фразу для подтверждения');
      return;
    }
    if (typed !== normalizeMnemonic(pendingMnemonic)) {
      out('Фразы не совпадают. Проверь, что записал всё без ошибок.');
      return;
    }
    out('Фраза подтверждена, вход…');
    location.href = './app.html';
  });
}

const btnRestore = $('#btn-restore');
if (btnRestore) {
  btnRestore.addEventListener('click', async () => {
    const phrase = $('#restoreMnemonic')?.value || '';
    const pass   = $('#restorePass')?.value   || '';
    try {
      await restoreAccount(phrase, pass);
    } catch (e) {
      out('ERR: ' + (e && e.message ? e.message : e));
    }
  });
}

```

### FILE: /var/www/logos/landing/landing/wallet/index.html
```
<!doctype html><meta charset="utf-8">
<title>Redirecting…</title>
<meta http-equiv="refresh" content="0; url=./login.html">
<a href="./login.html">Перейти в LOGOS Wallet</a>

```

### FILE: /var/www/logos/landing/landing/wallet/login.html
```
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Wallet — Вход</title>
  <style>
    body{
      font-family:system-ui,Segoe UI,Roboto,Arial,sans-serif;
      margin:0;background:#0b0c10;color:#e6edf3
    }
    header{
      padding:16px 20px;background:#11151a;
      border-bottom:1px solid #1e242c
    }
    h1{font-size:18px;margin:0}
    main{
      max-width:820px;
      margin:32px auto;
      padding:0 16px 48px
    }
    section{
      background:#11151a;
      margin:16px 0;
      border-radius:12px;
      padding:16px;
      border:1px solid #1e242c
    }
    label{display:block;margin:8px 0 6px}
    input,button,textarea{
      width:100%;
      padding:10px;
      border-radius:10px;
      border:1px solid #2a313a;
      background:#0b0f14;
      color:#e6edf3;
      box-sizing:border-box;
      font-size:14px;
    }
    textarea{
      min-height:70px;
      resize:vertical;
    }
    button{
      cursor:pointer;
      border:1px solid #3b7ddd;
      background:#1665c1;
    }
    button.secondary{background:#1b2129}
    button:disabled{opacity:.6;cursor:not-allowed}
    small{opacity:.8}
    .grid{
      display:grid;
      grid-template-columns:1fr 1fr;
      gap:12px
    }
    @media (max-width:720px){
      .grid{grid-template-columns:1fr}
    }
    .mono{font-family:ui-monospace,Menlo,Consolas,monospace}
    ul{list-style:none;padding:0;margin:8px 0}
    li{
      padding:8px;
      border:1px solid #2a313a;
      border-radius:8px;
      margin-bottom:6px;
      cursor:pointer;
      background:#0b0f14
    }
    .muted{font-size:13px;opacity:.8}
    #mnemonicSection{margin-top:24px}
    #out{
      margin-top:12px;
      font-family:ui-monospace,Menlo,Consolas,monospace;
      font-size:13px;
      white-space:pre-wrap;
    }
  </style>
</head>
<body>
<header>
  <h1>LOGOS Wallet — Secure (WebCrypto + IndexedDB + 16 слов)</h1>
</header>
<main>
  <section>
    <h3>Вход в существующий кошелёк</h3>
    <label>RID</label>
    <input id="loginRid" class="mono" placeholder="RID (base58) или выбери ниже"/>
    <label>Пароль</label>
    <input id="loginPass" type="password" placeholder="Пароль, которым шифровали ключ"/>

    <div class="grid" style="margin-top:12px">
      <button id="btn-login">Войти по RID + пароль</button>
      <button id="btn-list"  class="secondary">Показать сохранённые RID</button>
    </div>

    <div id="listWrap" style="display:none;margin-top:10px">
      <div class="muted">Локально сохранённые RID (кликни, чтобы подставить):</div>
      <ul id="ridList"></ul>
    </div>
  </section>

  <section>
    <h3>Создать новый кошелёк</h3>
    <p class="muted">
      Ключ генерируется в браузере, приватник шифруется с помощью пароля (PBKDF2 + AES‑GCM).
      Пароль: минимум 10 символов, буквы + цифры.
      После создания будет показана резервная фраза из 16 слов — <b>обязательно запиши её</b>.
    </p>
    <label>Новый пароль</label>
    <input id="createPass" type="password" placeholder="Минимум 10 символов, буквы + цифры"/>
    <button id="btn-create" style="margin-top:12px">Создать новый RID + фразу</button>

    <section id="mnemonicSection" style="display:none">
      <h4>Резервная фраза (16 слов)</h4>
      <p class="muted">
        Запиши эту фразу на бумагу и храни в безопасном месте. Это <b>единственный</b> способ
        восстановить кошелёк на новом устройстве. Мы нигде её не храним.
      </p>
      <label>Фраза (только чтение)</label>
      <textarea id="mnemonicShow" class="mono" readonly></textarea>
      <label>Повтори фразу для проверки</label>
      <textarea id="mnemonicConfirm" class="mono" placeholder="Введите те же 16 слов ещё раз"></textarea>
      <button id="btn-mnemonic-ok" style="margin-top:10px">
        Я записал фразу, перейти в кошелёк
      </button>
    </section>
  </section>

  <section>
    <h3>Восстановить кошелёк по фразе</h3>
    <p class="muted">
      Если устройство потеряно/очищено, используй 16‑словную фразу и задай <b>новый</b> пароль.
      Пароль можно поменять — фраза остаётся корнем ключа.
    </p>
    <label>Резервная фраза (16 слов)</label>
    <textarea id="restoreMnemonic" class="mono" placeholder="введите 16 слов через пробел"></textarea>
    <label>Новый пароль</label>
    <input id="restorePass" type="password" placeholder="Минимум 10 символов, буквы + цифры"/>
    <button id="btn-restore" style="margin-top:12px">Восстановить кошелёк по фразе</button>
  </section>

  <section>
    <h3>Сервис</h3>
    <p class="muted">
      Сброс (удаление всех локальных аккаунтов) доступен только на <code>localhost</code> — для разработки.
      В продакшене кнопка спрятана.
    </p>
    <button id="btn-reset" class="secondary">Сбросить все аккаунты (DEV)</button>
  </section>

  <pre id="out">Статус: жду действий…</pre>
</main>
<script src="./auth.js?v=20251129_01" defer></script>
</body>
</html>

```

### FILE: /var/www/logos/landing/landing/wallet/wallet.css
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

### FILE: /var/www/logos/landing/modules/about.html
```
<section id="about" class="section">
  <h2 class="section__title" data-i18n="about_title">What is LOGOS?</h2>
  <p class="section__lead" data-i18n="about_text">
    LOGOS is a resonance-based L1 blockchain. Its core relies on Σ(t), inspired by ancient Indian temple geometry.
  </p>
  <div class="cards">
    <article class="card"><h3 data-i18n="card1_title">Resonant Core</h3><p data-i18n="card1_text">Σ(t), Λ and phase filters keep the network stable.</p></article>
    <article class="card"><h3 data-i18n="card2_title">Real Privacy</h3><p data-i18n="card2_text">Minimal metadata, strict nonce policy and phase mixing.</p></article>
    <article class="card"><h3 data-i18n="card3_title">Production‑grade</h3><p data-i18n="card3_text">Rust core, Axum REST, Prometheus/Grafana, bridge journal, health checks.</p></article>
  </div>
</section>

```

### FILE: /var/www/logos/landing/modules/community.html
```
<section id="community" class="section section--alt">
  <h2 class="section__title">Сообщество и airdrop</h2>
  <p class="section__lead">
    LOGOS живёт за счёт людей. Airdrop — это вход в ядро сообщества и первый шаг
    к Web4: приватным, резонансным и устойчивым системам.
  </p>

  <!-- Airdrop блок -->
  <div id="airdrop" class="airdrop">
    <h3 class="section__subtitle">🎁 Airdrop LOGOS: что нужно сделать</h3>
    <ol class="airdrop__list">
      <li>Подключить LOGOS‑кошелёк и привязать его к airdrop‑профилю.</li>
      <li>Подписаться на наш Telegram‑канал <strong>@logosblockchain</strong>.</li>
      <li>Подписаться на X (Twitter) <strong>@OfficiaLogosLRB</strong>.</li>
      <li>Поставить лайк и сделать ретвит закреплённого твита кампании.</li>
      <li>Получить личную реферальную ссылку и пригласить до 5 друзей.</li>
      <li>Следить за прогрессом и статусом заданий на странице airdrop или через Telegram‑бота.</li>
    </ol>

    <a
      href="/airdrop.html"
      class="btn btn--primary airdrop__btn"
    >
      Перейти к airdrop‑заданиям
    </a>
  </div>

  <!-- блок про каналы/контакты -->
  <div class="community__row">
    <h3 class="section__subtitle">Каналы и связи</h3>
    <p class="section__text">
      Здесь — обновления сети, объявления о стейкинге, эксперименты с LOGOS‑AGI и
      резонансной архитектурой.
    </p>

    <div class="pill-row">
      <a class="pill" href="https://t.me/logosblockchain" target="_blank" rel="noreferrer">
        Telegram
      </a>
      <a class="pill" href="https://x.com/RspLogos" target="_blank" rel="noreferrer">
        X (Twitter)
      </a>
      <a class="pill" href="#token">
        Токеномика LGN
      </a>
    </div>

    <p class="section__meta">
      Email:
      <a href="mailto:simbiotai@proton.me">simbiotai@proton.me</a>
    </p>
  </div>
</section>

```

### FILE: /var/www/logos/landing/modules/header.html
```
<header class="topbar">
  <!-- Локальный CSS только для хэдера / гамбургера -->
  <style>
    header.topbar{
      position:relative;
      z-index:30;
    }

    .topbar__right{
      position:relative;
      display:flex;
      align-items:center;
      gap:10px;
    }

    .topbar__lang button{
      border:none;
      background:transparent;
      color:#d0c8f0;
      font-size:11px;
      text-transform:uppercase;
      letter-spacing:.12em;
      padding:2px 4px;
      cursor:pointer;
    }

    .topbar__lang button.is-active{
      font-weight:600;
      border-bottom:1px solid rgba(255,255,255,.7);
    }

    .topbar__menu-toggle{
      display:none;
    }

    .topbar__burger{
      width:32px;
      height:32px;
      border-radius:999px;
      border:1px solid rgba(255,255,255,.24);
      background:rgba(6,4,18,.9);
      display:inline-flex;
      align-items:center;
      justify-content:center;
      flex-direction:column;
      gap:3px;
      cursor:pointer;
    }

    .topbar__burger span{
      width:14px;
      height:1.6px;
      border-radius:999px;
      background:#f5f0ff;
    }

    .topbar__menu{
      position:absolute;
      top:120%;
      right:0;
      min-width:220px;
      max-width:260px;
      background:rgba(6,4,18,.97);
      border-radius:16px;
      border:1px solid rgba(255,255,255,.14);
      box-shadow:0 18px 50px rgba(0,0,0,.8);
      padding:10px 10px 8px;
      opacity:0;
      transform:translateY(-6px);
      pointer-events:none;
      transition:opacity .18s ease, transform .18s ease;
    }

    .topbar__menu-list{
      list-style:none;
      margin:0;
      padding:0;
      display:flex;
      flex-direction:column;
      gap:2px;
      font-size:13px;
    }

    .topbar__menu-link{
      display:flex;
      align-items:center;
      justify-content:space-between;
      padding:7px 8px;
      border-radius:10px;
      color:#f5f0ff;
      text-decoration:none;
      gap:8px;
    }

    .topbar__menu-link span:last-child{
      font-size:11px;
      color:#b9afd4;
      white-space:nowrap;
    }

    .topbar__menu-link:hover{
      background:rgba(169,107,255,.22);
    }

    .topbar__menu-sep{
      border:none;
      border-top:1px solid rgba(255,255,255,.12);
      margin:6px 0;
    }

    /* Связка чекбокса и панели */
    .topbar__menu-toggle:checked + label.topbar__burger + .topbar__menu{
      opacity:1;
      transform:translateY(0);
      pointer-events:auto;
    }

    @media (max-width: 720px){
      .topbar__nav{
        display:none;
      }
    }
  </style>

  <div class="topbar__left">
    <div class="logo">LOGOS</div>
    <div class="logo-sub">Resonance Blockchain</div>
  </div>

  <nav class="topbar__nav">
    <a href="#about" class="nav-link" data-i18n="nav_about">About</a>
    <a href="#tech" class="nav-link" data-i18n="nav_tech">Technology</a>
    <a href="#token" class="nav-link" data-i18n="nav_token">Token</a>
    <a href="#community" class="nav-link" data-i18n="nav_comm">Community</a>
  </nav>

  <div class="topbar__right">
    <div class="topbar__lang">
      <button type="button" data-lang-btn="ru">RU</button>
      <button type="button" data-lang-btn="en">EN</button>
      <button type="button" data-lang-btn="de">DE</button>
    </div>

    <input type="checkbox" id="topbar-menu-toggle" class="topbar__menu-toggle" />
    <label for="topbar-menu-toggle" class="topbar__burger" aria-label="Menu">
      <span></span><span></span><span></span>
    </label>

    <div class="topbar__menu">
      <ul class="topbar__menu-list">
        <li>
          <a href="#about" class="topbar__menu-link">
            <span data-i18n="nav_about">About</span>
          </a>
        </li>
        <li>
          <a href="#tech" class="topbar__menu-link">
            <span data-i18n="nav_tech">Technology</span>
          </a>
        </li>
        <li>
          <a href="#token" class="topbar__menu-link">
            <span data-i18n="nav_token">Token</span>
          </a>
        </li>
        <li>
          <a href="#community" class="topbar__menu-link">
            <span data-i18n="nav_comm">Community</span>
          </a>
        </li>

        <li><hr class="topbar__menu-sep" /></li>

        <li>
          <a href="mailto:simbiotai@proton.me?subject=LOGOS%20Presale%20/Seed" class="topbar__menu-link">
            <span>Presale / Seed</span>
            <span>✉️ simbiotai@proton.me</span>
          </a>
        </li>

        <li>
          <a href="/airdrop.html" class="topbar__menu-link">
            <span>Airdrop</span>
            <span>🎁 tasks & progress</span>
          </a>
        </li>

        <li>
          <a href="https://mw-expedition.com/wallet" class="topbar__menu-link">
            <span>Web Wallet</span>
            <span>beta</span>
          </a>
        </li>
        <li>
          <a href="https://mw-expedition.com/explorer" class="topbar__menu-link">
            <span>Explorer</span>
            <span>chain view</span>
          </a>
        </li>
        <li>
          <a href="https://mw-expedition.com/staking" class="topbar__menu-link">
            <span>Staking</span>
            <span>LGN</span>
          </a>
        </li>

        <li><hr class="topbar__menu-sep" /></li>

        <li>
          <a href="https://t.me/logosblockchain" target="_blank" rel="noopener" class="topbar__menu-link">
            <span>Telegram</span>
            <span>@logosblockchain</span>
          </a>
        </li>
        <li>
          <a href="https://x.com/RspLogos" target="_blank" rel="noopener" class="topbar__menu-link">
            <span>X (Twitter)</span>
            <span>@OfficiaLogosLRB</span>
          </a>
        </li>
        <li>
          <a href="https://t.me/logosblockchain" target="_blank" rel="noopener" class="topbar__menu-link">
            <span>Airdrop bot</span>
            <span>@Logos_lrb_bot</span>
          </a>
        </li>
      </ul>
    </div>
  </div>
</header>

```

### FILE: /var/www/logos/landing/modules/hero.html
```
<section class="hero">
  <div class="hero__text">
    <div class="hero__badge" data-i18n="badge_main">L1 • 81M LGN • Anonymous • Deflationary • Quantum-resistant</div>
    <h1 class="hero__title">
      <span class="hero__lambda">Λ</span>
      <span data-i18n="hero_title">Living resonance blockchain for the next era.</span>
    </h1>
    <p class="hero__subtitle" data-i18n="hero_sub">
      LOGOS combines ancient resonance structures of Indian temples with a high‑load L1 architecture designed for millions of users.
    </p>
    <div class="hero__buttons">
      <a href="#about" class="btn btn--primary" data-i18n="btn_learn_more">Learn more</a>
      <a href="/apk/app-20250830_1442.apk" class="btn btn--ghost" data-i18n="btn_download_apk">Download secure APK</a>
    </div>
    <div class="hero__meta">
      <span data-i18n="meta_supply">Total supply: 81 000 000 LGN</span>
      <span data-i18n="meta_ready">Built for real utility & mass adoption</span>
    </div>
  </div>
</section>

```

### FILE: /var/www/logos/landing/modules/staking.html
```
<section id="staking" class="section">
  <h2 class="section__title" data-i18n="stake_title">Staking & RSP protocol</h2>
  <p class="section__lead" data-i18n="stake_text">
    Staking LGN ties network security and the RSP protocol to long‑term incentives for holders.
  </p>
  <div class="cards">
    <article class="card">
      <h3 data-i18n="stake_item1_title">Base staking</h3>
      <p data-i18n="stake_item1_text">
        Delegate LGN to validators and receive rewards for helping secure the network.
      </p>
    </article>
    <article class="card">
      <h3 data-i18n="stake_item2_title">RSP protocol</h3>
      <p data-i18n="stake_item2_text">
        A security layer that accounts for network phase and behaviour, making staking and the whole economy more robust.
      </p>
    </article>
    <article class="card">
      <h3 data-i18n="stake_item3_title">Missions & rewards</h3>
      <p data-i18n="stake_item3_text">
        On‑chain activity, community quests and airdrop mechanics on top of base staking.
      </p>
    </article>
  </div>
</section>

```

### FILE: /var/www/logos/landing/modules/tech.html
```
<section id="tech" class="section section--alt">
  <h2 class="section__title" data-i18n="tech_title">Technology</h2>
  <div class="tech-grid">
    <div class="tech-col">
      <ul class="tech-list">
        <li data-i18n="tech_item1">L1 ledger on sled with atomic commits.</li>
        <li data-i18n="tech_item2">Resonance Consensus Protocol (RCP) with phase awareness.</li>
        <li data-i18n="tech_item3">Anti‑spam & dynamic balance against overload.</li>
        <li data-i18n="tech_item4">Encrypted bridge, durable journal & HMAC endpoints.</li>
        <li data-i18n="tech_item5">Web wallet, explorer & API for integrations.</li>
      </ul>
    </div>
    <div class="tech-col tech-col--note">
      <p data-i18n="tech_note">Private, resonance‑driven and robust systems — without sacrificing speed or UX.</p>
    </div>
  </div>
</section>

```

### FILE: /var/www/logos/landing/modules/token.html
```
<section id="token" class="section">
  <h2 class="section__title" data-i18n="token_title">LGN Tokenomics</h2>
  <p class="section__lead" data-i18n="token_text">LGN is the base token of LOGOS. Total 81 000 000 LGN. Deflationary.</p>
  <div class="token-grid">
    <div class="token-grid__item"><span class="token-grid__label" data-i18n="token_staking">Staking & Holders</span><span class="token-grid__value">25%</span></div>
    <div class="token-grid__item"><span class="token-grid__label" data-i18n="token_rcp">RSP security protocol</span><span class="token-grid__value">20%</span></div>
    <div class="token-grid__item"><span class="token-grid__label" data-i18n="token_liq">Liquidity (DEX/CEX)</span><span class="token-grid__value">15%</span></div>
    <div class="token-grid__item"><span class="token-grid__label" data-i18n="token_stab">Stability Fund</span><span class="token-grid__value">15%</span></div>
    <div class="token-grid__item"><span class="token-grid__label" data-i18n="token_core">Founder & Core Dev</span><span class="token-grid__value">20%</span></div>
    <div class="token-grid__item"><span class="token-grid__label" data-i18n="token_airdrop">Airdrop & DAO</span><span class="token-grid__value">5%</span></div>
  </div>
</section>

```

### FILE: /var/www/logos/landing/shared/airdrop-fix.js
```
(() => {
  'use strict';
  const API='/airdrop-api/api/airdrop';
  const K_T='logos_airdrop_token_v1', K_X='logos_airdrop_xu_v1';

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

### FILE: /var/www/logos/landing/styles.v20251124.css
```
:root{
  --bg:#05030b;
  --fg:#f5f0ff;
  --muted:#b9afd4;
  --accent:#e36bff;
  --border-soft:rgba(255,255,255,0.12);
  --card-bg:rgba(13,7,34,0.96);
  --shadow-soft:0 22px 60px rgba(0,0,0,0.75);
}

*{box-sizing:border-box;margin:0;padding:0}
html,body{
  min-height:100%;
  background:var(--bg);
  color:var(--fg);
  font-family:system-ui,-apple-system,"Inter",sans-serif;
  -webkit-font-smoothing:antialiased;
}
a{text-decoration:none;color:inherit}
img{max-width:100%;display:block}

/* Базовый градиент */

body{
  background:
    radial-gradient(1600px 900px at 10% 0%, rgba(130,90,240,.22), transparent 60%),
    radial-gradient(1500px 900px at 90% 100%, rgba(40,26,110,.30), transparent 65%),
    #05030b;
}

/* Резонансный слой */

.bg-layer{
  position:fixed;
  inset:0;
  z-index:-1;
  pointer-events:none;
  background:
    radial-gradient(circle at 15% 12%, rgba(210,160,255,0.26) 0, transparent 55%),
    radial-gradient(circle at 82% 78%, rgba(150,110,255,0.28) 0, transparent 60%),
    radial-gradient(circle at 48% 40%, rgba(255,255,255,0.08) 0, transparent 55%),
    repeating-radial-gradient(circle at 18% 18%,
      rgba(220,180,255,0.20) 0px,
      rgba(220,180,255,0.20) 1px,
      transparent 1px,
      transparent 18px),
    repeating-radial-gradient(circle at 80% 72%,
      rgba(190,150,255,0.18) 0px,
      rgba(190,150,255,0.18) 1px,
      transparent 1px,
      transparent 24px);
  mix-blend-mode:screen;
  opacity:.9;
}

/* Лейаут */

.page-wrap{
  max-width:960px;
  margin:0 auto;
  padding:20px 16px 40px;
}
@media (min-width:960px){
  .page-wrap{padding:26px 0 56px;}
}

/* Шапка */

.topbar{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:12px;
  margin-bottom:20px;
}
.brand{
  display:flex;
  flex-direction:column;
  gap:2px;
}
.brand__logo{
  font-size:14px;
  font-weight:700;
  letter-spacing:0.14em;
  text-transform:uppercase;
}
.brand__sub{
  font-size:10px;
  text-transform:uppercase;
  letter-spacing:0.18em;
  color:var(--muted);
}

/* Бургер */

.menu-toggle{
  width:34px;
  height:26px;
  border:none;
  background:transparent;
  cursor:pointer;
  display:flex;
  flex-direction:column;
  justify-content:space-between;
  padding:3px 2px;
}
.menu-toggle span{
  display:block;
  height:2px;
  border-radius:999px;
  background:#fdfbff;
  transition:transform .2s ease-out,opacity .2s ease-out;
}
body.menu-open .menu-toggle span:nth-child(1){
  transform:translateY(8px) rotate(45deg);
}
body.menu-open .menu-toggle span:nth-child(2){
  opacity:0;
}
body.menu-open .menu-toggle span:nth-child(3){
  transform:translateY(-8px) rotate(-45deg);
}

/* Меню-оверлей */

.menu[hidden]{display:none;}
.menu{
  position:fixed;
  inset:0;
  z-index:20;
  background:rgba(5,3,18,0.97);
  backdrop-filter:blur(18px);
}
.menu__inner{
  max-width:960px;
  margin:70px auto 24px;
  padding:0 16px 24px;
  display:grid;
  gap:18px;
}
.menu__section{
  border-radius:16px;
  border:1px solid rgba(255,255,255,0.10);
  background:rgba(12,7,32,0.98);
  padding:12px 14px;
}
.menu__label{
  font-size:11px;
  text-transform:uppercase;
  letter-spacing:0.18em;
  color:var(--muted);
  margin-bottom:8px;
}
.menu__langs{
  display:flex;
  gap:8px;
}
.menu__langs button{
  border-radius:999px;
  border:1px solid rgba(255,255,255,0.16);
  padding:6px 12px;
  font-size:11px;
  background:rgba(7,4,22,0.96);
  color:var(--muted);
  cursor:pointer;
}
.menu__langs button.is-active{
  background:var(--accent);
  border-color:var(--accent);
  color:#1b041c;
}
.menu__section a{
  display:inline-flex;
  margin:2px 4px 4px 0;
  padding:6px 12px;
  border-radius:999px;
  border:1px solid rgba(255,255,255,0.14);
  background:rgba(9,5,26,0.96);
  font-size:13px;
}
.menu__section a:hover{
  border-color:var(--accent);
}

/* Контент */

.page{
  display:flex;
  flex-direction:column;
  gap:18px;
}
.block{
  border-radius:20px;
  background:var(--card-bg);
  border:1px solid var(--border-soft);
  box-shadow:var(--shadow-soft);
  padding:20px 18px 22px;
}
.block__title{
  font-size:20px;
  margin-bottom:10px;
}
.block__text{
  font-size:14px;
  line-height:1.6;
  color:var(--fg);
  margin-bottom:8px;
}
.block__list{
  margin:4px 0 4px 20px;
}
.block__list li{
  font-size:14px;
  line-height:1.5;
  color:var(--muted);
  margin-bottom:4px;
}

@media (min-width:960px){
  .block{
    padding:24px 24px 26px;
  }
  .block__title{
    font-size:22px;
  }
  .block__text,.block__list li{
    font-size:15px;
  }
}

/* Футер */

.footer{
  margin-top:20px;
  font-size:11px;
  color:var(--muted);
}

```

### FILE: /var/www/logos/landing/wallet3/app.v3.js
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

### FILE: /var/www/logos/landing/wallet3/index.html
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

### FILE: /var/www/logos/landing/wallet/app.html
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

### FILE: /var/www/logos/landing/wallet/app.js
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

### FILE: /var/www/logos/landing/wallet/app.v2.js
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

### FILE: /var/www/logos/landing/wallet/app.v3.js
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

### FILE: /var/www/logos/landing/wallet/auth.js
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

### FILE: /var/www/logos/landing/wallet/css/styles.css
```
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

### FILE: /var/www/logos/landing/wallet/index.html
```
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

### FILE: /var/www/logos/landing/wallet.js
```
/* === (весь файл как в последнем «фарше») … НИЖЕ ПОКАЗЫВАЮ ТОЛЬКО ИЗМЕНЁННЫЕ ЧАСТИ === */

// … верх файла без изменений (utils/IDB конфиг/константы и т.п.)

async function vaultCreateWithPass(pass){
  try{
    // генерим пару и шифруем pkcs8
    const kp   = await crypto.subtle.generateKey({name:"Ed25519"},true,["sign","verify"]);
    const pkcs8= new Uint8Array(await crypto.subtle.exportKey("pkcs8",kp.privateKey));
    const pubRaw=new Uint8Array(await crypto.subtle.exportKey("raw",kp.publicKey));
    const salt = rand(SALT_LEN), iv = rand(IV_LEN);
    const key  = await kdf(pass,salt);
    const ct   = new Uint8Array(await crypto.subtle.encrypt({name:"AES-GCM",iv},key,pkcs8));

    // 1) СНАЧАЛА — резерв в localStorage (всегда)
    localStorage.setItem(LS, JSON.stringify({
      salt: btoa(String.fromCharCode(...salt)),
      iv:   btoa(String.fromCharCode(...iv)),
      ct:   btoa(String.fromCharCode(...ct)),
      pubRaw: btoa(String.fromCharCode(...pubRaw)),
      iter: PBKDF2_ITER
    }));

    // 2) Потом — IndexedDB (если доступна)
    try {
      const db = await idbOpenV3();
      await idbPut(db,{id:REC_ID, salt, iv, ct, pubRaw, iter:PBKDF2_ITER});
    } catch (e) {
      // не критично: работаем на резерве, просто сообщим
      console.warn("IDB write failed (fallback to LS only):", e);
      toast("IDB недоступна — ключ сохранён локально (LS)");
    }

    unlockedPriv = kp.privateKey;
    unlockedPubRaw = pubRaw;
    scheduleAutolock();
    return true;
  } catch (e) {
    console.error("vaultCreateWithPass error:", e);
    toast("Ошибка создания: " + (e?.message || e));
    return false;
  }
}

async function vaultImportPkcs8Base64(b64, pass){
  try{
    const pkcs8 = Uint8Array.from(atob(b64), c=>c.charCodeAt(0));
    // создадим временную пару только ради pubRaw
    const tmp   = await crypto.subtle.generateKey({name:"Ed25519"},true,["sign","verify"]);
    const pubRaw= new Uint8Array(await crypto.subtle.exportKey("raw",tmp.publicKey));
    const salt  = rand(SALT_LEN), iv=rand(IV_LEN);
    const key   = await kdf(pass,salt);
    const ct    = new Uint8Array(await crypto.subtle.encrypt({name:"AES-GCM",iv},key,pkcs8));

    // 1) резерв LS (всегда)
    localStorage.setItem(LS, JSON.stringify({
      salt: btoa(String.fromCharCode(...salt)),
      iv:   btoa(String.fromCharCode(...iv)),
      ct:   btoa(String.fromCharCode(...ct)),
      pubRaw: btoa(String.fromCharCode(...pubRaw)),
      iter: PBKDF2_ITER
    }));

    // 2) IndexedDB — в try/catch
    try {
      const db = await idbOpenV3();
      await idbPut(db,{id:REC_ID, salt, iv, ct, pubRaw, iter:PBKDF2_ITER});
    } catch (e) {
      console.warn("IDB write failed (fallback to LS only):", e);
      toast("IDB недоступна — ключ импортирован в LS");
    }

    unlockedPriv = await crypto.subtle.importKey("pkcs8", pkcs8, {name:"Ed25519"}, false, ["sign"]);
    unlockedPubRaw = pubRaw;
    scheduleAutolock();
    return true;
  } catch (e) {
    console.error("vaultImportPkcs8Base64 error:", e);
    toast("Ошибка импорта: " + (e?.message || e));
    return false;
  }
}

/* ======= overlay handlers ======= */
let tries=5;
async function handleCreate(){
  const a=$("#pwNew").value.trim(), b=$("#pwNew2").value.trim();
  if(a.length<8 || a!==b){ toast("Пароль ≥ 8 символов и должен совпадать"); return; }
  toast("Создаём и шифруем ключ…");
  const ok = await vaultCreateWithPass(a);
  if(!ok) return;          // уже показали причину в toast
  $("#lockOverlay").classList.add("hidden");
  tries=5;
  await afterUnlock();
}

async function handleUnlock(){
  const p=$("#pwUnlock").value.trim();
  try{
    const ok = await vaultUnlock(p);
    if(!ok) throw new Error("Bad password");
    $("#lockOverlay").classList.add("hidden");
    tries=5;
    await afterUnlock();
  }catch(e){
    tries--; $("#triesLeft2").textContent=String(tries);
    toast(tries>0 ? "Неверный пароль" : "Слишком много попыток — кошелёк сброшен");
    if(tries<=0){ await vaultReset(); location.reload(); }
  }
}

/* ======= остальной файл — БЕЗ ИЗМЕНЕНИЙ =======
   - vaultStatus/vaultUnlock/vaultLock/scheduleAutolock
   - export/import/reset кнопки
   - API вызовы / паспорт / история / стейкинг / отправка / биндинги
*/

```

### FILE: /var/www/logos/landing/wallet/js/api.js
```
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

### FILE: /var/www/logos/landing/wallet/js/app.js
```
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

### FILE: /var/www/logos/landing/wallet/js/app_wallet.js
```
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

### FILE: /var/www/logos/landing/wallet/js/core.js
```
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

### FILE: /var/www/logos/landing/wallet/js/unlock.js
```
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

### FILE: /var/www/logos/landing/wallet/js/vault_bridge.js
```
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

### FILE: /var/www/logos/landing/wallet/js/vault.js
```
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

### FILE: /var/www/logos/landing/wallet/login.html
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

### FILE: /var/www/logos/landing/wallet/ping.html
```
<!doctype html><meta charset="utf-8">
<title>Wallet JS Ping</title>
<button onclick="alert('JS OK')">JS TEST</button>

```

### FILE: /var/www/logos/landing/wallet/staking.js
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

### FILE: /var/www/logos/landing/wallet/wallet.css
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

### FILE: /var/www/logos/landing/wallet/wallet.js
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

### FILE: /var/www/logos/landing/www/explorer/explorer.css
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

### FILE: /var/www/logos/landing/www/explorer/explorer.js
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

### FILE: /var/www/logos/landing/www/explorer/index.html
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

### FILE: /var/www/logos/landing/www/index.html
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

### FILE: /var/www/logos/landing/www/styles.css
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

### FILE: /var/www/logos/landing/www/wallet3/app.v3.js
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

### FILE: /var/www/logos/landing/www/wallet3/index.html
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

### FILE: /var/www/logos/landing/www/wallet/app.html
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

### FILE: /var/www/logos/landing/www/wallet/app.js
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

### FILE: /var/www/logos/landing/www/wallet/app.v2.js
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

### FILE: /var/www/logos/landing/www/wallet/app.v3.js
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

### FILE: /var/www/logos/landing/www/wallet/auth.js
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

### FILE: /var/www/logos/landing/www/wallet-autosign.js
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

### FILE: /var/www/logos/landing/www/wallet/index.html
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

### FILE: /var/www/logos/landing/www/wallet.js
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

### FILE: /var/www/logos/landing/www/wallet/login.html
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

### FILE: /var/www/logos/landing/www/wallet/staking.js
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

### FILE: /var/www/logos/landing/www/wallet-sync.js
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

### FILE: /var/www/logos/landing/www/wallet-ui.js
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

### FILE: /var/www/logos/landing/www/wallet/wallet.css
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

### FILE: /var/www/logos/landing/www/wallet/wallet.js
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

### FILE: /var/www/logos/wallet/app.html
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

### FILE: /var/www/logos/wallet/app.js
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

### FILE: /var/www/logos/wallet/app.v2.js
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

### FILE: /var/www/logos/wallet/app.v3.js
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

### FILE: /var/www/logos/wallet/auth.js
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

### FILE: /var/www/logos/wallet/css/styles.css
```
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

### FILE: /var/www/logos/wallet/index.html
```
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

### FILE: /var/www/logos/wallet.js
```
/* === (весь файл как в последнем «фарше») … НИЖЕ ПОКАЗЫВАЮ ТОЛЬКО ИЗМЕНЁННЫЕ ЧАСТИ === */

// … верх файла без изменений (utils/IDB конфиг/константы и т.п.)

async function vaultCreateWithPass(pass){
  try{
    // генерим пару и шифруем pkcs8
    const kp   = await crypto.subtle.generateKey({name:"Ed25519"},true,["sign","verify"]);
    const pkcs8= new Uint8Array(await crypto.subtle.exportKey("pkcs8",kp.privateKey));
    const pubRaw=new Uint8Array(await crypto.subtle.exportKey("raw",kp.publicKey));
    const salt = rand(SALT_LEN), iv = rand(IV_LEN);
    const key  = await kdf(pass,salt);
    const ct   = new Uint8Array(await crypto.subtle.encrypt({name:"AES-GCM",iv},key,pkcs8));

    // 1) СНАЧАЛА — резерв в localStorage (всегда)
    localStorage.setItem(LS, JSON.stringify({
      salt: btoa(String.fromCharCode(...salt)),
      iv:   btoa(String.fromCharCode(...iv)),
      ct:   btoa(String.fromCharCode(...ct)),
      pubRaw: btoa(String.fromCharCode(...pubRaw)),
      iter: PBKDF2_ITER
    }));

    // 2) Потом — IndexedDB (если доступна)
    try {
      const db = await idbOpenV3();
      await idbPut(db,{id:REC_ID, salt, iv, ct, pubRaw, iter:PBKDF2_ITER});
    } catch (e) {
      // не критично: работаем на резерве, просто сообщим
      console.warn("IDB write failed (fallback to LS only):", e);
      toast("IDB недоступна — ключ сохранён локально (LS)");
    }

    unlockedPriv = kp.privateKey;
    unlockedPubRaw = pubRaw;
    scheduleAutolock();
    return true;
  } catch (e) {
    console.error("vaultCreateWithPass error:", e);
    toast("Ошибка создания: " + (e?.message || e));
    return false;
  }
}

async function vaultImportPkcs8Base64(b64, pass){
  try{
    const pkcs8 = Uint8Array.from(atob(b64), c=>c.charCodeAt(0));
    // создадим временную пару только ради pubRaw
    const tmp   = await crypto.subtle.generateKey({name:"Ed25519"},true,["sign","verify"]);
    const pubRaw= new Uint8Array(await crypto.subtle.exportKey("raw",tmp.publicKey));
    const salt  = rand(SALT_LEN), iv=rand(IV_LEN);
    const key   = await kdf(pass,salt);
    const ct    = new Uint8Array(await crypto.subtle.encrypt({name:"AES-GCM",iv},key,pkcs8));

    // 1) резерв LS (всегда)
    localStorage.setItem(LS, JSON.stringify({
      salt: btoa(String.fromCharCode(...salt)),
      iv:   btoa(String.fromCharCode(...iv)),
      ct:   btoa(String.fromCharCode(...ct)),
      pubRaw: btoa(String.fromCharCode(...pubRaw)),
      iter: PBKDF2_ITER
    }));

    // 2) IndexedDB — в try/catch
    try {
      const db = await idbOpenV3();
      await idbPut(db,{id:REC_ID, salt, iv, ct, pubRaw, iter:PBKDF2_ITER});
    } catch (e) {
      console.warn("IDB write failed (fallback to LS only):", e);
      toast("IDB недоступна — ключ импортирован в LS");
    }

    unlockedPriv = await crypto.subtle.importKey("pkcs8", pkcs8, {name:"Ed25519"}, false, ["sign"]);
    unlockedPubRaw = pubRaw;
    scheduleAutolock();
    return true;
  } catch (e) {
    console.error("vaultImportPkcs8Base64 error:", e);
    toast("Ошибка импорта: " + (e?.message || e));
    return false;
  }
}

/* ======= overlay handlers ======= */
let tries=5;
async function handleCreate(){
  const a=$("#pwNew").value.trim(), b=$("#pwNew2").value.trim();
  if(a.length<8 || a!==b){ toast("Пароль ≥ 8 символов и должен совпадать"); return; }
  toast("Создаём и шифруем ключ…");
  const ok = await vaultCreateWithPass(a);
  if(!ok) return;          // уже показали причину в toast
  $("#lockOverlay").classList.add("hidden");
  tries=5;
  await afterUnlock();
}

async function handleUnlock(){
  const p=$("#pwUnlock").value.trim();
  try{
    const ok = await vaultUnlock(p);
    if(!ok) throw new Error("Bad password");
    $("#lockOverlay").classList.add("hidden");
    tries=5;
    await afterUnlock();
  }catch(e){
    tries--; $("#triesLeft2").textContent=String(tries);
    toast(tries>0 ? "Неверный пароль" : "Слишком много попыток — кошелёк сброшен");
    if(tries<=0){ await vaultReset(); location.reload(); }
  }
}

/* ======= остальной файл — БЕЗ ИЗМЕНЕНИЙ =======
   - vaultStatus/vaultUnlock/vaultLock/scheduleAutolock
   - export/import/reset кнопки
   - API вызовы / паспорт / история / стейкинг / отправка / биндинги
*/

```

### FILE: /var/www/logos/wallet/js/api.js
```
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

### FILE: /var/www/logos/wallet/js/app.js
```
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

### FILE: /var/www/logos/wallet/js/app_wallet.js
```
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

### FILE: /var/www/logos/wallet/js/core.js
```
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

### FILE: /var/www/logos/wallet/js/unlock.js
```
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

### FILE: /var/www/logos/wallet/js/vault_bridge.js
```
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

### FILE: /var/www/logos/wallet/js/vault.js
```
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

### FILE: /var/www/logos/wallet/login.html
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

### FILE: /var/www/logos/wallet/ping.html
```
<!doctype html><meta charset="utf-8">
<title>Wallet JS Ping</title>
<button onclick="alert('JS OK')">JS TEST</button>

```

### FILE: /var/www/logos/wallet/staking.js
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

### FILE: /var/www/logos/wallet/wallet.css
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

### FILE: /var/www/logos/wallet/wallet.js
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
