"use strict";

loadTheme();

$("#themeBtn").onclick = () => {
  const cur = document.documentElement.dataset.theme || "dark";
  setTheme(cur === "dark" ? "light" : "dark");
  $("#themeBtn").textContent = "Theme: " + (document.documentElement.dataset.theme);
};
$("#themeBtn").textContent = "Theme: " + (document.documentElement.dataset.theme || "dark");

function toast(el, msg, cls=""){
  el.className = "toast " + cls;
  el.textContent = msg;
}

async function walletExists(){
  const meta = await kvGet("meta");
  const enc  = await kvGet("enc");
  return !!(meta && enc);
}

async function computeRID(pubKeyRawBuf){
  const rid = base58encode(new Uint8Array(pubKeyRawBuf));
  return rid;
}

async function createWallet(password){
  // generate Ed25519
  const kp = await crypto.subtle.generateKey({name:"Ed25519"}, true, ["sign","verify"]);
  const pkcs8 = await crypto.subtle.exportKey("pkcs8", kp.privateKey);
  const pubraw = await crypto.subtle.exportKey("raw", kp.publicKey);
  const rid = await computeRID(pubraw);

  const enc = await encryptBlob(password, pkcs8);
  const meta = {
    v:1,
    rid,
    created_at: new Date().toISOString(),
    pub_b58: rid,
  };

  await kvSet("meta", meta);
  await kvSet("enc", enc);
  return {rid};
}

async function unlockWallet(password){
  const meta = await kvGet("meta");
  const enc  = await kvGet("enc");
  if (!meta || !enc) throw new Error("Кошелёк не найден на устройстве. Нажми «Создать» или «Restore».");

  const pkcs8 = await decryptBlob(password, enc);
  const priv = await crypto.subtle.importKey("pkcs8", pkcs8, {name:"Ed25519"}, true, ["sign"]);
  return {rid: meta.rid, priv};
}

async function exportBackup(){
  const meta = await kvGet("meta");
  const enc  = await kvGet("enc");
  if (!meta || !enc) throw new Error("Сначала создай кошелёк.");
  // backup = meta + enc (без пароля). Пароль всё равно нужен чтобы расшифровать.
  const pack = {meta, enc};
  const json = JSON.stringify(pack);
  const b64  = bufToB64(utf8(json).buffer);
  return b64;
}

async function importBackup(b64){
  const json = new TextDecoder().decode(b64ToBuf(b64));
  const pack = JSON.parse(json);
  if (!pack || !pack.meta || !pack.enc || !pack.meta.rid) throw new Error("Неверный Backup Code.");
  await kvSet("meta", pack.meta);
  await kvSet("enc", pack.enc);
  return true;
}

$("#btnCreate").onclick = async () => {
  const pw = ($("#pwNew").value || "").trim();
  const el = $("#toastNew");
  try{
    if (pw.length < 12) throw new Error("Пароль должен быть минимум 12 символов.");
    if (await walletExists()) throw new Error("Кошелёк уже существует. Если нужно заново — нажми «Сброс».");
    toast(el, "Создаю ключи…");
    const {rid} = await createWallet(pw);
    toast(el, "Готово. RID: " + rid, "ok");
    setTimeout(()=>{ window.location.href = "./app.html"; }, 450);
  }catch(e){
    toast(el, String(e.message||e), "bad");
  }
};

$("#btnUnlock").onclick = async () => {
  const pw = ($("#pw").value || "").trim();
  const el = $("#toast");
  try{
    if (!pw) throw new Error("Введи пароль.");
    toast(el, "Проверяю пароль…");
    await unlockWallet(pw);
    toast(el, "Открыто.", "ok");
    localStorage.setItem("logos_unlocked", "1");
    setTimeout(()=>{ window.location.href = "./app.html"; }, 250);
  }catch(e){
    toast(el, String(e.message||e), "bad");
  }
};

$("#btnExport").onclick = async () => {
  const el = $("#toast");
  try{
    const b64 = await exportBackup();
    toast(el, "Backup Code (сохрани!):\n" + b64, "warn");
  }catch(e){
    toast(el, String(e.message||e), "bad");
  }
};

$("#btnImport").onclick = async () => {
  const el = $("#toast");
  try{
    const b64 = prompt("Вставь Backup Code (base64):");
    if (!b64) return;
    await importBackup(b64.trim());
    toast(el, "Backup восстановлен. Теперь введи пароль и открой.", "ok");
  }catch(e){
    toast(el, String(e.message||e), "bad");
  }
};

$("#btnWipe").onclick = async () => {
  const el = $("#toastNew");
  try{
    if (!confirm("Удалить локальные данные кошелька на этом устройстве?")) return;
    await kvDel("meta"); await kvDel("enc");
    localStorage.removeItem("logos_unlocked");
    toast(el, "Локальные данные удалены.", "ok");
  }catch(e){
    toast(el, String(e.message||e), "bad");
  }
};

// Auto redirect если уже есть кошелёк и он открыт
(async ()=>{
  try{
    if (await walletExists() && localStorage.getItem("logos_unlocked")==="1"){
      window.location.href="./app.html";
    }
  }catch(_){}
})();
