"""
migrate_v3.py — Run once to apply v3 database changes.
Usage: python3 migrate_v3.py
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from sqlalchemy import text
from app.core.database import SessionLocal

db = SessionLocal()
migrations = [
    ("urgent_reply VARCHAR(10)",
     "ALTER TABLE tasks ALTER COLUMN urgent_reply TYPE VARCHAR(10)"),
    ("TaskCategory land_dispute",
     """DO $$ BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_enum WHERE enumlabel='Land Dispute'
            AND enumtypid=(SELECT oid FROM pg_type WHERE typname='taskcategory'))
        THEN ALTER TYPE taskcategory ADD VALUE 'Land Dispute'; END IF;
     END $$"""),
    ("ActivityType reassigned/extended/deleted",
     """DO $$ BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_enum WHERE enumlabel='reassigned'
            AND enumtypid=(SELECT oid FROM pg_type WHERE typname='activitytype'))
        THEN ALTER TYPE activitytype ADD VALUE 'reassigned'; END IF;
        IF NOT EXISTS (SELECT 1 FROM pg_enum WHERE enumlabel='extended'
            AND enumtypid=(SELECT oid FROM pg_type WHERE typname='activitytype'))
        THEN ALTER TYPE activitytype ADD VALUE 'extended'; END IF;
        IF NOT EXISTS (SELECT 1 FROM pg_enum WHERE enumlabel='deleted'
            AND enumtypid=(SELECT oid FROM pg_type WHERE typname='activitytype'))
        THEN ALTER TYPE activitytype ADD VALUE 'deleted'; END IF;
     END $$"""),
]

for name, sql in migrations:
    try:
        db.execute(text(sql))
        db.commit()
        print(f"  ✅ {name}")
    except Exception as e:
        db.rollback()
        print(f"  ⚠  {name}: {e}")

db.close()
print("\nMigration complete. Restart backend.")
