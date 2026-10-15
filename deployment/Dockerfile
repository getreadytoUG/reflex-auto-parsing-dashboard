FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONUTF8=1

WORKDIR /app

COPY reflex_auto_parsing_dashboard/wheelhouse /app/wheelhouse

COPY reflex_auto_parsing_dashboard/frontend-offline /app/frontend-offline

COPY reflex_auto_parsing_dashboard/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --no-index --find-links=/app/wheelhouse/linux -r /app/requirements.txt && \
    rm -rf /app/wheelhouse

RUN mkdir -p /opt/bun /tmp/bun && \
    python -m zipfile -e /app/frontend-offline/bun/bun-linux-x64.zip /tmp/bun && \
    find /tmp/bun -type f -name bun -exec mv {} /opt/bun/bun \; && \
    rm -rf /tmp/bun && \
    chmod +x /opt/bun/bun && \
    /opt/bun/bun --version

RUN python -m tarfile -e /app/frontend-offline/node/node-v22.23.2-linux-x64.tar.xz /tmp/node && \
    mv /tmp/node/node-v22.23.2-linux-x64 /opt/node22 && \
    rm -rf /tmp/node && \
    /opt/node22/bin/node --version

ENV PATH="/opt/bun:/opt/node22/bin:%{PATH}" \
    REFLEX_USE_SYSTEM_BUN=1 \
    REFLEX_USE_SYSTEM_NODE=1

RUN bun --vesrion && node --vesrion && python -m reflex init || true

RUN tar -xzf /app/frontend-offline/node_modules-linux-x64.tar.gz -C /app/.web/ && \
    mkdir -p /root/linux-cache && \
    tar -xzf /app/frontend-offline/npm-cache-linux.tar.gz -C /root/ && \
    cp /app/frontend-offline/reflex.install_frontend_packages.cached.linux /app/.web/reflex.install_frontend_packages.cached && \
    cp /app/frontend-offline/package-lock.linux.json /app/.web/package-lock.json

RUN rm -rf /app/frontend-offline

COPY reflex_auto_parsing_dashboard/ /app/reflex_auto_parsing_dashboard

WORKDIR /app/reflex_auto_parsing_dashboard

