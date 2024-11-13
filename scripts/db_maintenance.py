#!/usr/bin/env python3
import argparse
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.db_init import init_database
from src.utils.db_manager import DBUtils

def main():
    parser = argparse.ArgumentParser(description='数据库维护工具')
    parser.add_argument('action', choices=['init', 'backup', 'restore'],
                      help='执行的操作: init(初始化), backup(备份), restore(恢复)')
    parser.add_argument('--backup-path', default='data/backup',
                      help='备份文件路径')
    
    args = parser.parse_args()
    
    if args.action == 'init':
        init_database()
    elif args.action == 'backup':
        DBUtils.backup_database(args.backup_path)
    elif args.action == 'restore':
        backup_file = os.path.join(args.backup_path, "conversations_backup.json")
        DBUtils.restore_database(backup_file)

if __name__ == "__main__":
    main() 