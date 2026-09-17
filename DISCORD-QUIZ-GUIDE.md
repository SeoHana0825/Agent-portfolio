# 🎓 Discord 인터랙티브 퀴즈 시스템

## 📋 개요

Discord 에서 직접 퀴즈를 풀고 실시간으로 채점받는 시스템입니다.

### 주요 기능

- ✅ **10 문제 퀴즈** - 과목별 10 문제씩 생성
- ✅ **Discord 연동** - Discord 에서 문제 표시 및 답변 수신
- ✅ **실시간 채점** - 답변 즉시 피드백
- ✅ **오답노트 자동화** - 틀린 문제 Obsidian 에 자동 기록
- ✅ **학습 통계** - 완료 후 상세 리포트

---

## 🚀 빠른 시작

### 1. 퀴즈 시작 명령

Discord 학습 스레드에서 다음 명령을 사용하세요:

```
/quiz start CS "Operating System"
```

또는:

```
/quiz start AI "Machine Learning"
```

### 2. 이용 가능한 과목

| 과목 | 주제 |
|------|------|
| **CS** | Operating System, Database, Network, Data Structures, Algorithms |
| **AI** | Machine Learning, Deep Learning, Neural Networks, NLP, Computer Vision |

---

## 📝 퀴즈 진행 방식

### 단계 1: 퀴즈 시작

```
에이전트: 🎓 CS - Operating System 퀴즈

         📝 문제 수: 10 개
         ⏱️ 제한시간: 문제당 30 초
         💡 답변 방법: A, B, C, D 중 하나를 메시지로 보내주세요!
         
         퀴즈를 시작하려면 `시작` 또는 `start` 라고 보내주세요!
```

### 단계 2: 문제 출제

```
📝 퀴즈 1/10

Q1. 가상 메모리의 주요 목적은 무엇인가요?

A. 디스크 공간 절약
B. 물리 메모리의 한계 극복
C. CPU 속도 향상
D. 네트워크 통신 최적화

---
⏱️ 제한시간: 30 초
```

### 단계 3: 답변 및 채점

**사용자가 `B` 라고 답변:**

```
✅ **정답입니다!**

💡 **해설:** 가상 메모리는 물리 RAM 보다 큰 프로그램을 실행할 수 있게 
         하며, 메모리 단편화를 해결합니다.

---
다음 문제까지 3 초...
```

**사용자가 `A` 라고 답변 (오답):**

```
❌ **오답입니다. 정답: B**

💡 **해설:** 가상 메모리의 핵심은 물리 메모리 크기 제한을 극복하는 것입니다.

📝 오답노트에 기록되었습니다.
```

### 단계 4: 완료 리포트

```
🎉 퀴즈 완료!

📊 결과
- 정답: 8/10
- 정답률: 80%

📝 오답노트: 2 개 기록됨
📁 위치: D:\YourVault\학습\CS\Operating-System\오답노트\

💪 화이팅!
```

---

## 🔧 명령어

### Discord 에서 실행

```bash
# CS 운영체제 퀴즈
/quiz start CS "Operating System"

# AI 머신러닝 퀴즈
/quiz start AI "Machine Learning"

# 커스텀 설정
/quiz start --subject CS --topic "Network" --count 10
```

### 터미널에서 실행

```bash
# 인터랙티브 퀴즈 시작
python3 /opt/data/scripts/discord-quiz-orchestrator.py

# CS 운영체제 퀴즈
python3 /opt/data/scripts/discord-quiz-orchestrator.py --subject CS --topic "Operating System"
```

---

## 📁 파일 구조

```
/opt/data/scripts/
├── discord-quiz-orchestrator.py    # 메인 오케스트레이터
├── discord-quiz-bot.py             # Discord 봇 로직
├── learning-agent.py               # 일일 자동 퀴즈
└── learning-agent-cli.py           # 대화형 CLI

/opt/data/skills/
└── discord-quiz-workflow/
    └── SKILL.md                    # 워크플로우 문서

D:\YourVault\학습\
├── CS\
│   └── Operating-System\
│       ├── 퀴즈\
│       └── 오답노트\
└── AI\
    └── Machine-Learning\
        ├── 퀴즈\
        └── 오답노트\
```

---

## ⚙️ 설정

### Discord 채널

- **학습 스레드 ID:** `YOUR_DISCORD_LEARNING_THREAD_ID`
- **알림:** 모든 퀴즈 활동
- **타임아웃:** 30 초/문제

### Obsidian 연동

- **Vault 경로:** `/mnt/d/YourVault` (Windows: `D:\YourVault`)
- **오답노트 폴더:** `학습/{과목}/{주제}/오답노트/`
- **태그:** `#오답노트`, `#review-needed`, `#{과목}`

---

## 📊 채점 규칙

| 항목 | 규칙 |
|------|------|
| **정답** | +1 점 |
| **오답** | 0 점 (오답노트 자동 생성) |
| **미답변** | 0 점 (30 초 타임아웃) |
| **정답률** | (정답 수 / 10) × 100 |

---

## 🎯 오답노트 자동 생성

오답 시 자동으로 다음과 같은 형식의 파일이 생성됩니다:

```markdown
---
created: 2026-08-07
subject: CS
topic: Operating System
status: review-needed
tags: [오답노트, CS, review-needed]
---

# 오답노트

## 📝 문제
가상 메모리의 주요 목적은 무엇인가요?

## ✍️ 내 답변
A

## ✅ 정답
B

## 💡 피드백
가상 메모리의 핵심은 물리 메모리 크기 제한을 극복하는 것입니다.

## 🔄 복습 기록
| 날짜 | 상태 | 비고 |
|------|------|------|
| 2026-08-07 | review-needed | 초기 기록 |
```

---

## 💡 팁

1. **매일 퀴즈** - 매일 오전 9 시 자동 퀴즈 + 수시 인터랙티브 퀴즈
2. **오답 복습** - 오답노트는 다음 날 반드시 복습
3. **점수 추적** - 정답률이 80% 이상일 때까지 반복
4. **친구와 경쟁** - Discord 에서 친구와 점수 공유

---

## 🛠️ 문제 해결

### Q: 퀴즈가 시작되지 않아요

A: 다음을 확인하세요:
- Discord 채널이 학습 스레드인지 확인
- `시작` 또는 `start` 메시지 전송
- Hermes 연결 상태 확인

### Q: 채점이 안 돼요

A: 다음을 확인하세요:
- 답변이 `A`, `B`, `C`, `D` 중 하나인지 확인
- 대소문자 구분 없음 (a, A 모두 가능)
- 30 초 이내 답변

### Q: 오답노트가 생성되지 않아요

A: 다음을 확인하세요:
- `D:\YourVault` 폴더 존재 확인
- 쓰기 권한 확인
- 파일명 중복 확인

---

## 📚 관련 문서

- [학습 에이전트](learning-agent)
- [Obsidian 연동 가이드](references/obsidian-schema.md)
- [Discord 도구 사용법](discord)

---

**💪 Discord 에서楽しく 학습하세요!**
