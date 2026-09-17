#!/bin/bash
# D:/YourAgent/ 폴더 구조 자동 생성 스크립트 (Windows PowerShell 용)
# Windows 에서 실행: .\setup-folders.ps1

$base = "D:\YourAgent"

Write-Host "🚀 AI Agent 폴더 구조 생성 중..." -ForegroundColor Cyan

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
    $path = Join-Path $base $folder
    if (!(Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-Host "  ✅ $folder" -ForegroundColor Green
    } else {
        Write-Host "  ⏭️  $folder (기존)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "✅ 폴더 구조 생성 완료!" -ForegroundColor Green
Write-Host ""
Write-Host "📁 생성된 구조:" -ForegroundColor Cyan
Write-Host "   D:/YourAgent/"
Write-Host "   ├── Obsidian_Vault/ (옵시디언 버클트)"
Write-Host "   ├── data/ (에이전트 데이터)"
Write-Host "   ├── scripts/ (실행 스크립트)"
Write-Host "   ├── templates/ (템플릿)"
Write-Host "   └── config/ (설정)"
Write-Host ""
Write-Host "💡 다음 단계:" -ForegroundColor Cyan
Write-Host "   1. Obsidian 실행"
Write-Host "   2. 'Open folder as vault' 선택"
Write-Host "   3. D:\YourAgent\Obsidian_Vault 선택"
Write-Host ""
