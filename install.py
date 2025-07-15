#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
import os
from pathlib import Path


def run_command(command: str, description: str = ""):
    """运行命令并显示进度"""
    if description:
        print(f"正在{description}...")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description}完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description}失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False


def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("错误: 需要Python 3.8或更高版本")
        return False
    print(f"✓ Python版本: {sys.version}")
    return True


def install_dependencies():
    """安装依赖包"""
    print("\n=== 安装依赖包 ===")
    
    # 升级pip
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "升级pip"):
        return False
    
    # 安装依赖
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "安装依赖包"):
        return False
    
    return True


def install_playwright_browsers():
    """安装Playwright浏览器"""
    print("\n=== 安装Playwright浏览器 ===")
    
    if not run_command(f"{sys.executable} -m playwright install chromium", "安装Chromium浏览器"):
        return False
    
    return True


def create_directories():
    """创建必要的目录"""
    print("\n=== 创建目录结构 ===")
    
    directories = ["logs", "data", "output"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ 创建目录: {directory}")
    
    return True


def test_installation():
    """测试安装"""
    print("\n=== 测试安装 ===")
    
    try:
        import playwright
        import loguru
        import requests
        print("✓ 所有依赖包导入成功")
        return True
    except ImportError as e:
        print(f"✗ 依赖包导入失败: {e}")
        return False


def main():
    """主安装函数"""
    print("=== 直播间弹幕抓取工具安装程序 ===\n")
    
    # 检查Python版本
    if not check_python_version():
        return False
    
    # 安装依赖
    if not install_dependencies():
        return False
    
    # 安装Playwright浏览器
    if not install_playwright_browsers():
        return False
    
    # 创建目录
    if not create_directories():
        return False
    
    # 测试安装
    if not test_installation():
        return False
    
    print("\n=== 安装完成 ===")
    print("现在你可以使用以下命令开始抓取弹幕:")
    print("\n抖音直播间:")
    print("python douyin_crawler.py --room_id <直播间ID>")
    print("\n淘宝直播间:")
    print("python taobao_crawler.py --room_id <直播间ID>")
    print("\n示例:")
    print("python example.py --platform douyin --room_id 123456789")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 