# 📁 AI Agent 폴더 구조 (D 드라이브 연동 가이드)

## 🎯 목표

학습 에이전트의 모든 데이터를 **D 드라이브**에 저장하여 Windows/Obsidian 과 연동

---

## 📋 1 단계: Windows 에서 폴더 생성 (수동)

Windows 탐색자에서 다음 폴더를 생성하세요:

```
D:\YourAgent\
├── Obsidian_Vault\
│   └── 학습\
│       ├── CS\
│       │   ├── Operating-System\
│       │   │   ├── 퀴즈\
│       │   │   └── 오답노트\
│       │   ├── Database\
│       │   │   ├── 퀴즈\
│       │   │   └── 오답노트\
│       │   └── Network\
│       ├── AI\
│       │   ├── Machine-Learning\
│       │   │   ├── 퀴즈\
│       │   │   └── 오답노트\
│       │   └── Deep-Learning\
│       └── Math\
│           ├── Linear-Algebra\
│           │   ├── 퀴즈\
│           │   └── 오답노트\
│           └── Probability\
├── data\
│   ├── wrong-answers\
│   └── quizzes\
├── scripts\
├── templates\
└── config\
```

### 빠른 생성 (PowerShell)

Windows PowerShell 을 관리자 권한으로 실행 후:

```powershell
$base = "D:\YourAgent"
$folders = @(
    "Obsidian_Vault\학습\CS\Operating-System\퀴즈",
    "Obsidian_Vault\학습\CS\Operating-System\오답노트",
    "Obsidian_Vault\학습\CS\Database\퀴즈",
    "Obsidian_Vault\학습\CS\Database\오답노트",
    "Obsidian_Vault\학습\CS\Network\퀴즈",
    "Obsidian_Vault\학습\CS\Network\오답노트",
    "Obsidian_Vault\학습\AI\Machine-Learning\퀴즈",
    "Obsidian_Vault\학습\AI\Machine-Learning\오답노트",
    "Obsidian_Vault\학습\AI\Deep-Learning\퀴즈",
    "Obsidian_Vault\학습\AI\Deep-Learning\오답노트",
    "Obsidian_Vault\학습\Math\Linear-Algebra\퀴즈",
    "Obsidian_Vault\학습\Math\Linear-Algebra\오답노트",
    "Obsidian_Vault\학습\Math\Probability\퀴즈",
    "Obsidian_Vault\학습\Math\Probability\오답노트",
    "data\wrong-answers",
    "data\quizzes",
    "scripts",
    "templates",
    "config"
)

foreach ($folder in $folders) {
    New-Item -ItemType Directory -Path (Join-Path $base $folder) -Force
}

Write-Host "✅ 폴더 구조 생성 완료!" -ForegroundColor Green
```

---

## 📋 2 단계: WSL 에서 접근 설정

WSL 에서 다음 명령어 실행:

```bash
# D 드라이브 접근 권한 확인
ls -la /mnt/d/YourAgent/

# 접근 가능하면 OK
# 접근 불가 시 Windows 에서 권한 설정 필요
```

---

## 📋 3 단계: Obsidian 설정

1. **Obsidian 실행** (Windows)
2. **Open folder as vault** 클릭
3. 경로 선택: `D:\YourAgent\Obsidian_Vault`
4. ✅ Vault 생성 완료

---

## 📋 4 단계: 에이전트 설정 수정

이미 수정된 파일:

- ✅ `/opt/data/skills/learning-agent/SKILL.md`
  - `obsidian_vault: /mnt/d/YourAgent/Obsidian_Vault`
  
- ✅ `/opt/data/skills/learning-agent/scripts/sync_obsidian.py`
  - 기본 경로: `/mnt/d/YourAgent/Obsidian_Vault`

- ✅ `/opt/data/skills/learning-agent/references/obsidian-schema.md`
  - 폴더 구조 업데이트

---

## 🔍 경로 매핑

| WSL 경로 | Windows 경로 |
|---------|-------------|
| `/mnt/d/YourAgent/Obsidian_Vault` | `D:\YourAgent\Obsidian_Vault` |
| `/mnt/d/YourAgent/data` | `D:\YourAgent\data` |
| `/mnt/d/YourAgent/scripts` | `D:\YourAgent\scripts` |
| `/mnt/d/YourAgent/templates` | `D:\YourAgent\templates` |
| `/mnt/d/YourAgent/config` | `D:\YourAgent\config` |

---

## ✅ 확인 사항

- [ ] Windows 에서 D:\YourAgent\ 폴더 생성 완료
- [ ] WSL 에서 `/mnt/d/YourAgent/` 접근 가능
- [ ] Obsidian Vault 설정 완료
- [ ] Minesync 연동 설정 (선택)

---

## 💡 팁

- **WSL ↔ Windows 파일 공유**: `/mnt/d/` 경로 사용
- **권한 문제**: Windows 에서 폴더 생성 후 WSL 에서 읽기/쓰기 가능
- **Obsidian 동기화**: Windows 에서 Obsidian 실행 → WSL 에서 에이전트 동작
