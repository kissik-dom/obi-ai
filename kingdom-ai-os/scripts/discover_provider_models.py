#!/usr/bin/env python3
"""Fetch one provider's authenticated model catalog; this does not run inference."""
from __future__ import annotations
import argparse, asyncio, json, sys
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
from app.services.model_probe import list_provider_models

async def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--provider', required=True, choices=('huggingface', 'openrouter', 'fireworks'))
    parser.add_argument('--output', default=None)
    args = parser.parse_args()
    result = await list_provider_models(args.provider)
    report = {'generated_at': datetime.now(timezone.utc).isoformat(), 'provider': args.provider, 'catalog_discovery_only': True, **result}
    out = Path(args.output) if args.output else ROOT / 'provider-catalog.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({k: report.get(k) for k in ('generated_at', 'provider', 'status', 'count_returned', 'reason', 'output')}, indent=2))
    return 0 if report.get('status') == 'passed' else 1

if __name__ == '__main__':
    raise SystemExit(asyncio.run(main()))
