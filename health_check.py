import os
import shutil
import psutil
from datetime import datetime, timedelta

BACKUP_DIR = 'Backups'


def check_memory():
    mem = psutil.virtual_memory()
    used_pct = mem.percent
    if used_pct < 75:
        status = 'OK'
    elif used_pct < 90:
        status = 'WARNING'
    else:
        status = 'ERROR'
    return {'used_percent': used_pct, 'status': status}


def check_disk():
    usage = shutil.disk_usage('/')
    used_pct = int(usage.used / usage.total * 100)
    status = 'OK' if used_pct < 85 else 'WARNING'
    return {'used_percent': used_pct, 'status': status}


def check_backups():
    if not os.path.isdir(BACKUP_DIR):
        return {'exists': False, 'latest': None, 'status': 'unhealthy'}
    files = [os.path.join(BACKUP_DIR, f) for f in os.listdir(BACKUP_DIR) if f.startswith('backup_')]
    if not files:
        return {'exists': True, 'latest': None, 'status': 'degraded'}
    latest = max(files, key=os.path.getmtime)
    age = datetime.utcnow() - datetime.utcfromtimestamp(os.path.getmtime(latest))
    status = 'healthy' if age < timedelta(days=1) else 'degraded'
    return {'exists': True, 'latest': os.path.basename(latest), 'age_seconds': int(age.total_seconds()), 'status': status}


def check_db():
    # En este laboratorio la DB puede ser un sqlite en data/
    db_dir = 'data'
    if os.path.isdir(db_dir) and any(db_dir for _ in os.listdir(db_dir)):
        return {'connected': True, 'status': 'healthy'}
    else:
        return {'connected': False, 'status': 'degraded'}


def run_all_checks():
    mem = check_memory()
    disk = check_disk()
    backups = check_backups()
    db = check_db()

    overall = 'healthy'
    if mem['status'] == 'ERROR' or disk['status'] == 'WARNING' or backups['status'] == 'unhealthy' or db['status'] == 'degraded':
        overall = 'degraded'
    return {
        'status': overall,
        'checks': {
            'memory': mem,
            'disk': disk,
            'backups': backups,
            'database': db
        }
    }

if __name__ == '__main__':
    import json
    print(json.dumps(run_all_checks(), indent=2))
