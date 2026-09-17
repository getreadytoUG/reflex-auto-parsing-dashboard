# 새 파싱 방법(Method) 추가하기

"파싱 방법"은 Documents 페이지의 "기본 Parser 프로필" 토글 아래 라디오 버튼으로 보이는
Gemma / MinerU / OpendataLoader 같은 항목을 말합니다. 형식(PDF/HWP/...)을 다루는
`app/parsers/contracts.py`의 `ParserAdapter`와는 다른 축으로, "어떤 엔진/모델로 파싱할지"를
고르는 값입니다. 건전지처럼 클래스 하나 넣었다 뺐다 할 수 있게 만들어져 있습니다.

작업은 **`app/parsers/methods.py` 한 파일**에서만 하면 됩니다. 다른 파일은 손댈 필요 없습니다.

## 1. 클래스 추가

`app/parsers/methods.py`에 클래스를 하나 만듭니다. `name`(문자열)과
`parse(document, options)` 메서드만 있으면 `ParsingMethod` Protocol을 만족합니다
([app/parsers/methods.py:12-16](app/parsers/methods.py)).

```python
class MyNewMethod:
    name = "MyNew"

    def parse(self, document: DocumentInput, options: ParseOptions) -> ParseResult:
        # 실제 파싱 로직 구현
        ...
        return ParseResult(
            job_id=...,
            document_id=document.document_id,
            parser_name=self.name,
        )
```

- `document`/`options`/`ParseResult`는 `app/parsers/contracts.py`에 정의된 공용 타입입니다.
- VLM/LLM이 필요하면 `app/services/llm_service.py`의 `get_llm()` / `get_vlm()`을 그대로
  가져다 쓰면 됩니다 (Gemma가 VLM을 쓸 것을 염두에 두고 만든 공용 클라이언트입니다).

## 2. 레지스트리에 등록

같은 파일 아래쪽의 `PARSING_METHODS` 딕셔너리에 인스턴스를 추가합니다.

```python
PARSING_METHODS: dict[str, ParsingMethod] = {
    m.name: m
    for m in (
        GemmaMethod(),
        MinerUMethod(),
        OpendataLoaderMethod(),
        MyNewMethod(),  # 추가
    )
}
```

이게 끝입니다. 아래 두 곳이 이 딕셔너리를 단일 소스로 참조하므로 UI에 자동으로 반영됩니다.

- `DocumentsState.parsing_methods`가 `PARSING_METHODS.keys()`에서 파생됩니다
  ([app/states/documents_state.py:61](app/states/documents_state.py)).
- 라디오 버튼 UI는 `rx.foreach(DocumentsState.parsing_methods, ...)`로 그 리스트를 그대로
  렌더링합니다 ([app/components/documents_panel.py:46-49](app/components/documents_panel.py)).

`app/states/documents_state.py`나 `app/components/documents_panel.py`는 새 방법을 추가할 때
건드릴 필요가 없습니다.

## 3. 지금 시점의 한계 (아직 안 된 것)

- 현재 세 클래스(`GemmaMethod`, `MinerUMethod`, `OpendataLoaderMethod`) 모두 `parse()`가
  `raise NotImplementedError(...)`만 하는 빈 껍데기입니다. 실제 파싱 로직은 아직 없습니다.
- Documents 표의 "파싱 실행" 버튼([app/components/documents_panel.py:292](app/components/documents_panel.py))은
  아직 어떤 이벤트 핸들러와도 연결되어 있지 않아, 라디오로 방법을 선택해도 실행까지 이어지지
  않습니다. 이 연결은 `TODO.md` 3번/4번 항목(업로드 이후 Job 제출·Worker 실행)이 먼저 갖춰져야
  합니다.
- 즉 지금 할 수 있는 것은 "새 파싱 방법을 목록에 추가하고 선택 가능하게 만드는 것"까지이고,
  그 방법으로 실제 문서를 파싱하는 것은 아직 별도 작업입니다.

## 참고

- 설계 배경: [docs/superpowers/specs/2026-09-17-documents-real-integration-design.md](docs/superpowers/specs/2026-09-17-documents-real-integration-design.md) 5절
- 남은 작업 전체 목록: [TODO.md](TODO.md)
