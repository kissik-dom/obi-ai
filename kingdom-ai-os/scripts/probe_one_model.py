#!/usr/bin/env python3
"""Run one explicit, cost-bearing model connectivity probe. Never run implicitly."""
from __future__ import annotations
import argparse, asyncio, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
from app.services.model_probe import probe_model

async def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--provider', required=True, choices=('huggingface', 'openrouter', 'fireworks'))
    parser.add_argument('--model-id', required=True, help='Exact model ID from that provider live catalog; do not guess.')
    parser.add_argument('--execute', action='store_true', help='Required to authorize one request that may incur charges.')
    args = parser.parse_args()
    if not args.execute:
        print(json.dumps({'status': 'blocked', 'reason': 'Pass --execute to authorize one live provider request', 'provider': args.provider, 'model_id': args.model_id}, indent=2))
        return 2
    result = await probe_model(args.provider, args.model_id)
    # The probe helper intentionally returns a short response excerpt. Do not print credentials or provider response bodies.
    print(json.dumps(result, indent=2))
    return 0 if result.get('status') == 'passed' else 1

if __name__ == '__main__':
    raise SystemExit(asyncio.run(main()))
