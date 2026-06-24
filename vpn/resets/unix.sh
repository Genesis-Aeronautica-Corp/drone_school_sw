#!/bin/bash

whoami
echo "PATH is: $PATH"
type pkill

set -e

TSD_BIN="$1"
STATE_DIR="$2"

echo "🔧 Stopping tailscaled..."
pkill -f "tailscaled" || true
echo "🧹 Removing state..."
rm -rf "$STATE_DIR"

echo "🚀 Starting tailscaled..."
#"$TSD_BIN" --tun=userspace-networking --state="$STATE_DIR/tailscaled.state" --socket="$STATE_DIR/tailscaled.sock" --port 41641 &

echo "✅ Done"
