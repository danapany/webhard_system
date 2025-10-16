import streamlit as st
from datetime import datetime, timedelta
from database.models import db
from config.settings import Config

class AuthManager:
    def __init__(self):
        self.session_timeout = timedelta(hours=Config.SESSION_TIMEOUT_HOURS)
    
    def is_authenticated(self):
        """사용자가 인증되어 있는지 확인"""
        if 'user' not in st.session_state:
            return False
        
        if 'last_activity' not in st.session_state:
            return False
        
        # 세션 타임아웃 확인
        if datetime.now() - st.session_state.last_activity > self.session_timeout:
            self.logout()
            return False
        
        # 마지막 활동 시간 업데이트
        st.session_state.last_activity = datetime.now()
        return True
    
    def login(self, username, password):
        """사용자 로그인"""
        user = db.authenticate_user(username, password)
        
        if user:
            st.session_state.user = user
            st.session_state.last_activity = datetime.now()
            return True
        
        return False
    
    def logout(self):
        """사용자 로그아웃"""
        if 'user' in st.session_state:
            del st.session_state.user
        if 'last_activity' in st.session_state:
            del st.session_state.last_activity
    
    def register(self, username, email, password, confirm_password):
        """사용자 회원가입"""
        # 입력값 검증
        if not username or not email or not password:
            return False, "모든 필드를 입력해주세요."
        
        if password != confirm_password:
            return False, "비밀번호가 일치하지 않습니다."
        
        if len(password) < 6:
            return False, "비밀번호는 6자리 이상이어야 합니다."
        
        # 사용자 생성
        user_id = db.create_user(username, email, password)
        
        if user_id:
            return True, "회원가입이 완료되었습니다!"
        else:
            return False, "이미 존재하는 사용자명 또는 이메일입니다."
    
    def get_current_user(self):
        """현재 로그인한 사용자 정보 반환"""
        if self.is_authenticated():
            # 최신 사용자 정보 조회 (포인트 등이 변경될 수 있음)
            return db.get_user_by_id(st.session_state.user['id'])
        return None
    
    def update_user_points(self):
        """현재 사용자의 포인트 정보 업데이트"""
        if self.is_authenticated():
            user = db.get_user_by_id(st.session_state.user['id'])
            if user:
                st.session_state.user = user

def show_login_page():
    """로그인 페이지 표시"""
    st.title("🍯 " + Config.SITE_NAME)
    st.subheader("로그인")
    
    # 탭으로 로그인/회원가입 구분
    tab1, tab2 = st.tabs(["로그인", "회원가입"])
    
    auth = AuthManager()
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("사용자명")
            password = st.text_input("비밀번호", type="password")
            submit = st.form_submit_button("로그인", use_container_width=True)
            
            if submit:
                if auth.login(username, password):
                    st.success("로그인 성공!")
                    st.rerun()
                else:
                    st.error("잘못된 사용자명 또는 비밀번호입니다.")
    
    with tab2:
        with st.form("register_form"):
            new_username = st.text_input("사용자명 (새 계정)")
            new_email = st.text_input("이메일")
            new_password = st.text_input("비밀번호 (새 계정)", type="password")
            confirm_password = st.text_input("비밀번호 확인", type="password")
            register = st.form_submit_button("회원가입", use_container_width=True)
            
            if register:
                success, message = auth.register(new_username, new_email, new_password, confirm_password)
                if success:
                    st.success(message)
                    st.info(f"🎉 회원가입 보너스로 {Config.INITIAL_POINTS} 포인트를 받았습니다!")
                else:
                    st.error(message)

def require_auth(func):
    """인증이 필요한 함수를 위한 데코레이터"""
    def wrapper(*args, **kwargs):
        auth = AuthManager()
        if not auth.is_authenticated():
            show_login_page()
            return
        return func(*args, **kwargs)
    return wrapper
