#!/usr/bin/env python3
"""
채점 스크립트
- 사용자 답변과 정답 비교
- 피드백 생성
- 오답노트 기록 여부 결정
"""

import json
import sys
from datetime import datetime

def grade_answer(user_answer, correct_answer, question_type="multiple_choice"):
    """
    답변 채점
    
    Args:
        user_answer: 사용자 답변
        correct_answer: 정답
        question_type: 문제 타입 (multiple_choice, short_answer, essay)
    
    Returns:
        dict: 채점 결과 (정답여부, 피드백)
    """
    is_correct = user_answer.strip().upper() == correct_answer.strip().upper()
    
    if is_correct:
        feedback = generate_positive_feedback()
    else:
        feedback = generate_corrective_feedback(user_answer, correct_answer)
    
    return {
        "correct": is_correct,
        "user_answer": user_answer,
        "correct_answer": correct_answer,
        "feedback": feedback,
        "timestamp": datetime.now().isoformat(),
        "needs_review": not is_correct
    }

def generate_positive_feedback():
    """정답 시 피드백"""
    return """
✅ 정답입니다! 🎉

잘 이해하고 계시네요.
이 개념을 계속 유지하면서 다른 문제도 풀어보세요!
"""

def generate_corrective_feedback(user_answer, correct_answer):
    """오답 시 피드백"""
    return f"""
❌ 아쉽게도 틀렸습니다.

**내 답변:** {user_answer}
**정답:** {correct_answer}

**피드백:**
어느 부분에서 혼동이 있으신 것 같아요.
기본 개념을 다시 한번 복습하는 것을 추천드립니다.

**핵심 개념:**
- 관련 개념을 다시 확인해보세요
- 예제 문제를 풀어보면 도움이 됩니다
"""

def save_wrong_answer(quiz_id, result, output_dir="data/wrong-answers"):
    """오답노트 저장"""
    if not result["needs_review"]:
        return None
    
    filename = f"{output_dir}/wrong_{quiz_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return filename

if __name__ == "__main__":
    # 테스트
    result = grade_answer("A", "A", "multiple_choice")
    print(json.dumps(result, ensure_ascii=False, indent=2))
