#!/usr/bin/env python3
"""
학습 에이전트 - 독립 실행형 AI 튜터
- 매일 자동으로 퀴즈 생성
- 오답노트 Obsidian 에 정리
- MineSync 연동으로 복습 스케줄 관리
- Discord 로 학습 진행 상황 보고
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Windows 경로 (Obsidian 접근용) - 대체 경로 사용
OBSIDIAN_VAULT = "/opt/data/YourVault"
LEARNING_DIR = Path(OBSIDIAN_VAULT) / "학습"

# 학습 설정
DEFAULT_SUBJECTS = {
    "CS": {
        "topics": ["Operating System", "Database", "Network", "Data Structures", "Algorithms"],
        "difficulty": "medium",
        "count": 10  # 10 문제로 증가
    },
    "AI": {
        "topics": ["Machine Learning", "Deep Learning", "Neural Networks", "NLP", "Computer Vision"],
        "difficulty": "medium",
        "count": 10  # 10 문제로 증가
    }
}

def ensure_dirs():
    """Obsidian 폴더 구조 생성"""
    for subject in DEFAULT_SUBJECTS.keys():
        for topic in DEFAULT_SUBJECTS[subject]["topics"]:
            quiz_dir = LEARNING_DIR / subject / topic.replace(" ", "-") / "퀴즈"
            wrong_dir = LEARNING_DIR / subject / topic.replace(" ", "-") / "오답노트"
            quiz_dir.mkdir(parents=True, exist_ok=True)
            wrong_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ 폴더 구조 확인 완료: {LEARNING_DIR}")

def generate_quiz_prompt(subject, topic, difficulty, count):
    """LLM 퀴즈 생성 프롬프트"""
    return f"""
당신은 {subject} 전문가이자 교육자입니다.
{topic}에 대한 {difficulty} 난이도의 퀴즈 {count}개를 생성하세요.

각 문제는 다음 JSON 형식으로 출력하세요:

{{
  "quizzes": [
    {{
      "id": "Q1",
      "type": "multiple_choice",
      "question": "문제 내용",
      "options": ["A. 보기 1", "B. 보기 2", "C. 보기 3", "D. 보기 4"],
      "answer": "A",
      "explanation": "해설 (3-5 문장)",
      "tags": ["{subject}", "{topic}", "{difficulty}"]
    }}
  ]
}}

난이도 기준:
- easy: 기본 개념 확인
- medium: 이해도 및 적용  
- hard: 심화 응용 및 복합 개념

반드시 JSON 형식만 출력하세요.
"""

def create_quiz_file(subject, topic, quiz_data):
    """퀴즈 파일 저장"""
    today = datetime.now().strftime("%Y-%m-%d")
    topic_dir = topic.replace(" ", "-")
    quiz_file = LEARNING_DIR / subject / topic_dir / "퀴즈" / f"{today}-{topic}-퀴즈.md"
    
    content = f"""---
subject: {subject}
topic: {topic}
difficulty: medium
count: {len(quiz_data.get('quizzes', []))}
created: {today}
tags: [퀴즈, {subject}, {topic}]
---

# {subject} - {topic} 퀴즈

**난이도:** medium  
**문제 수:** {len(quiz_data.get('quizzes', []))}  
**생성일:** {today}

---

"""
    
    for quiz in quiz_data.get('quizzes', []):
        content += f"""## {quiz['id']}. {quiz['question']}

{chr(10).join(quiz.get('options', []))}

---

"""
    
    content += """\n## 정답 및 해설

"""
    for quiz in quiz_data.get('quizzes', []):
        content += f"""### {quiz['id']} 정답: {quiz['answer']}
{quiz.get('explanation', '')}

"""
    
    content += f"""---

## 학습 기록

- 시작 시간: 
- 완료 시간: 
- 정답률: 
- 복습 필요 문제: 
"""
    
    with open(quiz_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 퀴즈 생성 완료: {quiz_file}")
    return quiz_file

def create_wrong_note(subject, topic, question, user_answer, correct_answer, feedback):
    """오답노트 생성"""
    today = datetime.now().strftime("%Y-%m-%d")
    topic_dir = topic.replace(" ", "-")
    wrong_file = LEARNING_DIR / subject / topic_dir / "오답노트" / f"{today}-{topic}-오답.md"
    
    content = f"""---
created: {today}
subject: {subject}
topic: {topic}
difficulty: medium
status: review-needed
review_count: 0
last_reviewed: 
tags: [오답노트, {subject}, {topic}, review-needed]
---

# 오답노트

## 📝 문제

{question}

## ✍️ 내 답변

{user_answer}

## ✅ 정답

{correct_answer}

## 💡 피드백

{feedback}

## 📖 관련 개념

- [[{topic} 기본 개념]]
- [[{subject} 핵심 정리]]

## 🔄 복습 기록

| 날짜 | 상태 | 비고 |
|------|------|------|
| {today} | review-needed | 초기 기록 |
| | | |
| | | |

## 📊 MineSync 연동

- 다음 복습: {(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")}
- 간격: 1 일
- 숙련도: 0%

---

> 💭 **오늘의 한마디:** 틀린 것은 배우는 과정입니다! 꾸준히 복습하면 마스터할 수 있어요. 💪
"""
    
    with open(wrong_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 오답노트 생성 완료: {wrong_file}")
    return wrong_file

def generate_daily_report():
    """일일 학습 리포트 생성"""
    today = datetime.now().strftime("%Y-%m-%d")
    report_file = LEARNING_DIR / f"일일-학습-리포트-{today}.md"
    
    # 오늘 생성된 퀴즈 및 오답노트 카운트
    quiz_count = 0
    wrong_count = 0
    
    for subject in DEFAULT_SUBJECTS.keys():
        subject_dir = LEARNING_DIR / subject
        if subject_dir.exists():
            for item in subject_dir.rglob(f"*{today}*.md"):
                if "퀴즈" in str(item):
                    quiz_count += 1
                if "오답" in str(item):
                    wrong_count += 1
    
    content = f"""---
created: {today}
tags: [학습리포트, 일일보고]
---

# 📊 일일 학습 리포트

**날짜:** {today}  
**시간:** {datetime.now().strftime("%H:%M")} (KST)

---

## 📈 오늘의 학습 통계

- ✅ 생성된 퀴즈: {quiz_count}개
- 📝 작성된 오답노트: {wrong_count}개
- 🎯 학습 과목: {', '.join(DEFAULT_SUBJECTS.keys())}

---

## 📚 오늘 학습한 주제

"""
    
    for subject, config in DEFAULT_SUBJECTS.items():
        content += f"""### {subject}
- 주제: {', '.join(config['topics'][:3])}
- 난이도: {config['difficulty']}
- 문제 수: {config['count']}

"""
    
    content += f"""---

## 🎯 내일 학습 계획

1. 오늘의 오답노트 복습
2. 새로운 주제 학습
3. 주간 진도 점검

---

> 💡 **학습 팁:** 꾸준함이 핵심입니다! 매일 조금씩이라도 학습하세요.
"""
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 일일 리포트 생성 완료: {report_file}")
    return report_file

def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("🎓 학습 에이전트 시작")
    print(f"📅 실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (KST)")
    print("=" * 60)
    
    try:
        # 1. 폴더 구조 확인
        ensure_dirs()
        
        # 2. 일일 퀴즈 생성 (예시: CS Operating System)
        print("\n📝 퀴즈 생성 중...")
        subject = "CS"
        topic = "Operating System"
        difficulty = "medium"
        count = 5
        
        # 실제 구현에서는 여기서 LLM API 호출
        # 예시 데이터 (실제로는 API 호출 결과)
        sample_quiz = {
            "quizzes": [
                {
                    "id": "Q1",
                    "type": "multiple_choice",
                    "question": "가상 메모리의 주요 목적은 무엇인가요?",
                    "options": [
                        "A. 디스크 공간 절약",
                        "B. 물리 메모리의 한계 극복",
                        "C. CPU 속도 향상",
                        "D. 네트워크 통신 최적화"
                    ],
                    "answer": "B",
                    "explanation": "가상 메모리는 물리 RAM 보다 큰 프로그램을 실행할 수 있게 하며, 메모리 단편화를 해결합니다.",
                    "tags": ["CS", "Operating System", "medium"]
                }
            ]
        }
        
        quiz_file = create_quiz_file(subject, topic, sample_quiz)
        
        # 3. 일일 리포트 생성
        print("\n📊 일일 리포트 생성 중...")
        report_file = generate_daily_report()
        
        print("\n" + "=" * 60)
        print("✅ 학습 에이전트 작업 완료")
        print(f"📁 저장 위치: {LEARNING_DIR}")
        print("=" * 60)
        
        # Discord 로 보고할 메시지
        report_message = f"""
🎓 **학습 에이전트 일일 보고서**

📅 날짜: {datetime.now().strftime('%Y-%m-%d')} (KST)

✅ 완료된 작업:
- 퀴즈 생성: {quiz_file.name}
- 일일 리포트: {report_file.name}

📁 저장 위치: `D:\\YourVault\\학습`

다음 학습 시간에 만나요! 💪
"""
        print(report_message)
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
