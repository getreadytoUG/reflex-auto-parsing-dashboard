# (주의) 맨 위에 "# syntax=docker/dockerfile:1" 를 넣지 마세요 — 빌드 시 Docker Hub 접속을 시도함
# =====================================================================
# 내부망(폐쇄망)에서 "내부망 소스코드"로 이미지를 빌드하는 Dockerfile
#
#  - 인터넷 없이 빌드됩니다. 필요한 건 전부 reflex-base 이미지 안에 있습니다
#    (외부망에서 docker/base.Dockerfile 로 만들어 docker load 로 반입).
#  - 이 파일 + .dockerignore + docker-compose.yml 을 소스 루트에 두고
#      docker compose up -d --build
# =====================================================================
FROM reflex-base:1.0.0

WORKDIR /app
COPY . .

# 내부망 requirements.txt 에 베이스 이미지에 없는 패키지가 있으면 여기서 바로 실패
# (인터넷 없이 "이미 설치됨"만 확인)
RUN pip install --no-index -r requirements.txt

# 브라우저가 접속할 백엔드 주소. localhost 는 브라우저가 접속한 서버 주소로
# 자동 치환되고, 포트는 실행 시 PUBLIC_PORT 로 바꿔 쓰므로 그대로 두면 됨.
ARG API_URL=http://localhost:8080
ENV REFLEX_API_URL=${API_URL} \
    BAKED_API_URL=${API_URL} \
    NPM_CONFIG_OFFLINE=true

# npm 오프라인 캐시(/opt/npm-cache)로 프런트엔드 패키지 설치 + 정적 빌드
RUN rm -rf .web /srv \
 && reflex export --frontend-only --no-zip --loglevel info \
 && mkdir -p /srv \
 && cp -r .web/build/client/. /srv/ \
 && rm -rf .web \
 && mkdir -p /app/uploaded_files /app/data

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1/ping', timeout=3)" || exit 1

CMD ["/start.sh"]
