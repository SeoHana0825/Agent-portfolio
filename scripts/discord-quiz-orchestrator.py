#!/usr/bin/env python3
"""
Discord 퀴즈 오케스트레이터
- Discord 에서 퀴즈 진행
- 사용자 답변 수신 및 채점
- 오답노트 자동 생성
"""

import json
import time
from datetime import datetime
from pathlib import Path

# 설정
DISCORD_CHANNEL_ID = "YOUR_DISCORD_LEARNING_THREAD_ID"
OBSIDIAN_VAULT = "/mnt/d/YourVault"
LEARNING_DIR = Path(OBSIDIAN_VAULT) / "학습"
QUIZ_SESSION_FILE = "/opt/data/data/quiz-session.json"

# Discord 도구 임포트 (Hermes)
from hermes_tools import terminal

def call_discord_tool(method, **kwargs):
    """Discord 도구 호출"""
    tool_name = "discord"
    arguments = {
        "action": method,
        "channel_id": DISCORD_CHANNEL_ID,
        **kwargs
    }
    
    # Hermes 도구 호출 (terminal 통해 Python 으로)
    code = f"""
import json
from hermes_tools import tool_call

result = tool_call(
    name="{tool_name}",
    arguments={json.dumps(arguments)}
)
print(json.dumps(result))
"""
    result = terminal(f"python3 -c '{code}'", timeout=30)
    return json.loads(result["output"]) if result["exit_code"] == 0 else None


def send_discord_message(message):
    """Discord 에 메시지 전송"""
    code = f"""
from hermes_tools import tool_call
import json

result = tool_call(
    name="discord",
    arguments={{
        "action": "send_message",
        "channel_id": "{DISCORD_CHANNEL_ID}",
        "content": '''{message}'''
    }}
)
print(json.dumps(result))
"""
    result = terminal(f"python3 -c '{code}'", timeout=30)
    return result["exit_code"] == 0


def get_recent_messages(limit=5):
    """최근 메시지 가져오기"""
    code = f"""
from hermes_tools import tool_call
import json

result = tool_call(
    name="discord",
    arguments={{
        "action": "fetch_messages",
        "channel_id": "{DISCORD_CHANNEL_ID}",
        "limit": {limit}
    }}
)
print(json.dumps(result))
"""
    result = terminal(f"python3 -c '{code}'", timeout=30)
    if result["exit_code"] == 0:
        data = json.loads(result["output"])
        return data.get("messages", [])
    return []


def generate_quiz_data(subject, topic):
    """퀴즈 데이터 생성 (10 문제)"""
    
    quiz_db = {
        ("CS", "Operating System"): [
            {"id": "Q1", "question": "가상 메모리의 주요 목적은?", "options": ["A. 디스크 공간 절약", "B. 물리 메모리의 한계 극복", "C. CPU 속도 향상", "D. 네트워크 통신 최적화"], "answer": "B", "explanation": "가상 메모리는 물리 RAM 보다 큰 프로그램을 실행할 수 있게 하며, 메모리 단편화를 해결합니다."},
            {"id": "Q2", "question": "페이지 폴트가 발생하는 상황은?", "options": ["A. 캐시 미스", "B. 필요한 페이지가 메모리에 없음", "C. 디스크 오류", "D. CPU 오버플로우"], "answer": "B", "explanation": "페이지 폴트는 참조하려는 페이지가 물리 메모리에 없을 때 발생합니다."},
            {"id": "Q3", "question": "라운드 로빈 스케줄링의 특징은?", "options": ["A. 우선순위 기반", "B. 시간 할당량 사용", "C. 가장 짧은 작업 우선", "D. 선점 불가능"], "answer": "B", "explanation": "라운드 로빈은 각 프로세스에 고정된 시간 할당량을 주고 순환하며 실행합니다."},
            {"id": "Q4", "question": "세마포어의 주요 용도는?", "options": ["A. 메모리 관리", "B. 프로세스 동기화", "C. 디스크 스케줄링", "D. 네트워크 라우팅"], "answer": "B", "explanation": "세마포어는 여러 프로세스의 동기화와 상호 배제를 위해 사용됩니다."},
            {"id": "Q5", "question": "데드락의 4 가지 필요 조건이 아닌 것은?", "options": ["A. 상호 배제", "B. 점유 대기", "C. 선점 가능", "D. 순환 대기"], "answer": "C", "explanation": "데드락의 4 가지 조건은 상호배제, 점유대기, 비선점, 순환대기입니다."},
            {"id": "Q6", "question": "스레드와 프로세스의 차이로 옳은 것은?", "options": ["A. 스레드는 메모리를 공유", "B. 프로세스가 더 가볍다", "C. 스레드가 더 많은 메모리 사용", "D. 차이 없음"], "answer": "A", "explanation": "스레드는 같은 프로세스 내의 메모리를 공유하지만, 프로세스는 독립된 메모리 공간을 가집니다."},
            {"id": "Q7", "question": "캐시 메모리의 주요 목적은?", "options": ["A. 데이터 영구 저장", "B. CPU 와 메모리 속도 차이 해소", "C. 디스크 공간 절약", "D. 네트워크 속도 향상"], "answer": "B", "explanation": "캐시 메모리는 빠른 속도로 CPU 와 주기억장치 간의 속도 차이를 완화합니다."},
            {"id": "Q8", "question": "인오드 (inode) 가 포함하는 정보는?", "options": ["A. 파일 내용", "B. 파일 메타데이터", "C. 디렉토리 구조", "D. 사용자 권한"], "answer": "B", "explanation": "인오드는 파일의 메타데이터 (크기, 권한, 타임스탬프 등) 를 저장합니다."},
            {"id": "Q9", "question": "페이징에서 페이지 크기는 일반적으로?", "options": ["A. 가변적", "B. 고정적", "C. 랜덤", "D. 사용자 선택"], "answer": "B", "explanation": "페이징에서는 메모리를 고정된 크기의 페이지로 나눕니다 (일반적으로 4KB)."},
            {"id": "Q10", "question": "컨텍스트 스위칭이란?", "options": ["A. 프로세스 간 전환", "B. 메모리 복사", "C. 디스크 읽기", "D. 네트워크 패킷 전송"], "answer": "A", "explanation": "컨텍스트 스위칭은 CPU 가 한 프로세스에서 다른 프로세스로 전환하는 과정입니다."}
        ],
        ("AI", "Machine Learning"): [
            {"id": "Q1", "question": "지도학습의 특징은?", "options": ["A. 레이블 없는 데이터", "B. 레이블 있는 데이터", "C. 보상 기반 학습", "D. 군집화 전용"], "answer": "B", "explanation": "지도학습은 입력과 정답 레이블이 있는 데이터로 모델을 훈련합니다."},
            {"id": "Q2", "question": "과적합을 방지하는 방법이 아닌 것은?", "options": ["A. 드롭아웃", "B. 데이터 증강", "C. 모델 복잡도 증가", "D. 정규화"], "answer": "C", "explanation": "모델 복잡도를 증가시키면 과적합이 더 심해집니다."},
            {"id": "Q3", "question": "경사 하강법의 목적은?", "options": ["A. 데이터 전처리", "B. 손실 함수 최소화", "C. 특징 추출", "D. 클러스터링"], "answer": "B", "explanation": "경사 하강법은 손실 함수를 최소화하는 가중치를 찾습니다."},
            {"id": "Q4", "question": "교차 검증의 주요 목적은?", "options": ["A. 데이터 증강", "B. 모델 일반화 성능 평가", "C. 특징 선택", "D. 하이퍼파라미터 고정"], "answer": "B", "explanation": "교차 검증은 데이터를 여러 부분으로 나누어 모델의 일반화 성능을 평가합니다."},
            {"id": "Q5", "question": "정밀도와 재현율의 관계로 옳은 것은?", "options": ["A. 항상 비례", "B. 트레이드오프 관계", "C. 항상 동일", "D. 무관"], "answer": "B", "explanation": "정밀도와 재현율은 일반적으로 트레이드오프 관계입니다."},
            {"id": "Q6", "question": "랜덤 포레스트는 어떤 알고리즘인가?", "options": ["A. 단일 결정 트리", "B. 앙상블 학습", "C. 신경망", "D. 서포트 벡터 머신"], "answer": "B", "explanation": "랜덤 포레스트는 여러 결정 트리의 앙상블입니다."},
            {"id": "Q7", "question": "K-평균 클러스터링의 K 는 무엇을 의미하는가?", "options": ["A. 데이터 포인트 수", "B. 클러스터 수", "C. 반복 횟수", "D. 특징 수"], "answer": "B", "explanation": "K 는 생성할 클러스터의 개수를 의미합니다."},
            {"id": "Q8", "question": "주성분 분석 (PCA) 의 주요 용도는?", "options": ["A. 분류", "B. 차원 축소", "C. 클러스터링", "D. 회귀"], "answer": "B", "explanation": "PCA 는 고차원 데이터를 저차원으로 축소하는 기법입니다."},
            {"id": "Q9", "question": "L1 정규화와 L2 정규화의 차이는?", "options": ["A. L1 은 희소성, L2 는 가중치 감소", "B. L1 이 더 빠름", "C. L2 만 사용 가능", "D. 차이 없음"], "answer": "A", "explanation": "L1 정규화는 희소성을, L2 정규화는 가중치 감소를 유도합니다."},
            {"id": "Q10", "question": "ROC 곡선에서 AUC 가 1 이라는 것은?", "options": ["A. 완전한 랜덤", "B. 완벽한 분류기", "C. 잘못된 모델", "D. 데이터 오류"], "answer": "B", "explanation": "AUC 가 1 이면 완벽한 분류기를 의미합니다."}
        ]
    }
    
    key = (subject, topic)
    if key in quiz_db:
        return quiz_db[key]
    
    # 기본값
    return quiz_db[("CS", "Operating System")]


def create_wrong_note(subject, topic, question, user_answer, correct_answer, explanation):
    """오답노트 생성"""
    today = datetime.now().strftime("%Y-%m-%d")
    topic_dir = topic.replace(" ", "-")
    wrong_dir = LEARNING_DIR / subject / topic_dir / "오답노트"
    wrong_dir.mkdir(parents=True, exist_ok=True)
    
    wrong_file = wrong_dir / f"{today}-{topic.replace(' ', '-')}-오답.md"
    
    content = f"""---
created: {today}
subject: {subject}
topic: {topic}
status: review-needed
review_count: 0
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
{explanation}

## 📖 관련 개념
- [[{topic} 기본 개념]]
- [[{subject} 핵심 정리]]

## 🔄 복습 기록
| 날짜 | 상태 | 비고 |
|------|------|------|
| {today} | review-needed | 초기 기록 |

## 📊 MineSync 연동
- 다음 복습: {(datetime.now()).strftime('%Y-%m-%d')}
- 간격: 1 일
- 숙련도: 0%

---
> 💭 **오늘의 한마디:** 틀린 것은 배우는 과정입니다! 💪
"""
    
    with open(wrong_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return wrong_file


def run_interactive_quiz(subject="CS", topic="Operating System"):
    """인터랙티브 퀴즈 실행"""
    
    print(f"\n🎓 {subject} - {topic} 퀴즈를 시작합니다!")
    
    # 1. 퀴즈 데이터 생성
    questions = generate_quiz_data(subject, topic)
    
    # 2. 시작 메시지
    start_message = f"""
🎓 **{subject} - {topic} 퀴즈**

📝 **문제 수:** 10 개
⏱️ **제한시간:** 문제당 30 초
💡 **답변 방법:** `A`, `B`, `C`, `D` 중 하나를 메시지로 보내주세요!

퀴즈를 시작하려면 `시작` 또는 `start` 라고 보내주세요!
"""
    send_discord_message(start_message)
    
    # 3. '시작' 메시지 대기
    while True:
        messages = get_recent_messages(limit=5)
        if messages:
            latest = messages[0]
            content = latest.get("content", "").strip().lower()
            if content in ["시작", "start"]:
                break
        time.sleep(1)
    
    # 4. 퀴즈 진행
    score = 0
    wrong_answers = []
    
    for i, q in enumerate(questions, 1):
        # 문제 게시
        question_msg = f"""
📝 **퀴즈 {i}/10**

**{q['id']}. {q['question']}**

{chr(10).join(q['options'])}

---
⏱️ 제한시간: 30 초
"""
        send_discord_message(question_msg)
        
        # 사용자 답변 대기 (간단한 구현: 30 초 대기)
        time.sleep(2)  # 실제로는 메시지 폴링
        
        # 최근 메시지 확인
        messages = get_recent_messages(limit=3)
        user_answer = "A"  # 기본값 (실제로는 사용자 입력)
        
        if messages:
            for msg in messages:
                content = msg.get("content", "").strip().upper()
                if content in ["A", "B", "C", "D"]:
                    user_answer = content
                    break
        
        # 채점
        is_correct = user_answer == q["answer"]
        if is_correct:
            score += 1
            feedback = "✅ **정답입니다!**"
        else:
            feedback = f"❌ **오답입니다. 정답: {q['answer']}**"
            wrong_answers.append((q, user_answer))
        
        # 피드백
        result_msg = f"""
{feedback}

💡 **해설:** {q['explanation']}

---
다음 문제까지 3 초...
"""
        send_discord_message(result_msg)
        time.sleep(3)
    
    # 5. 최종 결과
    percentage = (score / 10) * 100
    
    final_msg = f"""
🎉 **퀴즈 완료!**

📊 **결과**
- 정답: {score}/10
- 정답률: {percentage}%

"""
    
    if wrong_answers:
        final_msg += f"📝 **오답노트:** {len(wrong_answers)}개 기록됨\n"
        final_msg += f"📁 위치: `D:\\YourVault\\학습\\{subject}\\{topic.replace(' ', '-')}\\오답노트\\`\n"
    
    final_msg += "\n💪 화이팅!"
    
    send_discord_message(final_msg)
    
    # 6. 오답노트 생성
    for q, user_ans in wrong_answers:
        wrong_file = create_wrong_note(
            subject, topic,
            q["question"], user_ans,
            q["answer"], q["explanation"]
        )
        print(f"✅ 오답노트 생성: {wrong_file}")
    
    return {"score": score, "total": 10, "percentage": percentage}


if __name__ == "__main__":
    # 테스트 실행
    print("Discord 퀴즈 오케스트레이터")
    result = run_interactive_quiz("CS", "Operating System")
    print(f"\n결과: {result}")
