#!/usr/bin/env sh
set -eu
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$ROOT"
python - <<'PY'
import json
from pathlib import Path
import yaml
root = Path('.')
for name in ('registries/tabs.json','registries/models.json','registries/open_source_projects.json','registries/document_templates.json'):
    data=json.loads((root/name).read_text(encoding='utf-8'))
    assert isinstance(data,list), f'{name} must be an array'
    print(f'JSON PASS {name}: {len(data)} records')
status=json.loads((root/'docs/release-status.json').read_text(encoding='utf-8'))
assert status.get('release_status')=='NOT_RELEASE_READY' and status.get('deployment_authorized') is False
print('JSON PASS docs/release-status.json: release gate explicitly closed')
for name in ('docker-compose.yml','backend/litellm_config.yaml','.github/workflows/ci.yml','.github/workflows/model-live-smoke.yml','.github/workflows/model-catalog-discovery.yml'):
    yaml.safe_load((root/name).read_text(encoding='utf-8'))
    print(f'YAML syntax PASS {name}')
tabs=json.loads((root/'registries/tabs.json').read_text())
assert len(tabs)==28, f'expected 28 tab records, got {len(tabs)}'
assert len({t['id'] for t in tabs})==len(tabs), 'duplicate tab IDs'
models=json.loads((root/'registries/models.json').read_text())
assert len(models)>=100, f'expected at least 100 model intake records, got {len(models)}'
assert len({m['name'] for m in models})==len(models), 'duplicate model names'
assert all(m.get('status')=='UNVERIFIED' for m in models), 'seed model unexpectedly marked verified'
projects=json.loads((root/'registries/open_source_projects.json').read_text())
assert len(projects)>=500, f'expected at least 500 project intake candidates, got {len(projects)}'
assert len({p['name_as_written'] for p in projects})==len(projects), 'duplicate project names'
assert all(p.get('status')=='UNVERIFIED' for p in projects), 'seed project unexpectedly marked verified'
assert all(p.get('open_source_status','UNVERIFIED') in ('UNVERIFIED','VERIFIED_LICENSE') for p in projects), 'invalid open-source status'
assert all(p.get('license_source_url') for p in projects if p.get('open_source_status')=='VERIFIED_LICENSE'), 'verified license status requires a source URL'
templates=json.loads((root/'registries/document_templates.json').read_text())
assert len(templates)>=4 and len({t['id'] for t in templates})==len(templates), 'document template registry invalid'
model_report=json.loads((root/'docs/model-verification-report.json').read_text())
assert model_report['candidate_count']==len(models), 'model verification report does not match candidate count'
assert model_report['passed']==0 and model_report['execution_authorized'] is False, 'dry-run report must not claim live passes'
env=(root/'.env.example').read_text()
assert 'FIREWORKS_API_KEY=' in env and 'OPENROUTER_API_KEY=' in env and 'HF_TOKEN=' in env, 'all three provider key slots are required'
assert 'OPENAI_API_KEY=' not in env and 'ANTHROPIC_API_KEY=' not in env, 'unexpected additional provider key slot'
print('Registry integrity PASS')
PY
python -m compileall -q backend/app backend/tests
(cd backend && PYTHONPATH=. pytest -q)
