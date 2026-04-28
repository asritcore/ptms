@echo off
:: ── PTMS Setup Script (Windows) ───────────────────────────────────
:: Run ONCE on a fresh machine: Double-click setup.bat
:: ──────────────────────────────────────────────────────────────────

echo.
echo ==============================================
echo   PTMS -- ASR District Police -- Setup
echo ==============================================

cd /d "%~dp0backend"

:: 1. Write .env for Windows PostgreSQL (TCP connection)
echo.
echo 1. Writing .env configuration...
(
echo DATABASE_URL=postgresql://ptms_user:ptms_pass@localhost:5432/ptms_db
echo SECRET_KEY=ptms-anm-district-secret-key-2025
echo ALGORITHM=HS256
echo ACCESS_TOKEN_EXPIRE_MINUTES=480
) > .env
echo    [OK] .env written

:: 2. Remind user to create database in pgAdmin
echo.
echo 2. PostgreSQL Database Setup
echo    Open pgAdmin, connect to PostgreSQL, open Query Tool and run:
echo.
echo      CREATE USER ptms_user WITH PASSWORD 'ptms_pass';
echo      CREATE DATABASE ptms_db OWNER ptms_user;
echo      GRANT ALL PRIVILEGES ON DATABASE ptms_db TO ptms_user;
echo.
echo    Press any key after creating the database...
pause > nul

:: 3. Create virtual environment
echo.
echo 3. Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo    [ERROR] Python not found. Please install Python 3.11 and check Add to PATH.
    pause
    exit /b 1
)
echo    [OK] Virtual environment created

:: 4. Install packages
echo.
echo 4. Installing Python packages...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip -q
pip install bcrypt==4.0.1 python-dotenv==1.0.1 -q
pip install -r requirements.txt -q
echo    [OK] Packages installed

:: 5. Run migrations
echo.
echo 5. Running database migrations...
python migrate_deferrable.py
python migrate_urgent_reply.py
python migrate_v3.py
python migrate_v4.py
echo    [OK] Migrations complete

:: 6. Seed officers
echo.
echo 6. Seeding 106 ASR District officers...
python seed.py
echo    [OK] Officers seeded

:: 7. Admin account
echo.
echo 7. Creating Admin account...
python admin_setup.py
echo    [OK] Admin account ready

:: 8. Seed police stations
echo.
echo 8. Seeding 28 Police Stations with SHO mapping...
python seed_stations.py
echo    [OK] Police stations seeded

echo.
echo ==============================================
echo   [OK] Setup complete!
echo.
echo   Login credentials:
echo     Admin   : ADMIN  /  admin1234
echo     Officers: Officer ID  /  12345678
echo.
echo   To start the app every day:
echo     Double-click start.bat
echo   Then start Cloudflare tunnel:
echo     cloudflared tunnel run ptms
echo ==============================================
echo.
pause
