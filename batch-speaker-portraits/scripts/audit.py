"""Read-only PNG technical checks; never substitutes for visual review."""
import argparse
import json
from pathlib import Path
from PIL import Image

def audit(path, size, dpi):
    with Image.open(path) as im:
        im.load()
        density = im.info.get('dpi', (0, 0))
        hist = im.getchannel('A').histogram() if 'A' in im.getbands() else [0] * 256
        checks = {
            'png': im.format == 'PNG',
            'dimensions': im.size == (size, size),
            'dpi': len(density) == 2 and all(abs(v - dpi) <= 0.02 for v in density),
            'transparent_pixels': hist[0] > 0,
            'opaque_pixels': hist[255] > 0,
        }
        return {'path': str(path), 'size': list(im.size), 'dpi': density,
                'checks': checks, 'technical_pass': all(checks.values()),
                'visual_review': 'REQUIRED: identity, framing, head ratio, light/dark edges'}

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('files', nargs='+', type=Path)
    p.add_argument('--size', type=int, default=1200)
    p.add_argument('--dpi', type=float, default=144)
    args = p.parse_args()
    results = []
    for path in args.files:
        try:
            results.append(audit(path, args.size, args.dpi))
        except Exception as exc:
            results.append({'path': str(path), 'technical_pass': False, 'error': str(exc)})
    print(json.dumps(results, ensure_ascii=False, indent=2))
    raise SystemExit(0 if all(r['technical_pass'] for r in results) else 1)
