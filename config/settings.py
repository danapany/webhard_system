import os
from dotenv import load_dotenv
from pathlib import Path

# 환경변수 로드
load_dotenv()

class Config:
    # 데이터베이스 설정
    DB_PATH = os.getenv('DB_PATH', 'database/webhard.db')
    
    # 파일 업로드 설정
    UPLOAD_PATH = os.getenv('UPLOAD_PATH', 'uploads/')
    MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', 500))
    ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS', '').split(',')
    
    # 포인트 시스템 설정
    INITIAL_POINTS = int(os.getenv('INITIAL_POINTS', 1000))
    UPLOAD_BONUS_POINTS = int(os.getenv('UPLOAD_BONUS_POINTS', 50))
    DOWNLOAD_COST_POINTS = int(os.getenv('DOWNLOAD_COST_POINTS', 10))
    
    # 보안 설정
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-this-in-production')
    SESSION_TIMEOUT_HOURS = int(os.getenv('SESSION_TIMEOUT_HOURS', 24))
    
    # 사이트 설정
    SITE_NAME = os.getenv('SITE_NAME', '꿀파일 시스템')
    SITE_DESCRIPTION = os.getenv('SITE_DESCRIPTION', 'Streamlit 기반 파일 공유 플랫폼')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@webhard.com')
    
    # 카테고리 설정
    CATEGORIES = {
        'all': '전체',
        'movie': '영화', 
        'drama': '드라마',
        'video': '동영상',
        'game': '게임',
        'anime': '애니',
        'music': '음악',
        'document': '문서',
        'image': '이미지',
        'software': '소프트웨어',
        'other': '기타'
    }
    
    # 파일 타입별 카테고리 매핑
    FILE_TYPE_MAPPING = {
        'mp4': 'video', 'avi': 'video', 'mkv': 'video', 'mov': 'video', 'wmv': 'video',
        'jpg': 'image', 'jpeg': 'image', 'png': 'image', 'gif': 'image',
        'pdf': 'document', 'txt': 'document', 'docx': 'document', 'xlsx': 'document',
        'zip': 'software', 'rar': 'software', '7z': 'software', 'exe': 'software',
        'mp3': 'music', 'wav': 'music', 'flac': 'music'
    }
    
    @classmethod
    def ensure_directories(cls):
        """필요한 디렉토리들이 존재하는지 확인하고 없으면 생성"""
        directories = [
            Path(cls.UPLOAD_PATH),
            Path(cls.DB_PATH).parent,
            Path('static'),
            Path('modules'),
            Path('modules/auth'),
            Path('modules/file_manager'), 
            Path('modules/point_system'),
            Path('modules/ui')
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
