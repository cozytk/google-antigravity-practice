# 01. Antigravity 이해하기

이 문서는 실습을 시작하기 전에 Antigravity가 무엇인지, 화면이 어떻게 생겼는지, 그리고 권한 체계가 어떻게 동작하는지 이해하기 위한 가이드입니다.

설치와 실행은 [SETUP_GUIDE.md](SETUP_GUIDE.md)(실습 0)를 따라 하세요.

## 1. 용어부터: 에이전트, IDE, CLI

본문에 계속 나오는 단어 세 개를 먼저 정리합니다.

| 용어 | 뜻 |
|---|---|
| **에이전트(Agent)** | 목표를 주면 스스로 계획을 세우고, 파일을 읽고 쓰고, 명령을 실행해서 일을 끝내는 AI. 한 번 묻고 한 번 답하는 챗봇과 달리 **여러 단계를 알아서 진행**합니다. |
| **IDE** | Integrated Development Environment(통합 개발 환경). 개발자가 코드를 작성하는 전문 편집 프로그램입니다. 한글 문서를 쓸 때 한컴오피스를 쓰듯, 코드를 쓸 때 IDE를 씁니다. |
| **CLI** | Command Line Interface(명령줄 인터페이스). 마우스로 클릭하는 대신 **터미널이라는 검은 화면에 글자로 명령을 입력**해서 컴퓨터를 조작하는 방식입니다. 반대말은 GUI(그래픽 화면)입니다. |

## 2. Antigravity란?

**Antigravity는 Google이 만든 "에이전트 우선(agent-first)" 작업 플랫폼입니다.** AI 에이전트가 코드 작성, 터미널 명령 실행, 웹 브라우저 조작까지 스스로 수행하고, 사람은 에이전트가 만들어 내는 산출물(계획서, 작업 결과 요약, 스크린샷)을 검토하고 피드백하는 방식으로 협업합니다.

> 공식 소개: "Antigravity 2.0은 AI 에이전트들의 중앙 관제 센터(central command center)로, 에이전트를 띄우고, 지켜보고, 조율하는 통합 플랫폼입니다." — [공식 문서](https://antigravity.google/docs/overview)

기존 AI 채팅(Gemini 웹)과의 가장 큰 차이는 **AI가 내 컴퓨터에서 직접 일한다**는 점입니다.

| | Gemini 웹 채팅 | Antigravity 에이전트 |
|---|---|---|
| 결과물 | 텍스트 답변 | 실제 파일, 실행되는 프로그램 |
| 작업 방식 | 한 번 묻고 한 번 답함 | 계획 → 실행 → 검증을 스스로 반복 |
| 내 컴퓨터 접근 | 불가 | 파일 읽기/쓰기, 명령 실행, 브라우저 조작 |
| 사람의 역할 | 질문하기 | 목표 제시, 계획 승인, 결과 검토 |

Antigravity가 내세우는 협업 철학은 네 가지입니다 ([출시 블로그](https://antigravity.google/blog/introducing-google-antigravity)): **신뢰(Trust)** — 에이전트의 모든 행동을 일일이 지켜보는 대신 검증하기 쉬운 산출물로 보고받기, **자율성(Autonomy)** — 에이전트에게 충분한 도구와 권한 주기, **피드백(Feedback)** — 문서에 댓글 달듯 산출물에 코멘트 남기기, **자가개선(Self-improvement)** — 피드백에서 배우기.

## 3. Antigravity 2.0 / Antigravity IDE / Antigravity CLI

이름이 비슷한 세 가지가 있어서 처음에 헷갈리기 쉽습니다. **이번 수업에서 쓰는 것은 Antigravity 2.0 (데스크톱 GUI 앱)입니다.**

| 구분 | 형태 | 출시 | 설명 |
|---|---|---|---|
| **Antigravity IDE** (구버전) | 데스크톱 IDE | 2025년 11월 | VS Code 계열의 코드 편집기 안에 에이전트가 들어 있는 형태. 개발자 친화적 |
| **Antigravity 2.0** ✅ | **독립 데스크톱 앱 (GUI)** | 2026년 5월 (Google I/O) | IDE가 아닌 별도 앱. 코드 편집기 없이 에이전트와의 대화와 산출물 검토가 중심 |
| **Antigravity CLI** | 터미널 앱 (명령어 `agy`) | 2026년 5월 | 같은 에이전트 엔진을 터미널에서 쓰는 버전. 설정과 권한이 2.0과 자동 동기화 |

![Antigravity IDE(검은 그리드)와 2.0(흰 배경)의 앱 아이콘 비교](https://antigravity.google/assets/image/blog/app-icons.png)

왜 2.0이 따로 나왔을까요? Google은 "코딩을 넘어 모든 종류의 지식 노동(deep research, 문서 작업 등)을 위한 인터페이스"로 확장하기 위해 에이전트 화면을 IDE에서 분리했다고 설명합니다. 기존 IDE는 당분간 유지되지만, 에이전트 관리 기능은 점차 2.0으로 옮겨집니다. ([2.0 출시 블로그](https://antigravity.google/blog/introducing-google-antigravity-2-0))

> 참고: 터미널을 즐겨 쓰는 개발자용 도구였던 **Gemini CLI**는 Antigravity CLI로 통합이 진행 중입니다. 첫 실행 시 기존 Gemini CLI 설정을 자동으로 가져올 수 있습니다. ([마이그레이션 문서](https://antigravity.google/docs/gcli-migration))

![Antigravity 2.0의 에이전트 우선 레이아웃](https://antigravity.google/assets/image/blog/agy2-layout.jpg)

## 4. 주요 인터페이스와 기능 (공식 문서 기반)

### 4.1 Projects — 폴더가 곧 프로젝트

Antigravity에서 **내 컴퓨터의 폴더 하나가 프로젝트 하나**가 됩니다. 에이전트는 그 폴더 안에서만 기본적으로 일하고, 설정과 권한도 프로젝트 단위로 관리됩니다. 자세한 동작 원리는 [02_code_agent_context](../02_code_agent_context/README.md)에서 다룹니다.

### 4.2 모델 선택

대화 입력창 아래의 모델 선택 드롭다운에서 에이전트의 두뇌가 될 AI 모델을 고를 수 있습니다. Gemini 계열 외에 Anthropic의 Claude 모델도 선택할 수 있습니다.

![모델 선택 드롭다운](https://antigravity.google/assets/image/docs/model-selector.png)

### 4.3 Artifacts — 에이전트의 작업 보고서

**Artifact(아티팩트)는 에이전트가 자신의 진행 상황과 생각을 사람에게 보고하기 위해 만드는 구조화된 산출물**입니다. ([공식 문서](https://antigravity.google/docs/artifacts)) 종류는 작업 목록(task list), 구현 계획(implementation plan), 작업 후 요약(walkthrough), 스크린샷, 브라우저 녹화 등입니다.

이 구조가 중요한 이유: 에이전트가 수십 개의 파일을 만지는 동안 그 모든 과정을 사람이 지켜볼 수는 없습니다. 대신 **"검증하기 쉬운 보고서"를 받아서 그것만 검토**하면 됩니다. 회사에서 실무자의 모든 키보드 입력을 보지 않고 기획서와 결과 보고서를 검토하는 것과 같습니다.

**Implementation Plan (구현 계획)** — 에이전트가 코드를 고치기 전에 만드는 기술 계획서입니다. "Proceed" 버튼으로 승인하거나, 마음에 안 드는 부분에 인라인 코멘트를 달아 수정시킬 수 있습니다.

![Implementation Plan 아티팩트](https://antigravity.google/assets/image/docs/artifacts/artifact-implementation-plan.png)

![계획에 인라인 코멘트 남기기](https://antigravity.google/assets/image/docs/artifacts/artifact-implementation-plan-comments.png)

**Walkthrough (작업 요약)** — 작업이 끝난 후 무엇이 어떻게 바뀌었는지 정리한 보고서입니다. 브라우저 작업이 있었다면 스크린샷과 녹화가 함께 들어갑니다.

![Walkthrough 아티팩트](https://antigravity.google/assets/image/docs/artifacts/artifact-walkthrough.png)

**실행 모드** — 에이전트를 시킬 때 두 가지 모드가 있습니다 ([문서](https://antigravity.google/docs/artifact-review)):

| 모드 | 동작 | 언제 |
|---|---|---|
| **Planning Mode** | 작업 목록과 구현 계획을 먼저 만들고 승인을 받은 후 실행 | 중요한 작업, 처음 해보는 작업 |
| **Fast Mode** | 계획 없이 바로 실행 | 사소한 수정, 빠른 실험 |

### 4.4 Browser — 에이전트가 쓰는 브라우저

에이전트는 Chrome을 직접 조작해서 만든 웹 페이지를 열어 보고, 클릭해 보고, 스크린샷을 찍어 검증할 수 있습니다. 이때 **내 브라우저와 분리된 별도 Chrome 프로필**을 사용해서 내 로그인 정보나 쿠키에 접근하지 못하게 격리됩니다. ([문서](https://antigravity.google/docs/separate-chrome-profile))

![브라우저 스크린샷이 아티팩트로 저장된 모습](https://antigravity.google/assets/image/docs/artifacts/browser-screenshot-artifact.png)

### 4.5 슬래시 명령어

대화 입력창에 `/`로 시작하는 명령을 입력하면 특별한 동작을 시킬 수 있습니다. 이번 수업에서 직접 사용할 두 가지:

| 명령 | 설명 |
|---|---|
| `/grill-me` | 에이전트가 구현을 시작하기 **전에** 나에게 역으로 질문을 퍼붓게 합니다. 요구사항이 모호할 때 질의응답으로 계획을 맞춥니다. (grill = 꼬치꼬치 캐묻다) |
| `/goal` | 목표를 주면 중간에 멈춰서 묻지 않고 **목표가 달성될 때까지** 스스로 실행-검증을 반복합니다. |
| `/schedule` | 에이전트 작업을 예약 실행합니다 (매일 아침 보고서 생성 등). |
| `/browser` | 브라우저 사용을 명시적으로 시킵니다. |

### 4.6 그 외 기능 (이름만 알아두기)

- **Dynamic Subagents** — 에이전트가 보조 에이전트를 띄워 작업을 병렬로 나눠 처리
- **Scheduled Tasks** — 예약 실행 ([이미지](https://antigravity.google/assets/image/blog/scheduled-task.png))
- **Voice transcription** — 음성으로 지시 입력
- **JSON Hooks** — 에이전트 동작 전후에 자동으로 실행되는 스크립트 연결 (고급 기능)

## 5. Permissions — 권한 체계 (중요)

코드 에이전트는 강력한 만큼, **무엇을 허용할지 정하는 권한 체계**가 안전의 핵심입니다. Antigravity의 권한 엔진은 다음과 같이 동작합니다. ([공식 문서](https://antigravity.google/docs/permissions))

### 5.1 세 가지 리스트: Deny / Ask / Allow

모든 민감한 동작(파일 쓰기, 명령 실행, 웹 접근 등)은 세 리스트 중 하나에 속합니다.

| 리스트 | 동작 |
|---|---|
| **Deny** | 무조건 차단 |
| **Ask** | 실행 전에 사람에게 물어봄 (승인 카드가 뜸) |
| **Allow** | 자동 승인 |

우선순위는 **Deny > Ask > Allow**입니다. 같은 대상이 여러 리스트에 있으면 더 엄격한 쪽이 이깁니다.

권한이 적용되는 동작의 종류:

| 동작 | 의미 |
|---|---|
| `read_file` / `write_file` | 파일 읽기 / 쓰기 |
| `read_url` | 웹 페이지 읽기 |
| `execute_url` | 웹 페이지에서 클릭, 입력 등 실제 조작 |
| `command` | 터미널 명령 실행 |
| `mcp(서버/도구)` | 외부 연동 도구(MCP) 호출 |

모든 동작에 `*`(전부 허용) 와일드카드를 쓸 수 있습니다. 예를 들어 `read_url(*)`은 "모든 웹사이트 읽기 허용"입니다. **네트워크 접근은 프로젝트에서 따로 `*` 허용을 설정하지 않으면 매번 물어봅니다.**

### 5.2 기본값: 프로젝트 폴더 안은 자유, 밖은 물어보기

설정을 건드리지 않았을 때의 기본 동작:

- 프로젝트 폴더 **안의** 파일 읽기/쓰기 → **자동 허용**
- 그 외 전부(터미널 명령, 폴더 밖 파일, 웹 접근, MCP) → **물어봄(Ask)**

"폴더 안은 에이전트의 작업 책상이니 자유롭게 쓰게 하고, 책상 밖으로 나가는 일은 허락받게 한다"고 이해하면 됩니다.

### 5.3 프로젝트별 권한 vs 기본(글로벌) 권한

권한은 두 층으로 관리됩니다.

| 층 | 적용 범위 | 예 |
|---|---|---|
| **글로벌 권한** | 모든 프로젝트 공통 | "어떤 프로젝트든 `rm -rf`(폴더 통째 삭제)는 Deny" |
| **프로젝트 권한** | 해당 프로젝트만 | "이 프로젝트에서는 `npm` 명령 Allow" |

프로젝트는 글로벌 권한을 **상속**받고, 거기에 프로젝트별 권한을 더할 수 있습니다. 대화 중에 승인 카드에서 허용한 권한은 그 프로젝트에 저장되어 다음부터는 묻지 않습니다 — 쓸수록 내 작업 패턴에 맞게 권한이 학습되는 구조입니다. ([Projects 문서](https://antigravity.google/docs/projects))

### 5.4 터미널 명령 자동 실행 정책

설정의 **Terminal Command Auto Execution**에서 고를 수 있습니다. ([Agent Settings 문서](https://antigravity.google/docs/agent-settings))

| 옵션 | 동작 | 권장 |
|---|---|---|
| **Request Review** | Allow 리스트에 명시된 명령 외에는 전부 물어봄 | ✅ 수업에서는 이걸 사용 |
| **Always Proceed** | Deny 리스트에 있는 것 빼고 전부 자동 실행 | 익숙해진 후에 |

### 5.5 샌드박스 모드

**샌드박스(sandbox)** 란 프로그램을 모래 놀이터처럼 격리된 공간에서 실행해서, 실수하거나 위험한 동작을 해도 바깥(내 컴퓨터 전체)에 영향을 못 주게 하는 기술입니다.

Antigravity의 Terminal Sandboxing(프리뷰)을 켜면 에이전트가 실행하는 터미널 명령이 샌드박스 안에서 돌아갑니다. 이때 파일 권한 설정이 샌드박스의 접근 허용 목록으로, `read_url` 도메인 설정이 네트워크 허용 목록으로 그대로 적용됩니다. 즉 **권한 설정 하나로 파일과 네트워크 격리까지 일관되게 통제**됩니다. ([CLI Sandbox 문서](https://antigravity.google/docs/cli-sandbox))

### 5.6 브라우저 URL Allowlist

에이전트의 웹 접근은 2중 보호됩니다 ([문서](https://antigravity.google/docs/allowlist-denylist)): Google 서버가 관리하는 악성 URL 차단 목록(Denylist) + 내가 관리하는 허용 목록(Allowlist, 초기값은 `localhost`만). 허용 안 된 URL에 접근하려 하면 "Always allow" 버튼이 있는 확인 창이 뜹니다.

![미허용 URL 접근 시 확인 창](https://antigravity.google/assets/image/docs/always-allow-url.png)

## 6. 계정과 데이터 수집

요금제는 무료(개인) / Google AI Pro / Google AI Ultra / 조직용(Google Cloud 경유)으로 나뉩니다. 무료 계정으로도 Gemini와 Claude 모델을 일정 한도 내에서 쓸 수 있습니다. ([요금 안내](https://antigravity.google/pricing))

회사에서 쓸 때 가장 중요한 것은 **데이터 수집 정책**입니다. 아래는 Antigravity Business 계정의 설정 화면입니다.

![Antigravity Business 계정의 텔레메트리 설정 화면](images/account-telemetry-business.png)

화면의 빨간 박스 안내문 요약: **Business 계정은 텔레메트리(사용 데이터 수집)가 비활성화되어 있으며, 프롬프트·코드·모델 응답 내용은 수집하지 않습니다. 기능 사용 여부, 활성 사용자 수 같은 익명화된 일반 사용 통계만 수집합니다.**

Google의 기업용 공식 문구도 같은 방향입니다: "기업의 프롬프트, 응답, 코드, 텔레메트리는 고객의 프라이빗 환경 밖에 저장되지 않습니다." ([기업용 블로그](https://antigravity.google/blog/google-antigravity-for-enterprises))

> ⚠️ 반대로 **개인 무료 계정**은 설정에서 직접 옵트아웃하지 않으면 입력 내용이 모델 개선에 활용될 수 있습니다. 회사 업무 데이터는 반드시 회사 계정 정책 하에서 다루세요.

## 다음 단계

- 설치가 아직이라면 → [SETUP_GUIDE.md](SETUP_GUIDE.md) (실습 0)
- 설치가 끝났다면 → [02_code_agent_context](../02_code_agent_context/README.md)에서 에이전트의 동작 원리를 이해합니다.
