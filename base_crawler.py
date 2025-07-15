#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import json
import time
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from playwright.async_api import async_playwright, Browser, Page
from loguru import logger


class BaseCrawler(ABC):
    """弹幕抓取基类"""
    
    def __init__(self, room_id: str, platform: str, output_file: str = None):
        self.room_id = room_id
        self.platform = platform
        self.output_file = output_file or f"{platform}_{room_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.comments = []
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        
        # 设置日志
        Path("logs").mkdir(exist_ok=True)
        logger.add(f"logs/{platform}_{room_id}.log", rotation="1 day", retention="7 days")
    
    @abstractmethod
    async def _get_live_room_url(self) -> str:
        """获取直播间URL"""
        pass
    
    @abstractmethod
    async def _extract_comments_from_response(self, data: Dict):
        """从API响应中提取弹幕"""
        pass
    
    @abstractmethod
    async def _extract_comments_from_websocket(self, data: Dict):
        """从WebSocket消息中提取弹幕"""
        pass
    
    async def start(self):
        """启动抓取器"""
        try:
            async with async_playwright() as p:
                # 启动浏览器
                self.browser = await p.chromium.launch(
                    headless=False,  # 设置为 True 可以无头模式运行
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-web-security',
                        '--disable-features=VizDisplayCompositor'
                    ]
                )
                
                # 创建新页面
                self.page = await self.browser.new_page()
                
                # 设置用户代理
                await self.page.set_extra_http_headers({
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                })
                
                # 访问直播间
                await self._navigate_to_live_room()
                
                # 开始监听弹幕
                await self._start_comment_monitoring()
                
        except Exception as e:
            logger.error(f"启动失败: {e}")
            raise
    
    async def _navigate_to_live_room(self):
        """导航到直播间"""
        try:
            live_url = await self._get_live_room_url()
            logger.info(f"正在访问直播间: {live_url}")
            
            # 访问直播间
            await self.page.goto(live_url, wait_until="networkidle")
            
            # 等待页面加载
            await asyncio.sleep(5)
            
            # 检查是否成功进入直播间
            await self._check_live_room_status()
            
        except Exception as e:
            logger.error(f"导航到直播间失败: {e}")
            raise
    
    async def _check_live_room_status(self):
        """检查直播间状态"""
        try:
            # 检查是否存在直播结束提示
            end_text = await self.page.query_selector('text=直播已结束')
            if end_text:
                logger.warning("直播间已结束")
                return False
            
            logger.info("直播间加载成功")
            return True
            
        except Exception as e:
            logger.error(f"检查直播间状态失败: {e}")
            return False
    
    async def _start_comment_monitoring(self):
        """开始监听弹幕"""
        logger.info("开始监听弹幕...")
        
        try:
            # 监听网络请求，获取弹幕数据
            await self.page.route("**/*", self._handle_network_request)
            
            # 监听页面消息
            await self.page.on("websocket", self._handle_websocket)
            
            # 持续运行
            while True:
                await asyncio.sleep(1)
                
                # 定期保存数据
                if len(self.comments) % 10 == 0 and self.comments:
                    await self._save_comments()
                
        except KeyboardInterrupt:
            logger.info("收到中断信号，正在停止...")
        except Exception as e:
            logger.error(f"监听弹幕时发生错误: {e}")
        finally:
            await self._cleanup()
    
    async def _handle_network_request(self, route):
        """处理网络请求，提取弹幕数据"""
        try:
            request = route.request
            
            # 检查是否是弹幕相关的API请求
            if self._is_chat_api_request(request.url):
                response = await route.fetch()
                
                if response.ok:
                    try:
                        data = await response.json()
                        await self._extract_comments_from_response(data)
                    except json.JSONDecodeError:
                        pass
                        
            await route.continue_()
            
        except Exception as e:
            logger.error(f"处理网络请求失败: {e}")
            await route.continue_()
    
    def _is_chat_api_request(self, url: str) -> bool:
        """检查是否是聊天API请求"""
        chat_keywords = [
            "chat", "message", "comment", "im", "push", "fetch"
        ]
        return any(keyword in url.lower() for keyword in chat_keywords)
    
    async def _handle_websocket(self, websocket):
        """处理WebSocket连接"""
        logger.info(f"WebSocket连接: {websocket.url}")
        
        async def handle_message(msg):
            try:
                if msg.type == "text":
                    data = json.loads(msg.text)
                    await self._extract_comments_from_websocket(data)
            except Exception as e:
                logger.error(f"处理WebSocket消息失败: {e}")
        
        websocket.on("framesent", handle_message)
        websocket.on("framereceived", handle_message)
    
    async def _save_comments(self):
        """保存弹幕数据"""
        try:
            # 确保输出目录存在
            output_path = Path(self.output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 保存为JSON格式
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(self.comments, f, ensure_ascii=False, indent=2)
            
            logger.info(f"已保存 {len(self.comments)} 条弹幕到 {self.output_file}")
            
        except Exception as e:
            logger.error(f"保存弹幕失败: {e}")
    
    async def _cleanup(self):
        """清理资源"""
        try:
            if self.page:
                await self.page.close()
            if self.browser:
                await self.browser.close()
            
            # 最终保存
            await self._save_comments()
            logger.info("清理完成")
            
        except Exception as e:
            logger.error(f"清理失败: {e}")
    
    def add_comment(self, user: str, content: str, comment_type: str = "chat"):
        """添加弹幕"""
        comment = {
            "timestamp": datetime.now().isoformat(),
            "user": user,
            "content": content,
            "type": comment_type,
            "platform": self.platform,
            "room_id": self.room_id
        }
        self.comments.append(comment)
        logger.info(f"弹幕: {user}: {content}") 