# 直播间弹幕抓取工具

使用 Python Playwright 实现抖音直播间和淘宝直播间弹幕抓取功能。

## 功能特性

- 支持抖音直播间弹幕抓取
- 支持淘宝直播间弹幕抓取
- 实时弹幕数据获取
- 数据保存到JSON文件
- 详细的日志记录
- 自动重试和错误处理
- 支持无头模式运行

## 快速开始

### 1. 安装依赖

运行自动安装脚本：

```bash
python install.py
```

或者手动安装：

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. 获取直播间ID

#### 抖音直播间
- 打开抖音直播间页面
- 从URL中获取直播间ID，例如：`https://live.douyin.com/123456789` 中的 `123456789`

#### 淘宝直播间
- 打开淘宝直播间页面
- 从URL中获取直播间ID，例如：`https://live.taobao.com/live/987654321` 中的 `987654321`

### 3. 开始抓取

#### 使用示例脚本（推荐）

```bash
# 抓取抖音直播间弹幕
python example.py --platform douyin --room_id 123456789

# 抓取淘宝直播间弹幕
python example.py --platform taobao --room_id 987654321

# 指定输出文件
python example.py --platform douyin --room_id 123456789 --output my_comments.json
```

#### 直接使用抓取器

```bash
# 抖音直播间弹幕抓取
python douyin_crawler.py --room_id 123456789 --output douyin_comments.json

# 淘宝直播间弹幕抓取
python taobao_crawler.py --room_id 987654321 --output taobao_comments.json
```

## 输出格式

弹幕数据以JSON格式保存，包含以下字段：

```json
[
  {
    "timestamp": "2024-01-01T12:00:00",
    "user": "用户名",
    "content": "弹幕内容",
    "type": "chat",
    "platform": "douyin",
    "room_id": "123456789"
  }
]
```

## 项目结构

```
bullet-playwright/
├── douyin_crawler.py      # 抖音弹幕抓取器
├── taobao_crawler.py      # 淘宝弹幕抓取器
├── base_crawler.py        # 基础抓取器类
├── config.py              # 配置文件
├── utils.py               # 工具函数
├── example.py             # 示例脚本
├── install.py             # 安装脚本
├── requirements.txt       # 依赖包列表
├── README.md             # 说明文档
├── logs/                 # 日志目录
├── data/                 # 数据目录
└── output/               # 输出目录
```

## 配置选项

可以通过修改 `config.py` 文件来调整各种设置：

- 浏览器配置（无头模式、用户代理等）
- 网络请求超时时间
- 自动保存间隔
- 日志配置

## 注意事项

- 需要确保网络连接正常
- 直播间ID需要从直播间URL中获取
- 建议使用代理以避免IP限制
- 某些直播间可能有反爬虫机制，需要手动处理
- 程序运行时会打开浏览器窗口，可以设置为无头模式

## 故障排除

### 常见问题

1. **无法获取弹幕数据**
   - 检查直播间是否正在直播
   - 确认直播间ID是否正确
   - 尝试刷新页面或重新启动程序

2. **浏览器启动失败**
   - 确保已安装Playwright浏览器：`playwright install chromium`
   - 检查系统是否有足够的权限

3. **网络连接问题**
   - 检查网络连接
   - 尝试使用代理
   - 检查防火墙设置

### 日志查看

程序运行时会生成详细的日志文件，位于 `logs/` 目录下：

```bash
# 查看抖音抓取日志
tail -f logs/douyin_123456789.log

# 查看淘宝抓取日志
tail -f logs/taobao_987654321.log
```

## 开发说明

### 添加新平台支持

1. 继承 `BaseCrawler` 类
2. 实现抽象方法：
   - `_get_live_room_url()`
   - `_extract_comments_from_response()`
   - `_extract_comments_from_websocket()`
3. 在 `config.py` 中添加平台配置

### 自定义数据处理

可以修改 `_extract_comments_from_response()` 和 `_extract_comments_from_websocket()` 方法来适应不同平台的数据格式。

## 许可证

本项目仅供学习和研究使用，请遵守相关平台的使用条款。 