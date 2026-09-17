#!/usr/bin/env python3
"""
Discord 인터랙티브 퀴즈 시스템
- Discord 에 퀴즈 문제 게시
- 사용자 답변 수신 및 자동 채점
- 실시간 피드백 제공
- 오답노트 자동 생성
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Discord 연동
DISCORD_CHANNEL_ID = "YOUR_DISCORD_LEARNING_THREAD_ID"  # 학습 스레드
OBSIDIAN_VAULT = "/mnt/d/YourVault"
LEARNING_DIR = Path(OBSIDIAN_VAULT) / "학습"

# 퀴즈 세션 관리
QUIZ_SESSION_FILE = "/opt/data/data/quiz-session.json"

class QuizSession:
    """퀴즈 세션 관리"""
    
    def __init__(self):
        self.session_data = {
            "active": False,
            "subject": None,
            "topic": None,
            "questions": [],
            "current_question": 0,
            "answers": {},
            "score": 0,
            "started_at": None,
            "completed_at": None
        }
        self.load_session()
    
    def load_session(self):
        """세션 로드"""
        if Path(QUIZ_SESSION_FILE).exists():
            with open(QUIZ_SESSION_FILE, 'r', encoding='utf-8') as f:
                self.session_data = json.load(f)
    
    def save_session(self):
        """세션 저장"""
        Path(QUIZ_SESSION_FILE).parent.mkdir(parents=True, exist_ok=True)
        with open(QUIZ_SESSION_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.session_data, f, ensure_ascii=False, indent=2)
    
    def start_quiz(self, subject, topic, questions):
        """퀴즈 시작"""
        self.session_data = {
            "active": True,
            "subject": subject,
            "topic": topic,
            "questions": questions,
            "current_question": 0,
            "answers": {},
            "score": 0,
            "started_at": datetime.now().isoformat(),
            "completed_at": None
        }
        self.save_session()
    
    def submit_answer(self, question_id, answer):
        """답변 제출"""
        if not self.session_data["active"]:
            return None
        
        self.session_data["answers"][question_id] = answer
        self.save_session()
        
        # 채점
        current_q = self.session_data["questions"][self.session_data["current_question"]]
        is_correct = answer.strip().upper() == current_q["answer"].strip().upper()
        
        if is_correct:
            self.session_data["score"] += 1
        
        return {
            "correct": is_correct,
            "correct_answer": current_q["answer"],
            "explanation": current_q["explanation"]
        }
    
    def next_question(self):
        """다음 문제로"""
        self.session_data["current_question"] += 1
        if self.session_data["current_question"] >= len(self.session_data["questions"]):
            self.session_data["active"] = False
            self.session_data["completed_at"] = datetime.now().isoformat()
        self.save_session()
    
    def get_current_question(self):
        """현재 문제 반환"""
        if not self.session_data["active"]:
            return None
        idx = self.session_data["current_question"]
        if idx >= len(self.session_data["questions"]):
            return None
        return self.session_data["questions"][idx]
    
    def get_results(self):
        """결과 반환"""
        total = len(self.session_data["questions"])
        score = self.session_data["score"]
        return {
            "total": total,
            "score": score,
            "percentage": round((score / total) * 100, 1) if total > 0 else 0,
            "answers": self.session_data["answers"]
        }


def generate_quiz_questions(subject, topic, difficulty, count=10):
    """LLM 을 사용하여 퀴즈 문제 생성 (실제 구현에서는 API 호출)"""
    
    # 예시 문제 데이터 (실제로는 LLM API 호출)
    sample_questions = {
        "CS": {
            "Operating System": [
                {
                    "id": "Q1",
                    "type": "multiple_choice",
                    "question": "가상 메모리의 주요 목적은 무엇인가요?",
                    "options": ["A. 디스크 공간 절약", "B. 물리 메모리의 한계 극복", "C. CPU 속도 향상", "D. 네트워크 통신 최적화"],
                    "answer": "B",
                    "explanation": "가상 메모리는 물리 RAM 보다 큰 프로그램을 실행할 수 있게 하며, 메모리 단편화를 해결합니다."
                },
                {
                    "id": "Q2",
                    "type": "multiple_choice",
                    "question": "페이지 폴트 (Page Fault) 가 발생하는 상황은?",
                    "options": ["A. 캐시 미스 발생", "B. 필요한 페이지가 메모리에 없음", "C. 디스크 읽기 오류", "D. CPU 오버플로우"],
                    "answer": "B",
                    "explanation": "페이지 폴트는 참조하려는 페이지가 물리 메모리에 없을 때 발생합니다."
                },
                {
                    "id": "Q3",
                    "type": "multiple_choice",
                    "question": "라운드 로빈 (Round Robin) 스케줄링의 특징은?",
                    "options": ["A. 우선순위 기반", "B. 시간 할당량 (Time Quantum) 사용", "C. 가장 짧은 작업 우선", "D. 선점 불가능"],
                    "answer": "B",
                    "explanation": "라운드 로빈은 각 프로세스에 고정된 시간 할당량을 주고 순환하며 실행합니다."
                },
                {
                    "id": "Q4",
                    "type": "multiple_choice",
                    "question": "세마포어 (Semaphore) 의 주요 용도는?",
                    "options": ["A. 메모리 관리", "B. 프로세스 동기화", "C. 디스크 스케줄링", "D. 네트워크 라우팅"],
                    "answer": "B",
                    "explanation": "세마포어는 여러 프로세스의 동기화와 상호 배제를 위해 사용됩니다."
                },
                {
                    "id": "Q5",
                    "type": "multiple_choice",
                    "question": "데드락 (Deadlock) 의 4 가지 필요 조건이 아닌 것은?",
                    "options": ["A. 상호 배제", "B. 점유 대기", "C. 선점 가능", "D. 순환 대기"],
                    "answer": "C",
                    "explanation": "데드락의 4 가지 조건은 상호배제, 점유대기, 비선점, 순환대기입니다."
                },
                {
                    "id": "Q6",
                    "type": "multiple_choice",
                    "question": "스레드 (Thread) 와 프로세스 (Process) 의 차이로 옳은 것은?",
                    "options": ["A. 스레드는 메모리를 공유", "B. 프로세스가 더 가볍다", "C. 스레드가 더 많은 메모리 사용", "D. 차이 없음"],
                    "answer": "A",
                    "explanation": "스레드는 같은 프로세스 내의 메모리를 공유하지만, 프로세스는 독립된 메모리 공간을 가집니다."
                },
                {
                    "id": "Q7",
                    "type": "multiple_choice",
                    "question": "캐시 메모리의 주요 목적은?",
                    "options": ["A. 데이터 영구 저장", "B. CPU 와 메모리 속도 차이 해소", "C. 디스크 공간 절약", "D. 네트워크 속도 향상"],
                    "answer": "B",
                    "explanation": "캐시 메모리는 빠른 속도로 CPU 와 주기억장치 간의 속도 차이를 완화합니다."
                },
                {
                    "id": "Q8",
                    "type": "multiple_choice",
                    "question": "파일 시스템에서 인오드 (inode) 가 포함하는 정보는?",
                    "options": ["A. 파일 내용", "B. 파일 메타데이터", "C. 디렉토리 구조", "D. 사용자 권한"],
                    "answer": "B",
                    "explanation": "인오드는 파일의 메타데이터 (크기, 권한, 타임스탬프 등) 를 저장합니다."
                },
                {
                    "id": "Q9",
                    "type": "multiple_choice",
                    "question": "페이징 (Paging) 에서 페이지 크기는 일반적으로?",
                    "options": ["A. 가변적", "B. 고정적", "C. 랜덤", "D. 사용자의 선택"],
                    "answer": "B",
                    "explanation": "페이징에서는 메모리를 고정된 크기의 페이지로 나눕니다 (일반적으로 4KB)."
                },
                {
                    "id": "Q10",
                    "type": "multiple_choice",
                    "question": "컨텍스트 스위칭 (Context Switching) 이란?",
                    "options": ["A. 프로세스 간 전환", "B. 메모리 복사", "C. 디스크 읽기", "D. 네트워크 패킷 전송"],
                    "answer": "A",
                    "explanation": "컨텍스트 스위칭은 CPU 가 한 프로세스에서 다른 프로세스로 전환하는 과정입니다."
                }
            ]
        },
        "AI": {
            "Machine Learning": [
                {
                    "id": "Q1",
                    "type": "multiple_choice",
                    "question": "지도학습 (Supervised Learning) 의 특징은?",
                    "options": ["A. 레이블 없는 데이터", "B. 레이블 있는 데이터", "C. 보상 기반 학습", "D. 군집화 전용"],
                    "answer": "B",
                    "explanation": "지도학습은 입력과 정답 레이블이 있는 데이터로 모델을 훈련합니다."
                },
                {
                    "id": "Q2",
                    "type": "multiple_choice",
                    "question": "과적합 (Overfitting) 을 방지하는 방법이 아닌 것은?",
                    "options": ["A. 드롭아웃", "B. 데이터 증강", "C. 모델 복잡도 증가", "D. 정규화"],
                    "answer": "C",
                    "explanation": "모델 복잡도를 증가시키면 과적합이 더 심해집니다."
                },
                {
                    "id": "Q3",
                    "type": "multiple_choice",
                    "question": "경사 하강법 (Gradient Descent) 의 목적은?",
                    "options": ["A. 데이터 전처리", "B. 손실 함수 최소화", "C. 특징 추출", "D. 클러스터링"],
                    "answer": "B",
                    "explanation": "경사 하강법은 손실 함수를 최소화하는 가중치를 찾습니다."
                },
                {
                    "id": "Q4",
                    "type": "multiple_choice",
                    "question": "교차 검증 (Cross-Validation) 의 주요 목적은?",
                    "options": ["A. 데이터 증강", "B. 모델 일반화 성능 평가", "C. 특징 선택", "D. 하이퍼파라미터 고정"],
                    "answer": "B",
                    "explanation": "교차 검증은 데이터를 여러 부분으로 나누어 모델의 일반화 성능을 평가합니다."
                },
                {
                    "id": "Q5",
                    "type": "multiple_choice",
                    "question": "정밀도 (Precision) 와 재현율 (Recall) 의 관계로 옳은 것은?",
                    "options": ["A. 항상 비례", "B. 트레이드오프 관계", "C. 항상 동일", "D. 무관"],
                    "answer": "B",
                    "explanation": "정밀도와 재현율은 일반적으로 트레이드오프 관계입니다."
                },
                {
                    "id": "Q6",
                    "type": "multiple_choice",
                    "question": "랜덤 포레스트 (Random Forest) 는 어떤 알고리즘인가?",
                    "options": ["A. 단일 결정 트리", "B. 앙상블 학습", "C. 신경망", "D. 서포트 벡터 머신"],
                    "answer": "B",
                    "explanation": "랜덤 포레스트는 여러 결정 트리의 앙상블입니다."
                },
                {
                    "id": "Q7",
                    "type": "multiple_choice",
                    "question": "K-평균 (K-Means) 클러스터링의 K 는 무엇을 의미하는가?",
                    "options": ["A. 데이터 포인트 수", "B. 클러스터 수", "C. 반복 횟수", "D. 특징 수"],
                    "answer": "B",
                    "explanation": "K 는 생성할 클러스터의 개수를 의미합니다."
                },
                {
                    "id": "Q8",
                    "type": "multiple_choice",
                    "question": "주성분 분석 (PCA) 의 주요 용도는?",
                    "options": ["A. 분류", "B. 차원 축소", "C. 클러스터링", "D. 회귀"],
                    "answer": "B",
                    "explanation": "PCA 는 고차원 데이터를 저차원으로 축소하는 기법입니다."
                },
                {
                    "id": "Q9",
                    "type": "multiple_choice",
                    "question": "L1 정규화와 L2 정규화의 차이는?",
                    "options": ["A. L1 은 희소성, L2 는 가중치 감소", "B. L1 이 더 빠름", "C. L2 만 사용 가능", "D. 차이 없음"],
                    "answer": "A",
                    "explanation": "L1 정규화는 희소성을, L2 정규화는 가중치 감소를 유도합니다."
                },
                {
                    "id": "Q10",
                    "type": "multiple_choice",
                    "question": "ROC 곡선에서 AUC 가 1 이라는 것은?",
                    "options": ["A. 완전한 랜덤", "B. 완벽한 분류기", "C. 잘못된 모델", "D. 데이터 오류"],
                    "answer": "B",
                    "explanation": "AUC 가 1 이면 완벽한 분류기를 의미합니다."
                }
            ]
        }
    }
    
    # 해당 과목/주제의 문제 반환
    if subject in sample_questions and topic in sample_questions[subject]:
        return sample_questions[subject][topic][:count]
    
    # 기본 문제 반환
    return sample_questions.get("CS", {}).get("Operating System", [])[:count]


def format_discord_quiz_message(question, question_num, total):
    """Discord 에 게시할 퀴즈 메시지 포맷"""
    options_text = "\n".join(question["options"])
    
    return f"""
📝 **퀴즈 {question_num}/{total}**

**{question['id']}. {question['question']}**

{options_text}

---
💡 **답변 방법:** `A`, `B`, `C`, `D` 중 하나를 메시지로 보내주세요!
⏱️ **제한시간:** 30 초
"""


def format_grading_result(question, user_answer, result, question_num):
    """채점 결과 메시지"""
    if result["correct"]:
        emoji = "✅"
        score_text = "정답입니다!"
    else:
        emoji = "❌"
        score_text = f"오답입니다. 정답: {result['correct_answer']}"
    
    return f"""
{emoji} **문제 {question_num} 채점 결과**

{score_text}

💡 **해설:**
{result['explanation']}

---
3 초 후 다음 문제로 이동합니다...
"""


def format_final_results(session, subject, topic):
    """최종 결과 메시지"""
    results = session.get_results()
    
    return f"""
🎉 **퀴즈 완료!**

📊 **결과 요약**
- 과목: {subject}
- 주제: {topic}
- 정답 수: {results['score']}/{results['total']}
- 정답률: {results['percentage']}%

📈 **상세 결과:**
"""
    
    # 각 문제별 결과
    for q in session.session_data["questions"]:
        qid = q["id"]
        user_ans = session.session_data["answers"].get(qid, "미답변")
        correct_ans = q["answer"]
        is_correct = user_ans.strip().upper() == correct_ans.strip().upper()
        emoji = "✅" if is_correct else "❌"
        
        results_text = f"{emoji} {qid}: {user_ans} (정답: {correct_ans})\n"
    
    results_text += f"""
---
📁 **오답노트:** 틀린 문제는 자동으로 Obsidian 에 저장됩니다.
🎯 **다음 학습:** 내일 오전 9 시에 새로운 퀴즈가 생성됩니다!

화이팅! 💪
"""
    
    return results_text


# Discord 도구 연동을 위한 래퍼 함수
def send_discord_message(channel_id, message):
    """Discord 에 메시지 전송 (실제 구현에서는 discord 도구 사용)"""
    # 이 함수는 실제 Hermes 의 discord 도구를 통해 구현됨
    print(f"[DISCORD:{channel_id}] {message}")
    return True


def start_quiz_session(subject="CS", topic="Operating System"):
    """퀴즈 세션 시작"""
    print(f"\n🎓 {subject} - {topic} 퀴즈를 시작합니다!")
    
    # 문제 생성
    questions = generate_quiz_questions(subject, topic, "medium", count=10)
    
    # 세션 시작
    session = QuizSession()
    session.start_quiz(subject, topic, questions)
    
    return session, questions


if __name__ == "__main__":
    # 테스트 실행
    print("Discord 퀴즈 시스템 테스트")
    session, questions = start_quiz_session()
    print(f"생성된 문제 수: {len(questions)}")
