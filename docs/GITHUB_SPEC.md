# Kingdom AI OS — GitHub Specification

## Repository

- `kissik-dom/obi-ai`
- Branch: `main`
- Feature branches: `feat/<tab-or-service>`, `fix/<summary>`, `docs/<summary>`

## Commit convention

```
feat(tab-llm): add model fallback panel
fix(security): validate x-idempotency-key header
docs(spec): update ToolRegistry category A
test(test_all): add CUA isolation probe
infra(compose): add GPU worker healthcheck
```

## Push discipline

- Push after each tab is implemented, and after each docs/intent file.
- Never commit `.env` or OpenRouter keys. Example keys live only in `.env.example`.

## GitHub Actions

| Workflow | Trigger | Job |
| --- | --- | --- |
| Test | push, pull_request | `python3 test_all.py` + frontend `npm ci` + `npm run typecheck` |
| Deploy Vultr | workflow_dispatch | `bash vultr_deploy.sh` |
| Security scan | weekly | gitleaks, trivy compose scan |

`vultr_deploy.sh` is the only deploy path. It uploads `docker-compose.yml`,
`vultr_security_docker-compose.yml`, `vultr_gpu_docker-compose.override.yml`,
and `vultr_cloud_init.yaml`, then runs compose with healthcheck verification.
