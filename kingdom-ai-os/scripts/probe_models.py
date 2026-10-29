#!/usr/bin/env python3
"""Model verification runner. Dry-run is default; --execute may incur provider charges."""
from __future__ import annotations
import argparse, asyncio, json, sys, os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
from app.services.model_probe import probe_model, list_provider_models

async def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true', help='Send one short live response test per eligible exact model ID (may cost money).')
    parser.add_argument('--output', default=str(ROOT / 'docs' / 'model-verification-report.json'))
    args = parser.parse_args()
    models = json.loads((ROOT / 'registries' / 'models.json').read_text(encoding='utf-8'))
    report = {'generated_at': datetime.now(timezone.utc).isoformat(), 'execution_authorized': args.execute,
              'candidate_count': len(models), 'tested': 0, 'passed': 0, 'failed': 0, 'blocked': 0, 'provider_credentials_configured': {'fireworks': bool(os.getenv('FIREWORKS_API_KEY', '').strip()), 'openrouter': bool(os.getenv('OPENROUTER_API_KEY', '').strip()), 'huggingface': bool(os.getenv('HF_TOKEN', '').strip())}, 'results': []}
    catalog_cache = {}
    for item in models:
        provider_family = str(item.get('provider_family') or item.get('provider_family_source_claim') or '').casefold()
        provider = ('openrouter' if 'openrouter' in provider_family else 'fireworks' if 'fireworks' in provider_family else 'huggingface' if any(x in provider_family for x in ('huggingface', 'hugging face', 'hf inference')) else None)
        model_id = item.get('exact_provider_model_id')
        row = {'name': item.get('name'), 'provider': provider, 'model_id': model_id, 'status': 'blocked', 'reason': None}
        if not provider:
            row['reason'] = 'No verified supported provider mapping'
        elif not model_id:
            row['reason'] = 'Exact provider model ID is missing; cannot safely guess from display name'
        elif not args.execute:
            row['status'] = 'not_run'
            row['reason'] = 'Dry run only; rerun with --execute to authorize a live test'
        else:
            if provider not in catalog_cache:
                catalog_cache[provider] = await list_provider_models(provider)
            catalog = catalog_cache[provider]
            valid_ids = {m['id'] for m in catalog.get('models', [])}
            if catalog.get('status') != 'passed':
                row['reason'] = catalog.get('reason', 'Provider catalog unavailable')
            elif model_id not in valid_ids:
                row['status'] = 'failed'
                row['reason'] = 'Exact ID is not present in the live provider catalog'
            else:
                result = await probe_model(provider, model_id)
                row.update({k:v for k,v in result.items() if k in ('status','http_status','reason','response_received')})
                report['tested'] += 1
        report['results'].append(row)
    report['passed'] = sum(r['status'] == 'passed' for r in report['results'])
    report['failed'] = sum(r['status'] == 'failed' for r in report['results'])
    report['blocked'] = sum(r['status'] == 'blocked' for r in report['results'])
    report['not_run'] = sum(r['status'] == 'not_run' for r in report['results'])
    out = Path(args.output); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding='utf-8')
    report['output'] = str(out)
    print(json.dumps({k:report[k] for k in ('generated_at','execution_authorized','candidate_count','tested','passed','failed','blocked','not_run','provider_credentials_configured','output')}, indent=2))

if __name__ == '__main__':
    asyncio.run(main())
