# 퀴즈 생성 규칙

## 문제 형식

### 객관식
```
Q[n]. [문제 내용]
A. [보기 1]
B. [보기 2]
C. [보기 3]
D. [보기 4]

정답: [A/B/C/D]
해설: [3-5 문장 설명]
Tags: #[과목] #[주제] #[난이도]
```

### 단답형
```
Q[n]. [문제 내용]

정답: [정답]
해설: [3-5 문장 설명]
Tags: #[과목] #[주제] #[난이도]
```

### 서술형
```
Q[n]. [문제 내용]

모범답안: [상세 답변]
채점기준:
- [기준 1]
- [기준 2]
Tags: #[과목] #[주제] #[난이도]
```

## 난이도 기준

| 난이도 | 설명 | 예시 |
|-------|------|------|
| easy | 기본 개념 확인 | "용어의 정의는?" |
| medium | 이해도 확인 | "상황 적용 문제" |
| hard | 심화 응용 | "복합 개념 문제" |

## 과목 분류

- **CS**: Operating System, Database, Network, Data Structure, Algorithm
- **AI**: Machine Learning, Deep Learning, NLP, Computer Vision, Reinforcement Learning
- **Math**: Linear Algebra, Probability, Statistics, Calculus
- **Programming**: Python, JavaScript, Java, C++

## 생성 규칙

1. 한 번에 5-10 문제 생성
2. 난이도 비율: easy 30%, medium 50%, hard 20%
3. 동일한 개념이 반복되지 않도록 다양성 유지
4. 최신 경향 반영 (2024-2025 년 기준)
5. 실전 적용 가능한 문제 우선
