# 05. (참고자료) Google Workspace를 코드/CLI로 자동화하기

1일차에는 Apps Script로 Google Workspace를 자동화했습니다. 코드 에이전트를 배운 지금은 선택지가 하나 더 생겼습니다 — **에이전트에게 Workspace API를 직접 다루게 하는 것**입니다. 이 문서는 수업 범위를 넘어서는 참고자료입니다.

## 1. gws — Google Workspace CLI

**[gws](https://github.com/googleworkspace/cli)** 는 Google이 공개한 Workspace용 CLI입니다 (2026년 3월 공개, 오픈소스). Gmail, Drive, Calendar, Sheets, Docs, Chat 등 **모든 Workspace API를 터미널 명령 하나로** 다룰 수 있습니다.

```bash
# 설치 (macOS 기준)
brew install googleworkspace-cli   # 또는 npm install -g @googleworkspace/cli

# 로그인
gws auth login

# 예: 오늘 일정 보기
gws calendar +agenda

# 예: 메일 보내기
gws gmail +send --to someone@company.com --subject "보고서" --body "첨부 확인 부탁드립니다"
```

코드 에이전트 시대에 이 도구가 특히 중요한 이유:

- **모든 응답이 JSON(구조화된 데이터)** 으로 나옵니다 → 에이전트가 읽고 다음 작업에 쓰기 좋습니다.
- **MCP 서버가 내장**되어 있어 Antigravity, Claude Code 같은 에이전트에 바로 연결할 수 있습니다.
- 100개 이상의 에이전트 스킬(SKILL.md)이 함께 배포됩니다.

즉, 03에서 배운 Skills + 02에서 배운 MCP + Workspace가 한 도구로 만납니다. 에이전트에게 "지난주 안 읽은 메일 중 회신 필요한 것만 골라 시트로 정리해줘"라고 시킬 수 있는 기반이 됩니다.

> README에 "공식 지원 제품은 아님(not an officially supported Google product)"이라고 명시된 오픈소스입니다. 사내 도입 시 보안 검토를 거치세요.

> 참고: **GAM**이라는 유명한 도구도 있는데, 이것은 도메인 **관리자**(전체 계정 생성/삭제, 그룹 관리)용입니다. 일반 사용자의 업무 자동화에는 gws가 맞습니다.

## 2. Workspace API로 할 수 있는 것들

API(프로그램끼리 데이터를 주고받는 약속된 창구 — 1일차 03 실습에서 배웠습니다)가 Workspace 서비스마다 열려 있습니다.

| API | 무엇을 조작하나 | 업무 자동화 예시 |
|---|---|---|
| **Gmail API** | 메일 발송·검색·라벨 | 매일 아침 "미답변 고객 문의" 라벨 메일을 모아 요약 발송 / 첨부파일 자동 저장 |
| **Drive API** | 파일·폴더·공유 권한 | 주간 보고 폴더 자동 생성 + 팀 공유 권한 일괄 부여 / 오래된 외부 공유 링크 정리 |
| **Sheets API** | 시트 데이터 읽기/쓰기 | 외부 시스템 데이터를 매일 시트에 적재 / 설문 응답 자동 집계 |
| **Docs API** | 문서 생성·편집 | 시트 데이터로 계약서·송장 대량 생성 / 회의록 템플릿 자동 생성 |
| **Calendar API** | 일정 조회·등록 | 매주 월요일 이번 주 미팅을 모아 시트로 정리 / 온보딩 일정 일괄 등록 |
| **Slides API** | 프레젠테이션 생성 | 월간 실적 시트 → 보고용 슬라이드 자동 변환 |

## 3. Apps Script vs API 직접 호출 — 언제 무엇을 쓰나

| 구분 | Apps Script (1일차) | API 직접 호출 / gws (2일차 이후) |
|---|---|---|
| 실행 위치 | Google 클라우드 안 (서버 불필요) | 내 컴퓨터, 사내 서버, Cloud Run 등 |
| 인증 | 권한 동의 클릭이면 끝 | OAuth 설정 또는 `gws auth login` |
| 언어 | JavaScript만 | Python 등 자유 (에이전트가 알아서 선택) |
| 자동 실행 | 트리거 내장 (시간, 폼 제출 등) | 별도 구성 필요 (Cloud Run + 스케줄러 등) |
| 적합한 일 | Workspace **안에서 완결**되는 가벼운 자동화 | 외부 시스템 연동, 대량 처리, 실행 시간 6분 제한을 넘는 작업 |

판단 기준 한 줄: **"폼 제출 → 시트 기록 → 메일 발송"처럼 Workspace 안에서 끝나면 Apps Script, 외부 데이터·AI·대량 처리가 끼면 API 직접 호출.**

## 4. 해보기 (선택 과제)

Antigravity 에이전트에게 이렇게 시켜보세요.

```text
gws CLI(https://github.com/googleworkspace/cli)를 설치하고 내 계정으로 로그인을 안내해줘.
그 다음, 이번 주 내 캘린더 일정을 모두 가져와서
요일별로 정리한 마크다운 보고서를 만들어줘.
```

권한 승인 카드(설치 명령, 네트워크 접근)와 Google 로그인 동의 화면이 뜨는 것까지가 학습 내용입니다 — 1, 2일차에 배운 모든 권한 개념이 한 번에 등장합니다.
