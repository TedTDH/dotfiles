#!/usr/bin/env python3
# Boost saturation of pywal-generated kitty colors
import json
import colorsys
import sys

def boost_saturation(config_file, factor=1.6):
    with open(config_file, 'r') as f:
        lines = f.readlines()
    
    # Read the palette from colors.json
    import os
    palette_file = os.path.join(os.path.dirname(config_file), 'colors.json')
    with open(palette_file, 'r') as f:
        palette = json.load(f)
    
    # Boost saturation for colors 1-7 (standard), keep bright variants in sync
    boosted = {}
    for i in range(1, 8):
        c = palette['colors'][f'color{i}']
        r, g, b = int(c[1:3], 16)/255, int(c[3:5], 16)/255, int(c[5:7], 16)/255
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        s = min(1.0, s * factor)
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        boosted[i] = f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'
        # Also boost bright variant (color8 = color0 brightened, color9 = color1 brightened, etc.)
        boosted[i + 8] = boosted[i]
    
    # Brighten background (color0 -> color8)
    c0 = palette['colors']['color0']
    r, g, b = int(c0[1:3], 16)/255, int(c0[3:5], 16)/255, int(c0[5:7], 16)/255
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    l = min(1.0, l * 1.3)
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    boosted[0] = c0  # keep original background
    boosted[8] = f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'
    
    # Write back to colors-kitty.conf
    import re
    pattern = re.compile(r'^(color(\d+))\s+(.+)$')
    output = []
    for line in lines:
        m = pattern.match(line.strip())
        if m:
            idx = int(m.group(2))
            if idx in boosted:
                output.append(f'color{idx}       {boosted[idx]}\n')
            else:
                output.append(line)
        else:
            output.append(line)
    
    with open(config_file, 'w') as f:
        f.writelines(output)

if __name__ == '__main__':
    factor = float(sys.argv[2]) if len(sys.argv) > 2 else 1.6
    boost_saturation(sys.argv[1] if len(sys.argv) > 1 else '/home/archbtw/.cache/wal/colors-kitty.conf', factor)