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
from tools.web_search_tool import web_search_data

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
def get_weather(city: str) -> str:
    """查詢目的地的當前天氣資訊。"""
    return get_weather_data(city)


@mcp.tool()
def get_fun_fact() -> str:
    """提供一個旅途有趣的冷知識。"""
    return get_fun_fact_data()


@mcp.tool()
def get_advice() -> str:
    """提供一則旅行前的人生建議。"""
    return get_advice_data()

@mcp.tool()
def web_search(query: str) -> str:
    """即時搜尋網路資訊（搜尋景點、美食、天氣等）。
    當使用者需要最新的旅遊動態、在地美食評論或各國景點資訊時使用。
    """
    return web_search_data(query)


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
    mcp.run("sse")
