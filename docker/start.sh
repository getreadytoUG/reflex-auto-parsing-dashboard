#!/bin/sh
set -e

# 브라우저가 접속하는 외부 포트(compose 의 ports 왼쪽)를 프런트엔드에 반영.
# 빌드 때 박힌 백엔드 주소(BAKED_API_URL, 예: http://localhost:8080)의 포트를
# PUBLIC_PORT 로 바꿔 쓴다. 호스트(localhost)는 브라우저가 접속한 서버 주소로
# Reflex 가 자동 치환하므로 그대로 둔다.
PUBLIC_PORT="${PUBLIC_PORT:-8080}"
BAKED_HOSTPORT=$(echo "$BAKED_API_URL" | sed -E 's#^[a-z]+://([^/]+).*#\1#')
BAKED_HOST=${BAKED_HOSTPORT%%:*}

for f in /srv/assets/reflex-env-*.js; do
  [ -f "$f" ] || continue
  # 원본을 한 번 보관해 두고, 재시작할 때마다 원본에서 다시 만든다 (포트를 여러 번 바꿔도 안전)
  [ -f "$f.orig" ] || cp "$f" "$f.orig"
  sed "s#//${BAKED_HOSTPORT}/#//${BAKED_HOST}:${PUBLIC_PORT}/#g" "$f.orig" > "$f"
  rm -f "$f.gz"
done
echo "[start.sh] 프런트엔드 백엔드 포트: ${PUBLIC_PORT}"

# 정적 프런트엔드 + 리버스 프록시
nginx

# Reflex 백엔드 (프런트엔드는 이미 정적 빌드되어 있으므로 backend-only)
exec reflex run --env prod --backend-only \
  --backend-host 127.0.0.1 --backend-port 8000 \
  --loglevel info
