# DOC 6: SECURITY_SPEC.md - Zero-Trust, eBPF, Vault HSM, Cowrie Honeypot & VideoKYC

## 1. Seven-Layer Defense-in-Depth Architecture

1. **Layer 1: Behavioral WAF (`CrowdSec 100k` + `ModSecurity v3 OWASP CRS 4.2`)**
   - Detects zero-day and automated agent probes by **behavioral patterns** (JA3 TLS fingerprint, request velocity, absence of human pointer entropy) rather than static signatures alone.
   - Shares blocklists with 100k+ CrowdSec CTI sensors.
   - **Self-Allowlist Protection**: Requests presenting a valid `X-Kingdom-Internal` secret (verified against Vault HSM / `KINGDOM_INTERNAL_SECRET`) or allowlisted Vultr management IP never lock out the owner.

2. **Layer 2: Network IDS/IPS (`Suricata 7` + `Zeek 6`)**
   - Runs ET Open rulesets at line rate to catch covert exfiltration or anomalous outbound tunnels from worker containers.

3. **Layer 3: SIEM, FIM & Endpoint Forensics (`Wazuh 4.8` + `Osquery 5.12` + `Velociraptor`)**
   - Real-time File Integrity Monitoring (FIM), rootkit detection, and per-sandbox ML anomaly scoring logged immutably to `Loki` + `Prometheus` + `Grafana`.

4. **Layer 4: Kernel eBPF Runtime Security (`Falco` + `Tetragon Cilium` + `Tracee` + `KubeArmor` + Custom `Aya Rust / BCC Python`)**
   - `Falco` monitors 200+ syscall rules across all 2,000 CUA Spaces (`/proc`, `/var/run/docker.sock`, unexpected `execve` shells).
   - `Tetragon` (Cilium) provides kernel-level eBPF enforcement capable of synchronously blocking forbidden syscalls before execution.
   - `KubeArmor` binds LSM + eBPF confinement policies per container.
   - Custom `Aya` (Rust) and `BCC` (`kprobe__sys_openat`) templates allow bespoke kernel probes forwarding telemetry to Wazuh.

5. **Layer 5: Hardware-Grade Secret Management (`HashiCorp Vault 1.15 HSM Transit`)**
   - Financial keys, Aave V3 signing keys, and VideoKYC biometric hashes live **exclusively in Vault HSM Transit** (`:8200`), never in plaintext `.env` or MinIO files.
   - Financial endpoints enforce PCI-DSS controls: mTLS verification, strict `10 req/sec` token-bucket rate limiting, and anomaly circuit-breakers.

6. **Layer 6: Zero-Trust Mesh (`WireGuard` + `Vault PKI mTLS`)**
   - Each of the 2,000 CUA Spaces operates inside an isolated `/32` WireGuard tunnel with short-lived mTLS certificates; **no lateral movement** between Spaces is permitted.

7. **Layer 7: Legitimate Deception & Law-Enforcement Forensics (`Cowrie Honeypot` + `Canarytokens`)**
   - Decoy routes (`/admin`, `/financial`, `/photos`, and `/api/security/honeypot/*`) capture unauthorized intrusion attempts **lawfully** (never accessing an external party's webcam).
   - Every honeypot event logs:
     - `ip`, `asn`, `geoip`, `ja3` TLS fingerprint, `user_agent`, UTC `timestamp`
     - Client-transmitted `wifi_ssid` header/metadata (if sent by client)
     - Server location (`Vultr EWR - Newark, NJ`)
     - Server-side **honeypot session screen/transcript recording** (`honeypot_session_recording_id` of YOUR server's decoy session)
   - Exposed via:
     - `GET /api/security/attempts` -> Live feed for `SecurityViewer` UI
     - `POST /api/security/honeypot/log` -> Records decoy interaction
     - `GET /api/security/audit/export` -> Generates downloadable **Law-Enforcement Audit PDF** notarized with SHA-256 + OpenTimestamps / IPFS Kubo metadata.

## 2. Biometric Authentication & Mandatory Opt-In VideoKYC (`CompreFace` + `FIDO2 WebAuthn`)

To comply strictly with **Illinois BIPA, Indiana privacy statutes, and GDPR**:
1. **Explicit Informed Consent Required**: No biometric capture ever runs silently. Accessing restricted `/api/financial` or `/bank` vaults requires explicit opt-in consent (`consent: true`) after displaying collection purpose, retention window (`30 days`), and deletion policy.
2. **Capture & Vault HSM Encryption**: Upon opt-in, a 5-second `getUserMedia` verification clip / `CompreFace` `facial_enrolled` embedding + `FIDO2 WebAuthn` assertion is hashed and stored encrypted inside **Vault HSM** (never plaintext object storage), scheduled for automatic purge after 30 days.
3. **Graceful Opt-Out**: Declining biometric opt-in blocks only `/financial` and `/bank` routes while keeping general workspace tabs accessible.
4. **Endpoints**:
   - `GET /api/kyc/status`
   - `POST /api/kyc/verify`
   - `POST /api/security/biometric/opt-in`
   - `POST /api/security/bot/check`
