# FULL SOURCE — `/root/logos_lrb/modules`

**No truncation.** Full file contents inside code fences.


---

## FILE: `/root/logos_lrb/modules/beacon_emitter.rs`

```rs
use axum::{
    extract::State,
    routing::{get, post},
    Router,
};
use std::{net::SocketAddr, time::Duration};
use tower::{ServiceBuilder};
use tower_http::{
    cors::{Any, CorsLayer},
    trace::TraceLayer,
    timeout::TimeoutLayer,
    limit::{RequestBodyLimitLayer},
};
use tracing_subscriber::{EnvFilter, fmt};
use ed25519_dalek::{SigningKey, VerifyingKey, SignatureError};
use rand_core::OsRng;
use bs58;
use once_cell::sync::OnceCell;
use anyhow::Result;

mod api;
mod admin;
mod bridge;
mod gossip;
mod state;
mod peers;
mod fork;

#[derive(Clone)]
struct AppState {
    signing: SigningKey,
    verifying: VerifyingKey,
    rid_b58: String,
    admin_key: String,
    bridge_key: String,
}

static APP_STATE: OnceCell<AppState> = OnceCell::new();

fn load_signing_key() -> Result<SigningKey> {
    use std::env;
    if let Ok(hex) = env::var("LRB_NODE_SK_HEX") {
        let bytes = hex::decode(hex.trim())?;
        let sk = SigningKey::from_bytes(bytes.as_slice().try_into().map_err(|_| anyhow::anyhow!("bad SK len"))?);
        return Ok(sk);
    }
    if let Ok(path) = env::var("LRB_NODE_SK_PATH") {
        let data = std::fs::read(path)?;
        let sk = SigningKey::from_bytes(data.as_slice().try_into().map_err(|_| anyhow::anyhow!("bad SK len"))?);
        return Ok(sk);
    }
    anyhow::bail!("missing LRB_NODE_SK_HEX or LRB_NODE_SK_PATH");
}

fn rid_from_vk(vk: &VerifyingKey) -> String {
    bs58::encode(vk.as_bytes()).into_string()
}

fn read_env_required(n: &str) -> Result<String> {
    let v = std::env::var(n).map_err(|_| anyhow::anyhow!("missing env {}", n))?;
    Ok(v)
}

fn guard_secret(name: &str, v: &str) -> Result<()> {
    let bad = ["CHANGE_ADMIN_KEY","CHANGE_ME","", "changeme", "default"];
    if bad.iter().any(|b| v.eq_ignore_ascii_case(b)) {
        anyhow::bail!("{} is default/empty; refuse to start", name);
    }
    Ok(())
}

#[tokio::main]
async fn main() -> Result<()> {
    // tracing
    let filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new("info,tower_http=info,axum=info"));
    fmt().with_env_filter(filter).init();

    // keys + env
    let sk = load_signing_key()?;
    let vk = VerifyingKey::from(&sk);
    let rid = rid_from_vk(&vk);

    let admin_key = read_env_required("LRB_ADMIN_KEY")?;
    let bridge_key = read_env_required("LRB_BRIDGE_KEY")?;
    guard_secret("LRB_ADMIN_KEY", &admin_key)?;
    guard_secret("LRB_BRIDGE_KEY", &bridge_key)?;

    let state = AppState {
        signing: sk,
        verifying: vk,
        rid_b58: rid.clone(),
        admin_key,
        bridge_key,
    };
    APP_STATE.set(state.clone()).unwrap();

    // CORS
    let cors = {
        let allowed_origin = std::env::var("LRB_WALLET_ORIGIN").unwrap_or_else(|_| String::from("https://wallet.example"));
        CorsLayer::new()
            .allow_origin(allowed_origin.parse::<axum::http::HeaderValue>().unwrap())
            .allow_methods([axum::http::Method::GET, axum::http::Method::POST])
            .allow_headers([axum::http::header::CONTENT_TYPE, axum::http::header::AUTHORIZATION])
    };

    // limits/timeout
    let layers = ServiceBuilder::new()
        .layer(TraceLayer::new_for_http())
        .layer(TimeoutLayer::new(Duration::from_secs(10)))
        .layer(RequestBodyLimitLayer::new(512 * 1024)) // 512 KiB
        .layer(cors)
        .into_inner();

    // маршруты
    let app = Router::new()
        .route("/healthz", get(api::healthz))
        .route("/head", get(api::head))
        .route("/balance/:rid", get(api::balance))
        .route("/submit_tx", post(api::submit_tx))
        .route("/submit_tx_batch", post(api::submit_tx_batch))
        .route("/debug_canon", post(api::debug_canon))
        .route("/faucet", post(api::faucet)) // dev-only
        .route("/bridge/deposit", post(bridge::deposit))
        .route("/bridge/redeem", post(bridge::redeem))
        .route("/bridge/verify", post(bridge::verify))
        .route("/admin/snapshot", post(admin::snapshot))
        .route("/admin/restore", post(admin::restore))
        .route("/node/info", get(admin::node_info))
        .with_state(state)
        .layer(layers);

    let addr: SocketAddr = std::env::var("LRB_NODE_LISTEN")
        .unwrap_or_else(|_| "0.0.0.0:8080".into())
        .parse()?;
    tracing::info!("logos_node listening on {} (RID={})", addr, rid);
    axum::serve(tokio::net::TcpListener::bind(addr).await?, app).await?;
    Ok(())
}
```

---

## FILE: `/root/logos_lrb/modules/env_impact_tracker.py`

```py
# LOGOS Environmental Impact Tracker
# Автор: LOGOS Core Dev

import time
import json
import os
import psutil
from cryptography.fernet import Fernet
from typing import Dict
from resonance_analyzer import ResonanceAnalyzer

class EnvImpactTracker:
    def __init__(self):
        self.state_file = "env_impact_state.json"
        self.log_file = "env_impact_log.json"
        self.cipher = Fernet(Fernet.generate_key())
        self.lambda_zero = "Λ0"
        self.valid_symbols = ["☉", "??", "♁", "??", "??", "??", "Λ0", "∞"]
        self.collected: Dict[str, float] = {}
        self.interval_sec = 60
        self.last_record_time = 0
        self.network_activity = 1.0
        self.analyzer = ResonanceAnalyzer()
        self.thresholds = {"cpu": 80.0, "memory": 80.0, "disk": 90.0}
        self.load_state()

    def load_state(self):
        """Загружает состояние с расшифровкой."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "rb") as f:
                    data = self.cipher.decrypt(f.read())
                    self.collected = json.loads(data)
            except Exception as e:
                self.log_event(f"[!] Ошибка загрузки состояния: {e}")
                self.collected = {}

    def validate_symbol(self, symbol: str) -> bool:
        """Проверяет допустимость символа."""
        return symbol in self.valid_symbols

    def update_network_activity(self, activity: float):
        """Обновляет интервал сканирования на основе активности."""
        self.network_activity = max(0.1, min(activity, 10.0))
        self.interval_sec = max(30, min(120, 60 / self.network_activity))
        self.log_event(f"[INFO] Network activity updated: {self.network_activity}, interval={self.interval_sec}s")

    def scan(self, symbol: str = "Λ0") -> bool:
        """Собирает метрики воздействия."""
        now = time.time()
        if now - self.last_record_time < self.interval_sec:
            self.log_event("[!] Слишком частое сканирование")
            return False
        self.last_record_time = now

        if not self.validate_symbol(symbol):
            self.log_event(f"[!] Недопустимый символ: {symbol}")
            return False

        # Сбор метрик
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        net = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
        temp = psutil.sensors_temperatures() if hasattr(psutil, "sensors_temperatures") else {}

        # Адаптивная коррекция для Λ0
        adjustment = 1.2 if symbol == self.lambda_zero else 1.0

        impact = {
            "timestamp": now,
            "symbol": symbol,
            "cpu": round(cpu * adjustment, 2),
            "memory": round(mem * adjustment, 2),
            "disk": round(disk * adjustment, 2),
            "network_bytes": net,
            "thermal_zones": {k: [round(t.current, 2) for t in v] for k, v in temp.items()} if temp else {}
        }

        # Проверка аномалий
        anomalies = []
        if impact["cpu"] > self.thresholds["cpu"]:
            anomalies.append(f"CPU={impact['cpu']}%")
        if impact["memory"] > self.thresholds["memory"]:
            anomalies.append(f"MEM={impact['memory']}%")
        if impact["disk"] > self.thresholds["disk"]:
            anomalies.append(f"DISK={impact['disk']}%")

        # Интеграция с resonance_analyzer
        resonance = self.analyzer.analyze(symbol, 7.83 if symbol == self.lambda_zero else 1.618, 0.0)
        impact["resonance_score"] = resonance["resonance"]

        self.collected[str(int(now))] = impact
        self.save_state()

        log_message = f"Impact: CPU={impact['cpu']}%, MEM={impact['memory']}%, Symbol={symbol}, Resonance={resonance['resonance']:.4f}"
        if anomalies:
            log_message += f", Anomalies: {', '.join(anomalies)}"
        self.log_event(log_message)
        return True

    def save_state(self):
        """Сохраняет состояние с шифрованием."""
        data = json.dumps(self.collected, indent=2).encode()
        encrypted = self.cipher.encrypt(data)
        with open(self.state_file, "wb") as f:
            f.write(encrypted)

    def log_event(self, message: str):
        """Логирует событие."""
        log = {
            "event": "env_impact",
            "message": message,
            "timestamp": time.time()
        }
        encrypted = self.cipher.encrypt(json.dumps(log).encode() + b"\n")
        with open(self.log_file, "ab") as f:
            f.write(encrypted)

    def get_latest_impact(self) -> Dict:
        """Возвращает последнюю запись."""
        if self.collected:
            return list(self.collected.values())[-1]
        return {}

if __name__ == "__main__":
    tracker = EnvImpactTracker()
    tracker.update_network_activity(2.0)
    if tracker.scan(symbol="Λ0"):
        print("Последнее воздействие:", json.dumps(tracker.get_latest_impact(), indent=2))
    else:
        print("Ожидание интервала между сканами...")
```

---

## FILE: `/root/logos_lrb/modules/external_phase_broadcaster.rs`

```rs
//! Внешний широковещатель фаз: AEAD XChaCha20-Poly1305 + Ed25519 подпись.

use lrb_core::crypto::AeadBox;
use ed25519_dalek::{SigningKey, VerifyingKey, Signature, Signer, Verifier};
use anyhow::Result;

pub struct PhaseBroadcaster {
    aead: AeadBox,
    self_vk: VerifyingKey,
}

impl PhaseBroadcaster {
    pub fn new(key32: [u8;32], self_vk: VerifyingKey) -> Self {
        Self { aead: AeadBox::from_key(&key32), self_vk }
    }

    pub fn pack(&self, signer: &SigningKey, topic: &[u8], payload: &[u8]) -> Result<Vec<u8>> {
        let mut aad = Vec::with_capacity(topic.len()+32);
        aad.extend_from_slice(topic);
        aad.extend_from_slice(self.self_vk.as_bytes());

        let sealed = self.aead.seal(&aad, payload);
        let sig = signer.sign(&sealed);

        let mut out = Vec::with_capacity(64 + sealed.len());
        out.extend_from_slice(sig.as_ref());
        out.extend_from_slice(&sealed);
        Ok(out)
    }

    pub fn unpack(&self, sender_vk: &VerifyingKey, topic: &[u8], data: &[u8]) -> Result<Vec<u8>> {
        if data.len() < 64+24+16 { anyhow::bail!("phase_bcast: short"); }
        let (sig_bytes, sealed) = data.split_at(64);
        let sig = Signature::from_bytes(sig_bytes)?;
        sender_vk.verify_strict(sealed, &sig).map_err(|_| anyhow::anyhow!("phase_bcast: bad signature"))?;

        let mut aad = Vec::with_capacity(topic.len()+32);
        aad.extend_from_slice(topic);
        aad.extend_from_slice(self.self_vk.as_bytes());

        let pt = self.aead.open(&aad, sealed)?;
        Ok(pt)
    }
}
```

---

## FILE: `/root/logos_lrb/modules/external_phase_link.rs`

```rs
//! Безопасная версия external_phase_link без unsafe-кастов.
//! Состояние защищено через RwLock. Однопоточная производительность сохраняется.

use std::sync::{Arc, RwLock};
use anyhow::Result;

#[derive(Default, Clone, Debug)]
pub struct PhaseState {
    pub last_tick_ms: u64,
    pub phase_strength: f32,
}

#[derive(Clone)]
pub struct ExternalPhaseLink {
    state: Arc<RwLock<PhaseState>>,
}

impl ExternalPhaseLink {
    pub fn new() -> Self {
        Self { state: Arc::new(RwLock::new(PhaseState::default())) }
    }

    pub fn tick(&self, now_ms: u64, input_strength: f32) -> Result<()> {
        let mut st = self.state.write().expect("rwlock poisoned");
        st.last_tick_ms = now_ms;
        st.phase_strength = 0.9 * st.phase_strength + 0.1 * input_strength;
        Ok(())
    }

    pub fn snapshot(&self) -> PhaseState {
        self.state.read().expect("rwlock poisoned").clone()
    }
}
```

---

## FILE: `/root/logos_lrb/modules/genesis_fragment_seeds.rs`

```rs
//! Genesis Fragment Seeds: шифрованное хранение фрагментов seed.

use lrb_core::crypto::AeadBox;
use ed25519_dalek::{SigningKey, VerifyingKey, Signature, Signer, Verifier};
use anyhow::Result;

pub struct SeedVault { aead:AeadBox, self_vk:VerifyingKey }

impl SeedVault {
    pub fn new(key32:[u8;32], self_vk:VerifyingKey) -> Self { Self{ aead:AeadBox::from_key(&key32), self_vk } }

    pub fn pack_fragment(&self, signer:&SigningKey, label:&[u8], fragment:&[u8]) -> Result<Vec<u8>> {
        let mut aad=Vec::with_capacity(label.len()+32); aad.extend_from_slice(label); aad.extend_from_slice(self.self_vk.as_bytes());
        let sealed=self.aead.seal(&aad, fragment); let sig=signer.sign(&sealed);
        let mut out=Vec::with_capacity(64+sealed.len()); out.extend_from_slice(sig.as_ref()); out.extend_from_slice(&sealed); Ok(out)
    }

    pub fn unpack_fragment(&self, sender_vk:&VerifyingKey, label:&[u8], data:&[u8]) -> Result<Vec<u8>> {
        if data.len()<64+24+16 { anyhow::bail!("seed_vault: short"); }
        let(sig_bytes,sealed)=data.split_at(64); let sig=Signature::from_bytes(sig_bytes)?;
        sender_vk.verify_strict(sealed,&sig).map_err(|_|anyhow::anyhow!("seed_vault: bad sig"))?;
        let mut aad=Vec::with_capacity(label.len()+32); aad.extend_from_slice(label); aad.extend_from_slice(self.self_vk.as_bytes());
        Ok(self.aead.open(&aad, sealed)?)
    }
}
```

---

## FILE: `/root/logos_lrb/modules/go_to_market.yaml`

```yaml
yaml
version: 1.1
created: 2025-07-05
authors:
  - LOGOS Core Dev Team

valid_symbols: ["Λ0", "☉", "??", "♁", "??", "??", "??", "∞"]

launch_phases:
  - name: "Genesis Outreach"
    target: "Ранние сторонники, идеологические участники"
    duration_days: 14
    required_symbol: "Λ0"
    focus:
      - "Ритуальные миссии через ritual_quest.py"
      - "Формирование 81 ключевого RID"
      - "Публичное представление Λ0"
    channels:
      - "Telegram: logos_community_channel"
      - "Discord: logos_resonance_server"
      - "GitHub Issues: logos_network/repo"
    metrics:
      - "Количество валидных RID (rid_builder.py)"
      - "Реакция в resonance_feedback.py"
      - "DAO-активность (community_dao.yaml)"
    test_campaign:
      name: "simulate_genesis_outreach"
      description: "Эмуляция подключения 81 RID"

  - name: "LGN Liquidity Phase"
    target: "DEX и CEX листинг"
    duration_days: 30
    required_symbol: "any"
    focus:
      - "Запуск rLGN_converter.py"
      - "Добавление пары LGN/USDT"
      - "Обратная конвертация через DAO-гранты"
    exchanges:
      - "Uniswap: ERC-20 pair"
      - "MEXC: LGN/USDT"
      - "Gate.io: LGN/USDT"
    metrics:
      - "Объем торговли LGN"
      - "Задержки rLGN → LGN (rLGN_converter.py)"
      - "Количество DAO-кейсов (community_dao.yaml)"
    test_campaign:
      name: "simulate_liquidity_launch"
      description: "Эмуляция листинга на DEX/CEX"

  - name: "Main Resonance"
    target: "Массовый пользователь"
    duration_days: 90
    required_symbol: "any"
    focus:
      - "Образование: resonance_tutor.py"
      - "Фаза доверия: onboarding_ui.py"
      - "Публичные голосования в community_dao.yaml"
    regions:
      - name: "RU"
        languages: ["ru"]
      - name: "EU"
        languages: ["en", "de", "fr"]
      - name: "LATAM"
        languages: ["es", "pt"]
    metrics:
      - "Количество успешных входов в Σ(t) (onboarding_sim.py)"
      - "Активность в rituals (ritual_quest.py)"
      - "Обратная связь (resonance_feedback.py)"
    test_campaign:
      name: "simulate_mass_adoption"
      description: "Эмуляция 1000+ входов пользователей"

education_plan:
  modules:
    - "resonance_tutor.py"
    - "onboarding_ui.py"
    - "logos_ethics.md"
  campaigns:
    - name: "Enter the Phase"
      platform: "YouTube"
      type: "Анимированное видео"
      languages: ["en", "ru", "es"]
    - name: "RID Drop"
      platform: "Twitter"
      type: "Раздача RID с фазовыми квестами"
      languages: ["en", "ru", "es"]

integration_targets:
  wallets:
    - name: "TrustWallet"
      status: "Negotiation"
    - name: "Metamask"
      status: "Planned"
  blockchains:
    - "Ethereum (via symbolic_bridge.rs)"
    - "Polkadot"
    - "Cosmos"
  bridges:
    - "symbolic_bridge.rs"
    - "legacy_migrator.rs"

tracking:
  dashboard: "resonance_analytics_frontend"
  metrics:
    - rid_growth
    - lgn_volume
    - rlg_conversion_rate
    - dao_participation
  log_encryption:
    enabled: true
    encryption_key: "generate_at_runtime"  # AES-256

dao_support:
  proposals_enabled: true
  voting_required: true
  quorum: 0.33
  budget_lgn: 10888.0
  update_frequency_days: 14
```

---

## FILE: `/root/logos_lrb/modules/heartbeat_monitor.rs`

```rs
//! Heartbeat Monitor — безопасные heartbeat-кадры между узлами (AEAD+подпись).

use lrb_core::crypto::AeadBox;
use ed25519_dalek::{SigningKey, VerifyingKey, Signature, Signer, Verifier};
use anyhow::Result;

#[derive(Clone)]
pub struct HeartbeatMonitor { aead:AeadBox, self_vk:VerifyingKey }

impl HeartbeatMonitor {
    pub fn new(key32:[u8;32], self_vk:VerifyingKey) -> Self { Self{ aead:AeadBox::from_key(&key32), self_vk } }

    pub fn encode_ping(&self, signer:&SigningKey, channel:&[u8], payload:&[u8]) -> Result<Vec<u8>> {
        let mut aad=Vec::with_capacity(channel.len()+32); aad.extend_from_slice(channel); aad.extend_from_slice(self.self_vk.as_bytes());
        let sealed=self.aead.seal(&aad, payload); let sig=signer.sign(&sealed);
        let mut out=Vec::with_capacity(64+sealed.len()); out.extend_from_slice(sig.as_ref()); out.extend_from_slice(&sealed); Ok(out)
    }

    pub fn decode_frame(&self, sender_vk:&VerifyingKey, channel:&[u8], data:&[u8]) -> Result<Vec<u8>> {
        if data.len()<64+24+16 { anyhow::bail!("heartbeat: short frame"); }
        let(sig_bytes,sealed)=data.split_at(64); let sig=Signature::from_bytes(sig_bytes)?;
        sender_vk.verify_strict(sealed,&sig).map_err(|_|anyhow::anyhow!("heartbeat: bad signature"))?;
        let mut aad=Vec::with_capacity(channel.len()+32); aad.extend_from_slice(channel); aad.extend_from_slice(self.self_vk.as_bytes());
        Ok(self.aead.open(&aad, sealed)?)
    }
}
```

---

## FILE: `/root/logos_lrb/modules/legacy_migrator.rs`

```rs
//! Legacy Migrator: перенос артефактов со шифрованием и подписью.

use lrb_core::crypto::AeadBox;
use ed25519_dalek::{SigningKey, VerifyingKey, Signature, Signer, Verifier};
use anyhow::Result;

pub struct LegacyMigrator { aead:AeadBox, self_vk:VerifyingKey }

impl LegacyMigrator {
    pub fn new(key32:[u8;32], self_vk:VerifyingKey) -> Self { Self{ aead:AeadBox::from_key(&key32), self_vk } }

    pub fn wrap_blob(&self, signer:&SigningKey, kind:&[u8], blob:&[u8]) -> Result<Vec<u8>> {
        let mut aad=Vec::with_capacity(kind.len()+32); aad.extend_from_slice(kind); aad.extend_from_slice(self.self_vk.as_bytes());
        let sealed=self.aead.seal(&aad, blob); let sig=signer.sign(&sealed);
        let mut out=Vec::with_capacity(64+sealed.len()); out.extend_from_slice(sig.as_ref()); out.extend_from_slice(&sealed); Ok(out)
    }

    pub fn unwrap_blob(&self, sender_vk:&VerifyingKey, kind:&[u8], data:&[u8]) -> Result<Vec<u8>> {
        if data.len()<64+24+16 { anyhow::bail!("legacy_migrator: short"); }
        let(sig_bytes,sealed)=data.split_at(64); let sig=Signature::from_bytes(sig_bytes)?;
        sender_vk.verify_strict(sealed,&sig).map_err(|_|anyhow::anyhow!("legacy_migrator: bad sig"))?;
        let mut aad=Vec::with_capacity(kind.len()+32); aad.extend_from_slice(kind); aad.extend_from_slice(self.self_vk.as_bytes());
        Ok(self.aead.open(&aad, sealed)?)
    }
}
```

---

## FILE: `/root/logos_lrb/modules/maintenance_strategy.yaml`

```yaml
yaml
version: 1.1
created: 2025-07-05
authors:
  - LOGOS Core Dev Team

valid_symbols: ["Λ0", "☉", "??", "♁", "??", "??", "??", "∞"]

update_channels:
  - name: stable
    description: "Проверенные обновления, подписанные DAO"
    auto_deploy: false
    approval_required: true
    required_symbol: "Λ0"
  - name: beta
    description: "Тестирование новых модулей и интеграций"
    auto_deploy: true
    approval_required: false
    required_symbol: "any"
  - name: dev
    description: "Экспериментальная среда для новых функций"
    auto_deploy: true
    approval_required: false
    required_symbol: "any"

rotation_policy:
  modules:
    restart_interval_sec:
      default: 86400  # 24 часа
      adaptive:
        enabled: true
        network_activity_thresholds:
          low: { value: 172800, activity: 0.5 }  # 48 часов при низкой активности
          high: { value: 43200, activity: 5.0 }  # 12 часов при высокой
    max_failure_before_isolation: 3
    isolation_mode:
      enabled: true
      trigger_modules:
        - "rcp_engine.rs"
        - "phase_scaler.rs"
        - "resonance_analyzer.py"
      test_scenarios:
        - name: "simulate_module_failure"
          description: "Эмуляция отказа 3+ модулей"

lifecycle_hooks:
  pre_restart:
    - "backup_state with phase_backup.rs"
    - "notify_admins via telegram and email"
  post_restart:
    - "verify Σ(t) with phase_integrity.rs"
    - "send heartbeat to dao_monitor via community_dao.yaml"

compatibility_matrix:
  required_versions:
    rust: ">=1.74"
    python: ">=3.10"
    cargo: ">=1.70"
    serde_json: ">=1.0.96"
    ring: ">=0.17"

auto_patch:
  enabled: true
  modules_included:
    - "resonance_feedback.py"
    - "onboarding_ui.py"
    - "symbolic_firewall.rs"
  security_only: false
  max_patches_per_day: 3

release_schedule:
  cadence: "monthly"
  last_release: "2025-06-30"
  next_scheduled: "2025-07-31"
  lgn_budget_reserved: 888.0

logs:
  directory: "logs/maintenance/"
  encrypted: true
  encryption_key: "generate_at_runtime"  # AES-256
  notify_admins:
    channels:
      - telegram: "logos_maintenance_channel"
      - email: "alerts@logos.network"
  backup_to: "phase_backup.rs"
```

---

## FILE: `/root/logos_lrb/modules/resonance_analytics_frontend.tsx`

```tsx
tsx
// LOGOS Resonance Analytics Frontend
// Автор: LOGOS Core Dev

import React, { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { Alert, AlertDescription } from "@/components/ui/alert";

interface SigmaData {
  timestamp: number;
  sigma: number;
  symbol?: string; // Для Λ0
}

export default function ResonanceAnalytics() {
  const [data, setData] = useState<SigmaData[]>([]);
  const [timestamp, setTimestamp] = useState(0);
  const [latestSigma, setLatestSigma] = useState<number | null>(null);
  const [activityLevel, setActivityLevel] = useState("stable");
  const [error, setError] = useState<string | null>(null);
  const lambdaZero = "Λ0";

  useEffect(() => {
    const interval = setInterval(() => {
      fetch("/api/sigma", {
        headers: { Authorization: `Bearer ${process.env.REACT_APP_API_TOKEN}` }, // Токен для безопасности
      })
        .then((res) => {
          if (!res.ok) throw new Error(`HTTP error: ${res.status}`);
          return res.json();
        })
        .then((json) => {
          // Валидация данных
          if (!json || typeof json.timestamp !== "number" || typeof json.sigma !== "number") {
            throw new Error("Invalid API response");
          }
          const validatedData: SigmaData = {
            timestamp: json.timestamp,
            sigma: json.sigma,
            symbol: json.symbol || "unknown",
          };
          setData((prev) => [...prev.slice(-99), validatedData]);
          setTimestamp(json.timestamp);
          setLatestSigma(json.sigma);
          setActivityLevel(json.sigma > 5.0 ? "high" : json.sigma < -5.0 ? "low" : "stable");
          logEvent(`[FETCH] Sigma=${json.sigma}, Symbol=${json.symbol || "none"}`);
          setError(null);
        })
        .catch((err) => {
          setError(`Ошибка загрузки данных: ${err.message}`);
          logEvent(`[ERROR] Fetch failed: ${err.message}`);
        });
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  const logEvent = (message: string) => {
    // Логирование для resonance_analyzer.py
    const entry = {
      event: "resonance_analytics",
      message,
      timestamp: Math.floor(Date.now() / 1000),
    };
    // Предполагается, что логи отправляются в API или файл
    fetch("/api/log", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(entry),
    }).catch((err) => console.error("Log error:", err));
  };

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-xl font-bold">Resonance Σ(t) Monitoring</h1>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <Card>
        <CardContent className="p-4 space-y-2">
          <p className="text-sm text-muted-foreground">
            Последняя фаза: <strong>{latestSigma?.toFixed(4) ?? "N/A"}</strong>
          </p>
          <p className="text-sm">
            Активность сети: <span className="font-semibold">{activityLevel}</span>
          </p>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="timestamp"
                tickFormatter={(ts) => new Date(ts * 1000).toLocaleTimeString()}
              />
              <YAxis domain={[-10, 10]} />
              <Tooltip
                labelFormatter={(ts) => new Date(ts * 1000).toLocaleString()}
                formatter={(value: number, name: string, props: any) => [
                  value.toFixed(4),
                  props.payload.symbol === lambdaZero ? "Λ0 Sigma" : "Sigma",
                ]}
              />
              <Line
                type="monotone"
                dataKey="sigma"
                stroke={(d) => (d.symbol === lambdaZero ? "#FFD700" : "#8884d8")}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <div className="flex justify-end">
        <Button onClick={() => {
          setData([]);
          logEvent("[RESET] График очищен");
        }}>
          Очистить график
        </Button>
      </div>
    </div>
  );
}

```

---

## FILE: `/root/logos_lrb/modules/resonance_emergency_plan.yaml`

```yaml
yaml
version: 1.1
created: 2025-07-05
authors:
  - LOGOS Core Dev Team

valid_symbols: ["Λ0", "☉", "??", "♁", "??", "??", "??", "∞"]

critical_conditions:
  - id: PHASE-DROP
    name: "Резкое падение Σ(t)"
    detection_module: "phase_integrity.rs"
    response:
      - "Заморозить входящие транзакции (tx_spam_guard.rs)"
      - "Активировать phase_stabilizer.rs для восстановления Σ(t)"
      - "Рассылка сигнала Λ0 через beacon_emitter.rs"
    required_symbol: "Λ0"

  - id: BIOSPHERE-ALERT
    name: "Аномалия биосферы"
    detection_module: "biosphere_scanner.rs"
    response:
      - "Отключить усилители в resonance_math.rs"
      - "Снизить частоту вещания до 1.618 Hz"
      - "Сбор данных через resonance_feedback.py"
    required_symbol: "any"

  - id: DISSONANT-SYMBOL-ATTACK
    name: "Фазовая атака через недопустимые символы"
    detection_module: "symbolic_firewall.rs"
    response:
      - "Блокировка offending RID через tx_spam_guard.rs"
      - "Отзыв до 50% LGN через lgn_recall.rs"
      - "Фиксация в logs/emergency_dissonance.json"
    required_symbol: "Λ0"

  - id: NETWORK-OVERCLOCK
    name: "Перегрузка Σ(t) по частоте"
    detection_module: "dynamic_balance.rs"
    response:
      - "Увеличить LGN_cost вдвое в dynamic_balance.rs"
      - "Активация phase_scaler.rs для ребалансировки"
      - "Оповещение DAO через community_dao.yaml"
    required_symbol: "Λ0"

  - id: CRITICAL-CHAOS
    name: "Сбой более 70% узлов"
    detection_module: "phase_intercept_guard.rs"
    response:
      - "Переход в фазу auto_init_from_Λ0.py"
      - "Сброс Σ(t) до базового уровня (7.83 Hz)"
      - "Созыв DAO-кворума с 25% порогом"
    required_symbol: "Λ0"
    test_scenario: "simulate_70_percent_node_failure"

fallback_actions:
  if_logos_core_fails:
    - "Изоляция Λ0 ядра через genesis_fragment_seeds.rs"
    - "Включение аварийной цепочки backup_nodes.json"
    - "Восстановление через phase_backup.rs"
  if_feedback_shows_harm:
    - "Полное торможение Σ(t) в phase_stabilizer.rs"
    - "Миграция в low-resonance режим (1.618 Hz)"
    - "Обратный отчёт в DAO через resonance_feedback.py"

logs:
  directory: "logs/emergency/"
  encrypted: true
  encryption_key: "generate_at_runtime"  # AES-256
  notify_admins:
    channels:
      - telegram: "logos_emergency_channel"
      - email: "alerts@logos.network"

check_interval_sec:
  default: 60
  adaptive:
    enabled: true
    network_activity_thresholds:
      low: { value: 120, activity: 0.5 }
      high: { value: 30, activity: 5.0 }

rcp_override_allowed: false

test_scenarios:
  - name: "simulate_70_percent_node_failure"
    description: "Эмуляция сбоя 70% узлов для проверки CRITICAL-CHAOS"
    module: "phase_intercept_guard.rs"
  - name: "simulate_biosphere_anomaly"
    description: "Эмуляция аномалии биосферы для BIOSPHERE-ALERT"
    module: "biosphere_scanner.rs"
```

---

## FILE: `/root/logos_lrb/modules/resonance_meshmap.yaml`

```yaml
yaml
version: 1.1
generated: 2025-07-05
source: "phase_scaler.rs"

valid_symbols: ["Λ0", "☉", "??", "♁", "??", "??", "??", "∞"]

symbol_map:
  Λ0:
    color: "#FFD700"
    role: "Core synchronizer"
  ☉:
    color: "#FFA500"
    role: "Harmonizer"
  ??:
    color: "#FF4500"
    role: "Initiator"
  ♁:
    color: "#33CC33"
    role: "Stabilizer"
  ??:
    color: "#3399FF"
    role: "Flux"
  ??:
    color: "#996633"
    role: "Grounding"
  ??:
    color: "#AAAAAA"
    role: "Air flow"
  ∞:
    color: "#CCCCCC"
    role: "Infinity"

clusters:
  CLUSTER_7.830:
    label: "Schumann Core"
    max_nodes: 144
    active_nodes:
      - rid: "Λ0@7.83Hzφ0.000"
        joined: 2025-07-05T10:00:00Z
      - rid: "☉@7.83Hzφ0.4142"
        joined: 2025-07-05T10:01:03Z
    center_phase: 0.2
    symbol_dominance: "Λ0"
    overload_action: "Activate phase_scaler.rs rebalance"

  CLUSTER_432.000:
    label: "Harmonic Field"
    max_nodes: 288
    active_nodes:
      - rid: "??@432Hzφ-0.618"
        joined: 2025-07-05T10:02:44Z
      - rid: "♁@432Hzφ0.309"
        joined: 2025-07-05T10:04:12Z
    center_phase: -0.14
    symbol_dominance: "??"
    overload_action: "Activate phase_scaler.rs rebalance"

  CLUSTER_1.618:
    label: "Golden Mesh"
    max_nodes: 81
    active_nodes:
      - rid: "??@1.618Hzφ0.707"
        joined: 2025-07-05T10:08:00Z
    center_phase: 0.6
    symbol_dominance: "??"
    overload_action: "Activate phase_scaler.rs rebalance"

summary:
  total_clusters: 3
  total_active_rids: 5
  symbol_distribution:
    Λ0: 1
    ☉: 1
    ??: 1
    ♁: 1
    ??: 1

log_config:
  file: "resonance_meshmap_log.json"
  encrypted: true
  encryption_key: "generate_at_runtime"  # AES-256

update_config:
  enabled: true
  update_interval_sec: 300  # Каждые 5 минут
  modules:
    - "phase_scaler.rs"
    - "resonance_analyzer.py"
```

---

## FILE: `/root/logos_lrb/modules/resonance_tutor.py`

```py
# LOGOS Resonance Tutor
# Автор: LOGOS Core Dev

import time
import random
import json
import os
from typing import Dict
from cryptography.fernet import Fernet

class ResonanceTutor:
    def __init__(self):
        self.valid_symbols = {
            "☉": "Гармонизатор (Солнце) — баланс и инициатива.",
            "??": "Огонь — активное действие и импульс.",
            "♁": "Материя — плотность, привязка к реальности.",
            "??": "Вода — текучесть, перемены.",
            "??": "Земля — устойчивость и форма.",
            "??": "Воздух — связь и движение.",
            "Λ0": "Центральный символ. Начало всего. Не принадлежит никому.",
            "∞": "Бесконечность. Переход к высшим фазам."
        }
        self.freqs = [7.83, 1.618, 432.0, 864.0]
        self.log_file = "resonance_tutor_log.json"
        self.cipher = Fernet(Fernet.generate_key())
        self.progress = []
        self.run()

    def run(self):
        print("?? Добро пожаловать в обучающую систему LOGOS Resonance Tutor")
        self.log_event("Начало обучения")
        self.pause("Нажмите Enter, чтобы начать...")

        self.explain_symbols()
        self.explain_frequencies()
        self.explain_phase()
        self.explain_rid()
        self.explain_sigma()
        self.run_mini_test()
        self.final_message()

    def explain_symbols(self):
        print("\n?? Символы в LOGOS — это не просто знаки.")
        print("Они — архетипы. Смысловые структуры.")
        for s, desc in self.valid_symbols.items():
            print(f"  {s}: {desc}")
        self.progress.append({"step": "symbols", "completed": True})
        self.log_event("Объяснены символы")
        self.pause("→ Продолжить")

    def explain_frequencies(self):
        print("\n?? Частоты используются в LOGOS вместо хэшей.")
        print("Каждое действие связано с гармоникой:")
        for f in self.freqs:
            label = {
                7.83: "Шуман-резонанс Земли",
                1.618: "Золотое сечение",
                432.0: "Музыкальная гармония",
                864.0: "Частота Солнца"
            }.get(f, "Неизвестно")
            print(f"  {f} Hz — {label}")
        self.progress.append({"step": "frequencies", "completed": True})
        self.log_event("Объяснены частоты")
        self.pause("→ Дальше")

    def explain_phase(self):
        print("\n?? Фаза (φ) — положение во времени.")
        print("Фаза измеряется в радианах от -π до +π.")
        print("Она влияет на то, как ваш RID взаимодействует с Σ(t).")
        self.progress.append({"step": "phase", "completed": True})
        self.log_event("Объяснена фаза")
        self.pause("→ Понял")

    def explain_rid(self):
        symbol = random.choice(list(self.valid_symbols.keys()))
        freq = random.choice(self.freqs)
        phase = round(random.uniform(-3.14, 3.14), 4)
        rid = f"{symbol}@{freq}Hzφ{phase}"
        print("\n?? Ваш резонансный идентификатор (RID) — это:")
        print(f"  {rid}")
        print("RID — это адрес в сети LOGOS, основанный на смысле.")
        self.progress.append({"step": "rid", "completed": True})
        self.log_event(f"Объяснён RID: {rid}")
        self.pause("→ Дальше")

    def explain_sigma(self):
        print("\nΣ(t) — это суммарный резонанс сети.")
        print("Он вычисляется как гармоническая сумма частот и фаз всех RID.")
        print("Ваш вклад в Σ(t) — это ваш резонанс.")
        self.progress.append({"step": "sigma", "completed": True})
        self.log_event("Объяснён Σ(t)")
        self.pause("→ Продолжить")

    def run_mini_test(self):
        print("\n?? Мини-тест: выберите правильную частоту для Λ0")
        options = [7.83, 100.0, 0.0, 5000.0]
        correct = 7.83
        random.shuffle(options)
        for i, opt in enumerate(options, 1):
            print(f"{i}. {opt} Hz")
        choice = int(input("Ваш выбор (1-4): "))
        selected = options[choice - 1]
        if selected == correct:
            print("✅ Правильно! 7.83 Hz — Шуман-резонанс.")
            self.progress.append({"step": "mini_test", "result": "success"})
            self.log_event("Мини-тест пройден успешно")
        else:
            print(f"❌ Неверно. Правильный ответ: 7.83 Hz (Шуман-резонанс).")
            self.progress.append({"step": "mini_test", "result": "failed"})
            self.log_event(f"Мини-тест провален: выбрано {selected} Hz")
        self.pause("→ Завершить")

    def final_message(self):
        print("\n✅ Вы завершили вводный курс.")
        print("Теперь вы можете войти в резонанс через onboarding_sim.py или onboarding_ui.py.")
        print("?? Увидимся в Σ(t).")
        self.log_event("Обучение завершено")
        print("Для практики запустите: python onboarding_sim.py")

    def log_event(self, message: str):
        """Логирует событие в файл."""
        log_entry = {
            "event": "resonance_tutor",
            "message": message,
            "timestamp": time.time()
        }
        encrypted = self.cipher.encrypt(json.dumps(log_entry).encode() + b"\n")
        with open(self.log_file, "ab") as f:
            f.write(encrypted)

    def pause(self, prompt: str):
        input(f"\n{prompt}")

if __name__ == "__main__":
    ResonanceTutor()
```

---

## FILE: `/root/logos_lrb/modules/ritual_engine.rs`

```rs
//! Ritual Engine: доставка «ритуальных» сообщений c фазовой меткой, AEAD+подпись.

use lrb_core::crypto::AeadBox;
use ed25519_dalek::{SigningKey, VerifyingKey, Signature, Signer, Verifier};
use anyhow::Result;

pub struct RitualEngine { aead:AeadBox, self_vk:VerifyingKey }

impl RitualEngine {
    pub fn new(key32:[u8;32], self_vk:VerifyingKey) -> Self { Self{ aead:AeadBox::from_key(&key32), self_vk } }

    pub fn send(&self, signer:&SigningKey, phase_id:&[u8], msg:&[u8]) -> Result<Vec<u8>> {
        let mut aad=Vec::with_capacity(phase_id.len()+32); aad.extend_from_slice(phase_id); aad.extend_from_slice(self.self_vk.as_bytes());
        let sealed=self.aead.seal(&aad, msg); let sig=signer.sign(&sealed);
        let mut out=Vec::with_capacity(64+sealed.len()); out.extend_from_slice(sig.as_ref()); out.extend_from_slice(&sealed); Ok(out)
    }

    pub fn recv(&self, sender_vk:&VerifyingKey, phase_id:&[u8], data:&[u8]) -> Result<Vec<u8>> {
        if data.len()<64+24+16 { anyhow::bail!("ritual_engine: short"); }
        let(sig_bytes,sealed)=data.split_at(64); let sig=Signature::from_bytes(sig_bytes)?;
        sender_vk.verify_strict(sealed,&sig).map_err(|_|anyhow::anyhow!("ritual_engine: bad sig"))?;
        let mut aad=Vec::with_capacity(phase_id.len()+32); aad.extend_from_slice(phase_id); aad.extend_from_slice(self.self_vk.as_bytes());
        Ok(self.aead.open(&aad, sealed)?)
    }
}
```

---

## FILE: `/root/logos_lrb/modules/symbolic_parser.py`

```py
# LOGOS Symbolic Parser
# Автор: LOGOS Core Dev

import re
import math
from typing import List, Dict, Optional
from cryptography.fernet import Fernet
import json
import time

class SymbolicParser:
    def __init__(self):
        self.valid_symbols = ["Λ0", "☉", "??", "♁", "??", "??", "??", "∞"]
        self.lambda_zero = "Λ0"
        self.pattern = re.compile(r"(?P<symbol>[☉??♁??????Λ0∞])@(?P<freq>[0-9\.]+)Hzφ(?P<phase>[-0-9\.]+)")
        self.log_file = "symbolic_parser_log.json"
        self.cipher = Fernet(Fernet.generate_key())
        self.rid_cache: Dict[str, Dict] = {}  # Кэш для RID

    def extract_rids(self, text: str) -> List[str]:
        """Находит все валидные RID в тексте."""
        matches = self.pattern.findall(text)
        rids = [f"{m[0]}@{m[1]}Hzφ{m[2]}" for m in matches if m[0] in self.valid_symbols]
        self.log_event(f"[EXTRACT] Найдено {len(rids)} RID: {rids}")
        return rids

    def parse_rid(self, rid: str) -> Optional[Dict]:
        """Парсит одиночный RID в структуру."""
        # Проверка кэша
        if rid in self.rid_cache:
            self.log_event(f"[CACHE] RID {rid} из кэша")
            return self.rid_cache[rid]

        try:
            match = self.pattern.match(rid)
            if not match:
                self.log_event(f"[!] Неверный формат RID: {rid}")
                return None

            symbol = match.group("symbol")
            if symbol not in self.valid_symbols:
                self.log_event(f"[!] Недопустимый символ: {symbol}")
                return None

            freq = float(match.group("freq"))
            phase = float(match.group("phase"))

            # Проверка диапазонов
            if not (0.1 <= freq <= 10000.0):
                self.log_event(f"[!] Недопустимая частота: {freq}")
                return None
            if not (-math.pi <= phase <= math.pi):
                self.log_event(f"[!] Недопустимая фаза: {phase}")
                return None

            # Проверка через RCP (заглушка)
            if not self.validate_with_rcp(symbol, freq, phase):
                self.log_event(f"[!] RCP не подтвердил RID: {rid}")
                return None

            result = {
                "symbol": symbol,
                "frequency": freq,
                "phase": phase,
                "is_lambda_zero": symbol == self.lambda_zero
            }
            self.rid_cache[rid] = result
            self.log_event(f"[PARSE] Успешно разобран RID: {rid}")
            return result
        except Exception as e:
            self.log_event(f"[!] Ошибка разбора RID: {e}")
            return None

    def extract_symbols(self, text: str) -> List[str]:
        """Извлекает все допустимые символы в тексте."""
        symbols = [s for s in text if s in self.valid_symbols]
        if self.lambda_zero in symbols:
            symbols.insert(0, symbols.pop(symbols.index(self.lambda_zero)))  # Приоритет Λ0
        self.log_event(f"[EXTRACT] Найдено {len(symbols)} символов: {symbols}")
        return symbols

    def validate_rid_format(self, rid: str) -> bool:
        """Проверяет соответствие RID формату."""
        result = bool(self.parse_rid(rid))
        self.log_event(f"[VALIDATE] RID {rid} {'валиден' if result else 'невалиден'}")
        return result

    def validate_with_rcp(self, symbol: str, freq: float, phase: float) -> bool:
        """Заглушка для проверки через rcp_engine.rs."""
        return symbol == self.lambda_zero or (abs(freq - 7.83) < 0.1 and abs(phase) < 0.05)

    def log_event(self, message: str):
        """Логирует событие с шифрованием."""
        entry = {
            "event": "symbolic_parser",
            "message": message,
            "timestamp": time.time()
        }
        encrypted = self.cipher.encrypt(json.dumps(entry).encode() + b"\n")
        with open(self.log_file, "ab") as f:
            f.write(encrypted)

if __name__ == "__main__":
    parser = SymbolicParser()
    test = "Пример: ☉@432.0Hzφ0.618, Λ0@7.83Hzφ0.0 и ♁@1.618Hzφ-0.314"
    rids = parser.extract_rids(test)
    print("Найденные RID:", rids)
    for r in rids:
        parsed = parser.parse_rid(r)
        print("Разбор:", parsed)
```

---

## FILE: `/root/logos_lrb/modules/uplink_controller.rs`

```rs
//! Uplink Controller: надёжная упаковка кадров uplink → core.

use lrb_core::crypto::AeadBox;
use ed25519_dalek::{SigningKey, VerifyingKey, Signature, Signer, Verifier};
use anyhow::Result;

pub struct UplinkController {
    aead: AeadBox,
    self_vk: VerifyingKey,
}

impl UplinkController {
    pub fn new(key32:[u8;32], self_vk:VerifyingKey) -> Self {
        Self { aead:AeadBox::from_key(&key32), self_vk }
    }

    pub fn encode_frame(&self, signer:&SigningKey, channel:&[u8], frame:&[u8]) -> Result<Vec<u8>> {
        let mut aad = Vec::with_capacity(channel.len()+32);
        aad.extend_from_slice(channel);
        aad.extend_from_slice(self.self_vk.as_bytes());

        let sealed = self.aead.seal(&aad, frame);
        let sig = signer.sign(&sealed);

        let mut out = Vec::with_capacity(64+sealed.len());
        out.extend_from_slice(sig.as_ref());
        out.extend_from_slice(&sealed);
        Ok(out)
    }

    pub fn decode_frame(&self, sender_vk:&VerifyingKey, channel:&[u8], data:&[u8]) -> Result<Vec<u8>> {
        if data.len() < 64+24+16 { anyhow::bail!("uplink_controller: short"); }
        let (sig_bytes, sealed) = data.split_at(64);
        let sig = Signature::from_bytes(sig_bytes)?;
        sender_vk.verify_strict(sealed, &sig).map_err(|_| anyhow::anyhow!("uplink_controller: bad signature"))?;

        let mut aad = Vec::with_capacity(channel.len()+32);
        aad.extend_from_slice(channel);
        aad.extend_from_slice(self.self_vk.as_bytes());

        Ok(self.aead.open(&aad, sealed)?)
    }
}
```

---

## FILE: `/root/logos_lrb/modules/uplink_router.rs`

```rs
//! Uplink Router: безопасная пересылка кадров между маршрутами.

use lrb_core::crypto::AeadBox;
use ed25519_dalek::{SigningKey, VerifyingKey, Signature, Signer, Verifier};
use anyhow::Result;

pub struct UplinkRouter {
    aead: AeadBox,
    self_vk: VerifyingKey,
}

impl UplinkRouter {
    pub fn new(key32:[u8;32], self_vk:VerifyingKey) -> Self {
        Self { aead:AeadBox::from_key(&key32), self_vk }
    }

    pub fn wrap(&self, signer:&SigningKey, route:&[u8], payload:&[u8]) -> Result<Vec<u8>> {
        let mut aad = Vec::with_capacity(route.len()+32);
        aad.extend_from_slice(route);
        aad.extend_from_slice(self.self_vk.as_bytes());

        let sealed = self.aead.seal(&aad, payload);
        let sig = signer.sign(&sealed);

        let mut out = Vec::with_capacity(64+sealed.len());
        out.extend_from_slice(sig.as_ref());
        out.extend_from_slice(&sealed);
        Ok(out)
    }

    pub fn unwrap(&self, sender_vk:&VerifyingKey, route:&[u8], data:&[u8]) -> Result<Vec<u8>> {
        if data.len() < 64+24+16 { anyhow::bail!("uplink_router: short"); }
        let (sig_bytes, sealed) = data.split_at(64);
        let sig = Signature::from_bytes(sig_bytes)?;
        sender_vk.verify_strict(sealed, &sig).map_err(|_| anyhow::anyhow!("uplink_router: bad signature"))?;

        let mut aad = Vec::with_capacity(route.len()+32);
        aad.extend_from_slice(route);
        aad.extend_from_slice(self.self_vk.as_bytes());

        Ok(self.aead.open(&aad, sealed)?)
    }
}
```

---

## FILE: `/root/logos_lrb/modules/x_guard/Cargo.toml`

```toml
[package]
name = "logos_x_guard"
version = "0.1.0"
edition = "2021"

[dependencies]
tokio = { workspace = true }
axum = { workspace = true }
serde = { workspace = true }
serde_json = { workspace = true }
reqwest = { workspace = true }
tracing = { workspace = true }
tracing-subscriber = { workspace = true }
anyhow = { workspace = true }
```

---

## FILE: `/root/logos_lrb/modules/x_guard/src/main.rs`

```rs
use std::{net::SocketAddr, sync::Arc, time::Duration};

use anyhow::{anyhow, Context, Result};
use axum::{
    extract::State,
    http::StatusCode,
    response::IntoResponse,
    routing::{get, post},
    Json, Router,
};
use reqwest::{Client, StatusCode as HttpStatus};
use serde::{Deserialize, Serialize};
use serde_json::Value;
use tracing::{error, info};
use tracing_subscriber::{fmt, EnvFilter};
use tracing_subscriber::prelude::*;

#[derive(Clone, Debug)]
struct XCreds {
    api_key: String,
    api_secret: String,
    bearer_token: String,
    access_token: Option<String>,
    access_token_secret: Option<String>,
}

fn read_env_required(name: &str) -> Result<String> {
    std::env::var(name).with_context(|| format!("missing env {}", name))
}

fn read_env_optional(name: &str) -> Option<String> {
    std::env::var(name).ok().filter(|v| !v.trim().is_empty())
}

fn guard_secret(name: &str, value: &str) -> Result<()> {
    let bad = ["CHANGE_ME", "changeme", "default", "", "EXAMPLE_X_API_KEY_REPLACE_ME"];
    if bad.iter().any(|b| value.eq_ignore_ascii_case(b)) {
        return Err(anyhow!(
            "{} is default/empty placeholder; refuse to start",
            name
        ));
    }
    Ok(())
}

impl XCreds {
    fn from_env() -> Result<Self> {
        let api_key = read_env_required("X_API_KEY")?;
        let api_secret = read_env_required("X_API_SECRET")?;
        let bearer_token = read_env_required("X_BEARER_TOKEN")?;

        guard_secret("X_API_KEY", &api_key)?;
        guard_secret("X_API_SECRET", &api_secret)?;
        guard_secret("X_BEARER_TOKEN", &bearer_token)?;

        let access_token = read_env_optional("X_ACCESS_TOKEN");
        let access_token_secret = read_env_optional("X_ACCESS_TOKEN_SECRET");

        Ok(Self {
            api_key,
            api_secret,
            bearer_token,
            access_token,
            access_token_secret,
        })
    }
}

#[derive(Clone)]
struct XClient {
    http: Client,
    creds: Arc<XCreds>,
    base_url: String,
}

impl XClient {
    fn new(creds: XCreds) -> Self {
        let http = Client::builder()
            .timeout(Duration::from_secs(20))
            .pool_idle_timeout(Duration::from_secs(90))
            .tcp_keepalive(Duration::from_secs(60))
            .build()
            .expect("failed to build reqwest client");

        Self {
            http,
            creds: Arc::new(creds),
            base_url: "https://api.x.com/2".to_string(),
        }
    }

    async fn get_raw(&self, path: &str, query: &[(&str, &str)]) -> Result<Value> {
        let url = format!("{}{}", self.base_url, path);
        let mut attempt: u32 = 0;

        loop {
            attempt += 1;
            let resp = self
                .http
                .get(&url)
                .query(query)
                .bearer_auth(&self.creds.bearer_token)
                .send()
                .await
                .with_context(|| format!("request to {}", url))?;

            let status = resp.status();
            let text = resp.text().await.unwrap_or_default();

            if status == HttpStatus::TOO_MANY_REQUESTS && attempt < 4 {
                let sleep_secs = 30 * attempt;
                info!(
                    "rate limited by X on {}, attempt {} -> sleep {}s",
                    url, attempt, sleep_secs
                );
                tokio::time::sleep(Duration::from_secs(sleep_secs as u64)).await;
                continue;
            }

            if status.is_server_error() && attempt < 4 {
                let backoff = 2_u64.pow(attempt);
                info!(
                    "server error from X: {} on {}, retry in {}s",
                    status, url, backoff
                );
                tokio::time::sleep(Duration::from_secs(backoff)).await;
                continue;
            }

            if !status.is_success() {
                return Err(anyhow!(
                    "X API error: status={} body={}",
                    status.as_u16(),
                    text
                ));
            }

            let json: Value = serde_json::from_str(&text)
                .with_context(|| format!("parsing JSON from {}: {}", url, text))?;
            return Ok(json);
        }
    }

    async fn get_user_by_username(&self, username: &str) -> Result<UserInfo> {
        let path = format!("/users/by/username/{}", username);
        let json = self
            .get_raw(&path, &[("user.fields", "created_at,public_metrics")])
            .await?;

        let data = json
            .get("data")
            .ok_or_else(|| anyhow!("no data in user response"))?;

        let id = data
            .get("id")
            .and_then(|v| v.as_str())
            .ok_or_else(|| anyhow!("no id in user data"))?
            .to_string();

        let uname = data
            .get("username")
            .and_then(|v| v.as_str())
            .unwrap_or(username)
            .to_string();

        let created_at = data
            .get("created_at")
            .and_then(|v| v.as_str())
            .map(|s| s.to_string());

        let followers = data
            .get("public_metrics")
            .and_then(|v| v.get("followers_count"))
            .and_then(|v| v.as_u64());

        Ok(UserInfo {
            id,
            username: uname,
            created_at,
            followers,
        })
    }

    async fn user_follows(&self, source_user_id: &str, target_user_id: &str) -> Result<bool> {
        let path = format!("/users/{}/following", source_user_id);
        let json = self
            .get_raw(&path, &[("max_results", "1000"), ("user.fields", "id,username")])
            .await?;

        let data = json.get("data").and_then(|v| v.as_array()).cloned().unwrap_or_default();

        let found = data.iter().any(|u| {
            u.get("id")
                .and_then(|v| v.as_str())
                .map(|id| id == target_user_id)
                .unwrap_or(false)
        });

        Ok(found)
    }

    async fn user_liked_tweet(&self, user_id: &str, tweet_id: &str) -> Result<bool> {
        let path = format!("/tweets/{}/liking_users", tweet_id);
        let json = self
            .get_raw(&path, &[("max_results", "100"), ("user.fields", "id")])
            .await?;

        let data = json.get("data").and_then(|v| v.as_array()).cloned().unwrap_or_default();

        let found = data.iter().any(|u| {
            u.get("id")
                .and_then(|v| v.as_str())
                .map(|id| id == user_id)
                .unwrap_or(false)
        });

        Ok(found)
    }

    async fn user_retweeted_tweet(&self, user_id: &str, tweet_id: &str) -> Result<bool> {
        let path = format!("/tweets/{}/retweeted_by", tweet_id);
        let json = self
            .get_raw(&path, &[("max_results", "100"), ("user.fields", "id")])
            .await?;

        let data = json.get("data").and_then(|v| v.as_array()).cloned().unwrap_or_default();

        let found = data.iter().any(|u| {
            u.get("id")
                .and_then(|v| v.as_str())
                .map(|id| id == user_id)
                .unwrap_or(false)
        });

        Ok(found)
    }
}

#[derive(Clone, Debug)]
struct UserInfo {
    id: String,
    username: String,
    created_at: Option<String>,
    followers: Option<u64>,
}

#[derive(Clone)]
struct AppState {
    x: XClient,
}

#[derive(Serialize)]
struct HealthResponse {
    status: &'static str,
    service: &'static str,
}

async fn health(State(_state): State<Arc<AppState>>) -> Json<HealthResponse> {
    Json(HealthResponse {
        status: "ok",
        service: "logos_x_guard",
    })
}

#[derive(Deserialize)]
struct CheckRequest {
    user_username: String,
    project_username: String,
    tweet_id: String,
    #[serde(default = "default_true")]
    require_follow: bool,
    #[serde(default = "default_true")]
    require_like: bool,
    #[serde(default = "default_true")]
    require_retweet: bool,
    #[serde(default = "default_min_age")]
    min_account_age_days: u32,
    #[serde(default = "default_min_followers")]
    min_followers: u32,
}

fn default_true() -> bool {
    true
}
fn default_min_age() -> u32 {
    3
}
fn default_min_followers() -> u32 {
    3
}

#[derive(Serialize)]
struct CheckResponse {
    ok: bool,
    user_username: String,
    project_username: String,
    tweet_id: String,
    follow_ok: bool,
    like_ok: bool,
    retweet_ok: bool,
    age_ok: bool,
    followers_ok: bool,
    user_info: Value,
}

async fn check_airdrop(
    State(state): State<Arc<AppState>>,
    Json(req): Json<CheckRequest>,
) -> impl IntoResponse {
    let res = do_check_airdrop(state, req).await;
    match res {
        Ok(resp) => (StatusCode::OK, Json(resp)).into_response(),
        Err(err) => {
            error!("check_airdrop error: {:?}", err);
            let body = serde_json::json!({
                "ok": false,
                "error": "internal_error",
                "message": err.to_string(),
            });
            (StatusCode::BAD_GATEWAY, Json(body)).into_response()
        }
    }
}

async fn do_check_airdrop(state: Arc<AppState>, req: CheckRequest) -> Result<CheckResponse> {
    let user = state.x.get_user_by_username(&req.user_username).await?;
    let project = state
        .x
        .get_user_by_username(&req.project_username)
        .await?;

    let age_ok = true; // упрощённо, без парсинга created_at

    let followers_ok = user
        .followers
        .map(|c| c >= req.min_followers as u64)
        .unwrap_or(false);

    let mut follow_ok = true;
    let mut like_ok = true;
    let mut retweet_ok = true;

    if req.require_follow {
        follow_ok = state
            .x
            .user_follows(&user.id, &project.id)
            .await
            .unwrap_or(false);
    }

    if req.require_like {
        like_ok = state
            .x
            .user_liked_tweet(&user.id, &req.tweet_id)
            .await
            .unwrap_or(false);
    }

    if req.require_retweet {
        retweet_ok = state
            .x
            .user_retweeted_tweet(&user.id, &req.tweet_id)
            .await
            .unwrap_or(false);
    }

    let ok = follow_ok && like_ok && retweet_ok && age_ok && followers_ok;

    let user_info = serde_json::json!({
        "id": user.id,
        "username": user.username,
        "created_at": user.created_at,
        "followers": user.followers,
    });

    Ok(CheckResponse {
        ok,
        user_username: req.user_username,
        project_username: req.project_username,
        tweet_id: req.tweet_id,
        follow_ok,
        like_ok,
        retweet_ok,
        age_ok,
        followers_ok,
        user_info,
    })
}

#[tokio::main]
async fn main() -> Result<()> {
    let filter_layer =
        EnvFilter::try_from_default_env().unwrap_or_else(|_| "info,hyper=warn,reqwest=warn".into());
    let fmt_layer = fmt::layer().with_target(false);

    tracing_subscriber::registry()
        .with(filter_layer)
        .with(fmt_layer)
        .init();

    let creds = XCreds::from_env().context("reading X_* env vars")?;
    info!("X credentials loaded, starting service");

    let x_client = XClient::new(creds);
    let state = Arc::new(AppState { x: x_client });

    let app = Router::new()
        .route("/health", get(health))
        .route("/check_airdrop", post(check_airdrop))
        .with_state(state);

    let addr: SocketAddr = "0.0.0.0:8091".parse().unwrap();
    info!("LOGOS X Guard listening on {}", addr);

    let listener = tokio::net::TcpListener::bind(addr).await?;
    axum::serve(listener, app).await?;

    Ok(())
}
```
