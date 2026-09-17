#!/usr/bin/env python3
"""
Obsidian 동기화 스크립트
- 오답노트를 Markdown 형식으로 변환
- Obsidian Vault 에 저장
- 태그 및 링크 자동 생성
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

def load_wrong_answer(json_path):
    """오답 데이터 로드"""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_markdown(wrong_data, subject, topic):
    """
    Markdown 오답노트 생성
    
    Args:
        wrong_data: 오답 데이터 (JSON)
        subject: 과목 (CS, AI, Math)
        topic: 주제
    
    Returns:
        str: Markdown 내용
    """
    today = datetime.now().strftime("%Y-%m-%d")
    
    markdown = f"""---
created: {today}
subject: {subject}
topic: {topic}
difficulty: medium
status: review-needed
review_count: 0
last_reviewed: 
tags: [오답노트, {subject}, {topic}]
---

# 오답노트

## 문제
{wrong_data.get('question', 'N/A')}

## 내 답변
{wrong_data.get('user_answer', 'N/A')}

## 정답
{wrong_data.get('correct_answer', 'N/A')}

## 피드백
{wrong_data.get('feedback', 'N/A')}

## 관련 개념
- [[개념 1]]
- [[개념 2]]

## 복습 기록
{today} - 초기 기록
"""
    return markdown

def save_to_obsidian(markdown_content, subject, topic, vault_path="/mnt/d/YourVault"):
    """
    Obsidian Vault 에 저장
    
    Args:
        markdown_content: Markdown 내용
        subject: 과목
        topic: 주제
        vault_path: Obsidian Vault 경로
    """
    # 폴더 경로 생성
    base_path = Path(vault_path)  # WSL 경로 (/mnt/d/...)
    subject_path = base_path / "학습" / subject / topic / "오답노트"
    subject_path.mkdir(parents=True, exist_ok=True)
    
    # 파일명 생성
    filename = f"{datetime.now().strftime('%Y-%m-%d')}_{topic.replace(' ', '-')}.md"
    file_path = subject_path / filename
    
    # 저장
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"✅ Obsidian 저장 완료: {file_path}")
    return str(file_path)

if __name__ == "__main__":
    # 테스트
    test_data = {
        "question": "가상 메모리의 주요 목적은?",
        "user_answer": "메모리 속도 향상",
        "correct_answer": "물리 메모리의 한계를 극복하고 큰 프로그램을 실행하기 위함",
        "feedback": "가상 메모리는 속도보다 용량 확장이 주목적입니다."
    }
    
    md = generate_markdown(test_data, "CS", "Operating-System")
    print(md)
