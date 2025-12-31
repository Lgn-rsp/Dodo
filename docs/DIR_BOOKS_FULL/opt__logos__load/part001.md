# LOGOS — Directory Book: /opt/logos/load

_Generated: 2025-12-31T06:43:51Z_

**Part:** 1

---

## STRUCTURE

```text
/opt/logos/load
```

---

## FILES (FULL SOURCE)


### FILE: /opt/logos/load/gen_signed_tx.py

```
import os, json, binascii
from nacl import signing

NODE   = os.environ.get("LOGOS_NODE","http://127.0.0.1:8080")
FROM   = os.environ["RID_A"]
TO     = os.environ["RID_B"]
START  = int(os.environ.get("NONCE_START","1"))
COUNT  = int(os.environ.get("COUNT","50000"))
AMOUNT = int(os.environ.get("AMOUNT_MICRO","1111"))

sk = signing.SigningKey.generate()
def sig_hex(msg: bytes) -> str:
    return binascii.hexlify(sk.sign(msg).signature).decode()

with open("/opt/logos/load/tx_payloads.jsonl", "w") as f:
    for i in range(COUNT):
        nonce = START + i
        msg = f"{FROM}|{TO}|{AMOUNT}|{nonce}".encode("utf-8")
        payload = {
            "from": FROM, "to": TO, "amount": AMOUNT, "nonce": nonce,
            "sig_hex": sig_hex(msg)
        }
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")
print("Wrote", COUNT, "payloads -> /opt/logos/load/tx_payloads.jsonl")

```

### FILE: /opt/logos/load/read_test.js

```
import http from 'k6/http';
import { sleep, check } from 'k6';

export let options = {
  scenarios: {
    head:     { executor: 'constant-arrival-rate', rate: 300, timeUnit: '1s', duration: '60s', preAllocatedVUs: 50, exec: 'head' },
    balance:  { executor: 'constant-arrival-rate', rate: 500, timeUnit: '1s', duration: '60s', preAllocatedVUs: 80, exec: 'balance' },
    history:  { executor: 'constant-arrival-rate', rate: 200, timeUnit: '1s', duration: '60s', preAllocatedVUs: 50, exec: 'history' },
  },
  thresholds: {
    'http_req_duration{type:head}':    ['p(95)<10', 'p(99)<25'],
    'http_req_duration{type:balance}': ['p(95)<10', 'p(99)<25'],
    'http_req_duration{type:history}': ['p(95)<25', 'p(99)<50'],
    'http_req_failed': ['rate<0.001'],
  },
};

const BASE = __ENV.LOGOS_NODE || 'http://127.0.0.1:8080';
const RID_A = __ENV.RID_A;

export function head() {
  const res = http.get(`${BASE}/head`, { tags: { type: 'head' } });
  check(res, { '200': r => r.status === 200 });
}

export function balance() {
  const encRid = encodeURIComponent(RID_A);
  const res = http.get(`${BASE}/balance/${encRid}`, { tags: { type: 'balance' } });
  check(res, { '200': r => r.status === 200 });
}

export function history() {
  const encRid = encodeURIComponent(RID_A);
  const res = http.get(`${BASE}/archive/history/${encRid}`, { tags: { type: 'history' } });
  check(res, { '200': r => r.status === 200 });
  sleep(0.01);
}

```

### FILE: /opt/logos/load/write_test.js

```
import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';

export let options = {
  scenarios: {
    write: {
      executor: 'constant-arrival-rate',
      rate: 1000,          // RPS (можно поднять до 2k–5k)
      timeUnit: '1s',
      duration: '60s',
      preAllocatedVUs: 200,
      maxVUs: 2000,
    }
  },
  thresholds: {
    http_req_failed: ['rate<0.001'],     // <0.1% ошибок
    http_req_duration: ['p(95)<50', 'p(99)<100'], // латентность
  },
};

const BASE = __ENV.LOGOS_NODE || 'http://127.0.0.1:8080';

// Подгружаем подготовленные payloads (jsonl)
const lines = new SharedArray('txs', function () {
  const data = open('/opt/logos/load/tx_payloads.jsonl');
  return data.trim().split('\n');
});

let idx = 0;

export default function () {
  const i = (idx++) % lines.length;
  const payload = JSON.parse(lines[i]);
  const res = http.post(`${BASE}/submit_tx`, JSON.stringify(payload), {
    headers: { 'Content-Type': 'application/json' },
  });
  check(res, {
    '200': (r) => r.status === 200,
    'ok or bad nonce': (r) => {
      try { const j = r.json(); return j.ok === true || (j.info && String(j.info).includes('nonce')); } catch(e){ return false; }
    },
  });
  if (__ITER % 1000 === 0) sleep(0.01); // мелкий паузер для GC
}

```
