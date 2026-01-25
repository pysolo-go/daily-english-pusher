# Twitter Monitor & Email Notification

这个项目可以监控指定推特用户（如 Donald Trump）的新推文，并将内容（包括图片）发送到你的 QQ 邮箱。

## 目录结构
- `main.py`: 主程序，负责调度任务。
- `twitter_monitor.py`: 使用 Playwright 通过 Nitter 抓取推特内容。
- `email_sender.py`: 发送邮件模块。
- `config.py`: 配置加载。
- `.env`: 环境变量配置（需自行修改）。

## 安装依赖

确保你已经安装了 Python 3.7+。

```bash
pip install -r requirements.txt
playwright install chromium
```

## 配置

1. 打开 `.env` 文件。
2. 修改以下内容：
   - `QQ_EMAIL`: 你的 QQ 邮箱地址。
   - `QQ_EMAIL_PASSWORD`: 你的 QQ 邮箱授权码（不是登录密码）。获取方式：登录 QQ 邮箱 -> 设置 -> 账户 -> POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务 -> 开启 POP3/SMTP 服务 -> 生成授权码。
   - `RECEIVER_EMAIL`: 接收通知的邮箱（默认同发送邮箱）。

## 运行

```bash
python main.py
```

## 注意事项

- 程序默认每 5 分钟检查一次（可在 `config.py` 中修改）。
- 首次运行时，会抓取最新的一条推特作为基准（如果不发送邮件，只会记录 ID）。
- 使用 Nitter 镜像站进行抓取，如果默认镜像站失效，可以在 `twitter_monitor.py` 中更新 `NITTER_INSTANCES` 列表。
