# LOGOS — Directory Book: /var/www/logos/css

_Generated: 2025-12-31T06:43:51Z_

**Part:** 1

---

## STRUCTURE

```text
/var/www/logos/css
```

---

## FILES (FULL SOURCE)


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
