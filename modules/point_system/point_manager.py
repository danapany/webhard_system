import sqlite3
from datetime import datetime
from database.models import db
from config.settings import Config

class PointManager:
    def __init__(self):
        pass
    
    def get_user_points(self, user_id):
        """사용자의 현재 포인트 조회"""
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT points FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        
        return result['points'] if result else 0
    
    def can_afford_download(self, user_id, file_price=None):
        """다운로드 가능한 포인트가 있는지 확인"""
        if file_price is None:
            file_price = Config.DOWNLOAD_COST_POINTS
        
        user_points = self.get_user_points(user_id)
        return user_points >= file_price
    
    def process_download_payment(self, user_id, file_id, file_price=None):
        """다운로드 결제 처리"""
        if file_price is None:
            file_price = Config.DOWNLOAD_COST_POINTS
        
        if not self.can_afford_download(user_id, file_price):
            return False, "포인트가 부족합니다."
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            # 사용자 포인트 차감
            cursor.execute('''
                UPDATE users SET points = points - ? WHERE id = ?
            ''', (file_price, user_id))
            
            # 포인트 트랜잭션 기록
            cursor.execute('''
                INSERT INTO point_transactions (user_id, transaction_type, amount, description, file_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, 'spend', file_price, '파일 다운로드', file_id))
            
            # 다운로드 히스토리 기록
            cursor.execute('''
                INSERT INTO download_history (user_id, file_id, points_spent)
                VALUES (?, ?, ?)
            ''', (user_id, file_id, file_price))
            
            # 파일 다운로드 카운트 증가
            cursor.execute('''
                UPDATE files SET download_count = download_count + 1 WHERE id = ?
            ''', (file_id,))
            
            conn.commit()
            return True, f"{file_price} 포인트가 차감되었습니다."
            
        except Exception as e:
            conn.rollback()
            return False, f"결제 처리 중 오류가 발생했습니다: {str(e)}"
        finally:
            conn.close()
    
    def add_points(self, user_id, amount, description="포인트 충전"):
        """포인트 추가"""
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            # 사용자 포인트 추가
            cursor.execute('''
                UPDATE users SET points = points + ? WHERE id = ?
            ''', (amount, user_id))
            
            # 포인트 트랜잭션 기록
            cursor.execute('''
                INSERT INTO point_transactions (user_id, transaction_type, amount, description)
                VALUES (?, ?, ?, ?)
            ''', (user_id, 'earn', amount, description))
            
            conn.commit()
            return True, f"{amount} 포인트가 추가되었습니다."
            
        except Exception as e:
            conn.rollback()
            return False, f"포인트 추가 중 오류가 발생했습니다: {str(e)}"
        finally:
            conn.close()
    
    def get_point_history(self, user_id, limit=20, offset=0):
        """포인트 사용 내역 조회"""
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT pt.*, f.original_name as file_name
            FROM point_transactions pt
            LEFT JOIN files f ON pt.file_id = f.id
            WHERE pt.user_id = ?
            ORDER BY pt.created_at DESC
            LIMIT ? OFFSET ?
        ''', (user_id, limit, offset))
        
        transactions = cursor.fetchall()
        
        # 전체 개수 조회
        cursor.execute('''
            SELECT COUNT(*) as total
            FROM point_transactions
            WHERE user_id = ?
        ''', (user_id,))
        
        total_count = cursor.fetchone()['total']
        conn.close()
        
        return [dict(t) for t in transactions], total_count
    
    def get_download_history(self, user_id, limit=20, offset=0):
        """다운로드 내역 조회"""
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT dh.*, f.original_name, f.file_uuid, u.username as uploader_name
            FROM download_history dh
            JOIN files f ON dh.file_id = f.id
            JOIN users u ON f.uploader_id = u.id
            WHERE dh.user_id = ?
            ORDER BY dh.download_at DESC
            LIMIT ? OFFSET ?
        ''', (user_id, limit, offset))
        
        downloads = cursor.fetchall()
        
        # 전체 개수 조회
        cursor.execute('''
            SELECT COUNT(*) as total
            FROM download_history
            WHERE user_id = ?
        ''', (user_id,))
        
        total_count = cursor.fetchone()['total']
        conn.close()
        
        return [dict(d) for d in downloads], total_count
    
    def has_downloaded_file(self, user_id, file_id):
        """사용자가 이미 해당 파일을 다운로드했는지 확인"""
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) as count
            FROM download_history
            WHERE user_id = ? AND file_id = ?
        ''', (user_id, file_id))
        
        result = cursor.fetchone()
        conn.close()
        
        return result['count'] > 0
    
    def get_user_statistics(self, user_id):
        """사용자의 통계 정보 조회"""
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # 업로드한 파일 수
        cursor.execute('''
            SELECT COUNT(*) as uploaded_count
            FROM files
            WHERE uploader_id = ? AND is_active = 1
        ''', (user_id,))
        uploaded_count = cursor.fetchone()['uploaded_count']
        
        # 다운로드한 파일 수
        cursor.execute('''
            SELECT COUNT(*) as downloaded_count
            FROM download_history
            WHERE user_id = ?
        ''', (user_id,))
        downloaded_count = cursor.fetchone()['downloaded_count']
        
        # 업로드한 파일들의 총 다운로드 수
        cursor.execute('''
            SELECT SUM(download_count) as total_downloads
            FROM files
            WHERE uploader_id = ? AND is_active = 1
        ''', (user_id,))
        result = cursor.fetchone()
        total_downloads = result['total_downloads'] if result['total_downloads'] else 0
        
        # 총 획득 포인트
        cursor.execute('''
            SELECT SUM(amount) as total_earned
            FROM point_transactions
            WHERE user_id = ? AND transaction_type = 'earn'
        ''', (user_id,))
        result = cursor.fetchone()
        total_earned = result['total_earned'] if result['total_earned'] else 0
        
        # 총 사용 포인트
        cursor.execute('''
            SELECT SUM(amount) as total_spent
            FROM point_transactions
            WHERE user_id = ? AND transaction_type = 'spend'
        ''', (user_id,))
        result = cursor.fetchone()
        total_spent = result['total_spent'] if result['total_spent'] else 0
        
        conn.close()
        
        return {
            'uploaded_count': uploaded_count,
            'downloaded_count': downloaded_count,
            'total_downloads': total_downloads,
            'total_earned': total_earned,
            'total_spent': total_spent,
            'current_points': self.get_user_points(user_id)
        }
