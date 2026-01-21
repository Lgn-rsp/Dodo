# MEM Book (mempool / tx / block / verify / head)

- Generated: `20260121T154907Z`
- Repo: `/root/logos_lrb`

## Included files
- OK: /root/logos_lrb/lrb_core/Cargo.toml
- OK: /root/logos_lrb/lrb_core/src/types.rs
- OK: /root/logos_lrb/lrb_core/src/crypto.rs
- OK: /root/logos_lrb/lrb_core/src/anti_replay.rs
- OK: /root/logos_lrb/lrb_core/src/ledger.rs
- OK: /root/logos_lrb/lrb_core/src/spam_guard.rs
- OK: /root/logos_lrb/lrb_core/src/sigpool.rs
- OK: /root/logos_lrb/lrb_core/src/rcp_engine.rs
- OK: /root/logos_lrb/lrb_core/src/quorum.rs
- OK: /root/logos_lrb/lrb_core/src/phase_consensus.rs
- OK: /root/logos_lrb/lrb_core/src/phase_integrity.rs
- OK: /root/logos_lrb/node/Cargo.toml
- OK: /root/logos_lrb/node/build.rs
- OK: /root/logos_lrb/node/src/lib.rs
- OK: /root/logos_lrb/node/src/main.rs
- OK: /root/logos_lrb/node/src/state.rs
- OK: /root/logos_lrb/node/src/storage.rs
- OK: /root/logos_lrb/node/src/fork.rs
- MISSING: /root/logos_lrb/node/src/producer.rs
- OK: /root/logos_lrb/node/src/gossip.rs
- OK: /root/logos_lrb/node/src/peers.rs
- OK: /root/logos_lrb/node/src/guard.rs
- OK: /root/logos_lrb/node/src/metrics.rs
- OK: /root/logos_lrb/node/src/api/mod.rs
- OK: /root/logos_lrb/node/src/api/base.rs
- OK: /root/logos_lrb/node/src/api/tx.rs
- OK: /root/logos_lrb/node/src/archive/mod.rs
- OK: /root/logos_lrb/node/src/archive/pg.rs
- OK: /root/logos_lrb/node/src/archive/sqlite.rs

## Contents
- [lrb_core/Cargo.toml](#lrb_core-Cargo-toml)
- [lrb_core/src/types.rs](#lrb_core-src-types-rs)
- [lrb_core/src/crypto.rs](#lrb_core-src-crypto-rs)
- [lrb_core/src/anti_replay.rs](#lrb_core-src-anti_replay-rs)
- [lrb_core/src/ledger.rs](#lrb_core-src-ledger-rs)
- [lrb_core/src/spam_guard.rs](#lrb_core-src-spam_guard-rs)
- [lrb_core/src/sigpool.rs](#lrb_core-src-sigpool-rs)
- [lrb_core/src/rcp_engine.rs](#lrb_core-src-rcp_engine-rs)
- [lrb_core/src/quorum.rs](#lrb_core-src-quorum-rs)
- [lrb_core/src/phase_consensus.rs](#lrb_core-src-phase_consensus-rs)
- [lrb_core/src/phase_integrity.rs](#lrb_core-src-phase_integrity-rs)
- [node/Cargo.toml](#node-Cargo-toml)
- [node/build.rs](#node-build-rs)
- [node/src/lib.rs](#node-src-lib-rs)
- [node/src/main.rs](#node-src-main-rs)
- [node/src/state.rs](#node-src-state-rs)
- [node/src/storage.rs](#node-src-storage-rs)
- [node/src/fork.rs](#node-src-fork-rs)
- [node/src/gossip.rs](#node-src-gossip-rs)
- [node/src/peers.rs](#node-src-peers-rs)
- [node/src/guard.rs](#node-src-guard-rs)
- [node/src/metrics.rs](#node-src-metrics-rs)
- [node/src/api/mod.rs](#node-src-api-mod-rs)
- [node/src/api/base.rs](#node-src-api-base-rs)
- [node/src/api/tx.rs](#node-src-api-tx-rs)
- [node/src/archive/mod.rs](#node-src-archive-mod-rs)
- [node/src/archive/pg.rs](#node-src-archive-pg-rs)
- [node/src/archive/sqlite.rs](#node-src-archive-sqlite-rs)


## lrb_core/Cargo.toml
<a id="lrb_core-Cargo-toml"></a>

```toml
[package]
name = "lrb_core"
version = "0.1.0"
edition = "2021"

[dependencies]
anyhow = { workspace = true }
thiserror = { workspace = true }
serde = { workspace = true }
serde_json = { workspace = true }
tracing = { workspace = true }
bytes = { workspace = true }

# крипто/кодеки/идентификаторы
ring = { workspace = true }
rand = { workspace = true }
ed25519-dalek = { workspace = true }
sha2 = { workspace = true }
blake3 = { workspace = true }
hex = { workspace = true }
base64 = { workspace = true }
bs58 = { workspace = true }
uuid = { workspace = true }
bincode = { workspace = true }

# хранилище/сеть/асинхрон
sled = { workspace = true }
reqwest = { workspace = true }
tokio = { workspace = true }

```


## lrb_core/src/types.rs
<a id="lrb_core-src-types-rs"></a>

```rust
use anyhow::{anyhow, Result};
use blake3::Hasher;
use ed25519_dalek::{Signature, VerifyingKey};
use serde::{Deserialize, Serialize};
use std::time::{SystemTime, UNIX_EPOCH};
use uuid::Uuid;

// base64 v0.22 Engine API
use base64::engine::general_purpose::STANDARD as B64;
use base64::Engine;

pub type Amount = u64;
pub type Height = u64;
pub type Nonce = u64;

#[derive(Clone, Debug, Serialize, Deserialize, Eq, PartialEq, Hash)]
pub struct Rid(pub String); // base58(VerifyingKey)

impl Rid {
    pub fn from_pubkey(pk: &VerifyingKey) -> Self {
        Rid(bs58::encode(pk.to_bytes()).into_string())
    }
    pub fn as_str(&self) -> &str {
        &self.0
    }
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Tx {
    pub id: String, // blake3 of canonical form
    pub from: Rid,  // base58(pubkey)
    pub to: Rid,
    pub amount: Amount,
    pub nonce: Nonce,
    pub public_key: Vec<u8>, // 32 bytes (VerifyingKey)
    pub signature: Vec<u8>,  // 64 bytes (Signature)
}

impl Tx {
    pub fn canonical_bytes(&self) -> Vec<u8> {
        // Без id и signature для детерминированного хеша
        let m = serde_json::json!({
            "from": self.from.as_str(),
            "to": self.to.as_str(),
            "amount": self.amount,
            "nonce": self.nonce,
            "public_key": B64.encode(&self.public_key),
        });
        serde_json::to_vec(&m).expect("canonical json")
    }
    pub fn compute_id(&self) -> String {
        let mut hasher = Hasher::new();
        hasher.update(&self.canonical_bytes());
        hex::encode(hasher.finalize().as_bytes())
    }
    pub fn validate_shape(&self) -> Result<()> {
        if self.public_key.len() != 32 {
            return Err(anyhow!("bad pubkey len"));
        }
        if self.signature.len() != 64 {
            return Err(anyhow!("bad signature len"));
        }
        if self.amount == 0 {
            return Err(anyhow!("amount must be > 0"));
        }
        Ok(())
    }
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Block {
    pub height: Height,
    pub prev_hash: String,
    pub timestamp_ms: u128,
    pub proposer: Rid,
    pub txs: Vec<Tx>,
    pub block_hash: String,
    pub uuid: String, // для логов
}

impl Block {
    pub fn new(height: Height, prev_hash: String, proposer: Rid, txs: Vec<Tx>) -> Self {
        let ts = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_millis();
        let mut h = Hasher::new();
        h.update(prev_hash.as_bytes());
        h.update(proposer.as_str().as_bytes());
        for tx in &txs {
            h.update(tx.id.as_bytes());
        }
        h.update(&ts.to_le_bytes());
        let block_hash = hex::encode(h.finalize().as_bytes());
        Block {
            height,
            prev_hash,
            timestamp_ms: ts,
            proposer,
            txs,
            block_hash,
            uuid: Uuid::new_v4().to_string(),
        }
    }
}

pub fn parse_pubkey(pk: &[u8]) -> Result<VerifyingKey> {
    let arr: [u8; 32] = pk.try_into().map_err(|_| anyhow!("bad pubkey len"))?;
    Ok(VerifyingKey::from_bytes(&arr)?)
}

pub fn parse_sig(sig: &[u8]) -> Result<Signature> {
    let arr: [u8; 64] = sig.try_into().map_err(|_| anyhow!("bad signature len"))?;
    Ok(Signature::from_bytes(&arr))
}

```


## lrb_core/src/crypto.rs
<a id="lrb_core-src-crypto-rs"></a>

```rust
//! Безопасные AEAD-примитивы с уникальным nonce per message.
//! Использование:
//!   let (ct, nonce) = seal_aes_gcm(&key32, aad, &plain)?;
//!   let pt = open_aes_gcm(&key32, aad, nonce, &ct)?;

use anyhow::{anyhow, Result};
use rand::rngs::OsRng;
use rand::RngCore;
use ring::aead::{self, Aad, LessSafeKey, Nonce, UnboundKey};

/// 96-битный nonce для AES-GCM (RFC 5116). Генерируется на каждое сообщение.
#[derive(Clone, Copy, Debug)]
pub struct Nonce96(pub [u8; 12]);

impl Nonce96 {
    #[inline]
    pub fn random() -> Self {
        let mut n = [0u8; 12];
        OsRng.fill_bytes(&mut n);
        Self(n)
    }
}

/// Шифрование AES-256-GCM: возвращает (ciphertext||tag, nonce)
pub fn seal_aes_gcm(key32: &[u8; 32], aad: &[u8], plaintext: &[u8]) -> Result<(Vec<u8>, [u8; 12])> {
    let unbound = UnboundKey::new(&aead::AES_256_GCM, key32)
        .map_err(|e| anyhow!("ring UnboundKey::new failed: {:?}", e))?;
    let key = LessSafeKey::new(unbound);
    let nonce = Nonce96::random();

    let mut inout = plaintext.to_vec();
    key.seal_in_place_append_tag(Nonce::assume_unique_for_key(nonce.0), Aad::from(aad), &mut inout)
        .map_err(|_| anyhow!("AEAD seal failed"))?;
    Ok((inout, nonce.0))
}

/// Расшифрование AES-256-GCM: принимает nonce и (ciphertext||tag)
pub fn open_aes_gcm(key32: &[u8; 32], aad: &[u8], nonce: [u8; 12], ciphertext_and_tag: &[u8]) -> Result<Vec<u8>> {
    let unbound = UnboundKey::new(&aead::AES_256_GCM, key32)
        .map_err(|e| anyhow!("ring UnboundKey::new failed: {:?}", e))?;
    let key = LessSafeKey::new(unbound);

    let mut buf = ciphertext_and_tag.to_vec();
    let plain = key
        .open_in_place(Nonce::assume_unique_for_key(nonce), Aad::from(aad), &mut buf)
        .map_err(|_| anyhow!("AEAD open failed"))?;
    Ok(plain.to_vec())
}

```


## lrb_core/src/anti_replay.rs
<a id="lrb_core-src-anti_replay-rs"></a>

```rust
use std::collections::HashMap;

/// Простейшее TTL-окно: tag -> last_seen_ms
#[derive(Clone, Debug)]
pub struct AntiReplayWindow {
    ttl_ms: u128,
    map: HashMap<String, u128>,
}

impl AntiReplayWindow {
    pub fn new(ttl_ms: u128) -> Self {
        Self {
            ttl_ms,
            map: HashMap::new(),
        }
    }

    /// true, если новый (вставлен), false — если повтор/просрочен
    pub fn check_and_insert(&mut self, tag: String, now_ms: u128) -> bool {
        // Чистка "по ходу"
        self.gc(now_ms);
        if let Some(&seen) = self.map.get(&tag) {
            if now_ms.saturating_sub(seen) <= self.ttl_ms {
                return false; // повтор
            }
        }
        self.map.insert(tag, now_ms);
        true
    }

    pub fn gc(&mut self, now_ms: u128) {
        let ttl = self.ttl_ms;
        self.map.retain(|_, &mut t| now_ms.saturating_sub(t) <= ttl);
    }
}

```


## lrb_core/src/ledger.rs
<a id="lrb_core-src-ledger-rs"></a>

```rust
//! Ledger — sled-backed storage (single DB open only in AppState).
//! НИКАКИХ sled::open внутри этого модуля.

use anyhow::{anyhow, Result};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use sled::{Db, IVec, Tree};

const META_HEIGHT: &[u8]         = b"height";
const META_SUPPLY_MINTED: &[u8]  = b"supply_minted";
const META_SUPPLY_BURNED: &[u8]  = b"supply_burned";
const META_LAST_HASH: &[u8]      = b"last_block_hash";

#[derive(Clone)]
pub struct Ledger {
    pub(crate) db: Db,
    t_meta:  Tree,
    t_bal:   Tree,
    t_nonce: Tree,
    t_tx:    Tree,
    t_txidx: Tree,
    t_acctx: Tree,
    t_bmeta: Tree,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StoredTx {
    pub txid:   String,
    pub height: u64,
    pub from:   String,
    pub to:     String,
    pub amount: u64,
    pub nonce:  u64,
    pub memo:   Option<String>,
    pub ts:     Option<u64>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TxRec {
    pub txid:   String,
    pub height: u64,
    pub from:   String,
    pub to:     String,
    pub amount: u64,
    pub nonce:  u64,
    pub ts:     Option<u64>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BlockMeta {
    pub height:     u64,
    pub block_hash: String,
}


// ===== time helpers =====
pub fn now_ms() -> u64 {
    use std::time::{SystemTime, UNIX_EPOCH};
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_millis() as u64
}

impl Ledger {
    /// Создать Ledger из уже ОТКРЫТОГО sled::Db (AppState отвечает за open).
    pub fn from_db(db: Db) -> Self {
        let t_meta  = db.open_tree("meta").expect("open meta");
        let t_bal   = db.open_tree("bal").expect("open bal");
        let t_nonce = db.open_tree("nonce").expect("open nonce");
        let t_tx    = db.open_tree("tx").expect("open tx");
        let t_txidx = db.open_tree("txidx").expect("open txidx");
        let t_acctx = db.open_tree("acctx").expect("open acctx");
        let t_bmeta = db.open_tree("bmeta").expect("open bmeta");

        // инициализируем дефолты
        if t_meta.get(META_HEIGHT).ok().flatten().is_none() {
            t_meta.insert(META_HEIGHT, be_u64(0).to_vec()).unwrap();
        }
        if t_meta.get(META_SUPPLY_MINTED).ok().flatten().is_none() {
            t_meta.insert(META_SUPPLY_MINTED, be_u128(0).to_vec()).unwrap();
        }
        if t_meta.get(META_SUPPLY_BURNED).ok().flatten().is_none() {
            t_meta.insert(META_SUPPLY_BURNED, be_u128(0).to_vec()).unwrap();
        }
        if t_meta.get(META_LAST_HASH).ok().flatten().is_none() {
            t_meta.insert(META_LAST_HASH, b"".to_vec()).unwrap();
        }

        Self { db, t_meta, t_bal, t_nonce, t_tx, t_txidx, t_acctx, t_bmeta }
    }

    // ===== helpers for BE conversions =====
    #[inline]
    fn from_be_u64(iv: &IVec) -> u64 {
        let mut b = [0u8; 8];
        b.copy_from_slice(iv.as_ref());
        u64::from_be_bytes(b)
    }
    #[inline]
    fn from_be_u128(iv: &IVec) -> u128 {
        let mut b = [0u8; 16];
        b.copy_from_slice(iv.as_ref());
        u128::from_be_bytes(b)
    }

    // ===== meta/head =====
    pub fn height(&self) -> Result<u64> {
        Ok(self
            .t_meta
            .get(META_HEIGHT)?
            .map(|v| Self::from_be_u64(&v))
            .unwrap_or(0))
    }
    pub fn set_height(&self, h: u64) -> Result<()> {
        self.t_meta.insert(META_HEIGHT, be_u64(h).to_vec())?;
        Ok(())
    }
    pub fn last_block_hash(&self) -> Result<String> {
        Ok(self
            .t_meta
            .get(META_LAST_HASH)?
            .map(|v| String::from_utf8_lossy(&v).into())
            .unwrap_or_default())
    }
    pub fn set_last_block_hash(&self, s: &str) -> Result<()> {
        self.t_meta
            .insert(META_LAST_HASH, s.as_bytes().to_vec())?;
        Ok(())
    }
    pub fn head(&self) -> Result<(u64, String)> {
        Ok((self.height()?, self.last_block_hash()?))
    }

    
    pub fn head_height(&self) -> Result<u64> {
        self.height()
    }

    pub fn set_head(&self, h: u64, hash: &str) -> Result<()> {
        self.set_height(h)?;
        self.set_last_block_hash(hash)?;
        Ok(())
    }

// ===== supply =====
    pub fn supply(&self) -> Result<(u64, u64)> {
        let m = self
            .t_meta
            .get(META_SUPPLY_MINTED)?
            .map(|v| Self::from_be_u128(&v))
            .unwrap_or(0);
        let b = self
            .t_meta
            .get(META_SUPPLY_BURNED)?
            .map(|v| Self::from_be_u128(&v))
            .unwrap_or(0);
        let minted = u64::try_from(m).unwrap_or(u64::MAX);
        let burned = u64::try_from(b).unwrap_or(u64::MAX);
        Ok((minted, burned))
    }
    pub fn add_minted(&self, v: u64) -> Result<()> {
        let cur = self
            .t_meta
            .get(META_SUPPLY_MINTED)?
            .map(|iv| Self::from_be_u128(&iv))
            .unwrap_or(0);
        self.t_meta.insert(
            META_SUPPLY_MINTED,
            be_u128(cur.saturating_add(v as u128)).to_vec(),
        )?;
        Ok(())
    }
    pub fn add_burned(&self, v: u64) -> Result<()> {
        let cur = self
            .t_meta
            .get(META_SUPPLY_BURNED)?
            .map(|iv| Self::from_be_u128(&iv))
            .unwrap_or(0);
        self.t_meta.insert(
            META_SUPPLY_BURNED,
            be_u128(cur.saturating_add(v as u128)).to_vec(),
        )?;
        Ok(())
    }

    // ===== balances / nonce =====
    pub fn get_balance(&self, rid: &str) -> Result<u128> {
        Ok(self
            .t_bal
            .get(rid.as_bytes())?
            .map(|v| Self::from_be_u128(&v))
            .unwrap_or(0))
    }
    pub fn set_balance(&self, rid: &str, value: u128) -> Result<()> {
        self.t_bal
            .insert(rid.as_bytes(), be_u128(value).to_vec())?;
        Ok(())
    }
    pub fn get_nonce(&self, rid: &str) -> Result<u64> {
        Ok(self
            .t_nonce
            .get(rid.as_bytes())?
            .map(|v| Self::from_be_u64(&v))
            .unwrap_or(0))
    }
    pub fn bump_nonce(&self, rid: &str) -> Result<u64> {
        let n = self.get_nonce(rid)?.saturating_add(1);
        self.t_nonce
            .insert(rid.as_bytes(), be_u64(n).to_vec())?;
        Ok(n)
    }
    pub fn set_nonce(&self, rid: &str, value: u64) -> Result<()> {
        self.t_nonce
            .insert(rid.as_bytes(), be_u64(value).to_vec())?;
        Ok(())
    }

    // ===== tx fetch/index =====
    pub fn get_tx(&self, txid: &str) -> Result<Option<StoredTx>> {
        Ok(self
            .t_tx
            .get(txid.as_bytes())?
            .map(|v| serde_json::from_slice(&v))
            .transpose()?)
    }
    pub fn get_tx_height(&self, txid: &str) -> Result<Option<u64>> {
        Ok(self
            .t_txidx
            .get(txid.as_bytes())?
            .map(|v| Self::from_be_u64(&v)))
    }

    /// История аккаунта постранично. Делает scan_prefix по `rid|`.
    pub fn account_txs_page(
        &self,
        rid: &str,
        page: u32,
        per_page: u32,
    ) -> Result<Vec<TxRec>> {
        let per = per_page.clamp(1, 1000) as usize;
        let mut keys: Vec<IVec> = Vec::new();
        for item in self.t_acctx.scan_prefix(rid.as_bytes()) {
            let (k, _) = item?;
            keys.push(k);
        }
        keys.sort_unstable(); // <rid>|<BE height>|<txid>
        let start = (page as usize).saturating_mul(per);
        let end = (start + per).min(keys.len());

        let mut out = Vec::with_capacity(end.saturating_sub(start));
        for k in keys.get(start..end).unwrap_or(&[]) {
            if let Some(pos) = k.as_ref().iter().rposition(|&b| b == b'|') {
                let txid =
                    std::str::from_utf8(&k.as_ref()[pos + 1..]).unwrap_or_default();
                if let Some(stx) = self.get_tx(txid)? {
                    out.push(TxRec {
                        txid: stx.txid.clone(),
                        height: stx.height,
                        from: stx.from,
                        to: stx.to,
                        amount: stx.amount,
                        nonce: stx.nonce,
                        ts: stx.ts,
                    });
                }
            }
        }
        Ok(out)
    }

    /// Простой submit (DEMO): проверка баланса/nonce, применение, индексация.
    pub fn submit_tx_simple(
        &self,
        from: &str,
        to: &str,
        amount: u64,
        nonce: u64,
        memo: Option<&str>,
    ) -> Result<StoredTx> {
        let fb = self.get_balance(from)?;
        if fb < amount as u128 {
            return Err(anyhow!("insufficient_funds"));
        }
        let n = self.get_nonce(from)?;
        if n + 1 != nonce {
            return Err(anyhow!("bad_nonce"));
        }

        self.set_balance(from, fb - amount as u128)?;
        self.set_balance(
            to,
            self.get_balance(to)?.saturating_add(amount as u128),
        )?;
        self.set_nonce(from, nonce)?;

        let h = self.height()?.saturating_add(1);
        self.set_height(h)?;

        // txid = sha256(from|to|amount|nonce|ts)
        let ts = Some(unix_ts());
        let mut hasher = Sha256::new();
        hasher.update(from.as_bytes());
        hasher.update(b"|");
        hasher.update(to.as_bytes());
        hasher.update(b"|");
        hasher.update(&amount.to_be_bytes());
        hasher.update(b"|");
        hasher.update(&nonce.to_be_bytes());
        if let Some(t) = ts {
            hasher.update(&t.to_be_bytes());
        }
        let txid = hex::encode(hasher.finalize());

        let stx = StoredTx {
            txid: txid.clone(),
            height: h,
            from: from.to_string(),
            to: to.to_string(),
            amount,
            nonce,
            memo: memo.map(|s| s.to_string()),
            ts,
        };

        self.t_tx
            .insert(txid.as_bytes(), serde_json::to_vec(&stx)?)?;
        self.t_txidx
            .insert(txid.as_bytes(), be_u64(h).to_vec())?;

        // индекс по аккаунтам: <rid>|<BE height>|<txid>
        let mut kf =
            Vec::with_capacity(from.len() + 1 + 8 + 1 + txid.len());
        kf.extend_from_slice(from.as_bytes());
        kf.push(b'|');
        kf.extend_from_slice(&be_u64(h));
        kf.push(b'|');
        kf.extend_from_slice(txid.as_bytes());
        self.t_acctx.insert(kf, &[])?;

        let mut kt =
            Vec::with_capacity(to.len() + 1 + 8 + 1 + txid.len());
        kt.extend_from_slice(to.as_bytes());
        kt.push(b'|');
        kt.extend_from_slice(&be_u64(h));
        kt.push(b'|');
        kt.extend_from_slice(txid.as_bytes());
        self.t_acctx.insert(kt, &[])?;

        // минимальный BlockMeta (если нужно — обогащаем)
        let meta = BlockMeta {
            height: h,
            block_hash: self.last_block_hash().unwrap_or_default(),
        };
        self.t_bmeta
            .insert(be_u64(h).to_vec(), bincode::serialize(&meta).unwrap())?;

        Ok(stx)
    }

    pub fn get_block_by_height(&self, h: u64) -> Result<BlockMeta> {
        if let Some(v) = self.t_bmeta.get(be_u64(h))? {
            Ok(bincode::deserialize(&v)?)
        } else {
            Err(anyhow!("block_meta_not_found"))
        }
    }

    pub fn set_finalized(&self, _h: u64) -> Result<()> {
        Ok(())
    }

    // ====== заглушки для rcp_engine (совместимость API), делаем no-op ======
    pub fn commit_block_atomic<T>(&self, _b: &T) -> Result<()> {
        Ok(())
    }
    pub fn index_block<T, S>(
        &self,
        _h: u64,
        _block_hash: &str,
        _ts: S,
        _txs: &T,
    ) -> Result<()> {
        Ok(())
    }
}

// ===== little helpers =====
#[inline]
fn be_u64(v: u64) -> [u8; 8] {
    v.to_be_bytes()
}
#[inline]
fn be_u128(v: u128) -> [u8; 16] {
    v.to_be_bytes()
}

#[inline]
fn unix_ts() -> u64 {
    use std::time::{SystemTime, UNIX_EPOCH};
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs()
}

```


## lrb_core/src/spam_guard.rs
<a id="lrb_core-src-spam_guard-rs"></a>

```rust
use anyhow::{anyhow, Result};

#[derive(Clone, Debug)]
pub struct SpamGuard {
    max_mempool: usize,
    max_tx_per_block: usize,
    max_amount: u64,
}

impl SpamGuard {
    pub fn new(max_mempool: usize, max_tx_per_block: usize, max_amount: u64) -> Self {
        Self {
            max_mempool,
            max_tx_per_block,
            max_amount,
        }
    }
    pub fn check_mempool(&self, cur_len: usize) -> Result<()> {
        if cur_len > self.max_mempool {
            return Err(anyhow!("mempool overflow"));
        }
        Ok(())
    }
    pub fn check_amount(&self, amount: u64) -> Result<()> {
        if amount == 0 || amount > self.max_amount {
            return Err(anyhow!("amount out of bounds"));
        }
        Ok(())
    }
    pub fn max_block_txs(&self) -> usize {
        self.max_tx_per_block
    }
}

```


## lrb_core/src/sigpool.rs
<a id="lrb_core-src-sigpool-rs"></a>

```rust
use crate::phase_integrity::verify_tx_signature;
use crate::types::Tx;
use tokio::task::JoinSet;

/// Параллельная фильтрация валидных по подписи транзакций.
/// workers: количество тасков; по умолчанию 4–8 (задать через ENV в движке).
pub async fn filter_valid_sigs_parallel(txs: Vec<Tx>, workers: usize) -> Vec<Tx> {
    if txs.is_empty() {
        return txs;
    }
    let w = workers.max(1);
    let chunk = (txs.len() + w - 1) / w;
    let mut set = JoinSet::new();
    for part in txs.chunks(chunk) {
        let vec = part.to_vec();
        set.spawn(async move {
            let mut ok = Vec::with_capacity(vec.len());
            for t in vec {
                if verify_tx_signature(&t).is_ok() {
                    ok.push(t);
                }
            }
            ok
        });
    }
    let mut out = Vec::new();
    while let Some(res) = set.join_next().await {
        if let Ok(mut v) = res {
            out.append(&mut v);
        }
    }
    out
}

```


## lrb_core/src/rcp_engine.rs
<a id="lrb_core-src-rcp_engine-rs"></a>

```rust
use crate::sigpool::filter_valid_sigs_parallel;
use crate::{dynamic_balance::DynamicBalance, ledger::Ledger, spam_guard::SpamGuard, types::*};
use crate::{phase_consensus::PhaseConsensus, phase_filters::block_passes_phase};
use anyhow::Result;
use std::{
    sync::{Arc, Mutex},
    time::{Duration, SystemTime, UNIX_EPOCH},
};
use tokio::sync::{
    broadcast,
    mpsc::{unbounded_channel, UnboundedSender},
};

// точный монотонный ts для индексации
fn now_ms() -> u128 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_millis()
}

fn env_u64(key: &str, def: u64) -> u64 {
    std::env::var(key)
        .ok()
        .and_then(|s| s.parse::<u64>().ok())
        .unwrap_or(def)
}
fn env_usize(key: &str, def: usize) -> usize {
    std::env::var(key)
        .ok()
        .and_then(|s| s.parse::<usize>().ok())
        .unwrap_or(def)
}

#[derive(Clone)]
pub struct Engine {
    ledger: Arc<Ledger>,
    guard: SpamGuard,
    dyn_cost: DynamicBalance,
    proposer: Rid,
    mempool_tx: UnboundedSender<Tx>,
    mempool: Arc<Mutex<Vec<Tx>>>,
    commit_tx: Arc<Mutex<Option<broadcast::Sender<Block>>>>,

    slot_ms: u64,
    sig_workers: usize,
    consensus: Arc<Mutex<PhaseConsensus>>,
}

impl Engine {
    pub fn new(ledger: Ledger, proposer: Rid) -> Arc<Self> {
        let mempool_cap = env_u64("LRB_MEMPOOL_CAP", 100_000);
        let max_block_tx = env_u64("LRB_MAX_BLOCK_TX", 10_000);
        let max_amount = env_u64("LRB_MAX_AMOUNT", u64::MAX / 2);
        let slot_ms = env_u64("LRB_SLOT_MS", 500);
        let quorum_n = env_usize("LRB_QUORUM_N", 1);
        let sig_workers = env_usize("LRB_SIG_WORKERS", 4);

        let mempool: Arc<Mutex<Vec<Tx>>> = Arc::new(Mutex::new(Vec::new()));
        let (tx, rx) = unbounded_channel::<Tx>();

        let engine = Arc::new(Self {
            ledger: Arc::new(ledger),
            guard: SpamGuard::new(mempool_cap as usize, max_block_tx as usize, max_amount),
            dyn_cost: DynamicBalance::new(100, 2),
            proposer,
            mempool_tx: tx.clone(),
            mempool: mempool.clone(),
            commit_tx: Arc::new(Mutex::new(None)),
            slot_ms,
            sig_workers,
            consensus: Arc::new(Mutex::new(PhaseConsensus::new(quorum_n))),
        });

        // приём транзакций в mempool с лимитами
        let guard = engine.guard.clone();
        tokio::spawn(async move {
            let mut rx = rx;
            while let Some(tx) = rx.recv().await {
                let mut lock = mempool.lock().unwrap();
                if guard.check_mempool(lock.len()).is_ok() {
                    lock.push(tx);
                }
            }
        });

        engine
    }

    pub fn ledger(&self) -> Arc<Ledger> {
        self.ledger.clone()
    }
    pub fn proposer(&self) -> Rid {
        self.proposer.clone()
    }
    pub fn set_commit_notifier(&self, sender: broadcast::Sender<Block>) {
        *self.commit_tx.lock().unwrap() = Some(sender);
    }
    pub fn check_amount_valid(&self, amount: u64) -> Result<()> {
        self.guard.check_amount(amount)
    }
    pub fn mempool_sender(&self) -> UnboundedSender<Tx> {
        self.mempool_tx.clone()
    }
    pub fn mempool_len(&self) -> usize {
        self.mempool.lock().unwrap().len()
    }
    pub fn finalized_height(&self) -> u64 {
        self.consensus.lock().unwrap().finalized()
    }

    pub fn register_vote(&self, height: u64, block_hash: &str, rid_b58: &str) -> bool {
        let mut cons = self.consensus.lock().unwrap();
        if let Some((h, voted_hash)) = cons.vote(height, block_hash, rid_b58) {
            if let Ok(local) = self.ledger.get_block_by_height(h) {
                if local.block_hash == voted_hash {
                    let _ = self.ledger.set_finalized(h);
                    return true;
                }
            }
        }
        false
    }

    pub async fn run_block_producer(self: Arc<Self>) -> Result<()> {
        let mut interval = tokio::time::interval(Duration::from_millis(self.slot_ms));

        loop {
            interval.tick().await;

            // 1) забираем пачку из мемпула
            let raw = {
                let mut mp = self.mempool.lock().unwrap();
                if mp.is_empty() {
                    continue;
                }
                let take = self.guard.max_block_txs().min(mp.len());
                mp.drain(0..take).collect::<Vec<Tx>>()
            };

            // 2) проверка подписей параллельно
            let mut valid = filter_valid_sigs_parallel(raw, self.sig_workers).await;
            if valid.is_empty() {
                continue;
            }

            // 3) базовые лимиты/amount
            valid.retain(|t| self.guard.check_amount(t.amount).is_ok());
            if valid.is_empty() {
                continue;
            }

            // 4) формируем блок (h+1)
            let (h, prev_hash) = self.ledger.head().unwrap_or((0, String::new()));
            let b = Block::new(h + 1, prev_hash, self.proposer.clone(), valid);

            // 5) фазовый фильтр (резонанс). Если не прошёл — НЕ теряем tx: возвращаем в хвост mempool.
            if !block_passes_phase(&b) {
                let mut mp = self.mempool.lock().unwrap();
                mp.extend(b.txs.into_iter()); // вернуть в очередь, обработаем в следующем слоте
                continue;
            }

            // 6) атомарный коммит блока
            if let Err(e) = self.ledger.commit_block_atomic(&b) {
                // при ошибке — вернуть tx в mempool и идти дальше
                let mut mp = self.mempool.lock().unwrap();
                mp.extend(b.txs.into_iter());
                eprintln!("commit_block_atomic error at height {}: {:?}", b.height, e);
                continue;
            }

            // 7) индексирование блока для истории/эксплорера (не мешает продюсеру)
            let ts = now_ms();
            if let Err(e) = self.ledger.index_block(b.height, &b.block_hash, ts, &b.txs) {
                // индексация не должна ломать производство блоков
                eprintln!("index_block error at height {}: {:?}", b.height, e);
            }

            // 8) локальный голос и уведомление подписчикам
            let _ = self.register_vote(b.height, &b.block_hash, self.proposer.as_str());
            if let Some(tx) = self.commit_tx.lock().unwrap().as_ref() {
                let _ = tx.send(b.clone());
            }
        }
    }

    pub fn lgn_cost_microunits(&self) -> u64 {
        self.dyn_cost.lgn_cost(self.mempool_len() as usize)
    }
}

pub fn engine_with_channels(ledger: Ledger, proposer: Rid) -> (Arc<Engine>, UnboundedSender<Tx>) {
    let engine = Engine::new(ledger, proposer);
    let sender = engine.mempool_sender();
    (engine, sender)
}

```


## lrb_core/src/quorum.rs
<a id="lrb_core-src-quorum-rs"></a>

```rust
use anyhow::Result;
use base64::engine::general_purpose::STANDARD as B64;
use base64::Engine;
use ed25519_dalek::{Signature, Verifier, VerifyingKey};
use serde::{Deserialize, Serialize};

/// Голос за блок (по Σ-дайджесту)
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Vote {
    pub height: u64,
    pub block_hash: String,
    pub sigma_hex: String,
    pub voter_pk_b58: String,
    pub sig_b64: String,
    pub nonce_ms: u128,
}

pub fn verify_vote(v: &Vote) -> Result<()> {
    let pk_bytes = bs58::decode(&v.voter_pk_b58).into_vec()?;
    let vk =
        VerifyingKey::from_bytes(&pk_bytes.try_into().map_err(|_| anyhow::anyhow!("bad pk"))?)?;
    let sig_bytes = B64.decode(v.sig_b64.as_bytes())?;
    let sig = Signature::from_bytes(
        &sig_bytes
            .try_into()
            .map_err(|_| anyhow::anyhow!("bad sig"))?,
    );

    let mut payload = Vec::new();
    payload.extend_from_slice(v.sigma_hex.as_bytes());
    payload.extend_from_slice(v.block_hash.as_bytes());
    payload.extend_from_slice(&v.height.to_le_bytes());
    payload.extend_from_slice(&v.nonce_ms.to_le_bytes());

    vk.verify(&payload, &sig)
        .map_err(|e| anyhow::anyhow!("verify failed: {e}"))?;
    Ok(())
}

```


## lrb_core/src/phase_consensus.rs
<a id="lrb_core-src-phase_consensus-rs"></a>

```rust
use std::collections::{HashMap, HashSet};

/// Фазовый консенсус Σ(t) с учётом блока (height, block_hash).
/// Накапливает голоса RID'ов по конкретному хешу блока.
/// Финализованный height повышается, когда кворум собран по **одному** хешу на этом height.
pub struct PhaseConsensus {
    /// votes[height][block_hash] = {rid_b58, ...}
    votes: HashMap<u64, HashMap<String, HashSet<String>>>,
    finalized_h: u64,
    quorum_n: usize,
}

impl PhaseConsensus {
    pub fn new(quorum_n: usize) -> Self {
        Self {
            votes: HashMap::new(),
            finalized_h: 0,
            quorum_n,
        }
    }

    pub fn quorum_n(&self) -> usize {
        self.quorum_n
    }
    pub fn finalized(&self) -> u64 {
        self.finalized_h
    }

    /// Регистрируем голос. Возвращает Some((h,hash)) если по hash достигнут кворум.
    pub fn vote(&mut self, h: u64, block_hash: &str, rid_b58: &str) -> Option<(u64, String)> {
        let by_hash = self.votes.entry(h).or_default();
        let set = by_hash.entry(block_hash.to_string()).or_default();
        set.insert(rid_b58.to_string());
        if set.len() >= self.quorum_n {
            if h > self.finalized_h {
                self.finalized_h = h;
            }
            return Some((h, block_hash.to_string()));
        }
        None
    }

    /// Сколько голосов у конкретного (h,hash)
    #[allow(dead_code)]
    pub fn votes_for(&self, h: u64, block_hash: &str) -> usize {
        self.votes
            .get(&h)
            .and_then(|m| m.get(block_hash))
            .map(|s| s.len())
            .unwrap_or(0)
    }
}

```


## lrb_core/src/phase_integrity.rs
<a id="lrb_core-src-phase_integrity-rs"></a>

```rust
use crate::types::*;
use anyhow::{anyhow, Result};
use ed25519_dalek::Verifier as _; // для pk.verify(&msg, &sig)

pub fn verify_tx_signature(tx: &Tx) -> Result<()> {
    tx.validate_shape()?;

    let pk = crate::types::parse_pubkey(&tx.public_key)?;
    let sig = crate::types::parse_sig(&tx.signature)?;
    let msg = tx.canonical_bytes();

    pk.verify(&msg, &sig)
        .map_err(|e| anyhow!("bad signature: {e}"))?;

    // сверяем id
    if tx.id != tx.compute_id() {
        return Err(anyhow!("tx id mismatch"));
    }
    Ok(())
}

```


## node/Cargo.toml
<a id="node-Cargo-toml"></a>

```toml
[package]
name        = "logos_node"
version     = "0.1.0"
edition     = "2021"
license     = "Apache-2.0"
description = "LOGOS LRB node: Axum REST + archive + producer + wallet/stake"
build       = "build.rs"

# Основной бинарь узла
[[bin]]
name = "logos_node"
path = "src/main.rs"

[lib]
name = "logos_node"
path = "src/lib.rs"

[dependencies]
# базовый стек (всё из workspace)
axum.workspace                = true
tower.workspace               = true
tower-http.workspace          = true
tokio.workspace               = true

serde.workspace               = true
serde_json.workspace          = true
anyhow.workspace              = true
thiserror.workspace           = true
once_cell.workspace           = true
dashmap.workspace             = true
tracing.workspace             = true
tracing-subscriber.workspace  = true
sha2.workspace                = true   # canonical_msg в API

# хранилища/индексация
sled.workspace                = true
deadpool-postgres.workspace   = true
tokio-postgres.workspace      = true
rusqlite.workspace            = true
r2d2_sqlite.workspace         = true

# утилиты/крипта/метрики
hex.workspace                 = true
base64.workspace              = true
bs58.workspace                = true
ed25519-dalek.workspace       = true
blake3.workspace              = true
ipnet.workspace               = true
prometheus.workspace          = true
uuid.workspace                = true

# security & utils
hmac = { version = "0.12", default-features = false }
rand = { version = "0.8", features = ["std","std_rng"] }
parking_lot = "0.12"

# HTTP‑клиент (bridge payout + утилиты)
reqwest   = { workspace = true, features = ["rustls-tls","http2","json","blocking"] }
rand_core = "0.6"

# ядро
lrb_core = { path = "../lrb_core" }

[build-dependencies]
chrono = { version = "0.4", default-features = false, features = ["clock"] }

```


## node/build.rs
<a id="node-build-rs"></a>

```rust
use std::{env, fs, path::PathBuf, process::Command};

fn main() {
    // Короткий git hash
    let git_hash = Command::new("git")
        .args(["rev-parse", "--short=12", "HEAD"])
        .output()
        .ok()
        .and_then(|o| if o.status.success() {
            Some(String::from_utf8_lossy(&o.stdout).trim().to_string())
        } else { None })
        .unwrap_or_else(|| "unknown".into());

    // Текущая ветка
    let git_branch = Command::new("git")
        .args(["rev-parse", "--abbrev-ref", "HEAD"])
        .output()
        .ok()
        .and_then(|o| if o.status.success() {
            Some(String::from_utf8_lossy(&o.stdout).trim().to_string())
        } else { None })
        .unwrap_or_else(|| "unknown".into());

    // Время сборки (UTC, RFC3339)
    let ts = chrono::Utc::now().to_rfc3339();

    // Версия из Cargo.toml
    let pkg_ver = env::var("CARGO_PKG_VERSION").unwrap_or_else(|_| "0.0.0".into());

    // Пишем build_info.rs в OUT_DIR
    let out_dir = PathBuf::from(env::var("OUT_DIR").expect("OUT_DIR not set"));
    let dest = out_dir.join("build_info.rs");
    let contents = format!(
        "pub const BUILD_GIT_HASH: &str = \"{git_hash}\";\n\
         pub const BUILD_GIT_BRANCH: &str = \"{git_branch}\";\n\
         pub const BUILD_TIMESTAMP_RFC3339: &str = \"{ts}\";\n\
         pub const BUILD_PKG_VERSION: &str = \"{pkg_ver}\";\n"
    );
    fs::write(&dest, contents).expect("write build_info.rs failed");

    // Ретриггер
    println!("cargo:rerun-if-changed=build.rs");
    println!("cargo:rerun-if-changed=../Cargo.toml");
    println!("cargo:rerun-if-changed=.git/HEAD");
}

```


## node/src/lib.rs
<a id="node-src-lib-rs"></a>

```rust
pub mod api;
pub mod admin;
pub mod archive;
pub mod auth;
pub mod bridge;
pub mod bridge_journal;
pub mod gossip;
pub mod guard;
pub mod health;
pub mod metrics;
pub mod openapi;
pub mod payout_adapter;
pub mod peers;
pub mod producer;
pub mod state;
pub mod stake;
pub mod stake_claim;
pub mod storage;
pub mod version;
pub mod wallet;

```


## node/src/main.rs
<a id="node-src-main-rs"></a>

```rust
use axum::{routing::{get, post}, Router};
use tower::ServiceBuilder;
use tower_http::trace::TraceLayer;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt, EnvFilter};
use std::sync::Arc;
use tracing::{info, warn};

mod api;
mod bridge;
mod bridge_journal;
mod payout_adapter;   // адаптер выплат (используется в bridge)
mod admin;
mod gossip;
mod state;
mod peers;
mod guard;
mod metrics;
mod version;
mod storage;
mod archive;
mod openapi;
mod auth;
mod stake;
mod stake_claim;      // реальный claim_settle (зачисление в ledger)
mod health;           // /livez + /readyz
mod wallet;
mod producer;

fn router(app_state: Arc<state::AppState>) -> Router {
    Router::new()
        // --- public ---
        .route("/healthz", get(api::healthz))
        .route("/livez",  get(health::livez))       // liveness
        .route("/readyz", get(health::readyz))      // readiness
        .route("/head",    get(api::head))
        .route("/balance/:rid", get(api::balance))
        .route("/submit_tx",       post(api::submit_tx))
        .route("/debug_canon",  post(api::submit_tx))
        .route("/submit_tx_batch", post(api::submit_tx_batch))
        .route("/economy",         get(api::economy))
        .route("/history/:rid",    get(api::history))

        // --- archive API (PG) ---
        .route("/archive/blocks",       get(api::archive_blocks))
        .route("/archive/txs",          get(api::archive_txs))
        .route("/archive/history/:rid", get(api::archive_history))
        .route("/archive/tx/:txid",     get(api::archive_tx))

        // --- staking wrappers (совместимость с фронтом) ---
        .route("/stake/delegate",   post(api::stake_delegate))
        .route("/stake/undelegate", post(api::stake_undelegate))
        .route("/stake/claim",      post(api::stake_claim))
        .route("/stake/my/:rid",    get(api::stake_my))
        // реальный settle награды в ledger
        .route("/stake/claim_settle", post(stake_claim::claim_settle))

        // --- bridge (durable + payout, Send-safe) ---
        // JSON endpoints для mTLS+HMAC периметра (Nginx rewrites → сюда)
        .route("/bridge/deposit_json", post(bridge::deposit_json))
        .route("/bridge/redeem_json",  post(bridge::redeem_json))
        // Оставляем и «обычные» (внутренние) эндпоинты через безопасные замыкания
        .route(
            "/bridge/deposit",
            post(|st: axum::extract::State<Arc<state::AppState>>,
                  body: axum::Json<bridge::DepositReq>| async move {
                bridge::deposit(st, body).await
            })
        )
        .route(
            "/bridge/redeem",
            post(|st: axum::extract::State<Arc<state::AppState>>,
                  body: axum::Json<bridge::RedeemReq>| async move {
                bridge::redeem(st, body).await
            })
        )
        .route("/health/bridge",  get(bridge::health))

        // --- version / metrics / openapi ---
        .route("/version",      get(version::get))
        .route("/metrics",      get(metrics::prometheus))
        .route("/openapi.json", get(openapi::serve))

        // --- admin ---
        .route("/admin/set_balance", post(admin::set_balance))
        .route("/admin/bump_nonce",  post(admin::bump_nonce))
        .route("/admin/set_nonce",   post(admin::set_nonce))
        .route("/admin/mint",        post(admin::mint))
        .route("/admin/burn",        post(admin::burn))

        // --- legacy (если используются) ---
        .merge(wallet::routes())
        .merge(stake::routes())

        // --- layers/state ---
        .with_state(app_state)
        .layer(
            ServiceBuilder::new()
                .layer(TraceLayer::new_for_http())
                .layer(axum::middleware::from_fn(guard::rate_limit_mw))
                .layer(axum::middleware::from_fn(metrics::track))
        )
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // logging
    tracing_subscriber::registry()
        .with(
            EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| EnvFilter::new("info,hyper=warn"))
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    // secrets/keys (JWT, bridge key и т.п.)
    auth::assert_secrets_on_start().expect("secrets missing");

    // state
    let app_state = Arc::new(state::AppState::new()?);

    // optional archive из ENV
    if let Some(ar) = crate::archive::Archive::new_from_env().await {
        unsafe {
            let p = Arc::as_ptr(&app_state) as *mut state::AppState;
            (*p).archive = Some(ar);
        }
        info!("archive backend initialized");
    } else {
        warn!("archive disabled");
    }

    // producer (в нашей сборке локальный продюсер выключен и работает как follower)
    info!("producer start");
    let _producer = producer::run(app_state.clone());

    // воркер повторных выплат моста
    tokio::spawn(bridge::retry_worker(app_state.clone()));

    // bind & serve
    let addr = state::bind_addr()?;
    let listener = tokio::net::TcpListener::bind(addr).await?;
    info!("logos_node listening on {addr}");
    axum::serve(listener, router(app_state)).await?;
    Ok(())
}

```


## node/src/state.rs
<a id="node-src-state-rs"></a>

```rust
use std::env;
use std::net::SocketAddr;
use std::sync::Arc;

use anyhow::Result;
use parking_lot::Mutex;
use sled::Db;

use lrb_core::ledger::Ledger;

use crate::archive::Archive;

/// Глобальное состояние ноды.
///
/// db        — открытая sled-база;
/// ledger    — обёртка над db с балансами/tx;
/// archive   — опциональный Postgres-архив.
pub struct AppState {
    pub sled_db: Db,
    pub ledger: Arc<Mutex<Ledger>>,
    pub archive: Option<Archive>,
}

impl AppState {
    /// Открытие sled + Ledger.
    ///
    /// Путь берём из LRB_DATA_PATH или по умолчанию
    /// `/var/lib/logos/data.sled`.
    pub fn new() -> Result<Self> {
        let path = env::var("LRB_DATA_PATH")
            .unwrap_or_else(|_| "/var/lib/logos/data.sled".to_string());

        let db = sled::open(&path)?;
        let ledger = Ledger::from_db(db.clone());

        Ok(AppState {
            sled_db: db,
            ledger: Arc::new(Mutex::new(ledger)),
            archive: None,
        })
    }

    /// Доступ к sled для health/bridge_journal.
    pub fn sled(&self) -> &Db {
        &self.sled_db
    }
}

/// Адрес бинда HTTP-сервера.
/// LRB_BIND="0.0.0.0:8080" или дефолт 0.0.0.0:8080.
pub fn bind_addr() -> Result<SocketAddr> {
    let bind = env::var("LRB_BIND").unwrap_or_else(|_| "0.0.0.0:8080".to_string());
    Ok(bind.parse()?)
}

```


## node/src/storage.rs
<a id="node-src-storage-rs"></a>

```rust
use serde::{Deserialize, Serialize};

/// Вход транзакции — соответствуем полям, которые ожидает api.rs
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TxIn {
    pub from: String,      // RID отправителя
    pub to: String,        // RID получателя
    pub amount: u64,       // количество
    pub nonce: u64,        // обязательный
    pub memo: Option<String>,
    pub sig_hex: String,   // подпись в hex
}

/// Элемент истории для /history/:rid
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HistoryItem {
    pub txid: String,
    pub height: u64,
    pub from: String,
    pub to: String,
    pub amount: u64,
    pub nonce: u64,
    pub ts: Option<u64>,
}

/// Состояние аккаунта (минимум, который использует api.rs)
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct AccountState {
    pub balance: u64,
    pub nonce: u64,
}

```


## node/src/fork.rs
<a id="node-src-fork-rs"></a>

```rust
#![allow(dead_code)]
//! Fork-choice: минимальный детерминированный выбор на базе высоты/хэша.
//! Совместим с текущими типами ядра (Block из lrb_core::types).

use lrb_core::types::Block;

/// Выбор лучшей ветви из набора кандидатов.
/// Правила:
/// 1) Бóльшая высота предпочтительнее.
/// 2) При равной высоте — лексикографически наименьший block_hash.
pub fn choose_best<'a>(candidates: &'a [Block]) -> Option<&'a Block> {
    candidates
        .iter()
        .max_by(|a, b| match a.height.cmp(&b.height) {
            core::cmp::Ordering::Equal => a.block_hash.cmp(&b.block_hash).reverse(),
            ord => ord,
        })
}

#[cfg(test)]
mod tests {
    use super::*;
    fn mk(h: u64, hash: &str) -> Block {
        Block {
            height: h,
            block_hash: hash.to_string(),
            ..Default::default()
        }
    }

    #[test]
    fn pick_by_height_then_hash() {
        let a = mk(10, "ff");
        let b = mk(12, "aa");
        let c = mk(12, "bb");
        let out = choose_best(&[a, b.clone(), c]).unwrap();
        assert_eq!(out.height, 12);
        assert_eq!(out.block_hash, "aa");
    }
}

```


## node/src/gossip.rs
<a id="node-src-gossip-rs"></a>

```rust
#![allow(dead_code)]
//! Gossip-утилиты: сериализация/десериализация блоков для пересылки по сети.

use base64::{engine::general_purpose::STANDARD as B64, Engine as _};
use blake3;
use hex;
use lrb_core::{phase_filters::block_passes_phase, types::Block};
use serde::{Deserialize, Serialize};

/// Конверт для публикации блока в сети Gossip.
#[derive(Serialize, Deserialize)]
pub struct GossipEnvelope {
    pub topic: String,
    pub payload_b64: String,
    pub sigma_hex: String,
    pub height: u64,
}

/// Энкодим блок: base64-пейлоад, sigma_hex = blake3(payload).
pub fn encode_block(topic: &str, blk: &Block) -> anyhow::Result<GossipEnvelope> {
    let bytes = serde_json::to_vec(blk)?;
    let sigma_hex = hex::encode(blake3::hash(&bytes).as_bytes());
    Ok(GossipEnvelope {
        topic: topic.to_string(),
        payload_b64: B64.encode(bytes),
        sigma_hex,
        height: blk.height,
    })
}

/// Декодим блок из конверта.
pub fn decode_block(env: &GossipEnvelope) -> anyhow::Result<Block> {
    let bytes = B64.decode(&env.payload_b64)?;
    let blk: Block = serde_json::from_slice(&bytes)?;
    Ok(blk)
}

/// Пропускает ли блок фазовый фильтр (решение — по самому блоку).
pub fn pass_phase_filter(env: &GossipEnvelope) -> bool {
    if let Ok(blk) = decode_block(env) {
        block_passes_phase(&blk)
    } else {
        false
    }
}

```


## node/src/peers.rs
<a id="node-src-peers-rs"></a>

```rust
#![allow(dead_code)]
#![allow(dead_code)]
use std::time::{SystemTime, UNIX_EPOCH};
fn now_ms() -> u128 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map(|d| d.as_millis() as u128)
        .unwrap_or(0)
}

use once_cell::sync::Lazy;
use prometheus::{register_int_gauge, IntGauge};
use std::{
    collections::HashMap,
    sync::{Arc, Mutex},
    time::Duration,
};

static QUARANTINED_GAUGE: Lazy<IntGauge> =
    Lazy::new(|| register_int_gauge!("peers_quarantined", "quarantined peers").unwrap());
static PEERS_TOTAL_GAUGE: Lazy<IntGauge> =
    Lazy::new(|| register_int_gauge!("peers_total", "known peers").unwrap());

#[derive(Clone, Debug)]
pub struct PeerScore {
    pub last_seen_ms: u128,
    pub score_milli: i64,
    pub fails: u32,
    pub dups: u32,
    pub banned_until_ms: u128,
}
impl Default for PeerScore {
    fn default() -> Self {
        Self {
            last_seen_ms: now_ms(),
            score_milli: 0,
            fails: 0,
            dups: 0,
            banned_until_ms: 0,
        }
    }
}

/// Резонансные параметры скоринга
#[derive(Clone)]
pub struct PeerPolicy {
    pub ban_ttl_ms: u128,
    pub decay_ms: u128,
    pub up_tick: i64,
    pub dup_penalty: i64,
    pub invalid_penalty: i64,
    pub ban_threshold_milli: i64,
    pub unban_threshold_milli: i64,
}
impl Default for PeerPolicy {
    fn default() -> Self {
        Self {
            ban_ttl_ms: 60_000,    // 60s карантин
            decay_ms: 10_000,      // каждые 10s подплытие к 0
            up_tick: 150,          // успешный блок/голос +0.150
            dup_penalty: -50,      // дубликат −0.050
            invalid_penalty: -500, // невалидное сообщение −0.500
            ban_threshold_milli: -1500,
            unban_threshold_milli: -300,
        }
    }
}

#[derive(Clone)]
pub struct PeerBook {
    inner: Arc<Mutex<HashMap<String, PeerScore>>>, // pk_b58 -> score
    policy: PeerPolicy,
}
impl PeerBook {
    pub fn new(policy: PeerPolicy) -> Self {
        Self {
            inner: Arc::new(Mutex::new(HashMap::new())),
            policy,
        }
    }
    fn entry_mut(&self, _pk: &str) -> std::sync::MutexGuard<'_, HashMap<String, PeerScore>> {
        self.inner.lock().unwrap()
    }

    pub fn on_success(&self, pk: &str) {
        let mut m = self.entry_mut(pk);
        let s = m.entry(pk.to_string()).or_default();
        s.last_seen_ms = now_ms();
        s.score_milli += self.policy.up_tick;
        if s.score_milli > 5000 {
            s.score_milli = 5000;
        }
    }
    pub fn on_duplicate(&self, pk: &str) {
        let mut m = self.entry_mut(pk);
        let s = m.entry(pk.to_string()).or_default();
        s.dups += 1;
        s.score_milli += self.policy.dup_penalty;
        if s.score_milli < self.policy.ban_threshold_milli {
            s.banned_until_ms = now_ms() + self.policy.ban_ttl_ms;
        }
    }
    pub fn on_invalid(&self, pk: &str) {
        let mut m = self.entry_mut(pk);
        let s = m.entry(pk.to_string()).or_default();
        s.fails += 1;
        s.score_milli += self.policy.invalid_penalty;
        s.banned_until_ms = now_ms() + self.policy.ban_ttl_ms;
    }
    pub fn is_quarantined(&self, pk: &str) -> bool {
        let m = self.inner.lock().unwrap();
        m.get(pk)
            .map(|s| now_ms() < s.banned_until_ms)
            .unwrap_or(false)
    }
    pub fn tick(&self) {
        let mut m = self.inner.lock().unwrap();
        let now = now_ms();
        let mut banned = 0;
        for (_k, s) in m.iter_mut() {
            // decay к 0
            if s.score_milli < 0 {
                let dt = (now.saturating_sub(s.last_seen_ms)) as i128;
                if dt > 0 {
                    let steps = (dt as f64 / self.policy.decay_ms as f64).floor() as i64;
                    if steps > 0 {
                        s.score_milli += steps * 50; // +0.050/шаг
                        if s.score_milli > 0 {
                            s.score_milli = 0;
                        }
                        s.last_seen_ms = now;
                    }
                }
            }
            // снять бан, если вышли из «красной зоны»
            if s.banned_until_ms > 0
                && now >= s.banned_until_ms
                && s.score_milli > self.policy.unban_threshold_milli
            {
                s.banned_until_ms = 0;
            }
            if s.banned_until_ms > now {
                banned += 1;
            }
        }
        QUARANTINED_GAUGE.set(banned);
        PEERS_TOTAL_GAUGE.set(m.len() as i64);
    }
}
pub fn spawn_peer_aging(book: PeerBook) {
    tokio::spawn(async move {
        let mut t = tokio::time::interval(Duration::from_millis(2000));
        loop {
            t.tick().await;
            book.tick();
        }
    });
}

```


## node/src/guard.rs
<a id="node-src-guard-rs"></a>

```rust
use axum::{body::Body, http::Request, middleware::Next, response::Response};
use rand::{thread_rng, Rng};
use std::time::Duration;

/// Лёгкий фазовый «шум»: джиттер 0–7мс для submit/stake/bridge путей
pub async fn rate_limit_mw(req: Request<Body>, next: Next) -> Response {
    let p = req.uri().path();
    if p.starts_with("/submit_tx") || p.starts_with("/stake/") || p.starts_with("/bridge/") {
        let jitter = thread_rng().gen_range(0..=7);
        tokio::time::sleep(Duration::from_millis(jitter)).await;
    }
    next.run(req).await
}

```


## node/src/metrics.rs
<a id="node-src-metrics-rs"></a>

```rust
use axum::{
    body::Body,
    http::Request,
    middleware::Next,
    response::IntoResponse,
    http::StatusCode,
};
use once_cell::sync::Lazy;
use prometheus::{
    Encoder, HistogramVec, IntCounter, IntCounterVec, IntGauge, Registry, TextEncoder,
    register_histogram_vec, register_int_counter, register_int_counter_vec, register_int_gauge,
};
use std::time::Instant;

pub static REGISTRY: Lazy<Registry> = Lazy::new(Registry::new);

// ---- HTTP ----
static HTTP_REQS: Lazy<IntCounterVec> = Lazy::new(|| {
    register_int_counter_vec!("logos_http_requests_total","HTTP reqs",&["method","path","status"]).unwrap()
});
static HTTP_LAT: Lazy<HistogramVec> = Lazy::new(|| {
    register_histogram_vec!("logos_http_duration_seconds","HTTP latency",&["method","path","status"],
        prometheus::exponential_buckets(0.001,2.0,14).unwrap()).unwrap()
});

// ---- Chain ----
static BLOCKS_TOTAL: Lazy<IntCounter> = Lazy::new(|| register_int_counter!("logos_blocks_produced_total","Blocks total").unwrap());
static HEAD_HEIGHT: Lazy<IntGauge>    = Lazy::new(|| register_int_gauge!("logos_head_height","Head").unwrap());
static FINAL_HEIGHT: Lazy<IntGauge>   = Lazy::new(|| register_int_gauge!("logos_finalized_height","Finalized").unwrap());

// ---- Tx ----
static TX_ACCEPTED: Lazy<IntCounter> = Lazy::new(|| register_int_counter!("logos_tx_accepted_total","Accepted tx").unwrap());
static TX_REJECTED: Lazy<IntCounterVec> = Lazy::new(|| {
    register_int_counter_vec!("logos_tx_rejected_total","Rejected tx",&["reason"]).unwrap()
});

// ---- Bridge (durable) ----
static BRIDGE_OPS: Lazy<IntCounterVec> = Lazy::new(|| {
    register_int_counter_vec!("logos_bridge_ops_total","Bridge ops",&["kind","status"]).unwrap()
});

// ---- Archive backpressure ----
static ARCHIVE_QUEUE: Lazy<IntGauge> = Lazy::new(|| register_int_gauge!("logos_archive_queue","Archive queue depth").unwrap());

fn norm(p:&str)->String{
    if p.starts_with("/balance/") {"/balance/:rid".into()}
    else if p.starts_with("/history/"){"/history/:rid".into()}
    else if p.starts_with("/stake/my/"){"/stake/my/:rid".into()}
    else {p.to_string()}
}

pub async fn track(req: Request<Body>, next: Next) -> axum::response::Response {
    let m=req.method().as_str().to_owned();
    let p=norm(req.uri().path());
    let t=Instant::now();
    let res=next.run(req).await;
    let s=res.status().as_u16().to_string();
    HTTP_REQS.with_label_values(&[&m,&p,&s]).inc();
    HTTP_LAT.with_label_values(&[&m,&p,&s]).observe(t.elapsed().as_secs_f64());
    res
}

pub async fn prometheus()->impl IntoResponse{
    let mfs=REGISTRY.gather();
    let mut buf=Vec::new();
    let enc=TextEncoder::new();
    if let Err(_)=enc.encode(&mfs,&mut buf){ return (StatusCode::INTERNAL_SERVER_ERROR,"encode error").into_response(); }
    match String::from_utf8(buf){
        Ok(body)=>(StatusCode::OK,body).into_response(),
        Err(_)=>(StatusCode::INTERNAL_SERVER_ERROR,"utf8 error").into_response(),
    }
}

// API для модулей
pub fn inc_block_produced(){ BLOCKS_TOTAL.inc(); }
pub fn set_chain(h:u64, f:u64){ HEAD_HEIGHT.set(h as i64); FINAL_HEIGHT.set(f as i64); }
pub fn inc_tx_accepted(){ TX_ACCEPTED.inc(); }
pub fn inc_tx_rejected(reason:&'static str){ TX_REJECTED.with_label_values(&[reason]).inc(); }
pub fn inc_bridge(kind:&'static str, status:&'static str){ BRIDGE_OPS.with_label_values(&[kind,status]).inc(); }
pub fn set_archive_queue(n:i64){ ARCHIVE_QUEUE.set(n); }

// Совместимость со старым кодом
#[allow(dead_code)] pub fn inc_total(_label:&str){}

```


## node/src/api/mod.rs
<a id="node-src-api-mod-rs"></a>

```rust
//! API root: общие модели / утилиты подписи / экспорт хендлеров.

use axum::{http::StatusCode, Json};
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};
use sha2::{Digest, Sha256};
use ed25519_dalek::{
    Verifier, Signature, VerifyingKey, PUBLIC_KEY_LENGTH, SIGNATURE_LENGTH,
};

pub mod base;
pub mod tx;
pub mod archive;
pub mod staking;

// --------- базовые ответы ---------

#[derive(Serialize)]
pub struct OkMsg {
    pub status: &'static str,
}

#[derive(Serialize)]
pub struct Head {
    pub height: u64,
    pub finalized: u64,
}

#[derive(Serialize)]
pub struct Balance {
    pub rid: String,
    pub balance: u128,
    pub nonce: u64,
}

// --------- модели транзакций ---------

#[derive(Deserialize, Clone)]
pub struct TxIn {
    pub from: String,
    pub to: String,
    pub amount: u64,
    pub nonce: u64,
    /// подпись в hex, как шлёт кошелёк
    pub sig_hex: String,
    #[serde(default)]
    pub memo: Option<String>,
}

#[derive(Serialize)]
pub struct SubmitResult {
    pub ok: bool,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub txid: Option<String>,
    pub info: String,
}

#[derive(Serialize)]
pub struct SubmitBatchItem {
    pub ok: bool,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub txid: Option<String>,
    pub info: String,
    pub index: usize,
}

#[derive(Deserialize)]
pub struct SubmitBatchReq {
    pub txs: Vec<TxIn>,
}

// --------- экономика / история ---------

#[derive(Serialize)]
pub struct Economy {
    pub supply: u64,
    pub burned: u64,
    pub cap: u64,
}

#[derive(Serialize)]
pub struct HistoryItem {
    pub txid: String,
    pub height: u64,
    pub from: String,
    pub to: String,
    pub amount: u64,
    pub nonce: u64,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub ts: Option<u64>,
}

// --------- утилиты подписи (должны совпадать с кошельком) ---------

pub fn canonical_msg(from: &str, to: &str, amount: u64, nonce: u64) -> Vec<u8> {
    let mut h = Sha256::new();
    h.update(from.as_bytes());
    h.update(b"|");
    h.update(to.as_bytes());
    h.update(b"|");
    h.update(&amount.to_be_bytes());
    h.update(b"|");
    h.update(&nonce.to_be_bytes());
    h.finalize().to_vec()
}

pub fn verify_sig(from: &str, msg: &[u8], sig_hex: &str) -> Result<(), String> {
    let pubkey_bytes =
        bs58::decode(from).into_vec().map_err(|e| format!("bad_from_rid_base58: {e}"))?;
    if pubkey_bytes.len() != PUBLIC_KEY_LENGTH {
        return Err(format!(
            "bad_pubkey_len: got {} want {}",
            pubkey_bytes.len(),
            PUBLIC_KEY_LENGTH
        ));
    }

    let mut pk_arr = [0u8; PUBLIC_KEY_LENGTH];
    pk_arr.copy_from_slice(&pubkey_bytes);
    let vk = VerifyingKey::from_bytes(&pk_arr).map_err(|e| format!("bad_pubkey: {e}"))?;

    let sig_bytes = hex::decode(sig_hex).map_err(|e| format!("bad_sig_hex: {e}"))?;
    if sig_bytes.len() != SIGNATURE_LENGTH {
        return Err(format!(
            "bad_sig_len: got {} want {}",
            sig_bytes.len(),
            SIGNATURE_LENGTH
        ));
    }

    let mut sig_arr = [0u8; SIGNATURE_LENGTH];
    sig_arr.copy_from_slice(&sig_bytes);
    let sig = Signature::from_bytes(&sig_arr);

    vk.verify(msg, &sig).map_err(|_| "bad_signature".to_string())
}

// --------- /debug_canon — совместимость со старым кошельком ---------
//
// Понимаем оба формата:
//   { "tx": { "from": "...", "to": "...", "amount": 1, "nonce": 1 } }
//   { "from": "...", "to": "...", "amount": 1, "nonce": 1 }

pub async fn debug_canon(Json(body): Json<Value>) -> (StatusCode, Json<Value>) {
    fn extract(v: &Value) -> Result<(String, String, u64, u64), String> {
        if let Some(obj) = v.as_object() {
            // legacy: обёртка {"tx":{...}}
            if let Some(inner) = obj.get("tx") {
                return extract(inner);
            }

            let from = obj
                .get("from")
                .and_then(|x| x.as_str())
                .ok_or_else(|| "missing field `from`".to_string())?;
            let to = obj
                .get("to")
                .and_then(|x| x.as_str())
                .ok_or_else(|| "missing field `to`".to_string())?;
            let amount = obj
                .get("amount")
                .and_then(|x| x.as_u64())
                .ok_or_else(|| "missing field `amount`".to_string())?;
            let nonce = obj
                .get("nonce")
                .and_then(|x| x.as_u64())
                .ok_or_else(|| "missing field `nonce`".to_string())?;

            Ok((from.to_string(), to.to_string(), amount, nonce))
        } else {
            Err("expected JSON object".to_string())
        }
    }

    match extract(&body) {
        Ok((from, to, amount, nonce)) => {
            let msg = canonical_msg(&from, &to, amount, nonce);
            let canon_hex = hex::encode(msg);
            (
                StatusCode::OK,
                Json(json!({ "canon_hex": canon_hex })),
            )
        }
        Err(e) => (
            StatusCode::UNPROCESSABLE_ENTITY,
            Json(json!({ "error": e })),
        ),
    }
}

// --------- реэкспорт хендлеров для main.rs ---------

pub use base::{healthz, head, balance, economy, history};
pub use tx::{submit_tx, submit_tx_batch};
pub use archive::{archive_history, archive_tx, archive_blocks, archive_txs};
pub use staking::{stake_delegate, stake_undelegate, stake_claim, stake_my};

```


## node/src/api/base.rs
<a id="node-src-api-base-rs"></a>

```rust
use axum::{extract::{Path, State}, Json};
use std::sync::Arc;
use crate::state::AppState;
use super::{OkMsg, Head, Balance, Economy, HistoryItem};

pub async fn healthz() -> Json<OkMsg> {
    Json(OkMsg { status: "ok" })
}

pub async fn head(State(app): State<Arc<AppState>>) -> Json<Head> {
    let l = app.ledger.lock();
    // В новом ledger нет head_height(), используем height()
    let h = l.height().unwrap_or(0);
    let fin = h.saturating_sub(1);
    Json(Head { height: h, finalized: fin })
}

pub async fn balance(
    Path(rid): Path<String>,
    State(app): State<Arc<AppState>>,
) -> Json<Balance> {
    let l = app.ledger.lock();
    let bal = l.get_balance(&rid).unwrap_or(0);
    let n = l.get_nonce(&rid).unwrap_or(0);
    Json(Balance {
        rid,
        balance: bal as u128,
        nonce: n,
    })
}

pub async fn economy(State(app): State<Arc<AppState>>) -> Json<Economy> {
    const CAP_MICRO: u64 = 81_000_000_u64 * 1_000_000_u64;
    // ledger.supply() уже даёт (u64, u64)
    let (minted, burned) = app.ledger.lock().supply().unwrap_or((0, 0));
    let supply = minted.saturating_sub(burned);
    Json(Economy {
        supply,
        burned,
        cap: CAP_MICRO,
    })
}

pub async fn history(
    Path(rid): Path<String>,
    State(app): State<Arc<AppState>>,
) -> Json<Vec<HistoryItem>> {
    let l = app.ledger.lock();
    let rows = l.account_txs_page(&rid, 0, 100).unwrap_or_default();

    Json(
        rows
            .into_iter()
            .map(|r| HistoryItem {
                txid: r.txid,
                height: r.height,
                from: r.from,
                to: r.to,
                amount: r.amount,
                nonce: r.nonce,
                // r.ts сейчас Option<u64>, аккуратно делим на 1000
                ts: r.ts.map(|ts| ts / 1000),
            })
            .collect(),
    )
}

```


## node/src/api/tx.rs
<a id="node-src-api-tx-rs"></a>

```rust
use axum::{extract::State, http::StatusCode, Json};
use std::sync::Arc;
use tracing::{info, warn, error};

use crate::{state::AppState, metrics};
use super::{TxIn, SubmitResult, SubmitBatchReq, SubmitBatchItem};
use super::{canonical_msg, verify_sig};

pub async fn submit_tx(
    State(app): State<Arc<AppState>>,
    Json(tx): Json<TxIn>,
) -> (StatusCode, Json<SubmitResult>) {
    let msg = canonical_msg(&tx.from, &tx.to, tx.amount, tx.nonce);

    if let Err(e) = verify_sig(&tx.from, &msg, &tx.sig_hex) {
        metrics::inc_tx_rejected("bad_signature");
        return (
            StatusCode::UNAUTHORIZED,
            Json(SubmitResult { ok: false, txid: None, info: e }),
        );
    }

    let prev = app.ledger.lock().get_nonce(&tx.from).unwrap_or(0);
    if tx.nonce <= prev {
        metrics::inc_tx_rejected("nonce_reuse");
        return (
            StatusCode::CONFLICT,
            Json(SubmitResult {
                ok: false,
                txid: None,
                info: "nonce_reuse".into(),
            }),
        );
    }

    let stx = match app
        .ledger
        .lock()
        .submit_tx_simple(&tx.from, &tx.to, tx.amount, tx.nonce, tx.memo.as_deref())
    {
        Ok(s) => s,
        Err(e) => {
            metrics::inc_tx_rejected("internal");
            return (
                StatusCode::OK,
                Json(SubmitResult {
                    ok: false,
                    txid: None,
                    info: e.to_string(),
                }),
            );
        }
    };

    if let Some(arch) = &app.archive {
        let ts_sec = stx.ts.map(|ts| ts / 1000);
        match arch
            .record_tx(
                &stx.txid,
                stx.height,
                &stx.from,
                &stx.to,
                stx.amount,
                stx.nonce,
                ts_sec,
            )
            .await
        {
            Ok(()) => info!("archive: wrote tx {}", stx.txid),
            Err(e) => error!("archive: write failed: {}", e),
        }
    } else {
        warn!("archive: not configured");
    }

    metrics::inc_tx_accepted();
    (
        StatusCode::OK,
        Json(SubmitResult {
            ok: true,
            txid: Some(stx.txid),
            info: "accepted".into(),
        }),
    )
}

pub async fn submit_tx_batch(
    State(app): State<Arc<AppState>>,
    Json(req): Json<SubmitBatchReq>,
) -> (StatusCode, Json<Vec<SubmitBatchItem>>) {
    let mut out = Vec::with_capacity(req.txs.len());

    // 1) проверяем и коммитим tx по правилам (подпись, nonce)
    for (i, tx) in req.txs.into_iter().enumerate() {
        let msg = canonical_msg(&tx.from, &tx.to, tx.amount, tx.nonce);

        if let Err(e) = verify_sig(&tx.from, &msg, &tx.sig_hex) {
            metrics::inc_tx_rejected("bad_signature");
            out.push(SubmitBatchItem {
                ok: false,
                txid: None,
                info: e,
                index: i,
            });
            continue;
        }

        let prev = app.ledger.lock().get_nonce(&tx.from).unwrap_or(0);
        if tx.nonce <= prev {
            metrics::inc_tx_rejected("nonce_reuse");
            out.push(SubmitBatchItem {
                ok: false,
                txid: None,
                info: "nonce_reuse".into(),
                index: i,
            });
            continue;
        }

        match app
            .ledger
            .lock()
            .submit_tx_simple(&tx.from, &tx.to, tx.amount, tx.nonce, tx.memo.as_deref())
        {
            Ok(s) => {
                metrics::inc_tx_accepted();
                out.push(SubmitBatchItem {
                    ok: true,
                    txid: Some(s.txid),
                    info: "accepted".into(),
                    index: i,
                });
            }
            Err(e) => {
                metrics::inc_tx_rejected("internal");
                out.push(SubmitBatchItem {
                    ok: false,
                    txid: None,
                    info: e.to_string(),
                    index: i,
                });
            }
        }
    }

    // 2) инжест в архив — собираем только принятые
    if let Some(arch) = &app.archive {
        let mut rows: Vec<(String, u64, String, String, u64, u64, Option<u64>)> =
            Vec::new();

        for item in &out {
            if !item.ok {
                continue;
            }
            let txid = match &item.txid {
                Some(t) => t.clone(),
                None => continue,
            };

            if let Ok(Some(stx)) = app.ledger.lock().get_tx(&txid) {
                let ts_sec = stx.ts.map(|ts| ts / 1000);
                rows.push((
                    txid.clone(),
                    stx.height,
                    stx.from.clone(),
                    stx.to.clone(),
                    stx.amount,
                    stx.nonce,
                    ts_sec,
                ));
            }
        }

        if !rows.is_empty() {
            if let Err(e) = arch.record_txs_batch(&rows).await {
                error!("archive: batch write failed: {}", e);
            }
        }
    }

    (StatusCode::OK, Json(out))
}

```


## node/src/archive/mod.rs
<a id="node-src-archive-mod-rs"></a>

```rust
//! Postgres archive backend with simple batch insert & backpressure

use deadpool_postgres::{Manager, Pool};
use tokio_postgres::{NoTls, Row, Config};
use serde::Serialize;
use anyhow::Result;
use crate::metrics;

#[derive(Clone)]
pub struct Archive { pub(crate) pool: Pool }

impl Archive {
    pub async fn new_from_env() -> Option<Self> {
        let url = std::env::var("LRB_ARCHIVE_URL").ok()?;
        let cfg: Config = url.parse().ok()?;
        let mgr = Manager::new(cfg, NoTls);
        let pool = Pool::builder(mgr).max_size(16).build().ok()?;
        Some(Archive { pool })
    }

    pub async fn record_tx(&self, txid:&str, height:u64, from:&str, to:&str, amount:u64, nonce:u64, ts:Option<u64>) -> Result<()> {
        let client = self.pool.get().await?;
        client.execute(
            "insert into txs (txid,height,from_rid,to_rid,amount,nonce,ts) values ($1,$2,$3,$4,$5,$6,to_timestamp($7))",
            &[&txid, &(height as i64), &from, &to, &(amount as i64), &(nonce as i64), &(ts.unwrap_or(0) as i64)]
        ).await?;
        Ok(())
    }

    /// Batch-ingest (owned строки → без проблем с лайфтаймами)
    pub async fn record_txs_batch(
        &self,
        rows:&[(String,u64,String,String,u64,u64,Option<u64>)]
    ) -> Result<()> {
        use std::time::Duration;
        let client = self.pool.get().await?;
        let depth = rows.len() as i64;
        metrics::set_archive_queue(depth);

        let stmt = "insert into txs (txid,height,from_rid,to_rid,amount,nonce,ts) \
                    values ($1,$2,$3,$4,$5,$6,to_timestamp($7)) on conflict do nothing";

        for chunk in rows.chunks(500) {
            for r in chunk {
                client.execute(
                    stmt,
                    &[&r.0, &(r.1 as i64), &r.2, &r.3, &(r.4 as i64), &(r.5 as i64), &(r.6.unwrap_or(0) as i64)]
                ).await?;
            }
            if chunk.len()==500 { tokio::time::sleep(Duration::from_millis(2)).await; }
        }
        metrics::set_archive_queue(0);
        Ok(())
    }

    pub async fn history_by_rid(&self, rid:&str, limit:i64, before:Option<i64>) -> Result<Vec<TxRecord>> {
        let client = self.pool.get().await?;
        let rows = client.query(
            "select txid,height,from_rid,to_rid,amount,nonce,extract(epoch from ts)::bigint as ts \
             from txs where (from_rid=$1 or to_rid=$1) and ($2::bigint is null or height<$2) \
             order by height desc limit $3",
            &[&rid, &before, &limit]
        ).await?;
        Ok(rows.into_iter().map(TxRecord::from_row).collect())
    }

    pub async fn tx_by_id(&self, txid:&str) -> Result<Option<serde_json::Value>> {
        let client = self.pool.get().await?;
        let row = client.query_opt(
            "select txid,height,from_rid,to_rid,amount,nonce,extract(epoch from ts)::bigint as ts \
             from txs where txid=$1", &[&txid]
        ).await?;
        Ok(row.map(|r| serde_json::json!(TxRecord::from_row(r))))
    }

    pub async fn recent_blocks(&self, limit:i64, before:Option<i64>) -> Result<Vec<BlockRow>> {
        let client = self.pool.get().await?;
        let rows = client.query(
            "select height,hash,extract(epoch from ts)::bigint as ts,tx_count \
             from blocks where ($1::bigint is null or height<$1) order by height desc limit $2",
            &[&before, &limit]
        ).await?;
        Ok(rows.into_iter().map(BlockRow::from_row).collect())
    }

    pub async fn recent_txs(&self, limit:i64, rid:Option<&str>, before_ts:Option<i64>) -> Result<Vec<TxRecord>> {
        let client = self.pool.get().await?;
        let rows = if let Some(rid)=rid {
            client.query(
                "select txid,height,from_rid,to_rid,amount,nonce,extract(epoch from ts)::bigint as ts \
                 from txs where (from_rid=$1 or to_rid=$1) and ($2::bigint is null or extract(epoch from ts)<$2) \
                 order by ts desc limit $3",
                &[&rid, &before_ts, &limit]
            ).await?
        } else {
            client.query(
                "select txid,height,from_rid,to_rid,amount,nonce,extract(epoch from ts)::bigint as ts \
                 from txs where ($1::bigint is null or extract(epoch from ts)<$1) order by ts desc limit $2",
                &[&before_ts, &limit]
            ).await?
        };
        Ok(rows.into_iter().map(TxRecord::from_row).collect())
    }

    // нужен для /archive_block (и может использоваться API)
    pub async fn block_by_height(&self, h:i64) -> Result<Option<BlockRow>> {
        let client = self.pool.get().await?;
        let row = client.query_opt(
            "select height,hash,extract(epoch from ts)::bigint as ts,tx_count from blocks where height=$1",
            &[&h]
        ).await?;
        Ok(row.map(BlockRow::from_row))
    }
}

#[derive(Serialize)]
pub struct BlockRow { pub height:i64, pub hash:String, pub ts:i64, pub tx_count:i64 }
impl BlockRow { fn from_row(r:Row)->Self { Self{ height:r.get(0), hash:r.get(1), ts:r.get(2), tx_count:r.get(3) } } }

#[derive(Serialize)]
pub struct TxRecord { pub txid:String, pub height:i64, pub from:String, pub to:String, pub amount:i64, pub nonce:i64, pub ts:Option<i64> }
impl TxRecord { fn from_row(r:Row)->Self { Self{
    txid:r.get(0), height:r.get(1), from:r.get(2), to:r.get(3), amount:r.get(4), nonce:r.get(5), ts:r.get(6)
}}}

```


## node/src/archive/pg.rs
<a id="node-src-archive-pg-rs"></a>

```rust
//! Postgres архивация: deadpool-postgres, батч-вставки (prod).
//! ENV: LRB_ARCHIVE_URL=postgres://user:pass@host:5432/db

use anyhow::Result;
use deadpool_postgres::{Config, ManagerConfig, Pool, RecyclingMethod};
use tokio_postgres::NoTls;

#[derive(Clone)]
pub struct ArchivePg {
    pool: Pool,
}

impl ArchivePg {
    pub async fn new(url: &str) -> Result<Self> {
        // Правильная настройка пула: используем поле `url`
        let mut cfg = Config::new();
        cfg.url = Some(url.to_string());
        cfg.manager = Some(ManagerConfig { recycling_method: RecyclingMethod::Fast });
        // Можно добавить пул-лимиты при необходимости:
        // cfg.pool = Some(deadpool_postgres::PoolConfig { max_size: 32, ..Default::default() });

        let pool = cfg.create_pool(Some(deadpool_postgres::Runtime::Tokio1), NoTls)?;
        let a = Self { pool };
        a.ensure_schema().await?;
        Ok(a)
    }

    async fn ensure_schema(&self) -> Result<()> {
        let client = self.pool.get().await?;
        client.batch_execute(r#"
            CREATE TABLE IF NOT EXISTS tx (
                txid      TEXT PRIMARY KEY,
                height    BIGINT NOT NULL,
                from_rid  TEXT NOT NULL,
                to_rid    TEXT NOT NULL,
                amount    BIGINT NOT NULL,
                nonce     BIGINT NOT NULL,
                ts        BIGINT
            );
            CREATE TABLE IF NOT EXISTS account_tx (
                rid    TEXT NOT NULL,
                height BIGINT NOT NULL,
                txid   TEXT NOT NULL,
                PRIMARY KEY (rid, height, txid)
            );
            CREATE INDEX IF NOT EXISTS idx_tx_height ON tx(height);
            CREATE INDEX IF NOT EXISTS idx_ac_tx_rid_height ON account_tx(rid, height);
        "#).await?;
        Ok(())
    }

    pub async fn record_tx(
        &self,
        txid: &str,
        height: u64,
        from: &str,
        to: &str,
        amount: u64,
        nonce: u64,
        ts: Option<u64>
    ) -> Result<()> {
        let mut client = self.pool.get().await?; // <- нужен mut для build_transaction()
        let stmt1 = client.prepare_cached(
            "INSERT INTO tx(txid,height,from_rid,to_rid,amount,nonce,ts)
             VALUES ($1,$2,$3,$4,$5,$6,$7) ON CONFLICT DO NOTHING"
        ).await?;
        let stmt2 = client.prepare_cached(
            "INSERT INTO account_tx(rid,height,txid)
             VALUES ($1,$2,$3) ON CONFLICT DO NOTHING"
        ).await?;

        let h = height as i64;
        let a = amount as i64;
        let n = nonce as i64;
        let t = ts.map(|v| v as i64);

        let tr = client.build_transaction().start().await?;
        tr.execute(&stmt1, &[&txid, &h, &from, &to, &a, &n, &t]).await?;
        tr.execute(&stmt2, &[&from, &h, &txid]).await?;
        tr.execute(&stmt2, &[&to,   &h, &txid]).await?;
        tr.commit().await?;
        Ok(())
    }

    pub async fn history_page(&self, rid: &str, page: u32, per_page: u32) -> Result<Vec<serde_json::Value>> {
        let client = self.pool.get().await?;
        let per = per_page.clamp(1, 1000) as i64;
        let offset = (page as i64) * per;
        let stmt = client.prepare_cached(r#"
            SELECT t.txid,t.height,t.from_rid,t.to_rid,t.amount,t.nonce,t.ts
            FROM account_tx a JOIN tx t ON t.txid=a.txid
            WHERE a.rid=$1
            ORDER BY t.height DESC
            LIMIT $2 OFFSET $3
        "#).await?;
        let rows = client.query(&stmt, &[&rid, &per, &offset]).await?;
        Ok(rows.iter().map(|r| {
            serde_json::json!({
                "txid":   r.get::<_, String>(0),
                "height": r.get::<_, i64>(1),
                "from":   r.get::<_, String>(2),
                "to":     r.get::<_, String>(3),
                "amount": r.get::<_, i64>(4),
                "nonce":  r.get::<_, i64>(5),
                "ts":     r.get::<_, Option<i64>>(6),
            })
        }).collect())
    }

    pub async fn get_tx(&self, txid: &str) -> Result<Option<serde_json::Value>> {
        let client = self.pool.get().await?;
        let stmt = client.prepare_cached(
            "SELECT txid,height,from_rid,to_rid,amount,nonce,ts FROM tx WHERE txid=$1"
        ).await?;
        let row = client.query_opt(&stmt, &[&txid]).await?;
        Ok(row.map(|r| serde_json::json!({
            "txid":   r.get::<_, String>(0),
            "height": r.get::<_, i64>(1),
            "from":   r.get::<_, String>(2),
            "to":     r.get::<_, String>(3),
            "amount": r.get::<_, i64>(4),
            "nonce":  r.get::<_, i64>(5),
            "ts":     r.get::<_, Option<i64>>(6),
        })))
    }
}

```


## node/src/archive/sqlite.rs
<a id="node-src-archive-sqlite-rs"></a>

```rust
use anyhow::Result;
use r2d2::{Pool, PooledConnection};
use r2d2_sqlite::SqliteConnectionManager;
use rusqlite::{params, OptionalExtension};

#[derive(Clone)]
pub struct ArchiveSqlite { pool: Pool<SqliteConnectionManager> }

impl ArchiveSqlite {
    pub fn new_from_env() -> Option<Self> {
        let path = std::env::var("LRB_ARCHIVE_PATH").ok()?;
        let mgr  = SqliteConnectionManager::file(path);
        let pool = Pool::builder().max_size(8).build(mgr).ok()?;
        let a = Self { pool };
        a.ensure_schema().ok()?;
        Some(a)
    }
    fn conn(&self) -> Result<PooledConnection<SqliteConnectionManager>> { Ok(self.pool.get()?) }
    fn ensure_schema(&self) -> Result<()> {
        let c = self.conn()?;
        c.execute_batch(r#"
            PRAGMA journal_mode=WAL;
            PRAGMA synchronous=NORMAL;
            CREATE TABLE IF NOT EXISTS tx (txid TEXT PRIMARY KEY, height INTEGER, from_rid TEXT, to_rid TEXT, amount INTEGER, nonce INTEGER, ts INTEGER);
            CREATE TABLE IF NOT EXISTS account_tx (rid TEXT, height INTEGER, txid TEXT, PRIMARY KEY(rid,height,txid));
            CREATE INDEX IF NOT EXISTS idx_tx_height ON tx(height);
            CREATE INDEX IF NOT EXISTS idx_ac_tx_rid_height ON account_tx(rid,height);
        "#)?;
        Ok(())
    }
    pub fn record_tx(&self, txid:&str, h:u64, from:&str, to:&str, amount:u64, nonce:u64, ts:Option<u64>) -> Result<()> {
        let c = self.conn()?;
        let tx = c.unchecked_transaction()?;
        tx.execute("INSERT OR IGNORE INTO tx(txid,height,from_rid,to_rid,amount,nonce,ts) VALUES(?,?,?,?,?,?,?)",
            params![txid, h as i64, from, to, amount as i64, nonce as i64, ts.map(|v| v as i64)])?;
        tx.execute("INSERT OR IGNORE INTO account_tx(rid,height,txid) VALUES(?,?,?)", params![from, h as i64, txid])?;
        tx.execute("INSERT OR IGNORE INTO account_tx(rid,height,txid) VALUES(?,?,?)", params![to,   h as i64, txid])?;
        tx.commit()?;
        Ok(())
    }
    pub fn history_page(&self, rid:&str, page:u32, per_page:u32) -> Result<Vec<serde_json::Value>> {
        let c = self.conn()?;
        let per = per_page.clamp(1,1000) as i64;
        let offset = (page as i64) * per;
        let mut st = c.prepare(
            "SELECT t.txid,t.height,t.from_rid,t.to_rid,t.amount,t.nonce,t.ts \
             FROM account_tx a JOIN tx t ON t.txid=a.txid \
             WHERE a.rid=? ORDER BY t.height DESC LIMIT ? OFFSET ?")?;
        let rows = st.query_map(params![rid, per, offset], |row| Ok(serde_json::json!({
            "txid": row.get::<_, String>(0)?, "height": row.get::<_, i64>(1)?,
            "from": row.get::<_, String>(2)?, "to": row.get::<_, String>(3)?,
            "amount": row.get::<_, i64>(4)?, "nonce": row.get::<_, i64>(5)?,
            "ts": row.get::<_, Option<i64>>(6)?
        })))?;
        let mut out = Vec::with_capacity(per as usize);
        for it in rows { out.push(it?); }
        Ok(out)
    }
    pub fn get_tx(&self, txid:&str) -> Result<Option<serde_json::Value>> {
        let c = self.conn()?;
        let mut st = c.prepare("SELECT txid,height,from_rid,to_rid,amount,nonce,ts FROM tx WHERE txid=?")?;
        let v = st.query_row(params![txid], |r| Ok(serde_json::json!({
            "txid": r.get::<_, String>(0)?, "height": r.get::<_, i64>(1)?,
            "from": r.get::<_, String>(2)?, "to": r.get::<_, String>(3)?,
            "amount": r.get::<_, i64>(4)?, "nonce": r.get::<_, i64>(5)?,
            "ts": r.get::<_, Option<i64>>(6)?
        }))).optional()?;
        Ok(v)
    }
}

```

