"""Derive a bust crop from visible subject bounds; never overwrite the source."""
import argparse
from io import BytesIO
import json
from pathlib import Path
from PIL import Image


def crop_bust(source, output, remove_bottom=1/3, alpha_threshold=8, padding=4):
    source, output = Path(source), Path(output)
    if source.resolve() == output.resolve() or output.exists():
        raise ValueError('Refusing to overwrite source or existing output')
    if not 0 <= remove_bottom < 1 or not 1 <= alpha_threshold <= 255 or padding < 0:
        raise ValueError('Invalid crop parameters')
    with Image.open(source) as original:
        if 'A' not in original.getbands():
            raise ValueError('Input requires genuine alpha transparency')
        im = original.convert('RGBA')
        alpha = im.getchannel('A')
        histogram = alpha.histogram()
        if histogram[0] == 0:
            raise ValueError('Input has no fully transparent background pixels')
        bbox = alpha.point(lambda v: 255 if v >= alpha_threshold else 0).getbbox()
        if bbox is None:
            raise ValueError('Input contains no visible subject')
        left, top, right, bottom = bbox
        cut_bottom = max(top+1, round(top+(bottom-top)*(1-remove_bottom)))
        box = (max(0, left-padding), max(0, top-padding),
               min(im.width, right+padding), min(im.height, cut_bottom))
        cropped = im.crop(box)
        options = {}
        if original.info.get('dpi'):
            options['dpi'] = original.info['dpi']
        if original.info.get('icc_profile'):
            options['icc_profile'] = original.info['icc_profile']
        encoded = BytesIO()
        cropped.save(encoded, format='PNG', **options)
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open('xb') as target:
            target.write(encoded.getvalue())
    return {'source': str(source.resolve()), 'output': str(output.resolve()),
            'visible_bbox': list(bbox), 'crop_box': list(box),
            'remove_bottom': remove_bottom, 'size': list(cropped.size),
            'visual_review': 'Required: crown, shoulders, neckline, bust framing'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--remove-bottom', type=float, default=1/3)
    parser.add_argument('--alpha-threshold', type=int, default=8)
    parser.add_argument('--padding', type=int, default=4)
    args = parser.parse_args()
    try:
        result = crop_bust(args.source, args.output, args.remove_bottom,
                           args.alpha_threshold, args.padding)
    except (ValueError, OSError) as exc:
        parser.exit(1, str(exc)+'\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
