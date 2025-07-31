#!/usr/bin/env python3
"""
LEVIS Stocktake Dashboard Runner
Launch the interactive dashboard from the project root.

Usage:
    python run_dashboard.py
"""

import sys
import os
import subprocess

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    print("🚀 Launching LEVIS Stocktake Analysis Dashboard...")
    print("📊 Dashboard will open in your browser at: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the dashboard")
    print()
    
    try:
        # Run the dashboard
        subprocess.run(["streamlit", "run", "src/dashboard.py"])
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"\n❌ Error launching dashboard: {e}")
        print("Make sure Streamlit is installed: pip install streamlit") 