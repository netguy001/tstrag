#!/usr/bin/env python3
"""
Simple launcher - Uses existing venv, never deletes anything
Just run: python run.py
"""

import os
import subprocess
import platform

# Detect OS
is_windows = platform.system() == "Windows"

# Find Python in existing venv
if is_windows:
    python_exe = os.path.join("venv", "Scripts", "python.exe")
else:
    python_exe = os.path.join("venv", "bin", "python")

# Check venv exists
if not os.path.exists(python_exe):
    print("❌ venv not found! Please create it first.")
    exit(1)

# Run Flask app
print("🚀 Starting server at http://127.0.0.1:5001")
print("Press CTRL+C to stop\n")

try:
    subprocess.run([python_exe, "app.py"])
except KeyboardInterrupt:
    print("\n👋 Server stopped")
