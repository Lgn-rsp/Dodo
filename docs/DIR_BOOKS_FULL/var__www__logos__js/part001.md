# LOGOS — Directory Book: /var/www/logos/js

_Generated: 2025-12-31T06:43:51Z_

**Part:** 1

---

## STRUCTURE

```text
/var/www/logos/js
```

---

## FILES (FULL SOURCE)


### FILE: /var/www/logos/js/api.js

```
export const API_BASE="/api";
export async function apiGet(p){ const r=await fetch(`${API_BASE}${p}`); if(!r.ok) throw new Error(`GET ${p} -> ${r.status}`); return r.json(); }
export async function apiPost(p,b){ const r=await fetch(`${API_BASE}${p}`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)}); if(!r.ok){ const t=await r.text().catch(()=> ""); throw new Error(`POST ${p} -> ${r.status} ${t}`); } return r.json(); }

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
