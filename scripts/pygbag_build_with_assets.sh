#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ASSETS_SRC="$ROOT/assets"
WEB_DIR="$ROOT/web"
WEB_ASSETS="$WEB_DIR/assets"

if [ ! -d "$ASSETS_SRC" ]; then
  echo "No assets/ folder found in repo root; nothing to copy."
else
  # Ensure source assets do not contain macOS metadata that would be packaged
  echo "Removing .DS_Store from source assets..."
  find "$ASSETS_SRC" -name ".DS_Store" -delete || true

  # Remove any existing target asset dirs under web/
  for p in "$ASSETS_SRC"/*; do
    base=$(basename "$p")
    # skip hidden entries
    if [[ "$base" == .* ]]; then
      continue
    fi
    target="$WEB_DIR/$base"
    if [ -e "$target" ]; then
      echo "Removing existing $target"
      rm -rf "$target"
    fi
  done

  echo "Copying contents of assets/ -> web/ (preserve structure)..."
  # Copy each child of assets into web/, producing web/backgrounds, web/sounds, web/sprites
  for p in "$ASSETS_SRC"/*; do
    base=$(basename "$p")
    # skip hidden files like .DS_Store or .git
    if [[ "$base" == ".DS_Store" || "$base" == ".git" || "$base" == .* ]]; then
      continue
    fi
    target="$WEB_DIR/$base"
    echo " -> $p -> $target"
    cp -a "$p" "$WEB_DIR/" || { echo "copy failed for $p"; exit 1; }
  done
  echo "Copy complete."
fi

echo "Cleaning any .DS_Store under $WEB_DIR before packaging..."
find "$WEB_DIR" -name ".DS_Store" -delete || true

echo "Running pygbag build (may use significant memory)..."
# Run pygbag in background so we can wait for the apk to appear instead of
# being blocked by the internal HTTP serving loop used by the builder.
PYGBAG_LOG="$WEB_DIR/pygbag_build.log"
python3 -m pygbag web > "$PYGBAG_LOG" 2>&1 &
PYGBAG_PID=$!
echo "pygbag pid=$PYGBAG_PID, logging to $PYGBAG_LOG"

# Wait up to 5 minutes for the apk to appear; if pygbag exits early, show the log
APK="$WEB_DIR/build/web/web.apk"
MAX_WAIT=300
WAITED=0
while [ $WAITED -lt $MAX_WAIT ]; do
  if [ -f "$APK" ]; then
    echo "Found APK after $WAITED s"
    break
  fi
  # If pygbag exited without producing the APK, print the log and exit non-zero
  if ! ps -p $PYGBAG_PID > /dev/null 2>&1; then
    echo "pygbag process exited before producing APK; printing build log:"
    sed -n '1,400p' "$PYGBAG_LOG" || true
    exit 1
  fi
  sleep 1
  WAITED=$((WAITED + 1))
done

if [ ! -f "$APK" ]; then
  echo "web.apk not found after $MAX_WAIT s — printing pygbag log:"
  sed -n '1,400p' "$PYGBAG_LOG" || true
  if ps -p $PYGBAG_PID > /dev/null 2>&1; then
    kill $PYGBAG_PID || true
  fi
  exit 1
fi

# Give pygbag a short grace period to finish cleanly; otherwise kill it
GRACE=10
for i in $(seq 1 $GRACE); do
  if ! ps -p $PYGBAG_PID > /dev/null 2>&1; then
    break
  fi
  sleep 1
done
if ps -p $PYGBAG_PID > /dev/null 2>&1; then
  echo "pygbag still running after graceful wait — killing pid $PYGBAG_PID"
  kill $PYGBAG_PID || true
  sleep 1
fi

echo "Final cleanup of .DS_Store under $WEB_DIR..."
find "$WEB_DIR" -name ".DS_Store" -delete || true

echo "Listing APK contents: $APK"
unzip -l "$APK" || true

echo "Build script finished."
