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


@mcp.tool()
def get_trivia() -> str:
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
