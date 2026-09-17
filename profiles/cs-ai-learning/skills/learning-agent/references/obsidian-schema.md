# Obsidian 연동 스키마 (볼트 구조)

## 폴더 구조

```
D:\YourVault\
└── 학습\
    ├── Java\
        ├── 퀴즈\
        │   └── {{주제}}\
        ├── 오답노트\
        │   └── {{YYYY-MM-DD}}-{{주제}}-{{연번}}.md
        └── 개념\
            └── {{개념명}}.md
    ├── Spring\
        ├── 퀴즈\
        │   └── {{주제}}\
        ├── 오답노트\
        │   └── {{YYYY-MM-DD}}-{{주제}}-{{연번}}.md
        └── 개념\
            └── {{개념명}}.md
    ├── CS\
        ├── 퀴즈\
        │   └── {{주제}}\
        ├── 오답노트\
        │   └── {{YYYY-MM-DD}}-{{주제}}-{{연번}}.md
        └── 개념\
            └── {{개념명}}.md
    └── 99_MOC\
        ├── Java_Index.md
        ├── Spring_Index.md
        ├── CS_Index.md
        └── 학습_홈.md
```

## 파일 네이밍 규칙

### 오답노트
```
{{YYYY-MM-DD}}-{{주제}}-{{연번}}.md
예: 2026-08-07-Bean-Lifecycle-01.md
```

### 개념 노트
```
{{개념명}}.md
예: Spring-Bean-Lifecycle.md
```

### 퀴즈
```
{{YYYY-MM-DD}}-{{과목}}-{{주제}}.md
예: 2026-08-07-Java-Spring-Quiz.md
```

## 프론트매터 스키마

### 오답노트 (wrong-answer)
```yaml
---
date: {{생성일 (YYYY-MM-DD)}}
subject: {{과목 (Java/Spring/CS)}}
type: wrong-answer
status: 미복습 | 복습완료
related: [[연관 개념 노트]]
tags: [오답노트, {{과목}}, {{주제}}]
---
```

### 개념 노트 (concept)
```yaml
---
date: {{생성일 (YYYY-MM-DD)}}
subject: {{과목 (Java/Spring/CS)}}
type: concept
status: active
related: [[관련 개념 1]], [[관련 개념 2]]
tags: [개념노트, {{과목}}, {{주제}}]
---
```

### 퀴즈 (quiz)
```yaml
---
date: {{생성일 (YYYY-MM-DD)}}
subject: {{과목 (Java/Spring/CS)}}
type: quiz
difficulty: easy | medium | hard
count: {{문제수}}
tags: [퀴즈, {{과목}}, {{주제}}]
---
```

## 위키링크 규칙

### 개념 연결
- 오답노트 → 관련 개념: `[[Spring-Bean-Lifecycle]]`
- 개념 → 관련 개념: `[[의존성-주입]], [[AOP]]`
- 퀴즈 → 해설 개념: `[[트랜잭션-전파]]`

### MOC 연결
- 주간 오답: `[[2026-W32-Java-오답]]`
- 월간 정리: `[[2026-08-Java-정리]]`
- 과목 인덱스: `[[Java_Index]]`

## 태그 체계

| 태그 | 설명 |
|------|------|
| #오답노트 | 모든 오답노트 |
| #개념노트 | 개념 정리 노트 |
| #퀴즈 | 퀴즈 문제 |
| #Java #Spring #CS | 과목별 분류 |
| #미복습 #복습완료 | 복습 상태 |
| #W32 #2026-08 | 주/월 단위 정리 |

## 99_MOC 구조

### Java_Index.md
```markdown
# Java 학습 인덱스

## 📊 오답노트 (주별)
- [[2026-W32-Java-오답]]
- [[2026-W31-Java-오답]]

## 📚 개념 정리
- [[Java-Collection]]
- [[Java-Stream]]
- [[Java-Optional]]

## 📈 진도 현황
- ✅ 컬렉션 (완료)
- 🟡 스트림 (진행중)
- ⬜ Optional (예정)
```

### Spring_Index.md
```markdown
# Spring 학습 인덱스

## 📊 오답노트 (주별)
- [[2026-W32-Spring-오답]]
- [[2026-W31-Spring-오답]]

## 📚 개념 정리
- [[Spring-Bean-Lifecycle]]
- [[Spring-DI]]
- [[Spring-AOP]]
- [[Spring-Transaction]]

## 📈 진도 현황
- ✅ Bean Lifecycle (완료)
- 🟡 AOP (진행중)
- ⬜ Transaction (예정)
```

## 자동 업데이트 규칙

### 오답노트 생성 시
1. 해당 과목 폴더에 파일 생성
2. 관련 개념 노트 확인 → 없으면 생성
3. 위키링크로 상호 연결
4. 해당 주의 MOC 에 자동 추가

### 주간 MOC 반영 (매주 일요일)
```python
# update_moc.py 의사코드
def update_weekly_moc(subject, week):
    # 해당 주의 오답노트 검색
    wrong_notes = find_wrong_notes(subject, week)
    
    # MOC 파일 업데이트
    moc_file = f"99_MOC/{subject}_Index.md"
    add_links(moc_file, wrong_notes)
    
    # 진도 현황 업데이트
    update_progress(moc_file, wrong_notes)
```

## Obsidian 설정 권장사항

### 플러그인
- Dataview: 동적 쿼리 및 진도 표시
- Templater: 템플릿 자동 적용
- QuickAdd: 빠른 노트 생성
- Calendar: 날짜별 노트 탐색

### 설정
```yaml
링크 자동완성: 켜기
새 탭에서 열기: 끄기
대소문자 구분: 끄기
```

## 동기화 규칙

1. **Windows 경로 사용**: D:\YourVault (WSL 에서 /mnt/d/YourVault)
2. **중복 방지**: 날짜 + 주제 + 연번으로 유니크 키 생성
3. **위키링크 검증**: 깨진 링크定期检查
4. **백업**: Git 또는 Obsidian Sync 로 자동 백업

## 검색 쿼리 예시

```dataview
TABLE date, subject, status
FROM "학습"
WHERE type = "wrong-answer"
SORT date DESC
```

```dataview
TABLE file.link AS "개념"
FROM "학습"
WHERE type = "concept"
AND contains(related, [[Spring-Bean-Lifecycle]])
```
