#!/bin/bash
# === Minimal wallpaper rotator for Hyprland exec-once ===

# Configurable via environment or defaults
WALLPAPER_DIR="${WALLPAPER_DIR:-$HOME/Pictures/Wallpapers}"
INTERVAL="${WALLPAPER_INTERVAL:-1800}"
MATUGEN_CONFIG="${MATUGEN_CONFIG:-$HOME/.config/matugen/config.toml}"
MATUGEN_THEMES_DIR="${MATUGEN_THEMES_DIR:-$HOME/.local/share/matugen/themes}"

# Start daemon if needed
if ! pgrep -x "awww-daemon" >/dev/null; then
    awww-daemon &
    sleep 1
fi

# Wait until daemon is ready
until awww query >/dev/null 2>&1; do
    sleep 0.5
done

while true; do
    # Shuffle wallpapers
    mapfile -t wallpapers < <(find "$WALLPAPER_DIR" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.webp" \) -print0 2>/dev/null | shuf -z | xargs -0 -n1)

    [ ${#wallpapers[@]} -eq 0 ] && { sleep 30; continue; }

    for WALLPAPER in "${wallpapers[@]}"; do
        [ -f "$WALLPAPER" ] || continue

        # Set wallpaper (no background &)
        awww img "$WALLPAPER" \
            --transition-type center \
            --transition-step 60 \
            --transition-duration 1.5 >/dev/null 2>&1

        # Update colors: pywal for terminal (pushes sequences to running terms),
        # matugen for waybar
        wal -i "$WALLPAPER" -n -q >/dev/null 2>&1
        
        # Generate resolved matugen config
        MATUGEN_CONFIG_RESOLVED=$(mktemp)
        sed -e "s|{{MATUGEN_THEMES_DIR}}|$MATUGEN_THEMES_DIR|g" \
            -e "s|{{MATUGEN_OUTPUT_DIR}}|$HOME/.config|g" \
            "$MATUGEN_CONFIG" > "$MATUGEN_CONFIG_RESOLVED"
        matugen image "$WALLPAPER" --prefer darkness -c "$MATUGEN_CONFIG_RESOLVED" -q >/dev/null 2>&1
        rm -f "$MATUGEN_CONFIG_RESOLVED"

        sleep "$INTERVAL"
    done
done
