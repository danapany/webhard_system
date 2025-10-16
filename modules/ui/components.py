import streamlit as st
import pandas as pd
from datetime import datetime
from config.settings import Config
from modules.auth.auth_manager import AuthManager
from modules.file_manager.file_manager import FileManager
from modules.point_system.point_manager import PointManager

def show_ghibli_navigation():
    """지브리 스타일 네비게이션 메뉴"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #C8E6C9, #A5D6A7); 
                padding: 15px; border-radius: 25px; margin: 20px 0; 
                border: 3px solid #4CAF50; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
        <div style="display: flex; justify-content: space-around; align-items: center;">
            <span style="color: #1B5E20; font-weight: bold;">🌟 마법의 메뉴 🌟</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 메뉴 옵션들
    menu_options = [
        "🏠 마을 광장",
        "📤 나무 심기", 
        "📊 내 정원",
        "💰 도토리 주머니",
        "📜 수집 일지"
    ]
    
    # 가로 메뉴 버튼들
    cols = st.columns(len(menu_options))
    
    for i, (col, option) in enumerate(zip(cols, menu_options)):
        with col:
            if st.button(option, key=f"nav_{i}", use_container_width=True):
                st.session_state.current_menu = option
                st.rerun()
    
    # 현재 메뉴 상태 관리
    if 'current_menu' not in st.session_state:
        st.session_state.current_menu = "🏠 마을 광장"
    
    return st.session_state.current_menu

def show_ghibli_header():
    """지브리 스타일 헤더 표시"""
    auth = AuthManager()
    user = auth.get_current_user()
    
    # 상단 헤더
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    
    with col1:
        st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <h1 style="color: #2E7D32; font-family: 'Comic Sans MS', cursive; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
                🍯 꿀파일
            </h1>
            <span style="margin-left: 10px; color: #66BB6A; font-size: 14px;">자연이 주는 달콤한 공유</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # 카테고리
        category = st.selectbox(
            "🌿 카테고리",
            options=list(Config.CATEGORIES.keys()),
            format_func=lambda x: f"🌟 {Config.CATEGORIES[x]}",
            key="category_filter"
        )
    
    with col3:
        # 검색
        search_query = st.text_input(
            "🔍 마법의 검색",
            key="search_query",
            placeholder="원하는 파일을 찾아보세요...",
            help="숲 속에서 보물을 찾듯이 검색해보세요!"
        )
    
    with col4:
        if user:
            st.markdown(f"""
            <div style="text-align: center; background: linear-gradient(135deg, #FFE082, #FFCC02); 
                        padding: 15px; border-radius: 20px; border: 3px solid #FFA000; margin-top: 25px;">
                <div style="color: #E65100; font-weight: bold; font-size: 12px;">🌟 도토리 주머니</div>
                <div style="color: #BF360C; font-size: 20px; font-weight: bold;">{user['points']:,}P</div>
                <div style="color: #E65100; font-size: 10px;">✨ {user['username']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚪 숲으로 돌아가기", key="logout_btn"):
                auth.logout()
                st.rerun()
        else:
            st.button("🌱 숲에 들어가기", key="login_btn")
    
    return category, search_query

def show_menu_tabs():
    """상단 메뉴 탭 표시"""
    # 메뉴 탭
    menu = st.tabs(["🏠 메인", "📤 업로드", "📊 내 정보", "💰 포인트", "📜 다운로드 내역"])
    return menu

def show_ghibli_file_list(category='all', search_query='', page=1, per_page=10):
    """지브리 스타일 파일 목록 표시"""
    file_manager = FileManager()
    point_manager = PointManager()
    auth = AuthManager()
    user = auth.get_current_user()
    
    offset = (page - 1) * per_page
    files, total_count = file_manager.get_files_list(
        category=category,
        search_query=search_query,
        limit=per_page,
        offset=offset
    )
    
    if not files:
        st.markdown("""
        <div style="text-align: center; padding: 50px; background: linear-gradient(135deg, #E8F5E8, #C8E6C9); 
                    border-radius: 20px; border: 3px solid #4CAF50;">
            <h3 style="color: #2E7D32;">🌿 아직 이 숲에는 파일이 없어요</h3>
            <p style="color: #388E3C;">새로운 파일을 심어보세요!</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # 총 페이지 수 계산
    total_pages = (total_count + per_page - 1) // per_page
    
    # 파일 목록 헤더
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #A5D6A7, #81C784); 
                padding: 15px; border-radius: 15px; margin: 20px 0; border: 2px solid #4CAF50;">
        <h3 style="color: #1B5E20; text-align: center; margin: 0;">
            🌳 숲 속 보물 목록 ({total_count:,}개의 보물) 🌳
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # 테이블 헤더
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFE082, #FFCC02); 
                padding: 10px; border-radius: 10px; margin: 10px 0; border: 2px solid #FFA000;">
        <div style="display: grid; grid-template-columns: 0.5fr 3fr 1fr 1fr 1fr; gap: 10px; font-weight: bold; color: #E65100;">
            <div>🔢</div>
            <div>📁 보물 이름</div>
            <div>📏 크기</div>
            <div>🪙 가격</div>
            <div>⚡ 행동</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 파일 목록 표시
    for i, file in enumerate(files):
        # 카테고리별 이모지
        category_emoji = {
            'movie': '🎬', 'drama': '📺', 'video': '🎥', 'game': '🎮',
            'anime': '🌸', 'music': '🎵', 'document': '📄', 'image': '🖼️',
            'software': '💾', 'other': '🌿'
        }.get(file['category'], '🌿')
        
        # 파일 카드
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #F1F8E9, #DCEDC8); 
                    padding: 15px; border-radius: 15px; margin: 5px 0; 
                    border: 2px solid #8BC34A; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="display: grid; grid-template-columns: 0.5fr 3fr 1fr 1fr 1fr; gap: 10px; align-items: center;">
                <div style="text-align: center; font-weight: bold; color: #33691E;">
                    {offset + i + 1}
                </div>
                <div>
                    <div style="color: #2E7D32; font-weight: bold; font-size: 16px;">
                        {category_emoji} {file['original_name']}
                    </div>
                    <div style="color: #689F38; font-size: 12px;">
                        👤 {file['uploader_name']} | 📅 {file['created_at'][:10]} | 📂 {Config.CATEGORIES.get(file['category'], '기타')}
                    </div>
                </div>
                <div style="text-align: center; color: #558B2F; font-weight: bold;">
                    {file_manager.format_file_size(file['file_size'])}
                </div>
                <div style="text-align: center; color: #F57F17; font-weight: bold;">
                    {file['price']}P
                </div>
                <div style="text-align: center;">
        """, unsafe_allow_html=True)
        
        # 다운로드 버튼 로직
        if user:
            if file['uploader_id'] == user['id']:
                st.markdown("""
                <span style="background: #C8E6C9; color: #2E7D32; padding: 5px 10px; 
                             border-radius: 15px; font-size: 12px;">🌱 내 파일</span>
                """, unsafe_allow_html=True)
            elif point_manager.has_downloaded_file(user['id'], file['id']):
                if st.button("🔄 재수확", key=f"redown_{file['id']}", help="이미 수확한 보물을 다시 가져가기"):
                    show_ghibli_download_modal(file)
            elif point_manager.can_afford_download(user['id'], file['price']):
                if st.button("✨ 수확", key=f"down_{file['id']}", type="primary", help="도토리를 내고 보물 가져가기"):
                    show_ghibli_download_modal(file)
            else:
                st.markdown("""
                <span style="background: #FFCDD2; color: #C62828; padding: 5px 10px; 
                             border-radius: 15px; font-size: 12px;">💸 도토리 부족</span>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <span style="background: #FFE0B2; color: #EF6C00; padding: 5px 10px; 
                         border-radius: 15px; font-size: 12px;">🚪 입장 필요</span>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div></div>", unsafe_allow_html=True)
    
    # 페이지네이션
    if total_pages > 1:
        show_ghibli_pagination(page, total_pages)

def get_file_icon(file_type):
    """파일 타입에 따른 아이콘 반환"""
    icons = {
        'mp4': '🎬', 'avi': '🎬', 'mkv': '🎬', 'mov': '🎬', 'wmv': '🎬',
        'jpg': '🖼️', 'jpeg': '🖼️', 'png': '🖼️', 'gif': '🖼️',
        'pdf': '📄', 'txt': '📝', 'docx': '📄', 'xlsx': '📊',
        'zip': '📦', 'rar': '📦', '7z': '📦',
        'mp3': '🎵', 'wav': '🎵', 'flac': '🎵',
        'exe': '⚙️', 'msi': '⚙️'
    }
    return icons.get(file_type.lower(), '📁')

def show_ghibli_download_modal(file):
    """지브리 스타일 다운로드 모달 표시"""
    auth = AuthManager()
    point_manager = PointManager()
    file_manager = FileManager()
    user = auth.get_current_user()
    
    if not user:
        st.error("🚪 숲에 들어가려면 로그인이 필요해요!")
        return
    
    # 이미 다운로드한 파일인지 확인
    already_downloaded = point_manager.has_downloaded_file(user['id'], file['id'])
    
    with st.expander(f"🌟 {file['original_name']} 보물 수확하기", expanded=True):
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E8F5E8, #C8E6C9); 
                    padding: 20px; border-radius: 20px; border: 3px solid #4CAF50;">
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style="background: #F1F8E9; padding: 15px; border-radius: 15px; border: 2px solid #8BC34A;">
                <h4 style="color: #2E7D32; margin: 0;">📁 보물 정보</h4>
                <p style="color: #388E3C; margin: 5px 0;"><strong>이름:</strong> {file['original_name']}</p>
                <p style="color: #388E3C; margin: 5px 0;"><strong>크기:</strong> {file_manager.format_file_size(file['file_size'])}</p>
                <p style="color: #388E3C; margin: 5px 0;"><strong>나무지기:</strong> {file['uploader_name']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if already_downloaded:
                st.markdown("""
                <div style="background: #C8E6C9; padding: 15px; border-radius: 15px; border: 2px solid #4CAF50;">
                    <h4 style="color: #1B5E20; margin: 0;">✅ 이미 수확한 보물</h4>
                    <p style="color: #2E7D32; margin: 5px 0;">이미 가지고 있는 보물이에요!</p>
                    <p style="color: #2E7D32; margin: 5px 0;"><strong>비용:</strong> 0 도토리 (무료)</p>
                </div>
                """, unsafe_allow_html=True)
                cost = 0
            else:
                st.markdown(f"""
                <div style="background: #FFE082; padding: 15px; border-radius: 15px; border: 2px solid #FFA000;">
                    <h4 style="color: #E65100; margin: 0;">💰 도토리 교환</h4>
                    <p style="color: #EF6C00; margin: 5px 0;"><strong>필요한 도토리:</strong> {file['price']}개</p>
                    <p style="color: #EF6C00; margin: 5px 0;"><strong>내 도토리:</strong> {user['points']}개</p>
                </div>
                """, unsafe_allow_html=True)
                cost = file['price']
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 다운로드 버튼
        if st.button("🌟 보물 수확하기!", use_container_width=True, type="primary"):
            if cost > 0:
                success, message = point_manager.process_download_payment(
                    user['id'], file['id'], file['price']
                )
                if not success:
                    st.error(f"❌ {message}")
                    return
                
                st.success(f"✨ {message}")
                auth.update_user_points()  # 포인트 정보 갱신
            
            # 실제 파일 다운로드
            file_path = file_manager.get_file_path(file['stored_name'])
            if file_path and file_path.exists():
                with open(file_path, 'rb') as f:
                    st.download_button(
                        label="💾 보물 주머니에 담기",
                        data=f.read(),
                        file_name=file['original_name'],
                        mime=f"application/octet-stream",
                        use_container_width=True
                    )
                st.balloons()
                st.success("🎉 보물을 성공적으로 수확했어요!")
            else:
                st.error("❌ 보물을 찾을 수 없어요. 나무지기에게 문의해보세요!")

def show_download_modal(file):
    """다운로드 모달 표시"""
    auth = AuthManager()
    point_manager = PointManager()
    file_manager = FileManager()
    user = auth.get_current_user()
    
    if not user:
        st.error("🔐 로그인이 필요합니다.")
        return
    
    # 이미 다운로드한 파일인지 확인
    already_downloaded = point_manager.has_downloaded_file(user['id'], file['id'])
    
    # 파일 아이콘 가져오기
    file_icon = get_file_icon(file['file_type'])
    
    with st.expander(f"{file_icon} {file['original_name']} 다운로드", expanded=True):
        # 파일 정보 카드
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f8f9fa, #e9ecef); 
                    padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;
                    border: 1px solid #dee2e6;'>
        """, unsafe_allow_html=True)
        
        info_col1, info_col2 = st.columns(2)
        
        with info_col1:
            st.markdown(f"**📄 파일명:** {file['original_name']}")
            st.markdown(f"**📊 크기:** {file_manager.format_file_size(file['file_size'])}")
            st.markdown(f"**📂 카테고리:** {Config.CATEGORIES.get(file['category'], '기타')}")
        
        with info_col2:
            st.markdown(f"**👤 업로더:** {file['uploader_name']}")
            st.markdown(f"**📅 업로드일:** {file['created_at'][:10]}")
            st.markdown(f"**⬇️ 다운로드 수:** {file['download_count']}회")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 비용 정보
        cost_col1, cost_col2 = st.columns(2)
        
        with cost_col1:
            if already_downloaded:
                st.success("✅ **이미 다운로드한 파일입니다**")
                st.info("💰 **재다운로드 비용:** 무료")
                cost = 0
            else:
                st.warning(f"💰 **다운로드 비용:** {file['price']} 포인트")
                cost = file['price']
        
        with cost_col2:
            remaining_points = user['points'] - cost
            st.info(f"**💎 현재 포인트:** {user['points']} P")
            if cost > 0:
                if remaining_points >= 0:
                    st.success(f"**💎 차감 후 포인트:** {remaining_points} P")
                else:
                    st.error(f"**❌ 포인트 부족:** {cost - user['points']} P 더 필요")
        
        # 다운로드 버튼
        st.markdown("---")
        
        button_col1, button_col2 = st.columns([1, 1])
        
        with button_col1:
            if cost > user['points']:
                st.error("💸 포인트가 부족합니다")
            else:
                if st.button("⬇️ 다운로드 시작", use_container_width=True, type="primary"):
                    if cost > 0:
                        success, message = point_manager.process_download_payment(
                            user['id'], file['id'], file['price']
                        )
                        if not success:
                            st.error(f"❌ {message}")
                            return
                        
                        st.success(f"✅ {message}")
                        auth.update_user_points()  # 포인트 정보 갱신
                    
                    # 실제 파일 다운로드
                    file_path = file_manager.get_file_path(file['stored_name'])
                    if file_path and file_path.exists():
                        with open(file_path, 'rb') as f:
                            file_data = f.read()
                        
                        st.download_button(
                            label=f"💾 {file['original_name']} 저장",
                            data=file_data,
                            file_name=file['original_name'],
                            mime="application/octet-stream",
                            use_container_width=True,
                            help="클릭하여 파일을 컴퓨터에 저장하세요"
                        )
                        
                        st.balloons()
                        st.success("🎉 다운로드가 완료되었습니다!")
                    else:
                        st.error("❌ 파일을 찾을 수 없습니다.")
        
        with button_col2:
            if already_downloaded:
                st.info("🔄 재다운로드는 무료입니다")
            else:
                st.caption("💡 한 번 다운로드하면 무료로 재다운 가능")

def show_ghibli_pagination(current_page, total_pages):
    """지브리 스타일 페이지네이션 컨트롤 표시"""
    if total_pages <= 1:
        return
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #C8E6C9, #A5D6A7); 
                padding: 15px; border-radius: 20px; margin: 20px 0; border: 2px solid #4CAF50;">
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
    
    with col1:
        if current_page > 1:
            if st.button("🍃 이전 숲", key="prev_page", help="이전 페이지로"):
                st.session_state.current_page = current_page - 1
                st.rerun()
    
    with col2:
        if current_page > 1:
            if st.button("🌱 첫 숲", key="first_page", help="첫 페이지로"):
                st.session_state.current_page = 1
                st.rerun()
    
    with col3:
        st.markdown(f"""
        <div style="text-align: center; color: #1B5E20; font-weight: bold; font-size: 16px;">
            🌳 {current_page} / {total_pages} 숲 🌳
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if current_page < total_pages:
            if st.button("🌲 마지막 숲", key="last_page", help="마지막 페이지로"):
                st.session_state.current_page = total_pages
                st.rerun()
    
    with col5:
        if current_page < total_pages:
            if st.button("🌿 다음 숲", key="next_page", help="다음 페이지로"):
                st.session_state.current_page = current_page + 1
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_pagination(current_page, total_pages):
    """페이지네이션 컨트롤 표시"""
    if total_pages <= 1:
        return
    
    # 중앙 정렬을 위한 컨테이너
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # 페이지 정보
        st.markdown(f"<div style='text-align: center; margin-bottom: 1rem;'>📄 {current_page} / {total_pages} 페이지</div>", 
                   unsafe_allow_html=True)
        
        # 페이지네이션 버튼들
        pagination_cols = st.columns(7)
        
        # 처음 페이지
        with pagination_cols[0]:
            if current_page > 1:
                if st.button("⏪", help="첫 페이지", key="first_page"):
                    st.session_state.current_page = 1
                    st.rerun()
        
        # 이전 페이지
        with pagination_cols[1]:
            if current_page > 1:
                if st.button("◀", help="이전 페이지", key="prev_page"):
                    st.session_state.current_page = current_page - 1
                    st.rerun()
        
        # 현재 페이지 주변 표시
        start_page = max(1, current_page - 1)
        end_page = min(total_pages, current_page + 1)
        
        page_idx = 2
        for page_num in range(start_page, end_page + 1):
            if page_idx < 5:  # 최대 3개 페이지 번호만 표시
                with pagination_cols[page_idx]:
                    if page_num == current_page:
                        st.markdown(f"<div style='text-align: center; background: #ff9800; color: white; padding: 0.5rem; border-radius: 5px; font-weight: bold;'>{page_num}</div>", 
                                   unsafe_allow_html=True)
                    else:
                        if st.button(str(page_num), key=f"page_{page_num}"):
                            st.session_state.current_page = page_num
                            st.rerun()
                page_idx += 1
        
        # 다음 페이지
        with pagination_cols[5]:
            if current_page < total_pages:
                if st.button("▶", help="다음 페이지", key="next_page"):
                    st.session_state.current_page = current_page + 1
                    st.rerun()
        
        # 마지막 페이지
        with pagination_cols[6]:
            if current_page < total_pages:
                if st.button("⏩", help="마지막 페이지", key="last_page"):
                    st.session_state.current_page = total_pages
                    st.rerun()

def show_ghibli_upload_form():
    """지브리 스타일 파일 업로드 폼 표시"""
    auth = AuthManager()
    file_manager = FileManager()
    user = auth.get_current_user()
    
    st.markdown("""
    <div style="text-align: center; background: linear-gradient(135deg, #C8E6C9, #A5D6A7); 
                padding: 20px; border-radius: 20px; border: 3px solid #4CAF50; margin: 20px 0;">
        <h2 style="color: #1B5E20; margin: 0;">🌱 새로운 나무 심기</h2>
        <p style="color: #2E7D32; margin: 10px 0;">숲에 새로운 보물을 심어보세요!</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not user:
        st.error("🚪 숲에 들어가려면 로그인이 필요해요!")
        return
    
    # 업로드 가능한 파일 형식 안내
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: #E8F5E8; padding: 15px; border-radius: 15px; border: 2px solid #81C784;">
            <h4 style="color: #2E7D32; margin: 0;">📁 허용 형식</h4>
            <p style="color: #388E3C; margin: 5px 0; font-size: 12px;">{}</p>
        </div>
        """.format(', '.join(Config.ALLOWED_EXTENSIONS)), unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: #FFE082; padding: 15px; border-radius: 15px; border: 2px solid #FFA000;">
            <h4 style="color: #E65100; margin: 0;">📏 최대 크기</h4>
            <p style="color: #EF6C00; margin: 5px 0; font-weight: bold;">{Config.MAX_FILE_SIZE_MB} MB</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: #C8E6C9; padding: 15px; border-radius: 15px; border: 2px solid #4CAF50;">
            <h4 style="color: #1B5E20; margin: 0;">🎁 보너스</h4>
            <p style="color: #2E7D32; margin: 5px 0; font-weight: bold;">{Config.UPLOAD_BONUS_POINTS} 도토리</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 파일 업로드
    uploaded_files = st.file_uploader(
        "🌟 보물 파일을 선택하세요",
        accept_multiple_files=True,
        help="여러 파일을 동시에 심을 수 있어요!"
    )
    
    if uploaded_files:
        st.markdown("🌱 심을 보물들:")
        for uploaded_file in uploaded_files:
            st.write(f"• **{uploaded_file.name}** ({file_manager.format_file_size(uploaded_file.size)})")
        
        if st.button("🌟 나무 심기 시작!", type="primary", use_container_width=True):
            success_count = 0
            
            for uploaded_file in uploaded_files:
                success, message = file_manager.save_uploaded_file(uploaded_file, user['id'])
                
                if success:
                    st.success(f"✨ {uploaded_file.name}: {message}")
                    success_count += 1
                else:
                    st.error(f"❌ {uploaded_file.name}: {message}")
            
            if success_count > 0:
                st.balloons()
                auth.update_user_points()  # 포인트 정보 갱신
                st.success(f"🎉 총 {success_count}그루의 나무를 성공적으로 심었어요!")

def show_ghibli_user_stats():
    """지브리 스타일 사용자 통계 표시"""
    auth = AuthManager()
    point_manager = PointManager()
    user = auth.get_current_user()
    
    if not user:
        st.error("🚪 숲에 들어가려면 로그인이 필요해요!")
        return
    
    st.markdown(f"""
    <div style="text-align: center; background: linear-gradient(135deg, #C8E6C9, #A5D6A7); 
                padding: 20px; border-radius: 20px; border: 3px solid #4CAF50; margin: 20px 0;">
        <h2 style="color: #1B5E20; margin: 0;">🌳 {user['username']}님의 정원</h2>
        <p style="color: #2E7D32; margin: 10px 0;">당신이 가꾼 아름다운 숲을 확인해보세요</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 통계 조회
    stats = point_manager.get_user_statistics(user['id'])
    
    # 메트릭 표시
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background: #FFE082; padding: 15px; border-radius: 20px; border: 3px solid #FFA000; text-align: center;">
            <h3 style="color: #E65100; margin: 0;">{stats['current_points']:,}</h3>
            <p style="color: #EF6C00; margin: 5px 0; font-weight: bold;">🌟 현재 도토리</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: #C8E6C9; padding: 15px; border-radius: 20px; border: 3px solid #4CAF50; text-align: center;">
            <h3 style="color: #1B5E20; margin: 0;">{stats['uploaded_count']}</h3>
            <p style="color: #2E7D32; margin: 5px 0; font-weight: bold;">🌱 심은 나무</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: #E1F5FE; padding: 15px; border-radius: 20px; border: 3px solid #03A9F4; text-align: center;">
            <h3 style="color: #0277BD; margin: 0;">{stats['downloaded_count']}</h3>
            <p style="color: #0288D1; margin: 5px 0; font-weight: bold;">🎁 수확한 보물</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="background: #F3E5F5; padding: 15px; border-radius: 20px; border: 3px solid #9C27B0; text-align: center;">
            <h3 style="color: #7B1FA2; margin: 0;">{stats['total_downloads']}</h3>
            <p style="color: #8E24AA; margin: 5px 0; font-weight: bold;">✨ 인기도</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 포인트 내역
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background: #E8F5E8; padding: 15px; border-radius: 15px; border: 2px solid #8BC34A; text-align: center;">
            <h4 style="color: #2E7D32; margin: 0;">💰 총 획득 도토리</h4>
            <h3 style="color: #1B5E20; margin: 10px 0;">+{stats['total_earned']:,}P</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: #FFF3E0; padding: 15px; border-radius: 15px; border: 2px solid #FFB74D; text-align: center;">
            <h4 style="color: #EF6C00; margin: 0;">💸 총 사용 도토리</h4>
            <h3 style="color: #E65100; margin: 10px 0;">-{stats['total_spent']:,}P</h3>
        </div>
        """, unsafe_allow_html=True)

def show_ghibli_point_management():
    """지브리 스타일 포인트 관리 페이지"""
    auth = AuthManager()
    point_manager = PointManager()
    user = auth.get_current_user()
    
    st.markdown("""
    <div style="text-align: center; background: linear-gradient(135deg, #FFE082, #FFCC02); 
                padding: 20px; border-radius: 20px; border: 3px solid #FFA000; margin: 20px 0;">
        <h2 style="color: #E65100; margin: 0;">🌟 도토리 주머니 관리</h2>
        <p style="color: #EF6C00; margin: 10px 0;">소중한 도토리들을 관리해보세요</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not user:
        st.error("🚪 숲에 들어가려면 로그인이 필요해요!")
        return
    
    # 현재 포인트 표시
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="background: #FFE082; padding: 15px; border-radius: 20px; border: 3px solid #FFA000; text-align: center;">
            <h3 style="color: #E65100; margin: 0;">{user['points']:,}P</h3>
            <p style="color: #EF6C00; margin: 5px 0; font-weight: bold;">🌟 현재 도토리</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background: #FFCDD2; padding: 15px; border-radius: 20px; border: 3px solid #F44336; text-align: center;">
            <h3 style="color: #C62828; margin: 0;">{Config.DOWNLOAD_COST_POINTS}P</h3>
            <p style="color: #D32F2F; margin: 5px 0; font-weight: bold;">💸 수확 비용</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style="background: #C8E6C9; padding: 15px; border-radius: 20px; border: 3px solid #4CAF50; text-align: center;">
            <h3 style="color: #1B5E20; margin: 0;">{Config.UPLOAD_BONUS_POINTS}P</h3>
            <p style="color: #2E7D32; margin: 5px 0; font-weight: bold;">🎁 심기 보너스</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 포인트 히스토리
    st.markdown("""
    <div style="background: linear-gradient(135deg, #E8F5E8, #C8E6C9); 
                padding: 15px; border-radius: 15px; border: 2px solid #4CAF50; margin: 20px 0;">
        <h3 style="color: #1B5E20; text-align: center; margin: 0;">📊 도토리 사용 일지</h3>
    </div>
    """, unsafe_allow_html=True)
    
    transactions, total_count = point_manager.get_point_history(user['id'])
    
    if transactions:
        for transaction in transactions:
            transaction_type = "획득" if transaction['transaction_type'] == 'earn' else "사용"
            color = "#C8E6C9" if transaction['transaction_type'] == 'earn' else "#FFCDD2"
            border_color = "#4CAF50" if transaction['transaction_type'] == 'earn' else "#F44336"
            text_color = "#1B5E20" if transaction['transaction_type'] == 'earn' else "#C62828"
            sign = "+" if transaction['transaction_type'] == 'earn' else "-"
            
            st.markdown(f"""
            <div style="background: {color}; padding: 15px; border-radius: 15px; 
                        border: 2px solid {border_color}; margin: 10px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="color: {text_color}; margin: 0;">{transaction['description']}</h4>
                        {"<p style='margin: 5px 0; font-size: 12px; color: " + text_color + ";'>파일: " + transaction['file_name'] + "</p>" if transaction['file_name'] else ""}
                    </div>
                    <div style="text-align: right;">
                        <h3 style="color: {text_color}; margin: 0;">{sign}{transaction['amount']}P</h3>
                        <p style="margin: 5px 0; font-size: 12px; color: {text_color};">{transaction['created_at']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("🌿 아직 도토리 사용 내역이 없어요!")

def show_ghibli_download_history():
    """지브리 스타일 다운로드 내역 페이지"""
    auth = AuthManager()
    point_manager = PointManager()
    user = auth.get_current_user()
    
    st.markdown("""
    <div style="text-align: center; background: linear-gradient(135deg, #E1F5FE, #B3E5FC); 
                padding: 20px; border-radius: 20px; border: 3px solid #03A9F4; margin: 20px 0;">
        <h2 style="color: #0277BD; margin: 0;">📜 보물 수집 일지</h2>
        <p style="color: #0288D1; margin: 10px 0;">지금까지 수집한 보물들을 확인해보세요</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not user:
        st.error("🚪 숲에 들어가려면 로그인이 필요해요!")
        return
    
    downloads, total_count = point_manager.get_download_history(user['id'])
    
    if downloads:
        for download in downloads:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #F1F8E9, #DCEDC8); 
                        padding: 15px; border-radius: 15px; border: 2px solid #8BC34A; margin: 10px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="color: #2E7D32; margin: 0;">🎁 {download['original_name']}</h4>
                        <p style="margin: 5px 0; font-size: 12px; color: #388E3C;">나무지기: {download['uploader_name']}</p>
                    </div>
                    <div style="text-align: right;">
                        <h4 style="color: #EF6C00; margin: 0;">{download['points_spent']}P</h4>
                        <p style="margin: 5px 0; font-size: 12px; color: #558B2F;">{download['download_at']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="text-align: center; background: #E8F5E8; padding: 15px; 
                    border-radius: 15px; border: 2px solid #81C784; margin: 20px 0;">
            <h3 style="color: #2E7D32; margin: 0;">🎉 총 {total_count}개의 보물을 수집했어요!</h3>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; background: #FFF3E0; padding: 30px; 
                    border-radius: 15px; border: 2px solid #FFB74D;">
            <h3 style="color: #EF6C00; margin: 0;">🌿 아직 수집한 보물이 없어요</h3>
            <p style="color: #F57F17; margin: 10px 0;">마을 광장에서 보물을 찾아보세요!</p>
        </div>
        """, unsafe_allow_html=True)

def show_upload_form():
    """파일 업로드 폼 표시"""
    auth = AuthManager()
    file_manager = FileManager()
    user = auth.get_current_user()
    
    st.subheader("📤 파일 업로드")
    
    if not user:
        st.error("🔐 로그인이 필요합니다.")
        return
    
    # 업로드 정보 카드
    st.markdown("""
    <div style='background: linear-gradient(135deg, #e3f2fd, #bbdefb); 
                padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem;
                border: 1px solid #90caf9;'>
    """, unsafe_allow_html=True)
    
    info_col1, info_col2 = st.columns(2)
    
    with info_col1:
        st.markdown("### 📋 업로드 규정")
        st.markdown(f"**📁 지원 형식:** {', '.join(Config.ALLOWED_EXTENSIONS[:10])}...")
        st.markdown(f"**📏 최대 크기:** {Config.MAX_FILE_SIZE_MB} MB")
        st.markdown(f"**🎁 업로드 보너스:** {Config.UPLOAD_BONUS_POINTS} 포인트")
    
    with info_col2:
        st.markdown("### 💡 이용 팁")
        st.markdown("• 여러 파일을 한 번에 업로드 가능")
        st.markdown("• 파일명은 한글/영문 모두 지원")
        st.markdown("• 업로드 시 자동으로 카테고리 분류")
        st.markdown("• 중복 업로드 시 별도 파일로 저장")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 현재 포인트 표시
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.metric("💎 현재 포인트", f"{user['points']:,} P")
    with col2:
        st.metric("📤 업로드 시 획득", f"+{Config.UPLOAD_BONUS_POINTS} P")
    with col3:
        upload_count = st.number_input("업로드할 파일 수", min_value=1, max_value=10, value=1)
        expected_points = upload_count * Config.UPLOAD_BONUS_POINTS
        st.metric("🎯 예상 획득 포인트", f"+{expected_points} P")
    
    st.markdown("---")
    
    # 파일 업로드 영역
    st.markdown("### 📂 파일 선택")
    
    uploaded_files = st.file_uploader(
        "업로드할 파일을 선택하거나 드래그하세요",
        accept_multiple_files=True,
        help="드래그 앤 드롭으로 파일을 쉽게 업로드할 수 있습니다.",
        label_visibility="collapsed"
    )
    
    if uploaded_files:
        st.markdown("### 📋 선택된 파일 목록")
        
        total_size = 0
        valid_files = []
        
        for i, uploaded_file in enumerate(uploaded_files):
            col1, col2, col3, col4 = st.columns([0.5, 2, 1, 1])
            
            file_size_mb = file_manager.get_file_size_mb(uploaded_file.size)
            total_size += file_size_mb
            
            file_icon = get_file_icon(uploaded_file.name.split('.')[-1])
            is_valid = file_manager.is_allowed_file(uploaded_file.name) and file_size_mb <= Config.MAX_FILE_SIZE_MB
            
            with col1:
                st.write(f"{i+1}")
            
            with col2:
                if is_valid:
                    st.success(f"{file_icon} {uploaded_file.name}")
                    valid_files.append(uploaded_file)
                else:
                    st.error(f"❌ {uploaded_file.name}")
                    if not file_manager.is_allowed_file(uploaded_file.name):
                        st.caption("지원하지 않는 파일 형식")
                    elif file_size_mb > Config.MAX_FILE_SIZE_MB:
                        st.caption(f"파일 크기 초과 ({file_size_mb:.1f}MB)")
            
            with col3:
                st.write(f"{file_size_mb:.1f} MB")
            
            with col4:
                if is_valid:
                    st.write(f"+{Config.UPLOAD_BONUS_POINTS}P")
                else:
                    st.write("❌")
        
        # 업로드 요약
        st.markdown("---")
        summary_col1, summary_col2, summary_col3 = st.columns(3)
        
        with summary_col1:
            st.metric("📁 총 파일 수", f"{len(uploaded_files)}개")
        with summary_col2:
            st.metric("📊 총 크기", f"{total_size:.1f} MB")
        with summary_col3:
            total_bonus = len(valid_files) * Config.UPLOAD_BONUS_POINTS
            st.metric("🎁 총 획득 포인트", f"+{total_bonus} P")
        
        # 업로드 버튼
        if valid_files:
            if st.button("🚀 업로드 시작", type="primary", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                success_count = 0
                total_files = len(valid_files)
                
                for i, uploaded_file in enumerate(valid_files):
                    progress = (i + 1) / total_files
                    progress_bar.progress(progress)
                    status_text.text(f"업로드 중... ({i+1}/{total_files}) {uploaded_file.name}")
                    
                    success, message = file_manager.save_uploaded_file(uploaded_file, user['id'])
                    
                    if success:
                        success_count += 1
                        st.success(f"✅ {uploaded_file.name}: 업로드 완료!")
                    else:
                        st.error(f"❌ {uploaded_file.name}: {message}")
                
                progress_bar.progress(1.0)
                status_text.text("업로드 완료!")
                
                if success_count > 0:
                    st.balloons()
                    auth.update_user_points()  # 포인트 정보 갱신
                    
                    # 성공 요약
                    st.success(f"""
                    🎉 **업로드 완료!**
                    
                    • 성공: {success_count}개 파일
                    • 획득 포인트: +{success_count * Config.UPLOAD_BONUS_POINTS} P
                    • 현재 포인트: {user['points'] + (success_count * Config.UPLOAD_BONUS_POINTS)} P
                    """)
                    
                    # 3초 후 페이지 새로고침
                    import time
                    time.sleep(3)
                    st.rerun()
        else:
            st.warning("업로드 가능한 파일이 없습니다.")
    
    else:
        # 드래그 앤 드롭 안내
        st.markdown("""
        <div style='border: 3px dashed #ff9800; border-radius: 15px; 
                    padding: 3rem; text-align: center; background: linear-gradient(135deg, #fff9e6, #fff3cd);
                    margin: 2rem 0;'>
            <h3 style='color: #f57c00; margin-bottom: 1rem;'>📁 파일을 여기에 드래그하세요</h3>
            <p style='color: #6c757d; font-size: 1.1rem;'>또는 위의 버튼을 클릭하여 파일을 선택하세요</p>
            <p style='color: #6c757d;'>최대 {max_size}MB까지 업로드 가능</p>
        </div>
        """.format(max_size=Config.MAX_FILE_SIZE_MB), unsafe_allow_html=True)

def show_user_stats():
    """사용자 통계 표시"""
    auth = AuthManager()
    point_manager = PointManager()
    user = auth.get_current_user()
    
    if not user:
        st.error("🔐 로그인이 필요합니다.")
        return
    
    st.subheader(f"👤 {user['username']}님의 정보")
    
    # 사용자 기본 정보 카드
    st.markdown("""
    <div style='background: linear-gradient(135deg, #e8f5e8, #c8e6c9); 
                padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem;
                border: 1px solid #a5d6a7;'>
    """, unsafe_allow_html=True)
    
    user_info_col1, user_info_col2, user_info_col3 = st.columns(3)
    
    with user_info_col1:
        st.markdown(f"**👤 사용자명:** {user['username']}")
        st.markdown(f"**📧 이메일:** {user['email']}")
    
    with user_info_col2:
        st.markdown(f"**📅 가입일:** {user['created_at'][:10]}")
        if user['last_login']:
            st.markdown(f"**🕐 마지막 로그인:** {user['last_login'][:16]}")
    
    with user_info_col3:
        st.markdown(f"**🏃 계정 상태:** {'활성' if user['is_active'] else '비활성'}")
        st.markdown(f"**💎 현재 포인트:** {user['points']:,} P")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 통계 조회
    stats = point_manager.get_user_statistics(user['id'])
    
    # 주요 통계 메트릭
    st.markdown("### 📊 활동 통계")
    
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #ffecb3, #fff9c4); 
                    padding: 1.5rem; border-radius: 12px; text-align: center;
                    border: 1px solid #fff176; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <h3 style='color: #f57f17; margin: 0;'>📤</h3>
            <h2 style='color: #f57f17; margin: 0.5rem 0;'>{}</h2>
            <p style='color: #6c757d; margin: 0;'>업로드한 파일</p>
        </div>
        """.format(stats['uploaded_count']), unsafe_allow_html=True)
    
    with metric_col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #e1f5fe, #b3e5fc); 
                    padding: 1.5rem; border-radius: 12px; text-align: center;
                    border: 1px solid #81d4fa; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <h3 style='color: #0277bd; margin: 0;'>📥</h3>
            <h2 style='color: #0277bd; margin: 0.5rem 0;'>{}</h2>
            <p style='color: #6c757d; margin: 0;'>다운로드한 파일</p>
        </div>
        """.format(stats['downloaded_count']), unsafe_allow_html=True)
    
    with metric_col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #fce4ec, #f8bbd9); 
                    padding: 1.5rem; border-radius: 12px; text-align: center;
                    border: 1px solid #f48fb1; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <h3 style='color: #c2185b; margin: 0;'>⬇️</h3>
            <h2 style='color: #c2185b; margin: 0.5rem 0;'>{}</h2>
            <p style='color: #6c757d; margin: 0;'>내 파일 다운로드 수</p>
        </div>
        """.format(stats['total_downloads']), unsafe_allow_html=True)
    
    with metric_col4:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #e8f5e8, #c8e6c9); 
                    padding: 1.5rem; border-radius: 12px; text-align: center;
                    border: 1px solid #a5d6a7; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <h3 style='color: #388e3c; margin: 0;'>💎</h3>
            <h2 style='color: #388e3c; margin: 0.5rem 0;'>{:,}</h2>
            <p style='color: #6c757d; margin: 0;'>현재 포인트</p>
        </div>
        """.format(stats['current_points']), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 포인트 내역
    st.markdown("### 💰 포인트 요약")
    
    point_col1, point_col2, point_col3 = st.columns(3)
    
    with point_col1:
        st.metric("💚 총 획득 포인트", f"+{stats['total_earned']:,} P", 
                 delta=f"평균 {stats['total_earned']//max(1,stats['uploaded_count']):.0f}P/파일" if stats['uploaded_count'] > 0 else None)
    
    with point_col2:
        st.metric("💸 총 사용 포인트", f"-{stats['total_spent']:,} P",
                 delta=f"평균 {stats['total_spent']//max(1,stats['downloaded_count']):.0f}P/파일" if stats['downloaded_count'] > 0 else None)
    
    with point_col3:
        net_points = stats['total_earned'] - stats['total_spent']
        st.metric("📈 순 포인트", f"{net_points:,} P",
                 delta="수익" if net_points > 0 else "손실" if net_points < 0 else "균형")
    
    st.markdown("---")
    
    # 레벨 시스템 (재미 요소)
    st.markdown("### 🏆 사용자 레벨")
    
    # 간단한 레벨 계산 (총 활동량 기준)
    total_activity = stats['uploaded_count'] + stats['downloaded_count']
    
    if total_activity < 5:
        level = "🥉 브론즈"
        next_level_req = 5 - total_activity
        level_desc = "웹하드를 시작한 새내기"
    elif total_activity < 20:
        level = "🥈 실버"
        next_level_req = 20 - total_activity
        level_desc = "꾸준히 활동하는 사용자"
    elif total_activity < 50:
        level = "🥇 골드"
        next_level_req = 50 - total_activity
        level_desc = "웹하드의 숙련된 사용자"
    elif total_activity < 100:
        level = "💎 다이아몬드"
        next_level_req = 100 - total_activity
        level_desc = "웹하드 전문가"
    else:
        level = "👑 마스터"
        next_level_req = 0
        level_desc = "웹하드의 신"
    
    level_col1, level_col2 = st.columns([1, 2])
    
    with level_col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #fff3e0, #ffe0b2); 
                    padding: 2rem; border-radius: 12px; text-align: center;
                    border: 1px solid #ffcc02;'>
            <h2 style='margin: 0; color: #ef6c00;'>{level}</h2>
            <p style='margin: 0.5rem 0; color: #6c757d;'>{level_desc}</p>
            <h3 style='margin: 0; color: #ef6c00;'>{total_activity} 활동</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with level_col2:
        if next_level_req > 0:
            progress = total_activity / (total_activity + next_level_req)
            st.progress(progress)
            st.write(f"다음 레벨까지 {next_level_req}개 활동이 더 필요합니다!")
        else:
            st.progress(1.0)
            st.write("🎉 최고 레벨에 도달했습니다!")
        
        # 활동 추천
        st.markdown("#### 💡 레벨업 팁")
        if stats['uploaded_count'] < stats['downloaded_count']:
            st.info("📤 파일을 더 업로드해보세요! (보너스 포인트도 받을 수 있어요)")
        elif stats['downloaded_count'] < stats['uploaded_count']:
            st.info("📥 다른 사용자의 파일도 다운로드해보세요!")
        else:
            st.success("👍 균형잡힌 활동을 하고 계시네요!")
    
    st.markdown("---")
    
    # 최근 활동 (간단한 버전)
    st.markdown("### 📝 최근 활동")
    
    recent_col1, recent_col2 = st.columns(2)
    
    with recent_col1:
        st.markdown("#### 📤 최근 업로드")
        # 여기서는 간단히 통계만 표시
        if stats['uploaded_count'] > 0:
            st.success(f"총 {stats['uploaded_count']}개 파일 업로드")
            st.info(f"총 {stats['total_downloads']}회 다운로드됨")
        else:
            st.info("아직 업로드한 파일이 없습니다")
    
    with recent_col2:
        st.markdown("#### 📥 최근 다운로드")
        if stats['downloaded_count'] > 0:
            st.success(f"총 {stats['downloaded_count']}개 파일 다운로드")
            st.info(f"총 {stats['total_spent']}P 사용")
        else:
            st.info("아직 다운로드한 파일이 없습니다")
