#!/bin/bash

# 웹하드 시스템 실행 스크립트

echo "🍯 꿀파일 시스템을 시작합니다..."

# 가상환경이 있으면 활성화
if [ -d "venv" ]; then
    echo "가상환경을 활성화합니다..."
    source venv/bin/activate
fi

# 필요한 패키지 설치
echo "필요한 패키지를 설치합니다..."
pip install -r requirements.txt

# 필요한 디렉토리 생성
echo "필요한 디렉토리를 생성합니다..."
mkdir -p uploads
mkdir -p database
mkdir -p static

# Streamlit 앱 실행
echo "Streamlit 애플리케이션을 시작합니다..."
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
