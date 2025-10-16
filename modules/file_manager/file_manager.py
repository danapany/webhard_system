import os
import uuid
import shutil
import mimetypes
from pathlib import Path
from datetime import datetime
import sqlite3
from config.settings import Config
from database.models import db

class FileManager:
    def __init__(self):
        self.upload_path = Path(Config.UPLOAD_PATH)
        self.upload_path.mkdir(parents=True, exist_ok=True)
        
    def get_file_category(self, file_extension):
        """파일 확장자로 카테고리 결정"""
        ext = file_extension.lower().lstrip('.')
        return Config.FILE_TYPE_MAPPING.get(ext, 'other')
    
    def is_allowed_file(self, filename):
        """허용된 파일 타입인지 확인"""
        if not filename:
            return False
        
        ext = filename.rsplit('.', 1)[-1].lower()
        return ext in Config.ALLOWED_EXTENSIONS
    
    def get_file_size_mb(self, file_size):
        """파일 크기를 MB 단위로 변환"""
        return file_size / (1024 * 1024)
    
    def save_uploaded_file(self, uploaded_file, uploader_id):
        """업로드된 파일을 저장하고 데이터베이스에 정보 기록"""
        if not self.is_allowed_file(uploaded_file.name):
            return False, "허용되지 않는 파일 형식입니다."
        
        file_size_mb = self.get_file_size_mb(uploaded_file.size)
        if file_size_mb > Config.MAX_FILE_SIZE_MB:
            return False, f"파일 크기가 {Config.MAX_FILE_SIZE_MB}MB를 초과합니다."
        
        try:
            # 고유한 파일명 생성
            file_uuid = str(uuid.uuid4())
            file_extension = Path(uploaded_file.name).suffix
            stored_name = f"{file_uuid}{file_extension}"
            stored_path = self.upload_path / stored_name
            
            # 파일 저장
            with open(stored_path, "wb") as f:
                f.write(uploaded_file.read())
            
            # 파일 카테고리 결정
            category = self.get_file_category(file_extension)
            
            # 데이터베이스에 파일 정보 저장
            file_id = self._save_file_to_db(
                file_uuid=file_uuid,
                original_name=uploaded_file.name,
                stored_name=stored_name,
                file_size=uploaded_file.size,
                file_type=file_extension.lstrip('.'),
                category=category,
                uploader_id=uploader_id
            )
            
            if file_id:
                # 업로드 보너스 포인트 지급
                self._add_upload_bonus_points(uploader_id, file_id)
                return True, f"파일이 성공적으로 업로드되었습니다! (+{Config.UPLOAD_BONUS_POINTS} 포인트)"
            else:
                # 데이터베이스 저장 실패 시 파일 삭제
                stored_path.unlink()
                return False, "데이터베이스 오류가 발생했습니다."
                
        except Exception as e:
            return False, f"파일 업로드 중 오류가 발생했습니다: {str(e)}"
    
    def _save_file_to_db(self, file_uuid, original_name, stored_name, file_size, file_type, category, uploader_id):
        """파일 정보를 데이터베이스에 저장"""
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO files (file_uuid, original_name, stored_name, file_size, 
                                 file_type, category, uploader_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (file_uuid, original_name, stored_name, file_size, file_type, category, uploader_id))
            
            file_id = cursor.lastrowid
            conn.commit()
            return file_id
        except Exception as e:
            conn.rollback()
            return None
        finally:
            conn.close()
    
    def _add_upload_bonus_points(self, user_id, file_id):
        """업로드 보너스 포인트 지급"""
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            # 사용자 포인트 업데이트
            cursor.execute('''
                UPDATE users SET points = points + ? WHERE id = ?
            ''', (Config.UPLOAD_BONUS_POINTS, user_id))
            
            # 포인트 트랜잭션 기록
            cursor.execute('''
                INSERT INTO point_transactions (user_id, transaction_type, amount, description, file_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, 'earn', Config.UPLOAD_BONUS_POINTS, '파일 업로드 보너스', file_id))
            
            conn.commit()
        except Exception as e:
            conn.rollback()
        finally:
            conn.close()
    
    def get_files_list(self, category='all', search_query='', limit=20, offset=0):
        """파일 목록 조회"""
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # 기본 쿼리
        query = '''
            SELECT f.*, u.username as uploader_name 
            FROM files f 
            JOIN users u ON f.uploader_id = u.id 
            WHERE f.is_active = 1
        '''
        params = []
        
        # 카테고리 필터
        if category != 'all':
            query += ' AND f.category = ?'
            params.append(category)
        
        # 검색 필터
        if search_query:
            query += ' AND f.original_name LIKE ?'
            params.append(f'%{search_query}%')
        
        # 정렬 및 페이징
        query += ' ORDER BY f.created_at DESC LIMIT ? OFFSET ?'
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        files = cursor.fetchall()
        
        # 전체 개수 조회
        count_query = '''
            SELECT COUNT(*) as total
            FROM files f 
            WHERE f.is_active = 1
        '''
        count_params = []
        
        if category != 'all':
            count_query += ' AND f.category = ?'
            count_params.append(category)
        
        if search_query:
            count_query += ' AND f.original_name LIKE ?'
            count_params.append(f'%{search_query}%')
        
        cursor.execute(count_query, count_params)
        total_count = cursor.fetchone()['total']
        
        conn.close()
        
        return [dict(file) for file in files], total_count
    
    def get_file_by_uuid(self, file_uuid):
        """UUID로 파일 정보 조회"""
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT f.*, u.username as uploader_name 
            FROM files f 
            JOIN users u ON f.uploader_id = u.id 
            WHERE f.file_uuid = ? AND f.is_active = 1
        ''', (file_uuid,))
        
        file = cursor.fetchone()
        conn.close()
        
        return dict(file) if file else None
    
    def get_file_path(self, stored_name):
        """저장된 파일의 실제 경로 반환"""
        file_path = self.upload_path / stored_name
        return file_path if file_path.exists() else None
    
    def format_file_size(self, size_bytes):
        """파일 크기를 사람이 읽기 쉬운 형태로 포맷"""
        if size_bytes == 0:
            return "0B"
        
        size_names = ["B", "KB", "MB", "GB"]
        size = size_bytes
        unit = 0
        
        while size >= 1024 and unit < len(size_names) - 1:
            size /= 1024.0
            unit += 1
        
        return f"{size:.1f}{size_names[unit]}"
    
    def delete_file(self, file_uuid, user_id):
        """파일 삭제 (업로더만 가능)"""
        file_info = self.get_file_by_uuid(file_uuid)
        
        if not file_info:
            return False, "파일을 찾을 수 없습니다."
        
        if file_info['uploader_id'] != user_id:
            return False, "파일을 삭제할 권한이 없습니다."
        
        try:
            # 실제 파일 삭제
            file_path = self.get_file_path(file_info['stored_name'])
            if file_path and file_path.exists():
                file_path.unlink()
            
            # 데이터베이스에서 비활성화
            conn = db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE files SET is_active = 0 WHERE file_uuid = ?
            ''', (file_uuid,))
            
            conn.commit()
            conn.close()
            
            return True, "파일이 삭제되었습니다."
            
        except Exception as e:
            return False, f"파일 삭제 중 오류가 발생했습니다: {str(e)}"
