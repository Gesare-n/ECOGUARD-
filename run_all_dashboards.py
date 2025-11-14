"""
Acoustic Guardian - Run All Dashboards

Script to start all Streamlit dashboards simultaneously with proper port allocation.
"""

import subprocess
import sys
import time
import os

def run_all_dashboards():
    """Run all Streamlit dashboards simultaneously with proper port allocation."""
    
    print("🌳 Acoustic Guardian - Starting All Dashboards")
    print("=" * 50)
    
    # Dashboard configurations with ports
    dashboards = [
        {"name": "Main Dashboard", "file": "streamlit_dashboard.py", "port": 8501},
        {"name": "Institutional Dashboard", "file": "institutional_dashboard.py", "port": 8502},
        {"name": "Policy Dashboard", "file": "policy_dashboard.py", "port": 8503},
        {"name": "Research Dashboard", "file": "research_dashboard.py", "port": 8504},
        {"name": "Nairobi Dashboard", "file": "nairobi_dashboard.py", "port": 8505},
        {"name": "Deforestation Analysis", "file": "deforestation_analysis.py", "port": 8506},
        {"name": "Super User Dashboard", "file": "super_user_dashboard.py", "port": 8507}
    ]
    
    processes = []
    
    try:
        # Start each dashboard
        for dashboard in dashboards:
            if os.path.exists(dashboard["file"]):
                print(f"Starting {dashboard['name']} on port {dashboard['port']}...")
                cmd = [
                    sys.executable, "-m", "streamlit", "run",
                    dashboard["file"],
                    "--server.port", str(dashboard["port"]),
                    "--server.headless", "true"
                ]
                
                # Start process in background
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                processes.append({
                    "process": process,
                    "name": dashboard["name"],
                    "port": dashboard["port"]
                })
                
                # Small delay between starts
                time.sleep(2)
            else:
                print(f"Warning: {dashboard['file']} not found")
        
        print("\n✅ All dashboards started successfully!")
        print("\n📍 Access your dashboards at:")
        for dashboard in dashboards:
            if os.path.exists(dashboard["file"]):
                print(f"   http://localhost:{dashboard['port']} - {dashboard['name']}")
        
        print("\n🔄 Refresh this script to restart dashboards")
        print("❌ Press Ctrl+C to stop all dashboards")
        
        # Wait for all processes
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping all dashboards...")
            for p in processes:
                p["process"].terminate()
            print("✅ All dashboards stopped.")
            
    except Exception as e:
        print(f"❌ Error starting dashboards: {e}")
        # Clean up any started processes
        for p in processes:
            try:
                p["process"].terminate()
            except:
                pass

if __name__ == "__main__":
    run_all_dashboards()