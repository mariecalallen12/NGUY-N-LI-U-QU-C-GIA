#!/usr/bin/env python3
"""
Script tính toán tỷ lệ hoàn thiện dự án dựa trên checklist
"""

import re
import sys
from pathlib import Path
from typing import Dict, Tuple

# Exit codes
EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_INCOMPLETE = 2

def count_checklist_items(content: str) -> Tuple[int, int]:
    """
    Đếm số items trong checklist và số items đã hoàn thành
    
    Args:
        content: Nội dung file markdown
        
    Returns:
        Tuple (tổng số items, số items hoàn thành)
    """
    # Pattern cho unchecked item: - [ ]
    unchecked_pattern = r'^\s*-\s*\[\s*\]\s*.+'
    # Pattern cho checked item: - [x] hoặc - [X]
    checked_pattern = r'^\s*-\s*\[[xX]\]\s*.+'
    
    unchecked_items = len(re.findall(unchecked_pattern, content, re.MULTILINE))
    checked_items = len(re.findall(checked_pattern, content, re.MULTILINE))
    
    total_items = unchecked_items + checked_items
    
    return total_items, checked_items

def calculate_completion_rate(total: int, completed: int) -> float:
    """
    Tính tỷ lệ hoàn thiện
    
    Args:
        total: Tổng số items
        completed: Số items đã hoàn thành
        
    Returns:
        Tỷ lệ hoàn thiện (%)
    """
    if total == 0:
        return 0.0
    return (completed / total) * 100

def analyze_checklist(file_path: Path) -> Dict:
    """
    Phân tích file checklist
    
    Args:
        file_path: Đường dẫn đến file checklist
        
    Returns:
        Dictionary chứa thông tin phân tích
    """
    if not file_path.exists():
        return {
            'error': f'File không tồn tại: {file_path}'
        }
    
    content = file_path.read_text(encoding='utf-8')
    total, completed = count_checklist_items(content)
    completion_rate = calculate_completion_rate(total, completed)
    
    return {
        'file': str(file_path),
        'total_items': total,
        'completed_items': completed,
        'pending_items': total - completed,
        'completion_rate': completion_rate
    }

def get_completion_status(rate: float) -> str:
    """
    Lấy trạng thái dựa trên tỷ lệ hoàn thiện
    
    Args:
        rate: Tỷ lệ hoàn thiện (%)
        
    Returns:
        Trạng thái (string)
    """
    if rate == 100:
        return '✅ Hoàn thiện đầy đủ'
    elif rate >= 80:
        return '🟡 Gần hoàn thiện'
    elif rate >= 60:
        return '🟠 Đã phát triển cơ bản'
    else:
        return '🔴 Chưa đầy đủ'

def print_report(analysis: Dict):
    """
    In báo cáo phân tích
    
    Args:
        analysis: Dictionary chứa kết quả phân tích
    """
    if 'error' in analysis:
        print(f"❌ Lỗi: {analysis['error']}")
        return
    
    print("=" * 70)
    print("BÁO CÁO TỶ LẸ HOÀN THIỆN DỰ ÁN")
    print("=" * 70)
    print(f"\nFile phân tích: {analysis['file']}")
    print(f"\nTổng số items: {analysis['total_items']}")
    print(f"Items đã hoàn thành: {analysis['completed_items']}")
    print(f"Items còn lại: {analysis['pending_items']}")
    print(f"\nTỷ lệ hoàn thiện: {analysis['completion_rate']:.2f}%")
    print(f"Trạng thái: {get_completion_status(analysis['completion_rate'])}")
    print("\n" + "=" * 70)
    
    # Đề xuất hành động
    print("\nĐỀ XUẤT HÀNH ĐỘNG:")
    rate = analysis['completion_rate']
    
    if rate == 100:
        print("✓ Dự án đã hoàn thiện, chuyển sang giai đoạn đánh giá chất lượng")
    elif rate >= 80:
        print("✓ Tập trung hoàn thiện các items còn lại")
        print("✓ Review và test các features đã implement")
    elif rate >= 60:
        print("✓ Ưu tiên phát triển các features quan trọng còn thiếu")
        print("✓ Thiết lập CI/CD nếu chưa có")
    else:
        print("✓ Cần phát triển thêm nhiều components")
        print("✓ Xem xét lại timeline và resources")
        print("✓ Có thể cần support thêm từ team")
    
    print("=" * 70)

def main():
    """Main function"""
    # Xác định đường dẫn đến file checklist
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    checklist_file = repo_root / 'docs' / 'checklists' / 'CHECKLIST.md'
    
    # Cho phép override file path từ command line
    if len(sys.argv) > 1:
        checklist_file = Path(sys.argv[1])
    
    # Phân tích và in báo cáo
    analysis = analyze_checklist(checklist_file)
    print_report(analysis)
    
    # Exit code dựa trên completion rate
    if 'error' in analysis:
        sys.exit(EXIT_ERROR)
    elif analysis['completion_rate'] < 100:
        sys.exit(EXIT_INCOMPLETE)  # Chưa hoàn thiện 100%
    else:
        sys.exit(EXIT_SUCCESS)  # Hoàn thiện 100%

if __name__ == '__main__':
    main()
