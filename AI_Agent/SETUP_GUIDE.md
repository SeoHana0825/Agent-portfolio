# 🚀 학습 에이전트 설정 가이드

## 1️⃣ Windows 에서 폴더 생성

### 방법 A: PowerShell 스크립트 (권장)

1. PowerShell 실행
2. 다음 명령어 실행:
   ```powershell
   cd D:\YourAgent\scripts
   .\setup-folders.ps1
   ```

### 방법 B: 수동 생성

Windows 탐색자에서 `D:\YourAgent\` 폴더 생성 후 하위 폴더들 생성

---

## 2️⃣ Obsidian 설정

1. **Obsidian 실행** (Windows)
2. **Open folder as vault** 클릭
3. `D:\YourAgent\Obsidian_Vault` 선택
4. ✅ Vault 생성 완료

---

## 3️⃣ WSL 에서 접근 확인

```bash
# WSL 터미널에서
ls -la /mnt/d/YourAgent/
```

접근 가능하면 설정 완료!

---

## 4️⃣ 에이전트 실행

```bash
# 퀴즈 생성 예시
python /mnt/d/YourAgent/scripts/generate_quiz.py CS "Operating System" medium 5

# 또는 Hermes 스킬 사용
/quiz generate --subject CS --topic "Operating System" --difficulty medium
```

---

## 📁 폴더 구조

```
D:/YourAgent/
├── Obsidian_Vault/      # 옵시디언 버클트
│   └── 학습/
│       ├── CS/
│       ├── AI/
│       └── Math/
├── data/                # 학습 데이터
├── scripts/             # 실행 스크립트
├── templates/           # 템플릿
└── config/              # 설정
```

---

## 🔗 경로 매핑

| WSL | Windows |
|-----|---------|
| `/mnt/d/YourAgent/` | `D:\YourAgent\` |

---

## ❓ 문제 해결

### Q: `/mnt/d/` 접근 불가
**A:** Windows 에서 먼저 폴더를 생성하세요.

### Q: Obsidian 이 파일을 못 찾음
**A:** WSL 경로 (`/mnt/d/`) 대신 Windows 경로 (`D:\`) 사용

### Q: 권한 오류
**A:** Windows 에서 폴더 생성 후 WSL 에서 접근 가능

---

## 📞 문의

문제가 있으면 Discord 채널로 연락주세요!
