# noVNC Desktop Environment for NLP2CMD GUI Automation
# Provides a full Linux desktop accessible via browser (noVNC) and VNC.
# Playwright connects to the noVNC websocket to automate desktop apps.
#
# Usage:
#   docker compose -f docker/novnc/docker-compose.yml up -d
#   # Open http://localhost:6080 in browser to see the desktop
#   # Run: nlp2cmd --run "open calculator and type 2+2"

FROM debian:bookworm-slim@sha256:7ff6ba31527b9e336162fa061746c366c4b2032f4d2cff2078bea43f78efe3f8

ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:1
ENV VNC_PORT=5901
ENV NOVNC_PORT=6080
ENV VNC_RESOLUTION=1280x800
ENV PLAYWRIGHT_BROWSERS_PATH=/opt/playwright

# Install desktop environment + VNC + noVNC + common apps
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Window manager (lightweight)
    xfce4 xfce4-terminal dbus-x11 \
    # VNC server
    tigervnc-standalone-server tigervnc-common \
    # noVNC (web-based VNC client)
    novnc websockify \
    # Common desktop apps for demo
    xterm mousepad thunar galculator \
    # Native Firefox package; Ubuntu's transitional package requires Snap
    firefox-esr \
    # Utilities
    curl wget git sudo procps net-tools xdotool xclip \
    # Screenshot & video recording
    ffmpeg scrot imagemagick \
    # Python
    python3 python3-pip python3-venv \
    # Fonts
    fonts-liberation fonts-dejavu-core \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create non-root user FIRST so /home/nlp2cmd is owned correctly
RUN useradd -m -s /bin/bash nlp2cmd && \
    echo "nlp2cmd ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Create virtual environment for Python packages as nlp2cmd user
USER nlp2cmd
WORKDIR /home/nlp2cmd
RUN python3 -m venv /home/nlp2cmd/venv && \
    /home/nlp2cmd/venv/bin/pip install --no-cache-dir \
    playwright click rich python-dotenv pyyaml

# Install Playwright browsers (needs root for deps, then switch back)
USER root
RUN /home/nlp2cmd/venv/bin/python -m playwright install --with-deps chromium
USER nlp2cmd

# VNC startup script
COPY --chown=nlp2cmd:nlp2cmd start-vnc.sh /home/nlp2cmd/start-vnc.sh
RUN chmod +x /home/nlp2cmd/start-vnc.sh

# Demo scripts
COPY --chown=nlp2cmd:nlp2cmd demos/ /home/nlp2cmd/demos/

# Pre-create directories needed at runtime
RUN mkdir -p /home/nlp2cmd/.vnc /home/nlp2cmd/recordings

EXPOSE 5901 6080

CMD ["/home/nlp2cmd/start-vnc.sh"]
