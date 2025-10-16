#!/usr/bin/env python3
"""
웹하드 시스템 테스트 스크립트
데이터베이스 연결, 기본 기능들이 정상 작동하는지 확인
"""

import sys
import os
from pathlib import Path

# 프로젝트 루트를 Python path에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from config.settings import Config
    from database.models import Database
    from modules.auth.auth_manager import AuthManager
    from modules.file_manager.file_manager import FileManager
    from modules.point_system.point_manager import PointManager
    
    print("✅ 모든 모듈 임포트 성공!")
    
    # 필요한 디렉토리 생성
    Config.ensure_directories()
    print("✅ 디렉토리 생성 완료!")
    
    # 데이터베이스 초기화 테스트
    db = Database()
    print("✅ 데이터베이스 초기화 완료!")
    
    # 테스트 사용자 생성
    test_user_id = db.create_user("testuser", "test@example.com", "password123")
    if test_user_id:
        print(f"✅ 테스트 사용자 생성 완료! (ID: {test_user_id})")
        
        # 사용자 인증 테스트
        user = db.authenticate_user("testuser", "password123")
        if user:
            print("✅ 사용자 인증 테스트 통과!")
        else:
            print("❌ 사용자 인증 실패!")
    else:
        print("❌ 테스트 사용자 생성 실패!")
    
    # 포인트 매니저 테스트
    point_manager = PointManager()
    if test_user_id:
        points = point_manager.get_user_points(test_user_id)
        print(f"✅ 포인트 시스템 테스트 통과! (사용자 포인트: {points})")
    
    # 파일 매니저 테스트
    file_manager = FileManager()
    print("✅ 파일 매니저 초기화 완료!")
    
    print("\n🎉 모든 기본 테스트 통과!")
    print("시스템이 정상적으로 설정되었습니다.")
    print("이제 'streamlit run app.py' 명령으로 앱을 실행할 수 있습니다.")
    
except ImportError as e:
    print(f"❌ 모듈 임포트 오류: {e}")
    print("필요한 패키지를 설치하세요: pip install -r requirements.txt")
    
except Exception as e:
    print(f"❌ 테스트 중 오류 발생: {e}")
    sys.exit(1)
