# LOGOS — WALLET PERIMETER FULL BOOK (V2)

_Generated: 20260113T113407Z UTC_

## CANONICAL ROUTING FACTS (from nginx)

- PROD UI: `/wallet/` → `/opt/logos/www/wallet/`
- DEV UI: `/wallet_dev/` → `/opt/logos/www/wallet_dev/`
- V2 UI: `/wallet_v2/` → `/opt/logos/www/wallet_v2/`
- NODE API: `/node-api/` → `127.0.0.1:8080`
- WALLET API: `/wallet-api/` → `127.0.0.1:9090`
- COMPAT: `/api/` → `127.0.0.1:8080`
- COMPAT: `/proxy/` → `127.0.0.1:9090`

---

## INVENTORY (wallet folders found)

- /opt/logos/www/wallet
- /opt/logos/www/wallet_backup_20251129T115355Z
- /opt/logos/www/wallet_dev
- /opt/logos/www/wallet_dev.bad_20260103T085840Z
- /opt/logos/www/wallet_dev.bad_20260108T105453Z
- /opt/logos/www/wallet_dev.bak_403_20260104T144956Z
- /opt/logos/www/wallet_dev.bak_before_premium_20260109T073156Z
- /opt/logos/www/wallet_dev.bak_restore_20260108T092512Z
- /opt/logos/www/wallet_dev.broken_20260104T101553Z
- /opt/logos/www/wallet_dev.old_20260104T141213Z
- /opt/logos/www/wallet_dev.old_20260104T141233Z
- /opt/logos/www/wallet_dev.old_20260104T150050Z
- /opt/logos/www/wallet_dev.old_premium_20260108T094612Z
- /opt/logos/www/wallet_dev.prev_20260104T103941Z
- /opt/logos/www/wallet_dev_666
- /opt/logos/www/wallet_dev__111_20260111T150406Z
- /opt/logos/www/wallet_dev__111_20260111T150406Z.tar.gz
- /opt/logos/www/wallet_dev__222_20260111T151455Z
- /opt/logos/www/wallet_dev__222_20260111T151455Z.tar.gz
- /opt/logos/www/wallet_dev__222_20260111T151520Z
- /opt/logos/www/wallet_dev__222_20260111T151520Z.tar.gz
- /opt/logos/www/wallet_dev__777_20260111T114200Z
- /opt/logos/www/wallet_dev__777_20260111T114200Z.tar.gz
- /opt/logos/www/wallet_dev__999_20260111T143334Z
- /opt/logos/www/wallet_dev__999_20260111T143334Z.tar.gz
- /opt/logos/www/wallet_dev__bak_before_restore_20260112T090309Z
- /opt/logos/www/wallet_dev_bak_20260111T104857Z
- /opt/logos/www/wallet_dev_build
- /opt/logos/www/wallet_premium
- /opt/logos/www/wallet_v2
- /var/www/logos/wallet
- /var/www/logos/wallet.js
- /var/www/logos/wallet3

---

## API_BASE_URL / ROUTES REFERENCES (grep)

```txt
/opt/logos/www/wallet_dev/app.js.bak_send_endpoint_20260111T165637Z:145:      mkLine(container, "wallet-api latency", String(j.latency_ms) + " ms", String(j.latency_ms));
/opt/logos/www/wallet_dev/app.js.bak_send_endpoint_20260111T165637Z:157:    const API_BASE = window.API_BASE || "/api";
/opt/logos/www/wallet_dev/app.js.bak_send_endpoint_20260111T165637Z:158:    const WALLET_API = window.WALLET_API || "/wallet-api";
/opt/logos/www/wallet_dev/app.js.bak_send_endpoint_20260111T165637Z:182:      setStatus("ERR node-api: " + (e && e.message ? e.message : String(e)));
/opt/logos/www/wallet_dev/app.js.bak_send_endpoint_20260111T165637Z:195:      if ($("recvBox")) $("recvBox").innerHTML = '<div class="muted">ERR wallet-api receive: ' + escapeHtml(e.message||String(e)) + '</div>';
/opt/logos/www/wallet_dev/app.js.bak_send_endpoint_20260111T165637Z:208:      if ($("extBalBox")) $("extBalBox").innerHTML = '<div class="muted">ERR wallet-api balances: ' + escapeHtml(e.message||String(e)) + '</div>';
/opt/logos/www/wallet_dev/app.js.bak_send_endpoint_20260111T165637Z:240:      const { r } = await jfetch((window.WALLET_API||"/wallet-api") + "/v1/topup/request", {
/opt/logos/www/wallet_dev/app.js.bak_send_endpoint_20260111T165637Z:270:      const { r } = await jfetch((window.WALLET_API||"/wallet-api") + "/v1/quote", {
/opt/logos/www/wallet_dev/app.js.bak_send_endpoint_20260111T165637Z:303:      const { r } = await jfetch((window.WALLET_API||"/wallet-api") + "/v1/withdraw", {
/opt/logos/www/wallet_dev/app.js.bak_send_endpoint_20260111T165637Z:381:    // wallet-api (FastAPI proxy)
/opt/logos/www/wallet_dev/app.js.bak_send_endpoint_20260111T165637Z:382:    return (window.LOGOS_WALLET_API || window.WALLET_API || (window.location.origin.replace(/\/+$/, "") + "/wallet-api"));
/opt/logos/www/wallet_dev/app.js.bak_send_endpoint_20260111T165637Z:439:        <div class="muted">Обмен/ввод/вывод через wallet-api. Для обычных людей — без сырого текста.</div>
/opt/logos/www/wallet_dev/app.js.bak_send_endpoint_20260111T165637Z:633:  const NODE_API = (window.LOGOS_NODE_API || "/api").replace(/\/+$/,"");
/opt/logos/www/wallet_dev/app.html.bak_fix_links_20260109T122714Z:10:<script src="./api_base.js"></script>
/opt/logos/www/wallet_dev/app.html.bak_fix_links_20260109T122714Z:24:        <div class="pill">API: <span id="endpoint" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/app.html.bak_fix_links_20260109T122714Z:125:<!-- ====== External wallets (wallet-api) ====== -->
/opt/logos/www/wallet_dev/app.html.bak_fixTxIn_20260112T062533Z:10:    window.API_BASE="/api";            // node backend
/opt/logos/www/wallet_dev/app.html.bak_fixTxIn_20260112T062533Z:11:    window.WALLET_API="/wallet-api";   // wallet proxy
/opt/logos/www/wallet_dev/app.html.bak_fixTxIn_20260112T062533Z:18:      <div class="pill">API: <span id="api" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/app.html.bak_fixTxIn_20260112T062533Z:78:          <div class="muted">BTC/ETH/TRON/USDT адреса закреплены за RID (wallet-api).</div>
/opt/logos/www/wallet_dev/app.html.bak_fixTxIn_20260112T062533Z:82:            <summary>Details (wallet-api raw)</summary>
/opt/logos/www/wallet_dev/app.html.bak_fixTxIn_20260112T062533Z:89:          <div class="muted">Баланс внешних сетей (wallet-api).</div>
/opt/logos/www/wallet_dev/app.html.bak_fixTxIn_20260112T062533Z:93:            <summary>Details (wallet-api raw)</summary>
/opt/logos/www/wallet_dev/app.html.bak_fixTxIn_20260112T062533Z:105:          <div class="muted">Отправка через wallet-api /v1/withdraw (по OpenAPI: USDT + ETH).</div>
/opt/logos/www/wallet_dev/app.html.bak_fixTxIn_20260112T062533Z:134:            Для LGN-трансфера нужен endpoint в node-api (например /tx/send). Сейчас у тебя подтверждён только /balance.
/opt/logos/www/wallet_dev/app.html.bak_fixTxIn_20260112T062533Z:159:          <div class="muted">Получить адрес для пополнения (wallet-api /v1/topup/request).</div>
/opt/logos/www/wallet_dev/app.html.bak_fixTxIn_20260112T062533Z:176:          <div class="muted">Расчёт курса (wallet-api /v1/quote). amount — integer.</div>
/opt/logos/www/wallet_dev/app.html.bak_fixTxIn_20260112T062533Z:218:          <div class="muted mono">API_BASE = /api, WALLET_API = /wallet-api</div>
/opt/logos/www/wallet_dev/app.html.bak_submit_20260111T172540Z:10:    window.API_BASE="/api";            // node backend
/opt/logos/www/wallet_dev/app.html.bak_submit_20260111T172540Z:11:    window.WALLET_API="/wallet-api";   // wallet proxy
/opt/logos/www/wallet_dev/app.html.bak_submit_20260111T172540Z:18:      <div class="pill">API: <span id="api" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/app.html.bak_submit_20260111T172540Z:78:          <div class="muted">BTC/ETH/TRON/USDT адреса закреплены за RID (wallet-api).</div>
/opt/logos/www/wallet_dev/app.html.bak_submit_20260111T172540Z:82:            <summary>Details (wallet-api raw)</summary>
/opt/logos/www/wallet_dev/app.html.bak_submit_20260111T172540Z:89:          <div class="muted">Баланс внешних сетей (wallet-api).</div>
/opt/logos/www/wallet_dev/app.html.bak_submit_20260111T172540Z:93:            <summary>Details (wallet-api raw)</summary>
/opt/logos/www/wallet_dev/app.html.bak_submit_20260111T172540Z:105:          <div class="muted">Отправка через wallet-api /v1/withdraw (по OpenAPI: USDT + ETH).</div>
/opt/logos/www/wallet_dev/app.html.bak_submit_20260111T172540Z:134:            Для LGN-трансфера нужен endpoint в node-api (например /tx/send). Сейчас у тебя подтверждён только /balance.
/opt/logos/www/wallet_dev/app.html.bak_submit_20260111T172540Z:159:          <div class="muted">Получить адрес для пополнения (wallet-api /v1/topup/request).</div>
/opt/logos/www/wallet_dev/app.html.bak_submit_20260111T172540Z:176:          <div class="muted">Расчёт курса (wallet-api /v1/quote). amount — integer.</div>
/opt/logos/www/wallet_dev/app.html.bak_submit_20260111T172540Z:218:          <div class="muted mono">API_BASE = /api, WALLET_API = /wallet-api</div>
/opt/logos/www/wallet_dev/assets.js:24:    // node-api у тебя работает и так, но делаем безопасно
/opt/logos/www/wallet_dev/assets.js:25:    const cands = ["/node-api", "/node-api/api"];
/opt/logos/www/wallet_dev/assets.js:32:    return "/node-api";
/opt/logos/www/wallet_dev/assets.js:145:      // 1) LGN balance (node-api)
/opt/logos/www/wallet_dev/assets.js:148:      // 2) мульти-активы + адреса (wallet-api)
/opt/logos/www/wallet_dev/assets.js:149:      const b = await jget(`/wallet-api/v1/balances/${encodeURIComponent(rid)}`);
/opt/logos/www/wallet_dev/app.html.bak_sendmod_20260111T150430Z:10:    window.API_BASE="/api";            // node backend
/opt/logos/www/wallet_dev/app.html.bak_sendmod_20260111T150430Z:11:    window.WALLET_API="/wallet-api";   // wallet proxy
/opt/logos/www/wallet_dev/app.html.bak_sendmod_20260111T150430Z:18:      <div class="pill">API: <span id="api" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/app.html.bak_sendmod_20260111T150430Z:78:          <div class="muted">BTC/ETH/TRON/USDT адреса закреплены за RID (wallet-api).</div>
/opt/logos/www/wallet_dev/app.html.bak_sendmod_20260111T150430Z:82:            <summary>Details (wallet-api raw)</summary>
/opt/logos/www/wallet_dev/app.html.bak_sendmod_20260111T150430Z:89:          <div class="muted">Баланс внешних сетей (wallet-api).</div>
/opt/logos/www/wallet_dev/app.html.bak_sendmod_20260111T150430Z:93:            <summary>Details (wallet-api raw)</summary>
/opt/logos/www/wallet_dev/app.html.bak_sendmod_20260111T150430Z:105:          <div class="muted">Отправка через wallet-api /v1/withdraw (по OpenAPI: USDT + ETH).</div>
/opt/logos/www/wallet_dev/app.html.bak_sendmod_20260111T150430Z:134:            Для LGN-трансфера нужен endpoint в node-api (например /tx/send). Сейчас у тебя подтверждён только /balance.
/opt/logos/www/wallet_dev/app.html.bak_sendmod_20260111T150430Z:159:          <div class="muted">Получить адрес для пополнения (wallet-api /v1/topup/request).</div>
/opt/logos/www/wallet_dev/app.html.bak_sendmod_20260111T150430Z:176:          <div class="muted">Расчёт курса (wallet-api /v1/quote). amount — integer.</div>
/opt/logos/www/wallet_dev/app.html.bak_sendmod_20260111T150430Z:218:          <div class="muted mono">API_BASE = /api, WALLET_API = /wallet-api</div>
/opt/logos/www/wallet_dev/app.html.bak_topbal_20260111T081455Z:13:  <script src="./api_base.js?v=20260111_0723"></script>
/opt/logos/www/wallet_dev/app.html.bak_topbal_20260111T081455Z:34:        <div class="pill">API: <span id="endpoint" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/app.html.bak_topbal_20260111T081455Z:134:            <p class="muted">BTC/ETH/TRON/USDT адреса закреплены за RID (wallet-api). Просто копируй и принимай.</p>
/opt/logos/www/wallet_dev/app.html.bak_topbal_20260111T081455Z:253:          <p class="muted">Пресеты добавим дальше. Сейчас — quote/create через wallet-api openapi.</p>
/opt/logos/www/wallet_dev/app.js.bak_fix_login_20260109T130402Z:3:const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/node-api'));
/opt/logos/www/wallet_dev/app.js.bak_fix_login_20260109T130402Z:362:/* ====== LOGOS_EXT_WALLET_UI (wallet-api balances) ====== */
/opt/logos/www/wallet_dev/app.js.bak_fix_login_20260109T130402Z:365:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/app.js.bak_fix_login_20260109T130402Z:522:/* ====== LOGOS_BRIDGE_UI_BIND (auto-detect bridge endpoints from wallet-api openapi) ====== */
/opt/logos/www/wallet_dev/app.js.bak_fix_login_20260109T130402Z:525:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/app.html.bak_fullui_20260109T170643Z:14:  <script src="./api_base.js?v=20260109_01"></script>
/opt/logos/www/wallet_dev/app.html.bak_fullui_20260109T170643Z:36:        <div class="pill">API: <span id="endpoint" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/app.html.bak_fullui_20260109T170643Z:139:          <p class="muted">wallet-api + autodetect по openapi.json</p>
/opt/logos/www/wallet_dev/app.html.bak_ridui_20260111T091512Z:13:  <script src="./api_base.js?v=20260111_0723"></script>
/opt/logos/www/wallet_dev/app.html.bak_ridui_20260111T091512Z:34:        <div class="pill">API: <span id="endpoint" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/app.html.bak_ridui_20260111T091512Z:135:            <p class="muted">BTC/ETH/TRON/USDT адреса закреплены за RID (wallet-api). Просто копируй и принимай.</p>
/opt/logos/www/wallet_dev/app.html.bak_ridui_20260111T091512Z:254:          <p class="muted">Пресеты добавим дальше. Сейчас — quote/create через wallet-api openapi.</p>
/opt/logos/www/wallet_dev/index.html.bak_fix_20260109T131516Z:14:  <script src="./api_base.js?v=20260109_01"></script>
/opt/logos/www/wallet_dev/index.html.bak_fix_20260109T131516Z:35:        <div class="pill">API: <span id="endpoint" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/index.html.bak_fix_20260109T131516Z:138:          <p class="muted">wallet-api + autodetect по openapi.json</p>
/opt/logos/www/wallet_dev/_bak_premiumtabs_20260109T063827Z/app.js:3:const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/node-api'));
/opt/logos/www/wallet_dev/_bak_premiumtabs_20260109T063827Z/app.js:362:/* ====== LOGOS_EXT_WALLET_UI (wallet-api balances) ====== */
/opt/logos/www/wallet_dev/_bak_premiumtabs_20260109T063827Z/app.js:365:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/_bak_premiumtabs_20260109T063827Z/app.js:522:/* ====== LOGOS_BRIDGE_UI_BIND (auto-detect bridge endpoints from wallet-api openapi) ====== */
/opt/logos/www/wallet_dev/_bak_premiumtabs_20260109T063827Z/app.js:525:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/_bak_premiumtabs_20260109T063827Z/app.html:10:<script src="./api_base.js"></script>
/opt/logos/www/wallet_dev/_bak_premiumtabs_20260109T063827Z/app.html:24:        <div class="pill">API: <span id="endpoint" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/_bak_premiumtabs_20260109T063827Z/app.html:125:<!-- ====== External wallets (wallet-api) ====== -->
/opt/logos/www/wallet_dev/compat.js:5:  const API = location.origin + "/node-api";
/opt/logos/www/wallet_dev/app.html.bak_rm_connect_20260101T123446Z:10:<script src="./api_base.js"></script>
/opt/logos/www/wallet_dev/app.html.bak_rm_connect_20260101T123446Z:23:        <div class="pill">API: <span id="endpoint" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/app.js:145:      mkLine(container, "wallet-api latency", String(j.latency_ms) + " ms", String(j.latency_ms));
/opt/logos/www/wallet_dev/app.js:157:    const API_BASE = window.API_BASE || "/api";
/opt/logos/www/wallet_dev/app.js:158:    const WALLET_API = window.WALLET_API || "/wallet-api";
/opt/logos/www/wallet_dev/app.js:182:      setStatus("ERR node-api: " + (e && e.message ? e.message : String(e)));
/opt/logos/www/wallet_dev/app.js:195:      if ($("recvBox")) $("recvBox").innerHTML = '<div class="muted">ERR wallet-api receive: ' + escapeHtml(e.message||String(e)) + '</div>';
/opt/logos/www/wallet_dev/app.js:208:      if ($("extBalBox")) $("extBalBox").innerHTML = '<div class="muted">ERR wallet-api balances: ' + escapeHtml(e.message||String(e)) + '</div>';
/opt/logos/www/wallet_dev/app.js:240:      const { r } = await jfetch((window.WALLET_API||"/wallet-api") + "/v1/topup/request", {
/opt/logos/www/wallet_dev/app.js:270:      const { r } = await jfetch((window.WALLET_API||"/wallet-api") + "/v1/quote", {
/opt/logos/www/wallet_dev/app.js:303:      const { r } = await jfetch((window.WALLET_API||"/wallet-api") + "/v1/withdraw", {
/opt/logos/www/wallet_dev/app.js:381:    // wallet-api (FastAPI proxy)
/opt/logos/www/wallet_dev/app.js:382:    return (window.LOGOS_WALLET_API || window.WALLET_API || (window.location.origin.replace(/\/+$/, "") + "/wallet-api"));
/opt/logos/www/wallet_dev/app.js:439:        <div class="muted">Обмен/ввод/вывод через wallet-api. Для обычных людей — без сырого текста.</div>
/opt/logos/www/wallet_dev/app.js:633:  const NODE_API = (window.LOGOS_NODE_API || "/api").replace(/\/+$/,"");
/opt/logos/www/wallet_dev/app.html.bak_vbump_20260111T064142Z:13:  <script src="./api_base.js?v=20260110_01"></script>
/opt/logos/www/wallet_dev/app.html.bak_vbump_20260111T064142Z:34:        <div class="pill">API: <span id="endpoint" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/app.html.bak_vbump_20260111T064142Z:134:            <p class="muted">BTC/ETH/TRON/USDT адреса закреплены за RID (wallet-api). Просто копируй и принимай.</p>
/opt/logos/www/wallet_dev/app.html.bak_vbump_20260111T064142Z:253:          <p class="muted">Пресеты добавим дальше. Сейчас — quote/create через wallet-api openapi.</p>
/opt/logos/www/wallet_dev/index.html.bak_premium_20260109T123537Z:10:<script src="./api_base.js"></script>
/opt/logos/www/wallet_dev/index.html.bak_premium_20260109T123537Z:24:        <div class="pill">API: <span id="endpoint" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/index.html.bak_premium_20260109T123537Z:125:<!-- ====== External wallets (wallet-api) ====== -->
/opt/logos/www/wallet_dev/_bak_bridge_20260107T102822Z/app.js:3:const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/node-api'));
/opt/logos/www/wallet_dev/_bak_bridge_20260107T102822Z/app.js:362:/* ====== LOGOS_EXT_WALLET_UI (wallet-api balances) ====== */
/opt/logos/www/wallet_dev/_bak_bridge_20260107T102822Z/app.js:365:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/_bak_bridge_20260107T102822Z/app.js:522:/* ====== LOGOS_BRIDGE_UI_BIND (auto-detect bridge endpoints from wallet-api openapi) ====== */
/opt/logos/www/wallet_dev/_bak_bridge_20260107T102822Z/app.js:525:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/_bak_bridge_20260107T102822Z/app.html:10:<script src="./api_base.js"></script>
/opt/logos/www/wallet_dev/_bak_bridge_20260107T102822Z/app.html:24:        <div class="pill">API: <span id="endpoint" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/_bak_bridge_20260107T102822Z/app.html:125:<!-- ====== External wallets (wallet-api) ====== -->
/opt/logos/www/wallet_dev/app.html.bak_tabs_20260111T110201Z:8:  <script src="./api_base.js?v=1"></script>
/opt/logos/www/wallet_dev/app.html.bak_tabs_20260111T110201Z:14:      <div class="pill">API: <span id="api" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/app.html.bak_assetsfix_20260110T071213Z:14:  <script src="./api_base.js?v=20260109_99"></script>
/opt/logos/www/wallet_dev/app.html.bak_assetsfix_20260110T071213Z:40:        <div class="pill">API: <span id="endpoint" class="mono">/node-api</span></div>
/opt/logos/www/wallet_dev/app.html.bak_assetsfix_20260110T071213Z:108:          <p class="muted">Адреса и балансы привязаны к вашему RID через wallet-api.</p>
/opt/logos/www/wallet_dev/app.html.bak_assetsfix_20260110T071213Z:157:        <p class="muted">Транзакция подписывается локально (Ed25519) и отправляется батчем в node-api.</p>
/opt/logos/www/wallet_dev/app.html.bak_assetsfix_20260110T071213Z:215:        <p class="muted">Депозит / конвертация через wallet-api. Авто-детект эндпоинтов по openapi.json.</p>
/opt/logos/www/wallet_dev/app.html.bak_assetsfix_20260110T071213Z:310:            <button class="secondary" type="button" onclick="window.LOGOS_EXT_WALLET_UI?.tick?.();">Ping wallet-api</button>
/opt/logos/www/wallet_dev/api_base.js.bak_fix_base_20260111T065527Z:4:  // node backend (nginx /api -> 127.0.0.1:8080)
/opt/logos/www/wallet_dev/api_base.js.bak_fix_base_20260111T065527Z:5:  window.LOGOS_NODE_API   = origin + "/api";
/opt/logos/www/wallet_dev/api_base.js.bak_fix_base_20260111T065527Z:8:  window.LOGOS_WALLET_API = origin + "/wallet-api";
/opt/logos/www/wallet_dev/api_base.js.bak_fix_base_20260111T065527Z:11:  window.NODE_API   = "/api";
/opt/logos/www/wallet_dev/api_base.js.bak_fix_base_20260111T065527Z:12:  window.API_BASE   = "/api";
/opt/logos/www/wallet_dev/api_base.js.bak_fix_base_20260111T065527Z:13:  window.WALLET_API = "/wallet-api";
/opt/logos/www/wallet_dev/app.js.bak_fix_or_20260111T080227Z:5:// --- API router: chain endpoints live on /api (node), wallet proxy lives on /wallet-api
/opt/logos/www/wallet_dev/app.js.bak_fix_or_20260111T080227Z:12:    if (p.startsWith("/wallet-api/balance/")) u.pathname = p.replace("/wallet-api/balance/","/api/balance/");
/opt/logos/www/wallet_dev/app.js.bak_fix_or_20260111T080227Z:13:    if (p.startsWith("/wallet-api/v1/balances/")) u.pathname = p.replace("/wallet-api/v1/balances/","/api/balance/");
/opt/logos/www/wallet_dev/app.js.bak_fix_or_20260111T080227Z:14:    if (p.startsWith("/wallet-api/v1/balance/"))  u.pathname = p.replace("/wallet-api/v1/balance/","/api/balance/");
/opt/logos/www/wallet_dev/app.js.bak_fix_or_20260111T080227Z:17:    if (p == "/wallet-api/submit_tx" or p.endswith("/submit_tx")) u.pathname = "/api/submit_tx";
/opt/logos/www/wallet_dev/app.js.bak_fix_or_20260111T080227Z:20:    if (p.startsWith("/wallet-api/stake/")) u.pathname = p.replace("/wallet-api/stake/","/api/stake/");
/opt/logos/www/wallet_dev/app.js.bak_fix_or_20260111T080227Z:27:const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/node-api'));
/opt/logos/www/wallet_dev/app.js.bak_fix_or_20260111T080227Z:428:/* ====== LOGOS_EXT_WALLET_UI (wallet-api balances) ====== */
/opt/logos/www/wallet_dev/app.js.bak_fix_or_20260111T080227Z:431:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/app.js.bak_fix_or_20260111T080227Z:597:/* ====== LOGOS_BRIDGE_UI_BIND (auto-detect bridge endpoints from wallet-api openapi) ====== */
/opt/logos/www/wallet_dev/app.js.bak_fix_or_20260111T080227Z:600:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/modules/send.js.bak_fixTxIn_20260112T062533Z:17:    // node backend (nginx /api -> node)
/opt/logos/www/wallet_dev/modules/send.js.bak_fixTxIn_20260112T062533Z:18:    return (window.LOGOS_NODE_API || window.API_BASE || "/api");
/opt/logos/www/wallet_dev/modules/send.js.bak_restore_sendui_20260112T070813Z:15:    // у тебя нода проксится как /api (nginx)
/opt/logos/www/wallet_dev/modules/send.js.bak_restore_sendui_20260112T070813Z:16:    return (window.LOGOS_NODE_API || "/api").replace(/\/+$/,"");
/opt/logos/www/wallet_dev/modules/settings.js:26:      if (t.includes("raw") || s.includes("details") || s.includes("raw") || t.includes("wallet-api raw")) {
/opt/logos/www/wallet_dev/modules/settings.js:42:      if (t.trim() === "details (raw)" || t.trim() === "details (wallet-api raw)" ) {
/opt/logos/www/wallet_dev/modules/settings.js:172:        api: (window.LOGOS_NODE_API || window.API_BASE || "/api"),
/opt/logos/www/wallet_dev/modules/settings.js:173:        wallet_api: (window.LOGOS_WALLET_API || window.WALLET_API || "/wallet-api"),
/opt/logos/www/wallet_dev/modules/settings.js:222:      api: (window.LOGOS_NODE_API || window.API_BASE || "/api"),
/opt/logos/www/wallet_dev/modules/settings.js:223:      wallet_api: (window.LOGOS_WALLET_API || window.WALLET_API || "/wallet-api"),
/opt/logos/www/wallet_dev/modules/send.js.bak_real_20260112T084410Z:17:    // node backend (nginx /api -> node)
/opt/logos/www/wallet_dev/modules/send.js.bak_real_20260112T084410Z:18:    return (window.LOGOS_NODE_API || window.API_BASE || "/api");
/opt/logos/www/wallet_dev/modules/send.js.bak_submit_20260111T172540Z:17:    // node backend (nginx /api -> node)
/opt/logos/www/wallet_dev/modules/send.js.bak_submit_20260111T172540Z:18:    return (window.LOGOS_NODE_API || window.API_BASE || "/api");
/opt/logos/www/wallet_dev/modules/send.js:1:/* modules/send.js — REAL SEND LGN (TxIn -> /api/submit_tx) */
/opt/logos/www/wallet_dev/modules/send.js:15:    return (window.LOGOS_NODE_API || "/api").replace(/\/+$/,"");
/opt/logos/www/wallet_dev/app.html.bak_assetsfix_20260110T084839Z:13:  <script src="./api_base.js?v=20260109_30"></script>
/opt/logos/www/wallet_dev/app.html.bak_assetsfix_20260110T084839Z:36:        <div class="pill">API: <span id="endpoint" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/app.html.bak_assetsfix_20260110T084839Z:126:          <p class="muted">BTC/ETH/TRON/USDT закреплены за RID (wallet-api). Просто копируй и принимай.</p>
/opt/logos/www/wallet_dev/app.html.bak_assetsfix_20260110T084839Z:262:          <p class="muted">Quote / Create берём из wallet-api/openapi.json (авто-подхват).</p>
/opt/logos/www/wallet_dev/api_base.js.bak_fix_base_20260111T064058Z:4:  // nginx: /api -> node backend (127.0.0.1:8080)
/opt/logos/www/wallet_dev/api_base.js.bak_fix_base_20260111T064058Z:5:  // keep node-api as direct alias too
/opt/logos/www/wallet_dev/api_base.js.bak_fix_base_20260111T064058Z:6:  window.LOGOS_WALLET_API = origin + "/api";
/opt/logos/www/wallet_dev/api_base.js.bak_fix_base_20260111T064058Z:7:  window.LOGOS_NODE_API   = origin + "/node-api";
/opt/logos/www/wallet_dev/api_base.js.bak_fix_base_20260111T064058Z:10:  window.WALLET_API = "/api";
/opt/logos/www/wallet_dev/api_base.js.bak_fix_base_20260111T064058Z:11:  window.NODE_API   = "/api";
/opt/logos/www/wallet_dev/api_base.js.bak_fix_base_20260111T064058Z:12:  window.API_BASE   = "/api";
/opt/logos/www/wallet_dev/app.js.bak_assets_20260110T080352Z:3:const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/node-api'));
/opt/logos/www/wallet_dev/app.js.bak_assets_20260110T080352Z:362:/* ====== LOGOS_EXT_WALLET_UI (wallet-api balances) ====== */
/opt/logos/www/wallet_dev/app.js.bak_assets_20260110T080352Z:365:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/app.js.bak_assets_20260110T080352Z:522:/* ====== LOGOS_BRIDGE_UI_BIND (auto-detect bridge endpoints from wallet-api openapi) ====== */
/opt/logos/www/wallet_dev/app.js.bak_assets_20260110T080352Z:525:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/auth.html.bak_rm_connect_20260101T123446Z:10:<script src="./api_base.js"></script>
/opt/logos/www/wallet_dev/app.js.bak_fix_ext_20260109T122800Z:3:const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/node-api'));
/opt/logos/www/wallet_dev/app.js.bak_fix_ext_20260109T122800Z:362:/* ====== LOGOS_EXT_WALLET_UI (wallet-api balances) ====== */
/opt/logos/www/wallet_dev/app.js.bak_fix_ext_20260109T122800Z:365:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/app.js.bak_fix_ext_20260109T122800Z:522:/* ====== LOGOS_BRIDGE_UI_BIND (auto-detect bridge endpoints from wallet-api openapi) ====== */
/opt/logos/www/wallet_dev/app.js.bak_fix_ext_20260109T122800Z:525:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/app.js.bak_fix_ext_20260109T122800Z:684:/* ====== LOGOS_EXTERNAL_ASSETS (wallet-api receive/balances) ====== */
/opt/logos/www/wallet_dev/app.js.bak_fix_ext_20260109T122800Z:687:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/api_base.js.bak_fix_20260111T062231Z:4:  // nginx: /api -> node backend (127.0.0.1:8080)
/opt/logos/www/wallet_dev/api_base.js.bak_fix_20260111T062231Z:5:  // keep node-api as direct alias too
/opt/logos/www/wallet_dev/api_base.js.bak_fix_20260111T062231Z:6:  window.LOGOS_WALLET_API = origin + "/api";
/opt/logos/www/wallet_dev/api_base.js.bak_fix_20260111T062231Z:7:  window.LOGOS_NODE_API   = origin + "/node-api";
/opt/logos/www/wallet_dev/api_base.js.bak_fix_20260111T062231Z:10:  window.WALLET_API = "/api";
/opt/logos/www/wallet_dev/api_base.js.bak_fix_20260111T062231Z:11:  window.NODE_API   = "/api";
/opt/logos/www/wallet_dev/api_base.js.bak_fix_20260111T062231Z:12:  window.API_BASE   = "/api";
/opt/logos/www/wallet_dev/app.html.bak_assets_20260110T080352Z:13:  <script src="./api_base.js?v=20260109_30"></script>
/opt/logos/www/wallet_dev/app.html.bak_assets_20260110T080352Z:36:        <div class="pill">API: <span id="endpoint" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/app.html.bak_assets_20260110T080352Z:110:          <p class="muted">BTC/ETH/TRON/USDT закреплены за RID (wallet-api). Просто копируй и принимай.</p>
/opt/logos/www/wallet_dev/app.html.bak_assets_20260110T080352Z:238:          <p class="muted">Quote / Create берём из wallet-api/openapi.json (авто-подхват).</p>
/opt/logos/www/wallet_dev/app.html.bak_assetsfix_20260110T091111Z:13:  <script src="./api_base.js?v=20260110_01"></script>
/opt/logos/www/wallet_dev/app.html.bak_assetsfix_20260110T091111Z:34:        <div class="pill">API: <span id="endpoint" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/app.html.bak_assetsfix_20260110T091111Z:133:            <p class="muted">BTC/ETH/TRON/USDT адреса закреплены за RID (wallet-api). Просто копируй и принимай.</p>
/opt/logos/www/wallet_dev/app.html.bak_assetsfix_20260110T091111Z:252:          <p class="muted">Пресеты добавим дальше. Сейчас — quote/create через wallet-api openapi.</p>
/opt/logos/www/wallet_dev/app.html.bak_nacl_20260109T140204Z:14:  <script src="./api_base.js?v=20260109_01"></script>
/opt/logos/www/wallet_dev/app.html.bak_nacl_20260109T140204Z:35:        <div class="pill">API: <span id="endpoint" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/app.html.bak_nacl_20260109T140204Z:138:          <p class="muted">wallet-api + autodetect по openapi.json</p>
/opt/logos/www/wallet_dev/app.html.bak_assetsui_20260108T143744Z:10:<script src="./api_base.js"></script>
/opt/logos/www/wallet_dev/app.html.bak_assetsui_20260108T143744Z:24:        <div class="pill">API: <span id="endpoint" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/app.html.bak_assetsui_20260108T143744Z:125:<!-- ====== External wallets (wallet-api) ====== -->
/opt/logos/www/wallet_dev/app.js.bak_fix_balanceep_20260111T064121Z:3:const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/node-api'));
/opt/logos/www/wallet_dev/app.js.bak_fix_balanceep_20260111T064121Z:391:/* ====== LOGOS_EXT_WALLET_UI (wallet-api balances) ====== */
/opt/logos/www/wallet_dev/app.js.bak_fix_balanceep_20260111T064121Z:394:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/app.js.bak_fix_balanceep_20260111T064121Z:558:/* ====== LOGOS_BRIDGE_UI_BIND (auto-detect bridge endpoints from wallet-api openapi) ====== */
/opt/logos/www/wallet_dev/app.js.bak_fix_balanceep_20260111T064121Z:561:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/app.js.bak_fix_or_20260111T080255Z:5:// --- API router: chain endpoints live on /api (node), wallet proxy lives on /wallet-api
/opt/logos/www/wallet_dev/app.js.bak_fix_or_20260111T080255Z:12:    if (p.startsWith("/wallet-api/balance/")) u.pathname = p.replace("/wallet-api/balance/","/api/balance/");
/opt/logos/www/wallet_dev/app.js.bak_fix_or_20260111T080255Z:13:    if (p.startsWith("/wallet-api/v1/balances/")) u.pathname = p.replace("/wallet-api/v1/balances/","/api/balance/");
/opt/logos/www/wallet_dev/app.js.bak_fix_or_20260111T080255Z:14:    if (p.startsWith("/wallet-api/v1/balance/"))  u.pathname = p.replace("/wallet-api/v1/balance/","/api/balance/");
/opt/logos/www/wallet_dev/app.js.bak_fix_or_20260111T080255Z:17:    if (p === "/wallet-api/submit_tx" || p.endsWith("/submit_tx")) u.pathname = "/api/submit_tx";
/opt/logos/www/wallet_dev/app.js.bak_fix_or_20260111T080255Z:20:    if (p.startsWith("/wallet-api/stake/")) u.pathname = p.replace("/wallet-api/stake/","/api/stake/");
/opt/logos/www/wallet_dev/app.js.bak_fix_or_20260111T080255Z:27:const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/node-api'));
/opt/logos/www/wallet_dev/app.js.bak_fix_or_20260111T080255Z:428:/* ====== LOGOS_EXT_WALLET_UI (wallet-api balances) ====== */
/opt/logos/www/wallet_dev/app.js.bak_fix_or_20260111T080255Z:431:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/app.js.bak_fix_or_20260111T080255Z:597:/* ====== LOGOS_BRIDGE_UI_BIND (auto-detect bridge endpoints from wallet-api openapi) ====== */
/opt/logos/www/wallet_dev/app.js.bak_fix_or_20260111T080255Z:600:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/app.js.bak_before_fix_20260111T072300Z:3:const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/node-api'));
/opt/logos/www/wallet_dev/app.js.bak_before_fix_20260111T072300Z:391:/* ====== LOGOS_EXT_WALLET_UI (wallet-api balances) ====== */
/opt/logos/www/wallet_dev/app.js.bak_before_fix_20260111T072300Z:394:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/app.js.bak_before_fix_20260111T072300Z:558:/* ====== LOGOS_BRIDGE_UI_BIND (auto-detect bridge endpoints from wallet-api openapi) ====== */
/opt/logos/www/wallet_dev/app.js.bak_before_fix_20260111T072300Z:561:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/api_base.js:3:  window.API_BASE   = "/api";        // node backend (nginx -> 127.0.0.1:8080)
/opt/logos/www/wallet_dev/api_base.js:4:  window.WALLET_API = "/wallet-api"; // wallet proxy (FastAPI)
/opt/logos/www/wallet_dev/app.js.bak_uiclean_20260111T112205Z:94:    $("api").textContent = window.API_BASE || "/api";
/opt/logos/www/wallet_dev/app.js.bak_uiclean_20260111T112205Z:100:      const { r, ms } = await jfetch((window.API_BASE||"/api") + "/balance/" + encodeURIComponent(rid));
/opt/logos/www/wallet_dev/app.js.bak_uiclean_20260111T112205Z:116:      setStatus("ERR node-api: " + (e && e.message ? e.message : String(e)));
/opt/logos/www/wallet_dev/app.js.bak_uiclean_20260111T112205Z:121:      const { r } = await jfetch((window.WALLET_API||"/wallet-api") + "/v1/receive/" + encodeURIComponent(rid));
/opt/logos/www/wallet_dev/app.js.bak_uiclean_20260111T112205Z:128:      $("recvBox").innerHTML = '<div class="muted">ERR wallet-api receive: ' + escapeHtml(e.message||String(e)) + '</div>';
/opt/logos/www/wallet_dev/app.js.bak_uiclean_20260111T112205Z:133:      const { r } = await jfetch((window.WALLET_API||"/wallet-api") + "/v1/balances/" + encodeURIComponent(rid));
/opt/logos/www/wallet_dev/app.js.bak_uiclean_20260111T112205Z:140:      $("extBalBox").innerHTML = '<div class="muted">ERR wallet-api balances: ' + escapeHtml(e.message||String(e)) + '</div>';
/opt/logos/www/wallet_dev/app.js.bak_uiclean_20260111T112205Z:171:      const { r } = await jfetch((window.WALLET_API||"/wallet-api") + "/v1/topup/request", {
/opt/logos/www/wallet_dev/app.js.bak_uiclean_20260111T112205Z:195:      const { r } = await jfetch((window.WALLET_API||"/wallet-api") + "/v1/quote", {
/opt/logos/www/wallet_dev/app.js.bak_uiclean_20260111T112205Z:227:      const { r } = await jfetch((window.WALLET_API||"/wallet-api") + "/v1/withdraw", {
/opt/logos/www/wallet_dev/app.js.bak_before_router_20260111T074254Z:3:const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/node-api'));
/opt/logos/www/wallet_dev/app.js.bak_before_router_20260111T074254Z:404:/* ====== LOGOS_EXT_WALLET_UI (wallet-api balances) ====== */
/opt/logos/www/wallet_dev/app.js.bak_before_router_20260111T074254Z:407:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/app.js.bak_before_router_20260111T074254Z:571:/* ====== LOGOS_BRIDGE_UI_BIND (auto-detect bridge endpoints from wallet-api openapi) ====== */
/opt/logos/www/wallet_dev/app.js.bak_before_router_20260111T074254Z:574:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/app.js.bak_bootfix_20260111T081518Z:5:// --- API router: chain endpoints live on /api (node), wallet proxy lives on /wallet-api
/opt/logos/www/wallet_dev/app.js.bak_bootfix_20260111T081518Z:12:    if (p.startsWith("/wallet-api/balance/")) u.pathname = p.replace("/wallet-api/balance/","/api/balance/");
/opt/logos/www/wallet_dev/app.js.bak_bootfix_20260111T081518Z:13:    if (p.startsWith("/wallet-api/v1/balances/")) u.pathname = p.replace("/wallet-api/v1/balances/","/api/balance/");
/opt/logos/www/wallet_dev/app.js.bak_bootfix_20260111T081518Z:14:    if (p.startsWith("/wallet-api/v1/balance/"))  u.pathname = p.replace("/wallet-api/v1/balance/","/api/balance/");
/opt/logos/www/wallet_dev/app.js.bak_bootfix_20260111T081518Z:17:    if (p === "/wallet-api/submit_tx" || p.endsWith("/submit_tx")) u.pathname = "/api/submit_tx";
/opt/logos/www/wallet_dev/app.js.bak_bootfix_20260111T081518Z:20:    if (p.startsWith("/wallet-api/stake/")) u.pathname = p.replace("/wallet-api/stake/","/api/stake/");
/opt/logos/www/wallet_dev/app.js.bak_bootfix_20260111T081518Z:27:const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/node-api'));
/opt/logos/www/wallet_dev/app.js.bak_bootfix_20260111T081518Z:428:/* ====== LOGOS_EXT_WALLET_UI (wallet-api balances) ====== */
/opt/logos/www/wallet_dev/app.js.bak_bootfix_20260111T081518Z:431:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/app.js.bak_bootfix_20260111T081518Z:597:/* ====== LOGOS_BRIDGE_UI_BIND (auto-detect bridge endpoints from wallet-api openapi) ====== */
/opt/logos/www/wallet_dev/app.js.bak_bootfix_20260111T081518Z:600:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/auth.html.bak_theme_20260101T135217Z:10:<script src="./api_base.js"></script>
/opt/logos/www/wallet_dev/app.html.bak_directbind_20251223T163240Z:22:        <div class="pill">API: <span id="endpoint" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/app.js.bak_amountfix_20260110T113232Z:3:const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/node-api'));
/opt/logos/www/wallet_dev/app.js.bak_amountfix_20260110T113232Z:404:/* ====== LOGOS_EXT_WALLET_UI (wallet-api balances) ====== */
/opt/logos/www/wallet_dev/app.js.bak_amountfix_20260110T113232Z:407:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/app.js.bak_amountfix_20260110T113232Z:571:/* ====== LOGOS_BRIDGE_UI_BIND (auto-detect bridge endpoints from wallet-api openapi) ====== */
/opt/logos/www/wallet_dev/app.js.bak_amountfix_20260110T113232Z:574:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/app.js.bak_amountfix_20260110T113232Z:769:    // /node-api balance
/opt/logos/www/wallet_dev/app.js.bak_amountfix_20260110T113232Z:799:    const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/app.js.bak_amountfix_20260110T113232Z:803:    if (!r.ok) throw new Error("wallet-api HTTP " + r.status);
/opt/logos/www/wallet_dev/app.html.bak_ridui_20260111T091544Z:13:  <script src="./api_base.js?v=20260111_0723"></script>
/opt/logos/www/wallet_dev/app.html.bak_ridui_20260111T091544Z:34:        <div class="pill">API: <span id="endpoint" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/app.html.bak_ridui_20260111T091544Z:135:            <p class="muted">BTC/ETH/TRON/USDT адреса закреплены за RID (wallet-api). Просто копируй и принимай.</p>
/opt/logos/www/wallet_dev/app.html.bak_ridui_20260111T091544Z:254:          <p class="muted">Пресеты добавим дальше. Сейчас — quote/create через wallet-api openapi.</p>
/opt/logos/www/wallet_dev/app.html.bak_fullui_20260110T070800Z:14:  <script src="./api_base.js?v=20260109_99"></script>
/opt/logos/www/wallet_dev/app.html.bak_fullui_20260110T070800Z:40:        <div class="pill">API: <span id="endpoint" class="mono">/node-api</span></div>
/opt/logos/www/wallet_dev/app.html.bak_fullui_20260110T070800Z:108:          <p class="muted">Адреса и балансы привязаны к вашему RID через wallet-api.</p>
/opt/logos/www/wallet_dev/app.html.bak_fullui_20260110T070800Z:157:        <p class="muted">Транзакция подписывается локально (Ed25519) и отправляется батчем в node-api.</p>
/opt/logos/www/wallet_dev/app.html.bak_fullui_20260110T070800Z:215:        <p class="muted">Депозит / конвертация через wallet-api. Авто-детект эндпоинтов по openapi.json.</p>
/opt/logos/www/wallet_dev/app.html.bak_fullui_20260110T070800Z:310:            <button class="secondary" type="button" onclick="window.LOGOS_EXT_WALLET_UI?.tick?.();">Ping wallet-api</button>
/opt/logos/www/wallet_dev/app.js.bak_balances_20260110T091213Z:3:const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/node-api'));
/opt/logos/www/wallet_dev/app.js.bak_balances_20260110T091213Z:404:/* ====== LOGOS_EXT_WALLET_UI (wallet-api balances) ====== */
/opt/logos/www/wallet_dev/app.js.bak_balances_20260110T091213Z:407:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/app.js.bak_balances_20260110T091213Z:571:/* ====== LOGOS_BRIDGE_UI_BIND (auto-detect bridge endpoints from wallet-api openapi) ====== */
/opt/logos/www/wallet_dev/app.js.bak_balances_20260110T091213Z:574:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/app.js.bak_tabs_20260111T110230Z:94:    $("api").textContent = window.API_BASE || "/api";
/opt/logos/www/wallet_dev/app.js.bak_tabs_20260111T110230Z:100:      const { r, ms } = await jfetch((window.API_BASE||"/api") + "/balance/" + encodeURIComponent(rid));
/opt/logos/www/wallet_dev/app.js.bak_tabs_20260111T110230Z:116:      setStatus("ERR node-api: " + (e && e.message ? e.message : String(e)));
/opt/logos/www/wallet_dev/app.js.bak_tabs_20260111T110230Z:121:      const { r } = await jfetch((window.WALLET_API||"/wallet-api") + "/v1/receive/" + encodeURIComponent(rid));
/opt/logos/www/wallet_dev/app.js.bak_tabs_20260111T110230Z:128:      $("recvBox").innerHTML = '<div class="muted">ERR wallet-api receive: ' + escapeHtml(e.message||String(e)) + '</div>';
/opt/logos/www/wallet_dev/app.js.bak_tabs_20260111T110230Z:133:      const { r } = await jfetch((window.WALLET_API||"/wallet-api") + "/v1/balances/" + encodeURIComponent(rid));
/opt/logos/www/wallet_dev/app.js.bak_tabs_20260111T110230Z:140:      $("extBalBox").innerHTML = '<div class="muted">ERR wallet-api balances: ' + escapeHtml(e.message||String(e)) + '</div>';
/opt/logos/www/wallet_dev/app.js.bak_tabs_20260111T110230Z:171:      const { r } = await jfetch((window.WALLET_API||"/wallet-api") + "/v1/topup/request", {
/opt/logos/www/wallet_dev/app.js.bak_tabs_20260111T110230Z:195:      const { r } = await jfetch((window.WALLET_API||"/wallet-api") + "/v1/quote", {
/opt/logos/www/wallet_dev/app.js.bak_tabs_20260111T110230Z:227:      const { r } = await jfetch((window.WALLET_API||"/wallet-api") + "/v1/withdraw", {
/opt/logos/www/wallet_dev/api_base.js.bak_routes_20260111T072318Z:4:  // node backend (nginx /api -> 127.0.0.1:8080)
/opt/logos/www/wallet_dev/api_base.js.bak_routes_20260111T072318Z:5:  window.LOGOS_NODE_API   = origin + "/api";
/opt/logos/www/wallet_dev/api_base.js.bak_routes_20260111T072318Z:8:  window.LOGOS_WALLET_API = origin + "/wallet-api";
/opt/logos/www/wallet_dev/api_base.js.bak_routes_20260111T072318Z:11:  window.NODE_API   = "/api";
/opt/logos/www/wallet_dev/api_base.js.bak_routes_20260111T072318Z:12:  window.API_BASE   = "/api";
/opt/logos/www/wallet_dev/api_base.js.bak_routes_20260111T072318Z:13:  window.WALLET_API = "/wallet-api";
/opt/logos/www/wallet_dev/app.html.bak_nacl_20260110T115935Z:13:  <script src="./api_base.js?v=20260110_01"></script>
/opt/logos/www/wallet_dev/app.html.bak_nacl_20260110T115935Z:34:        <div class="pill">API: <span id="endpoint" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/app.html.bak_nacl_20260110T115935Z:133:            <p class="muted">BTC/ETH/TRON/USDT адреса закреплены за RID (wallet-api). Просто копируй и принимай.</p>
/opt/logos/www/wallet_dev/app.html.bak_nacl_20260110T115935Z:252:          <p class="muted">Пресеты добавим дальше. Сейчас — quote/create через wallet-api openapi.</p>
/opt/logos/www/wallet_dev/app.html.bak_ridinput_20260111T093714Z:13:  <script src="./api_base.js?v=20260111_0723"></script>
/opt/logos/www/wallet_dev/app.html.bak_ridinput_20260111T093714Z:34:        <div class="pill">API: <span id="endpoint" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/app.html.bak_ridinput_20260111T093714Z:135:            <p class="muted">BTC/ETH/TRON/USDT адреса закреплены за RID (wallet-api). Просто копируй и принимай.</p>
/opt/logos/www/wallet_dev/app.html.bak_ridinput_20260111T093714Z:254:          <p class="muted">Пресеты добавим дальше. Сейчас — quote/create через wallet-api openapi.</p>
/opt/logos/www/wallet_dev/app.html.bak_bust2_20260111_081542:13:  <script src="./api_base.js?v=20260111_0723"></script>
/opt/logos/www/wallet_dev/app.html.bak_bust2_20260111_081542:34:        <div class="pill">API: <span id="endpoint" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/app.html.bak_bust2_20260111_081542:135:            <p class="muted">BTC/ETH/TRON/USDT адреса закреплены за RID (wallet-api). Просто копируй и принимай.</p>
/opt/logos/www/wallet_dev/app.html.bak_bust2_20260111_081542:254:          <p class="muted">Пресеты добавим дальше. Сейчас — quote/create через wallet-api openapi.</p>
/opt/logos/www/wallet_dev/app.html.bak_premium_20260109T123537Z:14:  <script src="./api_base.js?v=20260109_01"></script>
/opt/logos/www/wallet_dev/app.html.bak_premium_20260109T123537Z:35:        <div class="pill">API: <span id="endpoint" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/app.html.bak_premium_20260109T123537Z:137:          <p class="muted">Депозит/заявки через wallet-api + автодетект эндпоинтов по openapi.json</p>
/opt/logos/www/wallet_dev/_bak_ui_20260107T101342Z/app.js:3:const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/node-api'));
/opt/logos/www/wallet_dev/_bak_ui_20260107T101342Z/app.html:10:<script src="./api_base.js"></script>
/opt/logos/www/wallet_dev/_bak_ui_20260107T101342Z/app.html:24:        <div class="pill">API: <span id="endpoint" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T091512Z:5:// --- API router: chain endpoints live on /api (node), wallet proxy lives on /wallet-api
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T091512Z:12:    if (p.startsWith("/wallet-api/balance/")) u.pathname = p.replace("/wallet-api/balance/","/api/balance/");
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T091512Z:13:    if (p.startsWith("/wallet-api/v1/balances/")) u.pathname = p.replace("/wallet-api/v1/balances/","/api/balance/");
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T091512Z:14:    if (p.startsWith("/wallet-api/v1/balance/"))  u.pathname = p.replace("/wallet-api/v1/balance/","/api/balance/");
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T091512Z:17:    if (p === "/wallet-api/submit_tx" || p.endsWith("/submit_tx")) u.pathname = "/api/submit_tx";
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T091512Z:20:    if (p.startsWith("/wallet-api/stake/")) u.pathname = p.replace("/wallet-api/stake/","/api/stake/");
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T091512Z:27:const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/node-api'));
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T091512Z:428:/* ====== LOGOS_EXT_WALLET_UI (wallet-api balances) ====== */
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T091512Z:431:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T091512Z:597:/* ====== LOGOS_BRIDGE_UI_BIND (auto-detect bridge endpoints from wallet-api openapi) ====== */
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T091512Z:600:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T091512Z:806:    // balance via NODE API (nginx /api -> node backend)
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T091512Z:807:    const url = "/api/balance/" + encodeURIComponent(rid);
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T091512Z:848:  const API = (window.API_BASE || window.NODE_API || "/api").replace(/\/+$/,'');
/opt/logos/www/wallet_dev/app.html.bak_bust_20260111_074349:13:  <script src="./api_base.js?v=20260111_0723"></script>
/opt/logos/www/wallet_dev/app.html.bak_bust_20260111_074349:34:        <div class="pill">API: <span id="endpoint" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/app.html.bak_bust_20260111_074349:134:            <p class="muted">BTC/ETH/TRON/USDT адреса закреплены за RID (wallet-api). Просто копируй и принимай.</p>
/opt/logos/www/wallet_dev/app.html.bak_bust_20260111_074349:253:          <p class="muted">Пресеты добавим дальше. Сейчас — quote/create через wallet-api openapi.</p>
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T092451Z:5:// --- API router: chain endpoints live on /api (node), wallet proxy lives on /wallet-api
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T092451Z:12:    if (p.startsWith("/wallet-api/balance/")) u.pathname = p.replace("/wallet-api/balance/","/api/balance/");
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T092451Z:13:    if (p.startsWith("/wallet-api/v1/balances/")) u.pathname = p.replace("/wallet-api/v1/balances/","/api/balance/");
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T092451Z:14:    if (p.startsWith("/wallet-api/v1/balance/"))  u.pathname = p.replace("/wallet-api/v1/balance/","/api/balance/");
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T092451Z:17:    if (p === "/wallet-api/submit_tx" || p.endsWith("/submit_tx")) u.pathname = "/api/submit_tx";
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T092451Z:20:    if (p.startsWith("/wallet-api/stake/")) u.pathname = p.replace("/wallet-api/stake/","/api/stake/");
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T092451Z:27:const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/node-api'));
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T092451Z:428:/* ====== LOGOS_EXT_WALLET_UI (wallet-api balances) ====== */
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T092451Z:431:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T092451Z:597:/* ====== LOGOS_BRIDGE_UI_BIND (auto-detect bridge endpoints from wallet-api openapi) ====== */
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T092451Z:600:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T092451Z:806:    // balance via NODE API (nginx /api -> node backend)
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T092451Z:807:    const url = "/api/balance/" + encodeURIComponent(rid);
/opt/logos/www/wallet_dev/app.js.bak_ridui_20260111T092451Z:848:  const API = (window.API_BASE || window.NODE_API || "/api").replace(/\/+$/,'');
/opt/logos/www/wallet_dev/app.html.bak_ridbal_20260110T082857Z:13:  <script src="./api_base.js?v=20260109_30"></script>
/opt/logos/www/wallet_dev/app.html.bak_ridbal_20260110T082857Z:36:        <div class="pill">API: <span id="endpoint" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/app.html.bak_ridbal_20260110T082857Z:124:          <p class="muted">BTC/ETH/TRON/USDT закреплены за RID (wallet-api). Просто копируй и принимай.</p>
/opt/logos/www/wallet_dev/app.html.bak_ridbal_20260110T082857Z:260:          <p class="muted">Quote / Create берём из wallet-api/openapi.json (авто-подхват).</p>
/opt/logos/www/wallet_dev/app.html.bak_tabsfix_20260110T072648Z:14:  <script src="./api_base.js?v=20260109_99"></script>
/opt/logos/www/wallet_dev/app.html.bak_tabsfix_20260110T072648Z:40:        <div class="pill">API: <span id="endpoint" class="mono">/node-api</span></div>
/opt/logos/www/wallet_dev/app.html.bak_tabsfix_20260110T072648Z:125:    <p class="muted">BTC/ETH/TRON/USDT адреса закреплены за RID (wallet-api). Просто копируй и принимай.</p>
/opt/logos/www/wallet_dev/app.html.bak_tabsfix_20260110T072648Z:206:          <p class="muted">Адреса и балансы привязаны к вашему RID через wallet-api.</p>
/opt/logos/www/wallet_dev/app.html.bak_tabsfix_20260110T072648Z:255:        <p class="muted">Транзакция подписывается локально (Ed25519) и отправляется батчем в node-api.</p>
/opt/logos/www/wallet_dev/app.html.bak_tabsfix_20260110T072648Z:313:        <p class="muted">Депозит / конвертация через wallet-api. Авто-детект эндпоинтов по openapi.json.</p>
/opt/logos/www/wallet_dev/app.html.bak_tabsfix_20260110T072648Z:408:            <button class="secondary" type="button" onclick="window.LOGOS_EXT_WALLET_UI?.tick?.();">Ping wallet-api</button>
/opt/logos/www/wallet_dev/app.js.bak_sendfix_20260111T155340Z:145:      mkLine(container, "wallet-api latency", String(j.latency_ms) + " ms", String(j.latency_ms));
/opt/logos/www/wallet_dev/app.js.bak_sendfix_20260111T155340Z:157:    const API_BASE = window.API_BASE || "/api";
/opt/logos/www/wallet_dev/app.js.bak_sendfix_20260111T155340Z:158:    const WALLET_API = window.WALLET_API || "/wallet-api";
/opt/logos/www/wallet_dev/app.js.bak_sendfix_20260111T155340Z:182:      setStatus("ERR node-api: " + (e && e.message ? e.message : String(e)));
/opt/logos/www/wallet_dev/app.js.bak_sendfix_20260111T155340Z:195:      if ($("recvBox")) $("recvBox").innerHTML = '<div class="muted">ERR wallet-api receive: ' + escapeHtml(e.message||String(e)) + '</div>';
/opt/logos/www/wallet_dev/app.js.bak_sendfix_20260111T155340Z:208:      if ($("extBalBox")) $("extBalBox").innerHTML = '<div class="muted">ERR wallet-api balances: ' + escapeHtml(e.message||String(e)) + '</div>';
/opt/logos/www/wallet_dev/app.js.bak_sendfix_20260111T155340Z:240:      const { r } = await jfetch((window.WALLET_API||"/wallet-api") + "/v1/topup/request", {
/opt/logos/www/wallet_dev/app.js.bak_sendfix_20260111T155340Z:270:      const { r } = await jfetch((window.WALLET_API||"/wallet-api") + "/v1/quote", {
/opt/logos/www/wallet_dev/app.js.bak_sendfix_20260111T155340Z:303:      const { r } = await jfetch((window.WALLET_API||"/wallet-api") + "/v1/withdraw", {
/opt/logos/www/wallet_dev/app.js.bak_sendfix_20260111T155340Z:381:    // wallet-api (FastAPI proxy)
/opt/logos/www/wallet_dev/app.js.bak_sendfix_20260111T155340Z:382:    return (window.LOGOS_WALLET_API || window.WALLET_API || (window.location.origin.replace(/\/+$/, "") + "/wallet-api"));
/opt/logos/www/wallet_dev/app.js.bak_sendfix_20260111T155340Z:439:        <div class="muted">Обмен/ввод/вывод через wallet-api. Для обычных людей — без сырого текста.</div>
/opt/logos/www/wallet_dev/auth.html:8:  <script src="./api_base.js?v=1"></script>
/opt/logos/www/wallet_dev/app.html.bak_real_20260112T084410Z:10:    window.API_BASE="/api";            // node backend
/opt/logos/www/wallet_dev/app.html.bak_real_20260112T084410Z:11:    window.WALLET_API="/wallet-api";   // wallet proxy
/opt/logos/www/wallet_dev/app.html.bak_real_20260112T084410Z:18:      <div class="pill">API: <span id="api" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/app.html.bak_real_20260112T084410Z:78:          <div class="muted">BTC/ETH/TRON/USDT адреса закреплены за RID (wallet-api).</div>
/opt/logos/www/wallet_dev/app.html.bak_real_20260112T084410Z:82:            <summary>Details (wallet-api raw)</summary>
/opt/logos/www/wallet_dev/app.html.bak_real_20260112T084410Z:89:          <div class="muted">Баланс внешних сетей (wallet-api).</div>
/opt/logos/www/wallet_dev/app.html.bak_real_20260112T084410Z:93:            <summary>Details (wallet-api raw)</summary>
/opt/logos/www/wallet_dev/app.html.bak_real_20260112T084410Z:105:          <div class="muted">Отправка через wallet-api /v1/withdraw (по OpenAPI: USDT + ETH).</div>
/opt/logos/www/wallet_dev/app.html.bak_real_20260112T084410Z:134:            Для LGN-трансфера нужен endpoint в node-api (например /tx/send). Сейчас у тебя подтверждён только /balance.
/opt/logos/www/wallet_dev/app.html.bak_real_20260112T084410Z:159:          <div class="muted">Получить адрес для пополнения (wallet-api /v1/topup/request).</div>
/opt/logos/www/wallet_dev/app.html.bak_real_20260112T084410Z:176:          <div class="muted">Расчёт курса (wallet-api /v1/quote). amount — integer.</div>
/opt/logos/www/wallet_dev/app.html.bak_real_20260112T084410Z:218:          <div class="muted mono">API_BASE = /api, WALLET_API = /wallet-api</div>
/opt/logos/www/wallet_dev/app.html.bak_tabs_20260111T110230Z:10:    window.API_BASE="/api";            // node backend
/opt/logos/www/wallet_dev/app.html.bak_tabs_20260111T110230Z:11:    window.WALLET_API="/wallet-api";   // wallet proxy
/opt/logos/www/wallet_dev/app.html.bak_tabs_20260111T110230Z:18:      <div class="pill">API: <span id="api" class="mono">/api</span></div>
/opt/logos/www/wallet_dev/app.html.bak_tabs_20260111T110230Z:78:          <div class="muted">BTC/ETH/TRON/USDT адреса закреплены за RID (wallet-api).</div>
/opt/logos/www/wallet_dev/app.html.bak_tabs_20260111T110230Z:82:            <summary>Details (wallet-api raw)</summary>
/opt/logos/www/wallet_dev/app.html.bak_tabs_20260111T110230Z:89:          <div class="muted">Баланс внешних сетей (wallet-api).</div>
/opt/logos/www/wallet_dev/app.html.bak_tabs_20260111T110230Z:93:            <summary>Details (wallet-api raw)</summary>
/opt/logos/www/wallet_dev/app.html.bak_tabs_20260111T110230Z:105:          <div class="muted">Отправка через wallet-api /v1/withdraw (по OpenAPI: USDT + ETH).</div>
/opt/logos/www/wallet_dev/app.html.bak_tabs_20260111T110230Z:134:            Для LGN-трансфера нужен endpoint в node-api (например /tx/send). Сейчас у тебя подтверждён только /balance.
/opt/logos/www/wallet_dev/app.html.bak_tabs_20260111T110230Z:157:          <div class="muted">Получить адрес для пополнения (wallet-api /v1/topup/request).</div>
/opt/logos/www/wallet_dev/app.html.bak_tabs_20260111T110230Z:174:          <div class="muted">Расчёт курса (wallet-api /v1/quote). amount — integer.</div>
/opt/logos/www/wallet_dev/app.html.bak_tabs_20260111T110230Z:216:          <div class="muted mono">API_BASE = /api, WALLET_API = /wallet-api</div>
/opt/logos/www/wallet_dev/app.js.bak_NOW_20260110T114809Z:3:const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/node-api'));
/opt/logos/www/wallet_dev/app.js.bak_NOW_20260110T114809Z:436:/* ====== LOGOS_EXT_WALLET_UI (wallet-api balances) ====== */
/opt/logos/www/wallet_dev/app.js.bak_NOW_20260110T114809Z:439:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/app.js.bak_NOW_20260110T114809Z:603:/* ====== LOGOS_BRIDGE_UI_BIND (auto-detect bridge endpoints from wallet-api openapi) ====== */
/opt/logos/www/wallet_dev/app.js.bak_NOW_20260110T114809Z:606:  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/app.js.bak_NOW_20260110T114809Z:804:    // /node-api balance
/opt/logos/www/wallet_dev/app.js.bak_NOW_20260110T114809Z:834:    const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");
/opt/logos/www/wallet_dev/app.js.bak_NOW_20260110T114809Z:838:    if (!r.ok) throw new Error("wallet-api HTTP " + r.status);
/opt/logos/www/wallet_dev/app.html.bak_renderfix_20260111T085559Z:13:  <script src="./api_base.js?v=20260111_0723"></script>
/opt/logos/www/wallet_dev/app.html.bak_renderfix_20260111T085559Z:34:        <div class="pill">API: <span id="endpoint" class="mono">/api</span></div>
```

---

## NODE API — OPENAPI (if fetched) / INVENTORY (if not)

- node_api_openapi.json: included as file below.

### endpoint inventory (HTTP codes)

```txt
200  http://127.0.0.1:8080/head
404  http://127.0.0.1:8080/health
200  http://127.0.0.1:8080/balance/test
404  http://127.0.0.1:8080/balance/
404  http://127.0.0.1:8080/balance
200  http://127.0.0.1:8080/balance/{rid}
404  http://127.0.0.1:8080/nonce/{rid}
405  http://127.0.0.1:8080/submit_tx
405  http://127.0.0.1:8080/submit_tx_batch
405  http://127.0.0.1:8080/debug_canon
404  http://127.0.0.1:8080/tx/
404  http://127.0.0.1:8080/history/
404  http://127.0.0.1:8080/stake/
```

---

## NGINX FULL DUMP (nginx -T)

```nginx
# configuration file /etc/nginx/nginx.conf:
user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
    worker_connections 4096;
    multi_accept on;
}

http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 4096;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    access_log /var/log/nginx/access.log;
    error_log  /var/log/nginx/error.log warn;

    # ВАЖНО: эти include обязаны быть внутри http{}
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}

# configuration file /etc/nginx/mime.types:

types {
    text/html                                        html htm shtml;
    text/css                                         css;
    text/xml                                         xml;
    image/gif                                        gif;
    image/jpeg                                       jpeg jpg;
    application/javascript                           js;
    application/atom+xml                             atom;
    application/rss+xml                              rss;

    text/mathml                                      mml;
    text/plain                                       txt;
    text/vnd.sun.j2me.app-descriptor                 jad;
    text/vnd.wap.wml                                 wml;
    text/x-component                                 htc;

    image/avif                                       avif;
    image/png                                        png;
    image/svg+xml                                    svg svgz;
    image/tiff                                       tif tiff;
    image/vnd.wap.wbmp                               wbmp;
    image/webp                                       webp;
    image/x-icon                                     ico;
    image/x-jng                                      jng;
    image/x-ms-bmp                                   bmp;

    font/woff                                        woff;
    font/woff2                                       woff2;

    application/java-archive                         jar war ear;
    application/json                                 json;
    application/mac-binhex40                         hqx;
    application/msword                               doc;
    application/pdf                                  pdf;
    application/postscript                           ps eps ai;
    application/rtf                                  rtf;
    application/vnd.apple.mpegurl                    m3u8;
    application/vnd.google-earth.kml+xml             kml;
    application/vnd.google-earth.kmz                 kmz;
    application/vnd.ms-excel                         xls;
    application/vnd.ms-fontobject                    eot;
    application/vnd.ms-powerpoint                    ppt;
    application/vnd.oasis.opendocument.graphics      odg;
    application/vnd.oasis.opendocument.presentation  odp;
    application/vnd.oasis.opendocument.spreadsheet   ods;
    application/vnd.oasis.opendocument.text          odt;
    application/vnd.openxmlformats-officedocument.presentationml.presentation
                                                     pptx;
    application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
                                                     xlsx;
    application/vnd.openxmlformats-officedocument.wordprocessingml.document
                                                     docx;
    application/vnd.wap.wmlc                         wmlc;
    application/wasm                                 wasm;
    application/x-7z-compressed                      7z;
    application/x-cocoa                              cco;
    application/x-java-archive-diff                  jardiff;
    application/x-java-jnlp-file                     jnlp;
    application/x-makeself                           run;
    application/x-perl                               pl pm;
    application/x-pilot                              prc pdb;
    application/x-rar-compressed                     rar;
    application/x-redhat-package-manager             rpm;
    application/x-sea                                sea;
    application/x-shockwave-flash                    swf;
    application/x-stuffit                            sit;
    application/x-tcl                                tcl tk;
    application/x-x509-ca-cert                       der pem crt;
    application/x-xpinstall                          xpi;
    application/xhtml+xml                            xhtml;
    application/xspf+xml                             xspf;
    application/zip                                  zip;

    application/octet-stream                         bin exe dll;
    application/octet-stream                         deb;
    application/octet-stream                         dmg;
    application/octet-stream                         iso img;
    application/octet-stream                         msi msp msm;

    audio/midi                                       mid midi kar;
    audio/mpeg                                       mp3;
    audio/ogg                                        ogg;
    audio/x-m4a                                      m4a;
    audio/x-realaudio                                ra;

    video/3gpp                                       3gpp 3gp;
    video/mp2t                                       ts;
    video/mp4                                        mp4;
    video/mpeg                                       mpeg mpg;
    video/ogg                                        ogv;
    video/quicktime                                  mov;
    video/webm                                       webm;
    video/x-flv                                      flv;
    video/x-m4v                                      m4v;
    video/x-matroska                                 mkv;
    video/x-mng                                      mng;
    video/x-ms-asf                                   asx asf;
    video/x-ms-wmv                                   wmv;
    video/x-msvideo                                  avi;
}

# configuration file /etc/nginx/conf.d/ratelimit.conf:
# === LOGOS LRB — единственное объявление зон ===
# QPS основного API (tx) ~30 r/s, запас 20m
limit_req_zone  $binary_remote_addr  zone=logos_tx_api:20m  rate=30r/s;

# QPS метрик ~5 r/s, маленькая зона
limit_req_zone  $binary_remote_addr  zone=logos_metrics:4m  rate=5r/s;

# Ограничение одновременных коннектов на IP
limit_conn_zone $binary_remote_addr  zone=logos_conn_api:10m;

# configuration file /etc/nginx/sites-enabled/logos-node-8000.conf:
server {
    listen 8000;
    server_name _;
    # если будете раздавать фронт-кошелёк со статикой — пропишите root
    # root /var/www/wallet;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# configuration file /etc/nginx/sites-enabled/logos.conf:
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
        try_files $uri $uri/ /wallet_dev/index.html;
        add_header Cache-Control "no-store" always;
        add_header Content-Security-Policy "default-src 'self'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/node-api https://mw-expedition.com/wallet-api; img-src 'self' data:; font-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline';" always;
    }

    location ^~ /wallet/ {
        try_files $uri /wallet/index.html;
        add_header Cache-Control "no-store" always;
        add_header Content-Security-Policy "default-src 'self'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/node-api https://mw-expedition.com/wallet-api; img-src 'self' data:; font-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline';" always;
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

---

## SYSTEMD UNITS

### logos-node@main

```ini
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
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=read-only
PrivateDevices=yes
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
PrivateTmp=true
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

### logos-wallet-proxy

```ini
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

### lrb-proxy

```ini
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

### lrb-scanner

```ini
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

---

## JOURNAL LOGS (last 200 lines)

### logos-node@main

```txt
Jan 06 03:42:24 vm15330919.example.com systemd[1]: Stopping logos-node@main.service - LOGOS LRB Node (main)...
Jan 06 03:42:24 vm15330919.example.com systemd[1]: logos-node@main.service: Deactivated successfully.
Jan 06 03:42:24 vm15330919.example.com systemd[1]: Stopped logos-node@main.service - LOGOS LRB Node (main).
Jan 06 03:42:24 vm15330919.example.com systemd[1]: logos-node@main.service: Consumed 1min 23.700s CPU time.
Jan 06 03:43:30 vm15330919.example.com systemd[1]: Started logos-node@main.service - LOGOS LRB Node (main).
Jan 06 03:43:32 vm15330919.example.com logos_node[971758]: 2026-01-06T03:43:32.019696Z  WARN logos_node: archive disabled
Jan 06 03:43:32 vm15330919.example.com logos_node[971758]: 2026-01-06T03:43:32.019763Z  INFO logos_node: producer start
Jan 06 03:43:32 vm15330919.example.com logos_node[971758]: 2026-01-06T03:43:32.019779Z  INFO logos_node::producer: producer: local block production is disabled in this build; node operates as follower (ledger + archive + bridge).
Jan 06 03:43:32 vm15330919.example.com logos_node[971758]: 2026-01-06T03:43:32.019927Z  INFO logos_node: logos_node listening on 0.0.0.0:8080
Jan 06 06:53:19 vm15330919.example.com systemd[1]: /etc/systemd/system/logos-node@.service:21: System call ~keyctl is not known, ignoring.
Jan 06 06:53:19 vm15330919.example.com systemd[1]: /etc/systemd/system/logos-node@.service.d/10-restart-policy.conf:4: Unknown key name 'StartLimitIntervalSec' in section 'Service', ignoring.
Jan 06 06:53:39 vm15330919.example.com systemd[1]: /etc/systemd/system/logos-node@.service:21: System call ~keyctl is not known, ignoring.
Jan 06 06:53:39 vm15330919.example.com systemd[1]: /etc/systemd/system/logos-node@.service.d/10-restart-policy.conf:4: Unknown key name 'StartLimitIntervalSec' in section 'Service', ignoring.
Jan 06 09:30:38 vm15330919.example.com systemd[1]: /etc/systemd/system/logos-node@.service:21: System call ~keyctl is not known, ignoring.
Jan 06 09:30:38 vm15330919.example.com systemd[1]: /etc/systemd/system/logos-node@.service.d/10-restart-policy.conf:4: Unknown key name 'StartLimitIntervalSec' in section 'Service', ignoring.
Jan 06 09:30:50 vm15330919.example.com systemd[1]: /etc/systemd/system/logos-node@.service:21: System call ~keyctl is not known, ignoring.
Jan 06 09:30:50 vm15330919.example.com systemd[1]: /etc/systemd/system/logos-node@.service.d/10-restart-policy.conf:4: Unknown key name 'StartLimitIntervalSec' in section 'Service', ignoring.
Jan 06 09:52:35 vm15330919.example.com systemd[1]: /etc/systemd/system/logos-node@.service:21: System call ~keyctl is not known, ignoring.
Jan 06 09:52:35 vm15330919.example.com systemd[1]: /etc/systemd/system/logos-node@.service.d/10-restart-policy.conf:4: Unknown key name 'StartLimitIntervalSec' in section 'Service', ignoring.
Jan 06 09:52:44 vm15330919.example.com systemd[1]: /etc/systemd/system/logos-node@.service:21: System call ~keyctl is not known, ignoring.
Jan 06 09:52:44 vm15330919.example.com systemd[1]: /etc/systemd/system/logos-node@.service.d/10-restart-policy.conf:4: Unknown key name 'StartLimitIntervalSec' in section 'Service', ignoring.
Jan 06 10:23:03 vm15330919.example.com systemd[1]: /etc/systemd/system/logos-node@.service:21: System call ~keyctl is not known, ignoring.
Jan 06 10:23:03 vm15330919.example.com systemd[1]: /etc/systemd/system/logos-node@.service.d/10-restart-policy.conf:4: Unknown key name 'StartLimitIntervalSec' in section 'Service', ignoring.
Jan 06 12:00:28 vm15330919.example.com systemd[1]: /etc/systemd/system/logos-node@.service:21: System call ~keyctl is not known, ignoring.
Jan 06 12:00:28 vm15330919.example.com systemd[1]: /etc/systemd/system/logos-node@.service.d/10-restart-policy.conf:4: Unknown key name 'StartLimitIntervalSec' in section 'Service', ignoring.
Jan 06 12:08:53 vm15330919.example.com systemd[1]: /etc/systemd/system/logos-node@.service:21: System call ~keyctl is not known, ignoring.
Jan 06 12:08:53 vm15330919.example.com systemd[1]: /etc/systemd/system/logos-node@.service.d/10-restart-policy.conf:4: Unknown key name 'StartLimitIntervalSec' in section 'Service', ignoring.
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
```

### logos-wallet-proxy

```txt
Jan 10 12:08:11 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 12:08:26 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 12:08:41 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 12:08:56 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 12:09:12 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 12:09:27 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 12:10:14 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 12:11:15 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 12:12:15 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 12:13:15 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 12:14:15 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 12:15:15 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 12:16:15 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 12:17:14 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 12:18:14 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 12:19:14 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 12:20:14 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 12:21:15 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 12:22:15 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:22:07 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:22:23 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:22:37 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:22:52 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:23:08 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:23:22 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:23:37 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:23:52 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:24:14 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:25:14 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:26:15 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:27:15 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:27:50 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:27:52 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:28:07 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:28:22 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:28:38 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:28:52 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:29:14 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:30:15 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:31:15 vm15330919.example.com uvicorn[1101248]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
Jan 10 13:32:15 vm15330919.example.com uvicorn[1101247]: INFO:     77.91.123.72:0 - "GET /v1/balances/AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt HTTP/1.1" 200 OK
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
```

### lrb-proxy

```txt
Jan 06 10:57:22 vm15330919.example.com uvicorn[2941549]: INFO:     127.0.0.1:50440 - "GET / HTTP/1.1" 200 OK
Jan 06 10:57:22 vm15330919.example.com uvicorn[2941549]: INFO:     45.159.248.232:0 - "GET / HTTP/1.1" 200 OK
Jan 06 11:12:08 vm15330919.example.com uvicorn[2941550]: INFO:     45.159.248.232:0 - "GET /v1/receive/RID_HERE HTTP/1.1" 404 Not Found
Jan 06 11:30:25 vm15330919.example.com uvicorn[2941549]: INFO:     127.0.0.1:45884 - "GET /openapi.json HTTP/1.1" 200 OK
Jan 06 11:30:25 vm15330919.example.com uvicorn[2941550]: INFO:     127.0.0.1:45886 - "GET /v1/receive/RID_HERE HTTP/1.1" 404 Not Found
Jan 06 11:30:44 vm15330919.example.com uvicorn[2941550]: INFO:     45.159.248.232:0 - "GET / HTTP/1.1" 200 OK
Jan 06 11:30:44 vm15330919.example.com uvicorn[2941550]: INFO:     45.159.248.232:0 - "GET /openapi.json HTTP/1.1" 200 OK
Jan 06 11:30:44 vm15330919.example.com uvicorn[2941550]: INFO:     45.159.248.232:0 - "GET /api/v1/receive/RID_HERE HTTP/1.1" 404 Not Found
Jan 06 11:38:03 vm15330919.example.com uvicorn[2941549]: INFO:     127.0.0.1:37948 - "GET /openapi.json HTTP/1.1" 200 OK
Jan 06 11:38:03 vm15330919.example.com uvicorn[2941549]: INFO:     127.0.0.1:37958 - "GET /v1/receive/RID_HERE HTTP/1.1" 404 Not Found
Jan 06 11:38:23 vm15330919.example.com uvicorn[2941549]: INFO:     45.159.248.232:0 - "GET /v1/receive/RID_HERE HTTP/1.1" 404 Not Found
Jan 06 11:39:14 vm15330919.example.com uvicorn[2941549]: INFO:     127.0.0.1:45928 - "GET /openapi.json HTTP/1.1" 200 OK
Jan 06 11:53:36 vm15330919.example.com systemd[1]: lrb-proxy.service: Main process exited, code=killed, status=9/KILL
Jan 06 11:53:37 vm15330919.example.com systemd[1]: lrb-proxy.service: Failed with result 'signal'.
Jan 06 11:53:37 vm15330919.example.com systemd[1]: lrb-proxy.service: Consumed 4h 46min 8.643s CPU time, 164.5M memory peak, 157.7M memory swap peak.
Jan 06 11:53:39 vm15330919.example.com systemd[1]: lrb-proxy.service: Scheduled restart job, restart counter is at 1.
Jan 06 11:53:39 vm15330919.example.com systemd[1]: Started lrb-proxy.service - LOGOS Wallet Proxy (FastAPI on :9090).
Jan 06 11:53:39 vm15330919.example.com uvicorn[1017299]: INFO:     Uvicorn running on http://0.0.0.0:9090 (Press CTRL+C to quit)
Jan 06 11:53:39 vm15330919.example.com uvicorn[1017299]: INFO:     Started parent process [1017299]
Jan 06 11:53:43 vm15330919.example.com uvicorn[1017302]: INFO:     Started server process [1017302]
Jan 06 11:53:43 vm15330919.example.com uvicorn[1017302]: INFO:     Waiting for application startup.
Jan 06 11:53:43 vm15330919.example.com uvicorn[1017302]: INFO:     Application startup complete.
Jan 06 11:53:43 vm15330919.example.com uvicorn[1017301]: INFO:     Started server process [1017301]
Jan 06 11:53:43 vm15330919.example.com uvicorn[1017301]: INFO:     Waiting for application startup.
Jan 06 11:53:43 vm15330919.example.com uvicorn[1017301]: INFO:     Application startup complete.
Jan 06 11:54:09 vm15330919.example.com uvicorn[1017302]: INFO Web3 connected: 0xdAC17F958D2ee523a2206206994597C13D831ec7
Jan 06 11:54:09 vm15330919.example.com uvicorn[1017302]: INFO:     127.0.0.1:39160 - "GET /openapi.json HTTP/1.1" 200 OK
Jan 06 11:55:07 vm15330919.example.com uvicorn[1017302]: INFO:     127.0.0.1:47438 - "GET /v1/receive/RID_HERE HTTP/1.1" 500 Internal Server Error
Jan 06 11:55:26 vm15330919.example.com uvicorn[1017301]: INFO Web3 connected: 0xdAC17F958D2ee523a2206206994597C13D831ec7
Jan 06 11:55:26 vm15330919.example.com uvicorn[1017301]: INFO:     45.159.248.232:0 - "GET /v1/receive/RID_HERE HTTP/1.1" 500 Internal Server Error
Jan 06 12:00:53 vm15330919.example.com uvicorn[1017301]: INFO:     127.0.0.1:44288 - "GET /v1/receive/RID_HERE HTTP/1.1" 500 Internal Server Error
Jan 06 12:01:11 vm15330919.example.com uvicorn[1017301]: INFO:     45.159.248.232:0 - "GET /v1/receive/RID_HERE HTTP/1.1" 500 Internal Server Error
Jan 06 12:09:14 vm15330919.example.com uvicorn[1017301]: INFO:     127.0.0.1:38242 - "GET /v1/receive/RID_HERE HTTP/1.1" 500 Internal Server Error
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
```

### lrb-scanner

```txt
Jan 13 11:19:37 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:37 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:37 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:37 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:37 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:37 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:37 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:37 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:37 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:37 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:37 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:37 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:37 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:37 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:37 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:37 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:37 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:37 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:37 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:37 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:37 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:37 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:37 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:37 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:37 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:37 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:37 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:37 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:37 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:37 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:37 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:37 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:37 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:37 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:37 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:37 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:37 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:37 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 13 11:19:38 vm15330919.example.com python[2941536]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 13 11:19:38 vm15330919.example.com python[2941536]: FROM kv
Jan 13 11:19:38 vm15330919.example.com python[2941536]: WHERE kv.k = ?]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: [parameters: ('last_scanned_block',)]
Jan 13 11:19:38 vm15330919.example.com python[2941536]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
```

---

## DB DISCOVERY (from env)

```txt
/etc/logos/wallet-proxy.env: WALLET_PROXY_DB_URL=sqlite:////opt/logos/wallet-proxy/wallet_proxy.db
```

---

## FILE INDEX

0001. `/etc/logos/airdrop-api.env`
0002. `/etc/logos/genesis.yaml`
0003. `/etc/logos/keys.env`
0004. `/etc/logos/keys.envy`
0005. `/etc/logos/logos_tg_bot.env`
0006. `/etc/logos/node-a.env`
0007. `/etc/logos/node-b.env`
0008. `/etc/logos/node-c.env`
0009. `/etc/logos/node-main.env`
0010. `/etc/logos/proxy.env`
0011. `/etc/logos/wallet-proxy.env`
0012. `/etc/nginx/conf.d/grafana.conf.off`
0013. `/etc/nginx/conf.d/ratelimit.conf`
0014. `/etc/nginx/nginx.conf`
0015. `/etc/nginx/sites-enabled/logos-node-8000.conf`
0016. `/etc/nginx/sites-enabled/logos.conf`
0017. `/etc/nginx/snippets/fastcgi-php.conf`
0018. `/etc/nginx/snippets/logos.yml`
0019. `/etc/nginx/snippets/logos_bridge_guard.conf`
0020. `/etc/nginx/snippets/snakeoil.conf`
0021. `/etc/systemd/system/alertmanager.service`
0022. `/etc/systemd/system/dbus-org.freedesktop.ModemManager1.service`
0023. `/etc/systemd/system/dbus-org.freedesktop.resolve1.service`
0024. `/etc/systemd/system/dbus-org.freedesktop.thermald.service`
0025. `/etc/systemd/system/dbus-org.freedesktop.timesync1.service`
0026. `/etc/systemd/system/grafana.service`
0027. `/etc/systemd/system/iscsi.service`
0028. `/etc/systemd/system/logos-agent.service`
0029. `/etc/systemd/system/logos-airdrop-api.service`
0030. `/etc/systemd/system/logos-airdrop-tg-bot.service`
0031. `/etc/systemd/system/logos-airdrop-tg-verify.service`
0032. `/etc/systemd/system/logos-guard-bot.service`
0033. `/etc/systemd/system/logos-healthcheck.service`
0034. `/etc/systemd/system/logos-ledger-backup.service`
0035. `/etc/systemd/system/logos-node.service`
0036. `/etc/systemd/system/logos-node.service.d/00-prod.conf`
0037. `/etc/systemd/system/logos-node.service.d/zz-keys.conf.disabled`
0038. `/etc/systemd/system/logos-node@.service`
0039. `/etc/systemd/system/logos-node@.service.d/10-restart-policy.conf`
0040. `/etc/systemd/system/logos-node@.service.d/20-env.conf`
0041. `/etc/systemd/system/logos-node@.service.d/30-hardening.conf`
0042. `/etc/systemd/system/logos-node@.service.d/31-bridge-key.conf`
0043. `/etc/systemd/system/logos-node@.service.d/40-log.conf`
0044. `/etc/systemd/system/logos-node@.service.d/41-faucet.conf`
0045. `/etc/systemd/system/logos-node@.service.d/env.conf`
0046. `/etc/systemd/system/logos-node@.service.d/override.conf`
0047. `/etc/systemd/system/logos-sled-backup.service`
0048. `/etc/systemd/system/logos-snapshot.service`
0049. `/etc/systemd/system/logos-wallet-proxy.service`
0050. `/etc/systemd/system/logos-wallet-proxy.service.d/override.conf`
0051. `/etc/systemd/system/logos-wallet-scanner.service`
0052. `/etc/systemd/system/logos-x-guard.service`
0053. `/etc/systemd/system/logos-x-guard.service.d/override.conf`
0054. `/etc/systemd/system/logos_guard_bot.service`
0055. `/etc/systemd/system/lrb-exporter.service`
0056. `/etc/systemd/system/lrb-proxy.service`
0057. `/etc/systemd/system/lrb-scanner.service`
0058. `/etc/systemd/system/node-exporter.service`
0059. `/etc/systemd/system/prometheus.service`
0060. `/etc/systemd/system/sshd-keygen@.service.d/disable-sshd-keygen-if-cloud-init-active.conf`
0061. `/etc/systemd/system/syslog.service`
0062. `/etc/systemd/system/vmtoolsd.service`
0063. `/opt/logos/wallet-proxy/app.py`
0064. `/opt/logos/wallet-proxy/init_db.py`
0065. `/opt/logos/wallet-proxy/requirements.txt`
0066. `/opt/logos/wallet-proxy/scanner.py`
0067. `/opt/logos/www/shared/airdrop-fix.js`
0068. `/opt/logos/www/shared/airdrop-x.js`
0069. `/opt/logos/www/shared/airdrop.css`
0070. `/opt/logos/www/shared/airdrop.js`
0071. `/opt/logos/www/shared/i18n.js`
0072. `/opt/logos/www/shared/tweetnacl.min.js`
0073. `/opt/logos/www/shared/wallet-theme.css`
0074. `/opt/logos/www/wallet/_bak_bridge_20260107T102635Z/app.css`
0075. `/opt/logos/www/wallet/_bak_bridge_20260107T102635Z/app.html`
0076. `/opt/logos/www/wallet/_bak_bridge_20260107T102635Z/app.js`
0077. `/opt/logos/www/wallet/_bak_bridge_20260107T102822Z/app.css`
0078. `/opt/logos/www/wallet/_bak_bridge_20260107T102822Z/app.html`
0079. `/opt/logos/www/wallet/_bak_bridge_20260107T102822Z/app.js`
0080. `/opt/logos/www/wallet/_bak_entry_20260107T105554Z/index.html`
0081. `/opt/logos/www/wallet/_bak_entry_20260108T142703Z/index.html`
0082. `/opt/logos/www/wallet/_bak_ui_20260107T101342Z/app.css`
0083. `/opt/logos/www/wallet/_bak_ui_20260107T101342Z/app.html`
0084. `/opt/logos/www/wallet/_bak_ui_20260107T101342Z/app.js`
0085. `/opt/logos/www/wallet/api_base.js`
0086. `/opt/logos/www/wallet/app.css`
0087. `/opt/logos/www/wallet/app.html`
0088. `/opt/logos/www/wallet/app.js`
0089. `/opt/logos/www/wallet/auth.css`
0090. `/opt/logos/www/wallet/auth.html`
0091. `/opt/logos/www/wallet/auth.js`
0092. `/opt/logos/www/wallet/compat.js`
0093. `/opt/logos/www/wallet/connect.js`
0094. `/opt/logos/www/wallet/index.html`
0095. `/opt/logos/www/wallet/login.html`
0096. `/opt/logos/www/wallet/ui.js`
0097. `/opt/logos/www/wallet/wallet.css`
0098. `/opt/logos/www/wallet_dev/_bak_bridge_20260107T102635Z/app.css`
0099. `/opt/logos/www/wallet_dev/_bak_bridge_20260107T102635Z/app.html`
0100. `/opt/logos/www/wallet_dev/_bak_bridge_20260107T102635Z/app.js`
0101. `/opt/logos/www/wallet_dev/_bak_bridge_20260107T102822Z/app.css`
0102. `/opt/logos/www/wallet_dev/_bak_bridge_20260107T102822Z/app.html`
0103. `/opt/logos/www/wallet_dev/_bak_bridge_20260107T102822Z/app.js`
0104. `/opt/logos/www/wallet_dev/_bak_entry_20260107T105554Z/index.html`
0105. `/opt/logos/www/wallet_dev/_bak_entry_20260108T142703Z/index.html`
0106. `/opt/logos/www/wallet_dev/_bak_premiumtabs_20260109T063827Z/app.html`
0107. `/opt/logos/www/wallet_dev/_bak_premiumtabs_20260109T063827Z/app.js`
0108. `/opt/logos/www/wallet_dev/_bak_premiumtabs_20260109T063827Z/ui.css`
0109. `/opt/logos/www/wallet_dev/_bak_ui_20260107T101342Z/app.css`
0110. `/opt/logos/www/wallet_dev/_bak_ui_20260107T101342Z/app.html`
0111. `/opt/logos/www/wallet_dev/_bak_ui_20260107T101342Z/app.js`
0112. `/opt/logos/www/wallet_dev/api_base.js`
0113. `/opt/logos/www/wallet_dev/app.css`
0114. `/opt/logos/www/wallet_dev/app.html`
0115. `/opt/logos/www/wallet_dev/app.js`
0116. `/opt/logos/www/wallet_dev/assets.js`
0117. `/opt/logos/www/wallet_dev/auth.css`
0118. `/opt/logos/www/wallet_dev/auth.html`
0119. `/opt/logos/www/wallet_dev/auth.js`
0120. `/opt/logos/www/wallet_dev/compat.js`
0121. `/opt/logos/www/wallet_dev/connect.js`
0122. `/opt/logos/www/wallet_dev/index.html`
0123. `/opt/logos/www/wallet_dev/login.html`
0124. `/opt/logos/www/wallet_dev/modules/send.js`
0125. `/opt/logos/www/wallet_dev/modules/settings.js`
0126. `/opt/logos/www/wallet_dev/modules/tx_redirect.js`
0127. `/opt/logos/www/wallet_dev/tabs.js`
0128. `/opt/logos/www/wallet_dev/ui.css`
0129. `/opt/logos/www/wallet_dev/ui.js`
0130. `/opt/logos/www/wallet_dev/wallet.css`
0131. `/opt/logos/www/wallet_premium/app.html`
0132. `/opt/logos/www/wallet_premium/app.js`
0133. `/opt/logos/www/wallet_premium/i18n.js`
0134. `/opt/logos/www/wallet_premium/premium.css`
0135. `/opt/logos/www/wallet_premium/ui.css`
0136. `/opt/logos/www/wallet_v2/api_base.js`
0137. `/opt/logos/www/wallet_v2/app.css`
0138. `/opt/logos/www/wallet_v2/app.html`
0139. `/opt/logos/www/wallet_v2/app.js`
0140. `/opt/logos/www/wallet_v2/auth.css`
0141. `/opt/logos/www/wallet_v2/auth.html`
0142. `/opt/logos/www/wallet_v2/auth.js`
0143. `/opt/logos/www/wallet_v2/compat.js`
0144. `/opt/logos/www/wallet_v2/index.html`
0145. `/opt/logos/www/wallet_v2/login.html`
0146. `/opt/logos/www/wallet_v2/ui.js`
0147. `/opt/logos/www/wallet_v2/wallet.css`
0148. `/var/www/logos/explorer/explorer.css`
0149. `/var/www/logos/explorer/explorer.js`
0150. `/var/www/logos/explorer/index.html`
0151. `/var/www/logos/wallet/app.html`
0152. `/var/www/logos/wallet/app.js`
0153. `/var/www/logos/wallet/app.v2.js`
0154. `/var/www/logos/wallet/app.v3.js`
0155. `/var/www/logos/wallet/auth.js`
0156. `/var/www/logos/wallet/css/styles.css`
0157. `/var/www/logos/wallet/index.html`
0158. `/var/www/logos/wallet/js/api.js`
0159. `/var/www/logos/wallet/js/app.js`
0160. `/var/www/logos/wallet/js/app_wallet.js`
0161. `/var/www/logos/wallet/js/core.js`
0162. `/var/www/logos/wallet/js/unlock.js`
0163. `/var/www/logos/wallet/js/vault.js`
0164. `/var/www/logos/wallet/js/vault_bridge.js`
0165. `/var/www/logos/wallet/login.html`
0166. `/var/www/logos/wallet/ping.html`
0167. `/var/www/logos/wallet/staking.js`
0168. `/var/www/logos/wallet/wallet.css`
0169. `/var/www/logos/wallet/wallet.js`
0170. `/var/www/logos/wallet3/app.v3.js`
0171. `/var/www/logos/wallet3/index.html`
0172. `docs/WALLET_PERIMETER_FULL_V2/node_api_openapi.json`
0173. `docs/WALLET_PERIMETER_FULL_V2/wallet_api_openapi.json`

---

## FILE: /etc/logos/airdrop-api.env

- bytes: 1608
- sha256: `c5b970d18f1a4a9983ff1c3070f8e24de110fdfe388b2b247a31da75c29332ae`

```env
AIRDROP_API_KEY=REDACTED

# Postgres DSN
AIRDROP_DB_DSN=postgresql://logos_airdrop:SUPER_STRONG_PASS@127.0.0.1:5432/logos_airdrop

# origin сайта, чтобы referral_url совпадал с фронтом
SITE_ORIGIN=https://mw-expedition.com

# бизнес‑параметры
AIRDROP_REF_TARGET=5

# rate limiting
AIRDROP_RATE_LIMIT_STATUS_PER_IP=120
AIRDROP_RATE_LIMIT_UPDATE_PER_TOKEN=REDACTED
AIRDROP_RATE_LIMIT_UPDATE_PER_IP=120

# пул коннектов
AIRDROP_DB_POOL_MIN=1
AIRDROP_DB_POOL_MAX=10

AIRDROP_PG_DSN=postgresql://logos_airdrop:SUPER_STRONG_PASS@127.0.0.1:5432/logos_airdrop
AIRDROP_X_TOKEN_KEY=REDACTED
X_PROJECT_USERNAME="RspLogos"
X_OAUTH_CLIENT_ID="PUT_CLIENT_ID"
X_OAUTH_CLIENT_SECRET=REDACTED
X_OAUTH_REDIRECT_URI="https://mw-expedition.com/airdrop-api/api/x/oauth/callback"
X_OAUTH_SCOPES="tweet.read users.read follows.read like.read offline.access"

# === X OAuth per-user (TEMP keys; rotate before public launch) ===
X_OAUTH_CLIENT_ID="bUkyakdydHJndDhKOHlva3BoWmg6MTpjaQ"
X_OAUTH_CLIENT_SECRET=REDACTED
X_OAUTH_REDIRECT_URI="https://mw-expedition.com/airdrop-api/api/x/oauth/callback"
X_OAUTH_SCOPES="tweet.read users.read follows.read like.read offline.access"

# Encrypt per-user OAuth tokens in DB
AIRDROP_X_TOKEN_KEY=REDACTED

# What to verify
X_PROJECT_USERNAME="RspLogos"
X_TASK_TWEET_ID="any"
X_TASK_TWEET_ID="2000522761953767743"
X_OAUTH_STATE_TTL=3600
X_OAUTH_COOLDOWN=60
X_OAUTH_STATE_GRACE=600
```

---

## FILE: /etc/logos/genesis.yaml

- bytes: 466
- sha256: `589fb6e0cf841263f98a291e554a4e07c49696625dad069ff2d1bb06dcdcd90a`

```yaml
l0_symbol: "Λ0"
sigma:
  f1: 7.83
  f2: 1.618
  harmonics: [432, 864, 3456]
emission:
  total_lgn: 81000000
fees:
  base_lgn_cost_microunits: 100
  burn_percent: 10
chain_id: "logos-devnet-1"
consensus:
  mode: "solo"
  slot_ms: 1000
  epoch_slots: 60
  genesis_time: "2025-11-10T16:16:02Z"
validators:
  - pubkey: "fcdd4b74cc6f354c44b68c0d73c08c143c80482be510e175351cd74e755c7bae"
    power: 1
    name: "dev-validator-1"
meta:
  name: "logos-devnet"
  version: 1
```

---

## FILE: /etc/logos/keys.env

- bytes: 255
- sha256: `dabcf32f185ebeec833604ce3d20a612bd1ef1b9cc7d9967ed8015de3bc50272`

```env
LRB_ADMIN_KEY=REDACTED
FOUNDER_SK_HEX=07dac25d61dce5d62c4e61b8ba2e3ed949413f7dc983d788e710a13b5471bace
RID_FOUNDER_MAIN=Λ0@7.83Hzφ0.3877
LRB_NODE_SK_HEX=890064b1128dc4c8ada856f6b3d84fb288894f7f9ece26404f48ab8deaf3ea94
```

---

## FILE: /etc/logos/keys.envy

- bytes: 294
- sha256: `f8c8aa68ae9d179cd2b75b1b355baeadfd08c9c0f76c52747f0a852db75486ba`

```envy
LRB_ADMIN_KEY=REDACTED
FOUNDER_SK_HEX=07dac25d61dce5d62c4e61b8ba2e3ed949413f7dc983d788e710a13b5471bace
RID_FOUNDER_MAIN=Λ0@7.83Hzφ0.3877
LRB_NODE_SK_HEX=890064b1128dc4c8ada856f6b3d84fb288894f7f9ece26404f48ab8deaf3ea94
LOGOS_AIRDROP_API_KEY=REDACTED
```

---

## FILE: /etc/logos/logos_tg_bot.env

- bytes: 90
- sha256: `e0ac7dcc0905d3a94cd6c0d7babdb5d55a80e02c69ec8d4f6c77a5c1d72404b7`

```env
LOGOS_TG_BOT_TOKEN=REDACTED
VERIFICATION_TIMEOUT=60
```

---

## FILE: /etc/logos/node-a.env

- bytes: 354
- sha256: `9c1168ec392d0806061b6f969ecf678220989bab80dbd45d601fe419f6f4dc0a`

```env
LRB_NODE_SK_HEX=e3e38ebb671a13acc8c2a218827f8fe1b58d82e163fb27caf80dcc435fa5b139
LRB_ADMIN_KEY=REDACTED
LRB_BRIDGE_KEY=REDACTED
LRB_WALLET_ORIGIN=https://45-159-248-232.sslip.io
LRB_NODE_LISTEN=0.0.0.0:8080
LRB_DATA_DIR=/var/lib/logos-a
RUST_LOG=info
LRB_RATE_BYPASS_CIDR=REDACTED
```

---

## FILE: /etc/logos/node-b.env

- bytes: 354
- sha256: `f4f5fd8c6b03d310e3397ea8e8b0b01691167565a65b5261c6039eb475e1cf29`

```env
LRB_NODE_SK_HEX=0d37088b09fed85dfac6f06e6a009fa76294257fd877412294909dd14d15c822
LRB_ADMIN_KEY=REDACTED
LRB_BRIDGE_KEY=REDACTED
LRB_WALLET_ORIGIN=https://45-159-248-232.sslip.io
LRB_NODE_LISTEN=0.0.0.0:8082
LRB_DATA_DIR=/var/lib/logos-b
RUST_LOG=info
LRB_RATE_BYPASS_CIDR=REDACTED
```

---

## FILE: /etc/logos/node-c.env

- bytes: 354
- sha256: `f56bd211d2bc01d788f12a7e85ce5722209856880e08c528d3b5625d861b647b`

```env
LRB_NODE_SK_HEX=66c3a13e8d67d153127338f135051edfdeb513853e6183477702b253f5f95874
LRB_ADMIN_KEY=REDACTED
LRB_BRIDGE_KEY=REDACTED
LRB_WALLET_ORIGIN=https://45-159-248-232.sslip.io
LRB_NODE_LISTEN=0.0.0.0:8084
LRB_DATA_DIR=/var/lib/logos-c
RUST_LOG=info
LRB_RATE_BYPASS_CIDR=REDACTED
```

---

## FILE: /etc/logos/node-main.env

- bytes: 918
- sha256: `fe2de36fdcb2252d04b1c5f15912e23e589329a7a37b18a82e705a58d4d9ed79`

```env

LOGOS_HTTP_ADDR=127.0.0.1:8080
LRB_HTTP_ADDR=127.0.0.1:8080
LOGOS_ENABLE_METRICS=1
LOGOS_ENABLE_OPENAPI=1
LOGOS_BRIDGE_ENABLE=1
LOGOS_PRODUCER_ENABLE=1
RUST_LOG=info,logos_node=info,lrb=info
LOGOS_GENESIS_PATH=/etc/logos/genesis.yaml
LOGOS_NODE_KEY_PATH=REDACTED
LRB_SLOT_MS=500

# X (Twitter / X) integration for LOGOS X Guard
X_API_KEY=REDACTED
X_API_SECRET=REDACTED
X_BEARER_TOKEN=REDACTED

X_ACCESS_TOKEN=REDACTED
X_ACCESS_TOKEN_SECRET=REDACTED


LRB_JWT_SECRET=REDACTED
LRB_BRIDGE_KEY=REDACTED
LRB_FAUCET_SECRET=REDACTED
```

---

## FILE: /etc/logos/proxy.env

- bytes: 734
- sha256: `a91b9ae3540a2e5e03ff4da3433285c3b10ad6acab880c8590c8e096665db537`

```env
# === LOGOS Wallet Proxy ENV ===

# LRB node connection
LRB_NODE_URL=http://127.0.0.1:8080
LRB_BRIDGE_KEY=REDACTED

# Ethereum provider (Infura mainnet)
ETH_PROVIDER_URL=https://mainnet.infura.io/v3/8b1effbe937f437fbcfd1e89470b63a4
USDT_ERC20_ADDRESS=0xdAC17F958D2ee523a2206206994597C13D831ec7
ETH_CONFIRMATIONS=6

# HD wallet (для депозитных адресов пользователей)
ETH_MNEMONIC=REDACTED

# Hot wallet (для выводов USDT)
ETH_HOT_WALLET_PK=0xd4bdbd56ed355a64495a2c496940b3fb1bd54a0278c8cf39b1a43baf0d034f38

# Proxy service settings
PROXY_HOST=0.0.0.0
PROXY_PORT=9090
```

---

## FILE: /etc/logos/wallet-proxy.env

- bytes: 602
- sha256: `83460dda846c0ee4601df90a17507f2edb0438d70eb1d4942c01c233c7b8ff9d`

```env
BTC_XPUB=zpub6rB41LL2MUYvPdrPNMrgpkUZyKiP2JDHJANGFWs4YhwEWP4f744e9w363B6d8faiovfRNwBPPCBKMxSqiA7kAyfyNTGNDSAKXwyJhP45kkM
ETH_XPUB=xpub6CqSrK5UrPJcfPUJ1WTTztBKacxqV6SA8637Lor6zrwbm3axCszexzcY4VpDZQ4esPqwR83RYozSHFPaE78kHGvY3AyxEPyK79AWs5r9AMi
TRON_XPUB=xpub6BgzjoofH8Qm6N1TbnhPwikBCbYCjZ9inGemDwC346JymmVCfbcL6Rfxrutr232LD8v8rJJX4zpit5QetPS9UbjSQwSckzsupJbxrfMgU3k

LRB_NODE_URL=http://127.0.0.1:8080
LRB_WALLET_CORS=*

# ETH RPC (needed for USDT / ETH)
ETH_PROVIDER_URL=https://mainnet.infura.io/v3/8b1effbe937f437fbcfd1e89470b63a4
WALLET_PROXY_DB_URL=sqlite:////opt/logos/wallet-proxy/wallet_proxy.db
```

---

## FILE: /etc/nginx/conf.d/grafana.conf.off

- bytes: 594
- sha256: `9d89701c4722a3feb3cd0a6bee20e9528b92cd0a3f0a994cdb7fed78ac381e12`

```off
server {
  listen 80;
  server_name _;

  # прокси на grafana, работающую на 3000
  location /grafana/ {
    proxy_pass         http://127.0.0.1:3000/;
    proxy_set_header   Host              $host;
    proxy_set_header   X-Real-IP         $remote_addr;
    proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
    proxy_set_header   X-Forwarded-Proto $scheme;
    proxy_read_timeout 60s;

    # важное правило, чтобы префикс не ломался при редиректах
    proxy_redirect     off;
    sub_filter_once    off;
  }
}
```

---

## FILE: /etc/nginx/conf.d/ratelimit.conf

- bytes: 476
- sha256: `63725e0f010b87fcf1c37255c6be31fe6f16a6453f75e99534d689ff43e22c96`

```conf
# === LOGOS LRB — единственное объявление зон ===
# QPS основного API (tx) ~30 r/s, запас 20m
limit_req_zone  $binary_remote_addr  zone=logos_tx_api:20m  rate=30r/s;

# QPS метрик ~5 r/s, маленькая зона
limit_req_zone  $binary_remote_addr  zone=logos_metrics:4m  rate=5r/s;

# Ограничение одновременных коннектов на IP
limit_conn_zone $binary_remote_addr  zone=logos_conn_api:10m;
```

---

## FILE: /etc/nginx/nginx.conf

- bytes: 609
- sha256: `59e2939963d1ee9fac93e791f52dd478fc0e38dffc61ba3a4f5d2af246f467c5`

```conf
user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
    worker_connections 4096;
    multi_accept on;
}

http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 4096;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    access_log /var/log/nginx/access.log;
    error_log  /var/log/nginx/error.log warn;

    # ВАЖНО: эти include обязаны быть внутри http{}
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

---

## FILE: /etc/nginx/sites-enabled/logos-node-8000.conf

- bytes: 422
- sha256: `d07583b1eb9bdf89ad76218bd6c3effe8409648916437f2eea1bb2dae38a816f`

```conf
server {
    listen 8000;
    server_name _;
    # если будете раздавать фронт-кошелёк со статикой — пропишите root
    # root /var/www/wallet;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## FILE: /etc/nginx/sites-enabled/logos.conf

- bytes: 4687
- sha256: `94d0c49969548172c7af362f6c281635b2a0afb002c7456b835ae338ed74b083`

```conf
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
        try_files $uri $uri/ /wallet_dev/index.html;
        add_header Cache-Control "no-store" always;
        add_header Content-Security-Policy "default-src 'self'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/node-api https://mw-expedition.com/wallet-api; img-src 'self' data:; font-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline';" always;
    }

    location ^~ /wallet/ {
        try_files $uri /wallet/index.html;
        add_header Cache-Control "no-store" always;
        add_header Content-Security-Policy "default-src 'self'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/node-api https://mw-expedition.com/wallet-api; img-src 'self' data:; font-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline';" always;
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

---

## FILE: /etc/nginx/snippets/fastcgi-php.conf

- bytes: 423
- sha256: `a9dd98bf9631d727f0a846a9c7f4fe6193468a714c782df26d5cc9a7756411f2`

```conf
# regex to split $uri to $fastcgi_script_name and $fastcgi_path
fastcgi_split_path_info ^(.+?\.php)(/.*)$;

# Check that the PHP script exists before passing it
try_files $fastcgi_script_name =404;

# Bypass the fact that try_files resets $fastcgi_path_info
# see: http://trac.nginx.org/nginx/ticket/321
set $path_info $fastcgi_path_info;
fastcgi_param PATH_INFO $path_info;

fastcgi_index index.php;
include fastcgi.conf;
```

---

## FILE: /etc/nginx/snippets/logos.yml

- bytes: 815
- sha256: `3604c1eb7572409927e07e037c3a2c4cabf677ab18299c1a32d7c7106372eaee`

```yml
groups:
- name: logos_node
  rules:
  - alert: NodeNotReady
    expr: probe_success{job="logos-readyz"} == 0
    for: 1m
    labels: { severity: critical }
    annotations: { summary: "LOGOS /readyz failing >1m" }

  - alert: HeightStuck
    expr: rate(logos_head_height[5m]) == 0
    for: 5m
    labels: { severity: critical }
    annotations: { summary: "Head не растёт 5 минут" }

  - alert: BridgeFailures
    expr: increase(logos_bridge_ops_total{status=~"failed|payout_failed"}[5m]) > 0
    for: 2m
    labels: { severity: critical }
    annotations: { summary: "Bridge failures >0 за 5 минут" }

  - alert: ArchiveBackpressureHigh
    expr: logos_archive_queue > 1000
    for: 3m
    labels: { severity: warning }
    annotations: { summary: "Archive queue depth high (>1000 3 мин)" }
```

---

## FILE: /etc/nginx/snippets/logos_bridge_guard.conf

- bytes: 150
- sha256: `3ae2650e8ae5c7331b2a98560c591f643d7b03dee7037550f98b9da7b96b762e`

```conf
# Проверка общего секрета для мостовых ручек
if ($http_x_bridge_key != "REDACTED_SHARED_SECRET") { return 401; }
```

---

## FILE: /etc/nginx/snippets/snakeoil.conf

- bytes: 217
- sha256: `69de463039725a6636b5a3ca87a0968dde646279bc8bb4419d200f547448a55a`

```conf
# Self signed certificates generated by the ssl-cert package
# Don't use them in a production server!

ssl_certificate /etc/ssl/certs/ssl-cert-snakeoil.pem;
ssl_certificate_key /etc/ssl/private/ssl-cert-snakeoil.key;
```

---

## FILE: /etc/systemd/system/alertmanager.service

- bytes: 400
- sha256: `ab5a29735bf33ca731364a6c69426c96383e490513bcf9ff805e9ef2a543bb98`

```service
[Unit]
Description=Alertmanager
After=network-online.target

[Service]
EnvironmentFile=/etc/alertmanager/secrets.env
ExecStart=/usr/local/bin/alertmanager \
  --config.file=/etc/alertmanager/alertmanager.yml \
  --storage.path=/var/lib/alertmanager \
  --web.listen-address=127.0.0.1:9093 \
  --cluster.listen-address=127.0.0.1:19094
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
```

---

## FILE: /etc/systemd/system/dbus-org.freedesktop.ModemManager1.service

- bytes: 515
- sha256: `7440e1296cf610dd3847641c2bc93cadf210b4021964d07b7a59b6cf3d5aee06`

```service
[Unit]
Description=Modem Manager
After=polkit.service
Requires=polkit.service
ConditionVirtualization=!container

[Service]
Type=dbus
BusName=org.freedesktop.ModemManager1
ExecStart=/usr/sbin/ModemManager
StandardError=null
Restart=on-abort
CapabilityBoundingSet=CAP_SYS_ADMIN CAP_NET_ADMIN
ProtectSystem=true
ProtectHome=true
PrivateTmp=true
RestrictAddressFamilies=AF_NETLINK AF_UNIX AF_QIPCRTR
NoNewPrivileges=true
User=root

[Install]
WantedBy=multi-user.target
Alias=dbus-org.freedesktop.ModemManager1.service
```

---

## FILE: /etc/systemd/system/dbus-org.freedesktop.resolve1.service

- bytes: 1898
- sha256: `db42a5af326aa171d320a3f18f5137c74025f84bf9fa2e58c5c9db335926c432`

```service
#  SPDX-License-Identifier: LGPL-2.1-or-later
#
#  This file is part of systemd.
#
#  systemd is free software; you can redistribute it and/or modify it
#  under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 2.1 of the License, or
#  (at your option) any later version.

[Unit]
Description=Network Name Resolution
Documentation=man:systemd-resolved.service(8)
Documentation=man:org.freedesktop.resolve1(5)
Documentation=https://www.freedesktop.org/wiki/Software/systemd/writing-network-configuration-managers
Documentation=https://www.freedesktop.org/wiki/Software/systemd/writing-resolver-clients

DefaultDependencies=no
After=systemd-sysctl.service systemd-sysusers.service
Before=sysinit.target network.target nss-lookup.target shutdown.target initrd-switch-root.target
Conflicts=shutdown.target initrd-switch-root.target
Wants=nss-lookup.target

[Service]
AmbientCapabilities=CAP_SETPCAP CAP_NET_RAW CAP_NET_BIND_SERVICE
BusName=org.freedesktop.resolve1
CapabilityBoundingSet=CAP_SETPCAP CAP_NET_RAW CAP_NET_BIND_SERVICE
ExecStart=!!/usr/lib/systemd/systemd-resolved
LockPersonality=yes
MemoryDenyWriteExecute=yes
NoNewPrivileges=yes
PrivateDevices=yes
PrivateTmp=yes
ProtectClock=yes
ProtectControlGroups=yes
ProtectHome=yes
ProtectKernelLogs=yes
ProtectKernelModules=yes
ProtectKernelTunables=yes
ProtectSystem=strict
Restart=always
RestartSec=0
RestrictAddressFamilies=AF_UNIX AF_NETLINK AF_INET AF_INET6
RestrictNamespaces=yes
RestrictRealtime=yes
RestrictSUIDSGID=yes
RuntimeDirectory=systemd/resolve
RuntimeDirectoryPreserve=yes
SystemCallArchitectures=native
SystemCallErrorNumber=EPERM
SystemCallFilter=@system-service
Type=notify
User=systemd-resolve
ImportCredential=network.dns
ImportCredential=network.search_domains
WatchdogSec=3min

[Install]
WantedBy=sysinit.target
Alias=dbus-org.freedesktop.resolve1.service
```

---

## FILE: /etc/systemd/system/dbus-org.freedesktop.thermald.service

- bytes: 309
- sha256: `157f0324b5a9cd68108221584812b4dd6932d9e8a1144f98dc942f713427f1d6`

```service
[Unit]
Description=Thermal Daemon Service
ConditionVirtualization=no

[Service]
Type=dbus
SuccessExitStatus=2
BusName=org.freedesktop.thermald
ExecStart=/usr/sbin/thermald --systemd --dbus-enable --adaptive
Restart=on-failure

[Install]
WantedBy=multi-user.target
Alias=dbus-org.freedesktop.thermald.service
```

---

## FILE: /etc/systemd/system/dbus-org.freedesktop.timesync1.service

- bytes: 1768
- sha256: `f7e5b08e61f52c3fd8fc9d3f96668cc12109499a3e4eb74f0e91cf068e7e063a`

```service
#  SPDX-License-Identifier: LGPL-2.1-or-later
#
#  This file is part of systemd.
#
#  systemd is free software; you can redistribute it and/or modify it
#  under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 2.1 of the License, or
#  (at your option) any later version.

[Unit]
Description=Network Time Synchronization
Documentation=man:systemd-timesyncd.service(8)
ConditionCapability=CAP_SYS_TIME
ConditionVirtualization=!container
DefaultDependencies=no
After=systemd-sysusers.service
Before=time-set.target sysinit.target shutdown.target
Conflicts=shutdown.target
Wants=time-set.target

[Service]
AmbientCapabilities=CAP_SYS_TIME
BusName=org.freedesktop.timesync1
CapabilityBoundingSet=CAP_SYS_TIME
# Turn off DNSSEC validation for hostname look-ups, since those need the
# correct time to work, but we likely won't acquire that without NTP. Let's
# break this chicken-and-egg cycle here.
Environment=SYSTEMD_NSS_RESOLVE_VALIDATE=0
ExecStart=!!/usr/lib/systemd/systemd-timesyncd
LockPersonality=yes
MemoryDenyWriteExecute=yes
NoNewPrivileges=yes
PrivateDevices=yes
PrivateTmp=yes
ProtectProc=invisible
ProtectControlGroups=yes
ProtectHome=yes
ProtectHostname=yes
ProtectKernelLogs=yes
ProtectKernelModules=yes
ProtectKernelTunables=yes
ProtectSystem=strict
Restart=always
RestartSec=0
RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6
RestrictNamespaces=yes
RestrictRealtime=yes
RestrictSUIDSGID=yes
RuntimeDirectory=systemd/timesync
StateDirectory=systemd/timesync
SystemCallArchitectures=native
SystemCallErrorNumber=EPERM
SystemCallFilter=@system-service @clock
Type=notify
User=systemd-timesync
WatchdogSec=3min

[Install]
WantedBy=sysinit.target
Alias=dbus-org.freedesktop.timesync1.service
```

---

## FILE: /etc/systemd/system/grafana.service

- bytes: 333
- sha256: `8937ec1e643084c86a7bf2ae62ca2a6b0dd5789fd1888d91325168f36218bcfa`

```service
[Unit]
Description=Grafana
After=network-online.target

[Service]
User=grafana
Group=grafana
ExecStart=/usr/share/grafana/bin/grafana-server \
  --homepath=/usr/share/grafana \
  --config=/etc/grafana/grafana.ini
WorkingDirectory=/usr/share/grafana
Restart=always
RestartSec=2
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

---

## FILE: /etc/systemd/system/iscsi.service

- bytes: 1003
- sha256: `b3988a2bdeab25498cef62a51e38b1905c9195d91dd55874a25f20061e7b780e`

```service
[Unit]
Description=Login to default iSCSI targets
Documentation=man:iscsiadm(8) man:iscsid(8)
Wants=network-online.target remote-fs-pre.target
After=network-online.target iscsid.service
Before=remote-fs-pre.target
DefaultDependencies=no
Conflicts=shutdown.target
Before=shutdown.target
# Must have some pre-defined targets to login to
ConditionDirectoryNotEmpty=|/etc/iscsi/nodes
# or have a session to use via iscsid
ConditionDirectoryNotEmpty=|/sys/class/iscsi_session

[Service]
Type=oneshot
RemainAfterExit=true
# iscsiadm --login will return 21 if no nodes are configured,
# and 15 if a session is alread logged in (which we do not
# consider an error)
SuccessExitStatus=15 21
# Note: iscsid will be socket activated by iscsiadm
ExecStart=/usr/sbin/iscsiadm -m node --loginall=automatic
ExecStart=/usr/lib/open-iscsi/activate-storage.sh
ExecStop=/usr/lib/open-iscsi/umountiscsi.sh
ExecStop=/bin/sync
ExecStop=/usr/lib/open-iscsi/logout-all.sh

[Install]
WantedBy=sysinit.target
Alias=iscsi.service
```

---

## FILE: /etc/systemd/system/logos-agent.service

- bytes: 290
- sha256: `5f09624dc668c20ccc6192b6b3f804b357a07161beb97b413a1415e1e14ac3b2`

```service
[Unit]
Description=Logos Codex Agent
After=network.target

[Service]
User=logos-agent
Group=logos-agent
EnvironmentFile=/etc/logos-agent.env
ExecStart=/opt/logos-agent/venv/bin/python /opt/logos-agent/agent.py --worker
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

---

## FILE: /etc/systemd/system/logos-airdrop-api.service

- bytes: 617
- sha256: `1a1e38a05ed34a2a8a04ecece5f5356e16d115df090c08f8cfb1f4063989d065`

```service
[Unit]
Description=LOGOS Airdrop API (FastAPI on :8092, Postgres)
After=network.target postgresql.service
Requires=network.target postgresql.service

[Service]
User=logos
Group=logos
WorkingDirectory=/opt/logos/airdrop-api

# Все секреты и DSN лежат здесь
EnvironmentFile=/etc/logos/airdrop-api.env
Environment=PYTHONUNBUFFERED=1

# Uvicorn внутри venv, 4 воркера
ExecStart=/opt/logos/airdrop-api/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 8092 --workers 4 --proxy-headers

Restart=always
RestartSec=3
TimeoutStopSec=20
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
```

---

## FILE: /etc/systemd/system/logos-airdrop-tg-bot.service

- bytes: 926
- sha256: `da28fc4975a69b3b660c620785da727d17b351aed16e5c79da03617509c4c31a`

```service
[Unit]
Description=LOGOS Airdrop Telegram Bot (subscription verifier)
After=network-online.target logos-airdrop-api.service
Wants=network-online.target

[Service]
User=logos
Group=logos
WorkingDirectory=/opt/logos/airdrop-tg-bot

# Никакие ключи не меняем — только подключаем где они лежат
EnvironmentFile=/etc/logos/logos_tg_bot.env
EnvironmentFile=/etc/logos/airdrop-api.env
EnvironmentFile=/etc/logos/node-main.env

Environment=TG_CHANNEL=@logosblockchain
Environment=AIRDROP_UPDATE_URL=http://127.0.0.1:8092/api/airdrop/update
Environment=AIRDROP_API_KEY_HEADER=X-API-Key
Environment=LOG_LEVEL=INFO

ExecStart=/opt/logos/airdrop-tg-bot/.venv/bin/python /opt/logos/airdrop-tg-bot/bot.py

Restart=always
RestartSec=3
TimeoutStopSec=20
LimitNOFILE=65535

StandardOutput=journal
StandardError=journal

NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

---

## FILE: /etc/systemd/system/logos-airdrop-tg-verify.service

- bytes: 595
- sha256: `5b7e99260d59dc6328fee76db1a39e033b5bb01c606fd4f423e38213ef3260ce`

```service
[Unit]
Description=LOGOS Airdrop Telegram Verifier
After=network-online.target logos-airdrop-api.service
Wants=network-online.target

[Service]
User=logos
Group=logos
WorkingDirectory=/opt/logos/airdrop-tg-bot

# Уже настроенные env (не меняем ключи, только подключаем)
EnvironmentFile=/etc/logos/node-main.env
EnvironmentFile=/etc/logos/airdrop-api.env

ExecStart=/opt/logos/airdrop-tg-bot/.venv/bin/python /opt/logos/airdrop-tg-bot/bot.py
Restart=always
RestartSec=2
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

---

## FILE: /etc/systemd/system/logos-guard-bot.service

- bytes: 449
- sha256: `ffe382136d5f7ddf8f4259f10acb141378027a6fd9caf2a306e3966ff319fe82`

```service
[Unit]
Description=LOGOS Guard Telegram Bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/var/www/logos/landing/logos_tg_bot/logos_guard_bot
ExecStart=/var/www/logos/landing/logos_tg_bot/logos_guard_bot/run_bot.sh
Restart=on-failure
RestartSec=5

# позже можно завести отдельного пользователя:
# User=logos
# Group=logos

[Install]
WantedBy=multi-user.target
```

---

## FILE: /etc/systemd/system/logos-healthcheck.service

- bytes: 120
- sha256: `5bac299dba405f179dde817467626bfae947f991335b98310df08ddc5d6fee58`

```service
[Unit]
Description=LOGOS LRB /readyz healthcheck

[Service]
Type=oneshot
ExecStart=/usr/local/bin/logos_readyz_check.sh
```

---

## FILE: /etc/systemd/system/logos-ledger-backup.service

- bytes: 455
- sha256: `f528e4b1d8a24678eadbafa722d55d3dc78819b25470f96619cf8edb6fdadf18`

```service
[Unit]
Description=LOGOS ledger backup (sled snapshot)
Wants=network-online.target
After=network-online.target

[Service]
Type=oneshot
User=root
ExecStart=/bin/bash -c 'set -euo pipefail; TS=$(date -u +%%Y-%%m-%%dT%%H-%%M-%%SZ); \
  systemctl stop logos-node@main; \
  tar -C /var/lib/logos -czf /var/backups/logos/ledger-$TS.tgz data.sled; \
  systemctl start logos-node@main; \
  find /var/backups/logos -type f -name "ledger-*.tgz" -mtime +14 -delete'
```

---

## FILE: /etc/systemd/system/logos-node.service

- bytes: 548
- sha256: `7f89f70ea57019a6dd813b77b9497b1255dcbdc8160e6f3fe09c03dd5f30d572`

```service
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
PrivateTmp=yes
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectControlGroups=yes
ReadWritePaths=/var/lib/logos

# env & secrets
EnvironmentFile=/etc/logos/keys.env
Environment=RUST_LOG=info
[Install]
WantedBy=multi-user.target
```

---

## FILE: /etc/systemd/system/logos-node.service.d/00-prod.conf

- bytes: 540
- sha256: `5f9b8a6caa8142cf868be8f6f6d864d787692d16df3145b5e13c5f4386d34c0f`

```conf
[Service]
Environment=LRB_DATA_PATH=/var/lib/logos/data.sled
Environment=LRB_NODE_LISTEN=127.0.0.1:8080
Environment=LRB_ARCHIVE_URL=postgres://logos:StrongPass123@127.0.0.1:5432/logos
Environment=LRB_WALLET_ORIGIN=https://45-159-248-232.sslip.io
Environment=LRB_SLOT_MS=200
# сгенерируй рандомные секреты:
#  openssl rand -hex 32
Environment=LRB_JWT_SECRET=8e7b2b39d44c4acfa20c7a51a21a4fe1e77b21b2dd4fd8f1c1c6e7bf0a0fbe9c
Environment=LRB_BRIDGE_KEY=6f0d1b3c4e5f6a7b8c9d0e1f2a3b4c5d6e7f8091a2b3c4d5e6f708192a3b4c5d
```

---

## FILE: /etc/systemd/system/logos-node.service.d/zz-keys.conf.disabled

- bytes: 610
- sha256: `2b892056fce012a6a747ecc17dd7d294c3df3ac5b1c704ba8868d7c355fb9769`

```disabled
[Service]
# Читаем файл с секретами (на будущее, если захочешь использовать keys.env)
EnvironmentFile=-/etc/logos/keys.env

# Узловые параметры (жёстко, чтобы сервис точно стартовал)
Environment=LRB_DATA_PATH=/var/lib/logos/data.sled
Environment=LRB_NODE_SK_HEX=31962399e9b0e278af3b328bc6e30bbd17d90c700a5f6c7ad3c4d4418ed8fd83
Environment=LRB_ADMIN_KEY=0448012cf1738fd048b154a1c367cb7cb42e3fee4ab26fb04268ab91e09fb475
Environment=LRB_BRIDGE_KEY=b294771b022226e3a9d6e21f395c7b490a7f42e1fa203cd2fbb62eb3f4718bcf
```

---

## FILE: /etc/systemd/system/logos-node@.service

- bytes: 604
- sha256: `633ece20fd2b41b237b20a4c12b509b74ccd857a48b7cb3a8a831fff936857c9`

```service
[Unit]
Description=LOGOS LRB Node (%i)
After=network-online.target
Wants=network-online.target

[Service]
User=logos
EnvironmentFile=/etc/logos/node-%i.env
ExecStart=/opt/logos/bin/logos_node
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=read-only
PrivateDevices=yes
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
```

---

## FILE: /etc/systemd/system/logos-node@.service.d/10-restart-policy.conf

- bytes: 85
- sha256: `1ea9c7b3ea1ca01ce8fcbac0682d2ade955be8a0d659e5c3c331051c370ea973`

```conf
[Service]
Restart=on-failure
RestartSec=3
StartLimitIntervalSec=60
StartLimitBurst=5
```

---

## FILE: /etc/systemd/system/logos-node@.service.d/20-env.conf

- bytes: 50
- sha256: `8c59efa1bb4a2119976dea4b6879c80b30f22395f26fed98afa97a8b859475eb`

```conf
[Service]
EnvironmentFile=-/etc/logos/node-%i.env
```

---

## FILE: /etc/systemd/system/logos-node@.service.d/30-hardening.conf

- bytes: 581
- sha256: `ac0fb8c4e5ca74cc597f617ad4a562cf7b173d1ebac1c8b11846fc7d14532cd6`

```conf
[Service]
# Sandbox
NoNewPrivileges=true
PrivateTmp=true
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
```

---

## FILE: /etc/systemd/system/logos-node@.service.d/31-bridge-key.conf

- bytes: 49
- sha256: `67afe565857dbd6e6fbb54bb333e9df07266a370a91fb78eddbe6be2e0576dba`

```conf
[Service]
Environment=LRB_BRIDGE_KEY=supersecret
```

---

## FILE: /etc/systemd/system/logos-node@.service.d/40-log.conf

- bytes: 94
- sha256: `b1799914a38b7d00541dbc2f84659773da3fdf5a3928e7fa75f9ea191282c4a5`

```conf
[Service]
Environment=RUST_LOG=trace,logos=trace,consensus=trace,axum=info,h2=info,tokio=info
```

---

## FILE: /etc/systemd/system/logos-node@.service.d/41-faucet.conf

- bytes: 323
- sha256: `ed9e21fe4cd410b6260f6ed692391ea16692f2ff07cf45089cae9f1f9b1e212b`

```conf
[Service]
# Типичные ключи, которые встречаются в таких сборках:
Environment=LOGOS_FAUCET_ENABLED=true
Environment=LRB_FAUCET_ENABLED=true
# (на некоторых билдах есть явный биндинг — пусть будет)
Environment=LOGOS_FAUCET_PATH=/faucet
```

---

## FILE: /etc/systemd/system/logos-node@.service.d/env.conf

- bytes: 288
- sha256: `80d51b476379eebc7b2df8568deaf673a20054f555069518db58a9e8239b726c`

```conf
[Service]
# Per-instance env (например /etc/logos/node-main.env)
EnvironmentFile=/etc/logos/node-%i.env
# Общие секреты (тот самый "keys", чтобы один раз положил — и все инстансы видят)
EnvironmentFile=/etc/logos/keys.env
```

---

## FILE: /etc/systemd/system/logos-node@.service.d/override.conf

- bytes: 121
- sha256: `ff22f4a5ded4e0dd5dd33ed690b813addeb2913cd6ffa658ae3513c37ab8b1cf`

```conf
[Service]
Environment=LOGOS_GENESIS_PATH=/etc/logos/genesis.yaml
Environment=LOGOS_NODE_KEY_PATH=/var/lib/logos/node_key
```

---

## FILE: /etc/systemd/system/logos-sled-backup.service

- bytes: 133
- sha256: `c748a3d215fd6062ec38c3a2ef4f7f969698927deb60666f421122b9fd7b3b3c`

```service
[Unit]
Description=Backup sled to /root/sled_backups

[Service]
Type=oneshot
User=root
ExecStart=/usr/local/bin/logos-sled-backup.sh
```

---

## FILE: /etc/systemd/system/logos-snapshot.service

- bytes: 271
- sha256: `1e1999a9184073503629bd566ab8a66e9a1f55a97c76c500edbdba4ed12429b1`

```service
[Unit]
Description=LOGOS LRB periodic snapshot

[Service]
Type=oneshot
EnvironmentFile=-/etc/logos/keys.env
ExecStart=/usr/bin/curl -s -H "X-Admin-Key: ${LRB_ADMIN_KEY}" \
  http://127.0.0.1:8080/admin/snapshot-file?name=snap-$(date +%%Y%%m%%dT%%H%%M%%S).json >/dev/null
```

---

## FILE: /etc/systemd/system/logos-wallet-proxy.service

- bytes: 459
- sha256: `631da03cb36c599027fb860a65a3530b3ac3c72bcb22906fd9c6ac05f3061b98`

```service
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
```

---

## FILE: /etc/systemd/system/logos-wallet-proxy.service.d/override.conf

- bytes: 244
- sha256: `b1eb69cc7346342ffe5ed6d302d86ca2685aa88b52a2957647fed6852ea5f9a8`

```conf
[Service]
EnvironmentFile=
EnvironmentFile=/etc/logos/wallet-proxy.env

# гарантируем, что таблица есть до старта uvicorn
ExecStartPre=/opt/logos/wallet-proxy/venv/bin/python3 /opt/logos/wallet-proxy/init_db.py
```

---

## FILE: /etc/systemd/system/logos-wallet-scanner.service

- bytes: 480
- sha256: `c160976b98a1eecad4698364e363c540263633dcec881bd19e6ae894dceb4a45`

```service
[Unit]
Description=LOGOS Wallet ETH->LRB USDT Scanner
After=network-online.target
Wants=network-online.target
PartOf=logos-wallet-proxy.service

[Service]
User=logos
Group=logos
WorkingDirectory=/opt/logos/wallet-proxy
EnvironmentFile=/etc/logos/wallet-proxy.env

ExecStart=/opt/logos/wallet-proxy/venv/bin/python /opt/logos/wallet-proxy/scanner.py

Restart=always
RestartSec=5

LimitNOFILE=65535
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

---

## FILE: /etc/systemd/system/logos-x-guard.service

- bytes: 869
- sha256: `2220c5ba1e7c6605418ae64d25c64d8d5e8230a4c61cb511c035733b0ab5896e`

```service
[Unit]
Description=LOGOS X Guard (Twitter airdrop verifier)
After=network-online.target logos-airdrop-api.service
Wants=network-online.target

[Service]
User=logos
Group=logos
WorkingDirectory=/opt/logos

EnvironmentFile=/etc/logos/node-main.env
EnvironmentFile=/etc/logos/airdrop-api.env

# PROD: не светим наружу, nginx/airdrop-api ходят по localhost
Environment=X_GUARD_BIND=127.0.0.1:8091

# Параметры "any лайк/ретвит/пост"
Environment=X_GUARD_RECENT_TWEETS=25
Environment=X_GUARD_USER_POSTS_SCAN=25
Environment=X_GUARD_MAX_PAGES=15
Environment=X_GUARD_TWEETS_CACHE_SEC=60
Environment=X_GUARD_CHECKS_CACHE_SEC=30

ExecStart=/opt/logos/bin/logos_x_guard
Restart=always
RestartSec=2
LimitNOFILE=65535
StandardOutput=journal
StandardError=journal

NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

---

## FILE: /etc/systemd/system/logos-x-guard.service.d/override.conf

- bytes: 198
- sha256: `6ed0fe1d12541f486601f16e67d00dbac01bc5271e93795bd9da50d0765feb73`

```conf
[Service]
Environment=X_GUARD_RECENT_TWEETS=8
Environment=X_GUARD_USER_POSTS_SCAN=8
Environment=X_GUARD_MAX_PAGES=3
Environment=X_GUARD_TWEETS_CACHE_SEC=600
Environment=X_GUARD_CHECKS_CACHE_SEC=180
```

---

## FILE: /etc/systemd/system/logos_guard_bot.service

- bytes: 360
- sha256: `a13e394a3c3cac37bb62c908a841a91be4bc528a6b136d779f37dd6045807f0f`

```service
[Unit]
Description=LOGOS Guard Telegram Bot
After=network.target

[Service]
Type=simple
WorkingDirectory=/var/www/logos/landing/logos_tg_bot/logos_guard_bot
ExecStart=/bin/bash /var/www/logos/landing/logos_tg_bot/logos_guard_bot/run_bot.sh
Restart=always
RestartSec=5
User=root
Group=root
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
```

---

## FILE: /etc/systemd/system/lrb-exporter.service

- bytes: 148
- sha256: `78ea1f21ca92506814a0d5df766f272ad2c3340fe20cb06cd43ef5042564220e`

```service
[Unit]
Description=LRB textfile exporter (economy/head)

[Service]
Type=oneshot
ExecStart=/usr/local/bin/lrb_exporter.sh
User=nodeexp
Group=nodeexp
```

---

## FILE: /etc/systemd/system/lrb-proxy.service

- bytes: 395
- sha256: `008a54ec09d2166ef931ca63217e135d2607554612bf3728349e5ed51acdd2ed`

```service
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

---

## FILE: /etc/systemd/system/lrb-scanner.service

- bytes: 378
- sha256: `35cc469a929a0f5f0f25595eb54597cce9af8ac33fc8dc7b6da82dc62cf8c260`

```service
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

---

## FILE: /etc/systemd/system/node-exporter.service

- bytes: 284
- sha256: `4ce6fd56ce4ba912f7fddbab2d51cce274aae90c754d4d83338f0ed4fb75ca2a`

```service
[Unit]
Description=Node Exporter (Prometheus)
After=network-online.target

[Service]
User=nodeexp
Group=nodeexp
ExecStart=/usr/local/bin/node_exporter \
  --collector.textfile.directory=/var/lib/node_exporter/textfile
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
```

---

## FILE: /etc/systemd/system/prometheus.service

- bytes: 352
- sha256: `776c17d67982b2963bceb9b776580bab28908c681dfed039093dcf6f8efc3bb7`

```service
[Unit]
Description=Prometheus
After=network-online.target

[Service]
User=prom
Group=prom
ExecStart=/usr/local/bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/var/lib/prometheus \
  --web.enable-lifecycle \
  --web.listen-address=127.0.0.1:9094
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
```

---

## FILE: /etc/systemd/system/sshd-keygen@.service.d/disable-sshd-keygen-if-cloud-init-active.conf

- bytes: 410
- sha256: `1d435e1d79784e95f1982b534a7c5f79a32fc3b91eda3f6cd67c97d23e0d1346`

```conf
# In some cloud-init enabled images the sshd-keygen template service may race
# with cloud-init during boot causing issues with host key generation.  This
# drop-in config adds a condition to sshd-keygen@.service if it exists and
# prevents the sshd-keygen units from running *if* cloud-init is going to run.
#
[Unit]
ConditionPathExists=!/run/systemd/generator.early/multi-user.target.wants/cloud-init.target
```

---

## FILE: /etc/systemd/system/syslog.service

- bytes: 890
- sha256: `2728f43f3e86d6eb2480d6cbc38a977e185b369c3733351459f40a9fc7581b2c`

```service
[Unit]
Description=System Logging Service
Requires=syslog.socket
Documentation=man:rsyslogd(8)
Documentation=man:rsyslog.conf(5)
Documentation=https://www.rsyslog.com/doc/

[Service]
Type=notify
ExecStartPre=/usr/lib/rsyslog/reload-apparmor-profile
ExecStart=/usr/sbin/rsyslogd -n -iNONE
StandardOutput=null
StandardError=journal
Restart=on-failure

# Increase the default a bit in order to allow many simultaneous
# files to be monitored, we might need a lot of fds.
LimitNOFILE=16384

CapabilityBoundingSet=CAP_BLOCK_SUSPEND CAP_CHOWN CAP_DAC_OVERRIDE CAP_LEASE CAP_NET_ADMIN CAP_NET_BIND_SERVICE CAP_SYS_ADMIN CAP_SYS_RESOURCE CAP_SYSLOG CAP_MAC_ADMIN CAP_SETGID CAP_SETUID
SystemCallFilter=@system-service
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX
NoNewPrivileges=yes
ProtectHome=no
ProtectClock=yes
ProtectHostname=yes

[Install]
WantedBy=multi-user.target
Alias=syslog.service
```

---

## FILE: /etc/systemd/system/vmtoolsd.service

- bytes: 489
- sha256: `8eeef9026c706c3ccca5a0f28bfcdad6fe1fc3fb787cdda17648360743a1b599`

```service
[Unit]
Description=Service for virtual machines hosted on VMware
Documentation=http://open-vm-tools.sourceforge.net/about.php
ConditionVirtualization=vmware
DefaultDependencies=no
Before=cloud-init-local.service
After=vgauth.service
After=apparmor.service
RequiresMountsFor=/tmp
After=systemd-remount-fs.service systemd-tmpfiles-setup.service systemd-modules-load.service

[Service]
ExecStart=/usr/bin/vmtoolsd
TimeoutStopSec=5

[Install]
WantedBy=multi-user.target
Alias=vmtoolsd.service
```

---

## FILE: /opt/logos/wallet-proxy/app.py

- bytes: 20679
- sha256: `7f8b2bfd50782d02a3d79fada39e147c03258e38e45c0894c1987240fa1d6126`

```py
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
ETH_RPC      = os.environ.get("ETH_PROVIDER_URL", "")
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
    token      = Column(String, nullable=False)
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
    token   = Column(String)
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
    token: Literal["USDT"] = "USDT"
    network: Literal["ETH"] = "ETH"

class TopupResponse(BaseModel):
    rid: str
    token: str
    network: str
    address: str

class WithdrawRequest(BaseModel):
    rid: str
    token: Literal["USDT"] = "USDT"
    network: Literal["ETH"] = "ETH"
    amount: int
    to_address: str
    request_id: str

class QuoteRequest(BaseModel):
    from_token: str
    to_token: str
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
                token=token,
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
                    token=req.token,
                    network=req.network,
                    address=deposit_address,
                )
            )
            s.commit()

    return TopupResponse(
        rid=req.rid,
        token=req.token,
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
                    token=req.token,
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

---

## FILE: /opt/logos/wallet-proxy/init_db.py

- bytes: 1607
- sha256: `53cc0c7af17d310a402d4ebcce776f07dfa3f1f5305d07fa4ac91d236471df2f`

```py
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

---

## FILE: /opt/logos/wallet-proxy/requirements.txt

- bytes: 1147
- sha256: `c415c58461a62721a8652b867901b6077d3b2b066a5f02ee38363b9e42575e8b`

```txt
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
SQLAlchemy==2.0.43
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

---

## FILE: /opt/logos/wallet-proxy/scanner.py

- bytes: 5538
- sha256: `85902cb2cd18aaa0377b1345d9e5b9122ad9e12e47e7a94cf0285c8bfde1d1ec`

```py
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
ETH_RPC      = os.environ.get("ETH_PROVIDER_URL", "")
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

---

## FILE: /opt/logos/www/shared/airdrop-fix.js

- bytes: 6704
- sha256: `6e36f506ef3c71a7319a608385a86ef0c9a2d8e032371120d5c1f8459787c660`

```js
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

---

## FILE: /opt/logos/www/shared/airdrop-x.js

- bytes: 2590
- sha256: `9d59d4a57965e770710f796607717e582781be7857aa192d06b0ba8e556a5c44`

```js
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

---

## FILE: /opt/logos/www/shared/airdrop.css

- bytes: 1864
- sha256: `310cde7cd767743bd26264131b2c80f87c754df4b05307ee2b06acd8b102c2b5`

```css
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

---

## FILE: /opt/logos/www/shared/airdrop.js

- bytes: 8118
- sha256: `fce79524431f0251627418191d8dcbb22889d1b0ce7f6bc3cdb1a1aa942b6944`

```js
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

---

## FILE: /opt/logos/www/shared/i18n.js

- bytes: 3124
- sha256: `64b572af7505da8ce2ee450940c6ae94a07ad284d6ecf85105488692f81a9d2c`

```js
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

---

## FILE: /opt/logos/www/shared/tweetnacl.min.js

- bytes: 18456
- sha256: `973cc5733cc7432e30ee4682098f413094f494bccf76a567c23908c5035ddbbc`

```js
!function(i){"use strict";var m=function(r,n){this.hi=0|r,this.lo=0|n},v=function(r){var n,e=new Float64Array(16);if(r)for(n=0;n<r.length;n++)e[n]=r[n];return e},a=function(){throw new Error("no PRNG")},o=new Uint8Array(16),e=new Uint8Array(32);e[0]=9;var c=v(),w=v([1]),g=v([56129,1]),y=v([30883,4953,19914,30187,55467,16705,2637,112,59544,30585,16505,36039,65139,11119,27886,20995]),l=v([61785,9906,39828,60374,45398,33411,5274,224,53552,61171,33010,6542,64743,22239,55772,9222]),t=v([54554,36645,11616,51542,42930,38181,51040,26924,56412,64982,57905,49316,21502,52590,14035,8553]),f=v([26200,26214,26214,26214,26214,26214,26214,26214,26214,26214,26214,26214,26214,26214,26214,26214]),s=v([41136,18958,6951,50414,58488,44335,6150,12099,55207,15867,153,11085,57099,20417,9344,11139]);function h(r,n){return r<<n|r>>>32-n}function b(r,n){var e=255&r[n+3];return(e=(e=e<<8|255&r[n+2])<<8|255&r[n+1])<<8|255&r[n+0]}function B(r,n){var e=r[n]<<24|r[n+1]<<16|r[n+2]<<8|r[n+3],t=r[n+4]<<24|r[n+5]<<16|r[n+6]<<8|r[n+7];return new m(e,t)}function p(r,n,e){var t;for(t=0;t<4;t++)r[n+t]=255&e,e>>>=8}function S(r,n,e){r[n]=e.hi>>24&255,r[n+1]=e.hi>>16&255,r[n+2]=e.hi>>8&255,r[n+3]=255&e.hi,r[n+4]=e.lo>>24&255,r[n+5]=e.lo>>16&255,r[n+6]=e.lo>>8&255,r[n+7]=255&e.lo}function u(r,n,e,t,o){var i,a=0;for(i=0;i<o;i++)a|=r[n+i]^e[t+i];return(1&a-1>>>8)-1}function A(r,n,e,t){return u(r,n,e,t,16)}function _(r,n,e,t){return u(r,n,e,t,32)}function U(r,n,e,t,o){var i,a,f,u=new Uint32Array(16),c=new Uint32Array(16),w=new Uint32Array(16),y=new Uint32Array(4);for(i=0;i<4;i++)c[5*i]=b(t,4*i),c[1+i]=b(e,4*i),c[6+i]=b(n,4*i),c[11+i]=b(e,16+4*i);for(i=0;i<16;i++)w[i]=c[i];for(i=0;i<20;i++){for(a=0;a<4;a++){for(f=0;f<4;f++)y[f]=c[(5*a+4*f)%16];for(y[1]^=h(y[0]+y[3]|0,7),y[2]^=h(y[1]+y[0]|0,9),y[3]^=h(y[2]+y[1]|0,13),y[0]^=h(y[3]+y[2]|0,18),f=0;f<4;f++)u[4*a+(a+f)%4]=y[f]}for(f=0;f<16;f++)c[f]=u[f]}if(o){for(i=0;i<16;i++)c[i]=c[i]+w[i]|0;for(i=0;i<4;i++)c[5*i]=c[5*i]-b(t,4*i)|0,c[6+i]=c[6+i]-b(n,4*i)|0;for(i=0;i<4;i++)p(r,4*i,c[5*i]),p(r,16+4*i,c[6+i])}else for(i=0;i<16;i++)p(r,4*i,c[i]+w[i]|0)}function E(r,n,e,t){U(r,n,e,t,!1)}function x(r,n,e,t){return U(r,n,e,t,!0),0}var d=new Uint8Array([101,120,112,97,110,100,32,51,50,45,98,121,116,101,32,107]);function K(r,n,e,t,o,i,a){var f,u,c=new Uint8Array(16),w=new Uint8Array(64);if(!o)return 0;for(u=0;u<16;u++)c[u]=0;for(u=0;u<8;u++)c[u]=i[u];for(;64<=o;){for(E(w,c,a,d),u=0;u<64;u++)r[n+u]=(e?e[t+u]:0)^w[u];for(f=1,u=8;u<16;u++)f=f+(255&c[u])|0,c[u]=255&f,f>>>=8;o-=64,n+=64,e&&(t+=64)}if(0<o)for(E(w,c,a,d),u=0;u<o;u++)r[n+u]=(e?e[t+u]:0)^w[u];return 0}function Y(r,n,e,t,o){return K(r,n,null,0,e,t,o)}function L(r,n,e,t,o){var i=new Uint8Array(32);return x(i,t,o,d),Y(r,n,e,t.subarray(16),i)}function T(r,n,e,t,o,i,a){var f=new Uint8Array(32);return x(f,i,a,d),K(r,n,e,t,o,i.subarray(16),f)}function k(r,n){var e,t=0;for(e=0;e<17;e++)t=t+(r[e]+n[e]|0)|0,r[e]=255&t,t>>>=8}var z=new Uint32Array([5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,252]);function R(r,n,e,t,o,i){var a,f,u,c,w=new Uint32Array(17),y=new Uint32Array(17),l=new Uint32Array(17),s=new Uint32Array(17),h=new Uint32Array(17);for(u=0;u<17;u++)y[u]=l[u]=0;for(u=0;u<16;u++)y[u]=i[u];for(y[3]&=15,y[4]&=252,y[7]&=15,y[8]&=252,y[11]&=15,y[12]&=252,y[15]&=15;0<o;){for(u=0;u<17;u++)s[u]=0;for(u=0;u<16&&u<o;++u)s[u]=e[t+u];for(s[u]=1,t+=u,o-=u,k(l,s),f=0;f<17;f++)for(u=w[f]=0;u<17;u++)w[f]=w[f]+l[u]*(u<=f?y[f-u]:320*y[f+17-u]|0)|0;for(f=0;f<17;f++)l[f]=w[f];for(u=c=0;u<16;u++)c=c+l[u]|0,l[u]=255&c,c>>>=8;for(c=c+l[16]|0,l[16]=3&c,c=5*(c>>>2)|0,u=0;u<16;u++)c=c+l[u]|0,l[u]=255&c,c>>>=8;c=c+l[16]|0,l[16]=c}for(u=0;u<17;u++)h[u]=l[u];for(k(l,z),a=0|-(l[16]>>>7),u=0;u<17;u++)l[u]^=a&(h[u]^l[u]);for(u=0;u<16;u++)s[u]=i[u+16];for(s[16]=0,k(l,s),u=0;u<16;u++)r[n+u]=l[u];return 0}function P(r,n,e,t,o,i){var a=new Uint8Array(16);return R(a,0,e,t,o,i),A(r,n,a,0)}function M(r,n,e,t,o){var i;if(e<32)return-1;for(T(r,0,n,0,e,t,o),R(r,16,r,32,e-32,r),i=0;i<16;i++)r[i]=0;return 0}function N(r,n,e,t,o){var i,a=new Uint8Array(32);if(e<32)return-1;if(L(a,0,32,t,o),0!==P(n,16,n,32,e-32,a))return-1;for(T(r,0,n,0,e,t,o),i=0;i<32;i++)r[i]=0;return 0}function O(r,n){var e;for(e=0;e<16;e++)r[e]=0|n[e]}function C(r){var n,e;for(e=0;e<16;e++)r[e]+=65536,n=Math.floor(r[e]/65536),r[(e+1)*(e<15?1:0)]+=n-1+37*(n-1)*(15===e?1:0),r[e]-=65536*n}function F(r,n,e){for(var t,o=~(e-1),i=0;i<16;i++)t=o&(r[i]^n[i]),r[i]^=t,n[i]^=t}function Z(r,n){var e,t,o,i=v(),a=v();for(e=0;e<16;e++)a[e]=n[e];for(C(a),C(a),C(a),t=0;t<2;t++){for(i[0]=a[0]-65517,e=1;e<15;e++)i[e]=a[e]-65535-(i[e-1]>>16&1),i[e-1]&=65535;i[15]=a[15]-32767-(i[14]>>16&1),o=i[15]>>16&1,i[14]&=65535,F(a,i,1-o)}for(e=0;e<16;e++)r[2*e]=255&a[e],r[2*e+1]=a[e]>>8}function G(r,n){var e=new Uint8Array(32),t=new Uint8Array(32);return Z(e,r),Z(t,n),_(e,0,t,0)}function q(r){var n=new Uint8Array(32);return Z(n,r),1&n[0]}function D(r,n){var e;for(e=0;e<16;e++)r[e]=n[2*e]+(n[2*e+1]<<8);r[15]&=32767}function I(r,n,e){var t;for(t=0;t<16;t++)r[t]=n[t]+e[t]|0}function V(r,n,e){var t;for(t=0;t<16;t++)r[t]=n[t]-e[t]|0}function X(r,n,e){var t,o,i=new Float64Array(31);for(t=0;t<31;t++)i[t]=0;for(t=0;t<16;t++)for(o=0;o<16;o++)i[t+o]+=n[t]*e[o];for(t=0;t<15;t++)i[t]+=38*i[t+16];for(t=0;t<16;t++)r[t]=i[t];C(r),C(r)}function j(r,n){X(r,n,n)}function H(r,n){var e,t=v();for(e=0;e<16;e++)t[e]=n[e];for(e=253;0<=e;e--)j(t,t),2!==e&&4!==e&&X(t,t,n);for(e=0;e<16;e++)r[e]=t[e]}function J(r,n){var e,t=v();for(e=0;e<16;e++)t[e]=n[e];for(e=250;0<=e;e--)j(t,t),1!==e&&X(t,t,n);for(e=0;e<16;e++)r[e]=t[e]}function Q(r,n,e){var t,o,i=new Uint8Array(32),a=new Float64Array(80),f=v(),u=v(),c=v(),w=v(),y=v(),l=v();for(o=0;o<31;o++)i[o]=n[o];for(i[31]=127&n[31]|64,i[0]&=248,D(a,e),o=0;o<16;o++)u[o]=a[o],w[o]=f[o]=c[o]=0;for(f[0]=w[0]=1,o=254;0<=o;--o)F(f,u,t=i[o>>>3]>>>(7&o)&1),F(c,w,t),I(y,f,c),V(f,f,c),I(c,u,w),V(u,u,w),j(w,y),j(l,f),X(f,c,f),X(c,u,y),I(y,f,c),V(f,f,c),j(u,f),V(c,w,l),X(f,c,g),I(f,f,w),X(c,c,f),X(f,w,l),X(w,u,a),j(u,y),F(f,u,t),F(c,w,t);for(o=0;o<16;o++)a[o+16]=f[o],a[o+32]=c[o],a[o+48]=u[o],a[o+64]=w[o];var s=a.subarray(32),h=a.subarray(16);return H(s,s),X(h,h,s),Z(r,h),0}function W(r,n){return Q(r,n,e)}function $(r,n){return a(n,32),W(r,n)}function rr(r,n,e){var t=new Uint8Array(32);return Q(t,e,n),x(r,o,t,d)}var nr=M,er=N;function tr(){var r,n,e,t=0,o=0,i=0,a=0,f=65535;for(e=0;e<arguments.length;e++)t+=(r=arguments[e].lo)&f,o+=r>>>16,i+=(n=arguments[e].hi)&f,a+=n>>>16;return new m((i+=(o+=t>>>16)>>>16)&f|(a+=i>>>16)<<16,t&f|o<<16)}function or(r,n){return new m(r.hi>>>n,r.lo>>>n|r.hi<<32-n)}function ir(){var r,n=0,e=0;for(r=0;r<arguments.length;r++)n^=arguments[r].lo,e^=arguments[r].hi;return new m(e,n)}function ar(r,n){var e,t,o=32-n;return n<32?(e=r.hi>>>n|r.lo<<o,t=r.lo>>>n|r.hi<<o):n<64&&(e=r.lo>>>n|r.hi<<o,t=r.hi>>>n|r.lo<<o),new m(e,t)}var fr=[new m(1116352408,3609767458),new m(1899447441,602891725),new m(3049323471,3964484399),new m(3921009573,2173295548),new m(961987163,4081628472),new m(1508970993,3053834265),new m(2453635748,2937671579),new m(2870763221,3664609560),new m(3624381080,2734883394),new m(310598401,1164996542),new m(607225278,1323610764),new m(1426881987,3590304994),new m(1925078388,4068182383),new m(2162078206,991336113),new m(2614888103,633803317),new m(3248222580,3479774868),new m(3835390401,2666613458),new m(4022224774,944711139),new m(264347078,2341262773),new m(604807628,2007800933),new m(770255983,1495990901),new m(1249150122,1856431235),new m(1555081692,3175218132),new m(1996064986,2198950837),new m(2554220882,3999719339),new m(2821834349,766784016),new m(2952996808,2566594879),new m(3210313671,3203337956),new m(3336571891,1034457026),new m(3584528711,2466948901),new m(113926993,3758326383),new m(338241895,168717936),new m(666307205,1188179964),new m(773529912,1546045734),new m(1294757372,1522805485),new m(1396182291,2643833823),new m(1695183700,2343527390),new m(1986661051,1014477480),new m(2177026350,1206759142),new m(2456956037,344077627),new m(2730485921,1290863460),new m(2820302411,3158454273),new m(3259730800,3505952657),new m(3345764771,106217008),new m(3516065817,3606008344),new m(3600352804,1432725776),new m(4094571909,1467031594),new m(275423344,851169720),new m(430227734,3100823752),new m(506948616,1363258195),new m(659060556,3750685593),new m(883997877,3785050280),new m(958139571,3318307427),new m(1322822218,3812723403),new m(1537002063,2003034995),new m(1747873779,3602036899),new m(1955562222,1575990012),new m(2024104815,1125592928),new m(2227730452,2716904306),new m(2361852424,442776044),new m(2428436474,593698344),new m(2756734187,3733110249),new m(3204031479,2999351573),new m(3329325298,3815920427),new m(3391569614,3928383900),new m(3515267271,566280711),new m(3940187606,3454069534),new m(4118630271,4000239992),new m(116418474,1914138554),new m(174292421,2731055270),new m(289380356,3203993006),new m(460393269,320620315),new m(685471733,587496836),new m(852142971,1086792851),new m(1017036298,365543100),new m(1126000580,2618297676),new m(1288033470,3409855158),new m(1501505948,4234509866),new m(1607167915,987167468),new m(1816402316,1246189591)];function ur(r,n,e){var t,o,i,a=[],f=[],u=[],c=[];for(o=0;o<8;o++)a[o]=u[o]=B(r,8*o);for(var w,y,l,s,h,v,g,b,p,A,_,U,E,x,d=0;128<=e;){for(o=0;o<16;o++)c[o]=B(n,8*o+d);for(o=0;o<80;o++){for(i=0;i<8;i++)f[i]=u[i];for(t=tr(u[7],ir(ar(x=u[4],14),ar(x,18),ar(x,41)),(p=u[4],A=u[5],_=u[6],0,U=p.hi&A.hi^~p.hi&_.hi,E=p.lo&A.lo^~p.lo&_.lo,new m(U,E)),fr[o],c[o%16]),f[7]=tr(t,ir(ar(b=u[0],28),ar(b,34),ar(b,39)),(l=u[0],s=u[1],h=u[2],0,v=l.hi&s.hi^l.hi&h.hi^s.hi&h.hi,g=l.lo&s.lo^l.lo&h.lo^s.lo&h.lo,new m(v,g))),f[3]=tr(f[3],t),i=0;i<8;i++)u[(i+1)%8]=f[i];if(o%16==15)for(i=0;i<16;i++)c[i]=tr(c[i],c[(i+9)%16],ir(ar(y=c[(i+1)%16],1),ar(y,8),or(y,7)),ir(ar(w=c[(i+14)%16],19),ar(w,61),or(w,6)))}for(o=0;o<8;o++)u[o]=tr(u[o],a[o]),a[o]=u[o];d+=128,e-=128}for(o=0;o<8;o++)S(r,8*o,a[o]);return e}var cr=new Uint8Array([106,9,230,103,243,188,201,8,187,103,174,133,132,202,167,59,60,110,243,114,254,148,248,43,165,79,245,58,95,29,54,241,81,14,82,127,173,230,130,209,155,5,104,140,43,62,108,31,31,131,217,171,251,65,189,107,91,224,205,25,19,126,33,121]);function wr(r,n,e){var t,o=new Uint8Array(64),i=new Uint8Array(256),a=e;for(t=0;t<64;t++)o[t]=cr[t];for(ur(o,n,e),e%=128,t=0;t<256;t++)i[t]=0;for(t=0;t<e;t++)i[t]=n[a-e+t];for(i[e]=128,i[(e=256-128*(e<112?1:0))-9]=0,S(i,e-8,new m(a/536870912|0,a<<3)),ur(o,i,e),t=0;t<64;t++)r[t]=o[t];return 0}function yr(r,n){var e=v(),t=v(),o=v(),i=v(),a=v(),f=v(),u=v(),c=v(),w=v();V(e,r[1],r[0]),V(w,n[1],n[0]),X(e,e,w),I(t,r[0],r[1]),I(w,n[0],n[1]),X(t,t,w),X(o,r[3],n[3]),X(o,o,l),X(i,r[2],n[2]),I(i,i,i),V(a,t,e),V(f,i,o),I(u,i,o),I(c,t,e),X(r[0],a,f),X(r[1],c,u),X(r[2],u,f),X(r[3],a,c)}function lr(r,n,e){var t;for(t=0;t<4;t++)F(r[t],n[t],e)}function sr(r,n){var e=v(),t=v(),o=v();H(o,n[2]),X(e,n[0],o),X(t,n[1],o),Z(r,t),r[31]^=q(e)<<7}function hr(r,n,e){var t,o;for(O(r[0],c),O(r[1],w),O(r[2],w),O(r[3],c),o=255;0<=o;--o)lr(r,n,t=e[o/8|0]>>(7&o)&1),yr(n,r),yr(r,r),lr(r,n,t)}function vr(r,n){var e=[v(),v(),v(),v()];O(e[0],t),O(e[1],f),O(e[2],w),X(e[3],t,f),hr(r,e,n)}function gr(r,n,e){var t,o=new Uint8Array(64),i=[v(),v(),v(),v()];for(e||a(n,32),wr(o,n,32),o[0]&=248,o[31]&=127,o[31]|=64,vr(i,o),sr(r,i),t=0;t<32;t++)n[t+32]=r[t];return 0}var br=new Float64Array([237,211,245,92,26,99,18,88,214,156,247,162,222,249,222,20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16]);function pr(r,n){var e,t,o,i;for(t=63;32<=t;--t){for(e=0,o=t-32,i=t-12;o<i;++o)n[o]+=e-16*n[t]*br[o-(t-32)],e=Math.floor((n[o]+128)/256),n[o]-=256*e;n[o]+=e,n[t]=0}for(o=e=0;o<32;o++)n[o]+=e-(n[31]>>4)*br[o],e=n[o]>>8,n[o]&=255;for(o=0;o<32;o++)n[o]-=e*br[o];for(t=0;t<32;t++)n[t+1]+=n[t]>>8,r[t]=255&n[t]}function Ar(r){var n,e=new Float64Array(64);for(n=0;n<64;n++)e[n]=r[n];for(n=0;n<64;n++)r[n]=0;pr(r,e)}function _r(r,n,e,t){var o,i,a=new Uint8Array(64),f=new Uint8Array(64),u=new Uint8Array(64),c=new Float64Array(64),w=[v(),v(),v(),v()];wr(a,t,32),a[0]&=248,a[31]&=127,a[31]|=64;var y=e+64;for(o=0;o<e;o++)r[64+o]=n[o];for(o=0;o<32;o++)r[32+o]=a[32+o];for(wr(u,r.subarray(32),e+32),Ar(u),vr(w,u),sr(r,w),o=32;o<64;o++)r[o]=t[o];for(wr(f,r,e+64),Ar(f),o=0;o<64;o++)c[o]=0;for(o=0;o<32;o++)c[o]=u[o];for(o=0;o<32;o++)for(i=0;i<32;i++)c[o+i]+=f[o]*a[i];return pr(r.subarray(32),c),y}function Ur(r,n,e,t){var o,i=new Uint8Array(32),a=new Uint8Array(64),f=[v(),v(),v(),v()],u=[v(),v(),v(),v()];if(e<64)return-1;if(function(r,n){var e=v(),t=v(),o=v(),i=v(),a=v(),f=v(),u=v();if(O(r[2],w),D(r[1],n),j(o,r[1]),X(i,o,y),V(o,o,r[2]),I(i,r[2],i),j(a,i),j(f,a),X(u,f,a),X(e,u,o),X(e,e,i),J(e,e),X(e,e,o),X(e,e,i),X(e,e,i),X(r[0],e,i),j(t,r[0]),X(t,t,i),G(t,o)&&X(r[0],r[0],s),j(t,r[0]),X(t,t,i),G(t,o))return 1;q(r[0])===n[31]>>7&&V(r[0],c,r[0]),X(r[3],r[0],r[1])}(u,t))return-1;for(o=0;o<e;o++)r[o]=n[o];for(o=0;o<32;o++)r[o+32]=t[o];if(wr(a,r,e),Ar(a),hr(f,u,a),vr(u,n.subarray(32)),yr(f,u),sr(i,f),e-=64,_(n,0,i,0)){for(o=0;o<e;o++)r[o]=0;return-1}for(o=0;o<e;o++)r[o]=n[o+64];return e}function Er(r,n){if(32!==r.length)throw new Error("bad key size");if(24!==n.length)throw new Error("bad nonce size")}function xr(){for(var r=0;r<arguments.length;r++)if(!(arguments[r]instanceof Uint8Array))throw new TypeError("unexpected type, use Uint8Array")}function dr(r){for(var n=0;n<r.length;n++)r[n]=0}i.lowlevel={crypto_core_hsalsa20:x,crypto_stream_xor:T,crypto_stream:L,crypto_stream_salsa20_xor:K,crypto_stream_salsa20:Y,crypto_onetimeauth:R,crypto_onetimeauth_verify:P,crypto_verify_16:A,crypto_verify_32:_,crypto_secretbox:M,crypto_secretbox_open:N,crypto_scalarmult:Q,crypto_scalarmult_base:W,crypto_box_beforenm:rr,crypto_box_afternm:nr,crypto_box:function(r,n,e,t,o,i){var a=new Uint8Array(32);return rr(a,o,i),nr(r,n,e,t,a)},crypto_box_open:function(r,n,e,t,o,i){var a=new Uint8Array(32);return rr(a,o,i),er(r,n,e,t,a)},crypto_box_keypair:$,crypto_hash:wr,crypto_sign:_r,crypto_sign_keypair:gr,crypto_sign_open:Ur,crypto_secretbox_KEYBYTES:32,crypto_secretbox_NONCEBYTES:24,crypto_secretbox_ZEROBYTES:32,crypto_secretbox_BOXZEROBYTES:16,crypto_scalarmult_BYTES:32,crypto_scalarmult_SCALARBYTES:32,crypto_box_PUBLICKEYBYTES:32,crypto_box_SECRETKEYBYTES:32,crypto_box_BEFORENMBYTES:32,crypto_box_NONCEBYTES:24,crypto_box_ZEROBYTES:32,crypto_box_BOXZEROBYTES:16,crypto_sign_BYTES:64,crypto_sign_PUBLICKEYBYTES:32,crypto_sign_SECRETKEYBYTES:64,crypto_sign_SEEDBYTES:32,crypto_hash_BYTES:64,gf:v,D:y,L:br,pack25519:Z,unpack25519:D,M:X,A:I,S:j,Z:V,pow2523:J,add:yr,set25519:O,modL:pr,scalarmult:hr,scalarbase:vr},i.randomBytes=function(r){var n=new Uint8Array(r);return a(n,r),n},i.secretbox=function(r,n,e){xr(r,n,e),Er(e,n);for(var t=new Uint8Array(32+r.length),o=new Uint8Array(t.length),i=0;i<r.length;i++)t[i+32]=r[i];return M(o,t,t.length,n,e),o.subarray(16)},i.secretbox.open=function(r,n,e){xr(r,n,e),Er(e,n);for(var t=new Uint8Array(16+r.length),o=new Uint8Array(t.length),i=0;i<r.length;i++)t[i+16]=r[i];return t.length<32||0!==N(o,t,t.length,n,e)?null:o.subarray(32)},i.secretbox.keyLength=32,i.secretbox.nonceLength=24,i.secretbox.overheadLength=16,i.scalarMult=function(r,n){if(xr(r,n),32!==r.length)throw new Error("bad n size");if(32!==n.length)throw new Error("bad p size");var e=new Uint8Array(32);return Q(e,r,n),e},i.scalarMult.base=function(r){if(xr(r),32!==r.length)throw new Error("bad n size");var n=new Uint8Array(32);return W(n,r),n},i.scalarMult.scalarLength=32,i.scalarMult.groupElementLength=32,i.box=function(r,n,e,t){var o=i.box.before(e,t);return i.secretbox(r,n,o)},i.box.before=function(r,n){xr(r,n),function(r,n){if(32!==r.length)throw new Error("bad public key size");if(32!==n.length)throw new Error("bad secret key size")}(r,n);var e=new Uint8Array(32);return rr(e,r,n),e},i.box.after=i.secretbox,i.box.open=function(r,n,e,t){var o=i.box.before(e,t);return i.secretbox.open(r,n,o)},i.box.open.after=i.secretbox.open,i.box.keyPair=function(){var r=new Uint8Array(32),n=new Uint8Array(32);return $(r,n),{publicKey:r,secretKey:n}},i.box.keyPair.fromSecretKey=function(r){if(xr(r),32!==r.length)throw new Error("bad secret key size");var n=new Uint8Array(32);return W(n,r),{publicKey:n,secretKey:new Uint8Array(r)}},i.box.publicKeyLength=32,i.box.secretKeyLength=32,i.box.sharedKeyLength=32,i.box.nonceLength=24,i.box.overheadLength=i.secretbox.overheadLength,i.sign=function(r,n){if(xr(r,n),64!==n.length)throw new Error("bad secret key size");var e=new Uint8Array(64+r.length);return _r(e,r,r.length,n),e},i.sign.open=function(r,n){if(xr(r,n),32!==n.length)throw new Error("bad public key size");var e=new Uint8Array(r.length),t=Ur(e,r,r.length,n);if(t<0)return null;for(var o=new Uint8Array(t),i=0;i<o.length;i++)o[i]=e[i];return o},i.sign.detached=function(r,n){for(var e=i.sign(r,n),t=new Uint8Array(64),o=0;o<t.length;o++)t[o]=e[o];return t},i.sign.detached.verify=function(r,n,e){if(xr(r,n,e),64!==n.length)throw new Error("bad signature size");if(32!==e.length)throw new Error("bad public key size");var t,o=new Uint8Array(64+r.length),i=new Uint8Array(64+r.length);for(t=0;t<64;t++)o[t]=n[t];for(t=0;t<r.length;t++)o[t+64]=r[t];return 0<=Ur(i,o,o.length,e)},i.sign.keyPair=function(){var r=new Uint8Array(32),n=new Uint8Array(64);return gr(r,n),{publicKey:r,secretKey:n}},i.sign.keyPair.fromSecretKey=function(r){if(xr(r),64!==r.length)throw new Error("bad secret key size");for(var n=new Uint8Array(32),e=0;e<n.length;e++)n[e]=r[32+e];return{publicKey:n,secretKey:new Uint8Array(r)}},i.sign.keyPair.fromSeed=function(r){if(xr(r),32!==r.length)throw new Error("bad seed size");for(var n=new Uint8Array(32),e=new Uint8Array(64),t=0;t<32;t++)e[t]=r[t];return gr(n,e,!0),{publicKey:n,secretKey:e}},i.sign.publicKeyLength=32,i.sign.secretKeyLength=64,i.sign.seedLength=32,i.sign.signatureLength=64,i.hash=function(r){xr(r);var n=new Uint8Array(64);return wr(n,r,r.length),n},i.hash.hashLength=64,i.verify=function(r,n){return xr(r,n),0!==r.length&&0!==n.length&&(r.length===n.length&&0===u(r,0,n,0,r.length))},i.setPRNG=function(r){a=r},function(){var o="undefined"!=typeof self?self.crypto||self.msCrypto:null;if(o&&o.getRandomValues){i.setPRNG(function(r,n){var e,t=new Uint8Array(n);for(e=0;e<n;e+=65536)o.getRandomValues(t.subarray(e,e+Math.min(n-e,65536)));for(e=0;e<n;e++)r[e]=t[e];dr(t)})}else"undefined"!=typeof require&&(o=require("crypto"))&&o.randomBytes&&i.setPRNG(function(r,n){var e,t=o.randomBytes(n);for(e=0;e<n;e++)r[e]=t[e];dr(t)})}()}("undefined"!=typeof module&&module.exports?module.exports:self.nacl=self.nacl||{});
```

---

## FILE: /opt/logos/www/shared/wallet-theme.css

- bytes: 7700
- sha256: `4ffbb844e24ea3b9df67fab065e6c20e8ac827972078cfcaf36815706c5a6c1a`

```css
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

---

## FILE: /opt/logos/www/wallet/_bak_bridge_20260107T102635Z/app.css

- bytes: 2416
- sha256: `6fe95464e581b9a746887921adbafd7a05e29e260cdb70e0b95e95c87db3ab83`

```css
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


/* ====== External wallets card ====== */
.extWalletCard{ margin-top:16px; }
.extHead{ display:flex; align-items:flex-start; justify-content:space-between; gap:12px; }
.extTitle{ font-weight:700; font-size:16px; letter-spacing:0.2px; }
.extSub{ opacity:.75; font-size:12px; margin-top:2px; }
.extMeta{ display:flex; gap:8px; align-items:center; }
.pill{ padding:6px 10px; border-radius:999px; font-size:12px; border:1px solid rgba(255,255,255,.10); background:rgba(255,255,255,.04); }
.pill.ok{ border-color: rgba(80,255,170,.25); background: rgba(80,255,170,.06); }
.pill.bad{ border-color: rgba(255,100,120,.25); background: rgba(255,100,120,.06); }
.pill.ghost{ opacity:.8; }

.extGrid{ margin-top:12px; display:flex; flex-direction:column; gap:10px; }
.extRow{
  display:grid;
  grid-template-columns: 140px 120px 1fr 78px;
  gap:10px;
  align-items:center;
  padding:10px 10px;
  border-radius:12px;
  border:1px solid rgba(255,255,255,.08);
  background: rgba(0,0,0,.18);
}
.extCoin{ font-weight:650; }
.extAmt{ font-variant-numeric: tabular-nums; opacity:.95; }
.extAddr{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; font-size:12px; opacity:.9; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.btnMini{
  padding:8px 10px;
  border-radius:10px;
  border:1px solid rgba(255,255,255,.10);
  background: rgba(255,255,255,.06);
  cursor:pointer;
}
.btnMini:hover{ background: rgba(255,255,255,.10); }
.extFoot{ display:flex; justify-content:space-between; align-items:center; gap:12px; margin-top:10px; }
.extHint{ opacity:.75; font-size:12px; }
.extSrc{ opacity:.6; font-size:12px; text-align:right; }
/* ====== /External wallets card ====== */
```

---

## FILE: /opt/logos/www/wallet/_bak_bridge_20260107T102635Z/app.html

- bytes: 6358
- sha256: `229e539b9458b5519463197777c9c303d70c248878ecfa8c30ef69e1257850ee`

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta http-equiv="Cache-Control" content="no-store"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Wallet</title>
  <link rel="stylesheet" href="/shared/wallet-themeP260101_01"/>
  <link rel="stylesheet" href="./appP260101_01"/>
<script src="./api_base.js"></script>
<link rel="stylesheet" href="/shared/wallet-theme.css?v=20260101_02"/>
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

<!-- ====== External wallets (wallet-api) ====== -->
<div class="card extWalletCard" id="extWalletCard" style="display:none;">
  <div class="extHead">
    <div>
      <div class="extTitle">External wallets</div>
      <div class="extSub">BTC / ETH / TRX / USDT — on-chain balances (watch-only)</div>
    </div>
    <div class="extMeta">
      <span class="pill" id="extWalletStatus">connecting…</span>
      <span class="pill ghost" id="extWalletLatency">—</span>
    </div>
  </div>

  <div class="extGrid">
    <div class="extRow">
      <div class="extCoin">BTC</div>
      <div class="extAmt" id="bal_btc">—</div>
      <div class="extAddr" id="addr_btc">—</div>
      <button class="btnMini" data-copy="addr_btc">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">ETH</div>
      <div class="extAmt" id="bal_eth">—</div>
      <div class="extAddr" id="addr_eth">—</div>
      <button class="btnMini" data-copy="addr_eth">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">TRX</div>
      <div class="extAmt" id="bal_trx">—</div>
      <div class="extAddr" id="addr_trx">—</div>
      <button class="btnMini" data-copy="addr_trx">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">USDT (ERC-20)</div>
      <div class="extAmt" id="bal_usdt_erc20">—</div>
      <div class="extAddr" id="addr_usdt_erc20">—</div>
      <button class="btnMini" data-copy="addr_usdt_erc20">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">USDT (TRC-20)</div>
      <div class="extAmt" id="bal_usdt_trc20">—</div>
      <div class="extAddr" id="addr_usdt_trc20">—</div>
      <button class="btnMini" data-copy="addr_usdt_trc20">Copy</button>
    </div>
  </div>

  <div class="extFoot">
    <div class="extHint" id="extWalletHint">Tip: deposits show up automatically (refresh every ~15s).</div>
    <div class="extSrc" id="extWalletSources">—</div>
  </div>
</div>
<!-- ====== /External wallets ====== -->

</body>
</html>
```

---

## FILE: /opt/logos/www/wallet/_bak_bridge_20260107T102635Z/app.js

- bytes: 16445
- sha256: `512531da4758ae0e55402363654e6ac8c586d32cd5d398319c1e497859d650f9`

```js
'use strict';

const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/node-api'));

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


/* ====== LOGOS_EXT_WALLET_UI (wallet-api balances) ====== */
(() => {
  const ORIGIN = (location.origin || "").replace(/\/$/, "");
  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");

  const $ = (id) => document.getElementById(id);
  const show = (el, on=true) => { if (el) el.style.display = on ? "" : "none"; };

  const trunc = (s, a=8, b=6) => {
    if (!s || typeof s !== "string") return "—";
    if (s.length <= a+b+3) return s;
    return s.slice(0,a) + "…" + s.slice(-b);
  };

  const safeNum = (x) => {
    const n = Number(x);
    return Number.isFinite(n) ? n : 0;
  };

  const fmtFixed = (n, d=6) => {
    try {
      return safeNum(n).toFixed(d).replace(/\.?0+$/, "");
    } catch {
      return String(n ?? "0");
    }
  };

  const satToBtc = (sat) => safeNum(sat) / 1e8;
  const weiToEth = (wei) => safeNum(wei) / 1e18;

  const getRID = () => {
    // подстрахуемся под разные ключи
    return (
      localStorage.getItem("RID") ||
      localStorage.getItem("rid") ||
      localStorage.getItem("logos_rid") ||
      ""
    ).trim();
  };

  const apiGet = async (url, timeoutMs=8000) => {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), timeoutMs);
    try {
      const r = await fetch(url, { signal: ctrl.signal, credentials: "omit" });
      if (!r.ok) throw new Error("HTTP " + r.status);
      return await r.json();
    } finally {
      clearTimeout(t);
    }
  };

  const bindCopyButtons = () => {
    document.querySelectorAll("[data-copy]").forEach((btn) => {
      if (btn.dataset.bound) return;
      btn.dataset.bound = "1";
      btn.addEventListener("click", async () => {
        const id = btn.getAttribute("data-copy");
        const el = $(id);
        const full = el ? (el.dataset.full || el.textContent || "") : "";
        if (!full || full === "—") return;
        try {
          await navigator.clipboard.writeText(full);
          const prev = btn.textContent;
          btn.textContent = "Copied";
          setTimeout(() => (btn.textContent = prev), 900);
        } catch {}
      });
    });
  };

  const setStatus = (ok, text) => {
    const s = $("extWalletStatus");
    if (!s) return;
    s.classList.remove("ok", "bad");
    s.classList.add(ok ? "ok" : "bad");
    s.textContent = text;
  };

  const setLatency = (ms) => {
    const el = $("extWalletLatency");
    if (!el) return;
    el.textContent = (ms != null) ? (ms + " ms") : "—";
  };

  const setAddr = (id, val) => {
    const el = $(id);
    if (!el) return;
    el.dataset.full = val || "";
    el.textContent = trunc(val || "");
  };

  const setAmt = (id, val) => {
    const el = $(id);
    if (!el) return;
    el.textContent = val;
  };

  const render = (payload) => {
    const a = payload.addresses || {};
    const b = payload.balances || {};
    setAddr("addr_btc", a.BTC);
    setAddr("addr_eth", a.ETH);
    setAddr("addr_trx", a.TRON);
    setAddr("addr_usdt_erc20", a.USDT_ERC20 || a.ETH);
    setAddr("addr_usdt_trc20", a.USDT_TRC20 || a.TRON);

    if (b.BTC) {
      setAmt("bal_btc", fmtFixed(satToBtc(b.BTC.total_sat || 0), 8) + " BTC");
    }
    if (b.ETH) {
      setAmt("bal_eth", fmtFixed(weiToEth(b.ETH.wei || 0), 6) + " ETH");
      const u = (b.ETH.usdt_erc20 || {});
      setAmt("bal_usdt_erc20", fmtFixed((safeNum(u.raw || 0) / 1e6), 2) + " USDT");
    }
    if (b.TRON) {
      setAmt("bal_trx", fmtFixed((safeNum(b.TRON.sun || 0) / 1e6), 6) + " TRX");
      const u = (b.TRON.usdt_trc20 || {});
      // raw может быть null если API не вернул токены — считаем 0
      setAmt("bal_usdt_trc20", fmtFixed((safeNum(u.raw || 0) / 1e6), 2) + " USDT");
    }

    const src = $("extWalletSources");
    if (src) {
      const sBTC = b.BTC?.source || "—";
      const sETH = b.ETH?.source || "—";
      const sTR  = b.TRON?.source || "—";
      src.textContent = `Sources: BTC=${sBTC} · ETH=${sETH} · TRON=${sTR}`;
    }

    setLatency(payload.latency_ms);
  };

  const tick = async () => {
    const rid = getRID();
    const card = $("extWalletCard");
    if (!rid) { show(card, false); return; }
    show(card, true);
    bindCopyButtons();

    try {
      setStatus(true, "updating…");
      // balances уже включает addresses, но на всякий страх — дернём receive один раз при первом показе
      const data = await apiGet(`${WALLET_API}/v1/balances/${encodeURIComponent(rid)}`, 12000);
      render(data);
      setStatus(true, "live");
    } catch (e) {
      setStatus(false, "offline");
    }
  };

  // старт
  setTimeout(() => tick(), 250);
  setInterval(() => tick(), 15000);

  window.LOGOS_EXT_WALLET_UI = { tick };
})();
 /* ====== /LOGOS_EXT_WALLET_UI ====== */
```

---

## FILE: /opt/logos/www/wallet/_bak_bridge_20260107T102822Z/app.css

- bytes: 2892
- sha256: `e067ac77ebcdf94fa36dc61e7c51faaee8cb264f8e3086ae60f6047215c12e68`

```css
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


/* ====== External wallets card ====== */
.extWalletCard{ margin-top:16px; }
.extHead{ display:flex; align-items:flex-start; justify-content:space-between; gap:12px; }
.extTitle{ font-weight:700; font-size:16px; letter-spacing:0.2px; }
.extSub{ opacity:.75; font-size:12px; margin-top:2px; }
.extMeta{ display:flex; gap:8px; align-items:center; }
.pill{ padding:6px 10px; border-radius:999px; font-size:12px; border:1px solid rgba(255,255,255,.10); background:rgba(255,255,255,.04); }
.pill.ok{ border-color: rgba(80,255,170,.25); background: rgba(80,255,170,.06); }
.pill.bad{ border-color: rgba(255,100,120,.25); background: rgba(255,100,120,.06); }
.pill.ghost{ opacity:.8; }

.extGrid{ margin-top:12px; display:flex; flex-direction:column; gap:10px; }
.extRow{
  display:grid;
  grid-template-columns: 140px 120px 1fr 78px;
  gap:10px;
  align-items:center;
  padding:10px 10px;
  border-radius:12px;
  border:1px solid rgba(255,255,255,.08);
  background: rgba(0,0,0,.18);
}
.extCoin{ font-weight:650; }
.extAmt{ font-variant-numeric: tabular-nums; opacity:.95; }
.extAddr{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; font-size:12px; opacity:.9; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.btnMini{
  padding:8px 10px;
  border-radius:10px;
  border:1px solid rgba(255,255,255,.10);
  background: rgba(255,255,255,.06);
  cursor:pointer;
}
.btnMini:hover{ background: rgba(255,255,255,.10); }
.extFoot{ display:flex; justify-content:space-between; align-items:center; gap:12px; margin-top:10px; }
.extHint{ opacity:.75; font-size:12px; }
.extSrc{ opacity:.6; font-size:12px; text-align:right; }
/* ====== /External wallets card ====== */


/* ====== Bridge result box ====== */
.bridgeResult{
  margin-top:10px;
  padding:10px 12px;
  border-radius:12px;
  border:1px solid rgba(255,255,255,.10);
  background: rgba(0,0,0,.18);
  font-size:12px;
  line-height:1.35;
  white-space:pre-wrap;
}
.bridgeResult.ok{ border-color: rgba(80,255,170,.25); background: rgba(80,255,170,.06); }
.bridgeResult.bad{ border-color: rgba(255,100,120,.25); background: rgba(255,100,120,.06); }
/* ====== /Bridge result box ====== */
```

---

## FILE: /opt/logos/www/wallet/_bak_bridge_20260107T102822Z/app.html

- bytes: 6433
- sha256: `1ef0ae58a9af795c54d5fc50d283309c20bc9741fb60d395fb930c80f3babb3c`

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta http-equiv="Cache-Control" content="no-store"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Wallet</title>
  <link rel="stylesheet" href="/shared/wallet-themeP260101_01"/>
  <link rel="stylesheet" href="./appP260101_01"/>
<script src="./api_base.js"></script>
<link rel="stylesheet" href="/shared/wallet-theme.css?v=20260101_02"/>
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

<!-- ====== External wallets (wallet-api) ====== -->
<div class="card extWalletCard" id="extWalletCard" style="display:none;">
  <div class="extHead">
    <div>
      <div class="extTitle">External wallets</div>
      <div class="extSub">BTC / ETH / TRX / USDT — on-chain balances (watch-only)</div>
    </div>
    <div class="extMeta">
      <span class="pill" id="extWalletStatus">connecting…</span>
      <span class="pill ghost" id="extWalletLatency">—</span>
    </div>
  </div>

  <div class="extGrid">
    <div class="extRow">
      <div class="extCoin">BTC</div>
      <div class="extAmt" id="bal_btc">—</div>
      <div class="extAddr" id="addr_btc">—</div>
      <button class="btnMini" data-copy="addr_btc">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">ETH</div>
      <div class="extAmt" id="bal_eth">—</div>
      <div class="extAddr" id="addr_eth">—</div>
      <button class="btnMini" data-copy="addr_eth">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">TRX</div>
      <div class="extAmt" id="bal_trx">—</div>
      <div class="extAddr" id="addr_trx">—</div>
      <button class="btnMini" data-copy="addr_trx">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">USDT (ERC-20)</div>
      <div class="extAmt" id="bal_usdt_erc20">—</div>
      <div class="extAddr" id="addr_usdt_erc20">—</div>
      <button class="btnMini" data-copy="addr_usdt_erc20">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">USDT (TRC-20)</div>
      <div class="extAmt" id="bal_usdt_trc20">—</div>
      <div class="extAddr" id="addr_usdt_trc20">—</div>
      <button class="btnMini" data-copy="addr_usdt_trc20">Copy</button>
    </div>
  </div>

  <div class="extFoot">
    <div class="extHint" id="extWalletHint">Tip: deposits show up automatically (refresh every ~15s).</div>
    <div class="extSrc" id="extWalletSources">—</div>
  </div>
</div>
<!-- ====== /External wallets ====== -->


<div class="bridgeResult" id="bridgeResult" style="display:none;"></div>

</body>
</html>
```

---

## FILE: /opt/logos/www/wallet/_bak_bridge_20260107T102822Z/app.js

- bytes: 21990
- sha256: `1a7eb3bfa116e1c2bfa84ac76ff16013ac50973001abd5af9a235b427961baa7`

```js
'use strict';

const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/node-api'));

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


/* ====== LOGOS_EXT_WALLET_UI (wallet-api balances) ====== */
(() => {
  const ORIGIN = (location.origin || "").replace(/\/$/, "");
  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");

  const $ = (id) => document.getElementById(id);
  const show = (el, on=true) => { if (el) el.style.display = on ? "" : "none"; };

  const trunc = (s, a=8, b=6) => {
    if (!s || typeof s !== "string") return "—";
    if (s.length <= a+b+3) return s;
    return s.slice(0,a) + "…" + s.slice(-b);
  };

  const safeNum = (x) => {
    const n = Number(x);
    return Number.isFinite(n) ? n : 0;
  };

  const fmtFixed = (n, d=6) => {
    try {
      return safeNum(n).toFixed(d).replace(/\.?0+$/, "");
    } catch {
      return String(n ?? "0");
    }
  };

  const satToBtc = (sat) => safeNum(sat) / 1e8;
  const weiToEth = (wei) => safeNum(wei) / 1e18;

  const getRID = () => {
    // подстрахуемся под разные ключи
    return (
      localStorage.getItem("RID") ||
      localStorage.getItem("rid") ||
      localStorage.getItem("logos_rid") ||
      ""
    ).trim();
  };

  const apiGet = async (url, timeoutMs=8000) => {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), timeoutMs);
    try {
      const r = await fetch(url, { signal: ctrl.signal, credentials: "omit" });
      if (!r.ok) throw new Error("HTTP " + r.status);
      return await r.json();
    } finally {
      clearTimeout(t);
    }
  };

  const bindCopyButtons = () => {
    document.querySelectorAll("[data-copy]").forEach((btn) => {
      if (btn.dataset.bound) return;
      btn.dataset.bound = "1";
      btn.addEventListener("click", async () => {
        const id = btn.getAttribute("data-copy");
        const el = $(id);
        const full = el ? (el.dataset.full || el.textContent || "") : "";
        if (!full || full === "—") return;
        try {
          await navigator.clipboard.writeText(full);
          const prev = btn.textContent;
          btn.textContent = "Copied";
          setTimeout(() => (btn.textContent = prev), 900);
        } catch {}
      });
    });
  };

  const setStatus = (ok, text) => {
    const s = $("extWalletStatus");
    if (!s) return;
    s.classList.remove("ok", "bad");
    s.classList.add(ok ? "ok" : "bad");
    s.textContent = text;
  };

  const setLatency = (ms) => {
    const el = $("extWalletLatency");
    if (!el) return;
    el.textContent = (ms != null) ? (ms + " ms") : "—";
  };

  const setAddr = (id, val) => {
    const el = $(id);
    if (!el) return;
    el.dataset.full = val || "";
    el.textContent = trunc(val || "");
  };

  const setAmt = (id, val) => {
    const el = $(id);
    if (!el) return;
    el.textContent = val;
  };

  const render = (payload) => {
    const a = payload.addresses || {};
    const b = payload.balances || {};
    setAddr("addr_btc", a.BTC);
    setAddr("addr_eth", a.ETH);
    setAddr("addr_trx", a.TRON);
    setAddr("addr_usdt_erc20", a.USDT_ERC20 || a.ETH);
    setAddr("addr_usdt_trc20", a.USDT_TRC20 || a.TRON);

    if (b.BTC) {
      setAmt("bal_btc", fmtFixed(satToBtc(b.BTC.total_sat || 0), 8) + " BTC");
    }
    if (b.ETH) {
      setAmt("bal_eth", fmtFixed(weiToEth(b.ETH.wei || 0), 6) + " ETH");
      const u = (b.ETH.usdt_erc20 || {});
      setAmt("bal_usdt_erc20", fmtFixed((safeNum(u.raw || 0) / 1e6), 2) + " USDT");
    }
    if (b.TRON) {
      setAmt("bal_trx", fmtFixed((safeNum(b.TRON.sun || 0) / 1e6), 6) + " TRX");
      const u = (b.TRON.usdt_trc20 || {});
      // raw может быть null если API не вернул токены — считаем 0
      setAmt("bal_usdt_trc20", fmtFixed((safeNum(u.raw || 0) / 1e6), 2) + " USDT");
    }

    const src = $("extWalletSources");
    if (src) {
      const sBTC = b.BTC?.source || "—";
      const sETH = b.ETH?.source || "—";
      const sTR  = b.TRON?.source || "—";
      src.textContent = `Sources: BTC=${sBTC} · ETH=${sETH} · TRON=${sTR}`;
    }

    setLatency(payload.latency_ms);
  };

  const tick = async () => {
    const rid = getRID();
    const card = $("extWalletCard");
    if (!rid) { show(card, false); return; }
    show(card, true);
    bindCopyButtons();

    try {
      setStatus(true, "updating…");
      // balances уже включает addresses, но на всякий страх — дернём receive один раз при первом показе
      const data = await apiGet(`${WALLET_API}/v1/balances/${encodeURIComponent(rid)}`, 12000);
      render(data);
      setStatus(true, "live");
    } catch (e) {
      setStatus(false, "offline");
    }
  };

  // старт
  setTimeout(() => tick(), 250);
  setInterval(() => tick(), 15000);

  window.LOGOS_EXT_WALLET_UI = { tick };
})();
 /* ====== /LOGOS_EXT_WALLET_UI ====== */


/* ====== LOGOS_BRIDGE_UI_BIND (auto-detect bridge endpoints from wallet-api openapi) ====== */
(() => {
  const ORIGIN = (location.origin || "").replace(/\/$/, "");
  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");

  const $ = (id) => document.getElementById(id);
  const rid = () =>
    (localStorage.getItem("RID") || localStorage.getItem("rid") || localStorage.getItem("logos_rid") || "").trim();

  const showResult = (ok, text) => {
    const box = $("bridgeResult");
    if (!box) return;
    box.style.display = "";
    box.classList.remove("ok","bad");
    box.classList.add(ok ? "ok" : "bad");
    box.textContent = text;
  };

  const apiGet = async (url, timeoutMs=12000) => {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), timeoutMs);
    try {
      const r = await fetch(url, { signal: ctrl.signal, credentials:"omit" });
      if (!r.ok) throw new Error("HTTP " + r.status);
      return await r.json();
    } finally { clearTimeout(t); }
  };

  const apiPost = async (url, body, timeoutMs=20000) => {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), timeoutMs);
    try {
      const r = await fetch(url, {
        method:"POST",
        headers:{ "Content-Type":"application/json" },
        body: JSON.stringify(body),
        signal: ctrl.signal,
        credentials:"omit",
      });
      const txt = await r.text();
      let data = null;
      try { data = JSON.parse(txt); } catch {}
      if (!r.ok) throw new Error("HTTP " + r.status + (txt ? (": " + txt.slice(0,300)) : ""));
      return data ?? { ok:true, raw: txt };
    } finally { clearTimeout(t); }
  };

  const normDir = (v) => (v || "").trim();
  const normChain = (v) => (v || "").trim();
  const normAmt = (v) => {
    const n = Number(String(v||"").replace(",", "."));
    return Number.isFinite(n) ? n : 0;
  };

  // --- autodetect endpoints
  let EP = { quote:null, create:null, status:null, openapi:null };

  const detectEndpoints = async () => {
    if (EP.openapi) return EP;
    try {
      const spec = await apiGet(`${WALLET_API}/openapi.json`, 12000);
      EP.openapi = spec;

      const paths = Object.keys(spec.paths || {});
      const cand = (re) => paths.filter(p => re.test(p)).sort();

      // ищем популярные варианты
      const quote = cand(/quote/i).find(p => /bridge|swap|rlgn|convert/i.test(p)) || cand(/bridge.*quote/i)[0] || cand(/quote/i)[0];
      const create = cand(/create|request|order|swap/i).find(p => /bridge|swap|rlgn|convert/i.test(p)) || cand(/bridge.*(create|request|order)/i)[0];
      const status = cand(/status|order/i).find(p => /bridge|swap|rlgn|convert/i.test(p)) || null;

      EP.quote = quote || null;
      EP.create = create || null;
      EP.status = status || null;

      return EP;
    } catch (e) {
      // fallback (если openapi не отдался)
      EP.quote  = "/v1/bridge/quote";
      EP.create = "/v1/bridge/create";
      EP.status = "/v1/bridge/status";
      return EP;
    }
  };

  const readForm = () => {
    const r = rid();
    if (!r) throw new Error("RID not found. Create/restore RID first.");
    const direction = normDir($("bridge_direction")?.value);
    const chain = normChain($("bridge_chain")?.value);
    const amount = normAmt($("bridge_amount")?.value);
    const ext_txid = ($("bridge_ext_txid")?.value || "").trim();

    return { rid: r, direction, chain, amount, ext_txid };
  };

  const doQuote = async () => {
    const ep = await detectEndpoints();
    if (!ep.quote) throw new Error("Bridge quote endpoint not found in openapi.");
    const f = readForm();

    // минимальный payload (без мусора)
    const body = {
      rid: f.rid,
      direction: f.direction,
      chain: f.chain,
      amount: f.amount,
      ext_txid: f.ext_txid || undefined,
    };

    const t0 = performance.now();
    const res = await apiPost(`${WALLET_API}${ep.quote}`, body, 20000);
    const ms = Math.round(performance.now() - t0);

    showResult(true, `[QUOTE ✅] ${ms} ms\n` + JSON.stringify(res, null, 2));
  };

  const doCreate = async () => {
    const ep = await detectEndpoints();
    if (!ep.create) throw new Error("Bridge create endpoint not found in openapi.");
    const f = readForm();

    const body = {
      rid: f.rid,
      direction: f.direction,
      chain: f.chain,
      amount: f.amount,
      ext_txid: f.ext_txid || undefined,
    };

    const t0 = performance.now();
    const res = await apiPost(`${WALLET_API}${ep.create}`, body, 25000);
    const ms = Math.round(performance.now() - t0);

    showResult(true, `[CREATE ✅] ${ms} ms\n` + JSON.stringify(res, null, 2));
  };

  const bind = () => {
    const bq = $("b_bridge_quote");
    const bc = $("b_bridge_create");
    if (bq && !bq.dataset.bound) {
      bq.dataset.bound = "1";
      bq.addEventListener("click", async () => {
        try { showResult(true, "Calculating…"); await doQuote(); }
        catch (e) { showResult(false, "[QUOTE ❌]\n" + (e?.message || String(e))); }
      });
    }
    if (bc && !bc.dataset.bound) {
      bc.dataset.bound = "1";
      bc.addEventListener("click", async () => {
        try { showResult(true, "Creating…"); await doCreate(); }
        catch (e) { showResult(false, "[CREATE ❌]\n" + (e?.message || String(e))); }
      });
    }
  };

  setTimeout(bind, 300);
  window.LOGOS_BRIDGE_UI_BIND = { bind };
})();
 /* ====== /LOGOS_BRIDGE_UI_BIND ====== */
```

---

## FILE: /opt/logos/www/wallet/_bak_entry_20260107T105554Z/index.html

- bytes: 7139
- sha256: `e426c27de94ac41eff08bc17823297f455eb4f004ab39ade2affba21e99928bc`

```html
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

---

## FILE: /opt/logos/www/wallet/_bak_entry_20260108T142703Z/index.html

- bytes: 6433
- sha256: `1ef0ae58a9af795c54d5fc50d283309c20bc9741fb60d395fb930c80f3babb3c`

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta http-equiv="Cache-Control" content="no-store"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Wallet</title>
  <link rel="stylesheet" href="/shared/wallet-themeP260101_01"/>
  <link rel="stylesheet" href="./appP260101_01"/>
<script src="./api_base.js"></script>
<link rel="stylesheet" href="/shared/wallet-theme.css?v=20260101_02"/>
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

<!-- ====== External wallets (wallet-api) ====== -->
<div class="card extWalletCard" id="extWalletCard" style="display:none;">
  <div class="extHead">
    <div>
      <div class="extTitle">External wallets</div>
      <div class="extSub">BTC / ETH / TRX / USDT — on-chain balances (watch-only)</div>
    </div>
    <div class="extMeta">
      <span class="pill" id="extWalletStatus">connecting…</span>
      <span class="pill ghost" id="extWalletLatency">—</span>
    </div>
  </div>

  <div class="extGrid">
    <div class="extRow">
      <div class="extCoin">BTC</div>
      <div class="extAmt" id="bal_btc">—</div>
      <div class="extAddr" id="addr_btc">—</div>
      <button class="btnMini" data-copy="addr_btc">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">ETH</div>
      <div class="extAmt" id="bal_eth">—</div>
      <div class="extAddr" id="addr_eth">—</div>
      <button class="btnMini" data-copy="addr_eth">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">TRX</div>
      <div class="extAmt" id="bal_trx">—</div>
      <div class="extAddr" id="addr_trx">—</div>
      <button class="btnMini" data-copy="addr_trx">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">USDT (ERC-20)</div>
      <div class="extAmt" id="bal_usdt_erc20">—</div>
      <div class="extAddr" id="addr_usdt_erc20">—</div>
      <button class="btnMini" data-copy="addr_usdt_erc20">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">USDT (TRC-20)</div>
      <div class="extAmt" id="bal_usdt_trc20">—</div>
      <div class="extAddr" id="addr_usdt_trc20">—</div>
      <button class="btnMini" data-copy="addr_usdt_trc20">Copy</button>
    </div>
  </div>

  <div class="extFoot">
    <div class="extHint" id="extWalletHint">Tip: deposits show up automatically (refresh every ~15s).</div>
    <div class="extSrc" id="extWalletSources">—</div>
  </div>
</div>
<!-- ====== /External wallets ====== -->


<div class="bridgeResult" id="bridgeResult" style="display:none;"></div>

</body>
</html>
```

---

## FILE: /opt/logos/www/wallet/_bak_ui_20260107T101342Z/app.css

- bytes: 682
- sha256: `2e8e444586c03fc5f72594fafb26e4ed1a8f1cba45d6214545e5b5ff1b5c49c4`

```css
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

---

## FILE: /opt/logos/www/wallet/_bak_ui_20260107T101342Z/app.html

- bytes: 4330
- sha256: `2e661941b4940a64318028b1f2e7f5e1416368d4d6d108086e3e44c1980ff0ea`

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta http-equiv="Cache-Control" content="no-store"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Wallet</title>
  <link rel="stylesheet" href="/shared/wallet-themeP260101_01"/>
  <link rel="stylesheet" href="./appP260101_01"/>
<script src="./api_base.js"></script>
<link rel="stylesheet" href="/shared/wallet-theme.css?v=20260101_02"/>
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
</body>
</html>
```

---

## FILE: /opt/logos/www/wallet/_bak_ui_20260107T101342Z/app.js

- bytes: 11592
- sha256: `297ab77d740c6f02befed611f151483809435b5cf6efba6e1c031efbeeaa698d`

```js
'use strict';

const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/node-api'));

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

---

## FILE: /opt/logos/www/wallet/api_base.js

- bytes: 178
- sha256: `ec9b0084cca46c0917a6843317daed618a2baa781d9182f2870903ee6cde6303`

```js
(() => {
  const origin = window.location.origin.replace(/\/+$/, "");
  window.LOGOS_WALLET_API = origin + "/wallet-api";
  window.LOGOS_NODE_API   = origin + "/node-api";
})();
```

---

## FILE: /opt/logos/www/wallet/app.css

- bytes: 2892
- sha256: `e067ac77ebcdf94fa36dc61e7c51faaee8cb264f8e3086ae60f6047215c12e68`

```css
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


/* ====== External wallets card ====== */
.extWalletCard{ margin-top:16px; }
.extHead{ display:flex; align-items:flex-start; justify-content:space-between; gap:12px; }
.extTitle{ font-weight:700; font-size:16px; letter-spacing:0.2px; }
.extSub{ opacity:.75; font-size:12px; margin-top:2px; }
.extMeta{ display:flex; gap:8px; align-items:center; }
.pill{ padding:6px 10px; border-radius:999px; font-size:12px; border:1px solid rgba(255,255,255,.10); background:rgba(255,255,255,.04); }
.pill.ok{ border-color: rgba(80,255,170,.25); background: rgba(80,255,170,.06); }
.pill.bad{ border-color: rgba(255,100,120,.25); background: rgba(255,100,120,.06); }
.pill.ghost{ opacity:.8; }

.extGrid{ margin-top:12px; display:flex; flex-direction:column; gap:10px; }
.extRow{
  display:grid;
  grid-template-columns: 140px 120px 1fr 78px;
  gap:10px;
  align-items:center;
  padding:10px 10px;
  border-radius:12px;
  border:1px solid rgba(255,255,255,.08);
  background: rgba(0,0,0,.18);
}
.extCoin{ font-weight:650; }
.extAmt{ font-variant-numeric: tabular-nums; opacity:.95; }
.extAddr{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; font-size:12px; opacity:.9; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.btnMini{
  padding:8px 10px;
  border-radius:10px;
  border:1px solid rgba(255,255,255,.10);
  background: rgba(255,255,255,.06);
  cursor:pointer;
}
.btnMini:hover{ background: rgba(255,255,255,.10); }
.extFoot{ display:flex; justify-content:space-between; align-items:center; gap:12px; margin-top:10px; }
.extHint{ opacity:.75; font-size:12px; }
.extSrc{ opacity:.6; font-size:12px; text-align:right; }
/* ====== /External wallets card ====== */


/* ====== Bridge result box ====== */
.bridgeResult{
  margin-top:10px;
  padding:10px 12px;
  border-radius:12px;
  border:1px solid rgba(255,255,255,.10);
  background: rgba(0,0,0,.18);
  font-size:12px;
  line-height:1.35;
  white-space:pre-wrap;
}
.bridgeResult.ok{ border-color: rgba(80,255,170,.25); background: rgba(80,255,170,.06); }
.bridgeResult.bad{ border-color: rgba(255,100,120,.25); background: rgba(255,100,120,.06); }
/* ====== /Bridge result box ====== */
```

---

## FILE: /opt/logos/www/wallet/app.html

- bytes: 6433
- sha256: `1ef0ae58a9af795c54d5fc50d283309c20bc9741fb60d395fb930c80f3babb3c`

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta http-equiv="Cache-Control" content="no-store"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Wallet</title>
  <link rel="stylesheet" href="/shared/wallet-themeP260101_01"/>
  <link rel="stylesheet" href="./appP260101_01"/>
<script src="./api_base.js"></script>
<link rel="stylesheet" href="/shared/wallet-theme.css?v=20260101_02"/>
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

<!-- ====== External wallets (wallet-api) ====== -->
<div class="card extWalletCard" id="extWalletCard" style="display:none;">
  <div class="extHead">
    <div>
      <div class="extTitle">External wallets</div>
      <div class="extSub">BTC / ETH / TRX / USDT — on-chain balances (watch-only)</div>
    </div>
    <div class="extMeta">
      <span class="pill" id="extWalletStatus">connecting…</span>
      <span class="pill ghost" id="extWalletLatency">—</span>
    </div>
  </div>

  <div class="extGrid">
    <div class="extRow">
      <div class="extCoin">BTC</div>
      <div class="extAmt" id="bal_btc">—</div>
      <div class="extAddr" id="addr_btc">—</div>
      <button class="btnMini" data-copy="addr_btc">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">ETH</div>
      <div class="extAmt" id="bal_eth">—</div>
      <div class="extAddr" id="addr_eth">—</div>
      <button class="btnMini" data-copy="addr_eth">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">TRX</div>
      <div class="extAmt" id="bal_trx">—</div>
      <div class="extAddr" id="addr_trx">—</div>
      <button class="btnMini" data-copy="addr_trx">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">USDT (ERC-20)</div>
      <div class="extAmt" id="bal_usdt_erc20">—</div>
      <div class="extAddr" id="addr_usdt_erc20">—</div>
      <button class="btnMini" data-copy="addr_usdt_erc20">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">USDT (TRC-20)</div>
      <div class="extAmt" id="bal_usdt_trc20">—</div>
      <div class="extAddr" id="addr_usdt_trc20">—</div>
      <button class="btnMini" data-copy="addr_usdt_trc20">Copy</button>
    </div>
  </div>

  <div class="extFoot">
    <div class="extHint" id="extWalletHint">Tip: deposits show up automatically (refresh every ~15s).</div>
    <div class="extSrc" id="extWalletSources">—</div>
  </div>
</div>
<!-- ====== /External wallets ====== -->


<div class="bridgeResult" id="bridgeResult" style="display:none;"></div>

</body>
</html>
```

---

## FILE: /opt/logos/www/wallet/app.js

- bytes: 21990
- sha256: `1a7eb3bfa116e1c2bfa84ac76ff16013ac50973001abd5af9a235b427961baa7`

```js
'use strict';

const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/node-api'));

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


/* ====== LOGOS_EXT_WALLET_UI (wallet-api balances) ====== */
(() => {
  const ORIGIN = (location.origin || "").replace(/\/$/, "");
  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");

  const $ = (id) => document.getElementById(id);
  const show = (el, on=true) => { if (el) el.style.display = on ? "" : "none"; };

  const trunc = (s, a=8, b=6) => {
    if (!s || typeof s !== "string") return "—";
    if (s.length <= a+b+3) return s;
    return s.slice(0,a) + "…" + s.slice(-b);
  };

  const safeNum = (x) => {
    const n = Number(x);
    return Number.isFinite(n) ? n : 0;
  };

  const fmtFixed = (n, d=6) => {
    try {
      return safeNum(n).toFixed(d).replace(/\.?0+$/, "");
    } catch {
      return String(n ?? "0");
    }
  };

  const satToBtc = (sat) => safeNum(sat) / 1e8;
  const weiToEth = (wei) => safeNum(wei) / 1e18;

  const getRID = () => {
    // подстрахуемся под разные ключи
    return (
      localStorage.getItem("RID") ||
      localStorage.getItem("rid") ||
      localStorage.getItem("logos_rid") ||
      ""
    ).trim();
  };

  const apiGet = async (url, timeoutMs=8000) => {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), timeoutMs);
    try {
      const r = await fetch(url, { signal: ctrl.signal, credentials: "omit" });
      if (!r.ok) throw new Error("HTTP " + r.status);
      return await r.json();
    } finally {
      clearTimeout(t);
    }
  };

  const bindCopyButtons = () => {
    document.querySelectorAll("[data-copy]").forEach((btn) => {
      if (btn.dataset.bound) return;
      btn.dataset.bound = "1";
      btn.addEventListener("click", async () => {
        const id = btn.getAttribute("data-copy");
        const el = $(id);
        const full = el ? (el.dataset.full || el.textContent || "") : "";
        if (!full || full === "—") return;
        try {
          await navigator.clipboard.writeText(full);
          const prev = btn.textContent;
          btn.textContent = "Copied";
          setTimeout(() => (btn.textContent = prev), 900);
        } catch {}
      });
    });
  };

  const setStatus = (ok, text) => {
    const s = $("extWalletStatus");
    if (!s) return;
    s.classList.remove("ok", "bad");
    s.classList.add(ok ? "ok" : "bad");
    s.textContent = text;
  };

  const setLatency = (ms) => {
    const el = $("extWalletLatency");
    if (!el) return;
    el.textContent = (ms != null) ? (ms + " ms") : "—";
  };

  const setAddr = (id, val) => {
    const el = $(id);
    if (!el) return;
    el.dataset.full = val || "";
    el.textContent = trunc(val || "");
  };

  const setAmt = (id, val) => {
    const el = $(id);
    if (!el) return;
    el.textContent = val;
  };

  const render = (payload) => {
    const a = payload.addresses || {};
    const b = payload.balances || {};
    setAddr("addr_btc", a.BTC);
    setAddr("addr_eth", a.ETH);
    setAddr("addr_trx", a.TRON);
    setAddr("addr_usdt_erc20", a.USDT_ERC20 || a.ETH);
    setAddr("addr_usdt_trc20", a.USDT_TRC20 || a.TRON);

    if (b.BTC) {
      setAmt("bal_btc", fmtFixed(satToBtc(b.BTC.total_sat || 0), 8) + " BTC");
    }
    if (b.ETH) {
      setAmt("bal_eth", fmtFixed(weiToEth(b.ETH.wei || 0), 6) + " ETH");
      const u = (b.ETH.usdt_erc20 || {});
      setAmt("bal_usdt_erc20", fmtFixed((safeNum(u.raw || 0) / 1e6), 2) + " USDT");
    }
    if (b.TRON) {
      setAmt("bal_trx", fmtFixed((safeNum(b.TRON.sun || 0) / 1e6), 6) + " TRX");
      const u = (b.TRON.usdt_trc20 || {});
      // raw может быть null если API не вернул токены — считаем 0
      setAmt("bal_usdt_trc20", fmtFixed((safeNum(u.raw || 0) / 1e6), 2) + " USDT");
    }

    const src = $("extWalletSources");
    if (src) {
      const sBTC = b.BTC?.source || "—";
      const sETH = b.ETH?.source || "—";
      const sTR  = b.TRON?.source || "—";
      src.textContent = `Sources: BTC=${sBTC} · ETH=${sETH} · TRON=${sTR}`;
    }

    setLatency(payload.latency_ms);
  };

  const tick = async () => {
    const rid = getRID();
    const card = $("extWalletCard");
    if (!rid) { show(card, false); return; }
    show(card, true);
    bindCopyButtons();

    try {
      setStatus(true, "updating…");
      // balances уже включает addresses, но на всякий страх — дернём receive один раз при первом показе
      const data = await apiGet(`${WALLET_API}/v1/balances/${encodeURIComponent(rid)}`, 12000);
      render(data);
      setStatus(true, "live");
    } catch (e) {
      setStatus(false, "offline");
    }
  };

  // старт
  setTimeout(() => tick(), 250);
  setInterval(() => tick(), 15000);

  window.LOGOS_EXT_WALLET_UI = { tick };
})();
 /* ====== /LOGOS_EXT_WALLET_UI ====== */


/* ====== LOGOS_BRIDGE_UI_BIND (auto-detect bridge endpoints from wallet-api openapi) ====== */
(() => {
  const ORIGIN = (location.origin || "").replace(/\/$/, "");
  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");

  const $ = (id) => document.getElementById(id);
  const rid = () =>
    (localStorage.getItem("RID") || localStorage.getItem("rid") || localStorage.getItem("logos_rid") || "").trim();

  const showResult = (ok, text) => {
    const box = $("bridgeResult");
    if (!box) return;
    box.style.display = "";
    box.classList.remove("ok","bad");
    box.classList.add(ok ? "ok" : "bad");
    box.textContent = text;
  };

  const apiGet = async (url, timeoutMs=12000) => {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), timeoutMs);
    try {
      const r = await fetch(url, { signal: ctrl.signal, credentials:"omit" });
      if (!r.ok) throw new Error("HTTP " + r.status);
      return await r.json();
    } finally { clearTimeout(t); }
  };

  const apiPost = async (url, body, timeoutMs=20000) => {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), timeoutMs);
    try {
      const r = await fetch(url, {
        method:"POST",
        headers:{ "Content-Type":"application/json" },
        body: JSON.stringify(body),
        signal: ctrl.signal,
        credentials:"omit",
      });
      const txt = await r.text();
      let data = null;
      try { data = JSON.parse(txt); } catch {}
      if (!r.ok) throw new Error("HTTP " + r.status + (txt ? (": " + txt.slice(0,300)) : ""));
      return data ?? { ok:true, raw: txt };
    } finally { clearTimeout(t); }
  };

  const normDir = (v) => (v || "").trim();
  const normChain = (v) => (v || "").trim();
  const normAmt = (v) => {
    const n = Number(String(v||"").replace(",", "."));
    return Number.isFinite(n) ? n : 0;
  };

  // --- autodetect endpoints
  let EP = { quote:null, create:null, status:null, openapi:null };

  const detectEndpoints = async () => {
    if (EP.openapi) return EP;
    try {
      const spec = await apiGet(`${WALLET_API}/openapi.json`, 12000);
      EP.openapi = spec;

      const paths = Object.keys(spec.paths || {});
      const cand = (re) => paths.filter(p => re.test(p)).sort();

      // ищем популярные варианты
      const quote = cand(/quote/i).find(p => /bridge|swap|rlgn|convert/i.test(p)) || cand(/bridge.*quote/i)[0] || cand(/quote/i)[0];
      const create = cand(/create|request|order|swap/i).find(p => /bridge|swap|rlgn|convert/i.test(p)) || cand(/bridge.*(create|request|order)/i)[0];
      const status = cand(/status|order/i).find(p => /bridge|swap|rlgn|convert/i.test(p)) || null;

      EP.quote = quote || null;
      EP.create = create || null;
      EP.status = status || null;

      return EP;
    } catch (e) {
      // fallback (если openapi не отдался)
      EP.quote  = "/v1/bridge/quote";
      EP.create = "/v1/bridge/create";
      EP.status = "/v1/bridge/status";
      return EP;
    }
  };

  const readForm = () => {
    const r = rid();
    if (!r) throw new Error("RID not found. Create/restore RID first.");
    const direction = normDir($("bridge_direction")?.value);
    const chain = normChain($("bridge_chain")?.value);
    const amount = normAmt($("bridge_amount")?.value);
    const ext_txid = ($("bridge_ext_txid")?.value || "").trim();

    return { rid: r, direction, chain, amount, ext_txid };
  };

  const doQuote = async () => {
    const ep = await detectEndpoints();
    if (!ep.quote) throw new Error("Bridge quote endpoint not found in openapi.");
    const f = readForm();

    // минимальный payload (без мусора)
    const body = {
      rid: f.rid,
      direction: f.direction,
      chain: f.chain,
      amount: f.amount,
      ext_txid: f.ext_txid || undefined,
    };

    const t0 = performance.now();
    const res = await apiPost(`${WALLET_API}${ep.quote}`, body, 20000);
    const ms = Math.round(performance.now() - t0);

    showResult(true, `[QUOTE ✅] ${ms} ms\n` + JSON.stringify(res, null, 2));
  };

  const doCreate = async () => {
    const ep = await detectEndpoints();
    if (!ep.create) throw new Error("Bridge create endpoint not found in openapi.");
    const f = readForm();

    const body = {
      rid: f.rid,
      direction: f.direction,
      chain: f.chain,
      amount: f.amount,
      ext_txid: f.ext_txid || undefined,
    };

    const t0 = performance.now();
    const res = await apiPost(`${WALLET_API}${ep.create}`, body, 25000);
    const ms = Math.round(performance.now() - t0);

    showResult(true, `[CREATE ✅] ${ms} ms\n` + JSON.stringify(res, null, 2));
  };

  const bind = () => {
    const bq = $("b_bridge_quote");
    const bc = $("b_bridge_create");
    if (bq && !bq.dataset.bound) {
      bq.dataset.bound = "1";
      bq.addEventListener("click", async () => {
        try { showResult(true, "Calculating…"); await doQuote(); }
        catch (e) { showResult(false, "[QUOTE ❌]\n" + (e?.message || String(e))); }
      });
    }
    if (bc && !bc.dataset.bound) {
      bc.dataset.bound = "1";
      bc.addEventListener("click", async () => {
        try { showResult(true, "Creating…"); await doCreate(); }
        catch (e) { showResult(false, "[CREATE ❌]\n" + (e?.message || String(e))); }
      });
    }
  };

  setTimeout(bind, 300);
  window.LOGOS_BRIDGE_UI_BIND = { bind };
})();
 /* ====== /LOGOS_BRIDGE_UI_BIND ====== */
```

---

## FILE: /opt/logos/www/wallet/auth.css

- bytes: 880
- sha256: `5bb92959c854d22f3ee130a885db5b63cc7b8ddef762aad30a83b7d9f0ea52c7`

```css
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

---

## FILE: /opt/logos/www/wallet/auth.html

- bytes: 5369
- sha256: `c8491a18dd149cf8d96dc87f99e6417b08d70d82b8c4b90ecdb03ec185cc2d22`

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta http-equiv="Cache-Control" content="no-store"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Wallet — Secure</title>
  <link rel="stylesheet" href="/shared/wallet-themeP260101_01"/>
  <link rel="stylesheet" href="./authP260101_01"/>
<script src="./api_base.js"></script>
<link rel="stylesheet" href="/shared/wallet-theme.css?v=20260101_02"/>
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
  <script src="./auth.js?v=20251212_04" defer></script>
</body>
</html>
```

---

## FILE: /opt/logos/www/wallet/auth.js

- bytes: 13622
- sha256: `3761a82a54d51ffea2cc362ea93c7fae7114ccd290beaabbb57a82cb0dd2a90a`

```js
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

---

## FILE: /opt/logos/www/wallet/compat.js

- bytes: 5512
- sha256: `a178c9fb576fbacbd49c8dd57e116b4d6e0b43c73677d826dde3d2adf393bb69`

```js
"use strict";

(function () {
  // Базовый URL API
  const API = location.origin + "/node-api";

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

---

## FILE: /opt/logos/www/wallet/connect.js

- bytes: 254
- sha256: `780dbed59f7f8e01732f51ff0185c31a4bd8c51359ca8eba40716e2d2aabd3cd`

```js
// LOGOS Wallet — Airdrop module REMOVED (2026-01-01)
// оставлено как безопасный stub, чтобы ничего не ломалось, если где-то осталась ссылка.
window.LOGOS_AIRDROP = { enabled: false };
```

---

## FILE: /opt/logos/www/wallet/index.html

- bytes: 6433
- sha256: `1ef0ae58a9af795c54d5fc50d283309c20bc9741fb60d395fb930c80f3babb3c`

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta http-equiv="Cache-Control" content="no-store"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Wallet</title>
  <link rel="stylesheet" href="/shared/wallet-themeP260101_01"/>
  <link rel="stylesheet" href="./appP260101_01"/>
<script src="./api_base.js"></script>
<link rel="stylesheet" href="/shared/wallet-theme.css?v=20260101_02"/>
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

<!-- ====== External wallets (wallet-api) ====== -->
<div class="card extWalletCard" id="extWalletCard" style="display:none;">
  <div class="extHead">
    <div>
      <div class="extTitle">External wallets</div>
      <div class="extSub">BTC / ETH / TRX / USDT — on-chain balances (watch-only)</div>
    </div>
    <div class="extMeta">
      <span class="pill" id="extWalletStatus">connecting…</span>
      <span class="pill ghost" id="extWalletLatency">—</span>
    </div>
  </div>

  <div class="extGrid">
    <div class="extRow">
      <div class="extCoin">BTC</div>
      <div class="extAmt" id="bal_btc">—</div>
      <div class="extAddr" id="addr_btc">—</div>
      <button class="btnMini" data-copy="addr_btc">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">ETH</div>
      <div class="extAmt" id="bal_eth">—</div>
      <div class="extAddr" id="addr_eth">—</div>
      <button class="btnMini" data-copy="addr_eth">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">TRX</div>
      <div class="extAmt" id="bal_trx">—</div>
      <div class="extAddr" id="addr_trx">—</div>
      <button class="btnMini" data-copy="addr_trx">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">USDT (ERC-20)</div>
      <div class="extAmt" id="bal_usdt_erc20">—</div>
      <div class="extAddr" id="addr_usdt_erc20">—</div>
      <button class="btnMini" data-copy="addr_usdt_erc20">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">USDT (TRC-20)</div>
      <div class="extAmt" id="bal_usdt_trc20">—</div>
      <div class="extAddr" id="addr_usdt_trc20">—</div>
      <button class="btnMini" data-copy="addr_usdt_trc20">Copy</button>
    </div>
  </div>

  <div class="extFoot">
    <div class="extHint" id="extWalletHint">Tip: deposits show up automatically (refresh every ~15s).</div>
    <div class="extSrc" id="extWalletSources">—</div>
  </div>
</div>
<!-- ====== /External wallets ====== -->


<div class="bridgeResult" id="bridgeResult" style="display:none;"></div>

</body>
</html>
```

---

## FILE: /opt/logos/www/wallet/login.html

- bytes: 318
- sha256: `409ff9c314f528c39591bcd2cb7bc400fc1eb9c9e25669f231ff1b73c1cd35d0`

```html
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

---

## FILE: /opt/logos/www/wallet/ui.js

- bytes: 3447
- sha256: `e2814b431d1cf6c38a9f2efb1513d597b402d488d40e968cb87289c66f92f550`

```js
(() => {
  // Берём API из app.js, если он есть, иначе собираем по origin
  const API_BASE = (window.API ||
                    window.API_ENDPOINT ||
                    (location.origin.replace(/\/$/, '') + '/node-api'));

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

---

## FILE: /opt/logos/www/wallet/wallet.css

- bytes: 5953
- sha256: `d808788cbb5a493d8185bb14b7021d8bcaeed7a56ce194e49e02c8aaf9607a9f`

```css
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

---

## FILE: /opt/logos/www/wallet_dev/_bak_bridge_20260107T102635Z/app.css

- bytes: 2416
- sha256: `6fe95464e581b9a746887921adbafd7a05e29e260cdb70e0b95e95c87db3ab83`

```css
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


/* ====== External wallets card ====== */
.extWalletCard{ margin-top:16px; }
.extHead{ display:flex; align-items:flex-start; justify-content:space-between; gap:12px; }
.extTitle{ font-weight:700; font-size:16px; letter-spacing:0.2px; }
.extSub{ opacity:.75; font-size:12px; margin-top:2px; }
.extMeta{ display:flex; gap:8px; align-items:center; }
.pill{ padding:6px 10px; border-radius:999px; font-size:12px; border:1px solid rgba(255,255,255,.10); background:rgba(255,255,255,.04); }
.pill.ok{ border-color: rgba(80,255,170,.25); background: rgba(80,255,170,.06); }
.pill.bad{ border-color: rgba(255,100,120,.25); background: rgba(255,100,120,.06); }
.pill.ghost{ opacity:.8; }

.extGrid{ margin-top:12px; display:flex; flex-direction:column; gap:10px; }
.extRow{
  display:grid;
  grid-template-columns: 140px 120px 1fr 78px;
  gap:10px;
  align-items:center;
  padding:10px 10px;
  border-radius:12px;
  border:1px solid rgba(255,255,255,.08);
  background: rgba(0,0,0,.18);
}
.extCoin{ font-weight:650; }
.extAmt{ font-variant-numeric: tabular-nums; opacity:.95; }
.extAddr{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; font-size:12px; opacity:.9; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.btnMini{
  padding:8px 10px;
  border-radius:10px;
  border:1px solid rgba(255,255,255,.10);
  background: rgba(255,255,255,.06);
  cursor:pointer;
}
.btnMini:hover{ background: rgba(255,255,255,.10); }
.extFoot{ display:flex; justify-content:space-between; align-items:center; gap:12px; margin-top:10px; }
.extHint{ opacity:.75; font-size:12px; }
.extSrc{ opacity:.6; font-size:12px; text-align:right; }
/* ====== /External wallets card ====== */
```

---

## FILE: /opt/logos/www/wallet_dev/_bak_bridge_20260107T102635Z/app.html

- bytes: 6358
- sha256: `229e539b9458b5519463197777c9c303d70c248878ecfa8c30ef69e1257850ee`

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta http-equiv="Cache-Control" content="no-store"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Wallet</title>
  <link rel="stylesheet" href="/shared/wallet-themeP260101_01"/>
  <link rel="stylesheet" href="./appP260101_01"/>
<script src="./api_base.js"></script>
<link rel="stylesheet" href="/shared/wallet-theme.css?v=20260101_02"/>
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

<!-- ====== External wallets (wallet-api) ====== -->
<div class="card extWalletCard" id="extWalletCard" style="display:none;">
  <div class="extHead">
    <div>
      <div class="extTitle">External wallets</div>
      <div class="extSub">BTC / ETH / TRX / USDT — on-chain balances (watch-only)</div>
    </div>
    <div class="extMeta">
      <span class="pill" id="extWalletStatus">connecting…</span>
      <span class="pill ghost" id="extWalletLatency">—</span>
    </div>
  </div>

  <div class="extGrid">
    <div class="extRow">
      <div class="extCoin">BTC</div>
      <div class="extAmt" id="bal_btc">—</div>
      <div class="extAddr" id="addr_btc">—</div>
      <button class="btnMini" data-copy="addr_btc">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">ETH</div>
      <div class="extAmt" id="bal_eth">—</div>
      <div class="extAddr" id="addr_eth">—</div>
      <button class="btnMini" data-copy="addr_eth">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">TRX</div>
      <div class="extAmt" id="bal_trx">—</div>
      <div class="extAddr" id="addr_trx">—</div>
      <button class="btnMini" data-copy="addr_trx">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">USDT (ERC-20)</div>
      <div class="extAmt" id="bal_usdt_erc20">—</div>
      <div class="extAddr" id="addr_usdt_erc20">—</div>
      <button class="btnMini" data-copy="addr_usdt_erc20">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">USDT (TRC-20)</div>
      <div class="extAmt" id="bal_usdt_trc20">—</div>
      <div class="extAddr" id="addr_usdt_trc20">—</div>
      <button class="btnMini" data-copy="addr_usdt_trc20">Copy</button>
    </div>
  </div>

  <div class="extFoot">
    <div class="extHint" id="extWalletHint">Tip: deposits show up automatically (refresh every ~15s).</div>
    <div class="extSrc" id="extWalletSources">—</div>
  </div>
</div>
<!-- ====== /External wallets ====== -->

</body>
</html>
```

---

## FILE: /opt/logos/www/wallet_dev/_bak_bridge_20260107T102635Z/app.js

- bytes: 16445
- sha256: `512531da4758ae0e55402363654e6ac8c586d32cd5d398319c1e497859d650f9`

```js
'use strict';

const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/node-api'));

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


/* ====== LOGOS_EXT_WALLET_UI (wallet-api balances) ====== */
(() => {
  const ORIGIN = (location.origin || "").replace(/\/$/, "");
  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");

  const $ = (id) => document.getElementById(id);
  const show = (el, on=true) => { if (el) el.style.display = on ? "" : "none"; };

  const trunc = (s, a=8, b=6) => {
    if (!s || typeof s !== "string") return "—";
    if (s.length <= a+b+3) return s;
    return s.slice(0,a) + "…" + s.slice(-b);
  };

  const safeNum = (x) => {
    const n = Number(x);
    return Number.isFinite(n) ? n : 0;
  };

  const fmtFixed = (n, d=6) => {
    try {
      return safeNum(n).toFixed(d).replace(/\.?0+$/, "");
    } catch {
      return String(n ?? "0");
    }
  };

  const satToBtc = (sat) => safeNum(sat) / 1e8;
  const weiToEth = (wei) => safeNum(wei) / 1e18;

  const getRID = () => {
    // подстрахуемся под разные ключи
    return (
      localStorage.getItem("RID") ||
      localStorage.getItem("rid") ||
      localStorage.getItem("logos_rid") ||
      ""
    ).trim();
  };

  const apiGet = async (url, timeoutMs=8000) => {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), timeoutMs);
    try {
      const r = await fetch(url, { signal: ctrl.signal, credentials: "omit" });
      if (!r.ok) throw new Error("HTTP " + r.status);
      return await r.json();
    } finally {
      clearTimeout(t);
    }
  };

  const bindCopyButtons = () => {
    document.querySelectorAll("[data-copy]").forEach((btn) => {
      if (btn.dataset.bound) return;
      btn.dataset.bound = "1";
      btn.addEventListener("click", async () => {
        const id = btn.getAttribute("data-copy");
        const el = $(id);
        const full = el ? (el.dataset.full || el.textContent || "") : "";
        if (!full || full === "—") return;
        try {
          await navigator.clipboard.writeText(full);
          const prev = btn.textContent;
          btn.textContent = "Copied";
          setTimeout(() => (btn.textContent = prev), 900);
        } catch {}
      });
    });
  };

  const setStatus = (ok, text) => {
    const s = $("extWalletStatus");
    if (!s) return;
    s.classList.remove("ok", "bad");
    s.classList.add(ok ? "ok" : "bad");
    s.textContent = text;
  };

  const setLatency = (ms) => {
    const el = $("extWalletLatency");
    if (!el) return;
    el.textContent = (ms != null) ? (ms + " ms") : "—";
  };

  const setAddr = (id, val) => {
    const el = $(id);
    if (!el) return;
    el.dataset.full = val || "";
    el.textContent = trunc(val || "");
  };

  const setAmt = (id, val) => {
    const el = $(id);
    if (!el) return;
    el.textContent = val;
  };

  const render = (payload) => {
    const a = payload.addresses || {};
    const b = payload.balances || {};
    setAddr("addr_btc", a.BTC);
    setAddr("addr_eth", a.ETH);
    setAddr("addr_trx", a.TRON);
    setAddr("addr_usdt_erc20", a.USDT_ERC20 || a.ETH);
    setAddr("addr_usdt_trc20", a.USDT_TRC20 || a.TRON);

    if (b.BTC) {
      setAmt("bal_btc", fmtFixed(satToBtc(b.BTC.total_sat || 0), 8) + " BTC");
    }
    if (b.ETH) {
      setAmt("bal_eth", fmtFixed(weiToEth(b.ETH.wei || 0), 6) + " ETH");
      const u = (b.ETH.usdt_erc20 || {});
      setAmt("bal_usdt_erc20", fmtFixed((safeNum(u.raw || 0) / 1e6), 2) + " USDT");
    }
    if (b.TRON) {
      setAmt("bal_trx", fmtFixed((safeNum(b.TRON.sun || 0) / 1e6), 6) + " TRX");
      const u = (b.TRON.usdt_trc20 || {});
      // raw может быть null если API не вернул токены — считаем 0
      setAmt("bal_usdt_trc20", fmtFixed((safeNum(u.raw || 0) / 1e6), 2) + " USDT");
    }

    const src = $("extWalletSources");
    if (src) {
      const sBTC = b.BTC?.source || "—";
      const sETH = b.ETH?.source || "—";
      const sTR  = b.TRON?.source || "—";
      src.textContent = `Sources: BTC=${sBTC} · ETH=${sETH} · TRON=${sTR}`;
    }

    setLatency(payload.latency_ms);
  };

  const tick = async () => {
    const rid = getRID();
    const card = $("extWalletCard");
    if (!rid) { show(card, false); return; }
    show(card, true);
    bindCopyButtons();

    try {
      setStatus(true, "updating…");
      // balances уже включает addresses, но на всякий страх — дернём receive один раз при первом показе
      const data = await apiGet(`${WALLET_API}/v1/balances/${encodeURIComponent(rid)}`, 12000);
      render(data);
      setStatus(true, "live");
    } catch (e) {
      setStatus(false, "offline");
    }
  };

  // старт
  setTimeout(() => tick(), 250);
  setInterval(() => tick(), 15000);

  window.LOGOS_EXT_WALLET_UI = { tick };
})();
 /* ====== /LOGOS_EXT_WALLET_UI ====== */
```

---

## FILE: /opt/logos/www/wallet_dev/_bak_bridge_20260107T102822Z/app.css

- bytes: 2892
- sha256: `e067ac77ebcdf94fa36dc61e7c51faaee8cb264f8e3086ae60f6047215c12e68`

```css
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


/* ====== External wallets card ====== */
.extWalletCard{ margin-top:16px; }
.extHead{ display:flex; align-items:flex-start; justify-content:space-between; gap:12px; }
.extTitle{ font-weight:700; font-size:16px; letter-spacing:0.2px; }
.extSub{ opacity:.75; font-size:12px; margin-top:2px; }
.extMeta{ display:flex; gap:8px; align-items:center; }
.pill{ padding:6px 10px; border-radius:999px; font-size:12px; border:1px solid rgba(255,255,255,.10); background:rgba(255,255,255,.04); }
.pill.ok{ border-color: rgba(80,255,170,.25); background: rgba(80,255,170,.06); }
.pill.bad{ border-color: rgba(255,100,120,.25); background: rgba(255,100,120,.06); }
.pill.ghost{ opacity:.8; }

.extGrid{ margin-top:12px; display:flex; flex-direction:column; gap:10px; }
.extRow{
  display:grid;
  grid-template-columns: 140px 120px 1fr 78px;
  gap:10px;
  align-items:center;
  padding:10px 10px;
  border-radius:12px;
  border:1px solid rgba(255,255,255,.08);
  background: rgba(0,0,0,.18);
}
.extCoin{ font-weight:650; }
.extAmt{ font-variant-numeric: tabular-nums; opacity:.95; }
.extAddr{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; font-size:12px; opacity:.9; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.btnMini{
  padding:8px 10px;
  border-radius:10px;
  border:1px solid rgba(255,255,255,.10);
  background: rgba(255,255,255,.06);
  cursor:pointer;
}
.btnMini:hover{ background: rgba(255,255,255,.10); }
.extFoot{ display:flex; justify-content:space-between; align-items:center; gap:12px; margin-top:10px; }
.extHint{ opacity:.75; font-size:12px; }
.extSrc{ opacity:.6; font-size:12px; text-align:right; }
/* ====== /External wallets card ====== */


/* ====== Bridge result box ====== */
.bridgeResult{
  margin-top:10px;
  padding:10px 12px;
  border-radius:12px;
  border:1px solid rgba(255,255,255,.10);
  background: rgba(0,0,0,.18);
  font-size:12px;
  line-height:1.35;
  white-space:pre-wrap;
}
.bridgeResult.ok{ border-color: rgba(80,255,170,.25); background: rgba(80,255,170,.06); }
.bridgeResult.bad{ border-color: rgba(255,100,120,.25); background: rgba(255,100,120,.06); }
/* ====== /Bridge result box ====== */
```

---

## FILE: /opt/logos/www/wallet_dev/_bak_bridge_20260107T102822Z/app.html

- bytes: 6433
- sha256: `1ef0ae58a9af795c54d5fc50d283309c20bc9741fb60d395fb930c80f3babb3c`

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta http-equiv="Cache-Control" content="no-store"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Wallet</title>
  <link rel="stylesheet" href="/shared/wallet-themeP260101_01"/>
  <link rel="stylesheet" href="./appP260101_01"/>
<script src="./api_base.js"></script>
<link rel="stylesheet" href="/shared/wallet-theme.css?v=20260101_02"/>
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

<!-- ====== External wallets (wallet-api) ====== -->
<div class="card extWalletCard" id="extWalletCard" style="display:none;">
  <div class="extHead">
    <div>
      <div class="extTitle">External wallets</div>
      <div class="extSub">BTC / ETH / TRX / USDT — on-chain balances (watch-only)</div>
    </div>
    <div class="extMeta">
      <span class="pill" id="extWalletStatus">connecting…</span>
      <span class="pill ghost" id="extWalletLatency">—</span>
    </div>
  </div>

  <div class="extGrid">
    <div class="extRow">
      <div class="extCoin">BTC</div>
      <div class="extAmt" id="bal_btc">—</div>
      <div class="extAddr" id="addr_btc">—</div>
      <button class="btnMini" data-copy="addr_btc">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">ETH</div>
      <div class="extAmt" id="bal_eth">—</div>
      <div class="extAddr" id="addr_eth">—</div>
      <button class="btnMini" data-copy="addr_eth">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">TRX</div>
      <div class="extAmt" id="bal_trx">—</div>
      <div class="extAddr" id="addr_trx">—</div>
      <button class="btnMini" data-copy="addr_trx">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">USDT (ERC-20)</div>
      <div class="extAmt" id="bal_usdt_erc20">—</div>
      <div class="extAddr" id="addr_usdt_erc20">—</div>
      <button class="btnMini" data-copy="addr_usdt_erc20">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">USDT (TRC-20)</div>
      <div class="extAmt" id="bal_usdt_trc20">—</div>
      <div class="extAddr" id="addr_usdt_trc20">—</div>
      <button class="btnMini" data-copy="addr_usdt_trc20">Copy</button>
    </div>
  </div>

  <div class="extFoot">
    <div class="extHint" id="extWalletHint">Tip: deposits show up automatically (refresh every ~15s).</div>
    <div class="extSrc" id="extWalletSources">—</div>
  </div>
</div>
<!-- ====== /External wallets ====== -->


<div class="bridgeResult" id="bridgeResult" style="display:none;"></div>

</body>
</html>
```

---

## FILE: /opt/logos/www/wallet_dev/_bak_bridge_20260107T102822Z/app.js

- bytes: 21990
- sha256: `1a7eb3bfa116e1c2bfa84ac76ff16013ac50973001abd5af9a235b427961baa7`

```js
'use strict';

const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/node-api'));

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


/* ====== LOGOS_EXT_WALLET_UI (wallet-api balances) ====== */
(() => {
  const ORIGIN = (location.origin || "").replace(/\/$/, "");
  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");

  const $ = (id) => document.getElementById(id);
  const show = (el, on=true) => { if (el) el.style.display = on ? "" : "none"; };

  const trunc = (s, a=8, b=6) => {
    if (!s || typeof s !== "string") return "—";
    if (s.length <= a+b+3) return s;
    return s.slice(0,a) + "…" + s.slice(-b);
  };

  const safeNum = (x) => {
    const n = Number(x);
    return Number.isFinite(n) ? n : 0;
  };

  const fmtFixed = (n, d=6) => {
    try {
      return safeNum(n).toFixed(d).replace(/\.?0+$/, "");
    } catch {
      return String(n ?? "0");
    }
  };

  const satToBtc = (sat) => safeNum(sat) / 1e8;
  const weiToEth = (wei) => safeNum(wei) / 1e18;

  const getRID = () => {
    // подстрахуемся под разные ключи
    return (
      localStorage.getItem("RID") ||
      localStorage.getItem("rid") ||
      localStorage.getItem("logos_rid") ||
      ""
    ).trim();
  };

  const apiGet = async (url, timeoutMs=8000) => {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), timeoutMs);
    try {
      const r = await fetch(url, { signal: ctrl.signal, credentials: "omit" });
      if (!r.ok) throw new Error("HTTP " + r.status);
      return await r.json();
    } finally {
      clearTimeout(t);
    }
  };

  const bindCopyButtons = () => {
    document.querySelectorAll("[data-copy]").forEach((btn) => {
      if (btn.dataset.bound) return;
      btn.dataset.bound = "1";
      btn.addEventListener("click", async () => {
        const id = btn.getAttribute("data-copy");
        const el = $(id);
        const full = el ? (el.dataset.full || el.textContent || "") : "";
        if (!full || full === "—") return;
        try {
          await navigator.clipboard.writeText(full);
          const prev = btn.textContent;
          btn.textContent = "Copied";
          setTimeout(() => (btn.textContent = prev), 900);
        } catch {}
      });
    });
  };

  const setStatus = (ok, text) => {
    const s = $("extWalletStatus");
    if (!s) return;
    s.classList.remove("ok", "bad");
    s.classList.add(ok ? "ok" : "bad");
    s.textContent = text;
  };

  const setLatency = (ms) => {
    const el = $("extWalletLatency");
    if (!el) return;
    el.textContent = (ms != null) ? (ms + " ms") : "—";
  };

  const setAddr = (id, val) => {
    const el = $(id);
    if (!el) return;
    el.dataset.full = val || "";
    el.textContent = trunc(val || "");
  };

  const setAmt = (id, val) => {
    const el = $(id);
    if (!el) return;
    el.textContent = val;
  };

  const render = (payload) => {
    const a = payload.addresses || {};
    const b = payload.balances || {};
    setAddr("addr_btc", a.BTC);
    setAddr("addr_eth", a.ETH);
    setAddr("addr_trx", a.TRON);
    setAddr("addr_usdt_erc20", a.USDT_ERC20 || a.ETH);
    setAddr("addr_usdt_trc20", a.USDT_TRC20 || a.TRON);

    if (b.BTC) {
      setAmt("bal_btc", fmtFixed(satToBtc(b.BTC.total_sat || 0), 8) + " BTC");
    }
    if (b.ETH) {
      setAmt("bal_eth", fmtFixed(weiToEth(b.ETH.wei || 0), 6) + " ETH");
      const u = (b.ETH.usdt_erc20 || {});
      setAmt("bal_usdt_erc20", fmtFixed((safeNum(u.raw || 0) / 1e6), 2) + " USDT");
    }
    if (b.TRON) {
      setAmt("bal_trx", fmtFixed((safeNum(b.TRON.sun || 0) / 1e6), 6) + " TRX");
      const u = (b.TRON.usdt_trc20 || {});
      // raw может быть null если API не вернул токены — считаем 0
      setAmt("bal_usdt_trc20", fmtFixed((safeNum(u.raw || 0) / 1e6), 2) + " USDT");
    }

    const src = $("extWalletSources");
    if (src) {
      const sBTC = b.BTC?.source || "—";
      const sETH = b.ETH?.source || "—";
      const sTR  = b.TRON?.source || "—";
      src.textContent = `Sources: BTC=${sBTC} · ETH=${sETH} · TRON=${sTR}`;
    }

    setLatency(payload.latency_ms);
  };

  const tick = async () => {
    const rid = getRID();
    const card = $("extWalletCard");
    if (!rid) { show(card, false); return; }
    show(card, true);
    bindCopyButtons();

    try {
      setStatus(true, "updating…");
      // balances уже включает addresses, но на всякий страх — дернём receive один раз при первом показе
      const data = await apiGet(`${WALLET_API}/v1/balances/${encodeURIComponent(rid)}`, 12000);
      render(data);
      setStatus(true, "live");
    } catch (e) {
      setStatus(false, "offline");
    }
  };

  // старт
  setTimeout(() => tick(), 250);
  setInterval(() => tick(), 15000);

  window.LOGOS_EXT_WALLET_UI = { tick };
})();
 /* ====== /LOGOS_EXT_WALLET_UI ====== */


/* ====== LOGOS_BRIDGE_UI_BIND (auto-detect bridge endpoints from wallet-api openapi) ====== */
(() => {
  const ORIGIN = (location.origin || "").replace(/\/$/, "");
  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");

  const $ = (id) => document.getElementById(id);
  const rid = () =>
    (localStorage.getItem("RID") || localStorage.getItem("rid") || localStorage.getItem("logos_rid") || "").trim();

  const showResult = (ok, text) => {
    const box = $("bridgeResult");
    if (!box) return;
    box.style.display = "";
    box.classList.remove("ok","bad");
    box.classList.add(ok ? "ok" : "bad");
    box.textContent = text;
  };

  const apiGet = async (url, timeoutMs=12000) => {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), timeoutMs);
    try {
      const r = await fetch(url, { signal: ctrl.signal, credentials:"omit" });
      if (!r.ok) throw new Error("HTTP " + r.status);
      return await r.json();
    } finally { clearTimeout(t); }
  };

  const apiPost = async (url, body, timeoutMs=20000) => {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), timeoutMs);
    try {
      const r = await fetch(url, {
        method:"POST",
        headers:{ "Content-Type":"application/json" },
        body: JSON.stringify(body),
        signal: ctrl.signal,
        credentials:"omit",
      });
      const txt = await r.text();
      let data = null;
      try { data = JSON.parse(txt); } catch {}
      if (!r.ok) throw new Error("HTTP " + r.status + (txt ? (": " + txt.slice(0,300)) : ""));
      return data ?? { ok:true, raw: txt };
    } finally { clearTimeout(t); }
  };

  const normDir = (v) => (v || "").trim();
  const normChain = (v) => (v || "").trim();
  const normAmt = (v) => {
    const n = Number(String(v||"").replace(",", "."));
    return Number.isFinite(n) ? n : 0;
  };

  // --- autodetect endpoints
  let EP = { quote:null, create:null, status:null, openapi:null };

  const detectEndpoints = async () => {
    if (EP.openapi) return EP;
    try {
      const spec = await apiGet(`${WALLET_API}/openapi.json`, 12000);
      EP.openapi = spec;

      const paths = Object.keys(spec.paths || {});
      const cand = (re) => paths.filter(p => re.test(p)).sort();

      // ищем популярные варианты
      const quote = cand(/quote/i).find(p => /bridge|swap|rlgn|convert/i.test(p)) || cand(/bridge.*quote/i)[0] || cand(/quote/i)[0];
      const create = cand(/create|request|order|swap/i).find(p => /bridge|swap|rlgn|convert/i.test(p)) || cand(/bridge.*(create|request|order)/i)[0];
      const status = cand(/status|order/i).find(p => /bridge|swap|rlgn|convert/i.test(p)) || null;

      EP.quote = quote || null;
      EP.create = create || null;
      EP.status = status || null;

      return EP;
    } catch (e) {
      // fallback (если openapi не отдался)
      EP.quote  = "/v1/bridge/quote";
      EP.create = "/v1/bridge/create";
      EP.status = "/v1/bridge/status";
      return EP;
    }
  };

  const readForm = () => {
    const r = rid();
    if (!r) throw new Error("RID not found. Create/restore RID first.");
    const direction = normDir($("bridge_direction")?.value);
    const chain = normChain($("bridge_chain")?.value);
    const amount = normAmt($("bridge_amount")?.value);
    const ext_txid = ($("bridge_ext_txid")?.value || "").trim();

    return { rid: r, direction, chain, amount, ext_txid };
  };

  const doQuote = async () => {
    const ep = await detectEndpoints();
    if (!ep.quote) throw new Error("Bridge quote endpoint not found in openapi.");
    const f = readForm();

    // минимальный payload (без мусора)
    const body = {
      rid: f.rid,
      direction: f.direction,
      chain: f.chain,
      amount: f.amount,
      ext_txid: f.ext_txid || undefined,
    };

    const t0 = performance.now();
    const res = await apiPost(`${WALLET_API}${ep.quote}`, body, 20000);
    const ms = Math.round(performance.now() - t0);

    showResult(true, `[QUOTE ✅] ${ms} ms\n` + JSON.stringify(res, null, 2));
  };

  const doCreate = async () => {
    const ep = await detectEndpoints();
    if (!ep.create) throw new Error("Bridge create endpoint not found in openapi.");
    const f = readForm();

    const body = {
      rid: f.rid,
      direction: f.direction,
      chain: f.chain,
      amount: f.amount,
      ext_txid: f.ext_txid || undefined,
    };

    const t0 = performance.now();
    const res = await apiPost(`${WALLET_API}${ep.create}`, body, 25000);
    const ms = Math.round(performance.now() - t0);

    showResult(true, `[CREATE ✅] ${ms} ms\n` + JSON.stringify(res, null, 2));
  };

  const bind = () => {
    const bq = $("b_bridge_quote");
    const bc = $("b_bridge_create");
    if (bq && !bq.dataset.bound) {
      bq.dataset.bound = "1";
      bq.addEventListener("click", async () => {
        try { showResult(true, "Calculating…"); await doQuote(); }
        catch (e) { showResult(false, "[QUOTE ❌]\n" + (e?.message || String(e))); }
      });
    }
    if (bc && !bc.dataset.bound) {
      bc.dataset.bound = "1";
      bc.addEventListener("click", async () => {
        try { showResult(true, "Creating…"); await doCreate(); }
        catch (e) { showResult(false, "[CREATE ❌]\n" + (e?.message || String(e))); }
      });
    }
  };

  setTimeout(bind, 300);
  window.LOGOS_BRIDGE_UI_BIND = { bind };
})();
 /* ====== /LOGOS_BRIDGE_UI_BIND ====== */
```

---

## FILE: /opt/logos/www/wallet_dev/_bak_entry_20260107T105554Z/index.html

- bytes: 7139
- sha256: `e426c27de94ac41eff08bc17823297f455eb4f004ab39ade2affba21e99928bc`

```html
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

---

## FILE: /opt/logos/www/wallet_dev/_bak_entry_20260108T142703Z/index.html

- bytes: 6433
- sha256: `1ef0ae58a9af795c54d5fc50d283309c20bc9741fb60d395fb930c80f3babb3c`

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta http-equiv="Cache-Control" content="no-store"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Wallet</title>
  <link rel="stylesheet" href="/shared/wallet-themeP260101_01"/>
  <link rel="stylesheet" href="./appP260101_01"/>
<script src="./api_base.js"></script>
<link rel="stylesheet" href="/shared/wallet-theme.css?v=20260101_02"/>
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

<!-- ====== External wallets (wallet-api) ====== -->
<div class="card extWalletCard" id="extWalletCard" style="display:none;">
  <div class="extHead">
    <div>
      <div class="extTitle">External wallets</div>
      <div class="extSub">BTC / ETH / TRX / USDT — on-chain balances (watch-only)</div>
    </div>
    <div class="extMeta">
      <span class="pill" id="extWalletStatus">connecting…</span>
      <span class="pill ghost" id="extWalletLatency">—</span>
    </div>
  </div>

  <div class="extGrid">
    <div class="extRow">
      <div class="extCoin">BTC</div>
      <div class="extAmt" id="bal_btc">—</div>
      <div class="extAddr" id="addr_btc">—</div>
      <button class="btnMini" data-copy="addr_btc">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">ETH</div>
      <div class="extAmt" id="bal_eth">—</div>
      <div class="extAddr" id="addr_eth">—</div>
      <button class="btnMini" data-copy="addr_eth">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">TRX</div>
      <div class="extAmt" id="bal_trx">—</div>
      <div class="extAddr" id="addr_trx">—</div>
      <button class="btnMini" data-copy="addr_trx">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">USDT (ERC-20)</div>
      <div class="extAmt" id="bal_usdt_erc20">—</div>
      <div class="extAddr" id="addr_usdt_erc20">—</div>
      <button class="btnMini" data-copy="addr_usdt_erc20">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">USDT (TRC-20)</div>
      <div class="extAmt" id="bal_usdt_trc20">—</div>
      <div class="extAddr" id="addr_usdt_trc20">—</div>
      <button class="btnMini" data-copy="addr_usdt_trc20">Copy</button>
    </div>
  </div>

  <div class="extFoot">
    <div class="extHint" id="extWalletHint">Tip: deposits show up automatically (refresh every ~15s).</div>
    <div class="extSrc" id="extWalletSources">—</div>
  </div>
</div>
<!-- ====== /External wallets ====== -->


<div class="bridgeResult" id="bridgeResult" style="display:none;"></div>

</body>
</html>
```

---

## FILE: /opt/logos/www/wallet_dev/_bak_premiumtabs_20260109T063827Z/app.html

- bytes: 6471
- sha256: `6031e62b982d6c0add7134977868ddb949eb12cb3b0bdb542d6a41a6507b8fd5`

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta http-equiv="Cache-Control" content="no-store"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Wallet</title>
  <link rel="stylesheet" href="/shared/wallet-themeP260101_01"/>
  <link rel="stylesheet" href="./appP260101_01"/>
<script src="./api_base.js"></script>
<link rel="stylesheet" href="/shared/wallet-theme.css?v=20260101_02"/>
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

<!-- ====== External wallets (wallet-api) ====== -->
<div class="card extWalletCard" id="extWalletCard" style="display:none;">
  <div class="extHead">
    <div>
      <div class="extTitle">External wallets</div>
      <div class="extSub">BTC / ETH / TRX / USDT — on-chain balances (watch-only)</div>
    </div>
    <div class="extMeta">
      <span class="pill" id="extWalletStatus">connecting…</span>
      <span class="pill ghost" id="extWalletLatency">—</span>
    </div>
  </div>

  <div class="extGrid">
    <div class="extRow">
      <div class="extCoin">BTC</div>
      <div class="extAmt" id="bal_btc">—</div>
      <div class="extAddr" id="addr_btc">—</div>
      <button class="btnMini" data-copy="addr_btc">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">ETH</div>
      <div class="extAmt" id="bal_eth">—</div>
      <div class="extAddr" id="addr_eth">—</div>
      <button class="btnMini" data-copy="addr_eth">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">TRX</div>
      <div class="extAmt" id="bal_trx">—</div>
      <div class="extAddr" id="addr_trx">—</div>
      <button class="btnMini" data-copy="addr_trx">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">USDT (ERC-20)</div>
      <div class="extAmt" id="bal_usdt_erc20">—</div>
      <div class="extAddr" id="addr_usdt_erc20">—</div>
      <button class="btnMini" data-copy="addr_usdt_erc20">Copy</button>
    </div>

    <div class="extRow">
      <div class="extCoin">USDT (TRC-20)</div>
      <div class="extAmt" id="bal_usdt_trc20">—</div>
      <div class="extAddr" id="addr_usdt_trc20">—</div>
      <button class="btnMini" data-copy="addr_usdt_trc20">Copy</button>
    </div>
  </div>

  <div class="extFoot">
    <div class="extHint" id="extWalletHint">Tip: deposits show up automatically (refresh every ~15s).</div>
    <div class="extSrc" id="extWalletSources">—</div>
  </div>
</div>
<!-- ====== /External wallets ====== -->


<div class="bridgeResult" id="bridgeResult" style="display:none;"></div>

<script src="assets.js?v=1"></script>
</body>
</html>
```

---

## FILE: /opt/logos/www/wallet_dev/_bak_premiumtabs_20260109T063827Z/app.js

- bytes: 21990
- sha256: `1a7eb3bfa116e1c2bfa84ac76ff16013ac50973001abd5af9a235b427961baa7`

```js
'use strict';

const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/node-api'));

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


/* ====== LOGOS_EXT_WALLET_UI (wallet-api balances) ====== */
(() => {
  const ORIGIN = (location.origin || "").replace(/\/$/, "");
  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");

  const $ = (id) => document.getElementById(id);
  const show = (el, on=true) => { if (el) el.style.display = on ? "" : "none"; };

  const trunc = (s, a=8, b=6) => {
    if (!s || typeof s !== "string") return "—";
    if (s.length <= a+b+3) return s;
    return s.slice(0,a) + "…" + s.slice(-b);
  };

  const safeNum = (x) => {
    const n = Number(x);
    return Number.isFinite(n) ? n : 0;
  };

  const fmtFixed = (n, d=6) => {
    try {
      return safeNum(n).toFixed(d).replace(/\.?0+$/, "");
    } catch {
      return String(n ?? "0");
    }
  };

  const satToBtc = (sat) => safeNum(sat) / 1e8;
  const weiToEth = (wei) => safeNum(wei) / 1e18;

  const getRID = () => {
    // подстрахуемся под разные ключи
    return (
      localStorage.getItem("RID") ||
      localStorage.getItem("rid") ||
      localStorage.getItem("logos_rid") ||
      ""
    ).trim();
  };

  const apiGet = async (url, timeoutMs=8000) => {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), timeoutMs);
    try {
      const r = await fetch(url, { signal: ctrl.signal, credentials: "omit" });
      if (!r.ok) throw new Error("HTTP " + r.status);
      return await r.json();
    } finally {
      clearTimeout(t);
    }
  };

  const bindCopyButtons = () => {
    document.querySelectorAll("[data-copy]").forEach((btn) => {
      if (btn.dataset.bound) return;
      btn.dataset.bound = "1";
      btn.addEventListener("click", async () => {
        const id = btn.getAttribute("data-copy");
        const el = $(id);
        const full = el ? (el.dataset.full || el.textContent || "") : "";
        if (!full || full === "—") return;
        try {
          await navigator.clipboard.writeText(full);
          const prev = btn.textContent;
          btn.textContent = "Copied";
          setTimeout(() => (btn.textContent = prev), 900);
        } catch {}
      });
    });
  };

  const setStatus = (ok, text) => {
    const s = $("extWalletStatus");
    if (!s) return;
    s.classList.remove("ok", "bad");
    s.classList.add(ok ? "ok" : "bad");
    s.textContent = text;
  };

  const setLatency = (ms) => {
    const el = $("extWalletLatency");
    if (!el) return;
    el.textContent = (ms != null) ? (ms + " ms") : "—";
  };

  const setAddr = (id, val) => {
    const el = $(id);
    if (!el) return;
    el.dataset.full = val || "";
    el.textContent = trunc(val || "");
  };

  const setAmt = (id, val) => {
    const el = $(id);
    if (!el) return;
    el.textContent = val;
  };

  const render = (payload) => {
    const a = payload.addresses || {};
    const b = payload.balances || {};
    setAddr("addr_btc", a.BTC);
    setAddr("addr_eth", a.ETH);
    setAddr("addr_trx", a.TRON);
    setAddr("addr_usdt_erc20", a.USDT_ERC20 || a.ETH);
    setAddr("addr_usdt_trc20", a.USDT_TRC20 || a.TRON);

    if (b.BTC) {
      setAmt("bal_btc", fmtFixed(satToBtc(b.BTC.total_sat || 0), 8) + " BTC");
    }
    if (b.ETH) {
      setAmt("bal_eth", fmtFixed(weiToEth(b.ETH.wei || 0), 6) + " ETH");
      const u = (b.ETH.usdt_erc20 || {});
      setAmt("bal_usdt_erc20", fmtFixed((safeNum(u.raw || 0) / 1e6), 2) + " USDT");
    }
    if (b.TRON) {
      setAmt("bal_trx", fmtFixed((safeNum(b.TRON.sun || 0) / 1e6), 6) + " TRX");
      const u = (b.TRON.usdt_trc20 || {});
      // raw может быть null если API не вернул токены — считаем 0
      setAmt("bal_usdt_trc20", fmtFixed((safeNum(u.raw || 0) / 1e6), 2) + " USDT");
    }

    const src = $("extWalletSources");
    if (src) {
      const sBTC = b.BTC?.source || "—";
      const sETH = b.ETH?.source || "—";
      const sTR  = b.TRON?.source || "—";
      src.textContent = `Sources: BTC=${sBTC} · ETH=${sETH} · TRON=${sTR}`;
    }

    setLatency(payload.latency_ms);
  };

  const tick = async () => {
    const rid = getRID();
    const card = $("extWalletCard");
    if (!rid) { show(card, false); return; }
    show(card, true);
    bindCopyButtons();

    try {
      setStatus(true, "updating…");
      // balances уже включает addresses, но на всякий страх — дернём receive один раз при первом показе
      const data = await apiGet(`${WALLET_API}/v1/balances/${encodeURIComponent(rid)}`, 12000);
      render(data);
      setStatus(true, "live");
    } catch (e) {
      setStatus(false, "offline");
    }
  };

  // старт
  setTimeout(() => tick(), 250);
  setInterval(() => tick(), 15000);

  window.LOGOS_EXT_WALLET_UI = { tick };
})();
 /* ====== /LOGOS_EXT_WALLET_UI ====== */


/* ====== LOGOS_BRIDGE_UI_BIND (auto-detect bridge endpoints from wallet-api openapi) ====== */
(() => {
  const ORIGIN = (location.origin || "").replace(/\/$/, "");
  const WALLET_API = (window.LOGOS_WALLET_API || (ORIGIN + "/wallet-api")).replace(/\/$/, "");

  const $ = (id) => document.getElementById(id);
  const rid = () =>
    (localStorage.getItem("RID") || localStorage.getItem("rid") || localStorage.getItem("logos_rid") || "").trim();

  const showResult = (ok, text) => {
    const box = $("bridgeResult");
    if (!box) return;
    box.style.display = "";
    box.classList.remove("ok","bad");
    box.classList.add(ok ? "ok" : "bad");
    box.textContent = text;
  };

  const apiGet = async (url, timeoutMs=12000) => {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), timeoutMs);
    try {
      const r = await fetch(url, { signal: ctrl.signal, credentials:"omit" });
      if (!r.ok) throw new Error("HTTP " + r.status);
      return await r.json();
    } finally { clearTimeout(t); }
  };

  const apiPost = async (url, body, timeoutMs=20000) => {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), timeoutMs);
    try {
      const r = await fetch(url, {
        method:"POST",
        headers:{ "Content-Type":"application/json" },
        body: JSON.stringify(body),
        signal: ctrl.signal,
        credentials:"omit",
      });
      const txt = await r.text();
      let data = null;
      try { data = JSON.parse(txt); } catch {}
      if (!r.ok) throw new Error("HTTP " + r.status + (txt ? (": " + txt.slice(0,300)) : ""));
      return data ?? { ok:true, raw: txt };
    } finally { clearTimeout(t); }
  };

  const normDir = (v) => (v || "").trim();
  const normChain = (v) => (v || "").trim();
  const normAmt = (v) => {
    const n = Number(String(v||"").replace(",", "."));
    return Number.isFinite(n) ? n : 0;
  };

  // --- autodetect endpoints
  let EP = { quote:null, create:null, status:null, openapi:null };

  const detectEndpoints = async () => {
    if (EP.openapi) return EP;
    try {
      const spec = await apiGet(`${WALLET_API}/openapi.json`, 12000);
      EP.openapi = spec;

      const paths = Object.keys(spec.paths || {});
      const cand = (re) => paths.filter(p => re.test(p)).sort();

      // ищем популярные варианты
      const quote = cand(/quote/i).find(p => /bridge|swap|rlgn|convert/i.test(p)) || cand(/bridge.*quote/i)[0] || cand(/quote/i)[0];
      const create = cand(/create|request|order|swap/i).find(p => /bridge|swap|rlgn|convert/i.test(p)) || cand(/bridge.*(create|request|order)/i)[0];
      const status = cand(/status|order/i).find(p => /bridge|swap|rlgn|convert/i.test(p)) || null;

      EP.quote = quote || null;
      EP.create = create || null;
      EP.status = status || null;

      return EP;
    } catch (e) {
      // fallback (если openapi не отдался)
      EP.quote  = "/v1/bridge/quote";
      EP.create = "/v1/bridge/create";
      EP.status = "/v1/bridge/status";
      return EP;
    }
  };

  const readForm = () => {
    const r = rid();
    if (!r) throw new Error("RID not found. Create/restore RID first.");
    const direction = normDir($("bridge_direction")?.value);
    const chain = normChain($("bridge_chain")?.value);
    const amount = normAmt($("bridge_amount")?.value);
    const ext_txid = ($("bridge_ext_txid")?.value || "").trim();

    return { rid: r, direction, chain, amount, ext_txid };
  };

  const doQuote = async () => {
    const ep = await detectEndpoints();
    if (!ep.quote) throw new Error("Bridge quote endpoint not found in openapi.");
    const f = readForm();

    // минимальный payload (без мусора)
    const body = {
      rid: f.rid,
      direction: f.direction,
      chain: f.chain,
      amount: f.amount,
      ext_txid: f.ext_txid || undefined,
    };

    const t0 = performance.now();
    const res = await apiPost(`${WALLET_API}${ep.quote}`, body, 20000);
    const ms = Math.round(performance.now() - t0);

    showResult(true, `[QUOTE ✅] ${ms} ms\n` + JSON.stringify(res, null, 2));
  };

  const doCreate = async () => {
    const ep = await detectEndpoints();
    if (!ep.create) throw new Error("Bridge create endpoint not found in openapi.");
    const f = readForm();

    const body = {
      rid: f.rid,
      direction: f.direction,
      chain: f.chain,
      amount: f.amount,
      ext_txid: f.ext_txid || undefined,
    };

    const t0 = performance.now();
    const res = await apiPost(`${WALLET_API}${ep.create}`, body, 25000);
    const ms = Math.round(performance.now() - t0);

    showResult(true, `[CREATE ✅] ${ms} ms\n` + JSON.stringify(res, null, 2));
  };

  const bind = () => {
    const bq = $("b_bridge_quote");
    const bc = $("b_bridge_create");
    if (bq && !bq.dataset.bound) {
      bq.dataset.bound = "1";
      bq.addEventListener("click", async () => {
        try { showResult(true, "Calculating…"); await doQuote(); }
        catch (e) { showResult(false, "[QUOTE ❌]\n" + (e?.message || String(e))); }
      });
    }
    if (bc && !bc.dataset.bound) {
      bc.dataset.bound = "1";
      bc.addEventListener("click", async () => {
        try { showResult(true, "Creating…"); await doCreate(); }
        catch (e) { showResult(false, "[CREATE ❌]\n" + (e?.message || String(e))); }
      });
    }
  };

  setTimeout(bind, 300);
  window.LOGOS_BRIDGE_UI_BIND = { bind };
})();
 /* ====== /LOGOS_BRIDGE_UI_BIND ====== */
```

---

## FILE: /opt/logos/www/wallet_dev/_bak_premiumtabs_20260109T063827Z/ui.css

- bytes: 1311
- sha256: `6a31b47f2fcf4f8b71e0cbb041cc2529b7bc2a0fd815468fe28943444e272751`

```css

/* assets ui */
.assetsWrap{display:block;margin-top:16px}
.assetsHead{display:flex;gap:12px;align-items:center;justify-content:space-between;margin:8px 0 14px}
.assetsTitle{font-weight:800;font-size:20px;letter-spacing:.2px}
.assetsSub{margin-top:4px;color:rgba(255,255,255,.62);font-size:12px}
.assetsGrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
@media (max-width: 900px){.assetsGrid{grid-template-columns:1fr}}
.assetCard{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:18px;padding:14px;box-shadow:0 16px 50px rgba(0,0,0,.35);backdrop-filter: blur(16px)}
.assetTop{display:flex;gap:12px;align-items:center}
.assetSym{width:48px;height:48px;border-radius:14px;display:flex;align-items:center;justify-content:center;font-weight:800;
  background:radial-gradient(120% 120% at 30% 10%, rgba(78,124,255,.35), rgba(139,92,246,.25), rgba(0,0,0,0));
  border:1px solid rgba(255,255,255,.12)
}
.assetName{font-weight:700}
.assetBal{margin-top:2px;font-size:13px;color:rgba(255,255,255,.75)}
.assetAddrRow{margin-top:12px;display:flex;gap:10px;align-items:center;justify-content:space-between}
.assetAddr{max-width:70%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:rgba(255,255,255,.85)}
.assetNote{margin-top:10px;font-size:12px}
```

---

## FILE: /opt/logos/www/wallet_dev/_bak_ui_20260107T101342Z/app.css

- bytes: 682
- sha256: `2e8e444586c03fc5f72594fafb26e4ed1a8f1cba45d6214545e5b5ff1b5c49c4`

```css
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

---

## FILE: /opt/logos/www/wallet_dev/_bak_ui_20260107T101342Z/app.html

- bytes: 4330
- sha256: `2e661941b4940a64318028b1f2e7f5e1416368d4d6d108086e3e44c1980ff0ea`

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta http-equiv="Cache-Control" content="no-store"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Wallet</title>
  <link rel="stylesheet" href="/shared/wallet-themeP260101_01"/>
  <link rel="stylesheet" href="./appP260101_01"/>
<script src="./api_base.js"></script>
<link rel="stylesheet" href="/shared/wallet-theme.css?v=20260101_02"/>
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
</body>
</html>
```

---

## FILE: /opt/logos/www/wallet_dev/_bak_ui_20260107T101342Z/app.js

- bytes: 11592
- sha256: `297ab77d740c6f02befed611f151483809435b5cf6efba6e1c031efbeeaa698d`

```js
'use strict';

const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/node-api'));

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

---

## FILE: /opt/logos/www/wallet_dev/api_base.js

- bytes: 179
- sha256: `874ec5a42d3f847f1ee763e0c7b58eeed65d524de43769b4d12b955d1874ef75`

```js
(() => {
  // same-origin only
  window.API_BASE   = "/api";        // node backend (nginx -> 127.0.0.1:8080)
  window.WALLET_API = "/wallet-api"; // wallet proxy (FastAPI)
})();
```

---

## FILE: /opt/logos/www/wallet_dev/app.css

- bytes: 5169
- sha256: `3c7185635d3801bccc82f9a56334f0fb8a8c6806b18132ffaf882b127c6bb1ac`

```css
:root{
  --bg:#070a12; --txt:#e7ecff; --mut:#9aa7d9;
  --br:rgba(255,255,255,.10); --br2:rgba(255,255,255,.16);
  --acc:#6f7bff; --acc2:#9b5cff;
  --ok:#2dd4bf; --bad:#fb7185;
}
*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0;
  font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
  background:
    radial-gradient(1200px 700px at 20% 0%, rgba(111,123,255,.18), transparent 60%),
    radial-gradient(900px 600px at 80% 10%, rgba(155,92,255,.14), transparent 55%),
    linear-gradient(180deg, #050812, var(--bg));
  color:var(--txt);
}
.mono{font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace}
.wrap{max-width:1240px;margin:26px auto;padding:0 16px}
.card{
  background: linear-gradient(180deg, rgba(255,255,255,.045), rgba(255,255,255,.02));
  border:1px solid var(--br);
  border-radius:18px;
  padding:18px;
  box-shadow: 0 10px 30px rgba(0,0,0,.35);
  backdrop-filter: blur(10px);
}
.topbar{
  display:flex;align-items:center;justify-content:space-between;
  padding:14px 16px;border-bottom:1px solid var(--br);
  background: rgba(0,0,0,.25);
  position:sticky;top:0;z-index:10;
  backdrop-filter: blur(12px);
}
.brand{font-weight:800;letter-spacing:.4px}
.topbar-right{display:flex;gap:10px;align-items:center;flex-wrap:wrap;justify-content:flex-end}
.pill{
  border:1px solid var(--br2);
  padding:6px 10px;border-radius:999px;
  background: rgba(0,0,0,.25);
  font-size:12px;
}
.h1{font-size:20px;font-weight:800;margin:10px 0 6px}
.h2{font-size:16px;font-weight:800;margin:0 0 8px}
.muted{color:var(--mut);font-size:12px;line-height:1.35}
label{font-size:12px;color:var(--mut)}
input, select, textarea{
  width:100%;
  padding:12px 12px;
  border-radius:14px;
  border:1px solid var(--br);
  background: rgba(0,0,0,.28);
  color:var(--txt);
  outline:none;
}
textarea{min-height:92px;resize:vertical}
input:focus, select:focus, textarea:focus{border-color:rgba(111,123,255,.55)}
.row{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:10px}
.btn{
  border:1px solid var(--br2);
  background: rgba(0,0,0,.22);
  color:var(--txt);
  padding:10px 12px;
  border-radius:14px;
  cursor:pointer;
  user-select:none;
}
.btn.small{padding:8px 10px;border-radius:12px;font-size:12px}
.btn.primary{
  border-color: rgba(111,123,255,.55);
  background: linear-gradient(135deg, rgba(111,123,255,.35), rgba(155,92,255,.25));
}
.btn.danger{
  border-color: rgba(251,113,133,.55);
  background: rgba(251,113,133,.12);
}
.status{margin-top:10px;color:var(--mut);font-size:12px;min-height:16px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media (max-width: 980px){.grid{grid-template-columns:1fr}}
.big-num{font-size:30px;font-weight:900;letter-spacing:.4px}
.pre{white-space:pre-wrap;word-break:break-word;background:rgba(0,0,0,.24);border:1px solid var(--br);padding:12px;border-radius:14px;color:var(--txt)}
details{margin-top:10px}

.tabs{
  display:flex;gap:10px;flex-wrap:wrap;
  margin:14px 0 16px;
}
.tab{
  border:1px solid var(--br2);
  background: rgba(0,0,0,.18);
  padding:10px 14px;border-radius:999px;
  cursor:pointer;
  font-size:13px;
}
.tab.active{
  border-color: rgba(111,123,255,.55);
  background: linear-gradient(135deg, rgba(111,123,255,.22), rgba(155,92,255,.16));
}
.panel{display:none}
.panel.active{display:block}
.kv{
  display:grid;grid-template-columns: 1fr auto;gap:10px;align-items:center;
  padding:10px;border:1px solid var(--br);border-radius:14px;background:rgba(0,0,0,.18);
  margin-top:10px;
}
.kv .k{color:var(--mut);font-size:12px}
.kv .v{font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size:12px; overflow-wrap:anywhere}
.badge-ok{color:var(--ok)}
.badge-bad{color:var(--bad)}

/* ===== Settings module helpers ===== */
.devOnly { display:none !important; }
.dev .devOnly { display:block !important; }

.kvRow{
  display:flex; align-items:center; justify-content:space-between;
  gap:12px;
  padding:10px 12px;
  border:1px solid rgba(255,255,255,.06);
  border-radius:12px;
  background: rgba(0,0,0,.10);
}
.btnRow{ display:flex; gap:10px; flex-wrap:wrap; }
.btn.danger{ border-color: rgba(255,107,107,.6); }
.btn.danger:hover{ filter:brightness(1.08); }

/* switch */
.switch{ position:relative; display:inline-block; width:44px; height:24px; }
.switch input{ opacity:0; width:0; height:0; }
.slider{
  position:absolute; cursor:pointer; inset:0;
  background: rgba(255,255,255,.10);
  border:1px solid rgba(255,255,255,.10);
  transition:.2s;
  border-radius:999px;
}
.slider:before{
  position:absolute; content:"";
  height:18px; width:18px; left:3px; top:50%;
  transform: translateY(-50%);
  background: rgba(255,255,255,.85);
  transition:.2s;
  border-radius:999px;
}
.switch input:checked + .slider{
  background: rgba(120,110,255,.35);
  border-color: rgba(120,110,255,.55);
}
.switch input:checked + .slider:before{
  transform: translateY(-50%) translateX(20px);
}

/* ===== Send module helpers ===== */
.grid2{ display:grid; grid-template-columns: 1fr 1fr; gap:10px; }
@media (max-width: 780px){ .grid2{ grid-template-columns:1fr; } }
.btnRow{ display:flex; gap:10px; flex-wrap:wrap; }
```

---

## FILE: /opt/logos/www/wallet_dev/app.html

- bytes: 8074
- sha256: `604c188b22588f050e2aebc00a6e52417640cbd5d85bcddfee387da4522cfeff`

```html
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>LOGOS Wallet</title>
  <link rel="stylesheet" href="./app.css?v=20260111_110230" />
  <script>
    // fixed routes (same-origin)
    window.API_BASE="/api";            // node backend
    window.WALLET_API="/wallet-api";   // wallet proxy
  </script>
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
          <div class="muted">
            Для LGN-трансфера нужен endpoint в node-api (например /tx/send). Сейчас у тебя подтверждён только /balance.
            Как только дашь ручку отправки — подключу в эту вкладку.
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
<script src="modules/settings.js?v=20260111_172540"></script>
  <script src="modules/tx_redirect.js?v=20260112_070814"></script>
<script src="modules/send.js?v=20260112_084410"></script>
</body>
</html>
```

---

## FILE: /opt/logos/www/wallet_dev/app.js

- bytes: 30839
- sha256: `4e9f1294832d3bdd78597a4f7caef5bf65d71d7b4c3fa3aa61974284ead15b83`

```js
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
        from_token: ($("qFrom")?.value || "").trim(),
        to_token: ($("qTo")?.value || "").trim(),
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
        token: "USDT",
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
    const inputs = qa("input", panel);
    const toRid   = inputs[0] || null;
    const amount  = inputs[1] || null;
    const memo    = inputs[2] || null;
    const btnFillMe = qa("button", panel).find(b => (b.textContent||"").toLowerCase().includes("мой rid"));
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
      privKey = await importPrivKeyFromJwk(jwk);
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

---

## FILE: /opt/logos/www/wallet_dev/assets.js

- bytes: 7861
- sha256: `c7138e4217262dfa8aa59f60c6497cb7075c0158cee66b8f5ff3476c56d2cc61`

```js
(() => {
  const $ = (q, el=document) => el.querySelector(q);

  function getRID(){
    return (localStorage.getItem("logos_rid") || "").trim();
  }

  async function jget(url){
    const r = await fetch(url, { cache: "no-store" });
    const t = await r.text();
    let data = {};
    try{ data = t ? JSON.parse(t) : {}; }catch(_){ data = { raw: t }; }
    if(!r.ok) throw new Error(`${r.status} ${url}: ${t.slice(0,200)}`);
    return data;
  }

  function fmtNum(x){
    if(x === null || x === undefined) return "0";
    const s = String(x);
    return s;
  }

  async function detectNodeBase(){
    // node-api у тебя работает и так, но делаем безопасно
    const cands = ["/node-api", "/node-api/api"];
    for(const b of cands){
      try{
        await jget(`${b}/healthz`);
        return b;
      }catch(_){}
    }
    return "/node-api";
  }

  function toast(msg){
    try{
      let t = $("#_toast");
      if(!t){
        t = document.createElement("div");
        t.id = "_toast";
        t.style.cssText = "position:fixed;left:50%;bottom:110px;transform:translateX(-50%);padding:10px 14px;border-radius:12px;z-index:9999;background:rgba(20,20,30,.75);border:1px solid rgba(255,255,255,.14);color:rgba(255,255,255,.92);backdrop-filter: blur(14px);box-shadow:0 20px 60px rgba(0,0,0,.5);font: 14px system-ui;opacity:0;transition:opacity .18s ease;";
        document.body.appendChild(t);
      }
      t.textContent = msg;
      t.style.opacity = "1";
      clearTimeout(t._tm);
      t._tm = setTimeout(()=>{ t.style.opacity="0"; }, 1400);
    }catch(_){}
  }

  async function copyText(txt){
    try{
      await navigator.clipboard.writeText(txt);
      toast("Скопировано");
    }catch(_){
      // fallback
      const ta = document.createElement("textarea");
      ta.value = txt;
      ta.style.position = "fixed";
      ta.style.left = "-9999px";
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      ta.remove();
      toast("Скопировано");
    }
  }

  function findAssetsHost(){
    // пробуем самые вероятные варианты (разная разметка)
    return (
      document.querySelector('[data-page="assets"]') ||
      document.getElementById("page-assets") ||
      document.getElementById("assetsPage") ||
      document.querySelector(".page.assets") ||
      document.querySelector(".assetsPage") ||
      document.querySelector('[data-tab="assets"]') ||
      null
    );
  }

  function ensureUI(host){
    let wrap = host.querySelector("#assetsWrap");
    if(!wrap){
      wrap = document.createElement("div");
      wrap.id = "assetsWrap";
      wrap.className = "assetsWrap";
      host.prepend(wrap);
    }

    wrap.innerHTML = `
      <div class="assetsHead">
        <div>
          <div class="assetsTitle">Активы</div>
          <div class="assetsSub">Баланс + адреса для депозита (BTC / ETH / TRON / USDT)</div>
        </div>
        <button class="btn btn--soft" id="assetsRefresh" type="button">Обновить</button>
      </div>

      <div class="assetsGrid" id="assetsGrid">
        <div class="assetCard"><div class="muted">Загрузка...</div></div>
      </div>
    `;
    return wrap;
  }

  function cardHTML({sym, name, bal, addr, note}){
    const addrShort = addr ? (addr.slice(0, 8) + "…" + addr.slice(-6)) : "—";
    return `
      <div class="assetCard">
        <div class="assetTop">
          <div class="assetSym">${sym}</div>
          <div class="assetMeta">
            <div class="assetName">${name}</div>
            <div class="assetBal">${bal}</div>
          </div>
        </div>

        <div class="assetAddrRow">
          <div class="assetAddr mono" title="${addr || ""}">${addrShort}</div>
          <button class="chip chip--small" type="button" data-copy="${addr || ""}">Copy</button>
        </div>

        ${note ? `<div class="assetNote muted">${note}</div>` : ``}
      </div>
    `;
  }

  async function loadAndRender(){
    const host = findAssetsHost();
    if(!host) return; // если активы-страницы нет, не мешаем UI

    const wrap = ensureUI(host);
    const grid = wrap.querySelector("#assetsGrid");
    const rid = getRID();

    if(!rid){
      grid.innerHTML = `<div class="assetCard"><div class="muted">RID не найден. Сначала создай/восстанови кошелёк.</div></div>`;
      return;
    }

    try{
      const nodeBase = await detectNodeBase();

      // 1) LGN balance (node-api)
      const lgn = await jget(`${nodeBase}/balance/${encodeURIComponent(rid)}`);

      // 2) мульти-активы + адреса (wallet-api)
      const b = await jget(`/wallet-api/v1/balances/${encodeURIComponent(rid)}`);

      const addr = (b && b.addresses) ? b.addresses : {};
      const bal  = (b && b.balances)  ? b.balances  : {};

      const cards = [];

      cards.push(cardHTML({
        sym: "LGN",
        name: "LOGOS",
        bal: fmtNum(lgn?.balance ?? 0),
        addr: rid,
        note: "Внутрисетевой RID (LGN)"
      }));

      cards.push(cardHTML({
        sym: "BTC",
        name: "Bitcoin",
        bal: fmtNum(bal?.BTC?.total_btc ?? "0"),
        addr: addr?.BTC || "",
        note: bal?.BTC?.source ? `Источник: ${bal.BTC.source}` : ""
      }));

      cards.push(cardHTML({
        sym: "ETH",
        name: "Ethereum",
        bal: fmtNum(bal?.ETH?.eth ?? "0"),
        addr: addr?.ETH || "",
        note: bal?.ETH?.source ? `Источник: ${bal.ETH.source}` : ""
      }));

      cards.push(cardHTML({
        sym: "TRX",
        name: "TRON",
        bal: fmtNum(bal?.TRON?.trx ?? "0"),
        addr: addr?.TRON || "",
        note: bal?.TRON?.source ? `Источник: ${bal.TRON.source}` : ""
      }));

      cards.push(cardHTML({
        sym: "USDT",
        name: "Tether (ERC20)",
        bal: fmtNum(bal?.ETH?.usdt_erc20?.usdt ?? "0"),
        addr: addr?.USDT_ERC20 || addr?.ETH || "",
        note: bal?.ETH?.usdt_erc20?.contract ? `Contract: ${bal.ETH.usdt_erc20.contract}` : ""
      }));

      cards.push(cardHTML({
        sym: "USDT",
        name: "Tether (TRC20)",
        bal: fmtNum(bal?.TRON?.usdt_trc20?.usdt ?? "0"),
        addr: addr?.USDT_TRC20 || addr?.TRON || "",
        note: bal?.TRON?.usdt_trc20?.contract ? `Contract: ${bal.TRON.usdt_trc20.contract}` : ""
      }));

      grid.innerHTML = cards.join("\n");

      // copy handlers
      grid.querySelectorAll("[data-copy]").forEach(btn => {
        btn.addEventListener("click", () => {
          const v = btn.getAttribute("data-copy") || "";
          if(!v) return toast("Адрес пустой");
          copyText(v);
        });
      });

    }catch(e){
      grid.innerHTML = `<div class="assetCard"><div class="muted">Ошибка загрузки: ${String(e).slice(0,200)}</div></div>`;
    }
  }

  function hook(){
    const host = findAssetsHost();
    if(!host) return;

    // кнопка обновить
    const r = document.getElementById("assetsRefresh");
    if(r && !r._wired){
      r._wired = true;
      r.addEventListener("click", loadAndRender);
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    // первая отрисовка + подстраховка
    loadAndRender();
    setTimeout(() => { hook(); loadAndRender(); }, 350);
  });

  // если вкладки переключаются через hidden/class — при переключении подхватим
  document.addEventListener("click", (ev) => {
    const t = ev.target;
    if(!(t instanceof HTMLElement)) return;
    const nav = t.closest('[data-nav="assets"],[data-tab="assets"]');
    if(nav){
      setTimeout(loadAndRender, 120);
    }
  });
})();
```

---

## FILE: /opt/logos/www/wallet_dev/auth.css

- bytes: 880
- sha256: `5bb92959c854d22f3ee130a885db5b63cc7b8ddef762aad30a83b7d9f0ea52c7`

```css
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

---

## FILE: /opt/logos/www/wallet_dev/auth.html

- bytes: 2670
- sha256: `7ae68951c0ca2a600afab6e118aeba40b46633b9e64fdc536c3060ff47440b26`

```html
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>LOGOS Wallet — Login</title>
  <link rel="stylesheet" href="./app.css?v=1" />
  <script src="./api_base.js?v=1"></script>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <div class="topbar" style="position:static;border:0;padding:0;background:transparent">
        <div class="brand">LOGOS Wallet</div>
        <div class="pill">HTTPS only</div>
      </div>

      <div class="h1">Доступ к кошельку</div>
      <div class="muted">Ключи живут локально в браузере. Сервер получает только подписанные операции.</div>

      <div style="margin-top:14px;display:grid;gap:10px">
        <label>RID</label>
        <input id="rid" class="mono" placeholder="RID..." autocomplete="off" />

        <label>Пароль</label>
        <input id="pass" type="password" placeholder="Пароль" autocomplete="off" />

        <div class="row">
          <button id="btnLogin" class="btn primary">Войти</button>
          <button id="btnSaved" class="btn">Показать сохранённый RID</button>
        </div>

        <div id="status" class="status"></div>
      </div>
    </div>
  </div>

<script>
(function(){
  const ridEl = document.getElementById("rid");
  const passEl = document.getElementById("pass");
  const statusEl = document.getElementById("status");

  function setStatus(t){ statusEl.textContent = t || ""; }

  function loadSaved(){
    try{
      const rid = localStorage.getItem("RID") || localStorage.getItem("logos_rid") || "";
      if (rid) ridEl.value = rid;
    }catch(e){}
  }
  loadSaved();

  document.getElementById("btnSaved").addEventListener("click", () => {
    loadSaved();
    setStatus(ridEl.value ? "RID подставлен из браузера." : "Сохранённого RID нет.");
  });

  document.getElementById("btnLogin").addEventListener("click", () => {
    const rid = (ridEl.value||"").trim();
    const pass = (passEl.value||"").trim();
    if (!rid || rid.length < 20) return setStatus("ERR: введи корректный RID.");
    if (!pass) return setStatus("ERR: введи пароль.");

    try{
      localStorage.setItem("RID", rid);
      localStorage.setItem("logos_rid", rid);
      localStorage.setItem("PASS", pass);
      localStorage.setItem("logos_pass", pass);
    }catch(e){}

    setStatus("OK: сохранено локально. Переход…");
    location.href = "./app.html?v=1";
  });
})();
</script>
</body>
</html>
```

---

## FILE: /opt/logos/www/wallet_dev/auth.js

- bytes: 9193
- sha256: `c8f6b8a29a087d0f3c3c127391f3c9098d4e0bc6711e7927d37f429f94dcebcb`

```js
'use strict';

const DB_NAME = 'logos_wallet_v2';
const STORE   = 'keys';
const enc = new TextEncoder();

const ED25519_PKCS8_PREFIX = new Uint8Array([
  0x30,0x2e,0x02,0x01,0x00,
  0x30,0x05,0x06,0x03,0x2b,0x65,0x70,
  0x04,0x22,0x04,0x20
]);

const $ = (id) => document.getElementById(id);

function setStatus(t){
  const el = $('status');
  if (el) el.textContent = 'Статус: ' + t;
}

function ensureEnv(){
  if (!window.isSecureContext) throw new Error('Нужен HTTPS (secure context)');
  if (!window.crypto?.subtle) throw new Error('WebCrypto недоступен');
  if (!window.indexedDB) throw new Error('IndexedDB недоступен');
  if (!window.nacl?.sign?.keyPair?.fromSeed) throw new Error('tweetnacl не загружен (нет window.nacl)');
}

const B58_ALPH = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";
function base58encode(bytes){
  const b = (bytes instanceof Uint8Array) ? bytes : new Uint8Array(bytes||[]);
  if (b.length === 0) return "";
  let digits = [0];
  for (let i=0;i<b.length;i++){
    let carry = b[i];
    for (let j=0;j<digits.length;j++){
      const x = digits[j]*256 + carry;
      digits[j] = x % 58;
      carry = (x/58) | 0;
    }
    while (carry){
      digits.push(carry % 58);
      carry = (carry/58) | 0;
    }
  }
  let out = "";
  for (let k=0;k<b.length && b[k]===0;k++) out += "1";
  for (let q=digits.length-1;q>=0;q--) out += B58_ALPH[digits[q]];
  return out;
}

async function sha256(u8){
  const d = await crypto.subtle.digest('SHA-256', u8);
  return new Uint8Array(d);
}

function pkcs8FromSeed(seed32){
  const seed = (seed32 instanceof Uint8Array) ? seed32 : new Uint8Array(seed32||[]);
  if (seed.length !== 32) throw new Error('seed must be 32 bytes');
  const out = new Uint8Array(ED25519_PKCS8_PREFIX.length + 32);
  out.set(ED25519_PKCS8_PREFIX, 0);
  out.set(seed, ED25519_PKCS8_PREFIX.length);
  return out;
}

async function deriveKey(pass, saltU8, usage=['encrypt','decrypt']){
  const keyMat = await crypto.subtle.importKey('raw', enc.encode(pass), 'PBKDF2', false, ['deriveKey']);
  return crypto.subtle.deriveKey(
    { name:'PBKDF2', salt: saltU8, iterations:120000, hash:'SHA-256' },
    keyMat,
    { name:'AES-GCM', length:256 },
    false,
    usage
  );
}

async function aesEncrypt(aesKey, plainU8){
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const ct = await crypto.subtle.encrypt({ name:'AES-GCM', iv }, aesKey, plainU8);
  return { iv, ct: new Uint8Array(ct) };
}

async function aesDecrypt(aesKey, ivU8, ctU8){
  const plain = await crypto.subtle.decrypt({ name:'AES-GCM', iv: ivU8 }, aesKey, ctU8);
  return new Uint8Array(plain);
}

let DBP = null;
function openDb(){
  if (DBP) return DBP;
  DBP = new Promise((resolve,reject)=>{
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

async function idbGet(key){
  const db = await openDb();
  return new Promise((resolve,reject)=>{
    const tx = db.transaction(STORE,'readonly');
    const st = tx.objectStore(STORE);
    const r = st.get(key);
    r.onsuccess = ()=>resolve(r.result || null);
    r.onerror = ()=>reject(r.error);
  });
}

async function idbPut(key, val){
  const db = await openDb();
  return new Promise((resolve,reject)=>{
    const tx = db.transaction(STORE,'readwrite');
    const st = tx.objectStore(STORE);
    const r = st.put(val, key);
    r.onsuccess = ()=>resolve(true);
    r.onerror = ()=>reject(r.error);
  });
}

async function idbListRids(){
  const db = await openDb();
  return new Promise((resolve,reject)=>{
    const tx = db.transaction(STORE,'readonly');
    const st = tx.objectStore(STORE);
    const out = [];
    const req = st.openCursor();
    req.onsuccess = () => {
      const cur = req.result;
      if (!cur) return resolve(out);
      const k = String(cur.key||'');
      if (k.startsWith('acct:')) out.push(k.slice(5));
      cur.continue();
    };
    req.onerror = ()=>reject(req.error);
  });
}

function setSession(rid, pass){
  // mirror to localStorage for app.js compatibility
  try {
    localStorage.setItem("logos_rid", String(rid||""));
    localStorage.setItem("RID", String(rid||""));
    if (pass != null) localStorage.setItem("logos_pass", String(pass||""));
  } catch(e) {}

  sessionStorage.setItem('logos_rid', rid);
  sessionStorage.setItem('logos_pass', pass);
  localStorage.setItem('logos_rid', rid);
  localStorage.setItem('logos_pass', pass);
}

function validatePass(p){
  const s = String(p||'').trim();
  if (s.length < 10) throw new Error('Пароль слишком короткий (мин 10)');
  return s;
}

function normalizePhrase(ph){
  return String(ph||'').trim().replace(/\s+/g,' ').toLowerCase();
}

const WORDS = [
  "alpha","bravo","canyon","delta","eagle","frost","galaxy","harbor","ivory","jungle","karma","legend",
  "matrix","nebula","orbit","pioneer","quantum","raven","signal","temple","union","vector","wander","xenon",
  "yellow","zenith","acoustic","breeze","crystal","drift","ember","forest","glimmer","horizon","island","jewel",
  "kernel","lunar","mirror","nova","oasis","prism","quiet","river","stone","thunder","ultra","vivid","whisper","zero"
];

function genPhrase16(){
  const rnd = crypto.getRandomValues(new Uint8Array(16));
  const w = [];
  for (let i=0;i<16;i++) w.push(WORDS[rnd[i] % WORDS.length]);
  return w.join(' ');
}

async function seedFromPhrase(phrase){
  const p = normalizePhrase(phrase);
  if (!p) throw new Error('Фраза пустая');
  const h = await sha256(enc.encode(p));
  return h.slice(0,32);
}

function ridFromSeed(seed32){
  const kp = nacl.sign.keyPair.fromSeed(seed32);
  const pub = new Uint8Array(kp.publicKey);
  return base58encode(pub);
}

async function storeAccount(rid, pass, seed32){
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const aes = await deriveKey(pass, salt, ['encrypt','decrypt']);
  const pkcs8 = pkcs8FromSeed(seed32);
  const {iv, ct} = await aesEncrypt(aes, pkcs8);

  const meta = { salt: Array.from(salt), iv: Array.from(iv), priv: Array.from(ct), ts: Date.now() };
  await idbPut('acct:' + rid, meta);
}

async function loadAndVerify(rid, pass){
  const meta = await idbGet('acct:' + rid);
  if (!meta) throw new Error('RID не найден на этом устройстве (нет локальной записи)');
  const salt = new Uint8Array(meta.salt || []);
  const iv   = new Uint8Array(meta.iv || []);
  const ct   = new Uint8Array(meta.priv || []);
  const aes  = await deriveKey(pass, salt, ['decrypt']);
  const pkcs8 = await aesDecrypt(aes, iv, ct);
  const seed = pkcs8.slice(ED25519_PKCS8_PREFIX.length);
  const checkRid = ridFromSeed(seed);
  if (checkRid !== rid) throw new Error('Неверный пароль');
  return true;
}

async function doShow(){
  try{
    ensureEnv();
    const list = await idbListRids();
    const box = $('savedList');
    if (box){
      box.style.display = '';
      box.textContent = list.length ? list.map(x=>'• '+x).join('\n') : '— пусто —';
    }
    setStatus('saved RID: ' + list.length);
  }catch(e){
    setStatus('ERR: ' + (e?.message || String(e)));
  }
}

async function doLogin(){
  try{
    ensureEnv();
    const rid = String($('ridIn')?.value||'').trim();
    const pass = validatePass($('passIn')?.value||'');
    if (!rid) throw new Error('RID пустой');
    setStatus('checking…');
    await loadAndVerify(rid, pass);
    setSession(rid, pass);
    setStatus('ok → opening wallet…');
    location.href = './app.html';
  }catch(e){
    setStatus('ERR: ' + (e?.message || String(e)));
  }
}

async function doCreate(){
  try{
    ensureEnv();
    const pass = validatePass($('newPass')?.value||'');
    const phrase = genPhrase16();
    const seed = await seedFromPhrase(phrase);
    const rid = ridFromSeed(seed);
    await storeAccount(rid, pass, seed);
    const out = $('newPhraseOut');
    if (out) out.value = phrase;
    setSession(rid, pass);
    setStatus('created: ' + rid + ' → opening wallet…');
    location.href = './app.html';
  }catch(e){
    setStatus('ERR: ' + (e?.message || String(e)));
  }
}

async function doRestore(){
  try{
    ensureEnv();
    const phrase = normalizePhrase($('phraseIn')?.value||'');
    const pass = validatePass($('restorePass')?.value||'');
    if (!phrase) throw new Error('Фраза пустая');
    const seed = await seedFromPhrase(phrase);
    const rid = ridFromSeed(seed);
    await storeAccount(rid, pass, seed);
    setSession(rid, pass);
    setStatus('restored: ' + rid + ' → opening wallet…');
    location.href = './app.html';
  }catch(e){
    setStatus('ERR: ' + (e?.message || String(e)));
  }
}

window.addEventListener('DOMContentLoaded', ()=>{
  $('btnShow')?.addEventListener('click', doShow);
  $('btnLogin')?.addEventListener('click', doLogin);
  $('btnCreate')?.addEventListener('click', doCreate);
  $('btnRestore')?.addEventListener('click', doRestore);
  setStatus('ready');
});
```

---

## FILE: /opt/logos/www/wallet_dev/compat.js

- bytes: 5512
- sha256: `a178c9fb576fbacbd49c8dd57e116b4d6e0b43c73677d826dde3d2adf393bb69`

```js
"use strict";

(function () {
  // Базовый URL API
  const API = location.origin + "/node-api";

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

---

## FILE: /opt/logos/www/wallet_dev/connect.js

- bytes: 254
- sha256: `780dbed59f7f8e01732f51ff0185c31a4bd8c51359ca8eba40716e2d2aabd3cd`

```js
// LOGOS Wallet — Airdrop module REMOVED (2026-01-01)
// оставлено как безопасный stub, чтобы ничего не ломалось, если где-то осталась ссылка.
window.LOGOS_AIRDROP = { enabled: false };
```

---

## FILE: /opt/logos/www/wallet_dev/index.html

- bytes: 403
- sha256: `70da1159649c00925542db4990ad894a30ffae46167fa2de4b539f94dce1bd9a`

```html
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta http-equiv="Cache-Control" content="no-store"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <meta http-equiv="refresh" content="0; url=./auth.html?v=20260109_20"/>
  <title>LOGOS Wallet</title>
</head>
<body>
  Redirecting… <a href="./auth.html?v=20260109_20">Open LOGOS Wallet</a>
</body>
</html>
```

---

## FILE: /opt/logos/www/wallet_dev/login.html

- bytes: 318
- sha256: `409ff9c314f528c39591bcd2cb7bc400fc1eb9c9e25669f231ff1b73c1cd35d0`

```html
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

---

## FILE: /opt/logos/www/wallet_dev/modules/send.js

- bytes: 7566
- sha256: `015fbc6b85158f2da785dcf9284d0bc8f299e91c210399143a5f51b71bad9002`

```js
/* modules/send.js — REAL SEND LGN (TxIn -> /api/submit_tx) */
(() => {
  function $(sel, root=document){ return root.querySelector(sel); }

  function ridGet(){
    return localStorage.getItem("RID")
      || localStorage.getItem("logos_rid")
      || localStorage.getItem("logos_last_rid")
      || sessionStorage.getItem("RID")
      || sessionStorage.getItem("logos_rid")
      || "";
  }

  function nodeApi(){
    return (window.LOGOS_NODE_API || "/api").replace(/\/+$/,"");
  }

  function setMsg(panel, text, ok=true){
    const el = $("#sendMsg", panel) || $(".sendMsg", panel);
    if (!el) return;
    el.textContent = text || "";
    el.style.opacity = text ? "1" : "0";
    el.style.color = ok ? "" : "#ff6b6b";
  }

  function b64ToU8(b64){
    b64 = (b64||"").replace(/-/g,'+').replace(/_/g,'/');
    while (b64.length % 4) b64 += "=";
    const s = atob(b64);
    const u = new Uint8Array(s.length);
    for (let i=0;i<s.length;i++) u[i] = s.charCodeAt(i);
    return u;
  }

  function hex(u8){
    let out = "";
    for (let i=0;i<u8.length;i++) out += u8[i].toString(16).padStart(2,"0");
    return out;
  }

  // точное преобразование LGN -> micro-LGN (6 decimals)
  function lgnToMicro(s){
    s = String(s||"").trim().replace(",",".");
    if (!s) return null;
    const m = s.match(/^(\d+)(?:\.(\d{0,6})\d*)?$/);
    if (!m) return null;
    const a = m[1];
    const frac = (m[2]||"").padEnd(6,"0");
    const microStr = a + frac;
    // без BigInt не рискуем переполнением? у нас u64 — используем BigInt
    return BigInt(microStr);
  }

  async function getJSON(url){
    const r = await fetch(url, {method:"GET"});
    const t = await r.text();
    let j=null; try{ j=JSON.parse(t);}catch(_){}
    if (!r.ok){
      const msg = j?.detail || j?.error || j?.message || t;
      throw new Error("HTTP " + r.status + ": " + msg);
    }
    return j ?? t;
  }

  async function postJSON(url, body){
    const r = await fetch(url, {
      method:"POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify(body || {})
    });
    const t = await r.text();
    let j=null; try{ j=JSON.parse(t);}catch(_){}
    if (!r.ok){
      const msg = j?.detail || j?.error || j?.message || t;
      throw new Error("HTTP " + r.status + ": " + msg);
    }
    return j ?? t;
  }

  // Пытаемся найти приватный ключ в localStorage (PKCS8 base64/base64url) — без знания имени.
  async function findEd25519PrivKeyForRid(rid){
    const keys = [];
    for (let i=0;i<localStorage.length;i++){
      const k = localStorage.key(i);
      const v = localStorage.getItem(k);
      if (!v) continue;
      if (v.length < 40) continue;
      keys.push([k,v]);
    }

    for (const [k,v] of keys){
      // пропускаем явно не ключи
      if (k.toLowerCase().includes("theme")) continue;
      if (k.toLowerCase().includes("lang")) continue;

      // пробуем как pkcs8 base64/base64url
      let u8 = null;
      try { u8 = b64ToU8(v); } catch(_){}
      if (!u8 || u8.length < 40) continue;

      try{
        const priv = await crypto.subtle.importKey(
          "pkcs8",
          u8,
          { name:"Ed25519" },
          false,
          ["sign"]
        );

        // проверяем: подпись должна валидироваться на pubkey, который соответствует RID
        // (RID у тебя base58(pubkey) — но мы не будем вычислять pubkey: просто вернём ключ и надеемся что он правильный;
        // если неправильный — сервер вернёт bad_signature)
        return priv;
      }catch(_){
        // not a pkcs8 ed25519
      }
    }
    return null;
  }

  function canonBytes(tx){
    // ВАЖНО: это канонизация “по-человечески”.
    // Если на ноде другой формат — сразу увидим "bad_signature", и тогда сделаем canon-endpoint.
    const memo = tx.memo ? String(tx.memo) : "";
    const s = `${tx.from}|${tx.to}|${tx.amount}|${tx.nonce}|${memo}`;
    return new TextEncoder().encode(s);
  }

  async function signTx(privKey, tx){
    const msg = canonBytes(tx);
    const sig = await crypto.subtle.sign({name:"Ed25519"}, privKey, msg);
    return hex(new Uint8Array(sig));
  }

  function render(){
    const panel =
      document.getElementById("panel-send")
      || document.getElementById("panel-transfer")
      || document.querySelector('[data-panel="send"]')
      || document.querySelector('#panel-send');

    if (!panel) return;

    const btnSend = $("#btnSendLGN", panel) || $("#sendBtn", panel) || panel.querySelector("button");
    if (!btnSend) return;

    btnSend.addEventListener("click", async () => {
      try{
        const from = ridGet();
        const to = ($("#sendToRid", panel)?.value || "").trim();
        const amountStr = ($("#sendAmount", panel)?.value || "").trim();
        const memo = ($("#sendMemo", panel)?.value || "").trim();

        if (!from) return setMsg(panel, "RID не найден. Перезайди в кошелёк.", false);
        if (!to || to.length < 12) return setMsg(panel, "Введи правильный RID получателя.", false);

        const micro = lgnToMicro(amountStr);
        if (micro === null) return setMsg(panel, "Введи сумму (например 1 или 0.5).", false);
        if (micro <= 0n) return setMsg(panel, "Сумма должна быть больше 0.", false);

        setMsg(panel, "Получаю nonce…", true);
        const bal = await getJSON(nodeApi() + "/balance/" + encodeURIComponent(from));
        const nonceNow = (bal && (bal.nonce ?? bal.nonce_u64 ?? bal.account_nonce)) ;
        if (nonceNow === undefined || nonceNow === null) {
          return setMsg(panel, "Не смог прочитать nonce из /balance. Нужно уточнить формат ответа.", false);
        }
        const nonce = BigInt(nonceNow) + 1n;

        setMsg(panel, "Ищу ключ…", true);
        const priv = await findEd25519PrivKeyForRid(from);
        if (!priv){
          return setMsg(panel, "Нет приватного ключа в браузере. Нужен импорт/создание ключа (добавим в Настройки).", false);
        }

        const tx = {
          from,
          to,
          amount: micro.toString(),
          nonce: nonce.toString(),
          memo: memo || null
        };

        setMsg(panel, "Подписываю…", true);
        const sig_hex = await signTx(priv, tx);

        setMsg(panel, "Отправляю в сеть…", true);
        const res = await postJSON(nodeApi() + "/submit_tx", {
          from: tx.from,
          to: tx.to,
          amount: Number(tx.amount), // u64 — у тебя тут маленькие суммы; если будут огромные — переведём на строку на сервере
          nonce: Number(tx.nonce),
          memo: tx.memo,
          sig_hex
        });

        setMsg(panel, "✅ Отправлено. " + (res?.txid ? ("txid: " + res.txid) : (res?.info ? res.info : "")), true);
      }catch(e){
        setMsg(panel, "ERR: " + (e?.message || e), false);
      }
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", render);
  else render();
})();
```

---

## FILE: /opt/logos/www/wallet_dev/modules/settings.js

- bytes: 9308
- sha256: `3dd796db98ca40f0a7ed939085b39f688f8b55bae8d9381b0ec78fe8d25eac8d`

```js
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
```

---

## FILE: /opt/logos/www/wallet_dev/modules/tx_redirect.js

- bytes: 2810
- sha256: `14d7c5b092238a1d20fddb2d5c5f333337c1cc1eaba5fe76d328a75267294b0f`

```js
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

---

## FILE: /opt/logos/www/wallet_dev/tabs.js

- bytes: 1290
- sha256: `469e4796efc07d114b121e511b4a44f37fc42b85b7551868f74fa7c769f4786a`

```js
'use strict';

(function () {
  function qs(sel, root=document){ return root.querySelector(sel); }
  function qsa(sel, root=document){ return Array.from(root.querySelectorAll(sel)); }

  function activate(name){
    const tabs  = qsa('.tab[data-tab]');
    const cards = qsa('.tabCard[data-tab]');

    tabs.forEach(b => b.classList.toggle('is-active', b.getAttribute('data-tab') === name));
    cards.forEach(c => c.classList.toggle('is-active', c.getAttribute('data-tab') === name));

    // optional: hash для прямой ссылки
    try { history.replaceState(null, '', '#'+name); } catch {}
    // вверх, чтобы не казалось что "всё в одной вкладке"
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  window.LOGOS_TABS = { activate };

  window.addEventListener('DOMContentLoaded', () => {
    const tabs = qsa('.tab[data-tab]');
    if (!tabs.length) return;

    tabs.forEach(btn => {
      btn.addEventListener('click', () => activate(btn.getAttribute('data-tab')));
    });

    const fromHash = (location.hash || '').replace('#','').trim();
    const initial = fromHash && tabs.some(t => t.getAttribute('data-tab') === fromHash)
      ? fromHash
      : tabs[0].getAttribute('data-tab');

    activate(initial);
  });
})();
```

---

## FILE: /opt/logos/www/wallet_dev/ui.css

- bytes: 2211
- sha256: `50b76a402741dad8aadafaa10bbcd00463f864129907bec514db771f80abfaa8`

```css

/* assets ui */
.assetsWrap{display:block;margin-top:16px}
.assetsHead{display:flex;gap:12px;align-items:center;justify-content:space-between;margin:8px 0 14px}
.assetsTitle{font-weight:800;font-size:20px;letter-spacing:.2px}
.assetsSub{margin-top:4px;color:rgba(255,255,255,.62);font-size:12px}
.assetsGrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
@media (max-width: 900px){.assetsGrid{grid-template-columns:1fr}}
.assetCard{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:18px;padding:14px;box-shadow:0 16px 50px rgba(0,0,0,.35);backdrop-filter: blur(16px)}
.assetTop{display:flex;gap:12px;align-items:center}
.assetSym{width:48px;height:48px;border-radius:14px;display:flex;align-items:center;justify-content:center;font-weight:800;
  background:radial-gradient(120% 120% at 30% 10%, rgba(78,124,255,.35), rgba(139,92,246,.25), rgba(0,0,0,0));
  border:1px solid rgba(255,255,255,.12)
}
.assetName{font-weight:700}
.assetBal{margin-top:2px;font-size:13px;color:rgba(255,255,255,.75)}
.assetAddrRow{margin-top:12px;display:flex;gap:10px;align-items:center;justify-content:space-between}
.assetAddr{max-width:70%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:rgba(255,255,255,.85)}
.assetNote{margin-top:10px;font-size:12px}

/* ===== LOGOS PREMIUM TABS ===== */
.bottombar{
  position:fixed; left:0; right:0; bottom:0;
  display:flex; gap:10px; padding:12px 12px;
  backdrop-filter: blur(14px);
  background: rgba(10,14,26,.72);
  border-top: 1px solid rgba(255,255,255,.08);
  z-index: 9999;
}
.bottombar .tabBtn{
  flex:1;
  padding:10px 8px;
  border-radius: 14px;
  border: 1px solid rgba(255,255,255,.10);
  background: rgba(255,255,255,.04);
  color: rgba(255,255,255,.86);
  font-weight: 600;
  cursor: pointer;
}
.bottombar .tabBtn.active{
  background: rgba(120,140,255,.18);
  border-color: rgba(120,140,255,.35);
  box-shadow: 0 8px 24px rgba(0,0,0,.35);
}
body{ padding-bottom: 86px !important; }

/* чуть “премиумнее” общий вид */
.tabCard{
  border: 1px solid rgba(255,255,255,.08) !important;
  box-shadow: 0 14px 40px rgba(0,0,0,.35) !important;
  border-radius: 18px !important;
}
```

---

## FILE: /opt/logos/www/wallet_dev/ui.js

- bytes: 3447
- sha256: `e2814b431d1cf6c38a9f2efb1513d597b402d488d40e968cb87289c66f92f550`

```js
(() => {
  // Берём API из app.js, если он есть, иначе собираем по origin
  const API_BASE = (window.API ||
                    window.API_ENDPOINT ||
                    (location.origin.replace(/\/$/, '') + '/node-api'));

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

---

## FILE: /opt/logos/www/wallet_dev/wallet.css

- bytes: 5953
- sha256: `d808788cbb5a493d8185bb14b7021d8bcaeed7a56ce194e49e02c8aaf9607a9f`

```css
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

---

## FILE: /opt/logos/www/wallet_premium/app.html

- bytes: 3251
- sha256: `3c9249d3f0d3d72e5dc2fa047d5092d5ab8b478ccf880296da51c12a29fc671d`

```html
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta http-equiv="Cache-Control" content="no-store"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Wallet</title>

  <link rel="stylesheet" href="./ui.css?v=premium_v1"/>
  <script src="./i18n.js?v=premium_v1" defer></script>
  <script src="./app.js?v=premium_v1" defer></script>
  <link rel="stylesheet" href="./premium.css?v=premium_fix_01"/>
</head>
<body>
  <div class="bg">
    <div class="noise"></div>
    <div class="glow g1"></div>
    <div class="glow g2"></div>
    <div class="glow g3"></div>
  </div>

  <header class="topbar">
    <div class="wrap">
      <div class="brand">
        <div class="logo"></div>
        <div class="brandText">
          <div class="brandTitle">LOGOS Wallet</div>
          <div class="brandSub" id="brandSub">Secure account-wallet for LGN & multi-assets</div>
        </div>
      </div>

      <div class="topRight">
        <div class="pill mono" id="pillNode">NODE: …</div>
        <div class="pill mono" id="pillWallet">WALLET: …</div>

        <button class="pill btn" id="btnLang">RU</button>
        <button class="pill btn" id="btnTheme">Theme</button>
      </div>
    </div>
  </header>

  <main class="main">
    <div class="wrap">
      <section class="heroCard">
        <div class="heroHead">
          <div>
            <div class="h1" id="pageTitle">—</div>
            <div class="sub" id="pageSub">—</div>
          </div>

          <div class="ridBox">
            <div class="ridLabel" id="ridLabel">RID</div>
            <div class="ridValue mono" id="ridValue">—</div>
            <div class="ridActions">
              <button class="btnSmall" id="btnCopyRid">Copy</button>
              <button class="btnSmall ghost" id="btnManageRid">Create / Restore</button>
            </div>
          </div>
        </div>
      </section>

      <section class="content" id="content"></section>
    </div>
  </main>

  <nav class="tabs" id="tabs">
    <button class="tab active" data-tab="home">
      <div class="ico">⌂</div>
      <div class="t" data-i18n="tab_home">Home</div>
    </button>

    <button class="tab" data-tab="assets">
      <div class="ico">◈</div>
      <div class="t" data-i18n="tab_assets">Assets</div>
    </button>

    <button class="tab" data-tab="staking">
      <div class="ico">◎</div>
      <div class="t" data-i18n="tab_staking">Staking</div>
    </button>

    <button class="tab" data-tab="card">
      <div class="ico">▢</div>
      <div class="t" data-i18n="tab_card">Card</div>
    </button>

    <button class="tab" data-tab="settings">
      <div class="ico">⚙</div>
      <div class="t" data-i18n="tab_settings">Settings</div>
    </button>
  </nav>

  <div class="toast" id="toast"></div>

  <div class="modal" id="modal" aria-hidden="true">
    <div class="modalBack" id="modalBack"></div>
    <div class="modalCard">
      <div class="modalTop">
        <div class="modalTitle" id="modalTitle">—</div>
        <button class="modalClose" id="modalClose">×</button>
      </div>
      <div class="modalBody" id="modalBody"></div>
      <div class="modalFoot" id="modalFoot"></div>
    </div>
  </div>
</body>
</html>
```

---

## FILE: /opt/logos/www/wallet_premium/app.js

- bytes: 21078
- sha256: `804f11ccc85419fa37427d9576aa6de2791f080111c03c2a5417d46d58f761ae`

```js
"use strict";

(() => {
  const $ = (q, el=document) => el.querySelector(q);
  const $$ = (q, el=document) => Array.from(el.querySelectorAll(q));

  function normalize(u){ return (u||"").toString().trim().replace(/\/+$/,""); }

  // ===== THEME / LANG =====
  function applyTheme(){
    const t = localStorage.getItem("logos_theme") || "dark";
    document.documentElement.dataset.theme = (t === "light") ? "light" : "dark";
  }
  function toggleTheme(){
    const cur = document.documentElement.dataset.theme || "dark";
    const next = (cur === "dark") ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    localStorage.setItem("logos_theme", next);
    toast("Theme: " + next);
  }

  function applyLang(){
    const lang = I18N.getLang();
    $("#btnLang").textContent = lang.toUpperCase();
    $("#brandSub").textContent = I18N.t("brand_sub");

    $$("[data-i18n]").forEach(el=>{
      const k = el.getAttribute("data-i18n");
      el.textContent = I18N.t(k);
    });

    // current page titles will be re-rendered by setTab()
  }
  function toggleLang(){
    const cur = I18N.getLang();
    const next = (cur === "ru") ? "en" : "ru";
    I18N.setLang(next);
    applyLang();
    render();
  }

  // ===== RID STORAGE (compat with your old keys) =====
  function getRid(){
    try{
      const a = JSON.parse(localStorage.getItem("logos_onb_v1") || "{}");
      if (a && a.rid) return String(a.rid);
    }catch(_){}
    const rid = localStorage.getItem("logos_rid") || localStorage.getItem("RID") || "";
    return String(rid || "");
  }

  function setRid(rid){
    const r = String(rid||"").trim();
    if (!r) return;
    localStorage.setItem("logos_rid", r);
    localStorage.setItem("RID", r);
  }

  async function copyText(text){
    try{
      await navigator.clipboard.writeText(String(text||""));
      toast(I18N.t("ok_copied"));
      return true;
    }catch(_){
      toast(I18N.t("err_copy"));
      return false;
    }
  }

  // ===== API BASE =====
  function apiBase(){
    // IMPORTANT: we keep same paths you already have on domain
    const origin = normalize(window.location.origin);
    return {
      node: origin + "/node-api",
      wallet: origin + "/wallet-api"
    };
  }

  async function fetchJson(url, opts={}, timeoutMs=6000){
    const ctrl = new AbortController();
    const t = setTimeout(()=>ctrl.abort(), timeoutMs);
    try{
      const res = await fetch(url, { ...opts, signal: ctrl.signal, cache: "no-store" });
      const ct = res.headers.get("content-type") || "";
      const txt = await res.text();
      if (!res.ok) throw new Error("HTTP " + res.status + " " + txt.slice(0,140));
      if (ct.includes("application/json")) return JSON.parse(txt);
      // allow plain text
      return { ok:true, text: txt };
    } finally {
      clearTimeout(t);
    }
  }

  // ===== UI helpers =====
  let toastTimer = null;
  function toast(msg){
    const el = $("#toast");
    el.textContent = msg;
    el.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(()=>el.classList.remove("show"), 1800);
  }

  function modalOpen(title, bodyHtml, footHtml=""){
    $("#modalTitle").textContent = title;
    $("#modalBody").innerHTML = bodyHtml;
    $("#modalFoot").innerHTML = footHtml;
    $("#modal").setAttribute("aria-hidden","false");
  }
  function modalClose(){
    $("#modal").setAttribute("aria-hidden","true");
  }

  // ===== STATUS pills =====
  async function updateStatus(){
    const base = apiBase();
    const rid = getRid();

    // NODE
    try{
      const j = await fetchJson(base.node + "/healthz");
      $("#pillNode").textContent = (j && j.status === "ok") ? "NODE: ON" : "NODE: ?";
      $("#pillNode").style.borderColor = (j && j.status === "ok") ? "rgba(34,197,94,.55)" : "";
    }catch(_){
      $("#pillNode").textContent = "NODE: OFF";
      $("#pillNode").style.borderColor = "rgba(248,113,113,.55)";
    }

    // WALLET
    if (!rid){
      $("#pillWallet").textContent = "WALLET: —";
      $("#pillWallet").style.borderColor = "";
      return;
    }
    try{
      // health endpoint may not exist; we still show OK if RID exists
      await fetchJson(base.wallet + "/healthz").catch(()=>null);
      $("#pillWallet").textContent = "WALLET: OK";
      $("#pillWallet").style.borderColor = "rgba(79,124,255,.55)";
    }catch(_){
      $("#pillWallet").textContent = "WALLET: OK";
      $("#pillWallet").style.borderColor = "rgba(79,124,255,.55)";
    }
  }

  // ===== RENDER =====
  const state = { tab: "home" };

  function setTab(tab){
    state.tab = tab;
    $$(".tab").forEach(b => b.classList.toggle("active", b.dataset.tab === tab));
    render();
  }

  function renderHeader(){
    const rid = getRid();
    $("#ridLabel").textContent = I18N.t("rid_label");
    $("#ridValue").textContent = rid ? rid : I18N.t("rid_missing");
    $("#btnCopyRid").textContent = I18N.t("btn_copy");
    $("#btnManageRid").textContent = I18N.t("btn_manage");
  }

  function viewHome(){
    $("#pageTitle").textContent = I18N.t("home_title");
    $("#pageSub").textContent = I18N.t("home_sub");

    const rid = getRid();

    const actions = `
      <div class="actions">
        <button class="btn primary" id="actReceive">${I18N.t("act_receive")}</button>
        <button class="btn" id="actSend">${I18N.t("act_send")}</button>
        <button class="btn" id="actSwap">${I18N.t("act_swap")}</button>
        <button class="btn" id="actFiat">${I18N.t("act_fiat")}</button>
        <button class="btn success" id="actStake">${I18N.t("act_stake")}</button>
      </div>
    `;

    const content = `
      <div class="grid two">
        <div class="card">
          <div class="cardIn">
            <div class="row">
              <div>
                <div class="cardTitle">${I18N.t("total_balance")}</div>
                <div class="cardSub">${I18N.t("lgn_first")}</div>
              </div>
              <div class="badge mono" id="currencyBadge">LGN</div>
            </div>

            <div class="row" style="align-items:flex-end">
              <div class="bigAmount" id="totalAmount">—</div>
              <div class="actions" style="margin:0">
                <button class="btn ghost" id="viewUSD">${I18N.t("view_usd")}</button>
                <button class="btn ghost" id="viewEUR">${I18N.t("view_eur")}</button>
              </div>
            </div>

            ${rid ? "" : `<div class="empty">${I18N.t("empty_need_rid")}</div>`}
            ${actions}
          </div>
        </div>

        <div class="card">
          <div class="cardIn">
            <div class="cardTitle">Activity</div>
            <div class="cardSub">History & notifications (next step)</div>
            <div class="empty">${I18N.t("empty_api")}</div>
          </div>
        </div>
      </div>
    `;

    $("#content").innerHTML = content;

    // set mock total
    $("#totalAmount").textContent = rid ? "0.00" : "—";

    $("#actReceive").onclick = () => openReceive();
    $("#actSend").onclick = () => openSend();
    $("#actSwap").onclick = () => openSwap();
    $("#actFiat").onclick = () => openFiat();
    $("#actStake").onclick = () => setTab("staking");

    $("#viewUSD").onclick = () => {
      $("#currencyBadge").textContent = "USD";
      $("#totalAmount").textContent = rid ? "0.00" : "—";
    };
    $("#viewEUR").onclick = () => {
      $("#currencyBadge").textContent = "EUR";
      $("#totalAmount").textContent = rid ? "0.00" : "—";
    };
  }

  function viewAssets(){
    $("#pageTitle").textContent = I18N.t("assets_title");
    $("#pageSub").textContent = I18N.t("assets_sub");

    const rid = getRid();
    const list = `
      <div class="list">
        <div class="item">
          <div class="itL">
            <div class="coin"></div>
            <div>
              <div class="sym">LGN</div>
              <div class="name">LOGOS Network</div>
            </div>
          </div>
          <div class="itR">
            <div class="val">0.00</div>
            <div class="small">≈ 0.00 USD</div>
          </div>
        </div>

        <div class="item">
          <div class="itL">
            <div class="coin" style="background: radial-gradient(10px 10px at 30% 30%, rgba(255,255,255,.55), transparent 65%), linear-gradient(135deg, rgba(34,197,94,.35), rgba(79,124,255,.25));"></div>
            <div>
              <div class="sym">USDT</div>
              <div class="name">Tether (bridge)</div>
            </div>
          </div>
          <div class="itR">
            <div class="val">0.00</div>
            <div class="small">≈ 0.00 USD</div>
          </div>
        </div>

        <div class="item">
          <div class="itL">
            <div class="coin" style="background: radial-gradient(10px 10px at 30% 30%, rgba(255,255,255,.55), transparent 65%), linear-gradient(135deg, rgba(251,191,36,.35), rgba(147,51,234,.25));"></div>
            <div>
              <div class="sym">BTC</div>
              <div class="name">Bitcoin (bridge)</div>
            </div>
          </div>
          <div class="itR">
            <div class="val">0.00</div>
            <div class="small">≈ 0.00 USD</div>
          </div>
        </div>
      </div>
    `;

    $("#content").innerHTML = `
      <div class="card">
        <div class="cardIn">
          <div class="row" style="margin-top:0">
            <div>
              <div class="cardTitle">Portfolio</div>
              <div class="cardSub">LGN first • multi-assets next</div>
            </div>
            <div class="actions" style="margin:0">
              <button class="btn primary" id="btnReceive">${I18N.t("act_receive")}</button>
              <button class="btn" id="btnSend">${I18N.t("act_send")}</button>
            </div>
          </div>

          ${rid ? "" : `<div class="empty">${I18N.t("empty_need_rid")}</div>`}
          ${list}
          <div class="empty">${I18N.t("empty_api")}</div>
        </div>
      </div>
    `;

    $("#btnReceive").onclick = () => openReceive();
    $("#btnSend").onclick = () => openSend();
  }

  function viewStaking(){
    $("#pageTitle").textContent = I18N.t("staking_title");
    $("#pageSub").textContent = I18N.t("staking_sub");

    const rid = getRid();
    $("#content").innerHTML = `
      <div class="grid two">
        <div class="card">
          <div class="cardIn">
            <div class="cardTitle">LGN Staking</div>
            <div class="cardSub">Stake • Unstake • Claim • Auto-compound (next)</div>

            ${rid ? "" : `<div class="empty">${I18N.t("empty_need_rid")}</div>`}

            <div class="row">
              <div>
                <div class="small">Staked</div>
                <div class="val" style="font-size:22px">0.00 LGN</div>
              </div>
              <div>
                <div class="small">Rewards</div>
                <div class="val" style="font-size:22px">0.00 LGN</div>
              </div>
            </div>

            <div class="row">
              <div class="badge">APR: —</div>
              <div class="badge">Unbonding: —</div>
            </div>

            <div class="actions">
              <button class="btn success" id="btnStake">Stake</button>
              <button class="btn" id="btnUnstake">Unstake</button>
              <button class="btn primary" id="btnClaim">Claim</button>
            </div>

            <div class="empty">${I18N.t("empty_api")}</div>
          </div>
        </div>

        <div class="card">
          <div class="cardIn">
            <div class="cardTitle">Validators</div>
            <div class="cardSub">Choose validator • delegation stats (next)</div>
            <div class="empty">${I18N.t("empty_api")}</div>
          </div>
        </div>
      </div>
    `;

    $("#btnStake").onclick = () => openStake();
    $("#btnUnstake").onclick = () => openStake("unstake");
    $("#btnClaim").onclick = () => openStake("claim");
  }

  function viewCard(){
    $("#pageTitle").textContent = I18N.t("card_title");
    $("#pageSub").textContent = I18N.t("card_sub");

    $("#content").innerHTML = `
      <div class="grid two">
        <div class="card">
          <div class="cardIn">
            <div class="cardTitle">LOGOS Card</div>
            <div class="cardSub">Premium spending layer (fiat integration later)</div>

            <div class="row">
              <div>
                <div class="small">Spending pocket</div>
                <div class="val" style="font-size:26px">0.00</div>
              </div>
              <div class="badge">KYC: —</div>
            </div>

            <div class="actions">
              <button class="btn primary" id="btnTopupPocket">Top up</button>
              <button class="btn" id="btnLimits">Limits</button>
              <button class="btn ghost" id="btnHistory">History</button>
            </div>

            <div class="empty">${I18N.t("empty_api")}</div>
          </div>
        </div>

        <div class="card">
          <div class="cardIn">
            <div class="cardTitle">Security</div>
            <div class="cardSub">Anti-fraud • time-lock • address whitelist (next)</div>
            <div class="empty">${I18N.t("empty_api")}</div>
          </div>
        </div>
      </div>
    `;

    $("#btnTopupPocket").onclick = () => openFiat();
    $("#btnLimits").onclick = () => openFiat();
    $("#btnHistory").onclick = () => openFiat();
  }

  function viewSettings(){
    $("#pageTitle").textContent = I18N.t("settings_title");
    $("#pageSub").textContent = I18N.t("settings_sub");

    $("#content").innerHTML = `
      <div class="grid two">
        <div class="card">
          <div class="cardIn">
            <div class="cardTitle">Security</div>
            <div class="cardSub">Seed control • passphrase • passkey (next)</div>

            <div class="actions">
              <button class="btn" id="btnSeed">Seed check</button>
              <button class="btn" id="btnPasskey">Passkey</button>
              <button class="btn" id="btnLimits2">Limits</button>
            </div>
            <div class="empty">${I18N.t("empty_api")}</div>
          </div>
        </div>

        <div class="card">
          <div class="cardIn">
            <div class="cardTitle">About</div>
            <div class="cardSub">Version • endpoints • diagnostics</div>

            <div class="list">
              <div class="item">
                <div class="itL"><div class="sym">Node API</div></div>
                <div class="itR"><div class="small mono" id="aboutNode">—</div></div>
              </div>
              <div class="item">
                <div class="itL"><div class="sym">Wallet API</div></div>
                <div class="itR"><div class="small mono" id="aboutWallet">—</div></div>
              </div>
            </div>

            <div class="actions">
              <button class="btn primary" id="btnDiag">Diagnostics</button>
            </div>
          </div>
        </div>
      </div>
    `;

    const base = apiBase();
    $("#aboutNode").textContent = base.node;
    $("#aboutWallet").textContent = base.wallet;

    $("#btnDiag").onclick = () => openDiag();
    $("#btnSeed").onclick = () => openOnboarding();
    $("#btnPasskey").onclick = () => openDiag();
    $("#btnLimits2").onclick = () => openDiag();
  }

  function render(){
    renderHeader();
    const tab = state.tab;
    if (tab === "home") return viewHome();
    if (tab === "assets") return viewAssets();
    if (tab === "staking") return viewStaking();
    if (tab === "card") return viewCard();
    if (tab === "settings") return viewSettings();
    viewHome();
  }

  // ===== Modals =====
  function openReceive(){
    const rid = getRid();
    if (!rid) return openOnboarding();
    modalOpen(I18N.t("m_receive_title"),
      `
      <div class="label">Asset</div>
      <select class="input" id="mAsset">
        <option>LGN</option>
        <option>USDT</option>
        <option>BTC</option>
      </select>
      <div class="label">Address / RID</div>
      <input class="input mono" value="${rid}" readonly/>
      <div class="hr"></div>
      <div class="empty">${I18N.t("empty_api")}</div>
      `,
      `<button class="btn primary" id="mCopy">Copy</button><button class="btn ghost" id="mClose">Close</button>`
    );
    $("#mCopy").onclick = () => copyText(rid);
    $("#mClose").onclick = () => modalClose();
  }

  function openSend(){
    const rid = getRid();
    if (!rid) return openOnboarding();
    modalOpen(I18N.t("m_send_title"),
      `
      <div class="label">To (RID / address)</div>
      <input class="input mono" id="toRid" placeholder="RID..."/>
      <div class="label">Amount (LGN)</div>
      <input class="input" id="amt" placeholder="0.00"/>
      <div class="hr"></div>
      <div class="empty">${I18N.t("empty_api")}</div>
      `,
      `<button class="btn primary" id="mSubmit">Sign & send</button><button class="btn ghost" id="mClose">Close</button>`
    );
    $("#mSubmit").onclick = () => toast("Next step: connect /withdraw + intent-sign");
    $("#mClose").onclick = () => modalClose();
  }

  function openSwap(){
    const rid = getRid();
    if (!rid) return openOnboarding();
    modalOpen(I18N.t("m_swap_title"),
      `
      <div class="label">From</div>
      <select class="input"><option>LGN</option><option>USDT</option></select>
      <div class="label">To</div>
      <select class="input"><option>USDT</option><option>LGN</option></select>
      <div class="label">Amount</div>
      <input class="input" placeholder="0.00"/>
      <div class="hr"></div>
      <div class="empty">${I18N.t("empty_api")}</div>
      `,
      `<button class="btn primary" id="mSwap">Continue</button><button class="btn ghost" id="mClose">Close</button>`
    );
    $("#mSwap").onclick = () => toast("Next step: bridge/swap endpoints");
    $("#mClose").onclick = () => modalClose();
  }

  function openFiat(){
    modalOpen(I18N.t("m_fiat_title"),
      `
      <div class="cardSub">SEPA / cards / KYC — after integration</div>
      <div class="empty">${I18N.t("empty_api")}</div>
      `,
      `<button class="btn ghost" id="mClose">Close</button>`
    );
    $("#mClose").onclick = () => modalClose();
  }

  function openStake(mode="stake"){
    const rid = getRid();
    if (!rid) return openOnboarding();
    const title = (mode==="claim") ? "Claim" : (mode==="unstake" ? "Unstake" : I18N.t("m_stake_title"));
    modalOpen(title,
      `
      <div class="label">Amount (LGN)</div>
      <input class="input" placeholder="0.00"/>
      <div class="label">Validator</div>
      <input class="input mono" placeholder="validator RID / key"/>
      <div class="hr"></div>
      <div class="empty">${I18N.t("empty_api")}</div>
      `,
      `<button class="btn primary" id="mDo">Continue</button><button class="btn ghost" id="mClose">Close</button>`
    );
    $("#mDo").onclick = () => toast("Next step: staking endpoints (delegate/undelegate/claim)");
    $("#mClose").onclick = () => modalClose();
  }

  function openDiag(){
    const base = apiBase();
    modalOpen("Diagnostics",
      `
      <div class="label">Node API</div>
      <input class="input mono" value="${base.node}" readonly/>
      <div class="label">Wallet API</div>
      <input class="input mono" value="${base.wallet}" readonly/>
      <div class="hr"></div>
      <div class="empty">UI is premium-ready. Next step: connect balance/history/topup/withdraw/staking.</div>
      `,
      `<button class="btn primary" id="mPing">Ping node</button><button class="btn ghost" id="mClose">Close</button>`
    );
    $("#mPing").onclick = async () => {
      try{
        const j = await fetchJson(base.node + "/healthz");
        toast("node: " + (j.status || "ok"));
      }catch(e){
        toast("node: OFF");
      }
    };
    $("#mClose").onclick = () => modalClose();
  }

  function openOnboarding(){
    toast(I18N.t("open_onboarding"));
    // Пока просто перекидываем на твой онбординг путь (можно заменить на SPA-экран)
    // Если у тебя другой путь — поменяем тут одной строкой.
    window.location.href = "/wallet_dev/welcome.html";
  }

  // ===== INIT =====
  function bind(){
    $("#btnTheme").onclick = toggleTheme;
    $("#btnLang").onclick = toggleLang;

    $("#btnCopyRid").onclick = () => {
      const rid = getRid();
      if (!rid) return toast(I18N.t("empty_need_rid"));
      copyText(rid);
    };
    $("#btnManageRid").onclick = openOnboarding;

    $$(".tab").forEach(b => b.onclick = () => setTab(b.dataset.tab));

    $("#modalBack").onclick = modalClose;
    $("#modalClose").onclick = modalClose;

    // default tab
    const hash = (location.hash || "").replace("#","");
    if (hash) state.tab = hash;
  }

  function boot(){
    applyTheme();
    applyLang();
    bind();
    render();
    updateStatus();
    setInterval(updateStatus, 7000);
  }

  document.addEventListener("DOMContentLoaded", boot);
})();
```

---

## FILE: /opt/logos/www/wallet_premium/i18n.js

- bytes: 3957
- sha256: `ec08ffaec38a151faee130b5f3d019db5bbe4db94b9c8be007e1fd555e95c25d`

```js
(() => {
  const dict = {
    ru: {
      brand_sub: "Безопасный аккаунт-кошелёк для LGN и мультикрипты",
      tab_home: "Главная",
      tab_assets: "Активы",
      tab_staking: "Стейкинг",
      tab_card: "Карта",
      tab_settings: "Настройки",

      home_title: "Главная",
      home_sub: "Баланс, быстрые действия и операции",
      assets_title: "Активы",
      assets_sub: "Портфель, получение/отправка и история",
      staking_title: "Стейкинг",
      staking_sub: "LGN: stake / unstake / claim",
      card_title: "Карта",
      card_sub: "Spending pocket, лимиты и статусы",
      settings_title: "Настройки",
      settings_sub: "Безопасность, язык/тема, интеграции",

      rid_label: "RID",
      rid_missing: "RID не создан — нажми Create / Restore",
      btn_copy: "Копировать",
      btn_manage: "Создать / Восстановить",

      act_receive: "Получить",
      act_send: "Отправить",
      act_swap: "Обмен",
      act_fiat: "Фиат",
      act_stake: "Стейкинг",

      total_balance: "Общий баланс",
      view_usd: "В USD",
      view_eur: "В EUR",
      lgn_first: "LGN — основной актив",

      empty_need_rid: "Сначала создай/восстанови кошелёк (RID).",
      empty_api: "API пока не подключён. UI готов — подключим ручки следующим шагом.",

      m_receive_title: "Получить",
      m_send_title: "Отправить",
      m_swap_title: "Обмен",
      m_fiat_title: "Фиат",
      m_stake_title: "Стейкинг",

      ok_copied: "Скопировано",
      err_copy: "Не удалось скопировать",
      open_onboarding: "Открываю онбординг…"
    },
    en: {
      brand_sub: "Secure account-wallet for LGN & multi-assets",
      tab_home: "Home",
      tab_assets: "Assets",
      tab_staking: "Staking",
      tab_card: "Card",
      tab_settings: "Settings",

      home_title: "Home",
      home_sub: "Balance, quick actions and operations",
      assets_title: "Assets",
      assets_sub: "Portfolio, receive/send and history",
      staking_title: "Staking",
      staking_sub: "LGN: stake / unstake / claim",
      card_title: "Card",
      card_sub: "Spending pocket, limits and statuses",
      settings_title: "Settings",
      settings_sub: "Security, language/theme, integrations",

      rid_label: "RID",
      rid_missing: "RID not set — press Create / Restore",
      btn_copy: "Copy",
      btn_manage: "Create / Restore",

      act_receive: "Receive",
      act_send: "Send",
      act_swap: "Swap",
      act_fiat: "Fiat",
      act_stake: "Stake",

      total_balance: "Total balance",
      view_usd: "In USD",
      view_eur: "In EUR",
      lgn_first: "LGN is the primary asset",

      empty_need_rid: "Create/restore wallet first (RID).",
      empty_api: "API not connected yet. UI is ready — we'll plug endpoints next.",

      m_receive_title: "Receive",
      m_send_title: "Send",
      m_swap_title: "Swap",
      m_fiat_title: "Fiat",
      m_stake_title: "Staking",

      ok_copied: "Copied",
      err_copy: "Copy failed",
      open_onboarding: "Opening onboarding…"
    }
  };

  function getLang(){
    const v = (localStorage.getItem("logos_lang") || "ru").toLowerCase();
    return (v === "en") ? "en" : "ru";
  }

  window.I18N = {
    getLang,
    t(key){
      const lang = getLang();
      return (dict[lang] && dict[lang][key]) || (dict.ru[key] || key);
    },
    setLang(lang){
      const v = (String(lang||"").toLowerCase() === "en") ? "en" : "ru";
      localStorage.setItem("logos_lang", v);
    }
  };
})();
```

---

## FILE: /opt/logos/www/wallet_premium/premium.css

- bytes: 3549
- sha256: `2e4a150995ffe4564658abc377e6f21f236e2c7319448d78fc7bf2dcd655facb`

```css
/* LOGOS Wallet Premium Override */
:root{
  --bg0:#050812;
  --bg1:#070B18;
  --glass: rgba(255,255,255,.06);
  --glass2: rgba(255,255,255,.04);
  --stroke: rgba(255,255,255,.10);
  --stroke2: rgba(255,255,255,.07);
  --txt: rgba(255,255,255,.92);
  --muted: rgba(255,255,255,.62);
  --shadow: 0 20px 60px rgba(0,0,0,.55);
  --r16: 16px;
  --r20: 20px;
  --r24: 24px;
  --pad: clamp(14px, 2.2vw, 22px);
  --w: 1120px;
}

/* фон “премиум” */
html,body{ height:100%; }
body{
  color: var(--txt);
  background:
    radial-gradient(900px 520px at 20% 8%, rgba(70,120,255,.18), transparent 60%),
    radial-gradient(820px 520px at 78% 16%, rgba(0,255,180,.14), transparent 60%),
    radial-gradient(720px 520px at 55% 92%, rgba(160,90,255,.12), transparent 65%),
    linear-gradient(180deg, var(--bg0), var(--bg1));
}

/* контейнер */
.container{
  max-width: var(--w) !important;
  padding-left: var(--pad) !important;
  padding-right: var(--pad) !important;
}

/* верхняя панель — плотнее и “дороже” */
.topbar{
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border-bottom: 1px solid var(--stroke2);
}
.brand__t{ font-size: 16px; letter-spacing: .2px; }
.brand__s{ color: var(--muted); }

/* карточки */
.card, .panel, .box, .section{
  background: linear-gradient(180deg, var(--glass), var(--glass2));
  border: 1px solid var(--stroke2);
  border-radius: var(--r24);
  box-shadow: var(--shadow);
}
.card{ padding: clamp(16px, 2.1vw, 22px); }
.card h1, .h1{ font-size: clamp(26px, 3.2vw, 34px); letter-spacing: .2px; }
.card h2, .h2{ font-size: clamp(18px, 2.4vw, 22px); color: var(--txt); }
.muted, .sub, .hint{ color: var(--muted) !important; }

/* кнопки — единая система */
button, .btn{
  border-radius: 14px !important;
  border: 1px solid var(--stroke2) !important;
  background: rgba(255,255,255,.06) !important;
  color: var(--txt) !important;
  transition: transform .12s ease, filter .12s ease, background .12s ease;
}
button:hover, .btn:hover{ filter: brightness(1.08); }
button:active, .btn:active{ transform: translateY(1px); }

.btnPrimary, .primary, .btn.primary{
  background: linear-gradient(135deg, rgba(80,120,255,.92), rgba(120,80,255,.75)) !important;
  border-color: rgba(170,190,255,.25) !important;
}
.btnSuccess, .success{
  background: linear-gradient(135deg, rgba(0,220,160,.92), rgba(0,170,120,.72)) !important;
  border-color: rgba(120,255,210,.22) !important;
}

/* поля ввода */
input, textarea, select{
  border-radius: 14px !important;
  background: rgba(0,0,0,.22) !important;
  border: 1px solid var(--stroke2) !important;
  color: var(--txt) !important;
}
input::placeholder, textarea::placeholder{ color: rgba(255,255,255,.35); }

/* нижняя навигация — “как приложение” */
.tabs{
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  background: rgba(10,14,25,.55) !important;
  border-top: 1px solid var(--stroke2);
}
.tab{
  border-radius: 16px !important;
}
.tab.active{
  background: rgba(255,255,255,.08) !important;
  border: 1px solid rgba(255,255,255,.12) !important;
}

/* чтобы не было ощущения “пустоты”: контентный блок ниже */
.content, #content{
  min-height: calc(100vh - 180px);
}

/* мобила */
@media (max-width: 520px){
  .brand__s{ display:none; }
  .card{ border-radius: 18px; }
  button, .btn{ width: 100%; }
  .tabs{ padding-bottom: env(safe-area-inset-bottom); }
}
```

---

## FILE: /opt/logos/www/wallet_premium/ui.css

- bytes: 15523
- sha256: `7b26184ecec58929a6e5890efa89e724c3f476cabdec8bf0ed482ff66824486a`

```css
:root{
  --bg0:#070A12;
  --bg1:#0B1020;
  --txt:#EAF0FF;
  --mut:#98A3C7;

  --card: rgba(255,255,255,.06);
  --card2: rgba(255,255,255,.04);
  --stroke: rgba(255,255,255,.10);
  --stroke2: rgba(255,255,255,.14);

  --shadow: 0 18px 80px rgba(0,0,0,.55);
  --blur: blur(18px);

  --r16: 16px;
  --r20: 20px;
  --r24: 24px;

  --s8:8px; --s10:10px; --s12:12px; --s14:14px;
  --s16:16px; --s18:18px; --s20:20px; --s24:24px; --s28:28px;

  --accent: #4F7CFF;
  --accent2:#22C55E;
  --warn:#FBBF24;
  --bad:#F87171;

  --tabH: 74px;
  --maxW: 1120px;

  --font: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial;
  --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
}

:root[data-theme="light"]{
  --bg0:#F6F8FF;
  --bg1:#EEF2FF;
  --txt:#0C1222;
  --mut:#4B5563;
  --card: rgba(10,20,40,.06);
  --card2: rgba(10,20,40,.04);
  --stroke: rgba(10,20,40,.10);
  --stroke2: rgba(10,20,40,.14);
  --shadow: 0 20px 90px rgba(10,20,40,.14);
}

*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0;
  font-family: var(--font);
  color: var(--txt);
  background: radial-gradient(1200px 700px at 20% 10%, rgba(79,124,255,.18), transparent 60%),
              radial-gradient(900px 600px at 80% 20%, rgba(34,197,94,.12), transparent 55%),
              linear-gradient(180deg, var(--bg0), var(--bg1));
  overflow-x:hidden;
}

/* Background */
.bg{position:fixed; inset:0; pointer-events:none; z-index:-1;}
.noise{
  position:absolute; inset:-40px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='220' height='220' filter='url(%23n)' opacity='.22'/%3E%3C/svg%3E");
  opacity:.18;
  mix-blend-mode: overlay;
}
.glow{position:absolute; width:520px; height:520px; border-radius:999px; filter: blur(70px); opacity:.20;}
.g1{left:-120px; top:-120px; background: rgba(79,124,255,.85);}
.g2{right:-160px; top:60px; background: rgba(34,197,94,.75);}
.g3{left:35%; bottom:-220px; background: rgba(147,51,234,.60);}

/* Layout */
.wrap{max-width: var(--maxW); margin:0 auto; padding: 0 var(--s20);}
.topbar{
  position:sticky; top:0; z-index:20;
  backdrop-filter: var(--blur);
  background: linear-gradient(180deg, rgba(0,0,0,.35), rgba(0,0,0,0));
  border-bottom: 1px solid rgba(255,255,255,.06);
}
:root[data-theme="light"] .topbar{
  background: linear-gradient(180deg, rgba(255,255,255,.75), rgba(255,255,255,0));
  border-bottom: 1px solid rgba(10,20,40,.08);
}
.topbar .wrap{
  display:flex; align-items:center; justify-content:space-between;
  padding: 14px var(--s20);
}

.brand{display:flex; align-items:center; gap:12px;}
.logo{
  width:38px; height:38px; border-radius: 14px;
  background:
    radial-gradient(12px 12px at 30% 30%, rgba(255,255,255,.65), transparent 60%),
    radial-gradient(18px 18px at 70% 60%, rgba(79,124,255,.95), transparent 60%),
    linear-gradient(135deg, rgba(34,197,94,.35), rgba(147,51,234,.35));
  box-shadow: 0 10px 30px rgba(79,124,255,.18);
  border: 1px solid rgba(255,255,255,.12);
}
.brandTitle{font-weight: 800; letter-spacing:.2px;}
.brandSub{font-size: 12px; color: var(--mut); margin-top:2px;}

.topRight{display:flex; align-items:center; gap:10px; flex-wrap:wrap; justify-content:flex-end;}
.pill{
  border:1px solid rgba(255,255,255,.12);
  background: rgba(255,255,255,.06);
  color: var(--txt);
  padding: 8px 12px;
  border-radius: 999px;
  font-size: 12px;
  line-height: 1;
  box-shadow: 0 10px 40px rgba(0,0,0,.12);
}
:root[data-theme="light"] .pill{
  background: rgba(10,20,40,.06);
  border:1px solid rgba(10,20,40,.10);
  box-shadow: 0 10px 40px rgba(10,20,40,.08);
}
.pill.mono{font-family: var(--mono);}
.pill.btn{
  cursor:pointer;
  transition: transform .12s ease, background .12s ease, border-color .12s ease;
}
.pill.btn:hover{transform: translateY(-1px); border-color: rgba(255,255,255,.18); background: rgba(255,255,255,.08);}

.main{padding: 18px 0 calc(var(--tabH) + 28px);}
.heroCard{
  border-radius: var(--r24);
  background: linear-gradient(180deg, rgba(255,255,255,.08), rgba(255,255,255,.04));
  border: 1px solid rgba(255,255,255,.10);
  box-shadow: var(--shadow);
  overflow:hidden;
}
:root[data-theme="light"] .heroCard{
  background: linear-gradient(180deg, rgba(10,20,40,.06), rgba(10,20,40,.03));
  border: 1px solid rgba(10,20,40,.10);
}
.heroHead{
  padding: 18px 18px 16px;
  display:flex; align-items:flex-start; justify-content:space-between; gap: 16px;
}
.h1{font-size: 28px; font-weight: 900; letter-spacing:.2px;}
.sub{margin-top:6px; font-size: 13px; color: var(--mut);}

.ridBox{
  min-width: 320px;
  max-width: 520px;
  border-radius: 18px;
  border:1px solid rgba(255,255,255,.10);
  background: rgba(0,0,0,.18);
  padding: 12px 12px 10px;
}
:root[data-theme="light"] .ridBox{background: rgba(255,255,255,.55);}
.ridLabel{font-size:12px; color: var(--mut);}
.ridValue{
  margin-top:6px;
  font-family: var(--mono);
  font-size: 12px;
  word-break: break-all;
  opacity:.95;
}
.ridActions{margin-top:10px; display:flex; gap:8px; justify-content:flex-end;}
.btnSmall{
  cursor:pointer;
  border-radius: 12px;
  padding: 8px 10px;
  font-size: 12px;
  color: var(--txt);
  border:1px solid rgba(255,255,255,.12);
  background: rgba(255,255,255,.06);
  transition: transform .12s ease, background .12s ease, border-color .12s ease;
}
.btnSmall:hover{transform: translateY(-1px); border-color: rgba(255,255,255,.18); background: rgba(255,255,255,.09);}
.btnSmall.ghost{background: transparent;}

.content{margin-top: 16px;}
.grid{display:grid; grid-template-columns: 1fr; gap: 14px;}
@media (min-width: 900px){
  .grid.two{grid-template-columns: 1fr 1fr;}
}

.card{
  border-radius: var(--r20);
  border:1px solid rgba(255,255,255,.10);
  background: rgba(255,255,255,.06);
  box-shadow: 0 16px 70px rgba(0,0,0,.25);
  overflow:hidden;
}
:root[data-theme="light"] .card{
  background: rgba(10,20,40,.05);
  border:1px solid rgba(10,20,40,.10);
  box-shadow: 0 16px 70px rgba(10,20,40,.10);
}
.cardIn{padding: 16px;}
.cardTitle{font-weight: 800; font-size: 14px;}
.cardSub{margin-top:6px; font-size: 12px; color: var(--mut);}

.row{display:flex; align-items:center; justify-content:space-between; gap: 12px; margin-top: 12px;}
.mono{font-family: var(--mono);}

.bigAmount{
  font-size: 34px;
  font-weight: 900;
  letter-spacing:.2px;
}
.badge{
  font-size: 12px;
  padding: 6px 10px;
  border-radius: 999px;
  border:1px solid rgba(255,255,255,.12);
  background: rgba(255,255,255,.06);
  color: var(--mut);
}

.actions{
  display:flex; gap: 10px; flex-wrap:wrap;
  margin-top: 12px;
}
.btn{
  cursor:pointer;
  border-radius: 16px;
  padding: 12px 14px;
  font-weight: 800;
  font-size: 13px;
  border:1px solid rgba(255,255,255,.12);
  background: rgba(255,255,255,.06);
  color: var(--txt);
  transition: transform .12s ease, background .12s ease, border-color .12s ease;
}
.btn:hover{transform: translateY(-1px); border-color: rgba(255,255,255,.18); background: rgba(255,255,255,.09);}
.btn.primary{background: linear-gradient(135deg, rgba(79,124,255,.95), rgba(79,124,255,.55)); border-color: rgba(79,124,255,.70);}
.btn.success{background: linear-gradient(135deg, rgba(34,197,94,.95), rgba(34,197,94,.55)); border-color: rgba(34,197,94,.70);}
.btn.ghost{background: transparent;}
.btn.w100{width:100%}

.list{
  margin-top: 12px;
  border-radius: 16px;
  overflow:hidden;
  border:1px solid rgba(255,255,255,.08);
}
.item{
  display:flex; align-items:center; justify-content:space-between;
  padding: 12px 12px;
  border-top:1px solid rgba(255,255,255,.06);
  background: rgba(0,0,0,.14);
}
.item:first-child{border-top:none;}
:root[data-theme="light"] .item{background: rgba(255,255,255,.55);}
.itL{display:flex; align-items:center; gap: 10px;}
.coin{
  width: 34px; height: 34px; border-radius: 14px;
  border:1px solid rgba(255,255,255,.14);
  background: radial-gradient(10px 10px at 30% 30%, rgba(255,255,255,.55), transparent 65%),
              linear-gradient(135deg, rgba(79,124,255,.45), rgba(147,51,234,.35));
}
.sym{font-weight: 900;}
.name{font-size: 12px; color: var(--mut); margin-top:2px;}
.itR{text-align:right;}
.val{font-weight: 900;}
.small{font-size: 12px; color: var(--mut); margin-top:2px;}

.empty{
  margin-top: 10px;
  padding: 14px;
  border-radius: 16px;
  border:1px dashed rgba(255,255,255,.14);
  color: var(--mut);
}

/* Tabs */
.tabs{
  position:fixed; left:0; right:0; bottom:0;
  height: var(--tabH);
  display:flex; gap:10px;
  padding: 10px 12px;
  backdrop-filter: var(--blur);
  background: rgba(0,0,0,.32);
  border-top: 1px solid rgba(255,255,255,.06);
  z-index: 30;
}
:root[data-theme="light"] .tabs{
  background: rgba(255,255,255,.75);
  border-top: 1px solid rgba(10,20,40,.08);
}
.tab{
  flex:1;
  cursor:pointer;
  border-radius: 16px;
  border: 1px solid rgba(255,255,255,.10);
  background: rgba(255,255,255,.06);
  color: var(--txt);
  padding: 10px 6px;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  gap: 6px;
  transition: transform .12s ease, background .12s ease, border-color .12s ease;
}
.tab:hover{transform: translateY(-1px); border-color: rgba(255,255,255,.16); background: rgba(255,255,255,.08);}
.tab.active{
  background: linear-gradient(135deg, rgba(79,124,255,.35), rgba(34,197,94,.16));
  border-color: rgba(79,124,255,.26);
}
.ico{opacity:.95; font-size: 14px;}
.t{font-size: 12px; font-weight: 800; opacity:.95;}

/* Toast */
.toast{
  position:fixed; left:50%; transform:translateX(-50%);
  bottom: calc(var(--tabH) + 16px);
  padding: 10px 14px;
  border-radius: 999px;
  border:1px solid rgba(255,255,255,.12);
  background: rgba(0,0,0,.35);
  backdrop-filter: var(--blur);
  color: var(--txt);
  font-size: 13px;
  opacity:0; pointer-events:none;
  transition: opacity .18s ease, transform .18s ease;
  z-index: 40;
}
.toast.show{opacity:1; transform:translateX(-50%) translateY(-2px);}

/* Modal */
.modal{position:fixed; inset:0; display:none; z-index:50;}
.modal[aria-hidden="false"]{display:block;}
.modalBack{position:absolute; inset:0; background: rgba(0,0,0,.55);}
.modalCard{
  position:absolute; left:50%; top:50%;
  transform: translate(-50%,-50%);
  width: min(560px, calc(100vw - 26px));
  border-radius: 22px;
  border:1px solid rgba(255,255,255,.12);
  background: rgba(10,14,24,.78);
  backdrop-filter: var(--blur);
  box-shadow: 0 30px 120px rgba(0,0,0,.65);
  overflow:hidden;
}
:root[data-theme="light"] .modalCard{background: rgba(255,255,255,.92);}
.modalTop{
  display:flex; align-items:center; justify-content:space-between;
  padding: 14px 14px;
  border-bottom:1px solid rgba(255,255,255,.08);
}
.modalTitle{font-weight: 900;}
.modalClose{
  cursor:pointer;
  width: 34px; height: 34px;
  border-radius: 12px;
  border:1px solid rgba(255,255,255,.12);
  background: rgba(255,255,255,.06);
  color: var(--txt);
  font-size: 18px;
}
.modalBody{padding: 14px;}
.modalFoot{padding: 0 14px 14px; display:flex; gap:10px; justify-content:flex-end;}

.input{
  width:100%;
  border-radius: 16px;
  padding: 12px 12px;
  border:1px solid rgba(255,255,255,.12);
  background: rgba(255,255,255,.06);
  color: var(--txt);
  outline:none;
  font-size: 13px;
}
.input::placeholder{color: rgba(152,163,199,.75);}
.label{font-size: 12px; color: var(--mut); margin: 10px 0 6px;}
.hr{height:1px; background: rgba(255,255,255,.08); margin: 12px 0;}

/* =========================
   PREMIUM V2 OVERRIDES
   ========================= */

/* softer, richer background motion */
@keyframes logosFloat {
  from { transform: translate3d(0,0,0) scale(1); opacity:.20; }
  to   { transform: translate3d(0,-18px,0) scale(1.03); opacity:.24; }
}
.glow{ animation: logosFloat 18s ease-in-out infinite alternate; }
.g2{ animation-duration: 22s; }
.g3{ animation-duration: 26s; }

.topbar{
  border-bottom: 1px solid rgba(255,255,255,.07);
}
:root[data-theme="light"] .topbar{
  border-bottom: 1px solid rgba(10,20,40,.09);
}

.heroCard, .card, .modalCard{
  position: relative;
}

/* premium gradient border */
.heroCard::before, .card::before, .modalCard::before{
  content:"";
  position:absolute; inset:0;
  border-radius: inherit;
  padding: 1px;
  background: linear-gradient(135deg,
    rgba(255,255,255,.18),
    rgba(79,124,255,.18),
    rgba(34,197,94,.14),
    rgba(255,255,255,.10)
  );
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events:none;
  opacity:.55;
}

.heroCard{
  background:
    radial-gradient(900px 420px at 20% 0%, rgba(79,124,255,.16), transparent 55%),
    radial-gradient(900px 420px at 80% 0%, rgba(34,197,94,.12), transparent 55%),
    linear-gradient(180deg, rgba(255,255,255,.08), rgba(255,255,255,.04));
}

.card{
  background:
    radial-gradient(680px 340px at 15% 0%, rgba(255,255,255,.06), transparent 60%),
    rgba(255,255,255,.06);
}

:root[data-theme="light"] .heroCard{
  background:
    radial-gradient(900px 420px at 20% 0%, rgba(79,124,255,.11), transparent 55%),
    radial-gradient(900px 420px at 80% 0%, rgba(34,197,94,.10), transparent 55%),
    linear-gradient(180deg, rgba(10,20,40,.06), rgba(10,20,40,.03));
}

/* typography tighter */
.h1{ font-size: 30px; letter-spacing:.15px; }
.sub{ font-size: 13px; line-height: 1.35; }

/* RID box more premium */
.ridBox{
  background: rgba(0,0,0,.22);
  border: 1px solid rgba(255,255,255,.10);
  box-shadow: 0 18px 70px rgba(0,0,0,.35);
}
:root[data-theme="light"] .ridBox{
  background: rgba(255,255,255,.70);
  box-shadow: 0 18px 70px rgba(10,20,40,.10);
}

/* buttons: consistent height, better shine */
.btn, .btnSmall{
  letter-spacing: .15px;
}
.btn{
  padding: 12px 16px;
  border-radius: 16px;
  box-shadow: 0 14px 50px rgba(0,0,0,.18);
}
.btn.primary{
  background: linear-gradient(135deg, rgba(79,124,255,1), rgba(79,124,255,.55));
  box-shadow: 0 18px 60px rgba(79,124,255,.18);
}
.btn.success{
  background: linear-gradient(135deg, rgba(34,197,94,1), rgba(34,197,94,.55));
  box-shadow: 0 18px 60px rgba(34,197,94,.16);
}
.btn.ghost{
  background: rgba(255,255,255,.04);
}
.btn:hover{ background: rgba(255,255,255,.10); }
.btn.primary:hover{ filter: brightness(1.03); }
.btn.success:hover{ filter: brightness(1.03); }

/* empty state: remove dashed, make it premium block */
.empty{
  border: 1px solid rgba(255,255,255,.10);
  border-radius: 16px;
  background: rgba(255,255,255,.05);
  color: rgba(152,163,199,.95);
}

/* tabs: safe-area + tighter premium feel */
.tabs{
  padding-bottom: calc(10px + env(safe-area-inset-bottom));
  height: calc(var(--tabH) + env(safe-area-inset-bottom));
  background: rgba(0,0,0,.42);
}
:root[data-theme="light"] .tabs{
  background: rgba(255,255,255,.86);
}

.tab{
  border-radius: 18px;
}
.tab.active{
  background: linear-gradient(135deg, rgba(79,124,255,.40), rgba(34,197,94,.18));
  box-shadow: 0 18px 60px rgba(0,0,0,.22);
}

/* responsive: phone/tablet */
@media (max-width: 980px){
  .heroHead{ flex-direction: column; align-items: stretch; }
  .ridBox{ min-width: 0; width: 100%; }
  .topbar .wrap{ gap: 10px; }
  .topRight{ justify-content: flex-start; }
}

@media (max-width: 520px){
  .wrap{ padding: 0 14px; }
  .h1{ font-size: 24px; }
  .pill{ padding: 7px 10px; font-size: 11px; }
  .btn{ width: 100%; justify-content:center; }
  .actions{ gap: 8px; }
  .tabs{ gap: 8px; }
  .t{ font-size: 11px; }
}
```

---

## FILE: /opt/logos/www/wallet_v2/api_base.js

- bytes: 178
- sha256: `ec9b0084cca46c0917a6843317daed618a2baa781d9182f2870903ee6cde6303`

```js
(() => {
  const origin = window.location.origin.replace(/\/+$/, "");
  window.LOGOS_WALLET_API = origin + "/wallet-api";
  window.LOGOS_NODE_API   = origin + "/node-api";
})();
```

---

## FILE: /opt/logos/www/wallet_v2/app.css

- bytes: 682
- sha256: `2e8e444586c03fc5f72594fafb26e4ed1a8f1cba45d6214545e5b5ff1b5c49c4`

```css
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

---

## FILE: /opt/logos/www/wallet_v2/app.html

- bytes: 4271
- sha256: `1e467004ae5ef7c4cc0fedc6db2815a21b75a5e6eb5dc01aa850076b7ee1fdf5`

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta http-equiv="Cache-Control" content="no-store"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Wallet</title>
<script src="./api_base.js"></script>
<link rel="stylesheet" href="/shared/wallet-theme.css?v=20260101_v2"/>
<link rel="stylesheet" href="./app.css?v=20260101_v2"/>
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
</body>
</html>
```

---

## FILE: /opt/logos/www/wallet_v2/app.js

- bytes: 11592
- sha256: `297ab77d740c6f02befed611f151483809435b5cf6efba6e1c031efbeeaa698d`

```js
'use strict';

const API = (window.API_ENDPOINT || (location.origin.replace(/\/$/, '') + '/node-api'));

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

---

## FILE: /opt/logos/www/wallet_v2/auth.css

- bytes: 880
- sha256: `5bb92959c854d22f3ee130a885db5b63cc7b8ddef762aad30a83b7d9f0ea52c7`

```css
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

---

## FILE: /opt/logos/www/wallet_v2/auth.html

- bytes: 5310
- sha256: `172474077c95c5416351c1c8fb5395fc6873ef1dd707766305cf4a1e54559b62`

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta http-equiv="Cache-Control" content="no-store"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LOGOS Wallet — Secure</title>
<script src="./api_base.js"></script>
<link rel="stylesheet" href="/shared/wallet-theme.css?v=20260101_v2"/>
<link rel="stylesheet" href="./auth.css?v=20260101_v2"/>
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
  <script src="./auth.js?v=20251212_04" defer></script>
</body>
</html>
```

---

## FILE: /opt/logos/www/wallet_v2/auth.js

- bytes: 13439
- sha256: `e1b59d809dd464f168fe52c06d4bec95f5739c63e14c7fff0f32b43a49f468dc`

```js
(() => {
  try {
    const q = new URLSearchParams(location.search);
    if (q.get("connect") === "1") {
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

---

## FILE: /opt/logos/www/wallet_v2/compat.js

- bytes: 5512
- sha256: `a178c9fb576fbacbd49c8dd57e116b4d6e0b43c73677d826dde3d2adf393bb69`

```js
"use strict";

(function () {
  // Базовый URL API
  const API = location.origin + "/node-api";

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

---

## FILE: /opt/logos/www/wallet_v2/index.html

- bytes: 256
- sha256: `e78933e9729d46fa2a7f0f45fc58917fa27a19b294bea052518d518c27333602`

```html
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <meta http-equiv="refresh" content="0; url=./auth.html">
  <title>LOGOS Wallet</title>
</head>
<body></body>
</html>
```

---

## FILE: /opt/logos/www/wallet_v2/login.html

- bytes: 318
- sha256: `409ff9c314f528c39591bcd2cb7bc400fc1eb9c9e25669f231ff1b73c1cd35d0`

```html
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

---

## FILE: /opt/logos/www/wallet_v2/ui.js

- bytes: 3447
- sha256: `e2814b431d1cf6c38a9f2efb1513d597b402d488d40e968cb87289c66f92f550`

```js
(() => {
  // Берём API из app.js, если он есть, иначе собираем по origin
  const API_BASE = (window.API ||
                    window.API_ENDPOINT ||
                    (location.origin.replace(/\/$/, '') + '/node-api'));

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

---

## FILE: /opt/logos/www/wallet_v2/wallet.css

- bytes: 5953
- sha256: `d808788cbb5a493d8185bb14b7021d8bcaeed7a56ce194e49e02c8aaf9607a9f`

```css
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

---

## FILE: /var/www/logos/explorer/explorer.css

- bytes: 898
- sha256: `0952db5465ce69b04c3559e658e4c6d575e01c8a26d28e022f1987a6d4f8ddba`

```css
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

---

## FILE: /var/www/logos/explorer/explorer.js

- bytes: 3977
- sha256: `bfc2b03314887fd05ebaacab69042e7e97a9c48c1ea194fc5c7d90d090b1712b`

```js
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

---

## FILE: /var/www/logos/explorer/index.html

- bytes: 8165
- sha256: `2814580324c6e2bd931bf8f73353a302eb7c3d92f6b0c2e04c22ede5d35598cf`

```html
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

---

## FILE: /var/www/logos/wallet/app.html

- bytes: 3367
- sha256: `634d3867f77eaeb5b11e7c03a6f23a7891bd1ec3cadede0b0ed29aec5eb8d0d2`

```html
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

---

## FILE: /var/www/logos/wallet/app.js

- bytes: 7641
- sha256: `a301fedea06feff7c9c43f1fd80e19f66355711e7a300310854392fdb5a50ea9`

```js
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

---

## FILE: /var/www/logos/wallet/app.v2.js

- bytes: 7526
- sha256: `e9acf520c904ab392b74518030f6f81c0da9b43d938f7d408f374468f168d7c2`

```js
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

---

## FILE: /var/www/logos/wallet/app.v3.js

- bytes: 6952
- sha256: `e9f7272b2a65262b3713102884f515e82b1b3b52f9fb10de54a46f778ebe409b`

```js
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

---

## FILE: /var/www/logos/wallet/auth.js

- bytes: 6002
- sha256: `fefed14c6d58709cc481ccb34378dc5240a2f76c0b5d315328b0706527c7cc3a`

```js
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

---

## FILE: /var/www/logos/wallet/css/styles.css

- bytes: 2270
- sha256: `a2dd294d4f6f10b6a01511de57b69bee4e5aed2457bf893c03c77d4f96d2dba1`

```css
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

---

## FILE: /var/www/logos/wallet/index.html

- bytes: 5903
- sha256: `0629ed0668698ab977e320303911233410e28219845e1012e59ed9fd751877ae`

```html
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

---

## FILE: /var/www/logos/wallet/js/api.js

- bytes: 446
- sha256: `d7c8de571b89cf178b4c084cf461a26512eafef8ca6b4efdf4e1bcd995fabbc3`

```js
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

---

## FILE: /var/www/logos/wallet/js/app.js

- bytes: 3610
- sha256: `ff9df2e7272ed410962e42170babe3e5b855cbc494d8c1a1e502acebcf62c5a0`

```js
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

---

## FILE: /var/www/logos/wallet/js/app_wallet.js

- bytes: 4816
- sha256: `3ec80420f9bfbedb73db755a6f688ac4a9d16a3691b89f191f083fcd3c72ba22`

```js
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

---

## FILE: /var/www/logos/wallet/js/core.js

- bytes: 1634
- sha256: `c7945df9a59702b6472d5dfc23ab3a2ecafd0e8da09f0b6ff9326f2ff5404999`

```js
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

---

## FILE: /var/www/logos/wallet/js/unlock.js

- bytes: 3602
- sha256: `f819fe2b9511596855587364fe63cd812a5a5a5818eef3705d837aa192b0920d`

```js
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

---

## FILE: /var/www/logos/wallet/js/vault.js

- bytes: 4090
- sha256: `6ac459153d56c6341c228bc0d5a9b89dac4c3328ee721f2de223426add371360`

```js
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

---

## FILE: /var/www/logos/wallet/js/vault_bridge.js

- bytes: 2674
- sha256: `71a3433fd19f20429ee8cd6da2d595d741cf773a5ed046a8b723a5fc58578b8a`

```js
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

---

## FILE: /var/www/logos/wallet/login.html

- bytes: 2647
- sha256: `3ca5265f2e0466f2eff556f4dba96f74b7eb273d46c7e80f40a4ed2c5cf89f76`

```html
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

---

## FILE: /var/www/logos/wallet/ping.html

- bytes: 118
- sha256: `f61ad705f4efcaf7052bfc46732bb9dbe7a114080497fe517298ffb76037fe38`

```html
<!doctype html><meta charset="utf-8">
<title>Wallet JS Ping</title>
<button onclick="alert('JS OK')">JS TEST</button>
```

---

## FILE: /var/www/logos/wallet/staking.js

- bytes: 2843
- sha256: `ca94693b752e5a374ec8cba2b8021aac7980bfca2fa709085e42cd7a883eab80`

```js
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

---

## FILE: /var/www/logos/wallet/wallet.css

- bytes: 2693
- sha256: `1413b79b9823910371cf973a3a7cb70c20d73be37196ca319d58a36298be85ad`

```css
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

---

## FILE: /var/www/logos/wallet/wallet.js

- bytes: 9153
- sha256: `5249fd53f7d4a5ad1031f904ae24a52041c26cc90599a9d42e2ae6ff1c0bb80c`

```js
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

---

## FILE: /var/www/logos/wallet3/app.v3.js

- bytes: 6763
- sha256: `2c33a6e556cae1e08ac3a6e41d53f83b0a4b8c0d046e06ae942715202d4cb349`

```js
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

---

## FILE: /var/www/logos/wallet3/index.html

- bytes: 3528
- sha256: `16003569d375db6705f3ef3ef95cc6bada61364a55382823e7f25af1a7dd8717`

```html
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

---

## FILE: docs/WALLET_PERIMETER_FULL_V2/node_api_openapi.json

- bytes: 9861
- sha256: `937381217e4244fdb79c730f21892ad79849995bb2dc84dfbec91d2c3e903b88`

```json
{
  "openapi": "3.0.3",
  "info": {
    "title": "LOGOS LRB — Core API",
    "version": "0.1.0",
    "description": "Public & Admin API for LOGOS LRB (strict CSP, JWT admin, rToken bridge, archive)"
  },
  "servers": [{ "url": "https://45-159-248-232.sslip.io" }],
  "paths": {
    "/healthz": {
      "get": { "summary": "Healthcheck", "responses": { "200": { "description": "OK", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/OkMsg" } } } } } }
    },
    "/head": {
      "get": { "summary": "Chain head", "responses": { "200": { "description": "Head", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/Head" } } } } } }
    },
    "/balance/{rid}": {
      "get": {
        "summary": "Account balance & nonce",
        "parameters": [{ "name": "rid", "in": "path", "required": true, "schema": { "type": "string" } }],
        "responses": { "200": { "description": "Balance", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/Balance" } } } } }
      }
    },
    "/submit_tx": {
      "post": {
        "summary": "Submit transaction",
        "requestBody": { "required": true, "content": { "application/json": { "schema": { "$ref": "#/components/schemas/TxIn" } } } },
        "responses": { "200": { "description": "Result", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/SubmitResult" } } } } }
      }
    },
    "/economy": {
      "get": { "summary": "Economy snapshot", "responses": { "200": { "description": "Economy", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/Economy" } } } } } }
    },
    "/history/{rid}": {
      "get": {
        "summary": "History by RID (from sled index)",
        "parameters": [{ "name": "rid", "in": "path", "required": true, "schema": { "type": "string" } }],
        "responses": {
          "200": { "description": "History", "content": { "application/json": { "schema": { "type": "array", "items": { "$ref": "#/components/schemas/HistoryItem" } } } } }
        }
      }
    },
    "/archive/history/{rid}": {
      "get": {
        "summary": "History by RID (archive backend: SQLite/PG)",
        "parameters": [{ "name": "rid", "in": "path", "required": true, "schema": { "type": "string" } }],
        "responses": {
          "200": { "description": "History", "content": { "application/json": { "schema": { "type": "array", "items": { "type": "object" } } } } }
        }
      }
    },
    "/archive/tx/{txid}": {
      "get": {
        "summary": "Get TX by txid (archive backend)",
        "parameters": [{ "name": "txid", "in": "path", "required": true, "schema": { "type": "string" } }],
        "responses": {
          "200": { "description": "TX (if any)", "content": { "application/json": { "schema": { "type": "object" } } } }
        }
      }
    },
    "/bridge/deposit": {
      "post": {
        "summary": "Register external deposit to rToken",
        "security": [{ "BridgeKey": [] }],
        "requestBody": { "required": true, "content": { "application/json": { "schema": { "$ref": "#/components/schemas/DepositReq" } } } },
        "responses": { "200": { "description": "BridgeResp", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/BridgeResp" } } } } }
      }
    },
    "/bridge/redeem": {
      "post": {
        "summary": "Request redeem from rToken to external chain",
        "security": [{ "BridgeKey": [] }],
        "requestBody": { "required": true, "content": { "application/json": { "schema": { "$ref": "#/components/schemas/RedeemReq" } } } },
        "responses": { "200": { "description": "BridgeResp", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/BridgeResp" } } } } }
      }
    },
    "/bridge/verify": {
      "post": {
        "summary": "Verify bridge operation",
        "security": [{ "BridgeKey": [] }],
        "requestBody": { "required": true, "content": { "application/json": { "schema": { "$ref": "#/components/schemas/VerifyReq" } } } },
        "responses": { "200": { "description": "BridgeResp", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/BridgeResp" } } } } }
      }
    },
    "/admin/set_balance": {
      "post": {
        "summary": "Set balance (admin)",
        "security": [{ "AdminJWT": [] }],
        "requestBody": { "required": true, "content": { "application/json": { "schema": { "$ref": "#/components/schemas/SetBalanceReq" } } } },
        "responses": { "200": { "description": "OK", "content": { "application/json": { "schema": { "type": "object" } } } } }
      }
    },
    "/admin/set_nonce": {
      "post": {
        "summary": "Set nonce (admin)",
        "security": [{ "AdminJWT": [] }],
        "requestBody": { "required": true, "content": { "application/json": { "schema": { "$ref": "#/components/schemas/SetNonceReq" } } } },
        "responses": { "200": { "description": "OK", "content": { "application/json": { "schema": { "type": "object" } } } } }
      }
    },
    "/admin/bump_nonce": {
      "post": {
        "summary": "Bump nonce (admin)",
        "security": [{ "AdminJWT": [] }],
        "requestBody": { "required": true, "content": { "application/json": { "schema": { "$ref": "#/components/schemas/BumpNonceReq" } } } },
        "responses": { "200": { "description": "OK", "content": { "application/json": { "schema": { "type": "object" } } } } }
      }
    },
    "/admin/mint": {
      "post": {
        "summary": "Add minted amount (admin)",
        "security": [{ "AdminJWT": [] }],
        "requestBody": { "required": true, "content": { "application/json": { "schema": { "$ref": "#/components/schemas/MintReq" } } } },
        "responses": { "200": { "description": "OK", "content": { "application/json": { "schema": { "type": "object" } } } } }
      }
    },
    "/admin/burn": {
      "post": {
        "summary": "Add burned amount (admin)",
        "security": [{ "AdminJWT": [] }],
        "requestBody": { "required": true, "content": { "application/json": { "schema": { "$ref": "#/components/schemas/BurnReq" } } } },
        "responses": { "200": { "description": "OK", "content": { "application/json": { "schema": { "type": "object" } } } } }
      }
    }
  },
  "components": {
    "securitySchemes": {
      "AdminJWT": { "type": "apiKey", "in": "header", "name": "X-Admin-JWT" },
      "BridgeKey": { "type": "apiKey", "in": "header", "name": "X-Bridge-Key" }
    },
    "schemas": {
      "OkMsg": { "type": "object", "properties": { "status": { "type": "string" } }, "required": ["status"] },
      "Head":  { "type": "object", "properties": { "height": { "type": "integer", "format": "uint64" } }, "required": ["height"] },
      "Balance": {
        "type": "object",
        "properties": { "rid": { "type": "string" }, "balance": { "type": "string" }, "nonce": { "type": "integer", "format": "uint64" } },
        "required": ["rid","balance","nonce"]
      },
      "TxIn": {
        "type": "object",
        "properties": {
          "from": { "type": "string" }, "to": { "type": "string" },
          "amount": { "type": "integer", "format": "uint64" },
          "nonce": { "type": "integer", "format": "uint64" },
          "memo": { "type": "string", "nullable": true },
          "sig_hex": { "type": "string" }
        },
        "required": ["from","to","amount","nonce","sig_hex"]
      },
      "SubmitResult": {
        "type": "object",
        "properties": {
          "ok": { "type": "boolean" },
          "txid": { "type": "string", "nullable": true },
          "info": { "type": "string" }
        }, "required": ["ok","info"]
      },
      "Economy": {
        "type": "object",
        "properties": { "supply": { "type": "integer" }, "burned": { "type": "integer" }, "cap": { "type": "integer" } },
        "required": ["supply","burned","cap"]
      },
      "HistoryItem": {
        "type": "object",
        "properties": {
          "txid": { "type": "string" }, "height": { "type": "integer" }, "from": { "type": "string" },
          "to": { "type": "string" }, "amount": { "type": "integer" }, "nonce": { "type": "integer" }, "ts": { "type": "integer", "nullable": true }
        },
        "required": ["txid","height","from","to","amount","nonce"]
      },
      "DepositReq": {
        "type": "object",
        "properties": { "txid":{ "type": "string" }, "amount":{ "type": "integer" }, "from_chain":{ "type": "string" }, "to_rid":{ "type": "string" } },
        "required": ["txid","amount","from_chain","to_rid"]
      },
      "RedeemReq": {
        "type": "object",
        "properties": { "rtoken_tx":{ "type": "string" }, "to_chain":{ "type": "string" }, "to_addr":{ "type": "string" }, "amount":{ "type": "integer" } },
        "required": ["rtoken_tx","to_chain","to_addr","amount"]
      },
      "VerifyReq": {
        "type": "object",
        "properties": { "op_id":{ "type": "string" } }, "required": ["op_id"]
      },
      "BridgeResp": {
        "type": "object",
        "properties": { "ok":{ "type": "boolean" }, "op_id":{ "type": "string" }, "info":{ "type": "string" } },
        "required": ["ok","op_id","info"]
      },
      "SetBalanceReq": { "type": "object", "properties": { "rid":{"type":"string"}, "amount":{"type":"string"} }, "required": ["rid","amount"] },
      "SetNonceReq":   { "type": "object", "properties": { "rid":{"type":"string"}, "value":{"type":"integer"} }, "required": ["rid","value"] },
      "BumpNonceReq":  { "type": "object", "properties": { "rid":{"type":"string"} }, "required": ["rid"] },
      "MintReq":       { "type": "object", "properties": { "amount":{"type":"integer"} }, "required": ["amount"] },
      "BurnReq":       { "type": "object", "properties": { "amount":{"type":"integer"} }, "required": ["amount"] }
    }
  }
}
```

---

## FILE: docs/WALLET_PERIMETER_FULL_V2/wallet_api_openapi.json

- bytes: 4758
- sha256: `639671c328c2da74c95c7bcae14f2e79b66327e8670a51333d392372f99f1ed7`

```json
{"openapi":"3.1.0","info":{"title":"LRB Wallet Proxy","version":"1.2"},"paths":{"/metrics":{"get":{"summary":"Metrics","operationId":"metrics_metrics_get","responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{}}}}}}},"/v1/receive/{rid}":{"get":{"summary":"Receive Addresses","operationId":"receive_addresses_v1_receive__rid__get","parameters":[{"name":"rid","in":"path","required":true,"schema":{"type":"string","title":"Rid"}}],"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/v1/balances/{rid}":{"get":{"summary":"Balances","operationId":"balances_v1_balances__rid__get","parameters":[{"name":"rid","in":"path","required":true,"schema":{"type":"string","title":"Rid"}}],"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/":{"get":{"summary":"Root","operationId":"root__get","responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{}}}}}}},"/v1/topup/request":{"post":{"summary":"Topup Request","operationId":"topup_request_v1_topup_request_post","requestBody":{"content":{"application/json":{"schema":{"$ref":"#/components/schemas/TopupRequest"}}},"required":true},"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/TopupResponse"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/v1/withdraw":{"post":{"summary":"Withdraw","operationId":"withdraw_v1_withdraw_post","requestBody":{"content":{"application/json":{"schema":{"$ref":"#/components/schemas/WithdrawRequest"}}},"required":true},"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/v1/quote":{"post":{"summary":"Quote","operationId":"quote_v1_quote_post","requestBody":{"content":{"application/json":{"schema":{"$ref":"#/components/schemas/QuoteRequest"}}},"required":true},"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/QuoteResponse"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}}},"components":{"schemas":{"HTTPValidationError":{"properties":{"detail":{"items":{"$ref":"#/components/schemas/ValidationError"},"type":"array","title":"Detail"}},"type":"object","title":"HTTPValidationError"},"QuoteRequest":{"properties":{"from_token":{"type":"string","title":"From Token"},"to_token":{"type":"string","title":"To Token"},"amount":{"type":"integer","title":"Amount"}},"type":"object","required":["from_token","to_token","amount"],"title":"QuoteRequest"},"QuoteResponse":{"properties":{"price":{"type":"number","title":"Price"},"expected_out":{"type":"number","title":"Expected Out"}},"type":"object","required":["price","expected_out"],"title":"QuoteResponse"},"TopupRequest":{"properties":{"rid":{"type":"string","title":"Rid"},"token":{"type":"string","const":"USDT","title":"Token","default":"USDT"},"network":{"type":"string","const":"ETH","title":"Network","default":"ETH"}},"type":"object","required":["rid"],"title":"TopupRequest"},"TopupResponse":{"properties":{"rid":{"type":"string","title":"Rid"},"token":{"type":"string","title":"Token"},"network":{"type":"string","title":"Network"},"address":{"type":"string","title":"Address"}},"type":"object","required":["rid","token","network","address"],"title":"TopupResponse"},"ValidationError":{"properties":{"loc":{"items":{"anyOf":[{"type":"string"},{"type":"integer"}]},"type":"array","title":"Location"},"msg":{"type":"string","title":"Message"},"type":{"type":"string","title":"Error Type"}},"type":"object","required":["loc","msg","type"],"title":"ValidationError"},"WithdrawRequest":{"properties":{"rid":{"type":"string","title":"Rid"},"token":{"type":"string","const":"USDT","title":"Token","default":"USDT"},"network":{"type":"string","const":"ETH","title":"Network","default":"ETH"},"amount":{"type":"integer","title":"Amount"},"to_address":{"type":"string","title":"To Address"},"request_id":{"type":"string","title":"Request Id"}},"type":"object","required":["rid","amount","to_address","request_id"],"title":"WithdrawRequest"}}}}
```

---

