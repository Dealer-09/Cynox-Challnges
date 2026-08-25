FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    openssh-server python3 sudo --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Create user
RUN useradd -m -s /bin/bash bucky && \
    echo "bucky:w1nt3r_s0ld13r" | chpasswd

# Sudo rule — wildcard allows passing any file as arg
RUN echo "bucky ALL=(root) NOPASSWD: /usr/bin/python3 /opt/shield/monitor.py *" \
    >> /etc/sudoers

# The monitor script — loads a plugin file via exec()
RUN mkdir -p /opt/shield
RUN cat > /opt/shield/monitor.py << 'PYEOF'
import sys, os

if len(sys.argv) < 2:
    print("Usage: monitor.py <plugin_file>")
    sys.exit(1)

plugin = sys.argv[1]
print(f"[SHIELD] Loading telemetry plugin: {plugin}")
exec(open(plugin).read())   # loads and runs the plugin file as root
PYEOF

RUN echo "cyn0x{sud0_w1ldc4rd_py_3x3c_priv3sc}" > /root/flag.txt && \
    chmod 400 /root/flag.txt

# SSH setup
RUN mkdir /var/run/sshd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]