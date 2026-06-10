#!/bin/bash
# === Minimal wallpaper rotator for Hyprland exec-once ===

DIR="$HOME/Pictures/Wallpapers"
INTERVAL=1800

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
    mapfile -t wallpapers < <(find "$DIR" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.webp" \) -print0 2>/dev/null | shuf -z | xargs -0 -n1)

    [ ${#wallpapers[@]} -eq 0 ] && { sleep 30; continue; }

    for WALLPAPER in "${wallpapers[@]}"; do
        [ -f "$WALLPAPER" ] || continue

        # Set wallpaper (no background &)
        awww img "$WALLPAPER" \
            --transition-type center \
            --transition-step 60 \
            --transition-duration 1.5 >/dev/null 2>&1

        # Update colors
        wal -i "$WALLPAPER" -n -q >/dev/null 2>&1

        sleep "$INTERVAL"
    done
done
