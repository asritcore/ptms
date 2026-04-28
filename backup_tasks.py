#!/usr/bin/env python3
"""
backup_tasks.py — Windows version
Saves task backup to Desktop\PTMS\Backups\
Schedule via Task Scheduler (see README)
"""
import sys, os, csv
from datetime import datetime
from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

try:
    from app.core.database import SessionLocal
    from app.models.task import Task
    from app.models.officer import Officer
    from app.models.subtask import SubTask
    from app.models.station import PoliceStation
except Exception as e:
    print(f"ERROR: {e}"); sys.exit(1)

# Save to Windows Desktop\PTMS\Backups\
BACKUP_DIR = Path.home() / "Desktop" / "PTMS" / "Backups"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

today    = datetime.now().strftime('%Y-%m-%d')
filename = BACKUP_DIR / f"PTMS_Tasks_{today}.csv"

db = SessionLocal()
try:
    tasks    = db.query(Task).all()
    officers = {o.id: o for o in db.query(Officer).all()}
    def oname(oid):
        o = officers.get(oid)
        return f"{o.rank} {o.name}" if o else oid

    rows = []
    for t in tasks:
        rows.append({
            'Task ID':         t.id,
            'Title':           t.title,
            'Description':     t.description or '',
            'Category':        t.category.value if hasattr(t.category,'value') else str(t.category),
            'Priority':        t.priority.value if hasattr(t.priority,'value') else str(t.priority),
            'Status':          t.status.value   if hasattr(t.status,'value')   else str(t.status),
            'Urgent Reply':    t.urgent_reply or '',
            'Due Date':        str(t.due_date) if t.due_date else '',
            'Assigned By ID':  t.assigned_by,
            'Assigned By':     oname(t.assigned_by),
            'Assigned To ID':  t.assigned_to,
            'Assigned To':     oname(t.assigned_to),
            'Created At':      str(t.created_at)[:19] if t.created_at else '',
        })

    if not rows:
        print("No tasks found — backup skipped"); sys.exit(0)

    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Backup saved: {filename}  ({len(rows)} tasks)")

    # Keep last 30 backups
    all_backups = sorted(BACKUP_DIR.glob("PTMS_Tasks_*.csv"))
    if len(all_backups) > 30:
        for old in all_backups[:-30]:
            old.unlink()
            print(f"  Removed old backup: {old.name}")
except Exception as e:
    print(f"ERROR: {e}"); sys.exit(1)
finally:
    db.close()
