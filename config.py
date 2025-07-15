#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
from typing import Dict, Any


class Config:
    """配置管理类"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.logs_dir = self.base_dir / "logs"
        self.data_dir = self.base_dir / "data"
        
        # 创建必要的目录
        self.logs_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)
    
    # 浏览器配置
    BROWSER_CONFIG = {
        "headless": False,  # 是否无头模式
        "args": [
            '--disable-blink-features=AutomationControlled',
            '--disable-web-security',
            '--disable-features=VizDisplayCompositor',
            '--no-sandbox',
            '--disable-dev-shm-usage'
        ]
    }
    
    # 用户代理
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
    # 抖音配置
    DOUYIN_CONFIG = {
        "base_url": "https://live.douyin.com",
        "api_patterns": [
            "webcast/im/fetch",
            "webcast/im/push"
        ],
        "websocket_patterns": [
            "wss://webcast3-ws-web-lq.douyin.com"
        ]
    }
    
    # 淘宝配置
    TAOBAO_CONFIG = {
        "base_url": "https://live.taobao.com",
        "api_patterns": [
            "live.taobao.com/api/chat",
            "live.taobao.com/api/message",
            "live.taobao.com/api/comment"
        ],
        "websocket_patterns": [
            "wss://live.taobao.com"
        ]
    }
    
    # 日志配置
    LOG_CONFIG = {
        "rotation": "1 day",
        "retention": "7 days",
        "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    }
    
    # 数据保存配置
    SAVE_CONFIG = {
        "auto_save_interval": 10,  # 每10条弹幕自动保存一次
        "file_format": "json",
        "encoding": "utf-8"
    }
    
    # 网络请求配置
    NETWORK_CONFIG = {
        "timeout": 30000,  # 30秒超时
        "retry_times": 3,
        "retry_delay": 1
    }
    
    @classmethod
    def get_platform_config(cls, platform: str) -> Dict[str, Any]:
        """获取平台配置"""
        if platform == "douyin":
            return cls.DOUYIN_CONFIG
        elif platform == "taobao":
            return cls.TAOBAO_CONFIG
        else:
            raise ValueError(f"不支持的平台: {platform}")
    
    @classmethod
    def get_browser_config(cls) -> Dict[str, Any]:
        """获取浏览器配置"""
        return cls.BROWSER_CONFIG.copy()
    
    @classmethod
    def get_log_config(cls) -> Dict[str, Any]:
        """获取日志配置"""
        return cls.LOG_CONFIG.copy()
    
    @classmethod
    def get_save_config(cls) -> Dict[str, Any]:
        """获取保存配置"""
        return cls.SAVE_CONFIG.copy()
    
    @classmethod
    def get_network_config(cls) -> Dict[str, Any]:
        """获取网络配置"""
        return cls.NETWORK_CONFIG.copy()


# 全局配置实例
config = Config() 