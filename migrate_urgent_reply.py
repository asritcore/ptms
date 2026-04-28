"""
migrate_urgent_reply.py
Adds urgent_reply column to the tasks table.
Run ONCE after updating the code.
Usage: python3 migrate_urgent_reply.py
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.core.database import SessionLocal

db = SessionLocal()
try:
    db.execute(text("""
        ALTER TABLE tasks
        ADD COLUMN IF NOT EXISTS urgent_reply VARCHAR(5) DEFAULT NULL
    """))
    db.commit()
    print("✅ urgent_reply column added to tasks table.")
    print("   Now restart the backend.")
except Exception as e:
    db.rollback()
    print(f"❌ Error: {e}")
finally:
    db.close()
