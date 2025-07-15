#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import argparse
from pathlib import Path

from douyin_crawler import DouyinCrawler
from taobao_crawler import TaobaoCrawler


async def run_douyin_crawler(room_id: str, output_file: str = None):
    """运行抖音弹幕抓取器"""
    print(f"开始抓取抖音直播间 {room_id} 的弹幕...")
    
    crawler = DouyinCrawler(room_id, output_file)
    await crawler.start()


async def run_taobao_crawler(room_id: str, output_file: str = None):
    """运行淘宝弹幕抓取器"""
    print(f"开始抓取淘宝直播间 {room_id} 的弹幕...")
    
    crawler = TaobaoCrawler(room_id, output_file)
    await crawler.start()


async def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="直播间弹幕抓取示例")
    parser.add_argument("--platform", choices=["douyin", "taobao"], required=True, help="平台选择")
    parser.add_argument("--room_id", required=True, help="直播间ID")
    parser.add_argument("--output", help="输出文件路径")
    
    args = parser.parse_args()
    
    # 创建日志目录
    Path("logs").mkdir(exist_ok=True)
    
    try:
        if args.platform == "douyin":
            await run_douyin_crawler(args.room_id, args.output)
        elif args.platform == "taobao":
            await run_taobao_crawler(args.room_id, args.output)
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序运行出错: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 