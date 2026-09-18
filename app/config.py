"""내부망 환경변수를 한 곳에서 읽어 서비스 계층에 제공한다.

값이 없어도 import 자체는 실패하지 않는다 (로컬 개발 시 일부만 채워 쓸 수 있게).
실제로 값이 필요한 시점(서비스 함수 호출 시)에 비어있으면 명확한 에러를 낸다.
"""

import os

from dotenv import load_dotenv

load_dotenv()

DRM_BASE_URL = os.getenv("DRM_BASE_URL")
UPLOAD_BASE_URL = os.getenv("UPLOAD_BASE_URL")
DELETE_BASE_URL = os.getenv("DELETE_BASE_URL")

QDRANT_BASE_URL = os.getenv("QDRANT_BASE_URL")
PARENT_COLLECTION = os.getenv("PARENT_COLLECTION")
CHILD_COLLECTION = os.getenv("CHILD_COLLECTION")

API_BASE_URL = os.getenv("API_BASE_URL")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

VLM_API_KEY = os.getenv("VLM_API_KEY")
VLM_BASE_URL = os.getenv("VLM_BASE_URL")
VLM_MODEL_NAME = os.getenv("VLM_MODEL_NAME")
