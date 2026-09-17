#!/usr/bin/env python3
"""
퀴즈 생성 스크립트
- 과목, 주제, 난이도를 입력받아 AI 가 문제 생성
- 생성된 문제는 JSON 형식으로 저장
"""

import json
import sys
from datetime import datetime

def generate_quiz_prompt(subject, topic, difficulty, count=5):
    """LLM 에 보낼 프롬프트 생성"""
    return f"""
당신은 {subject} 전문가이자 교육자입니다.
{topic}에 대한 {difficulty} 난이도의 퀴즈 {count}개를 생성하세요.

각 문제는 다음 형식을 JSON 으로 출력하세요:

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

def save_quiz(quiz_data, output_path):
    """퀴즈 데이터 저장"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(quiz_data, f, ensure_ascii=False, indent=2)
    print(f"✅ 퀴즈 저장 완료: {output_path}")

if __name__ == "__main__":
    # 예시: python generate_quiz.py CS "Operating System" medium 5
    if len(sys.argv) < 4:
        print("사용법: python generate_quiz.py <subject> <topic> <difficulty> [count]")
        sys.exit(1)
    
    subject = sys.argv[1]
    topic = sys.argv[2]
    difficulty = sys.argv[3]
    count = int(sys.argv[4]) if len(sys.argv) > 4 else 5
    
    prompt = generate_quiz_prompt(subject, topic, difficulty, count)
    print("생성 프롬프트:")
    print(prompt)
    # 실제 구현에서는 여기서 LLM API 호출
