"use strict";

loadTheme();

const NODE_API   = (window.LOGOS_NODE_API || (location.origin + "/node-api")).replace(/\/+$/,"");
const WALLET_API = (window.LOGOS_WALLET_API || (location.origin + "/wallet-api")).replace(/\/+$/,"");

$("#nodeApi").textContent = NODE_API;
$("#walletApi").textContent = WALLET_API;

function toast(el, msg, cls=""){ el.className = "toast " + cls; el.textContent = msg; }

$("#themeBtn").onclick = () => {
  const cur = document.documentElement.dataset.theme || "dark";
  setTheme(cur === "dark" ? "light" : "dark");
  $("#themeBtn").textContent = "Theme: " + (document.documentElement.dataset.theme);
};
$("#themeBtn").textContent = "Theme: " + (document.documentElement.dataset.theme || "dark");

$("#logoutBtn").onclick = () => {
  localStorage.removeItem("logos_unlocked");
  window.location.href="./auth.html";
};

async function walletMeta(){
  const meta = await kvGet("meta");
  if (!meta || !meta.rid) throw new Error("Кошелёк не найден. Вернись и создай/восстанови.");
  return meta;
}

async function requireUnlocked(){
  if (localStorage.getItem("logos_unlocked") !== "1"){
    throw new Error("Кошелёк заблокирован. Вернись на вход.");
  }
}

async function getBalance(rid){
  // ожидаем: {rid,balance,nonce} (если nonce нет — покажем 0)
  const j = await fetchJSON(`${NODE_API}/balance/${encodeURIComponent(rid)}`);
  return {balance: j.balance ?? null, nonce: j.nonce ?? 0};
}

async function getHead(){
  const j = await fetchJSON(`${NODE_API}/head`);
  return j;
}

async function signTx(privKey, from, to, amountStr, nonce){
  // canonical: from|to|amount|nonce -> sha256 -> ed25519 sign
  const msg = await sha256Bytes(utf8(`${from}|${to}|${amountStr}|${nonce}`));
  const sig = await crypto.subtle.sign({name:"Ed25519"}, privKey, msg);
  return bufToHex(sig);
}

async function unlockWithPassword(){
  const pw = prompt("Пароль для подписи:");
  if (!pw) throw new Error("Отменено.");
  const enc  = await kvGet("enc");
  const meta = await kvGet("meta");
  const pkcs8 = await decryptBlob(pw, enc);
  const priv = await crypto.subtle.importKey("pkcs8", pkcs8, {name:"Ed25519"}, true, ["sign"]);
  return {rid: meta.rid, priv};
}

async function refreshAll(){
  const el = $("#toast");
  try{
    await requireUnlocked();
    const meta = await walletMeta();

    $("#ridPill").textContent = "RID: " + meta.rid;
    $("#ridPill").onclick = async()=>{ await navigator.clipboard.writeText(meta.rid); toast(el, "RID скопирован.", "ok"); };

    const head = await getHead();
    $("#head").textContent = JSON.stringify(head);

    const b = await getBalance(meta.rid);
    $("#bal").textContent = String(b.balance);
    $("#nonce").textContent = String(b.nonce);
    $("#nonceIn").value = String((b.nonce|0) + 1);

    toast(el, "Обновлено.", "ok");
  }catch(e){
    toast(el, String(e.message||e), "bad");
  }
}

function setTab(name){
  for (const b of document.querySelectorAll(".navbtn")){
    b.classList.toggle("active", b.dataset.tab === name);
  }
  for (const id of ["assets","send","history","staking","settings"]){
    const el = $(`#tab-${id}`);
    el.classList.toggle("hidden", id !== name);
  }
}

for (const b of document.querySelectorAll(".navbtn")){
  b.onclick = ()=> setTab(b.dataset.tab);
}

$("#btnRefresh").onclick = refreshAll;
$("#btnCopyRID").onclick = async()=>{
  const meta = await walletMeta();
  await navigator.clipboard.writeText(meta.rid);
  toast($("#toast"), "RID скопирован.", "ok");
};

$("#btnSend").onclick = async()=>{
  const el = $("#toastSend");
  try{
    await requireUnlocked();
    const meta = await walletMeta();
    const to = ($("#toRid").value||"").trim();
    const amountStr = ($("#amount").value||"").trim();
    const nonce = parseInt(($("#nonceIn").value||"").trim(),10);

    if (!to) throw new Error("Укажи RID получателя.");
    if (!amountStr) throw new Error("Укажи сумму.");
    if (!Number.isFinite(nonce) || nonce <= 0) throw new Error("Некорректный nonce.");

    toast(el, "Подписываю…");
    const {priv} = await unlockWithPassword();
    const sig_hex = await signTx(priv, meta.rid, to, amountStr, nonce);

    const payload = {from: meta.rid, to, amount: amountStr, nonce, memo:"", sig_hex};
    const j = await fetchJSON(`${NODE_API}/submit_tx`, {
      method:"POST",
      headers: {"content-type":"application/json"},
      body: JSON.stringify(payload)
    });
    toast(el, "OK: " + JSON.stringify(j), "ok");
    await refreshAll();
  }catch(e){
    toast(el, String(e.message||e), "bad");
  }
};

$("#btnHist").onclick = async()=>{
  const box = $("#histBox");
  const el = $("#toast");
  try{
    await requireUnlocked();
    const meta = await walletMeta();
    // если у тебя другой путь истории — скажешь, подгоним
    const j = await fetchJSON(`${NODE_API}/history/${encodeURIComponent(meta.rid)}`);
    box.textContent = JSON.stringify(j, null, 2);
  }catch(e){
    toast(el, String(e.message||e), "bad");
  }
};

$("#btnStakeMy").onclick = async()=>{
  const box = $("#stakeBox");
  const el = $("#toast");
  try{
    await requireUnlocked();
    const meta = await walletMeta();
    const j = await fetchJSON(`${NODE_API}/stake/my/${encodeURIComponent(meta.rid)}`);
    box.textContent = JSON.stringify(j, null, 2);
  }catch(e){
    toast(el, String(e.message||e), "bad");
  }
};

$("#btnExport").onclick = async()=>{
  const el = $("#toastSet");
  try{
    const meta = await walletMeta();
    const enc  = await kvGet("enc");
    const pack = {meta, enc};
    const b64 = bufToB64(utf8(JSON.stringify(pack)).buffer);
    toast(el, "Backup Code:\n" + b64, "warn");
  }catch(e){
    toast(el, String(e.message||e), "bad");
  }
};

$("#btnLock").onclick = async()=>{
  localStorage.removeItem("logos_unlocked");
  toast($("#toastSet"), "Заблокировано. Вернись на вход.", "ok");
};

(async ()=>{
  try{
    const meta = await walletMeta();
    $("#ridPill").textContent = "RID: " + meta.rid;
    await refreshAll();
  }catch(e){
    toast($("#toast"), String(e.message||e), "bad");
    setTimeout(()=>window.location.href="./auth.html", 600);
  }
})();
