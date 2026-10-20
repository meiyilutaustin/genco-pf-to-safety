"""Encode direct rendered PNG frames as a lossless 12fps WebP loop."""
from pathlib import Path
import sys
from PIL import Image
paths=sorted(Path(sys.argv[1]).glob('*.png'))
frames=[]
for p in paths:
    with Image.open(p) as im: frames.append(im.convert('RGB'))
durations=[round((i+1)*1000/12)-round(i*1000/12) for i in range(len(frames))]
frames[0].save(sys.argv[2],save_all=True,append_images=frames[1:],duration=durations,loop=0,lossless=True,method=4)
