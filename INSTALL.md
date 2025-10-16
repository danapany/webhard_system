# 🍯 꿀파일 웹하드 시스템 설치 가이드

## 📋 시스템 요구사항
- Python 3.8 이상
- pip (Python 패키지 매니저)
- 최소 2GB 여유 디스크 공간

## 🚀 빠른 시작

### 1. 프로젝트 다운로드
```bash
# 프로젝트를 원하는 위치에 압축 해제
unzip webhard_system.zip
cd webhard_system
```

### 2. 가상환경 생성 (권장)
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Linux/Mac)
source venv/bin/activate

# 가상환경 활성화 (Windows)
venv\Scripts\activate
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. 시스템 테스트
```bash
python test_system.py
```

### 5. 애플리케이션 실행
```bash
streamlit run app.py
```

또는 실행 스크립트 사용:
```bash
./run.sh
```

### 6. 브라우저에서 접속
```
http://localhost:8501
```

## 🐳 Docker로 실행

### Docker Compose 사용 (권장)
```bash
docker-compose up -d
```

### 직접 Docker 빌드
```bash
docker build -t webhard-system .
docker run -p 8501:8501 -v $(pwd)/uploads:/app/uploads -v $(pwd)/database:/app/database webhard-system
```

## ⚙️ 환경 설정

### .env 파일 수정
`.env` 파일을 열어서 다음 설정들을 원하는 대로 수정하세요:

```env
# 데이터베이스 설정
DB_PATH=database/webhard.db

# 파일 업로드 설정
UPLOAD_PATH=uploads/
MAX_FILE_SIZE_MB=500
ALLOWED_EXTENSIONS=mp4,avi,mkv,mov,wmv,jpg,jpeg,png,gif,pdf,txt,docx,xlsx,zip,rar,7z

# 포인트 시스템 설정
INITIAL_POINTS=1000
UPLOAD_BONUS_POINTS=50
DOWNLOAD_COST_POINTS=10

# 보안 설정 (반드시 변경하세요!)
SECRET_KEY=your-secret-key-here-change-this-in-production
SESSION_TIMEOUT_HOURS=24

# 사이트 설정
SITE_NAME=꿀파일 시스템
SITE_DESCRIPTION=Streamlit 기반 파일 공유 플랫폼
ADMIN_EMAIL=admin@webhard.com
```

## 🔧 트러블슈팅

### 포트가 이미 사용 중인 경우
```bash
# 다른 포트로 실행
streamlit run app.py --server.port 8502
```

### 패키지 설치 오류
```bash
# pip 업그레이드
pip install --upgrade pip

# 캐시 클리어 후 재설치
pip install --no-cache-dir -r requirements.txt
```

### 권한 오류 (Linux/Mac)
```bash
# 업로드 디렉토리 권한 설정
chmod 755 uploads/
chmod 755 database/
```

### 데이터베이스 초기화
```bash
# 데이터베이스 파일 삭제 후 재시작
rm database/webhard.db
python test_system.py
```

## 📁 프로젝트 구조
```
webhard_system/
├── app.py                 # 메인 애플리케이션
├── .env                   # 환경변수
├── requirements.txt       # 패키지 의존성
├── run.sh                # 실행 스크립트
├── test_system.py        # 시스템 테스트
├── Dockerfile            # Docker 설정
├── docker-compose.yml    # Docker Compose 설정
├── config/               # 설정 파일들
│   └── settings.py
├── database/             # 데이터베이스 관련
│   └── models.py
├── modules/              # 핵심 모듈들
│   ├── auth/            # 인증 관련
│   ├── file_manager/    # 파일 관리
│   ├── point_system/    # 포인트 시스템
│   └── ui/              # UI 컴포넌트
├── uploads/              # 업로드된 파일 저장소
└── static/               # 정적 파일들
```

## 🎯 주요 기능

### 사용자 기능
- 회원가입 / 로그인
- 파일 업로드 (보너스 포인트 획득)
- 파일 다운로드 (포인트 사용)
- 포인트 관리
- 다운로드 내역 확인

### 파일 관리
- 다양한 파일 형식 지원
- 카테고리별 자동 분류
- 파일 검색 및 필터링
- 파일 크기 제한

### 포인트 시스템
- 회원가입 보너스
- 업로드 보너스
- 다운로드 비용
- 포인트 사용 내역

## 🔒 보안 고려사항

### 프로덕션 배포 시
1. `.env` 파일의 `SECRET_KEY` 변경
2. 파일 업로드 디렉토리 권한 설정
3. HTTPS 사용
4. 방화벽 설정
5. 정기적인 백업

## 📞 지원

문제가 발생하면 다음을 확인해주세요:
1. Python 버전 (3.8 이상)
2. 패키지 설치 상태
3. 디렉토리 권한
4. 포트 충돌
5. 시스템 테스트 결과

## 🔄 업데이트

새 버전으로 업데이트하려면:
1. 기존 데이터 백업
2. 새 파일들로 교체
3. requirements.txt로 패키지 업데이트
4. 테스트 실행
