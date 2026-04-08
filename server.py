"""
W8 分組實作：MCP Server
主題：（填入你們選的主題）

分工說明：
- 各組員在 tools/ 建立自己的 Tool，import 到這裡用 @mcp.tool() 註冊
- 指定一位組員負責 @mcp.resource()
- 指定一位組員負責 @mcp.prompt()
"""

from mcp.server.fastmcp import FastMCP
from tools.weather_tool import get_weather_data
from tools.fact_tool import get_fun_fact_data
from tools.advice_tool import get_advice_data

mcp = FastMCP("第1組-TravelAdvisor")


# ════════════════════════════════
#  Tools：各組員各自負責一個 Tool
# ════════════════════════════════

# 範例（替換成你們自己的 Tool）：
# from tools.weather_tool import get_weather_data
#
# @mcp.tool()
# def get_weather(city: str) -> str:
#     """取得指定城市的即時天氣資訊。
#     當使用者詢問天氣、溫度、是否該帶傘時使用。"""
#     return get_weather_data(city)


@mcp.tool()
def hello(name: str) -> str:
    """跟使用者打招呼。測試用，確認 MCP Server 正常運作。"""
    return f"你好，{name}！MCP Server 運作正常 🎉"


def get_trivia(topic: str = "隨機") -> str:
    """提供旅途相關的知識問答（Trivia）。
    當使用者詢問旅遊常識、旅行小知識、出國須知或想測試旅遊知識時使用。
    topic 可選：交通、安全、文化、美食、語言、隨機
    """
    valid_topics = ["交通", "安全", "文化", "美食", "語言"]
    topic_hint = topic if topic in valid_topics else "任意旅途相關"

    return (
        f"請你扮演一位旅遊達人，針對「{topic_hint}」主題，"
        f"自由發揮出一道有趣的旅途知識問答（Trivia）。\n\n"
        f"格式如下：\n"
        f"🌍【旅途知識問答 — {topic_hint}】\n\n"
        f"❓ 問題：（請自行設計一個有趣、實用的旅遊問題）\n\n"
        f"✅ 解答：（請提供清楚且知識性的解答）\n\n"
        f"請用繁體中文回答，內容要有趣、實用，讓旅人印象深刻。\n"
        f"（可選主題：{'、'.join(valid_topics)}、隨機）"
    )




@mcp.tool()
def get_activity() -> str:
    """推薦活動（透過 Bored API 取得靈感）。
    當使用者覺得無聊、想找點事情做或需要活動建議時使用。
    """
    import httpx

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

        return (
            f"🎯【活動推薦】\n\n"
            f"💡 建議：{activity}\n"
            f"🏷️ 類型：{category_zh}\n"
            f"👥 人數：{participants} 人\n"
            f"💰 花費：{price_msg}\n\n"
            f"這是一個不錯的點子，試試看吧！✨"
        )
    except Exception as e:
        return f"暫時無法取得活動建議，請稍後再試。 (錯誤: {str(e)})"


# ════════════════════════════════
#  Resource：提供靜態參考資料
#  URI 格式：info://名稱 或 docs://名稱
# ════════════════════════════════

# 範例（替換成符合你們主題的內容）：
#
# @mcp.resource("info://tips")
# def get_tips() -> str:
#     """（主題）的實用小提示"""
#     return (
#         "實用小提示：\n"
#         "- 提示 1\n"
#         "- 提示 2\n"
#         "- 提示 3"
#     )


# ════════════════════════════════
#  Prompt：整合多個 Tool 的提示詞模板
#  使用者透過 /use <名稱> [參數] 呼叫
# ════════════════════════════════

# 範例（替換成符合你們主題的內容）：
#
# @mcp.prompt()
# def my_plan(topic: str) -> str:
#     """產生（主題）計畫的提示詞"""
#     return (
#         f"請幫我規劃關於 {topic} 的計畫：\n"
#         f"1. 先使用相關工具取得資訊\n"
#         f"2. 根據資訊提供 3 個具體建議\n"
#         f"3. 附上一則笑話或建議讓我開心\n"
#         f"請用繁體中文回答。"
#     )


if __name__ == "__main__":
    mcp.run()
