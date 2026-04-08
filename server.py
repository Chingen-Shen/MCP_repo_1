"""
W8 分組實作：MCP Server
主題：（填入你們選的主題）

分工說明：
- 各組員在 tools/ 建立自己的 Tool，import 到這裡用 @mcp.tool() 註冊
- 指定一位組員負責 @mcp.resource()
- 指定一位組員負責 @mcp.prompt()
"""

from mcp.server.fastmcp import FastMCP
from tools.get_activity_tool import get_activity_data
from tools.get_trivia_tool import get_trivia_data
from tools.weather_tool import get_weather_data
from tools.fact_tool import get_fun_fact_data
from tools.advice_tool import get_advice_data

mcp = FastMCP("第1組-TravelAdvisor")


# ════════════════════════════════
#  Tools：各組員各自負責一個 Tool
# ════════════════════════════════

@mcp.tool()
def get_weather(city: str) -> str:
    """取得指定城市的即時天氣資訊。當使用者詢問天氣、溫度時使用。"""
    return get_weather_data(city)

@mcp.tool()
def get_activity(city: str = None) -> str:
    """推薦旅行中的休閒活動內容。可指定城市。"""
    return get_activity_data(city)

@mcp.tool()
def get_trivia(topic: str = "隨機") -> str:
    """提供旅途相關的知識問答（Trivia）。
    topic 可選：交通、安全、文化、美食、語言、隨機
    """
    return get_trivia_data(topic)

@mcp.tool()
def get_fun_fact() -> str:
    """旅途趣味冷知識。"""
    return get_fun_fact_data()

@mcp.tool()
def get_advice() -> str:
    """旅行前的人生建議。"""
    return get_advice_data()

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
