#!/usr/bin/env python3
"""Fetch images from Pexels into assets/images/sandbox for testing.

Usage examples:
  python tools/fetch_pexels_sandbox.py --query "family" --count 3 --orientation landscape --min-width 1200
  PEXELS_API_KEY env var will be used if --api-key is not provided.

This script saves originals into `assets/images/sandbox/` named:
  sandbox-{slug}-{i}.jpg

Optional --resize WxH will create an additional file with suffix -WxH.jpg
"""
import os
import sys
import argparse
import requests
from urllib.parse import urlparse

try:
    from PIL import Image
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False


DEFAULT_DEST = "assets/images/sandbox"


def slugify(s: str) -> str:
    return ''.join(c if c.isalnum() else '-' for c in s.lower()).strip('-')


def download(url, dest_path):
    resp = requests.get(url, stream=True, timeout=30)
    resp.raise_for_status()
    with open(dest_path, 'wb') as f:
        for chunk in resp.iter_content(8192):
            f.write(chunk)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--api-key', '-k', help='Pexels API key (or set PEXELS_API_KEY env var)')
    parser.add_argument('--query', '-q', default='seguros', help='Search query / topic')
    parser.add_argument('--count', '-c', type=int, default=3, help='Number of images to download')
    parser.add_argument('--orientation', choices=['landscape', 'portrait', 'square'], default='landscape')
    parser.add_argument('--min-width', type=int, default=0)
    parser.add_argument('--min-height', type=int, default=0)
    parser.add_argument('--resize', help='Optional WxH to resize downloaded image into additional file (e.g. 1200x448)')
    parser.add_argument('--dest', default=DEFAULT_DEST, help='Destination folder (defaults to assets/images/sandbox)')
    parser.add_argument('--per-page', type=int, default=15, help='Pexels per_page (max 80)')
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get('PEXELS_API_KEY')
    if not api_key:
        print('ERROR: Provide --api-key or set PEXELS_API_KEY env var', file=sys.stderr)
        sys.exit(2)

    os.makedirs(args.dest, exist_ok=True)

    headers = {'Authorization': api_key}
    url = 'https://api.pexels.com/v1/search'
    params = {
        'query': args.query,
        'per_page': args.per_page,
        'orientation': args.orientation,
        'page': 1,
    }

    downloaded = 0
    page = 1
    slug = slugify(args.query)

    while downloaded < args.count:
        params['page'] = page
        r = requests.get(url, headers=headers, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        photos = data.get('photos', [])
        if not photos:
            print('No more photos returned by API.')
            break

        for i, photo in enumerate(photos):
            if downloaded >= args.count:
                break
            src = photo.get('src', {})
            # prefer large or original
            img_url = src.get('large2x') or src.get('large') or src.get('original')
            if not img_url:
                continue

            width = photo.get('width', 0)
            height = photo.get('height', 0)
            if width < args.min_width or height < args.min_height:
                continue

            out_name = f"hero-{slug}-{downloaded+1}.jpg"
            out_path = os.path.join(args.dest, out_name)
            try:
                print(f'Downloading {img_url} -> {out_path}')
                download(img_url, out_path)
            except Exception as e:
                print('Failed to download:', e)
                continue

            if args.resize and PIL_AVAILABLE:
                try:
                    w, h = map(int, args.resize.lower().split('x'))
                    im = Image.open(out_path).convert('RGB')
                    # center-crop to cover
                    src_w, src_h = im.size
                    src_ratio = src_w / src_h
                    dst_ratio = w / h
                    if src_ratio > dst_ratio:
                        # crop width
                        new_w = int(dst_ratio * src_h)
                        left = (src_w - new_w) // 2
                        im = im.crop((left, 0, left + new_w, src_h))
                    else:
                        # crop height
                        new_h = int(src_w / dst_ratio)
                        top = (src_h - new_h) // 2
                        im = im.crop((0, top, src_w, top + new_h))
                    im = im.resize((w, h), Image.LANCZOS)
                    resized_path = os.path.join(args.dest, f"hero-{slug}-{downloaded+1}-{w}x{h}.jpg")
                    im.save(resized_path, quality=90)
                    print('Wrote resized:', resized_path)
                except Exception as e:
                    print('Resize failed:', e)

            downloaded += 1

        if downloaded < args.count:
            page += 1
            if page > 100:
                break

    print(f'Downloaded {downloaded} images to {args.dest}')


if __name__ == '__main__':
    main()
