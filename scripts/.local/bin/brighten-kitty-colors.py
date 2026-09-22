#!/usr/bin/env python3
# Post-process kitty colors to create actual bright variants
import sys
import re
import colorsys

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(
        int(max(0, min(255, rgb[0] * 255))),
        int(max(0, min(255, rgb[1] * 255))),
        int(max(0, min(255, rgb[2] * 255)))
    )

def brighten_hex(hex_color, factor=1.5):
    """Brighten a hex color by increasing lightness in HSL space"""
    r, g, b = hex_to_rgb(hex_color)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    # Increase lightness
    l = min(1.0, l * factor)
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return rgb_to_hex((r, g, b))

def process_config(config_file):
    with open(config_file, 'r') as f:
        lines = f.readlines()
    
    colors = {}
    color_pattern = re.compile(r'^color(\d+)\s+(.+)$')
    
    for line in lines:
        m = color_pattern.match(line.strip())
        if m:
            idx = int(m.group(1))
            colors[idx] = m.group(2).strip()
    
    # Create bright variants
    for i in range(1, 8):
        if i in colors:
            colors[i + 8] = brighten_hex(colors[i], 1.5)
    
    # Brighten background too (color0 -> color8)
    if 0 in colors:
        colors[8] = brighten_hex(colors[0], 1.3)
    
    # Write back
    output = []
    for line in lines:
        m = color_pattern.match(line.strip())
        if m:
            idx = int(m.group(1))
            if idx in colors:
                output.append(f'color{idx}       {colors[idx]}\n')
            else:
                output.append(line)
        else:
            output.append(line)
    
    with open(config_file, 'w') as f:
        f.writelines(output)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        process_config(sys.argv[1])
    else:
        process_config('/home/archbtw/.cache/wal/colors-kitty.conf')