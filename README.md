# Hermes AI Agent System

개인용 로컬 AI 에이전트를 **멀티 프로필 · 멀티 채널 오케스트레이션 플랫폼**으로 확장한 프로젝트입니다.
오픈소스 에이전트 프레임워크 위에 Discord 게이트웨이, cron 기반 자동화, Obsidian 연동 학습 튜터 에이전트를 직접 설계·구축하여 WSL2 + Docker 환경(`restart: unless-stopped`)에서 상시 운영했습니다. 실제 cron 실행 기록 기준 일일 퀴즈 작업이 34회, 주간 AI 트렌드 리포트가 6회 수행된 이력이 있습니다.

> 이 저장소는 실제 운영 스냅샷에서 API 키·토큰·개인 식별 정보를 전부 제거하고 플레이스홀더로 치환한 **포트폴리오 공개용 버전**입니다.

---

## 1. 프로젝트 개요

| 항목 | 내용 |
|---|---|
| 목적 | 개인 AI 비서를 상시 운영 가능한 형태로 구축하고, 그 위에 실사용 자동화(학습 튜터·퀴즈 봇)를 얹기 |
| 운영 환경 | Windows + WSL2 + Docker |
| 코어 프레임워크 | [Hermes Agent](https://github.com/nousresearch/hermes-agent) (Nous Research, MIT License) — vendored & 커스터마이징 |
| 직접 설계·구현한 부분 | 멀티 프로필 게이트웨이 구성, Discord 자동화(cron), 학습 튜터 에이전트(SOUL/스킬/퀴즈 시스템), Docker 배포 구성 |
| 그대로 가져와 운영한 부분 | WhatsApp 브릿지(Baileys) — Hermes Agent 공식 모듈을 배포·운영 |
| LLM Provider | Alibaba Cloud DashScope (Qwen 3.5 Plus) |

---

## 2. 아키텍처

하나의 컨테이너 안에서 **두 개의 독립된 에이전트 게이트웨이**(루트 오케스트레이터 + 전용 학습 에이전트)를 동시에 구동하고, 작업 위임은 크론/칸반을 통해 이루어지도록 설계했습니다.

```mermaid
flowchart TB
    subgraph Docker["Docker Container (WSL2)"]
        direction TB
        Entry["entrypoint.sh<br/>(멀티 게이트웨이 부트스트랩)"]
        Root["default gateway<br/>(헤르메스 · 루트 오케스트레이터)"]
        CS["cs-ai-learning gateway<br/>(학습 전용 에이전트)"]
        Entry --> Root
        Entry --> CS
    end

    Discord["Discord<br/>(멀티 스레드)"]
    WhatsApp["WhatsApp<br/>(Baileys 브릿지, Node.js)"]
    Cron["Cron Jobs<br/>(정기 리포트 · 퀴즈 자동 생성)"]
    Obsidian["Obsidian Vault<br/>(퀴즈 · 오답노트 · 개념노트)"]
    LLM["Alibaba DashScope<br/>Qwen 3.5 Plus"]

    Discord <--> Root
    WhatsApp <--> Root
    Cron --> Root
    Root -- "위임: kanban + notify-subscribe" --> CS
    CS --> Obsidian
    Root --> LLM
    CS --> LLM
```

**설계 포인트**
- **역할 분리**: 루트 에이전트(`SOUL.md`)는 의도 분류·작업 위임만 담당하고, 도메인 지식(Java/Spring/CS/AI 퀴즈)은 전용 프로필(`cs-ai-learning`)에 위임 — 위임은 `delegate_task`가 아닌 **칸반 카드 생성 + 알림 구독** 방식을 사용해, 하위 에이전트가 자신의 모델·페르소나·기억을 그대로 유지하도록 함
- **멀티 게이트웨이 동시 구동**: `entrypoint.sh`가 대시보드/루트 게이트웨이/학습 게이트웨이를 백그라운드로 함께 띄우고, 재시작 시 `gateway_state.json`을 강제 초기화해 상태 충돌을 방지
- **네트워크 안정성**: 스냅샷 시점 `cron/jobs.json`을 보면 5개 cron job 모두 최근 실행이 `Discord send failed: ... [Temporary failure in name resolution]` / `[Network is unreachable]` 오류로 실패해 있었습니다 — 이 WSL2/Docker 환경의 Discord DNS 해석 문제에 대응하기 위해 `hermes-docker/docker-compose.yml`에서 Cloudflare IP로 `extra_hosts`를 고정하는 하드닝 버전을 별도로 구성했습니다 (s6-overlay 기반 프로세스 감독 포함)

---

## 3. 주요 기능

### 🤖 멀티 프로필 에이전트 오케스트레이션
- 루트(default) 에이전트가 요청 의도를 분류해 반복 작업은 **cron**, 1회성 추적 작업은 **칸반 카드**로 위임
- 프로필별로 독립된 `config.yaml` / `SOUL.md` / 메모리 스코프를 가짐 (`cs-ai-learning`은 자체 Discord 게이트웨이 없이 루트로부터의 위임만 받는 구조)

### 💬 Discord 멀티스레드 자동화
- 요일별 cron 자동화 5종으로 학습 스레드에 퀴즈·리포트를 전달 (아래 "자동화 파이프라인" 참고)
- 실시간 인터랙티브 퀴즈(`/quiz start` 명령, `scripts/discord-quiz-orchestrator.py` / `discord-quiz-bot.py`)는 세션 관리·채점 로직까지 설계했으나, Discord 메시지 실시간 폴링 연동은 프로토타입 단계에 머물렀습니다 — `QUIZ-SETUP-COMPLETE.md`에도 "Discord 메시지 명령 (구현 필요)"로 명시되어 있고, 실제 코드에도 `user_answer = "A"  # 기본값 (실제로는 사용자 입력)` 같은 스텁이 남아있습니다

### 📱 WhatsApp 연동 (Hermes Agent 공식 브릿지 모듈 배포·운영)
- `scripts/whatsapp-bridge/`는 Hermes Agent 프로젝트의 공식 Baileys 브릿지를 그대로 가져와 배포한 것입니다 (직접 작성한 코드 아님 — vendored, `hermes-agent/scripts/whatsapp-bridge/`와 100% 동일)
- 셀프챗 모드 / 봇 모드, LID(Linked Identity Device)·전화번호 양방향 매핑 얼로우리스트, 동시 발송 직렬화 큐(#33360 크로스챗 오염 방지), 재연결 타임아웃 가드, 미디어 다운로드 실패 노출(nanoclaw#2895), DNS 리바인딩 방어(GHSA-ppp5-vxwm-4cf7) 등을 이미 갖춘 상태로 제공됨
- 이 모듈을 실제로 컨테이너에 배포하고, Discord 게이트웨이와 함께 멀티채널 구조로 동작하도록 설정·운영한 것이 본인의 작업 범위입니다

### 🎓 CS/AI 학습 튜터 에이전트 (`cs-ai-learning` 프로필)
- 20년차 백엔드 튜터 페르소나, Java/Spring 중심 실무 코드 + 상세 주석
- **3단계 점진적 힌트** 시스템(키워드 → 코드 스니펫 → 유사 코드 완성본) 후 정답 제공, 퀴즈 최초 응답에는 정답·해설을 절대 포함하지 않도록 강제
- 오답노트 자동 생성 → Obsidian 위키링크로 개념노트와 연결 → 주간 `99_MOC` 인덱스에 자동 반영
- 주간 복습 퀴즈: 오답 빈도 기반 가중 재출제 로직 (오답 최다 30% · 차순위 20% · 중요개념 10% · 랜덤 40%, 과목 비율 CS 30%/AI 40%/Programming 30%)
- 오답노트에 "다음 복습일 / 간격 / 숙련도" 필드를 두고 `minesync_enabled` 설정 플래그를 마련해 외부 간격 반복(spaced repetition) 도구(MineSync)와 연동할 수 있는 구조를 잡아둠 — 다만 실제 MineSync API 호출 코드는 없고, 현재는 고정값을 기록하는 자리표시자 수준

### 🧩 스킬 생태계
- **번들 마켓플레이스 스킬** 16개 카테고리(apple, github, devops, research, mlops, social-media 등) — hermes-agent의 공식 Skills Hub(`hermes skills install`/`browse`)를 통해 설치되어 필요 시 바로 활용 가능한 상태
- **직접 작성한 커스텀 스킬** 2종: `learning-agent`(퀴즈/채점/오답노트/Obsidian 동기화), `discord-quiz-workflow`(Discord 인터랙티브 퀴즈 진행)
- 사용 빈도를 추적해 오래 안 쓴 스킬을 자동으로 stale 처리하는 **스킬 큐레이터**가 주기적으로 실행됨 (`skills/.curator_state`, `.usage.json`)

### ⏰ 자동화 파이프라인 (`cron/jobs.json`)

| 작업 | 스케줄 | 설명 | 실행 이력(`completed`) |
|---|---|---|---|
| AI 에이전트 트렌드 보고 | 매주 금요일 08:00 | 웹 검색으로 최신 AI 에이전트/멀티에이전트 동향을 한국어로 요약해 보고 | 6회 |
| 일일 학습 퀴즈 & 리포트 | 매일 09:00 | `learning-agent.py` 실행 → CS/AI 퀴즈 생성 + 일일 리포트를 Obsidian에 저장 | 34회 |
| 알고리즘 스터디 리마인드 | 매주 화요일 20:00 | 스터디 준비/복습 내용 확인 및 지원 | 6회 |
| 주간 복습 퀴즈 | 매주 금요일 10:00 | `learning-agent` 스킬을 통해 그 주 출제됐던 문제 중 30문제를 가중치 기반으로 재출제 | 5회 |
| 월간 퀴즈 정리 | 매월 1일 02:00 | 생성된 지 30일 지난 퀴즈 문서를 Obsidian 볼트에서 정리 | 1회 |

*(실행 이력은 스냅샷 시점 `cron/jobs.json`의 `repeat.completed` 값 기준 — 단, 5개 작업 모두 가장 최근 실행은 Discord 연결 오류로 실패한 상태였습니다. 아래 "알려진 이슈" 참고)*

---

## 4. 기술 스택

- **에이전트 코어**: Hermes Agent (Python), 멀티 에이전트/멀티 채널 게이트웨이 프레임워크
- **LLM**: Alibaba Cloud DashScope(Qwen 3.5 Plus), OpenAI-compatible 엔드포인트. `config.yaml`에는 OpenRouter/Bedrock/Kimi/MiniMax 등으로의 fallback 설정 예시가 문서화되어 있으나 현재는 주석 처리되어 비활성 상태
- **메모리/컨텍스트**: 컨텍스트 압축(`compression`) 및 `mnemosyne` 기반 장기 메모리 관리가 활성화되어 있음
- **보안**: hermes-agent 프레임워크가 기본 제공하는 시크릿 마스킹(`redact_secrets`)·사전 실행 스캐닝(`tirith`) 기능 — `config.yaml`에는 커스텀 옵션 예시가 주석으로 문서화되어 있을 뿐, 별도로 재정의하지는 않고 프레임워크 기본값을 그대로 사용
- **메시징 연동**: Discord(네이티브 툴셋), WhatsApp(Baileys 기반 — Hermes Agent 공식 브릿지 모듈 배포·운영)
- **자동화**: Cron 기반 스케줄링, Kanban 기반 작업 위임
- **지식 관리**: Obsidian(마크다운 + 위키링크 + 프론트매터 스키마)
- **인프라**: Docker, Docker Compose, WSL2, s6-overlay 기반 프로세스 관리

---

## 5. 테스트 및 안정성

`scripts/whatsapp-bridge/`(Hermes Agent 공식 브릿지, vendored)에는 실제 운영 장애를 회귀 테스트로 남긴 유닛 테스트가 포함되어 있으며, 배포 전 이를 그대로 실행해 신뢰성을 확인했습니다.

| 테스트 파일 | 검증 대상 |
|---|---|
| `allowlist.test.mjs` | 전화번호 ↔ LID 매핑 해석, 빈 얼로우리스트는 전원 차단(#8389 회귀 방지) |
| `owner_message_gate.test.mjs` | 본인이 직접 보낸 메시지의 포워딩 여부 분류(에코/비활성/얼로우리스트 불일치/정상 전달) |
| `bridge.reconnect.test.mjs` | 재연결 스케줄러가 실패 시 반드시 재시도하고 성공 시 멈추는지, 버전 조회가 타임아웃 내에 반드시 완료되는지 검증 |
| `bridge.sendqueue.test.mjs` | 동시 발송 요청이 항상 FIFO로 직렬화되는지(#33360 크로스챗 오염 회귀 방지) |
| `bridge.native.test.mjs` | 인용/미디어/위치/투표 메시지 파싱과 미디어 다운로드 실패 처리 |

`node --test scripts/whatsapp-bridge/*.test.mjs` 로 실행할 수 있습니다. (테스트 코드 자체는 Hermes Agent 프로젝트의 일부이며, 본인이 작성한 것은 아닙니다.)

---

## 6. 디렉토리 구조

```
.
├── SOUL.md                    # 루트 에이전트 정체성/역할 정의
├── config.yaml                # 루트 에이전트 운영 설정
├── entrypoint.sh              # 멀티 게이트웨이 부트스트랩 스크립트
├── docker-compose.root.yml    # 기본 Docker 구성
├── hermes-docker/             # 커스텀 Docker 구성 (DNS 고정, s6 서비스 등)
├── cron/jobs.json             # 정기 자동화 작업 정의
├── AI_Agent/                  # Windows/WSL 폴더 연동 설정 가이드 (초기 버전)
├── profiles/
│   └── cs-ai-learning/        # 학습 전용 독립 에이전트 프로필
├── skills/
│   ├── learning-agent/        # 퀴즈 생성·채점·오답노트 스킬 (직접 작성)
│   ├── discord-quiz-workflow/ # Discord 인터랙티브 퀴즈 워크플로우 (직접 작성)
│   └── (기타 마켓플레이스 번들 스킬 다수)
├── scripts/
│   ├── learning-agent*.py     # 일일 자동 퀴즈 / 대화형 CLI
│   ├── discord-quiz-*.py      # Discord 퀴즈 세션 관리·채점
│   └── whatsapp-bridge/       # WhatsApp 연동 브릿지 (Hermes Agent 공식 모듈, vendored)
├── DISCORD-QUIZ-GUIDE.md      # Discord 인터랙티브 퀴즈 사용 가이드
├── LEARNING-AGENT-README.md   # 학습 에이전트 종합 가이드
├── QUIZ-SETUP-COMPLETE.md     # 퀴즈 시스템 구축 기록
├── java-collections-quiz.md   # 생성된 퀴즈 예시 (HashSet)
└── hermes-agent/              # 오픈소스 에이전트 프레임워크 본체 (vendored, MIT)
```

---

## 7. 시작하기

> 실제 배포 시 아래 플레이스홀더 값(`YOUR_*`, `D:\YourVault` 등)을 본인 환경에 맞게 교체하세요.

```bash
# 1. 시크릿 설정 (실제 값은 절대 저장소에 커밋하지 않음)
cp .env.example ~/.hermes/.env
# ~/.hermes/.env 에 DASHSCOPE_API_KEY, DISCORD_BOT_TOKEN, HERMES_DASHBOARD_BASIC_AUTH_* 등 실제 값 입력

# 2. Docker로 실행
docker compose -f docker-compose.root.yml up -d
# 또는 DNS 고정 + s6 감독이 포함된 하드닝 버전
docker compose -f hermes-docker/docker-compose.yml up -d

# 3. WhatsApp 브릿지 (선택)
cd scripts/whatsapp-bridge && npm install && npm start
```

설정 파일(`config.yaml`, `cron/jobs.json` 등)의 Discord 채널/유저 ID는 전부 `YOUR_DISCORD_*_ID` 형태의 플레이스홀더이므로, 본인의 실제 Discord 채널/유저 ID로 교체해야 동작합니다.

---

## 8. 보안 참고사항

- 이 저장소에는 **실제 API 키·토큰·비밀번호가 포함되어 있지 않습니다.** 모든 `.env.example`은 값이 없는 템플릿이며, 실제 시크릿은 로컬 `~/.hermes/.env`에서만 관리됩니다.
- Discord 채널/스레드/유저 ID, 로컬 사용자명, 개인 볼트 경로 등 운영 중 노출됐던 식별자는 공개 전 전부 플레이스홀더로 치환했습니다.
- hermes-agent 프레임워크 자체가 `redact_secrets`(시크릿 마스킹)를 기본값으로 켜두고 있어, 별도 설정 없이도 툴 출력·로그에서 API 키/토큰 패턴이 자동으로 가려집니다.
- WhatsApp 브릿지는 루프백 전용 바인딩과 Host 헤더 검증으로 DNS 리바인딩 공격을 방어하도록 구성되어 있습니다.

---

## 9. 알려진 이슈 및 진행 중인 작업

스냅샷을 있는 그대로 정직하게 남깁니다.

- **Discord 연결 오류**: 스냅샷 시점 `cron/jobs.json` 기준 5개 cron job 모두 가장 최근 실행이 `Discord send failed: ... [Temporary failure in name resolution]` 또는 `[Network is unreachable]` 오류로 실패했습니다. WSL2/Docker 환경의 DNS 해석 문제로 추정되며, 이를 해결하기 위해 `hermes-docker/docker-compose.yml`에 Cloudflare IP 고정(`extra_hosts`) 설정을 추가했습니다.
- **Discord 인터랙티브 퀴즈 미완성**: `/quiz start` 같은 실시간 Discord 명령형 퀴즈는 세션 관리·채점 로직(`discord-quiz-orchestrator.py`, `discord-quiz-bot.py`)까지는 설계했지만, 실제 Discord 메시지 실시간 폴링 연동은 프로토타입 단계입니다. `QUIZ-SETUP-COMPLETE.md`에도 "구현 필요"로 명시되어 있고, 코드에도 `사용자 답변 대기 (실제로는 메시지 폴링)` 주석과 함께 답변을 하드코딩된 기본값(`"A"`)으로 처리하는 부분이 남아 있습니다. 실제로 안정적으로 동작한 것은 **cron 기반 일일 퀴즈 생성**(`learning-agent.py`, 34회 실행 이력) 쪽입니다.

---

## 10. 라이선스 및 출처

- 에이전트 코어 프레임워크와 WhatsApp 브릿지 모듈(`scripts/whatsapp-bridge/`)은 [nousresearch/hermes-agent](https://github.com/nousresearch/hermes-agent) (MIT License)를 그대로 가져온 것입니다.
- 그 위의 멀티 프로필 오케스트레이션 설계, Discord 자동화(cron/칸반 위임), 학습 튜터 에이전트(SOUL·스킬·퀴즈 시스템), Docker 배포 구성(DNS 고정, 멀티 게이트웨이 부트스트랩 등)은 본인이 직접 설계·구현했습니다.

---

**Author**: [SeoHana0825](https://github.com/SeoHana0825)
