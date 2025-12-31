# 如何获取免费/高性价比的 API Key？

对于学习者，我强烈推荐以下几种获取方式。大部分都有免费额度，足够你完成本教程的学习。

## 1. 硅基流动 (SiliconFlow) - **强烈推荐**
聚合了 DeepSeek、Qwen (通义千问)、Llama 3 等主流开源模型，注册通常会赠送大量额度（如 14元-20元不等，够用很久）。

- **费用**：注册即送额度，部分模型（如 Qwen-7B）甚至永久免费。
- **注册地址**：[https://cloud.siliconflow.cn/](https://cloud.siliconflow.cn/)
- **配置方式** (.env)：
  ```ini
  OPENAI_API_KEY=sk-xxxx (在控制台创建)
  OPENAI_BASE_URL=https://api.siliconflow.cn/v1
  ```
- **优势**：速度快，兼容 OpenAI SDK，不用魔法。

## 2. DeepSeek (深度求索) - **官方**
目前最强的国产模型之一，性价比极高（GPT-4 级别的能力，1% 的价格）。

- **费用**：注册通常赠送 10元 - 500万 tokens（相当多）。即使花钱也很便宜。
- **注册地址**：[https://platform.deepseek.com/](https://platform.deepseek.com/)
- **配置方式** (.env)：
  ```ini
  OPENAI_API_KEY=sk-xxxx
  OPENAI_BASE_URL=https://api.deepseek.com
  ```

## 3. Moonshot AI (Kimi)
国内体验很好的长文本模型。

- **费用**：注册送 15元 左右额度。
- **注册地址**：[https://platform.moonshot.cn/](https://platform.moonshot.cn/)
- **配置方式** (.env)：
  ```ini
  OPENAI_API_KEY=sk-xxxx
  OPENAI_BASE_URL=https://api.moonshot.cn/v1
  ```

## 4. Ollama (本地运行) - **完全免费**
利用你自己的电脑算力运行模型。如果你是 Mac (M1/M2/M3)，体验会非常好。

- **费用**：0元。
- **安装**：
  1. 访问 [https://ollama.com/](https://ollama.com/) 下载安装。
  2. 终端运行：`ollama run llama3` 或 `ollama run qwen2`。
- **配置方式** (.env)：
  ```ini
  OPENAI_API_KEY=ollama (随便填)
  OPENAI_BASE_URL=http://localhost:11434/v1
  ```

---

## 建议
先去 **硅基流动 (SiliconFlow)** 注册一个账号，拿免费额度跑通代码。这是最快、最稳的白嫖方式。
