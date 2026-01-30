#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script - Support macOS, Windows, Linux

Usage:
    python build.py              # Build for current platform
    python build.py macos        # Build macOS
    python build.py windows      # Build Windows
    python build.py linux        # Build Linux
    python build.py ci           # Generate GitHub Actions workflow
"""

import subprocess
import sys
import os
import shutil
import argparse

APP_NAME = "analyze_wechat_transactions"
PYTHON_FILE = f"{APP_NAME}.py"
ICON_FILE = "icon.ico"


def get_platform():
    """Get current platform"""
    if sys.platform == "darwin":
        return "macos"
    elif sys.platform == "win32":
        return "windows"
    elif sys.platform.startswith("linux"):
        return "linux"
    else:
        return "unknown"


def clean_build():
    """Clean build directories"""
    dirs_to_clean = ["build", "dist"]
    for d in dirs_to_clean:
        if os.path.exists(d):
            print(f"Cleaning directory: {d}")
            shutil.rmtree(d)


def get_icon_cmd():
    """Get icon parameter"""
    if os.path.exists(ICON_FILE):
        return ["-i", ICON_FILE]
    return []


def build_macos():
    """Build macOS (.app)"""
    print("\n=== Building macOS ===")

    clean_build()

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "-F",           # Single file
        "-w",           # No console window
        "--osx-bundle-identifier", "com.wxls.analyzer",
    ]
    cmd.extend(get_icon_cmd())
    cmd.extend(["--clean", PYTHON_FILE])

    result = subprocess.run(cmd)
    if result.returncode == 0:
        exe_path = f"dist/{APP_NAME}"
        if os.path.exists(exe_path):
            print(f"[OK] macOS build success: {exe_path}")
    else:
        print("[FAIL] macOS build failed")
        return False
    return True


def build_windows():
    """Build Windows"""
    print("\n=== Building Windows ===")

    clean_build()

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "-F",           # Single file
        "-w",           # No console window
    ]
    cmd.extend(get_icon_cmd())
    cmd.extend(["--clean", PYTHON_FILE])

    result = subprocess.run(cmd)
    if result.returncode == 0:
        exe_path = f"dist/{APP_NAME}.exe"
        if os.path.exists(exe_path):
            print(f"[OK] Windows build success: {exe_path}")
        else:
            print("[OK] Build completed (check dist directory)")
    else:
        print("[FAIL] Windows build failed")
        return False
    return True


def build_linux():
    """Build Linux"""
    print("\n=== Building Linux ===")

    clean_build()

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "-F",           # Single file
        "-w",           # No console window
    ]
    cmd.extend(get_icon_cmd())
    cmd.extend(["--clean", PYTHON_FILE])

    result = subprocess.run(cmd)
    if result.returncode == 0:
        exe_path = f"dist/{APP_NAME}"
        if os.path.exists(exe_path):
            print(f"[OK] Linux build success: {exe_path}")
    else:
        print("[FAIL] Linux build failed")
        return False
    return True


def generate_github_workflow():
    """Generate GitHub Actions workflow file"""
    workflow_dir = ".github/workflows"
    os.makedirs(workflow_dir, exist_ok=True)

    workflow = """name: Build Multi-Platform

on:
  push:
    branches: [main]
  release:
    types: [created]

jobs:
  build:
    runs-on: ${{ matrix.os }}

    strategy:
      matrix:
        os: [macos-latest, windows-latest, ubuntu-latest]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pyinstaller pyqt6 pandas matplotlib openpyxl pdfplumber

      - name: Build on macOS
        if: runner.os == 'macOS'
        run: |
          pip install pyobjc
          python build.py macos

      - name: Build on Windows
        if: runner.os == 'Windows'
        run: |
          python build.py windows

      - name: Build on Linux
        if: runner.os == 'Linux'
        run: |
          python build.py linux

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: ${{ runner.os }}-build
          path: dist/
"""

    workflow_path = os.path.join(workflow_dir, "build.yml")
    with open(workflow_path, "w", encoding="utf-8") as f:
        f.write(workflow)

    print(f"[OK] GitHub Actions workflow generated: {workflow_path}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Build script - Support macOS, Windows, Linux"
    )
    parser.add_argument(
        "platform",
        nargs="?",
        choices=["macos", "windows", "linux", "ci"],
        default=get_platform(),
        help="Target platform (default: current platform)",
    )

    args = parser.parse_args()

    if args.platform == "ci":
        generate_github_workflow()
    elif args.platform == "macos":
        build_macos()
    elif args.platform == "windows":
        build_windows()
    elif args.platform == "linux":
        build_linux()
    else:
        print(f"Unsupported platform: {args.platform}")


if __name__ == "__main__":
    main()
