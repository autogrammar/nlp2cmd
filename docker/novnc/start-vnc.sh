#!/bin/bash
# Start VNC server + noVNC websocket proxy
set -euo pipefail

echo "=== NLP2CMD Desktop Environment ==="
echo "User: $(whoami) | Home: $HOME"

# Create xstartup
mkdir -p "$HOME/.vnc"
cat > "$HOME/.vnc/xstartup" << 'XEOF'
#!/bin/bash
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
exec dbus-run-session -- startxfce4
XEOF
chmod +x "$HOME/.vnc/xstartup"

# Kill any existing VNC server on :1
vncserver -kill :1 2>/dev/null || true
sleep 1

# Start VNC server (no auth — local Docker demo only)
echo "Starting VNC server on :1 (${VNC_RESOLUTION})..."
vncserver :1 \
    -geometry "$VNC_RESOLUTION" \
    -depth 24 \
    -SecurityTypes None \
    --I-KNOW-THIS-IS-INSECURE \
    -localhost no

echo "VNC server started on :1 (port $VNC_PORT)"

# Wait for VNC to be ready
sleep 2

# Start noVNC websocket proxy
echo "Starting noVNC websocket proxy on port $NOVNC_PORT..."
echo ""
echo "noVNC:  http://localhost:$NOVNC_PORT/vnc.html?autoconnect=true"
echo "VNC:    localhost:$VNC_PORT (no authentication; loopback publication only)"
echo ""

# Ensure recordings dir exists
mkdir -p "$HOME/recordings"

# Keep the proxy in the foreground so startup/bind failures stop the container.
exec websockify --web=/usr/share/novnc/ "$NOVNC_PORT" "localhost:$VNC_PORT"
