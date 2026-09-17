# 🚀 CS/AI 학습 에이전트 시작하기

## 1️⃣ 프로필 활성화

```bash
# 방법 1: 전용 실행기 사용
cs-ai-learning chat

# 방법 2: 환경변수 설정
export HERMES_HOME=/opt/data/profiles/cs-ai-learning
hermes chat
```

## 2️⃣ API 키 설정 (필수)

완료됨 ✓ — Alibaba Cloud API 키 설정 완료

## 3️⃣ 사용 예시

### 퀴즈 요청
```
"Java 컬렉션 관련 문제 내줘"
"Spring Bean Lifecycle 관련 퀴즈 내줘"
"AI 기초 지식 퀴즈 내줘"
"선형대수 행렬 관련 문제 내줘"
"머신러닝 과적합 개념 물어봐"
```

### 개념 설명
```
"@PostConstruct 가 뭐야?"
"Spring AOP 원리 설명해줘"
"경사하강법이 뭐야?"
"과적합을 방지하는 방법 알려줘"
"벡터와 행렬 차이 설명해줘"
```

### 오답 복습
```
"어제 틀린 문제 복습시켜줘"
"지난주 오답노트 정리해줘"
```

## 4️⃣ Obsidian 연동

모든 학습 기록은 자동으로 Obsidian 에 저장됩니다:

- **위치**: `D:\YourVault\학습\`
- **Java**: `학습/Java/`
- **Spring**: `학습/Spring/`
- **CS**: `학습/CS/`
- **AI**: `학습/AI/`
- **인덱스**: `학습/99_MOC/Java_Index.md`, `Spring_Index.md`, `CS_Index.md`, `AI_Index.md`

## 5️⃣ 학습 범위

### Java
- ✅ 기본 문법 (변수, 타입, 연산자, 제어문)
- ✅ 객체지향 (클래스, 상속, 다형성, 캡슐화, 추상화)
- ✅ 컬렉션 (List, Set, Map, Queue)
- ✅ 스트림 및 람다
- ✅ 예외처리
- ✅ 멀티스레드

### Spring Boot
- ✅ IoC/DI 컨테이너
- ✅ Bean Lifecycle
- ✅ @PostConstruct, @PreDestroy
- ✅ AOP (관점 지향 프로그래밍)
- ✅ Spring MVC
- ✅ Spring JPA
- ✅ Spring Security

### CS (Computer Science)
- ✅ 자료구조 (배열, 리스트, 스택, 큐, 트리, 그래프, 해시)
- ✅ 알고리즘 (정렬, 탐색, DP, 그리디)
- ✅ 운영체제 (프로세스, 스레드, 메모리)
- ✅ 네트워크 (TCP/IP, HTTP, DNS)
- ✅ 데이터베이스 (RDBMS, SQL, 인덱스)

### AI (Artificial Intelligence) - 기초 지식
- ✅ **선형대수**: 벡터, 행렬, 고유값, 특이값 분해 (SVD)
- ✅ **확률통계**: 확률분포, 기댓값, 분산, 가설검정, 베이지안
- ✅ **머신러닝 기초**: 회귀, 분류, 클러스터링, 과적합, 교차검증
- ✅ **딥러닝 기초**: 신경망, 역전파, 활성화 함수, 손실 함수, 최적화
- ✅ **기본 용어**: 에포크, 배치, 학습률, 가중치, 편향, 경사하강법

## 6️⃣ 학습 팁

1. **매일 3 문제**: 꾸준한 퀴즈 풀이로 개념 강화
2. **3 단계 힌트**: 바로 정답을 보지 않고 힌트를 따라 생각하기
3. **오답노트 활용**: 틀린 문제는 자동으로 정리됨
4. **주간 복습**: 매주 MOC 에서 오답노트 리뷰
5. **개념 연결**: 위키링크로 지식 네트워크 구축
6. **AI 기초 병행**: Java/Spring 학습과 함께 AI 기초 지식도 함께 습득

## ⚙️ 설정 커스터마이징

`/opt/data/profiles/cs-ai-learning/config.yaml` 수정:

```yaml
learning-agent:
  default_subject: AI  # Java/Spring/CS/AI 중 선택
  default_difficulty: beginner  # beginner/junior/intermediate/advanced
  quiz_count: 5  # 한 번에 낼 퀴즈 수
```

## 📞 문제 해결

- API 키 오류: `cs-ai-learning setup` 재실행
- Obsidian 연동 안 됨: 경로 확인 (`/mnt/d/YourVault/`)
- 한국어로 안 나옴: config.yaml 에 `language: ko` 확인

---

**마지막 업데이트**: 2026-08-07 (KST)
