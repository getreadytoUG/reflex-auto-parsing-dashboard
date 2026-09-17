"""파싱 방법(엔진/모델) 계약 — 형식(PDF/HWP/...) 축인 contracts.ParserAdapter와 달리
'어떤 엔진으로 파싱할지'의 축이라 별도 파일로 분리한다.

contracts.py와 같은 원칙을 따른다: Reflex 미import, 실제 구현 없음.
"건전지처럼 넣었다 뺄 수 있게" — 새 방법 추가 = 클래스 하나 더 만들고
PARSING_METHODS 딕셔너리에 등록하면 끝. UI는 이 딕셔너리의 키에서 옵션을 파생시킨다.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from app.parsers.contracts import DocumentInput, ParseOptions, ParseResult


@runtime_checkable
class ParsingMethod(Protocol):
    name: str

    def parse(self, document: DocumentInput, options: ParseOptions) -> ParseResult: ...


class GemmaMethod:
    name = "Gemma"

    def parse(self, document: DocumentInput, options: ParseOptions) -> ParseResult:
        raise NotImplementedError("Gemma 파싱 방법 미구현")


class MinerUMethod:
    name = "MinerU"

    def parse(self, document: DocumentInput, options: ParseOptions) -> ParseResult:
        raise NotImplementedError("MinerU 파싱 방법 미구현")


class OpendataLoaderMethod:
    name = "OpendataLoader"

    def parse(self, document: DocumentInput, options: ParseOptions) -> ParseResult:
        raise NotImplementedError("OpendataLoader 파싱 방법 미구현")


PARSING_METHODS: dict[str, ParsingMethod] = {
    m.name: m for m in (GemmaMethod(), MinerUMethod(), OpendataLoaderMethod())
}

__all__ = [
    "GemmaMethod",
    "MinerUMethod",
    "OpendataLoaderMethod",
    "PARSING_METHODS",
    "ParsingMethod",
]
