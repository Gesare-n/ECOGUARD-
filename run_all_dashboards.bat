@echo off
echo Starting EcoGuard Streamlit Dashboards...
echo.

cd /d D:\AcousticGuardian

echo Starting Main Dashboard on port 8501...
start "Main Dashboard" python -m streamlit run streamlit_dashboard.py --server.port 8501

timeout /t 2 /nobreak >nul

echo Starting Institutional Dashboard on port 8502...
start "Institutional Dashboard" python -m streamlit run institutional_dashboard.py --server.port 8502

timeout /t 2 /nobreak >nul

echo Starting Policy Dashboard on port 8503...
start "Policy Dashboard" python -m streamlit run policy_dashboard.py --server.port 8503

timeout /t 2 /nobreak >nul

echo Starting Research Dashboard on port 8504...
start "Research Dashboard" python -m streamlit run research_dashboard.py --server.port 8504

timeout /t 2 /nobreak >nul

echo Starting Nairobi Dashboard on port 8505...
start "Nairobi Dashboard" python -m streamlit run nairobi_dashboard.py --server.port 8505

timeout /t 2 /nobreak >nul

echo Starting Enhanced Dashboard on port 8506...
start "Enhanced Dashboard" python -m streamlit run enhanced_dashboard.py --server.port 8506

timeout /t 2 /nobreak >nul

echo Starting Super User Dashboard on port 8507...
start "Super User Dashboard" python -m streamlit run super_user_dashboard.py --server.port 8507

echo.
echo All dashboards started successfully!
echo.
echo Main Dashboard: http://localhost:8501
echo Institutional Dashboard: http://localhost:8502
echo Policy Dashboard: http://localhost:8503
echo Research Dashboard: http://localhost:8504
echo Nairobi Dashboard: http://localhost:8505
echo Enhanced Dashboard: http://localhost:8506
echo Super User Dashboard: http://localhost:8507
echo.
pause