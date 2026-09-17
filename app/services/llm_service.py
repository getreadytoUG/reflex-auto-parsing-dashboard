"""재사용 가능한 LLM/VLM 클라이언트 팩토리.

매번 새 인스턴스를 만드는 팩토리 함수로 둔다 — 호출부마다 temperature 등을
다르게 넘길 수 있어야 하므로 싱글턴으로 고정하지 않는다.
"""

from __future__ import annotations

from langchain_openai import ChatOpenAI

from app import config


def get_llm(**overrides) -> ChatOpenAI:
    return ChatOpenAI(
        api_key=config.OPENAI_API_KEY,
        base_url=config.OPENAI_BASE_URL,
        model=config.MODEL_NAME,
        **overrides,
    )


def get_vlm(**overrides) -> ChatOpenAI:
    return ChatOpenAI(
        api_key=config.VLM_API_KEY,
        base_url=config.VLM_BASE_URL,
        model=config.VLM_MODEL_NAME,
        **overrides,
    )
