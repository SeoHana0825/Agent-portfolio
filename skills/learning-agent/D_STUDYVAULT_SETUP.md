# 📁 학습 에이전트 폴더 구조 (D:\YourVault 연동)

## ✅ 설정 완료 경로

| 구분 | WSL 경로 | Windows 경로 |
|------|---------|-------------|
| Obsidian Vault | `/mnt/d/YourVault` | `D:\YourVault` |
| 데이터 | `/opt/data/YourVault/data` | `D:\YourVault\data` (선택) |
| 스크립트 | `/opt/data/skills/learning-agent/scripts` | - |

---

## 📂 Obsidian 폴더 구조

```
D:/YourVault/
└── 학습/
    ├── CS/
    │   ├── Operating-System/
    │   │   ├── 퀴즈/
    │   │   └── 오답노트/
    │   ├── Database/
    │   │   ├── 퀴즈/
    │   │   └── 오답노트/
    │   └── Network/
    │       ├── 퀴즈/
    │       └── 오답노트/
    ├── AI/
    │   ├── Machine-Learning/
    │   │   ├── 퀴즈/
    │   │   └── 오답노트/
    │   └── Deep-Learning/
    │       ├── 퀴즈/
    │       └── 오답노트/
    └── Math/
        ├── Linear-Algebra/
        │   ├── 퀴즈/
        │   └── 오답노트/
        └── Probability/
            ├── 퀴즈/
            └── 오답노트/
```

---

## 🔧 수정된 파일 목록

| 파일 | 수정 내용 |
|------|----------|
| `/opt/data/skills/learning-agent/SKILL.md` | `obsidian_vault: /mnt/d/YourVault` |
| `/opt/data/skills/learning-agent/scripts/sync_obsidian.py` | 기본 경로 변경 |
| `/opt/data/skills/learning-agent/references/obsidian-schema.md` | 폴더 구조 업데이트 |
| `/opt/data/AI_Agent/config/agent-config.yaml` | 경로 매핑 업데이트 |

---

## ✅ 확인 사항

- [x] WSL 에서 `/mnt/d/YourVault/` 접근 가능
- [x] Obsidian Vault 가 `D:\YourVault` 로 설정됨
- [x] 테스트 파일 생성 완료 (`/opt/data/YourVault/학습/...`)

---

## 📋 다음 단계

1. **테스트 파일 복사** (WSL → Windows)
   ```powershell
   Copy-Item "\\wsl$\Ubuntu\opt\data\YourVault\학습\*" -Destination "D:\YourVault\학습\" -Recurse -Force
   ```

2. **Obsidian 에서 확인**
   - `학습/CS/Operating-System/오답노트/2026-08-07-OS-테스트.md`
   - `학습/AI/Machine-Learning/오답노트/2026-08-07-ML-테스트.md`
   - `학습/진도리포트/2026-08-07-테스트 - 주간리포트.md`

3. **태그 검색 테스트**
   - `tag:#오답노트`
   - `tag:#CS`
   - `tag:#테스트`

---

*2026-08-07 기준*
