"""
admin_setup.py
Run once after first install to create the ADMIN account.
Usage: python admin_setup.py
"""
import sys, os, bcrypt, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pathlib import Path
from app.core.database import SessionLocal, engine, Base
from app.models.task import Task, TaskActivity
from app.models.officer import Officer

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Add ADMIN to DB
admin = db.query(Officer).filter(Officer.id == 'ADMIN').first()
if not admin:
    db.add(Officer(
        id='ADMIN', name='System Admin', rank='Admin',
        level=99, report_to=None, password_hash='file_managed',
    ))
    db.commit()
    print('ADMIN added to database ✓')
else:
    print('ADMIN already in database ✓')
db.close()

# Add ADMIN to passwords.json
pw_file = Path(__file__).parent / 'data' / 'passwords.json'
data = {}
if pw_file.exists():
    data = json.loads(pw_file.read_text())
data['ADMIN'] = bcrypt.hashpw(b'admin1234', bcrypt.gensalt(12)).decode()
pw_file.write_text(json.dumps(data, indent=2))
print('ADMIN password set → admin1234 ✓')
print('\nDone. Login with: ADMIN / admin1234')
