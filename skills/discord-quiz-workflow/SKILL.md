---
name: discord-quiz-workflow
description: "Discord 인터랙티브 퀴즈 - 10 문제 생성, 실시간 채점, 오답노트 자동화"
version: 1.0.0
author: SeoHana0825
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [discord, quiz, learning, interactive, grading]
---

# Discord 퀴즈 워크플로우

Discord 에서 직접 퀴즈를 풀고 실시간 채점을 받는 인터랙티브 학습 시스템입니다.

## 주요 기능

1. **10 문제 퀴즈 생성** - 과목별 10 문제씩 생성
2. **Discord 인터랙션** - Discord 에서 문제 표시 및 답변 수신
3. **실시간 채점** - 답변 즉시 채점 및 피드백
4. **오답노트 자동 생성** - 틀린 문제 Obsidian 에 자동 기록
5. **학습 통계** - 퀴즈 완료 후 상세 리포트

## 명령어

```bash
# 퀴즈 시작
/quiz start --subject CS --topic "Operating System"

# 답변 제출
A  # 또는 B, C, D

# 퀴즈 상태 확인
/quiz status

# 오답노트 확인
/wrong-note list
```

## Discord 워크플로우

### 1. 퀴즈 시작

```
에이전트: 📝 퀴즈 1/10

         Q1. 가상 메모리의 주요 목적은 무엇인가요?
         
         A. 디스크 공간 절약
         B. 물리 메모리의 한계 극복
         C. CPU 속도 향상
         D. 네트워크 통신 최적화

         ---
         💡 답변 방법: A, B, C, D 중 하나를 메시지로 보내주세요!
```

### 2. 답변 및 채점

```
사용자: B

에이전트: ✅ 정답입니다!

         💡 해설: 가상 메모리는 물리 RAM 보다 큰 프로그램을 실행할 수 있게 
                  하며, 메모리 단편화를 해결합니다.
         
         3 초 후 다음 문제로 이동합니다...
```

### 3. 오답 처리

```
사용자: A

에이전트: ❌ 오답입니다. 정답: B

         💡 해설: 가상 메모리의 핵심은 물리 메모리 크기 제한을 극복하는 것입니다.
         
         📝 오답노트에 기록되었습니다.
```

### 4. 완료 리포트

```
에이전트: 🎉 퀴즈 완료!

         📊 결과 요약
         - 과목: CS
         - 주제: Operating System
         - 정답 수: 8/10
         - 정답률: 80%
         
         📁 오답노트: D:\YourVault\학습\CS\Operating-System\오답노트\
```

## 파일 구조

```
/opt/data/skills/discord-quiz-workflow/
├── SKILL.md
├── scripts/
│   ├── discord-quiz-bot.py
│   └── quiz-grader.py
├── templates/
│   ├── quiz-message.md
│   └── grading-result.md
└── data/
    └── quiz-sessions/
```

## 구현 단계

### 1. 퀴즈 생성 (10 문제)

```python
questions = generate_quiz_questions(
    subject="CS",
    topic="Operating System",
    difficulty="medium",
    count=10  # 10 문제
)
```

### 2. Discord 게시

```python
# 각 문제를 Discord 에 순차적 게시
for i, q in enumerate(questions, 1):
    message = format_quiz_message(q, i, len(questions))
    discord.send(channel_id, message)
    
    # 사용자 답변 대기 (30 초 타임아웃)
    answer = wait_for_answer(timeout=30)
    
    # 채점
    result = grade_answer(q, answer)
    
    # 피드백
    discord.send(format_grading_result(result))
    
    # 오답이면 기록
    if not result["correct"]:
        create_wrong_note(q, answer, result)
```

### 3. 오답노트 생성

```python
def create_wrong_note(question, user_answer, result):
    template = f"""
    ---
    created: {datetime.now().strftime('%Y-%m-%d')}
    subject: CS
    topic: Operating System
    status: review-needed
    tags: [오답노트, CS, review-needed]
    ---
    
    # 오답노트
    
    ## 문제
    {question['question']}
    
    ## 내 답변
    {user_answer}
    
    ## 정답
    {result['correct_answer']}
    
    ## 피드백
    {result['explanation']}
    """
    
    save_to_obsidian(template)
```

## 설정

### Discord 채널

- **학습 스레드 ID:** `YOUR_DISCORD_LEARNING_THREAD_ID`
- **알림 설정:** 모든 퀴즈 활동
- **타임아웃:** 30 초/문제

### Obsidian 연동

- **Vault:** `/mnt/d/YourVault`
- **폴더:** `학습/{과목}/{주제}/오답노트/`
- **태그:** `#오답노트`, `#review-needed`

## 사용 예시

### CS 운영체제 퀴즈

```
/quiz start CS "Operating System"
```

### AI 머신러닝 퀴즈

```
/quiz start AI "Machine Learning"
```

### 커스텀 설정

```
/quiz start --subject CS --topic "Network" --count 10 --difficulty hard
```

## 채점 규칙

- **정답:** +1 점
- **오답:** 0 점 (오답노트 자동 생성)
- **미답변:** 0 점 (타임아웃)
- **정답률:** (정답 수 / 10) * 100

## 피드백 가이드라인

1. **즉시 피드백** - 답변 후 3 초 이내
2. **상세 해설** - 2-3 문장 설명
3. **격려 메시지** - 오답일 경우에도 긍정적 피드백
4. **오답노트 링크** - 자동 저장 위치 안내

## 관련 문서

- [학습 에이전트](learning-agent)
- [Obsidian 연동](references/obsidian-schema.md)
- [Discord 도구](discord)
