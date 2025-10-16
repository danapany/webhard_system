import streamlit as st
import os
import sys
from pathlib import Path

# 프로젝트 루트를 Python path에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 모듈 임포트
from config.settings import Config
from modules.auth.auth_manager import AuthManager, show_login_page, require_auth
from modules.ui.components import (
    show_ghibli_header, show_ghibli_navigation, show_ghibli_file_list, 
    show_ghibli_upload_form, show_ghibli_user_stats, show_ghibli_point_management,
    show_ghibli_download_history
)
from modules.point_system.point_manager import PointManager

# Streamlit 페이지 설정
st.set_page_config(
    page_title=Config.SITE_NAME,
    page_icon="🍯",
    layout="wide",
    initial_sidebar_state="collapsed"  # 사이드바 축소
)

# 지브리 스타일 CSS
def load_ghibli_css():
    st.markdown("""
    <style>
    /* 전체 앱 배경 */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 100%;
        background: linear-gradient(135deg, #E8F5E8, #F1F8E9);
    }
    
    /* 지브리 색상 변수 */
    :root {
        --ghibli-green-dark: #1B5E20;
        --ghibli-green-medium: #2E7D32;
        --ghibli-green-light: #4CAF50;
        --ghibli-green-bg: #C8E6C9;
        --ghibli-yellow: #FFE082;
        --ghibli-orange: #FF9800;
        --ghibli-brown: #8D6E63;
        --ghibli-cream: #FFF8E1;
    }
    
    /* 메인 헤더 스타일 */
    .ghibli-header {
        background: linear-gradient(135deg, #A5D6A7, #81C784);
        padding: 20px;
        border-radius: 25px;
        border: 3px solid #4CAF50;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #66BB6A, #4CAF50) !important;
        color: white !important;
        border: 2px solid #2E7D32 !important;
        border-radius: 20px !important;
        font-weight: bold !important;
        box-shadow: 0 3px 6px rgba(46, 125, 50, 0.3) !important;
        transition: all 0.3s ease !important;
        font-family: 'Comic Sans MS', cursive !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #4CAF50, #388E3C) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(46, 125, 50, 0.4) !important;
    }
    
    /* Primary 버튼 스타일 */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #FFE082, #FFCC02) !important;
        color: #E65100 !important;
        border: 2px solid #FFA000 !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #FFCC02, #FF9800) !important;
    }
    
    /* 입력 필드 스타일 */
    .stTextInput > div > div > input {
        border: 2px solid #81C784 !important;
        border-radius: 15px !important;
        background: #F8FFF8 !important;
        font-family: 'Comic Sans MS', cursive !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4CAF50 !important;
        box-shadow: 0 0 10px rgba(76, 175, 80, 0.3) !important;
    }
    
    /* 셀렉트박스 스타일 */
    .stSelectbox > div > div > div {
        border: 2px solid #81C784 !important;
        border-radius: 15px !important;
        background: #F8FFF8 !important;
        font-family: 'Comic Sans MS', cursive !important;
    }
    
    /* 메트릭 카드 스타일 */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #FFE082, #FFCC02) !important;
        border: 3px solid #FFA000 !important;
        border-radius: 20px !important;
        padding: 15px !important;
        box-shadow: 0 4px 8px rgba(255, 160, 0, 0.3) !important;
    }
    
    [data-testid="metric-container"] > div {
        color: #E65100 !important;
        font-weight: bold !important;
        font-family: 'Comic Sans MS', cursive !important;
    }
    
    /* 성공 메시지 */
    .stSuccess {
        background: linear-gradient(135deg, #C8E6C9, #A5D6A7) !important;
        border: 2px solid #4CAF50 !important;
        border-radius: 15px !important;
        color: #1B5E20 !important;
    }
    
    /* 에러 메시지 */
    .stError {
        background: linear-gradient(135deg, #FFCDD2, #F8BBD9) !important;
        border: 2px solid #F44336 !important;
        border-radius: 15px !important;
    }
    
    /* 정보 메시지 */
    .stInfo {
        background: linear-gradient(135deg, #E1F5FE, #B3E5FC) !important;
        border: 2px solid #03A9F4 !important;
        border-radius: 15px !important;
    }
    
    /* 경고 메시지 */
    .stWarning {
        background: linear-gradient(135deg, #FFF3E0, #FFE0B2) !important;
        border: 2px solid #FF9800 !important;
        border-radius: 15px !important;
    }
    
    /* 확장 가능한 섹션 */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #C8E6C9, #A5D6A7) !important;
        border: 2px solid #4CAF50 !important;
        border-radius: 15px !important;
        color: #1B5E20 !important;
        font-weight: bold !important;
        font-family: 'Comic Sans MS', cursive !important;
    }
    
    .streamlit-expanderContent {
        background: #F1F8E9 !important;
        border: 2px solid #8BC34A !important;
        border-top: none !important;
        border-radius: 0 0 15px 15px !important;
    }
    
    /* 파일 업로더 스타일 */
    .stFileUploader > div {
        border: 3px dashed #81C784 !important;
        border-radius: 20px !important;
        background: linear-gradient(135deg, #E8F5E8, #F1F8E9) !important;
        padding: 20px !important;
    }
    
    /* 다운로드 버튼 스타일 */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #FFCC02, #FF9800) !important;
        color: #E65100 !important;
        border: 2px solid #F57F17 !important;
        border-radius: 20px !important;
        font-weight: bold !important;
        font-family: 'Comic Sans MS', cursive !important;
    }
    
    /* 제목 스타일 */
    h1, h2, h3 {
        color: #2E7D32 !important;
        font-family: 'Comic Sans MS', cursive !important;
        text-shadow: 2px 2px 4px rgba(46, 125, 50, 0.2) !important;
    }
    
    /* 사이드바 스타일 (사용하지 않지만 대비) */
    .css-1d391kg {
        background: linear-gradient(180deg, #E8F5E8, #C8E6C9) !important;
    }
    
    /* 캡션 텍스트 */
    .caption {
        color: #558B2F !important;
        font-style: italic !important;
    }
    </style>
    """, unsafe_allow_html=True)

def show_point_management():
    """포인트 관리 페이지"""
    auth = AuthManager()
    point_manager = PointManager()
    user = auth.get_current_user()
    
    st.subheader("💰 포인트 관리")
    
    if not user:
        st.error("로그인이 필요합니다.")
        return
    
    # 현재 포인트 표시
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("현재 포인트", f"{user['points']:,}P")
    with col2:
        st.metric("다운로드 비용", f"{Config.DOWNLOAD_COST_POINTS}P")
    with col3:
        st.metric("업로드 보너스", f"{Config.UPLOAD_BONUS_POINTS}P")
    
    st.divider()
    
    # 포인트 히스토리
    st.subheader("📊 포인트 사용 내역")
    
    transactions, total_count = point_manager.get_point_history(user['id'])
    
    if transactions:
        for transaction in transactions:
            col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
            
            with col1:
                st.write(transaction['description'])
                if transaction['file_name']:
                    st.caption(f"파일: {transaction['file_name']}")
            
            with col2:
                transaction_type = "획득" if transaction['transaction_type'] == 'earn' else "사용"
                st.write(transaction_type)
            
            with col3:
                color = "green" if transaction['transaction_type'] == 'earn' else "red"
                sign = "+" if transaction['transaction_type'] == 'earn' else "-"
                st.markdown(f"<span style='color: {color}'>{sign}{transaction['amount']}P</span>", 
                           unsafe_allow_html=True)
            
            with col4:
                st.caption(transaction['created_at'])
        
        st.divider()
    else:
        st.info("포인트 사용 내역이 없습니다.")

def show_download_history():
    """다운로드 내역 페이지"""
    auth = AuthManager()
    point_manager = PointManager()
    user = auth.get_current_user()
    
    st.subheader("📜 다운로드 내역")
    
    if not user:
        st.error("로그인이 필요합니다.")
        return
    
    downloads, total_count = point_manager.get_download_history(user['id'])
    
    if downloads:
        for download in downloads:
            col1, col2, col3, col4 = st.columns([3, 1, 1, 2])
            
            with col1:
                st.write(f"**{download['original_name']}**")
                st.caption(f"업로더: {download['uploader_name']}")
            
            with col2:
                st.write(f"{download['points_spent']}P")
            
            with col3:
                st.caption("완료")
            
            with col4:
                st.caption(download['download_at'])
        
        st.divider()
        st.info(f"총 {total_count}개의 파일을 다운로드했습니다.")
    else:
        st.info("다운로드 내역이 없습니다.")

@require_auth
def show_ghibli_main_app():
    """지브리 스타일 메인 애플리케이션 화면"""
    # 지브리 CSS 로드
    load_ghibli_css()
    
    # 헤더 표시
    category, search_query = show_ghibli_header()
    
    # 네비게이션 메뉴
    menu = show_ghibli_navigation()
    
    # 현재 페이지 상태 관리
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1
    
    # 카테고리나 검색어가 변경되면 페이지를 1로 리셋
    if 'last_category' not in st.session_state:
        st.session_state.last_category = category
    if 'last_search' not in st.session_state:
        st.session_state.last_search = search_query
        
    if (st.session_state.last_category != category or 
        st.session_state.last_search != search_query):
        st.session_state.current_page = 1
        st.session_state.last_category = category
        st.session_state.last_search = search_query
    
    # 메뉴에 따른 페이지 표시
    if menu == "🏠 마을 광장":
        # 메인 페이지 - 파일 목록
        show_ghibli_file_list(
            category=category,
            search_query=search_query,
            page=st.session_state.current_page
        )
    
    elif menu == "📤 나무 심기":
        show_ghibli_upload_form()
    
    elif menu == "📊 내 정원":
        show_ghibli_user_stats()
    
    elif menu == "💰 도토리 주머니":
        show_ghibli_point_management()
    
    elif menu == "📜 수집 일지":
        show_ghibli_download_history()

def main():
    """메인 함수"""
    # 필요한 디렉토리 생성
    Config.ensure_directories()
    
    # 데이터베이스 초기화
    from database.models import db
    
    # 인증 확인
    auth = AuthManager()
    
    if not auth.is_authenticated():
        show_login_page()
    else:
        show_ghibli_main_app()

if __name__ == "__main__":
    main()
