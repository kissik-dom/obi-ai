# Kingdom AI OS — Architecture

## 1. System overview

Kingdom AI OS is a 24-tab private operating system. The browser is the only
user surface. `frontend` (Vite, React 18, port **5173**) speaks JSON to
`backend` (FastAPI, port **8000**). Backend never exposes raw infrastructure
ports to the browser; it brokers every dependency through typed APIs and a
LiteLLM Router proxy config with 10 rotating OpenRouter keys.

### Control plane

```
Browser 5173
  │  HTTPS/WSS + JSON (idempotency key, request id)
  ▼
Frontend React 18 Vite 5173
  │  TanStack Query + Zustand
  ▼
FastAPI backend 8000
  ├─ /api/<tab>/chat|agents|tasks/open|tasks/completed|training|knowledge|files|tools|outputs|settings
  ├─ KingdomSecurityMiddleware
  ├─ LiteLLM Router (OpenRouter x10, fallbacks, num_retries=3, timeout=60)
  └─ celery beat (testing_agent every 1200s)

Dependencies:
  ├─ Qdrant 6333        vector memory + knowledge
  ├─ MinIO 9000/9001    sandbox + finished objects
  ├─ Vault 8200         secrets, HSM/transit, KYC vault
  ├─ Postgres 5432      system of record
  ├─ Redis 6379         queues, cache, idempotency
  ├─ CUA Fleet 2000×5   isolated computer-use spaces
  ├─ GPU Workers 200×5  VRAM jobs, model inference, video/image
  └─ Security plane     CrowdSec/Wazuh/Suricata/Falco/Tetragon/Cowrie/CompreFace/WireGuard
```

## 2. Data flow

| Hop | From | To | Protocol | Notes |
| --- | --- | --- | --- | --- |
| 1 | frontend 5173 | backend 8000 | HTTP/JSON | every mutation includes `x-idempotency-key` |
| 2 | backend 8000 | Qdrant 6333 | gRPC/HTTP | vector upsert/search |
| 3 | backend 8000 | MinIO 9000 | S3 | sandbox/finished buckets |
| 4 | backend 8000 | Vault 8200 | HTTP | secret lease, HSM transit |
| 5 | backend 8000 | Postgres 5432 | SQL | Alembic migrations |
| 6 | backend 8000 | Redis 6379 | RESP | Celery + locks |
| 7 | backend 8000 | CUA Fleet 2000-2004 | WebSocket | isolated desktop browser |
| 8 | backend 8000 | GPU Workers 200-204 | HTTP | inference jobs |
| 9 | backend 8000 | LiteLLM Router | HTTPS | OpenRouter fallback |
| 10 | backend 8000 | Security plane | JSON/syslog | alerts + evidence |

## 3. docker-compose services

| Service | Image | Port(s) | Replicas | Healthcheck |
| --- | --- | --- | --- | --- |
| frontend | node:22-alpine | 5173:5173 | 1 | `wget -qO- http://localhost:5173` |
| backend | python:3.12-slim | 8000:8000 | 1 | `/healthz` Python urllib |
| qdrant | qdrant/qdrant | 6333:6333 | 1 | `/healthz` |
| minio | minio/minio | 9000:9000, 9001:9001 | 1 | `/minio/health/live` |
| minio-init | minio/mc | none | 1 | init buckets, exits |
| vault | hashicorp/vault | 8200:8200 | 1 | `vault status` |
| postgres | postgres:16-alpine | 5432:5432 | 1 | `pg_isready` |
| redis | redis:7-alpine | 6379:6379 | 1 | `redis-cli ping` |
| cua-fleet | ghcr.io/kingdom/cua-worker | 2000-2004 | 5 | `/healthz` |
| gpu-workers | ghcr.io/kingdom/gpu-worker | 200-204 | 5 | `/healthz` |
| crowdsec | crowdsecurity/crowdsec | 8080 | 1 | `cscli metrics` |
| wazuh-indexer | wazuh/wazuh-indexer | 9200 | 1 | `/` |
| wazuh-manager | wazuh/wazuh-manager | 1514-1515 | 1 | `wazuh-control status` |
| wazuh-dashboard | wazuh/wazuh-dashboard | 443 | 1 | `/` |
| suricata | jasonish/suricata | none | 1 | `suricatasc -c uptime` |
| falco | falcosecurity/falco | none | 1 | pid alive |
| tetragon | quay.io/cilium/tetragon | none | 1 | pid alive |
| cowrie | cowrie/cowrie | 2222 | 1 | TCP 2222 |
| compreface | exadel/compreface | 8001 | 1 | `/health` |
| wireguard | linuxserver/wireguard | 51820/udp | 1 | `wg show` |

## 4. Non-negotiable topology

- Default ports above are fixed. Only `/healthz` and tab APIs are exposed publicly.
- MinIO console 9001 is not exposed publicly.
- Vault/Postgres/Redis/Qdrant bind to internal Docker network.
- CUA and GPU fleets are scaled with `deploy.replicas: 5` and isolated service accounts.
- Security services share a dedicated capture network and cannot reach Vault.
