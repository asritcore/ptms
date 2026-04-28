"""
migrate_deferrable.py
Alters the officers_report_to_fkey constraint to be DEFERRABLE INITIALLY DEFERRED.
Run once: python3 migrate_deferrable.py
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from sqlalchemy import text
from app.core.database import SessionLocal

db = SessionLocal()
try:
    # Drop old constraint and recreate as deferrable
    db.execute(text("""
        ALTER TABLE officers
            DROP CONSTRAINT IF EXISTS officers_report_to_fkey;
    """))
    db.execute(text("""
        ALTER TABLE officers
            ADD CONSTRAINT officers_report_to_fkey
            FOREIGN KEY (report_to) REFERENCES officers(id)
            DEFERRABLE INITIALLY DEFERRED;
    """))
    db.commit()
    print("✅ officers_report_to_fkey is now DEFERRABLE INITIALLY DEFERRED")
except Exception as e:
    db.rollback()
    print(f"❌ Error: {e}")
finally:
    db.close()
