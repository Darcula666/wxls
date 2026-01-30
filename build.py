#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键打包脚本 - 支持 macOS、Windows、Linux

用法:
    python build.py              # 打包当前平台
    python build.py macos        # 打包 macOS
    python build.py windows      # 打包 Windows
    python build.py linux        # 打包 Linux
    python build.py ci           # 生成 GitHub Actions 工作流

示例:
    python build.py macos        # 打包 macOS
    python build.py windows      # 打包 Windows
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
    """获取当前平台"""
    if sys.platform == "darwin":
        return "macos"
    elif sys.platform == "win32":
        return "windows"
    elif sys.platform.startswith("linux"):
        return "linux"
    else:
        return "unknown"


def clean_build():
    """清理构建目录"""
    dirs_to_clean = ["build", "dist"]
    for d in dirs_to_clean:
        if os.path.exists(d):
            print(f"清理目录: {d}")
            shutil.rmtree(d)


def get_icon_cmd():
    """获取图标参数"""
    if os.path.exists(ICON_FILE):
        return ["-i", ICON_FILE]
    return []


def build_macos():
    """打包 macOS (.app)"""
    print("\n=== 打包 macOS ===")

    clean_build()

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "-F",           # 单文件
        "-w",           # 无控制台窗口
        "--osx-bundle-identifier", "com.wxls.analyzer",
    ]
    cmd.extend(get_icon_cmd())
    cmd.extend(["--clean", PYTHON_FILE])

    result = subprocess.run(cmd)
    if result.returncode == 0:
        exe_path = f"dist/{APP_NAME}"
        if os.path.exists(exe_path):
            print(f"✓ macOS 打包成功: {exe_path}")
    else:
        print("✗ macOS 打包失败")
        return False
    return True


def build_windows():
    """打包 Windows"""
    print("\n=== 打包 Windows ===")

    clean_build()

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "-F",           # 单文件
        "-w",           # 无控制台窗口
    ]
    cmd.extend(get_icon_cmd())
    cmd.extend(["--clean", PYTHON_FILE])

    result = subprocess.run(cmd)
    if result.returncode == 0:
        exe_path = f"dist/{APP_NAME}.exe"
        if os.path.exists(exe_path):
            print(f"✓ Windows 打包成功: {exe_path}")
        else:
            print("✓ 打包完成（请检查 dist 目录）")
    else:
        print("✗ Windows 打包失败")
        return False
    return True


def build_linux():
    """打包 Linux"""
    print("\n=== 打包 Linux ===")

    clean_build()

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "-F",           # 单文件
        "-w",           # 无控制台窗口
    ]
    cmd.extend(get_icon_cmd())
    cmd.extend(["--clean", PYTHON_FILE])

    result = subprocess.run(cmd)
    if result.returncode == 0:
        exe_path = f"dist/{APP_NAME}"
        if os.path.exists(exe_path):
            print(f"✓ Linux 打包成功: {exe_path}")
    else:
        print("✗ Linux 打包失败")
        return False
    return True


def generate_github_workflow():
    """生成 GitHub Actions 工作流文件"""
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

    print(f"✓ GitHub Actions 工作流已生成: {workflow_path}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="一键打包脚本 - 支持 macOS、Windows、Linux"
    )
    parser.add_argument(
        "platform",
        nargs="?",
        choices=["macos", "windows", "linux", "ci"],
        default=get_platform(),
        help="指定打包平台 (默认: 当前平台)",
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
        print(f"不支持的平台: {args.platform}")


if __name__ == "__main__":
    main()
