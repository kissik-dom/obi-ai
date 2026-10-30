# Kingdom AI OS — Security Specification

## Defense in depth

| Layer | Tool | Role |
| --- | --- | --- |
| Edge/IPS | CrowdSec | reputation, bouncer, scenarios |
| SIEM | Wazuh (indexer + manager + dashboard) | log correlation, FIM, alerting |
| NIDS | Suricata | network signature and anomaly detection |
| Runtime | Falco | eBPF syscall anomaly detection |
| eBPF/Kernel | Tetragon | observability + enforcement |
| Secrets | Vault + HSM/Transit | key custody, lease, KYC vault |
| VPN | WireGuard | administrative lane only |
| Honeypot | Cowrie | SSH/Telnet trap on 2222 |
| KYC | CompreFace + FIDO2 WebAuthn + VideoKYC | liveness, face match, strong auth |
| App | KingdomSecurityMiddleware | headers, body limit, request ID |

## Vault HSM

- Root key never leaves Vault; HSM/transit encrypts fin/legal/KYC artifacts.
- Per-tab token roles. No tab can read another tab's secret path.
- Leases are short. Every service uses dynamic credentials.

## CompreFace VideoKYC

- Passport/OMNIVIDENS agent collects video selfie.
- CompreFace verifies liveness and 1:1 face match to passport.
- WebAuthn hardware keys are required for Security/Admin and financial vault writes.
- A deterministic `kyc_id` is stored in Postgres and Vault; raw video deleted after verification.

## Honeypot policy

- Cowrie listens on public 2222 only. Any interaction is an incident.
- Wazuh + Suricata correlate honeypot source with production traffic.
- Repeated source is banned by CrowdSec and reported to the Security Honeypot agent.

## Incident flow

tap -> Suricata/Falco/Tetragon -> Wazuh SIEM -> Hermes Security agent -> admin notification.
