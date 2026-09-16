## Document Parsing Platform 목업 계획
- [x] 웜 그레이 작업 공간, 네이비·앰버 상태 색상, 조밀한 한국어 업무용 타이포그래피를 일관되게 적용한 공통 Sidebar와 Dashboard 목업을 구성한다. KPI, 파일 유형별 분포, Parser 처리량, 최근 Job 테이블을 현실적인 샘플 데이터로 표현한다.
- [x] Documents와 Parsing Jobs 목업을 구성한다. 업로드 영역, 문서 목록, Parser 선택과 작업 버튼, 상태 필터, 다중 Job 진행률·현재 단계·페이지·오류 상태를 보여주되 실제 업로드·파싱·저장은 수행하지 않는다.
- [x] Validation과 Settings 목업을 구성한다. 원본 미리보기, Markdown/JSON/Block 탭, Heading Tree와 구조 편집 도구, Reparse·Export 버튼, Parser/Worker/Storage 설정 화면을 시각화하고 향후 실제 Parser를 연결할 명확한 Adapter 인터페이스 경계를 마련한다.