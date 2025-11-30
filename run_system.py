#!/usr/bin/env python3
"""
Startup script to run both FastAPI backend and Streamlit frontend
"""
import subprocess
import sys
import time
import os
from threading import Thread

def run_fastapi():
    """Run the FastAPI backend"""
    print("Starting FastAPI backend...")
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\nFastAPI backend stopped.")
    except Exception as e:
        print(f"Error running FastAPI: {e}")

def run_streamlit():
    """Run the Streamlit frontend"""
    print("Starting Streamlit frontend...")
    try:
        # Change to frontend directory and run streamlit
        os.chdir("frontend")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\nStreamlit frontend stopped.")
    except Exception as e:
        print(f"Error running Streamlit: {e}")

def main():
    """Main function to run both services"""
    print("RAG System with Authentication - Startup Script")
    print("=" * 50)
    
    # Check if required files exist
    if not os.path.exists("app.py"):
        print("Error: app.py not found. Make sure you're in the correct directory.")
        return
    
    if not os.path.exists("frontend/app.py"):
        print("Error: frontend/app.py not found. Make sure the frontend directory exists.")
        return
    
    print("Starting both FastAPI backend and Streamlit frontend...")
    print("FastAPI will run on: http://localhost:8000")
    print("Streamlit will run on: http://localhost:8501")
    print("\nPress Ctrl+C to stop both services")
    print("-" * 50)
    
    # Start FastAPI in a separate thread
    fastapi_thread = Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()
    
    # Wait a moment for FastAPI to start
    time.sleep(3)
    
    # Start Streamlit (this will block until stopped)
    try:
        run_streamlit()
    except KeyboardInterrupt:
        print("\nShutting down both services...")

if __name__ == "__main__":
    main()
