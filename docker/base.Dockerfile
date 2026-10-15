# syntax=docker/dockerfile:1
# =====================================================================
# reflex-base : 폐쇄망 빌드용 "환경" 이미지 (소스코드 없음)
#
#  - 외부망(인터넷 O)에서만 빌드합니다.
#      docker build --platform linux/amd64 -f docker/base.Dockerfile -t reflex-base:1.0.0 .
#  - 안에 들어가는 것: Python 패키지(venv), Bun, Node/npm, nginx,
#    npm 오프라인 캐시(/opt/npm-cache), nginx.conf, start.sh
#  - 내부망에서는 프로젝트 루트의 Dockerfile 이 이 이미지를 FROM 으로 써서
#    "내부망 소스코드"를 인터넷 없이 빌드합니다.
# =====================================================================
FROM python:3.11-slim

ENV PYTHONUTF8=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    REFLEX_TELEMETRY_ENABLED=false

# nginx: 정적 프런트엔드 서빙 + 백엔드(/_event 웹소켓 등) 리버스 프록시
RUN apt-get update \
 && apt-get install -y --no-install-recommends nginx \
 && rm -rf /var/lib/apt/lists/* \
 && rm -f /etc/nginx/sites-enabled/default

# Bun 1.3.14 — rxconfig.py 의 Linux 고정 경로(/opt/bun/bun)
COPY --from=oven/bun:1.3.14 /usr/local/bin/bun /opt/bun/bun
# Node.js 22 (Reflex 최소 22.22.0) — 오프라인 빌드는 npm + 로컬 캐시로 수행
COPY --from=node:22.23.2-bookworm-slim /usr/local/bin/node /usr/local/bin/node
COPY --from=node:22.23.2-bookworm-slim /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -s ../lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm \
 && ln -s ../lib/node_modules/npm/bin/npx-cli.js /usr/local/bin/npx \
 && ln -s /opt/bun/bun /usr/local/bin/bun \
 && bun --version && node --version && npm --version

# Python 패키지
RUN python -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# 프런트엔드는 npm + 오프라인 캐시로 빌드 (OFFLINE_SETUP.md 와 같은 방식)
ENV REFLEX_USE_NPM=1 \
    NPM_CONFIG_CACHE=/opt/npm-cache \
    NPM_CONFIG_AUDIT=false \
    NPM_CONFIG_FUND=false \
    NPM_CONFIG_UPDATE_NOTIFIER=false

# --- npm 캐시 채우기 (인터넷 사용) ---------------------------------------
# 1) 현재 소스로 한 번 export → Reflex 기본 패키지 + vite 빌드 도구가 캐시에 들어감
# 2) Reflex 내장 컴포넌트가 쓰는 npm 패키지 전부(차트/마크다운/코드블록/데이터그리드 등)를
#    추가로 캐시 → 내부망 코드가 새 컴포넌트를 써도 오프라인 빌드 가능
COPY . /tmp/warm
COPY docker/warm-npm-packages.txt /tmp/warm-npm-packages.txt
RUN cd /tmp/warm \
 && rm -rf .web \
 && reflex export --frontend-only --no-zip --loglevel info \
 && cd .web \
 && cp package.json /tmp/package.base.json \
 && (npm install --no-save --legacy-peer-deps $(cat /tmp/warm-npm-packages.txt) || echo "[warm] bulk failed") \
 # 내부망 코드가 이 중 "일부"만 써도 의존성이 같은 버전으로 풀리도록, 기본 상태에서 하나씩도 설치해 캐시
 && for p in $(cat /tmp/warm-npm-packages.txt); do \
      cp /tmp/package.base.json package.json; \
      npm install --no-save --legacy-peer-deps "$p" >/dev/null 2>&1 && echo "[warm] ok $p" || echo "[warm] skip $p"; \
    done \
 && cd / && rm -rf /tmp/warm /opt/npm-cache/_logs \
 && du -sh /opt/npm-cache

# 내부망 빌드/실행 공통 파일
COPY docker/nginx.conf /etc/nginx/conf.d/reflex.conf
COPY docker/start.sh /start.sh
RUN sed -i 's/\r$//' /start.sh && chmod +x /start.sh
