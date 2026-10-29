#!/usr/bin/env python3
"""Discover chat models currently exposed by Hugging Face Inference Providers.

This is catalog discovery, not a live model quality test. It uses HF_TOKEN and
never writes the token to output. Catalog availability and pricing can change.
"""
from __future__ import annotations
import argparse, asyncio, json, os
from datetime import datetime, timezone
from pathlib import Path
import httpx

ROOT = Path(__file__).resolve().parents[1]

async def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default=str(ROOT / 'docs' / 'huggingface-live-catalog.json'))
    args = parser.parse_args()
    token = os.getenv('HF_TOKEN', '').strip()
    report = {'generated_at': datetime.now(timezone.utc).isoformat(), 'source': 'https://router.huggingface.co/v1/models', 'catalog_discovery_only': True, 'credential_configured': bool(token), 'status': 'blocked', 'models': [], 'count': 0}
    if not token:
        report['reason'] = 'HF_TOKEN is not configured'
    else:
        try:
            async with httpx.AsyncClient(timeout=30, follow_redirects=False) as client:
                response = await client.get('https://router.huggingface.co/v1/models', headers={'Authorization': f'Bearer {token}'})
            if response.status_code < 200 or response.status_code >= 300:
                report.update(status='failed', http_status=response.status_code, reason='Hugging Face model catalog request failed; inspect account permissions/billing privately')
            else:
                body = response.json()
                for item in body.get('data', []) if isinstance(body, dict) else []:
                    if not isinstance(item, dict) or not isinstance(item.get('id'), str):
                        continue
                    providers = []
                    for provider in item.get('providers', []) or []:
                        if isinstance(provider, dict):
                            providers.append({k: provider.get(k) for k in ('provider', 'status', 'context_length', 'pricing', 'supports_tools', 'supports_structured_output', 'first_token_latency_ms', 'throughput', 'is_model_author') if k in provider})
                    report['models'].append({'id': item['id'], 'owned_by': item.get('owned_by'), 'architecture': item.get('architecture'), 'providers': providers})
                report.update(status='passed', count=len(report['models']))
        except (httpx.HTTPError, ValueError):
            report.update(status='failed', reason='Catalog connection or response parsing failed')
    out = Path(args.output); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({k: report.get(k) for k in ('generated_at', 'status', 'credential_configured', 'count', 'reason', 'output')}, indent=2))
    return 0 if report['status'] == 'passed' else 1

if __name__ == '__main__':
    raise SystemExit(asyncio.run(main()))
