#!/usr/bin/env python3
"""
지브리 스타일 웹하드 시스템 문법 테스트 스크립트
실행 전에 Python 문법 오류가 있는지 확인합니다.
"""

import sys
import os
from pathlib import Path
import ast

def test_syntax():
    """Python 파일들의 문법을 테스트합니다."""
    
    print("🌿 지브리 스타일 웹하드 시스템 문법 검사 시작...")
    
    # 테스트할 Python 파일들
    python_files = [
        "app.py",
        "config/settings.py", 
        "database/models.py",
        "modules/auth/auth_manager.py",
        "modules/file_manager/file_manager.py",
        "modules/point_system/point_manager.py",
        "modules/ui/components.py"
    ]
    
    errors = []
    
    for file_path in python_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    source = f.read()
                
                # Python 문법 검사
                ast.parse(source)
                print(f"✅ {file_path} - 문법 OK")
                
            except SyntaxError as e:
                error_msg = f"❌ {file_path} - 문법 오류: {e.msg} (라인 {e.lineno})"
                print(error_msg)
                errors.append(error_msg)
                
            except Exception as e:
                error_msg = f"⚠️ {file_path} - 확인 중 오류: {str(e)}"
                print(error_msg)
                errors.append(error_msg)
        else:
            error_msg = f"❓ {file_path} - 파일이 존재하지 않음"
            print(error_msg)
            errors.append(error_msg)
    
    print("\n" + "="*50)
    
    if errors:
        print(f"❌ {len(errors)}개의 문제가 발견되었습니다:")
        for error in errors:
            print(f"  - {error}")
        print("\n💡 문제를 해결한 후 다시 테스트해주세요.")
        return False
    else:
        print("🎉 모든 파일의 문법이 정상입니다!")
        print("✨ 이제 'streamlit run app.py' 명령으로 앱을 실행할 수 있습니다.")
        return True

if __name__ == "__main__":
    success = test_syntax()
    sys.exit(0 if success else 1)
