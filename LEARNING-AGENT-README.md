# 🎓 학습 에이전트 (Learning Agent)

AI 기반 개인 학습 튜터 - 퀴즈 생성, 채점, 오답노트 자동 관리

---

## 📋 개요

학습 에이전트는 **매일 자동으로** 학습을 도와주는 독립 AI 에이전트입니다.

### 주요 기능

- ✅ **자동 퀴즈 생성** - 매일 오전 9 시 KST 에 CS/AI 과목 퀴즈 생성
- ✅ **오답노트 자동 정리** - 틀린 문제 Obsidian 에 자동 기록
- ✅ **학습 진도 추적** - 일일/주간 학습 리포트 생성
- ✅ **복습 스케줄링** - MineSync 연동으로 간격 반복 학습
- ✅ **Discord 알림** - 학습 진행 상황 실시간 보고

---

## 🚀 빠른 시작

### 1. 자동 실행 (권장)

매일 오전 9 시에 자동으로 실행됩니다:

```bash
# Cron job 상태 확인
hermes cron list

# 수동으로 즉시 실행
hermes cron run <job_id>
```

### 2. 수동 실행

대话형 CLI 사용:

```bash
python3 /opt/data/scripts/learning-agent-cli.py
```

### 3. 스크립트 직접 실행

```bash
python3 /opt/data/scripts/learning-agent.py
```

---

## 📁 파일 구조

```
D:\YourVault\
└── 학습\
    ├── CS\
        ├── Operating-System\
            ├── 퀴즈\
            │   └── 2026-08-07-Operating-System-퀴즈.md
            └── 오답노트\
                └── 2026-08-07-Operating-System-오답.md
        ├── Database\
        ├── Network\
        └── ...
    ├── AI\
        ├── Machine-Learning\
        ├── Deep-Learning\
        └── ...
    └── 일일 - 학습 - 리포트-2026-08-07.md
```

---

## 📝 사용 예시

### 퀴즈 생성 (자동)

매일 오전 9 시 자동 생성:

```
📅 2026-08-07 09:00 KST
✅ CS - Operating System 퀴즈 생성
✅ AI - Machine Learning 퀴즈 생성
✅ 일일 학습 리포트 생성
```

### 퀴즈 예시

```markdown
# CS - Operating System 퀴즈

**난이도:** medium  
**문제 수:** 5  

---

## Q1. 가상 메모리의 주요 목적은 무엇인가요?

A. 디스크 공간 절약
B. 물리 메모리의 한계 극복
C. CPU 속도 향상
D. 네트워크 통신 최적화

---

## 정답 및 해설

### Q1 정답: B
가상 메모리는 물리 RAM 보다 큰 프로그램을 실행할 수 있게 하며, 
메모리 단편화를 해결합니다.
```

### 오답노트 예시

```markdown
---
created: 2026-08-07
subject: CS
topic: Operating System
status: review-needed
tags: [오답노트, CS, Operating-System, review-needed]
---

# 오답노트

## 📝 문제
가상 메모리의 주요 목적은 무엇인가요?

## ✍️ 내 답변
A. 디스크 공간 절약

## ✅ 정답
B. 물리 메모리의 한계 극복

## 💡 피드백
가상 메모리의 핵심은 물리 메모리 크기 제한을 극복하는 것입니다.

## 🔄 복습 기록
| 날짜 | 상태 | 비고 |
|------|------|------|
| 2026-08-07 | review-needed | 초기 기록 |

## 📊 MineSync 연동
- 다음 복습: 2026-08-08
- 간격: 1 일
- 숙련도: 0%
```

---

## ⚙️ 설정

### Cron Job 설정

- **Job ID:** `1699462bb22b`
- **이름:** 학습 에이전트 - 일일 퀴즈 및 리포트
- **스케줄:** `0 9 * * *` (매일 오전 9 시)
- **배달:** Discord 학습 스레드

### Obsidian 연동

- **Vault 경로:** `/mnt/d/YourVault` (Windows: `D:\YourVault`)
- **학습 폴더:** `학습/`
- **태그 체계:** `#오답노트`, `#CS`, `#AI`, `#review-needed`

---

## 🔧 커스터마이징

### 학습 과목 추가

`/opt/data/scripts/learning-agent.py` 수정:

```python
DEFAULT_SUBJECTS = {
    "CS": {
        "topics": ["Operating System", "Database", "Network"],
        "difficulty": "medium",
        "count": 5
    },
    "AI": {
        "topics": ["Machine Learning", "Deep Learning"],
        "difficulty": "medium",
        "count": 3
    },
    # 새 과목 추가
    "Math": {
        "topics": ["Linear Algebra", "Probability"],
        "difficulty": "medium",
        "count": 4
    }
}
```

### 실행 시간 변경

```bash
# 오후 8 시로 변경
hermes cron update <job_id> --schedule "0 20 * * *"
```

---

## 📊 Discord 알림

학습 에이전트는 매일 작업 완료 후 Discord 에 보고합니다:

```
🎓 학습 에이전트 일일 보고서

📅 날짜: 2026-08-07 (KST)

✅ 완료된 작업:
- 퀴즈 생성: 2026-08-07-Operating-System-퀴즈.md
- 일일 리포트: 일일 - 학습 - 리포트-2026-08-07.md

📁 저장 위치: D:\YourVault\학습

다음 학습 시간에 만나요! 💪
```

---

## 🎯 학습 팁

1. **매일 꾸준히** - 오전 9 시 퀴즈를 꼭 풀어보세요
2. **오답노트 복습** - 틀린 문제는 다음 날 반드시 복습
3. **MineSync 연동** - 복습 스케줄을 MineSync 로 관리
4. **Obsidian 정리** - 태그와 링크로 지식 그래프 구축

---

## 🛠️ 문제 해결

### Q: 파일이 생성되지 않아요

A: 다음을 확인하세요:
- `/mnt/d/YourVault` 경로 존재 확인
- 쓰기 권한 확인
- Cron job 실행 상태 확인 (`hermes cron list`)

### Q: Discord 알림이 안 와요

A: 다음을 확인하세요:
- Cron job 의 `deliver` 설정 확인
- Discord 채널 ID 확인
- Hermes 연결 상태 확인

### Q: 퀴즈 난이도를 조절하고 싶어요

A: `learning-agent.py` 의 `DEFAULT_SUBJECTS` 에서 `difficulty` 변경

---

## 📚 관련 문서

- [학습 에이전트 스킬](/opt/data/skills/learning-agent/SKILL.md)
- [Obsidian 연동 가이드](/opt/data/skills/learning-agent/references/obsidian-schema.md)
- [MineSync 연동 방법](https://minesync.nousresearch.com)

---

## 🚀 다음 단계

1. ✅ 오늘 생성된 퀴즈 풀어보기
2. ✅ 오답노트에 첫 기록 추가
3. ✅ MineSync 와 연동 설정
4. ✅ 학습 친구와 공유하기

---

**💭 오늘의 한마디:** 꾸준함이 핵심입니다! 매일 조금씩이라도 학습하세요. 💪
