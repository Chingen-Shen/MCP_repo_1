# MCP Server + AI agent 分組實作

> 課程：AI Agent 開發 — MCP（Model Context Protocol）
> 主題：旅遊顧問 MCP Server

## Server 功能總覽

> 說明這個 MCP Server 提供哪些 Tool

| Tool 名稱                 | 功能說明     | 負責組員 |
| ------------------------- | ------------ | -------- |
|  weather_tool             | 查詢即時天氣   |  沈靖恩   |
|  fact_tool                | 旅途趣味冷知識 |  沈靖恩   |
|  advice_tool              | 旅行前的人生建議 |  沈靖恩   |
|  get_activity_tool        | 推薦活動      |  黃柏豪   |
|  get_trivia_tool          | 旅途知識問答   |  黃柏豪   |
|  web_search_tool          | 搜尋景點、美食 |  黃柏豪   |


---

## 組員與分工

| 姓名 | 負責功能            | 檔案          | 使用的 API |
| ---- | ------------------- | ------------- | ---------- |
| 沈靖恩 | 查詢即時天氣         | `tools/weather_tool.py`    |  "https://wttr.in/{city}?format=j1" |
| 沈靖恩 | 旅途趣味冷知識       | `tools/fact_tool.py`     | "https://uselessfacts.jsph.pl/api/v2/facts/random" |
| 沈靖恩 | 旅行前的人生建議      | `tools/advice_tool.py`    |  "	https://api.adviceslip.com/advice" |
| 黃柏豪 | 推薦活動            | `tools/get_activity_tool.py`    |  "https://bored-api.appbrewery.com/random" |
| 黃柏豪 | 旅途知識問答         | `tools/get_trivia_tool.py`    |  "https://opentdb.com/api.php?amount=1" |
| 黃柏豪 | 搜尋景點、美食       | `tools/web_search_tool.py`    |  "duckduckgo-search" |
| 黃柏豪 | Resource + Prompt  | `server.py` | —         |
| 黃柏豪 | Agent（用 AI 產生）  | `agent.py`  | Gemini API |

---

## 專案架構

```
├── server.py              # MCP Server 主程式
├── agent.py               # MCP Client + Gemini Agent（用 AI 產生）
├── check_models.py
├── tools/
│   ├── __init__.py
│   ├── example_tool.py    # 範例（可刪除）
│   ├── advice_tool.py     # 沈靖恩 的 Tool
│   ├── fact_tool.py       # 沈靖恩 的 Tool
│   ├── get_activity_tool.py    # 黃柏豪 的 Tool
│   ├── get_trivia_tool.py      # 黃柏豪 的 Tool
│   ├── weather_tool.py         # 沈靖恩 的 Tool
│   └── web_search_tool.py      # 黃柏豪 的 Tool
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 使用方式

```bash
# 1. 建立虛擬環境
python3 -m venv .venv
source .venv/bin/activate

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 設定 API Key
cp .env.example .env
# 編輯 .env，填入你的 GEMINI_API_KEY

# 4. 用 MCP Inspector 測試 Server
mcp dev server.py

# 5. 用 Agent 對話
python agent.py
```

---

## 測試結果

### MCP Inspector 截圖

> 貼上 Inspector 的截圖（Tools / Resources / Prompts 三個分頁都要有）

<img width="1440" height="900" alt="截圖 2026-04-09 22 28 19" src="https://github.com/user-attachments/assets/6101801b-7a6c-47bf-8901-dc76d597af0c" />

<img width="1440" height="900" alt="截圖 2026-04-09 22 29 44" src="https://github.com/user-attachments/assets/4cebef7e-1379-4e38-baf3-82c44b173a92" />

<img width="1440" height="900" alt="截圖 2026-04-09 22 30 21" src="https://github.com/user-attachments/assets/cb7bb1e3-3bc8-42ed-83e0-b78378080013" />

<img width="1440" height="900" alt="截圖 2026-04-09 22 31 22" src="https://github.com/user-attachments/assets/a0924e78-3321-4288-9010-8c96ca166a77" />

<img width="1440" height="900" alt="截圖 2026-04-09 22 31 32" src="https://github.com/user-attachments/assets/22c3386d-1b32-49de-9ce4-f6c04539d9a2" />


### Agent 對話截圖

> 貼上 Agent 對話的截圖（顯示 Gemini 呼叫 Tool 的過程，以及使用 /use 呼叫 Prompt 的結果）

---

## 各 Tool 說明

### `advice_tool`（負責：沈靖恩）

- **功能**：旅行前的人生建議
- **使用 API**：https://api.adviceslip.com/advice
- **參數**：
- **回傳範例**：

```python
import requests

def get_advice_data() -> str:
    """旅行前的人生建議。"""
    try:
        url = "https://api.adviceslip.com/advice"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return f"🌟 給您的旅行建議：\n{data['slip']['advice']}"
    except Exception as e:
        return f"無法獲取建議：{str(e)}"
```

### `fact_tool`（負責：沈靖恩）

- **功能**：旅途趣味冷知識
- **使用 API**：https://uselessfacts.jsph.pl/api/v2/facts/random	
- **參數**：
- **回傳範例**：

```python
import requests

def get_fun_fact_data() -> str:
    """旅途趣味冷知識。"""
    try:
        url = "https://uselessfacts.jsph.pl/api/v2/facts/random"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return f"💡 旅途冷知識：\n{data['text']}"
    except Exception as e:
        return f"無法獲取冷知識：{str(e)}"
```

  

### `get_activity_tool`（負責：黃柏豪）

- **功能**：推薦活動
- **使用 API**：https://bored-api.appbrewery.com/random	
- **參數**：String city
- **回傳範例**：

```python
"""
Tool：取得當地活動

輸入地點的關鍵字後，會回傳一系列的活動建議。
"""

import httpx

TOOL_INFO = {
    "name": "get_activity",
    "api": "https://bored-api.appbrewery.com/random",
    "author": "黃柏豪",
}

def get_activity_data(city: str = None) -> str:
    """推薦活動（透過 Bored API 取得靈感）。
    當使用者覺得無聊、想找點事情做或需要活動建議時使用。
    """
    url = "https://bored-api.appbrewery.com/random"
    try:
        # 設定較短的 timeout 避免阻塞
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        data = response.json()

        activity = data.get("activity", "找不到活動內容")
        category = data.get("type", "其他")
        participants = data.get("participants", 1)
        price_range = data.get("price", 0)

        # 簡單的活動類別對應表
        type_map = {
            "education": "📚 教育學習",
            "recreational": "🎾 休閒娛樂",
            "social": "👯 社交活動",
            "diy": "🛠️ 手作 DIY",
            "charity": "💖 公益慈善",
            "cooking": "🍳 烹飪美食",
            "relaxation": "🧘 放鬆身心",
            "music": "🎵 音樂藝術",
            "busywork": "📋 規律事務",
        }
        category_zh = type_map.get(category, category)

        # 價格描述
        price_msg = "💎 免費" if price_range == 0 else "💳 付費活動" if price_range > 0.5 else "🪙 低花費"

        city_prefix = f"在 {city} " if city else ""
        return (
            f"🎯【活動推薦】\n\n"
            f"💡 建議：{city_prefix}{activity}\n"
            f"🏷️ 類型：{category_zh}\n"
            f"👥 人數：{participants} 人\n"
            f"💰 花費：{price_msg}\n\n"
            f"這是一個不錯的點子，試試看吧！✨"
        )
    except Exception as e:
        return f"暫時無法取得活動建議，請稍後再試。 (錯誤: {str(e)})"

```

### `get_trivia_tool`（負責：黃柏豪）

- **功能**：旅途知識問答
- **使用 API**：https://opentdb.com/api.php?amount=1	
- **參數**：
- **回傳範例**：

```python
import requests

# Tool 資訊（給人看的，不影響 MCP）
TOOL_INFO = {
    "name": "get_trivia",
    "api": "https://opentdb.com/api.php?amount=1&category=22",
    "author": "黃柏豪",
}

def get_trivia_data() -> str:
    """旅途知識問答（從 OpenTDB 獲取真實題目）。
    當使用者想玩問答遊戲、測試旅遊或地理常識時使用。
    """
    import httpx
    import html
    import random

    # OpenTDB API, category 22 是地理 (Geography)，適合旅途主題
    url = "https://opentdb.com/api.php?amount=1&category=22"
    
    try:
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        data = response.json()

        if data.get("response_code") != 0:
            return "暫時找不到題目，請稍後再試。"

        result = data["results"][0]
        question = html.unescape(result["question"])
        correct_answer = html.unescape(result["correct_answer"])
        incorrect_answers = [html.unescape(ans) for ans in result["incorrect_answers"]]
        category = html.unescape(result["category"])
        difficulty = result["difficulty"].capitalize()

        # 組合所有選項並打散
        options = incorrect_answers + [correct_answer]
        random.shuffle(options)

        options_str = "\n".join([f"- {opt}" for opt in options])

        return (
            f"🌍【旅途知識問答 — {category}】\n"
            f"標籤：{difficulty}\n\n"
            f"❓ 問題：{question}\n\n"
            f"💡 選項：\n{options_str}\n\n"
            f"請想好答案後，問我正確解答！"
        )
    except Exception as e:
        return f"連線到題庫時發生錯誤：{str(e)}"
```
### `weather_tool`（負責：沈靖恩）

- **功能**：查詢目的地天氣
- **使用 API**：https://wttr.in/{city}?format=j1	
- **參數**：
- **回傳範例**：

```python
import requests

def get_weather_data(city: str) -> str:
    """取得指定城市的即時天氣資訊。"""
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        current = data['current_condition'][0]
        temp_c = current['temp_C']
        desc = current['weatherDesc'][0]['value']
        humidity = current['humidity']
        
        return f"📍 {city} 的當前天氣：\n🌡️ 溫度：{temp_c}°C\n🌤️ 況狀：{desc}\n💧 濕度：{humidity}%"
    except Exception as e:
        return f"無法取得天氣資訊：{str(e)}"
```
### `web_search_tool`（負責：黃柏豪）

- **功能**：搜尋景點、美食
- **使用 API**：duckduckgo-search	
- **參數**：String query
- **回傳範例**：

```python
import requests
from ddgs import DDGS
import logging

# 設定小型日誌
logger = logging.getLogger(__name__)

def web_search_data(query: str) -> str:
    """即時搜尋網路資訊（搜尋景點、美食、天氣等）。
    當使用者需要最新的旅遊動態、在地美食評論或各國景點資訊時使用。
    """
    try:
        results = []
        # 使用 DDGS 進行網路搜尋
        with DDGS() as ddgs:
            # max_results=5 取得前 5 筆結果
            # 可以根據需求設定 region，例如 'wt-wt' (全球) 或 'tw-tzh' (台灣)
            for r in ddgs.text(query, max_results=5):
                title = r.get('title', '無標題')
                href = r.get('href', '#')
                body = r.get('body', '無摘要內容')
                
                results.append(
                    f"🔗 [{title}]({href})\n"
                    f"📝 {body}\n"
                )
        
        if not results:
            return f"🔍 搜尋結果：找不到關於「{query}」的相關內容。請嘗試更換關鍵字再試一次。"

        content = "\n---\n".join(results)
        return (
            f"🔍 【網路搜尋結果：{query}】\n\n"
            f"{content}\n\n"
            f"---\n"
            f"*資訊來自 DuckDuckGo 搜尋*"
        )
        
    except Exception as e:
        logger.error(f"Web search error: {str(e)}")
        return f"⚠️ 搜尋時發生錯誤，請稍後再試。 (詳細資訊: {str(e)})"
```

---

## 心得

### 遇到最難的問題

> 寫下這次實作遇到最困難的事，以及怎麼解決的
> 沈靖恩覺得最困難的就是ai一直跑啊跑，說了一大堆問題，然後說自己會解決，但是跑了三百年都沒解決。
> 最後的解法就是，沈靖恩在乾瞪程式碼之後決定問老師。
> 後來發現沒辦法connect的原因是程式碼的網址和mcp inspector的不一樣 並且transport type選錯了，更改之後，他就能正常connect了！！

### MCP 跟上週的 Tool Calling 有什麼不同？

> 用自己的話說說，做完後你覺得 MCP 的好處是什麼
