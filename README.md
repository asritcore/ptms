# PTMS — Police Task Management System
## ASR (Alluri SeethaRama Raju) District Police — Windows Version

---

## Quick Start (First Time)

1. Install Python 3.11 — https://www.python.org/downloads/windows
   - ✅ CHECK "Add Python to PATH" during install

2. Install PostgreSQL 16 — https://www.enterprisedb.com/downloads/postgres-postgresql-installer
   - Create database using pgAdmin (see Installation Guide)

3. Install Cloudflare Tunnel — see Installation Guide Section 5

4. Double-click `setup.bat` — follow on-screen instructions

---

## Daily Use

| Action | Command |
|--------|---------|
| Start app | Double-click `start.bat` |
| Start Cloudflare | `cloudflared tunnel run ptms` in new cmd window |

---

## URLs

- **Local**: http://localhost:8000
- **Live**: https://asrptms.org (or your district URL)

---

## Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `ADMIN` | `admin1234` |
| Officers | Officer ID | `12345678` |

---

## Ports

| App | Port |
|-----|------|
| PTMS | 8000 |

---

## Database

| Setting | Value |
|---------|-------|
| Host | localhost |
| Port | 5432 |
| Database | ptms_db |
| User | ptms_user |
| Password | ptms_pass |

---

## File Structure

```
ptms\
├── setup.bat           ← Run once during installation
├── start.bat           ← Run every day to start app
├── README.md
└── backend\
    ├── .env            ← Created by setup.bat
    ├── app\            ← FastAPI application
    ├── data\           ← Officer hierarchy data
    ├── index.html      ← Frontend
    ├── requirements.txt
    ├── seed.py
    ├── migrate_v4.py
    └── venv\           ← Created by setup.bat
```

---

## Backup Database

```bat
pg_dump -U ptms_user -h localhost ptms_db > C:\ptms_backup.sql
```

## Restore Database

```bat
psql -U ptms_user -h localhost ptms_db < C:\ptms_backup.sql
```

---

## Troubleshooting

**Python not found**
```
Reinstall Python and check "Add to PATH"
```

**PostgreSQL connection error**
```
Open Services → find postgresql-x64-16 → Start
```

**Port 8000 in use**
```
Task Manager → Details → find python.exe → End Task
```
