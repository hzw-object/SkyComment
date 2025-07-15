#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import requests
from urllib.parse import urlparse, parse_qs
from typing import Optional, Tuple


def extract_room_id_from_url(url: str, platform: str) -> Optional[str]:
    """从直播间URL中提取直播间ID"""
    try:
        if platform == "douyin":
            return _extract_douyin_room_id(url)
        elif platform == "taobao":
            return _extract_taobao_room_id(url)
        else:
            raise ValueError(f"不支持的平台: {platform}")
    except Exception as e:
        print(f"提取直播间ID失败: {e}")
        return None


def _extract_douyin_room_id(url: str) -> Optional[str]:
    """提取抖音直播间ID"""
    # 抖音直播间URL模式
    patterns = [
        r'live\.douyin\.com/(\d+)',  # https://live.douyin.com/123456789
        r'live\.douyin\.com/([a-zA-Z0-9]+)',  # https://live.douyin.com/abc123
        r'douyin\.com/(\d+)',  # https://www.douyin.com/123456789
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


def _extract_taobao_room_id(url: str) -> Optional[str]:
    """提取淘宝直播间ID"""
    # 淘宝直播间URL模式
    patterns = [
        r'live\.taobao\.com/live/(\d+)',  # https://live.taobao.com/live/123456789
        r'live\.taobao\.com/(\d+)',  # https://live.taobao.com/123456789
        r'live\.taobao\.com/live/([a-zA-Z0-9]+)',  # https://live.taobao.com/live/abc123
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


def validate_room_id(room_id: str, platform: str) -> bool:
    """验证直播间ID格式"""
    if platform == "douyin":
        # 抖音直播间ID通常是数字或字母数字组合
        return bool(re.match(r'^[a-zA-Z0-9]+$', room_id))
    elif platform == "taobao":
        # 淘宝直播间ID通常是数字
        return bool(re.match(r'^\d+$', room_id))
    else:
        return False


def get_room_info(room_id: str, platform: str) -> Optional[dict]:
    """获取直播间信息"""
    try:
        if platform == "douyin":
            return _get_douyin_room_info(room_id)
        elif platform == "taobao":
            return _get_taobao_room_info(room_id)
        else:
            raise ValueError(f"不支持的平台: {platform}")
    except Exception as e:
        print(f"获取直播间信息失败: {e}")
        return None


def _get_douyin_room_info(room_id: str) -> Optional[dict]:
    """获取抖音直播间信息"""
    try:
        url = f"https://live.douyin.com/{room_id}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            # 这里可以解析页面内容获取直播间信息
            # 由于抖音有反爬机制，这里只是示例
            return {
                "room_id": room_id,
                "platform": "douyin",
                "url": url,
                "status": "available"
            }
    except Exception as e:
        print(f"获取抖音直播间信息失败: {e}")
    
    return None


def _get_taobao_room_info(room_id: str) -> Optional[dict]:
    """获取淘宝直播间信息"""
    try:
        url = f"https://live.taobao.com/live/{room_id}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            # 这里可以解析页面内容获取直播间信息
            return {
                "room_id": room_id,
                "platform": "taobao",
                "url": url,
                "status": "available"
            }
    except Exception as e:
        print(f"获取淘宝直播间信息失败: {e}")
    
    return None


def parse_live_url(url: str) -> Tuple[Optional[str], Optional[str]]:
    """解析直播间URL，返回平台和直播间ID"""
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        
        if "douyin" in domain:
            room_id = _extract_douyin_room_id(url)
            return "douyin", room_id
        elif "taobao" in domain:
            room_id = _extract_taobao_room_id(url)
            return "taobao", room_id
        else:
            return None, None
    except Exception as e:
        print(f"解析直播间URL失败: {e}")
        return None, None


def format_output_filename(platform: str, room_id: str, extension: str = "json") -> str:
    """格式化输出文件名"""
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{platform}_{room_id}_{timestamp}.{extension}"


if __name__ == "__main__":
    # 测试函数
    test_urls = [
        "https://live.douyin.com/123456789",
        "https://live.taobao.com/live/987654321",
        "https://www.douyin.com/abc123",
    ]
    
    for url in test_urls:
        platform, room_id = parse_live_url(url)
        if platform and room_id:
            print(f"URL: {url}")
            print(f"平台: {platform}")
            print(f"直播间ID: {room_id}")
            print(f"输出文件名: {format_output_filename(platform, room_id)}")
            print("-" * 50) 