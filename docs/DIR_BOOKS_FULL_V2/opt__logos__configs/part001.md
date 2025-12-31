# FULL SOURCE — `/opt/logos/configs`

**No truncation.** Full file contents inside code fences.


---

## FILE: `/opt/logos/configs/genesis.yaml`

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

## FILE: `/opt/logos/configs/logos_config.yaml`

```yaml
node:
  listen: "0.0.0.0:8080"
  data_path: "/var/lib/logos/data.sled"
  node_key_path: "/var/lib/logos/node_key"
limits:
  mempool_cap: 100000
  max_block_tx: 10000
  slot_ms: 500
guard:
  rate_limit_qps: 30
  cidr_bypass: ["127.0.0.1/32","::1/128"]
phase:
  enabled: true
  freqs_hz: [7.83, 1.618, 432]
  min_score: -0.2
bridge:
  max_per_tx: 10000000
explorer:
  page_size: 50
```
