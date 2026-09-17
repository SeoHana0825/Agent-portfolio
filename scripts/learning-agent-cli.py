#!/usr/bin/env python3
"""
학습 에이전트 - 대화형 CLI
사용자와 직접 상호작용하며 퀴즈 생성, 채점, 오답노트 관리
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Windows 경로
OBSIDIAN_VAULT = "/mnt/d/YourVault"
LEARNING_DIR = Path(OBSIDIAN_VAULT) / "학습"

def show_menu():
    """메뉴 표시"""
    print("\n" + "=" * 60)
    print("🎓 학습 에이전트 - 대화형 메뉴")
    print("=" * 60)
    print("1. 📝 새 퀴즈 생성")
    print("2. ✅ 퀴즈 채점")
    print("3. 📖 오답노트 확인")
    print("4. 📊 학습 진도 리포트")
    print("5. 🔄 복습 문제 확인")
    print("0. 종료")
    print("=" * 60)

def generate_quiz_interactive():
    """대화형 퀴즈 생성"""
    print("\n📝 퀴즈 생성")
    print("-" * 40)
    
    subject = input("과목을 입력하세요 (CS/AI/Math): ").strip().upper()
    topic = input("주제를 입력하세요 (예: Operating System): ").strip()
    difficulty = input("난이도를 입력하세요 (easy/medium/hard): ").strip().lower()
    count = input("문제 수를 입력하세요 (기본값: 5): ").strip()
    count = int(count) if count.isdigit() else 5
    
    print(f"\n✅ {subject} - {topic} 퀴즈 {count}개 생성 중...")
    print("🔔 힌트: 실제 퀴즈는 매일 오전 9 시에 자동 생성됩니다.")
    print(f"📁 저장 위치: {LEARNING_DIR}/{subject}/{topic.replace(' ', '-')}/퀴즈/")

def grade_quiz_interactive():
    """퀴즈 채점"""
    print("\n✅ 퀴즈 채점")
    print("-" * 40)
    
    question_id = input("문제 ID 를 입력하세요 (예: Q1): ").strip()
    user_answer = input("답변을 입력하세요: ").strip()
    
    print(f"\n📊 채점 결과:")
    print(f"문제: {question_id}")
    print(f"내 답변: {user_answer}")
    print("⏳ AI 채점 결과 대기 중...")
    print("🔔 힌트: 오답은 자동으로 오답노트에 기록됩니다.")

def show_wrong_notes():
    """오답노트 확인"""
    print("\n📖 오답노트 확인")
    print("-" * 40)
    
    subject = input("과목을 입력하세요 (CS/AI/Math/ALL): ").strip().upper()
    
    wrong_dir = LEARNING_DIR / ("**" if subject == "ALL" else f"{subject}/**/오답노트")
    wrong_files = list(LEARNING_DIR.glob(str(wrong_dir / "*.md")))
    
    if wrong_files:
        print(f"\n✅ 찾은 오답노트: {len(wrong_files)}개")
        for f in wrong_files[:10]:  # 최대 10 개 표시
            print(f"  - {f.name}")
    else:
        print("\n📭 아직 오답노트가 없습니다.")

def show_progress_report():
    """학습 진도 리포트"""
    print("\n📊 학습 진도 리포트")
    print("-" * 40)
    
    today = datetime.now().strftime("%Y-%m-%d")
    report_file = LEARNING_DIR / f"일일 - 학습 - 리포트-{today}.md"
    
    if report_file.exists():
        print(f"\n✅ 오늘 리포트 존재: {report_file.name}")
        with open(report_file, 'r', encoding='utf-8') as f:
            content = f.read()
            print("\n" + content[:500])  # 처음 500 자만 표시
    else:
        print("\n📭 오늘 리포트가 아직 생성되지 않았습니다.")
        print("🕘 오전 9 시에 자동 생성됩니다.")

def show_review_items():
    """복습 문제 확인"""
    print("\n🔄 복습 문제 확인")
    print("-" * 40)
    
    print("⏳ MineSync 연동된 복습 스케줄 확인 중...")
    print("🔔 힌트: 오답노트에 '다음 복습일'이 기록됩니다.")

def main():
    """메인 루프"""
    print("\n" + "=" * 60)
    print("🎓 학습 에이전트에 오신 것을 환영합니다!")
    print(f"📁 Obsidian Vault: {OBSIDIAN_VAULT}")
    print(f"📚 학습 폴더: {LEARNING_DIR}")
    print("=" * 60)
    
    while True:
        show_menu()
        choice = input("\n선택하세요 (0-5): ").strip()
        
        if choice == "1":
            generate_quiz_interactive()
        elif choice == "2":
            grade_quiz_interactive()
        elif choice == "3":
            show_wrong_notes()
        elif choice == "4":
            show_progress_report()
        elif choice == "5":
            show_review_items()
        elif choice == "0":
            print("\n👋 다음에 만나요! 화이팅! 💪")
            break
        else:
            print("\n❌ 잘못된 입력입니다. 다시 선택하세요.")

if __name__ == "__main__":
    main()
