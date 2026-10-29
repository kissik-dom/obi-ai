#!/usr/bin/env python3
"""Inventory large document/image collections without silently skipping files.

Creates a deterministic manifest with file hashes, sizes, extension, and status.
Does not upload files, extract archives, or call external services. ZIP files are
listed as containers; recursively ingest their contents only after explicit extraction.
"""
from __future__ import annotations
import argparse, hashlib, json, os
from pathlib import Path
from datetime import datetime, timezone

SUPPORTED = {'.pdf','.png','.jpg','.jpeg','.webp','.tif','.tiff','.bmp','.gif','.heic','.heif','.docx','.doc','.pptx','.ppt','.xlsx','.xls','.odt','.ods','.odp','.txt','.md','.html','.htm','.rtf','.zip','.7z','.tar','.gz'}

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('source', type=Path, help='directory containing documents/images')
    ap.add_argument('--output', type=Path, default=Path('ingest-manifest.json'))
    ap.add_argument('--recursive', action='store_true', help='walk subdirectories; otherwise only immediate files')
    ap.add_argument('--max-files', type=int, default=0, help='optional safety cap; 0 means no cap')
    args=ap.parse_args()
    src=args.source.expanduser().resolve()
    if not src.is_dir(): raise SystemExit(f'ERROR: source is not a directory: {src}')
    it=src.rglob('*') if args.recursive else src.iterdir()
    paths=sorted((p for p in it if p.is_file() and p.resolve()!=args.output.resolve()), key=lambda p:str(p).casefold())
    records=[]
    for p in paths:
        ext=p.suffix.lower()
        rec={'relative_path':str(p.relative_to(src)), 'extension':ext or '(none)', 'size_bytes':None,'sha256':None,'inventory_status':'inventoried' if ext in SUPPORTED else 'unsupported_type','ocr_status':'not_run','extraction_status':'not_run'}
        try: rec['size_bytes']=p.stat().st_size; rec['sha256']=sha256(p)
        except OSError as e: rec['inventory_status']='read_error'; rec['error_type']=type(e).__name__
        records.append(rec)
        if args.max_files and len(records)>=args.max_files: break
    supported=sum(r['inventory_status']=='inventoried' for r in records)
    out={'schema_version':1,'created_at':datetime.now(timezone.utc).isoformat(),'source_directory_name':src.name,'recursive':args.recursive,'truncated_by_max_files':bool(args.max_files and len(records)>=args.max_files),'summary':{'files_seen':len(records),'supported_types':supported,'unsupported_types':sum(r['inventory_status']=='unsupported_type' for r in records),'read_errors':sum(r['inventory_status']=='read_error' for r in records),'ocr_completed':0,'extraction_completed':0},'records':records}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(out['summary'],indent=2)); print(f'Manifest: {args.output.resolve()}')
    if out['summary']['read_errors']: raise SystemExit(2)
if __name__=='__main__': main()
