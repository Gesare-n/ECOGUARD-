@echo off
echo Acoustic Guardian - Simulation Setup
echo ==================================

echo Installing required Python packages...
pip install -r requirements.txt

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Update the configuration values in simulate_sensor.py
echo 2. Run the simulation: python simulate_sensor.py
echo.