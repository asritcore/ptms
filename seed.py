#!/usr/bin/env python3
"""
seed_asr.py — ASR District DB Seeder
"""

import sys, os, json, bcrypt
from pathlib import Path
from datetime import date, timedelta

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.models.officer import Officer
from app.models.task import Task, TaskActivity, TaskStatus, TaskCategory, TaskPriority, ActivityType
from app.models.subtask import SubTask
from app.models.station import PoliceStation

Base.metadata.create_all(bind=engine)
db = SessionLocal()

def add_days(n): return (date.today() + timedelta(days=n)).isoformat()

print("Generating password hash...")
correct_hash = bcrypt.hashpw(b"12345678", bcrypt.gensalt(12)).decode("utf-8")

DATA_DIR  = Path(__file__).parent / "data"
hier_file = DATA_DIR / "hierarchy.json"
officers_data = json.loads(hier_file.read_text()).get("officers", [])

print("Clearing old tasks...")
db.query(TaskActivity).delete()
db.query(Task).delete()
db.commit()

print("Rebuilding officers...")
for o in officers_data:
    db.merge(Officer(
        id=o["id"],
        name=o["name"],
        rank=o["rank"],
        level=o["level"],
        report_to=o.get("report_to"),
        password_hash="file_managed"
    ))
db.commit()

print("Seeding ASR tasks...")

sample_tasks = [
    {
        "title": "Monthly Law & Order Review",
        "description": "Compile ASR district report",
        "category": TaskCategory.admin,
        "priority": TaskPriority.high,
        "assigned_by": "ASR_SP",
        "assigned_to": "ASR_ADDL_SP",
        "due_date": add_days(5),
        "status": TaskStatus.in_progress,
        "activity": [("ASR_SP", ActivityType.assigned, "Submit report")]
    },
    {
        "title": "Chintapalli Inspection",
        "description": "Inspect all circles",
        "category": TaskCategory.admin,
        "priority": TaskPriority.high,
        "assigned_by": "ASR_SP",
        "assigned_to": "ASR_DSP_CHINT",
        "due_date": add_days(7),
        "status": TaskStatus.in_progress,
        "activity": [("ASR_SP", ActivityType.assigned, "Complete inspection")]
    },
    {
        "title": "Araku Safety Plan",
        "description": "Tourist safety planning",
        "category": TaskCategory.crime,
        "priority": TaskPriority.high,
        "assigned_by": "ASR_DSP_PDR",
        "assigned_to": "ASR_CI_ARAKU",
        "due_date": add_days(5),
        "status": TaskStatus.in_progress,
        "activity": [("ASR_DSP_PDR", ActivityType.assigned, "Submit plan")]
    },
    {
        "title": "Weekly Crime Report - Mampa",
        "description": "Weekly submission",
        "category": TaskCategory.crime,
        "priority": TaskPriority.low,
        "assigned_by": "ASR_CI_KOYYURU",
        "assigned_to": "ASR_SI_MAMPA",
        "due_date": add_days(2),
        "status": TaskStatus.in_progress,
        "activity": [("ASR_CI_KOYYURU", ActivityType.assigned, "Submit Monday")]
    }
]

for td in sample_tasks:
    task = Task(
        title=td["title"],
        description=td["description"],
        category=td["category"],
        priority=td["priority"],
        assigned_by=td["assigned_by"],
        assigned_to=td["assigned_to"],
        due_date=td["due_date"],
        status=td["status"],
    )
    db.add(task)
    db.flush()

    for actor, atype, remark in td["activity"]:
        db.add(TaskActivity(task_id=task.id, actor_id=actor, action_type=atype, remark=remark))

db.commit()

print("✅ ASR seeding completed.")
db.close()
